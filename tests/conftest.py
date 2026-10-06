"""Shared fixtures and helpers for the cyberkb test suite."""

from __future__ import annotations

import json
import shutil
from datetime import UTC, date, datetime
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from cyberkb.build import build
from cyberkb.frontmatter import Classification, FrontMatter, render_document
from cyberkb.paths import RepoPaths
from cyberkb.providers.http import HttpResponse, HttpTransportError
from cyberkb.taxonomy import Taxonomy, load_taxonomy

if TYPE_CHECKING:
    from collections.abc import Mapping

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REAL_TAXONOMY = PROJECT_ROOT / "schema" / "taxonomy.yaml"
FIXED_NOW = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)


def http_json(status: int, obj: object, headers: Mapping[str, str] | None = None) -> HttpResponse:
    """Build an :class:`HttpResponse` whose body is ``obj`` serialised to JSON."""
    return HttpResponse(status, json.dumps(obj).encode("utf-8"), dict(headers or {}))


def http_text(status: int, body: str, headers: Mapping[str, str] | None = None) -> HttpResponse:
    """Build an :class:`HttpResponse` with a raw (possibly non-JSON) text body."""
    return HttpResponse(status, body.encode("utf-8"), dict(headers or {}))


class FakeTransport:
    """A Transport double returning queued responses or raising queued faults.

    This is the project's only legitimate test double: it stands in for the real
    network at the exact HTTP boundary a provider cannot cross in a unit test.
    Every bit of provider logic (request building, status handling, parsing,
    discovery, rotation) runs for real against it.
    """

    def __init__(self, *items: HttpResponse | HttpTransportError) -> None:
        """Queue the responses/faults to hand back, in order."""
        self._items = list(items)
        self.calls: list[tuple[str, str, bytes | None, dict[str, str]]] = []

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout: float,
    ) -> HttpResponse:
        """Record the call and return (or raise) the next queued item."""
        _ = timeout
        self.calls.append((method, url, body, dict(headers)))
        item = self._items.pop(0)
        if isinstance(item, HttpTransportError):
            raise item
        return item


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
    write_resource(repo)
    result = build(repo, generated_at=FIXED_NOW)
    assert result.ok
    return repo
