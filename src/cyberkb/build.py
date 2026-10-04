"""The build step: regenerate every generated artefact from the library.

``build`` is deterministic and idempotent. It loads the library, and if it is
clean, writes ``index.json``, ``index.yaml``, the README AUTO-INDEX block and
one ``README.md`` per category -- but only the files whose content actually
changed, so an unchanged tree produces an empty diff.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from cyberkb.catalog import build_catalog, catalog_json, catalog_yaml, strip_volatile_lines
from cyberkb.errors import KBError
from cyberkb.fsutil import atomic_write_text, read_text
from cyberkb.library import load_library
from cyberkb.render import render_category_page, render_index_block, splice_readme
from cyberkb.taxonomy import load_taxonomy

if TYPE_CHECKING:
    from datetime import datetime
    from pathlib import Path

    from cyberkb.library import LoadedLibrary, Resource
    from cyberkb.paths import RepoPaths
    from cyberkb.taxonomy import Taxonomy

__all__ = ["BuildResult", "build"]

_MAX_README_BYTES = 1024 * 1024


@dataclass(frozen=True, slots=True)
class BuildResult:
    """Outcome of a build."""

    changed: tuple[str, ...]
    resource_count: int
    problems: tuple[tuple[str, str], ...]

    @property
    def ok(self) -> bool:
        """``True`` when the library loaded without problems."""
        return not self.problems


def build(paths: RepoPaths, *, generated_at: datetime | None = None) -> BuildResult:
    """Regenerate all derived artefacts; refuse to write if the library is unclean.

    Raises:
        KBError: the taxonomy is invalid.
    """
    taxonomy = load_taxonomy(paths.root)
    library: LoadedLibrary = load_library(paths, taxonomy)
    if not library.ok:
        return BuildResult((), len(library.resources), library.problems)

    resources = library.resources
    catalog = build_catalog(resources, taxonomy, generated_at=generated_at)
    changed: list[str] = []

    if _write_timestamped(paths, paths.index_json, catalog_json(catalog)):
        changed.append(paths.index_json.name)
    if _write_timestamped(paths, paths.index_yaml, catalog_yaml(catalog)):
        changed.append(paths.index_yaml.name)

    block = render_index_block(catalog, resources, taxonomy)
    changed.extend(_write_readme(paths, block))
    changed.extend(_write_category_pages(paths, resources, taxonomy))
    return BuildResult(tuple(changed), len(resources), ())


def _write_timestamped(paths: RepoPaths, path: Path, candidate: str) -> bool:
    """Write ``candidate`` unless it differs from disk only by the timestamp line.

    This keeps ``build`` idempotent: re-running it on an unchanged library
    produces no diff, even though each build computes a fresh timestamp.
    """
    try:
        existing = read_text(path, root=paths.root, max_bytes=_MAX_README_BYTES)
    except KBError:
        return atomic_write_text(path, candidate)
    if strip_volatile_lines(existing) == strip_volatile_lines(candidate):
        return False
    return atomic_write_text(path, candidate)


def _write_readme(paths: RepoPaths, block: str) -> list[str]:
    try:
        readme = read_text(paths.readme, root=paths.root, max_bytes=_MAX_README_BYTES)
    except KBError:
        readme = ""
    updated = splice_readme(readme, block)
    return ["README.md"] if _write_timestamped(paths, paths.readme, updated) else []


def _write_category_pages(
    paths: RepoPaths,
    resources: tuple[Resource, ...],
    taxonomy: Taxonomy,
) -> list[str]:
    changed: list[str] = []
    present: dict[str, list[Resource]] = {}
    for resource in resources:
        present.setdefault(resource.category, []).append(resource)
    for category_id, subset in present.items():
        page = paths.library / category_id / "README.md"
        if atomic_write_text(page, render_category_page(category_id, subset, taxonomy)):
            changed.append(f"library/{category_id}/README.md")
    return changed
