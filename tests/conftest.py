"""Shared fixtures and helpers for the cyberkb test suite."""

from __future__ import annotations

import shutil
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from cyberkb.frontmatter import Classification, FrontMatter, render_document
from cyberkb.paths import RepoPaths
from cyberkb.taxonomy import Taxonomy, load_taxonomy

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REAL_TAXONOMY = PROJECT_ROOT / "schema" / "taxonomy.yaml"
FIXED_NOW = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)


@pytest.fixture(scope="session")
def taxonomy() -> Taxonomy:
    """The real repository taxonomy, loaded once per test session."""
    return load_taxonomy(PROJECT_ROOT)


@pytest.fixture
def repo(tmp_path: Path) -> RepoPaths:
    """An empty repository skeleton with the real taxonomy and an inbox."""
    (tmp_path / "schema").mkdir()
    shutil.copy(REAL_TAXONOMY, tmp_path / "schema" / "taxonomy.yaml")
    (tmp_path / "library").mkdir()
    (tmp_path / "inbox").mkdir()
    (tmp_path / "README.md").write_text(
        "# Test KB\n\n<!-- BEGIN AUTO-INDEX -->\nplaceholder\n<!-- END AUTO-INDEX -->\n",
        encoding="utf-8",
    )
    return RepoPaths.at(tmp_path)


def make_front_matter(**overrides: object) -> FrontMatter:
    """Build a valid :class:`FrontMatter` with sensible defaults for tests."""
    defaults: dict[str, object] = {
        "id": "ckb-000000000001",
        "title": "Sample Resource",
        "category": "offensive-security",
        "format": "guide",
        "language": "en",
        "license": "CC-BY-4.0",
        "added": date(2026, 1, 1),
        "classification": Classification("manual", 1.0),
        "tags": ("nmap",),
        "summary": "A sample resource for tests.",
        "authors": (),
        "source_url": None,
    }
    defaults.update(overrides)
    return FrontMatter(**defaults)  # type: ignore[arg-type]


def write_resource(
    repo: RepoPaths,
    *,
    category: str = "offensive-security",
    body: str = "# Sample\n\nSome body text about penetration testing and nmap.\n",
    filename: str = "sample.md",
    **fm_overrides: object,
) -> Path:
    """Write a valid library document and return its path."""
    fm_overrides.setdefault("category", category)
    front_matter = make_front_matter(**fm_overrides)
    directory = repo.library / category
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    path.write_text(render_document(front_matter, body), encoding="utf-8")
    return path


@pytest.fixture
def built_repo(repo: RepoPaths) -> RepoPaths:
    """A repository with one valid resource and freshly generated artefacts."""
    from cyberkb.build import build

    write_resource(repo)
    result = build(repo, generated_at=FIXED_NOW)
    assert result.ok
    return repo
