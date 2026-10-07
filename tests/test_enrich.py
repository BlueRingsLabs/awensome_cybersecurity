"""Tests for enriching the library through the rotation engine and the ledger."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from cyberkb.enrich import EnrichStatus, enrich_library
from cyberkb.enrich_state import EnrichState, ResourceState, load_state
from cyberkb.frontmatter import Classification, split_front_matter
from cyberkb.providers.rotation import RotationSettings
from cyberkb.taxonomy import load_taxonomy
from tests.conftest import write_resource
from tests.llmfakes import (
    Router,
    answer,
    default_google_listing,
    google_answer,
    google_error,
    item,
    make_classifier,
    single_model_catalog,
    validated_today,
)

if TYPE_CHECKING:
    from cyberkb.classify.llm import LLMClassifier
    from cyberkb.paths import RepoPaths
    from cyberkb.providers.http import HttpResponse
    from cyberkb.taxonomy import Taxonomy
    from tests.llmfakes import FakeTime

HEURISTIC = Classification("heuristic", 0.4)
A = "ckb-00000000000a"
B = "ckb-00000000000b"


def _classifier(
    taxonomy: Taxonomy, *responses: HttpResponse, settings: RotationSettings | None = None
) -> tuple[LLMClassifier, FakeTime, Router]:
    router = Router().add("google:list", default_google_listing())
    router.add("google:gemma-t-it", *responses)
    classifier, time = make_classifier(
        router,
        taxonomy,
        catalog_doc=single_model_catalog(),
        validations=validated_today(),
        settings=settings or RotationSettings(model_retries=0, list_passes=1),
    )
    return classifier, time, router


def _ok(ref: str, **overrides: Any) -> HttpResponse:  # noqa: ANN401
    return google_answer(answer(item(ref, **overrides)))


def _heuristic(repo: RepoPaths, rid: str, *, filename: str, title: str = "Doc", **kw: Any) -> None:  # noqa: ANN401
    write_resource(
        repo, filename=filename, id=rid, title=title, classification=HEURISTIC, summary="", **kw
    )


def _front(repo: RepoPaths, relative: str) -> dict[str, Any]:
    raw, _ = split_front_matter((repo.root / relative).read_text(encoding="utf-8"))
    assert raw is not None
    return raw


def test_manual_resources_are_skipped_without_a_call(repo: RepoPaths) -> None:
    """Manual classifications are out of scope: nothing is sent, nothing is pending."""
    taxonomy = load_taxonomy(repo.root)
    write_resource(repo, filename="manual.md")
    classifier, _, router = _classifier(taxonomy)
    state = EnrichState()
    report = enrich_library(repo, taxonomy, classifier, state)
    assert report.outcomes[0].status is EnrichStatus.SKIPPED
    assert report.final_status == "complete"
    assert router.bodies("google:gemma-t-it") == []
    assert state.resources == {}


def test_upgrade_moves_on_category_change_and_persists_immediately(repo: RepoPaths) -> None:
    """A new category moves the file atomically; the ledger records who did it."""
    taxonomy = load_taxonomy(repo.root)
    _heuristic(repo, A, filename="a.md", title="Alpha", category="foundations-and-systems")
    classifier, _, _ = _classifier(
        taxonomy, _ok(A, title="Alpha Guide", category="offensive-security")
    )
    state = EnrichState()
    report = enrich_library(repo, taxonomy, classifier, state)
    outcome = report.outcomes[0]
    assert outcome.status is EnrichStatus.ENRICHED
    assert outcome.destination == "library/offensive-security/alpha.md"
    assert outcome.detail == "foundations-and-systems -> offensive-security"
    assert not (repo.library / "foundations-and-systems" / "a.md").exists()
    raw = _front(repo, outcome.destination)
    assert raw["classification"]["method"] == "llm"
    assert raw["classified_by"].startswith("google:gemma-t-it@")
    assert raw["summary"].startswith("A practical guide")
    ledger = load_state(repo)
    entry = ledger.resources[A]
    assert (entry.status, entry.provider, entry.model) == ("enriched", "google", "gemma-t-it")
    assert entry.path == outcome.destination
    assert ledger.in_flight is None
    assert report.final_status == "complete"
    assert outcome.to_dict()["provider"] == "google"


def test_upgrade_in_place_when_the_category_is_unchanged(repo: RepoPaths) -> None:
    """Same category: the file is rewritten in place."""
    taxonomy = load_taxonomy(repo.root)
    _heuristic(repo, A, filename="a.md", body="# A\n\nBy Jane Doe. Notes on nmap.\n")
    classifier, _, _ = _classifier(taxonomy, _ok(A))
    report = enrich_library(repo, taxonomy, classifier, EnrichState())
    assert report.outcomes[0].destination == "library/offensive-security/a.md"
    assert _front(repo, "library/offensive-security/a.md")["classification"]["method"] == "llm"


def test_moving_never_overwrites_an_existing_file(repo: RepoPaths) -> None:
    """A slug collision in the destination category gets a numbered name."""
    taxonomy = load_taxonomy(repo.root)
    write_resource(repo, filename="kept-title.md", title="Kept Title", id=B)
    _heuristic(repo, A, filename="doc.md", title="Kept Title", category="foundations-and-systems")
    classifier, _, _ = _classifier(taxonomy, _ok(A, title="Kept Title"))
    report = enrich_library(repo, taxonomy, classifier, EnrichState())
    assert report.enriched == 1
    assert (repo.library / "offensive-security" / "kept-title-2.md").exists()
    assert (repo.library / "offensive-security" / "kept-title.md").exists()


def test_a_resource_every_model_fails_is_recorded_and_left_untouched(repo: RepoPaths) -> None:
    """A content-filtered document is FAILED with its cause; its file is unchanged."""
    taxonomy = load_taxonomy(repo.root)
    _heuristic(repo, A, filename="a.md")
    before = (repo.library / "offensive-security" / "a.md").read_bytes()
    classifier, _, _ = _classifier(taxonomy, google_answer(answer(), finish="SAFETY"))
    state = EnrichState()
    report = enrich_library(repo, taxonomy, classifier, state)
    outcome = report.outcomes[0]
    assert outcome.status is EnrichStatus.FAILED
    assert outcome.category == "content_filter"
    assert (repo.library / "offensive-security" / "a.md").read_bytes() == before
    entry = load_state(repo).resources[A]
    assert (entry.status, entry.last_error_category, entry.attempts) == (
        "failed",
        "content_filter",
        1,
    )
    assert report.final_status == "failed"
    assert report.capacity_exhausted is False
    assert "could not be classified" in report.reason


def test_failed_resources_get_another_chance_after_pending_ones(repo: RepoPaths) -> None:
    """Pending work goes first; a previously failed resource is retried afterwards."""
    taxonomy = load_taxonomy(repo.root)
    _heuristic(repo, A, filename="a.md")
    _heuristic(repo, B, filename="b.md")
    state = EnrichState(
        resources={
            A: ResourceState("failed", "x", attempts=1, last_error_category="content_filter")
        }
    )
    classifier, _, router = _classifier(taxonomy, _ok(B), _ok(A))
    report = enrich_library(repo, taxonomy, classifier, state)
    sent = [json.dumps(b) for b in router.bodies("google:gemma-t-it")]
    assert B in sent[0]
    assert A in sent[1]
    assert report.enriched == 2
    assert state.resources[A].attempts == 2
    assert state.resources[A].last_error_category is None


def test_exhausted_capacity_defers_everything_left(repo: RepoPaths) -> None:
    """When no model is left, remaining resources stay pending and the run says why."""
    taxonomy = load_taxonomy(repo.root)
    _heuristic(repo, A, filename="a.md")
    _heuristic(repo, B, filename="b.md")
    classifier, _, _ = _classifier(taxonomy, google_error(500, "INTERNAL", "down"))
    state = EnrichState()
    report = enrich_library(repo, taxonomy, classifier, state)
    assert [o.status for o in report.outcomes] == [EnrichStatus.DEFERRED, EnrichStatus.DEFERRED]
    assert report.capacity_exhausted is True
    assert report.final_status == "failed"
    assert "every model is exhausted or failed" in report.reason
    assert state.counts() == {"pending": 2, "enriched": 0, "failed": 0}


def test_limit_processes_some_and_defers_the_rest(repo: RepoPaths) -> None:
    """--limit caps attempts; the remainder is deferred and the run is partial."""
    taxonomy = load_taxonomy(repo.root)
    _heuristic(repo, A, filename="a.md")
    _heuristic(repo, B, filename="b.md")
    classifier, _, _ = _classifier(taxonomy, _ok(A))
    report = enrich_library(repo, taxonomy, classifier, EnrichState(), limit=1)
    assert report.enriched == 1
    assert report.deferred == 1
    assert report.budget_reached is True
    assert report.final_status == "partial"
    assert "run budget" in report.reason


def test_time_budget_defers_the_remaining_work(repo: RepoPaths) -> None:
    """--max-seconds stops new work once spent, even before the first request."""
    taxonomy = load_taxonomy(repo.root)
    _heuristic(repo, A, filename="a.md")
    classifier, time, _ = _classifier(taxonomy)
    clock_values = iter([0.0, 10.0])
    report = enrich_library(
        repo, taxonomy, classifier, EnrichState(), max_seconds=5.0, clock=lambda: next(clock_values)
    )
    assert report.deferred == 1
    assert report.final_status == "partial"
    _ = time


def test_a_deferral_inside_the_engine_stops_the_run(repo: RepoPaths) -> None:
    """If the engine runs out of budget mid-request, nothing else is attempted."""
    taxonomy = load_taxonomy(repo.root)
    _heuristic(repo, A, filename="a.md")
    _heuristic(repo, B, filename="b.md")
    busy = google_error(503, "UNAVAILABLE", "busy")
    classifier, time, router = _classifier(
        taxonomy,
        busy,
        settings=RotationSettings(model_retries=2, backoff_base=200.0, backoff_cap=400.0),
    )
    report = enrich_library(
        repo, taxonomy, classifier, EnrichState(), max_seconds=50.0, clock=time.clock
    )
    assert [o.status for o in report.outcomes] == [EnrichStatus.DEFERRED, EnrichStatus.DEFERRED]
    assert report.final_status == "partial"
    assert len(router.bodies("google:gemma-t-it")) == 1


def test_llm_resources_are_left_until_forced(repo: RepoPaths) -> None:
    """Already-enriched resources are unchanged unless --force re-queues them."""
    taxonomy = load_taxonomy(repo.root)
    write_resource(
        repo,
        filename="a.md",
        id=A,
        classification=Classification("llm", 0.9, "gemma-t-it"),
        classified_by="google:gemma-t-it@2026-10-06T00:00:00Z",
    )
    classifier, _, _ = _classifier(taxonomy, _ok(A))
    first = enrich_library(repo, taxonomy, classifier, EnrichState())
    assert first.outcomes[0].status is EnrichStatus.UNCHANGED
    assert first.unchanged == 1
    assert first.skipped == 0
    forced = enrich_library(repo, taxonomy, classifier, EnrichState(), force=True)
    assert forced.enriched == 1
