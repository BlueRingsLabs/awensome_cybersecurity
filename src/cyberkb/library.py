"""Reading the curated library from disk.

A :class:`Resource` is one validated library document: its front matter plus
derived facts (path, size, word count, body digest). :func:`load_library`
walks ``library/<category>/`` and returns every resource together with any
problems found, so the catalog builder and the CI check share exactly one
notion of what the library contains.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING

from cyberkb.errors import FrontMatterError, KBError
from cyberkb.frontmatter import FrontMatter, parse_front_matter, split_front_matter
from cyberkb.fsutil import read_text, relpath
from cyberkb.textutil import word_count

if TYPE_CHECKING:
    from pathlib import Path

    from cyberkb.paths import RepoPaths
    from cyberkb.taxonomy import Taxonomy

__all__ = ["LoadedLibrary", "Resource", "load_library"]

MAX_RESOURCE_BYTES = 8 * 1024 * 1024
#: Generated per-category index page; it is an output, never a resource.
CATEGORY_PAGE_NAME = "README.md"


def _resource_files(directory: Path) -> list[Path]:
    return [p for p in sorted(directory.glob("*.md")) if p.name != CATEGORY_PAGE_NAME]


@dataclass(frozen=True, slots=True)
class Resource:
    """One validated resource in the library."""

    front_matter: FrontMatter
    path: str
    size_bytes: int
    word_count: int
    body_sha256: str

    @property
    def id(self) -> str:
        """Stable resource id."""
        return self.front_matter.id

    @property
    def category(self) -> str:
        """Primary category id."""
        return self.front_matter.category


@dataclass(frozen=True, slots=True)
class LoadedLibrary:
    """Everything the library loader found, including problems."""

    resources: tuple[Resource, ...]
    problems: tuple[tuple[str, str], ...]

    @property
    def ok(self) -> bool:
        """``True`` when every document loaded without a problem."""
        return not self.problems


def _category_dirs(library: Path, taxonomy: Taxonomy) -> list[tuple[str, Path]]:
    return [(cat.id, library / cat.id) for cat in taxonomy.categories]


def load_library(paths: RepoPaths, taxonomy: Taxonomy) -> LoadedLibrary:
    """Load and validate every resource under ``library/``.

    The loader never raises on document-level problems; it records each as
    ``(relative_path, message)`` and keeps going, so one malformed file does
    not hide the state of the rest. It also flags files that sit directly in
    ``library/`` (they must live inside a category folder) and category
    folders that do not exist in the taxonomy.
    """
    resources: list[Resource] = []
    problems: list[tuple[str, str]] = []
    library = paths.library
    known = {cat.id for cat in taxonomy.categories}

    if not library.is_dir():
        return LoadedLibrary((), ())

    problems.extend(
        (relpath(stray, paths.root), "Markdown file must live inside a category folder")
        for stray in sorted(library.glob("*.md"))
        if stray.name != CATEGORY_PAGE_NAME
    )
    problems.extend(
        (relpath(child, paths.root), f"not a taxonomy category: {child.name!r}")
        for child in sorted(p for p in library.iterdir() if p.is_dir())
        if child.name not in known
    )

    for category_id, directory in _category_dirs(library, taxonomy):
        if not directory.is_dir():
            continue
        for md in _resource_files(directory):
            rel = relpath(md, paths.root)
            try:
                resource = _load_resource(md, rel, category_id, paths, taxonomy)
            except KBError as exc:
                problems.append((rel, str(exc)))
                continue
            resources.append(resource)

    _detect_duplicates(resources, problems)
    resources.sort(key=lambda r: (r.category, r.front_matter.title.casefold(), r.id))
    return LoadedLibrary(tuple(resources), tuple(problems))


def _load_resource(
    md: Path,
    rel: str,
    category_id: str,
    paths: RepoPaths,
    taxonomy: Taxonomy,
) -> Resource:
    text = read_text(md, root=paths.root, max_bytes=MAX_RESOURCE_BYTES)
    raw, body = split_front_matter(text)
    if raw is None:
        msg = "document has no YAML front matter"
        raise FrontMatterError(msg)
    front_matter = parse_front_matter(raw, taxonomy)
    if front_matter.category != category_id:
        msg = (
            f"front matter category {front_matter.category!r} does not match folder {category_id!r}"
        )
        raise FrontMatterError(msg)
    return Resource(
        front_matter=front_matter,
        path=rel,
        size_bytes=len(text.encode("utf-8")),
        word_count=word_count(body),
        body_sha256=hashlib.sha256(body.encode("utf-8")).hexdigest(),
    )


def _detect_duplicates(resources: list[Resource], problems: list[tuple[str, str]]) -> None:
    by_id: dict[str, list[str]] = {}
    by_body: dict[str, list[str]] = {}
    for resource in resources:
        by_id.setdefault(resource.id, []).append(resource.path)
        by_body.setdefault(resource.body_sha256, []).append(resource.path)
    for ident, locations in sorted(by_id.items()):
        if len(locations) > 1:
            problems.append(
                (locations[0], f"duplicate id {ident} also used by: {', '.join(locations[1:])}")
            )
    for locations in by_body.values():
        if len(locations) > 1:
            ordered = sorted(locations)
            problems.append((ordered[0], f"identical body to: {', '.join(ordered[1:])}"))
