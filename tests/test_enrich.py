"""Tests for backfilling summaries and classifications via the LLM."""

from __future__ import annotations

import io
import json
from typing import TYPE_CHECKING, Any

from cyberkb.classify.llm import LLMClassifier
from cyberkb.enrich import EnrichStatus, enrich_library
from cyberkb.frontmatter import Classification
from cyberkb.library import load_library
from cyberkb.obslog import StructuredLogger
from cyberkb.providers.gemini import GeminiProvider
from cyberkb.providers.orchestrator import Orchestrator, OrchestratorSettings
from cyberkb.taxonomy import load_taxonomy
from tests.conftest import FakeTransport, http_json, http_text, write_resource

if TYPE_CHECKING:
    from collections.abc import Callable

    from cyberkb.paths import RepoPaths
    from cyberkb.providers.http import HttpResponse, HttpTransportError
    from cyberkb.taxonomy import Taxonomy

HEURISTIC = Classification("heuristic", 0.4)


def _clock() -> Callable[[], float]:
    state = {"v": 0.0}

    def tick() -> float:
        state["v"] += 1.0
        return state["v"]

    return tick


def _classifier(taxonomy: Taxonomy, *items: HttpResponse | HttpTransportError) -> LLMClassifier:
    provider = GeminiProvider("key", transport=FakeTransport(*items), clock=_clock())
    orchestrator = Orchestrator(
        [provider],
        logger=StructuredLogger(io.StringIO()),
        sleep=lambda _s: None,
        clock=_clock(),
        settings=OrchestratorSettings(max_retries=2),
    )
    orchestrator._selected = {"gemini": ("gemini-test",)}  # noqa: SLF001 - seed validated model
    return LLMClassifier(orchestrator, taxonomy)


def _envelope(ref: str, category: str, summary: str) -> HttpResponse:
    item: dict[str, Any] = {
        "ref": ref,
        "title": "Kept Title",
        "category": category,
        "format": "guide",
        "language": "en",
        "tags": ["nmap"],
        "summary": summary,
        "confidence": 0.95,
    }
    text = json.dumps({"classifications": [item]})
    return http_json(200, {"candidates": [{"content": {"parts": [{"text": text}]}}]})


def _only_id(repo: RepoPaths, taxonomy: Taxonomy) -> str:
    return load_library(repo, taxonomy).resources[0].id


def test_enrich_skips_manual_resources(repo: RepoPaths) -> None:
    """A manually classified resource is never touched by enrichment."""
    taxonomy = load_taxonomy(repo.root)
    write_resource(repo, filename="manual.md", classification=Classification("manual", 1.0))
    report = enrich_library(repo, taxonomy, _classifier(taxonomy), force=False)
    assert report.skipped == 1
    assert report.enriched == 0


def test_enrich_upgrades_heuristic_and_moves_on_category_change(repo: RepoPaths) -> None:
    """A heuristic resource adopts the LLM category/summary and the file moves."""
    taxonomy = load_taxonomy(repo.root)
    write_resource(
        repo,
        category="foundations-and-systems",
        filename="doc.md",
        title="Kept Title",
        classification=HEURISTIC,
        summary="",
        body="# Kept Title\n\nA document about exploitation and penetration testing with nmap.\n",
    )
    rid = _only_id(repo, taxonomy)
    classifier = _classifier(taxonomy, _envelope(rid, "offensive-security", "An LLM summary."))
    report = enrich_library(repo, taxonomy, classifier)
    assert report.enriched == 1
    assert not (repo.library / "foundations-and-systems" / "doc.md").exists()
    moved = next((repo.library / "offensive-security").glob("*.md"))
    front = moved.read_text(encoding="utf-8")
    assert "summary: An LLM summary." in front
    assert "method: llm" in front
    assert "classified_by: gemini:gemini-test@" in front


def test_enrich_in_place_when_category_unchanged(repo: RepoPaths) -> None:
    """When the LLM keeps the category, the summary is backfilled in place."""
    taxonomy = load_taxonomy(repo.root)
    path = write_resource(
        repo,
        category="offensive-security",
        filename="keep.md",
        title="Kept Title",
        classification=HEURISTIC,
        summary="",
    )
    rid = _only_id(repo, taxonomy)
    classifier = _classifier(taxonomy, _envelope(rid, "offensive-security", "Filled summary."))
    report = enrich_library(repo, taxonomy, classifier)
    assert report.enriched == 1
    assert path.exists()  # same file, updated in place
    assert "summary: Filled summary." in path.read_text(encoding="utf-8")


def test_enrich_unchanged_when_no_provider_available(repo: RepoPaths) -> None:
    """A heuristic resource is left as-is when every provider fails."""
    taxonomy = load_taxonomy(repo.root)
    write_resource(repo, filename="x.md", classification=HEURISTIC, summary="", title="Kept Title")
    classifier = _classifier(taxonomy, http_text(500, "boom"), http_text(500, "boom"))
    report = enrich_library(repo, taxonomy, classifier)
    assert report.unchanged == 1
    assert report.enriched == 0


def test_enrich_leaves_llm_resources_until_forced(repo: RepoPaths) -> None:
    """An already-LLM-classified resource is unchanged unless force is set."""
    taxonomy = load_taxonomy(repo.root)
    write_resource(
        repo,
        category="offensive-security",
        filename="llm.md",
        title="Kept Title",
        classification=Classification("llm", 0.9, "old-model"),
        summary="old",
    )
    report = enrich_library(repo, taxonomy, _classifier(taxonomy), force=False)
    assert report.unchanged == 1

    rid = _only_id(repo, taxonomy)
    classifier = _classifier(taxonomy, _envelope(rid, "offensive-security", "fresh summary"))
    forced = enrich_library(repo, taxonomy, classifier, force=True)
    assert forced.enriched == 1


def test_enrich_move_avoids_filename_collision(repo: RepoPaths) -> None:
    """When the destination slug is taken, the moved file gets a unique name."""
    taxonomy = load_taxonomy(repo.root)
    write_resource(
        repo,
        category="offensive-security",
        filename="kept-title.md",
        title="Kept Title",
        classification=Classification("manual", 1.0),
        body="# Kept Title\n\nA pre-existing manual note about exploit development here.\n",
    )
    write_resource(
        repo,
        category="foundations-and-systems",
        filename="doc.md",
        title="Kept Title",
        classification=HEURISTIC,
        summary="",
        body="# Kept Title\n\nA distinct document about nmap and penetration testing.\n",
    )
    rid = next(
        r.id
        for r in load_library(repo, taxonomy).resources
        if r.front_matter.classification.method == "heuristic"
    )
    classifier = _classifier(taxonomy, _envelope(rid, "offensive-security", "Moved summary."))
    report = enrich_library(repo, taxonomy, classifier)
    assert report.enriched == 1
    assert (repo.library / "offensive-security" / "kept-title-2.md").exists()
    assert (repo.library / "offensive-security" / "kept-title.md").exists()  # original untouched


def test_enrich_outcome_statuses_are_reported(repo: RepoPaths) -> None:
    """The report distinguishes enriched, unchanged and skipped resources."""
    taxonomy = load_taxonomy(repo.root)
    write_resource(repo, filename="manual.md", classification=Classification("manual", 1.0))
    report = enrich_library(repo, taxonomy, _classifier(taxonomy))
    assert report.outcomes[0].status is EnrichStatus.SKIPPED


def _two_heuristics(repo: RepoPaths) -> None:
    write_resource(
        repo,
        category="offensive-security",
        filename="a.md",
        id="ckb-000000000001",
        title="Alpha Title",
        classification=HEURISTIC,
        summary="",
        body="# Alpha Title\n\nnmap host discovery and port scanning in a penetration test.\n",
    )
    write_resource(
        repo,
        category="offensive-security",
        filename="b.md",
        id="ckb-000000000002",
        title="Beta Title",
        classification=HEURISTIC,
        summary="",
        body="# Beta Title\n\nmore nmap scanning and exploit development for an authorized test.\n",
    )


def test_enrich_limit_processes_some_and_defers_the_rest(repo: RepoPaths) -> None:
    """``limit`` caps LLM calls this run; the remainder is reported as deferred."""
    taxonomy = load_taxonomy(repo.root)
    _two_heuristics(repo)
    first = load_library(repo, taxonomy).resources[0].id
    # Exactly one envelope is supplied: a second LLM call would exhaust the
    # transport and raise, so this also proves only one resource was processed.
    classifier = _classifier(taxonomy, _envelope(first, "offensive-security", "Only one."))
    report = enrich_library(repo, taxonomy, classifier, limit=1)
    assert report.enriched == 1
    assert report.deferred == 1
    assert {o.status for o in report.outcomes} == {EnrichStatus.ENRICHED, EnrichStatus.DEFERRED}


def test_enrich_limit_zero_defers_all_without_calling_a_provider(repo: RepoPaths) -> None:
    """``limit=0`` defers every resource and never contacts a provider."""
    taxonomy = load_taxonomy(repo.root)
    _two_heuristics(repo)
    # No transport items: any LLM call would raise, so passing proves none happened.
    report = enrich_library(repo, taxonomy, _classifier(taxonomy), limit=0)
    assert report.deferred == 2
    assert report.enriched == 0


def test_enrich_time_budget_defers_remaining(repo: RepoPaths) -> None:
    """``max_seconds`` stops starting new work once the wall-clock budget is spent."""
    taxonomy = load_taxonomy(repo.root)
    _two_heuristics(repo)
    first = load_library(repo, taxonomy).resources[0].id
    classifier = _classifier(taxonomy, _envelope(first, "offensive-security", "Within budget."))
    # start()->0, first resource check->10 (<50, processed), second check->100 (>=50, deferred);
    # any further call returns the exhausted default, keeping the budget spent.
    ticks = iter((0.0, 10.0, 100.0))
    report = enrich_library(
        repo, taxonomy, classifier, max_seconds=50.0, clock=lambda: next(ticks, 100.0)
    )
    assert report.enriched == 1
    assert report.deferred == 1
