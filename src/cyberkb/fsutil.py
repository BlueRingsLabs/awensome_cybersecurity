"""Filesystem access with a hostile-input threat model.

Contributor pull requests can contain symbolic links, oversized blobs and
binary data. The pipeline later runs with repository write access and an API
key in its environment, so every read of repository content goes through
:func:`read_text`, which refuses anything but a regular file that physically
lives inside the repository. Writes are atomic and skip unchanged files so
regenerating the catalog never produces spurious diffs.
"""

from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path

from cyberkb.errors import ContentRejectedError, UnsafePathError

__all__ = ["atomic_write_text", "ensure_within", "read_text", "relpath"]

_O_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)


def ensure_within(path: Path, root: Path) -> Path:
    """Return ``path`` made absolute, refusing any location outside ``root``.

    Every existing component between ``root`` and ``path`` is checked with
    ``lstat`` so a symlinked directory cannot redirect the access.

    Raises:
        UnsafePathError: when the path escapes ``root`` or traverses a symlink.
    """
    root = root.resolve()
    candidate = path if path.is_absolute() else root / path
    candidate = Path(os.path.normpath(candidate))
    try:
        rel = candidate.relative_to(root)
    except ValueError as exc:
        msg = f"{path} is outside the repository root"
        raise UnsafePathError(msg) from exc
    current = root
    for part in rel.parts:
        current = current / part
        try:
            mode = os.lstat(current).st_mode
        except FileNotFoundError:
            break
        if stat.S_ISLNK(mode):
            msg = f"{relpath(current, root)} is a symbolic link; links are not accepted"
            raise UnsafePathError(msg)
    return candidate


def relpath(path: Path, root: Path) -> str:
    """POSIX-style path of ``path`` relative to ``root`` (for messages and catalogs)."""
    return Path(os.path.relpath(path, root)).as_posix()


def read_text(path: Path, *, root: Path, max_bytes: int) -> str:
    """Read a UTF-8 text file that must be a regular, non-linked file under ``root``.

    Invalid UTF-8 sequences are replaced rather than fatal, but NUL bytes mark
    the file as binary and are rejected.

    Raises:
        UnsafePathError: symlink, outside ``root`` or not a regular file.
        ContentRejectedError: larger than ``max_bytes`` or binary.
    """
    target = ensure_within(path, root)
    try:
        fd = os.open(target, os.O_RDONLY | _O_NOFOLLOW)
    except OSError as exc:
        msg = f"cannot open {relpath(target, root)}: {exc.strerror}"
        raise UnsafePathError(msg) from exc
    # Check the kind of the open descriptor before wrapping it, so a directory
    # (which os.fdopen would reject with IsADirectoryError) is reported clearly.
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        msg = f"{relpath(target, root)} is not a regular file"
        raise UnsafePathError(msg)
    with os.fdopen(fd, "rb") as handle:
        data = handle.read(max_bytes + 1)
    if len(data) > max_bytes:
        msg = f"{relpath(target, root)} exceeds the {max_bytes:,}-byte size limit"
        raise ContentRejectedError(msg)
    if b"\x00" in data:
        msg = f"{relpath(target, root)} contains NUL bytes (binary content is not accepted)"
        raise ContentRejectedError(msg)
    return data.decode("utf-8-sig", errors="replace")


def atomic_write_text(path: Path, text: str) -> bool:
    """Atomically replace ``path`` with ``text`` (UTF-8, LF). Return ``True`` if it changed.

    The data is written to a sibling temporary file, flushed to disk and
    renamed over the target, so readers never observe a half-written file and
    an interrupted run never corrupts the catalog.
    """
    encoded = text.encode("utf-8")
    try:
        if path.read_bytes() == encoded:
            return False
    except FileNotFoundError:
        path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        tmp.chmod(0o644)
        tmp.replace(path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return True
