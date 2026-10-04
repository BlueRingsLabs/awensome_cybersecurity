"""Tests for hardened filesystem access."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from cyberkb.errors import ContentRejectedError, UnsafePathError
from cyberkb.fsutil import atomic_write_text, ensure_within, read_text, relpath


def test_read_text_ok(tmp_path: Path) -> None:
    (tmp_path / "f.md").write_text("hello", encoding="utf-8")
    assert read_text(tmp_path / "f.md", root=tmp_path, max_bytes=100) == "hello"


def test_read_text_strips_bom(tmp_path: Path) -> None:
    (tmp_path / "f.md").write_bytes(b"\xef\xbb\xbfhi")
    assert read_text(tmp_path / "f.md", root=tmp_path, max_bytes=100) == "hi"


def test_read_text_too_large(tmp_path: Path) -> None:
    (tmp_path / "big.md").write_text("x" * 50, encoding="utf-8")
    with pytest.raises(ContentRejectedError, match="size limit"):
        read_text(tmp_path / "big.md", root=tmp_path, max_bytes=10)


def test_read_text_binary_rejected(tmp_path: Path) -> None:
    (tmp_path / "b.md").write_bytes(b"ok\x00nope")
    with pytest.raises(ContentRejectedError, match="NUL"):
        read_text(tmp_path / "b.md", root=tmp_path, max_bytes=100)


def test_read_text_missing(tmp_path: Path) -> None:
    with pytest.raises(UnsafePathError):
        read_text(tmp_path / "nope.md", root=tmp_path, max_bytes=100)


def test_read_text_directory_rejected(tmp_path: Path) -> None:
    (tmp_path / "d").mkdir()
    with pytest.raises(UnsafePathError):
        read_text(tmp_path / "d", root=tmp_path, max_bytes=100)


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX symlink semantics")
def test_read_text_symlink_rejected(tmp_path: Path) -> None:
    (tmp_path / "secret.md").write_text("s", encoding="utf-8")
    (tmp_path / "link.md").symlink_to(tmp_path / "secret.md")
    with pytest.raises(UnsafePathError, match="link"):
        read_text(tmp_path / "link.md", root=tmp_path, max_bytes=100)


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX symlink semantics")
def test_ensure_within_symlinked_dir_rejected(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (tmp_path / "root").mkdir()
    (tmp_path / "root" / "evil").symlink_to(outside)
    with pytest.raises(UnsafePathError, match="link"):
        ensure_within(tmp_path / "root" / "evil" / "x.md", tmp_path / "root")


def test_ensure_within_escape_rejected(tmp_path: Path) -> None:
    (tmp_path / "root").mkdir()
    with pytest.raises(UnsafePathError, match="outside"):
        ensure_within(tmp_path / "root" / ".." / "etc", tmp_path / "root")


def test_ensure_within_accepts_relative(tmp_path: Path) -> None:
    (tmp_path / "a").mkdir()
    resolved = ensure_within(Path("a/b.md"), tmp_path)
    assert resolved == tmp_path / "a" / "b.md"


def test_relpath(tmp_path: Path) -> None:
    assert relpath(tmp_path / "a" / "b.md", tmp_path) == "a/b.md"


def test_atomic_write_creates(tmp_path: Path) -> None:
    target = tmp_path / "sub" / "out.txt"
    assert atomic_write_text(target, "data") is True
    assert target.read_text(encoding="utf-8") == "data"


def test_atomic_write_skips_unchanged(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"
    atomic_write_text(target, "same")
    assert atomic_write_text(target, "same") is False


def test_atomic_write_changes(tmp_path: Path) -> None:
    target = tmp_path / "out.txt"
    atomic_write_text(target, "one")
    assert atomic_write_text(target, "two") is True
    assert target.read_text(encoding="utf-8") == "two"


def test_atomic_write_cleans_up_on_error(tmp_path: Path, monkeypatch) -> None:
    target = tmp_path / "out.txt"

    def boom(*_args: object, **_kwargs: object) -> None:
        msg = "disk full"
        raise OSError(msg)

    monkeypatch.setattr("os.fsync", boom)
    with pytest.raises(OSError, match="disk full"):
        atomic_write_text(target, "data")
    assert list(tmp_path.glob(".out.txt*")) == []
