"""Tests for the ingestion orchestrator."""

from __future__ import annotations

import json
from datetime import date
from typing import TYPE_CHECKING

from cyberkb.classify.llm import LLMClassifier
from cyberkb.frontmatter import split_front_matter
from cyberkb.ingest import IngestStatus, discover_submissions, ingest_inbox
from cyberkb.library import load_library
from cyberkb.llm import GeminiClient, HttpResponse
from cyberkb.taxonomy import load_taxonomy

if TYPE_CHECKING:
    from cyberkb.paths import RepoPaths
    from cyberkb.taxonomy import Taxonomy

TODAY = date(2026, 1, 15)
NMAP_BODY = (
    "# A practical Nmap scanning guide\n\n"
    "Nmap is the de facto network scanner for penetration testing and reconnaissance. "
    "This guide covers host discovery, port scanning and service detection for an "
    "authorized pentest.\n"
)


def _tax(repo: RepoPaths) -> Taxonomy:
    """Load the taxonomy for a test repository."""
    return load_taxonomy(repo.root)


def _drop(repo: RepoPaths, name: str, text: str) -> None:
    """Write a raw submission into the repository inbox."""
    (repo.inbox / name).write_text(text, encoding="utf-8")


def test_discover_submissions(repo: RepoPaths) -> None:
    """Only top-level Markdown files in the inbox are discovered, sorted."""
    _drop(repo, "a.md", "x")
    _drop(repo, "b.md", "y")
    (repo.inbox / "note.txt").write_text("ignored", encoding="utf-8")
    found = discover_submissions(repo)
    assert [p.name for p in found] == ["a.md", "b.md"]


def test_discover_no_inbox(repo: RepoPaths) -> None:
    """A missing inbox yields no submissions."""
    repo.inbox.rmdir()
    assert discover_submissions(repo) == []


def test_ingest_files_a_document(repo: RepoPaths) -> None:
    """A valid submission is filed with front matter and removed from the inbox."""
    _drop(repo, "nmap.md", NMAP_BODY)
    report = ingest_inbox(repo, _tax(repo), today=TODAY)
    assert report.filed == 1
    outcome = report.outcomes[0]
    assert outcome.status is IngestStatus.FILED
    assert outcome.category == "offensive-security"
    assert outcome.destination is not None
    assert not (repo.inbox / "nmap.md").exists()
    doc = (repo.root / outcome.destination).read_text(encoding="utf-8")
    raw, _ = split_front_matter(doc)
    assert raw is not None
    assert raw["id"] == outcome.resource_id
    assert raw["added"] == TODAY


def test_ingest_rejects_empty(repo: RepoPaths) -> None:
    """An empty (page-marker-only) submission is rejected and left in place."""
    _drop(repo, "empty.md", "[[ PAGE 1 ]]\n[[ PAGE 2 ]]\n")
    report = ingest_inbox(repo, _tax(repo), today=TODAY)
    assert report.rejected == 1
    assert report.outcomes[0].status is IngestStatus.REJECTED
    assert (repo.inbox / "empty.md").exists()


def test_ingest_rejects_binary(repo: RepoPaths) -> None:
    """A submission containing NUL bytes is rejected as binary."""
    (repo.inbox / "bin.md").write_bytes(b"content\x00with nul")
    report = ingest_inbox(repo, _tax(repo), today=TODAY)
    assert report.rejected == 1


def test_ingest_rejects_bad_front_matter(repo: RepoPaths) -> None:
    """A submission with a terminated but invalid front-matter block is rejected."""
    _drop(repo, "bad.md", "---\n: ::bad\n---\n\n" + NMAP_BODY)
    report = ingest_inbox(repo, _tax(repo), today=TODAY)
    assert report.rejected == 1
    assert report.outcomes[0].status is IngestStatus.REJECTED


def test_ingest_honours_contributor_hints(repo: RepoPaths) -> None:
    """Valid contributor hints override the classifier and mark the method manual."""
    body = "---\ncategory: malware-analysis\ntitle: Custom Title\n---\n\n" + NMAP_BODY
    _drop(repo, "hinted.md", body)
    report = ingest_inbox(repo, _tax(repo), today=TODAY)
    outcome = report.outcomes[0]
    assert outcome.category == "malware-analysis"
    assert outcome.destination is not None
    doc = (repo.root / outcome.destination).read_text(encoding="utf-8")
    raw, _ = split_front_matter(doc)
    assert raw is not None
    assert raw["title"] == "Custom Title"
    assert raw["classification"]["method"] == "manual"


def test_ingest_detects_license(repo: RepoPaths) -> None:
    """An open licence grant in the body is detected and recorded."""
    grant = "This work is licensed under a Creative Commons Attribution 4.0 International License."
    body = NMAP_BODY + "\n\n" + grant + "\n"
    _drop(repo, "lic.md", body)
    report = ingest_inbox(repo, _tax(repo), today=TODAY)
    assert report.outcomes[0].destination is not None
    doc = (repo.root / report.outcomes[0].destination).read_text(encoding="utf-8")
    raw, _ = split_front_matter(doc)
    assert raw is not None
    assert raw["license"] == "CC-BY-4.0"


def test_ingest_extracts_authors(repo: RepoPaths) -> None:
    """A byline in the body is extracted into the authors field."""
    _drop(repo, "byline.md", "# Guide\n\nBy Jane Roe\n\n" + NMAP_BODY)
    report = ingest_inbox(repo, _tax(repo), today=TODAY)
    assert report.outcomes[0].destination is not None
    doc = (repo.root / report.outcomes[0].destination).read_text(encoding="utf-8")
    raw, _ = split_front_matter(doc)
    assert raw is not None
    assert raw["authors"] == ["Jane Roe"]


def test_ingest_avoids_filename_collision(repo: RepoPaths) -> None:
    """Two different documents with the same title slug get distinct filenames."""
    _drop(repo, "one.md", NMAP_BODY)
    ingest_inbox(repo, _tax(repo), today=TODAY)
    _drop(
        repo,
        "two.md",
        NMAP_BODY.replace("de facto", "widely used different wording entirely here"),
    )
    ingest_inbox(repo, _tax(repo), today=TODAY, taken_ids=frozenset())
    dests = sorted(
        p.name for p in (repo.library / "offensive-security").glob("*.md") if p.name != "README.md"
    )
    assert len(dests) == 2


def test_ingest_id_collision_uses_taken(repo: RepoPaths) -> None:
    """Re-ingesting identical content with the id already taken mints a new id."""
    _drop(repo, "one.md", NMAP_BODY)
    report1 = ingest_inbox(repo, _tax(repo), today=TODAY)
    first_id = report1.outcomes[0].resource_id
    loaded = load_library(repo, _tax(repo))
    taken = frozenset(r.id for r in loaded.resources)
    _drop(repo, "dup.md", NMAP_BODY)
    report2 = ingest_inbox(repo, _tax(repo), today=TODAY, taken_ids=taken)
    assert report2.outcomes[0].resource_id != first_id


def test_ingest_staging_when_unclassifiable(repo: RepoPaths) -> None:
    """A document with no security signal is staged as uncategorized."""
    body = "# Notes\n\n" + " ".join(["lorem ipsum dolor sit amet consectetur"] * 10)
    _drop(repo, "vague.md", body)
    report = ingest_inbox(repo, _tax(repo), today=TODAY)
    assert report.staged == 1
    assert report.outcomes[0].category == "uncategorized"


def test_ingest_empty_inbox(repo: RepoPaths) -> None:
    """Ingesting an empty inbox produces no outcomes."""
    report = ingest_inbox(repo, _tax(repo), today=TODAY)
    assert report.outcomes == ()


class _FixedTransport:
    """A transport that always returns the same canned Gemini response."""

    def __init__(self, body: bytes) -> None:
        """Store the canned response body."""
        self._body = body

    def post(self, *_a: object, **_k: object) -> HttpResponse:
        """Return the canned response regardless of arguments."""
        return HttpResponse(200, self._body)


def test_ingest_with_llm_classifier(repo: RepoPaths) -> None:
    """With an LLM classifier, the model's title, method and summary are recorded."""
    item = {
        "ref": "0",
        "title": "LLM Titled Guide",
        "category": "offensive-security",
        "format": "guide",
        "language": "en",
        "tags": ["nmap"],
        "summary": "An LLM summary.",
        "confidence": 0.95,
    }
    payload = {
        "candidates": [{"content": {"parts": [{"text": json.dumps({"classifications": [item]})}]}}],
    }
    transport = _FixedTransport(json.dumps(payload).encode())
    client = GeminiClient("key", ("gemini-test",), transport=transport, sleep=lambda _s: None)
    classifier = LLMClassifier(client, _tax(repo))
    _drop(repo, "nmap.md", NMAP_BODY)
    report = ingest_inbox(repo, _tax(repo), classifier=classifier, today=TODAY, batch_size=5)
    assert report.outcomes[0].destination is not None
    doc = (repo.root / report.outcomes[0].destination).read_text(encoding="utf-8")
    raw, _ = split_front_matter(doc)
    assert raw is not None
    assert raw["title"] == "LLM Titled Guide"
    assert raw["classification"]["method"] == "llm"
    assert raw["summary"] == "An LLM summary."
