"""Tests for the rotation engine: discovery, validation, pacing, retries, routing.

Every test drives the real adapters, engine and classifier; only the network
(:class:`tests.llmfakes.Router`) and the clock (:class:`tests.llmfakes.FakeTime`)
are doubles.
"""

from __future__ import annotations

import copy
import json
from typing import TYPE_CHECKING, Any

import pytest

from cyberkb.classify.base import Document
from cyberkb.errors import FailureCategory, ProviderConfigError
from cyberkb.providers.governor import DailyUsage
from cyberkb.providers.http import HttpTransportError
from cyberkb.providers.rotation import (
    CachedValidation,
    GenerationRequest,
    RotationSettings,
    SlotStatus,
    estimate_tokens,
)
from tests.llmfakes import (
    CATALOG_DOC,
    FLASH,
    GEMMA,
    GROQ,
    Router,
    answer,
    default_google_listing,
    discovered_router,
    google_answer,
    google_error,
    google_listing,
    groq_answer,
    groq_error,
    groq_listing,
    http,
    item,
    make_classifier,
    make_engine,
    probe_ok,
    quota_failure,
    validated_today,
)

if TYPE_CHECKING:
    from cyberkb.classify.llm import LLMClassifier
    from cyberkb.providers.http import HttpResponse
    from cyberkb.taxonomy import Taxonomy

DAY = "2026-10-07"
BODY = "# Nmap\n\nPort scanning and service detection with nmap during a penetration test.\n"


def _doc(ref: str = "doc-1", body: str = BODY) -> Document:
    return Document(ref=ref, stem=ref, body=body)


def _ok(ref: str = "doc-1") -> HttpResponse:
    return google_answer(answer(item(ref)))


def _groq_ok(ref: str = "doc-1", **kwargs: Any) -> HttpResponse:  # noqa: ANN401
    return groq_answer(answer(item(ref)), **kwargs)


def _status(classifier: LLMClassifier, key: str) -> str:
    for model in classifier.engine.model_report():
        if f"{model['provider']}:{model['api_id']}" == key:
            return str(model["status"])
    msg = f"no model {key}"
    raise AssertionError(msg)


def _model(classifier: LLMClassifier, key: str) -> dict[str, Any]:
    return next(
        m for m in classifier.engine.model_report() if f"{m['provider']}:{m['api_id']}" == key
    )


def test_discovery_resolves_the_catalog_and_validates_lazily(taxonomy: Taxonomy) -> None:
    """Only the first model is probed, on first use; the rest stay unvalidated."""
    router = discovered_router().add("google:gemma-t-it", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.result is not None
    assert single.result.provider == "google"
    assert single.result.model == "gemma-t-it"
    assert _status(classifier, GEMMA) == "active"
    assert _model(classifier, GEMMA)["mode"] == "json_schema"
    assert _status(classifier, FLASH) == "unvalidated"
    assert _status(classifier, GROQ) == "unvalidated"
    assert router.pending() == {}
    providers = classifier.engine.provider_report()
    assert providers["google"]["status"] == "up"
    assert providers["google"]["listed_models"] == 2
    assert providers["google"]["successes"] == 2


def test_listing_models_outside_the_catalog_are_reported_not_used(taxonomy: Taxonomy) -> None:
    """Extra live models are audited; excluded ones never become candidates."""
    router = (
        Router()
        .add(
            "google:list",
            google_listing(("gemma-t-it", "Gemma Test IT"), ("gemini-other", "Gemini Other")),
        )
        .add("groq:list", groq_listing("groq-a", "openai/gpt-oss-safeguard-20b"))
    )
    classifier, _ = make_classifier(router, taxonomy)
    report = classifier.engine.provider_report()
    assert report["google"]["listed_not_in_catalog"] == ["gemini-other"]
    assert report["groq"]["listed_not_in_catalog"] == ["openai/gpt-oss-safeguard-20b"]
    flash = next(
        m for m in classifier.engine.model_report() if m["declared_name"] == "Gemini Test Flash"
    )
    assert flash["status"] == "unresolved"
    assert flash["reason"] == "not listed by the provider"
    assert flash["usage_today"] is None


def test_rejected_key_fails_fast(taxonomy: Taxonomy) -> None:
    """An auth failure while listing stops the run before any classification."""
    router = Router().add("google:list", google_error(403, "PERMISSION_DENIED", "denied"))
    with pytest.raises(ProviderConfigError, match="rejected GEMINI_API_KEY"):
        make_classifier(router, taxonomy)


def test_a_failed_listing_takes_only_that_provider_out(taxonomy: Taxonomy) -> None:
    """A network failure listing Google leaves Groq to serve."""
    router = (
        Router()
        .add("google:list", HttpTransportError("unreachable", timeout=False))
        .add("groq:list", groq_listing("groq-a"))
        .add("groq:groq-a", groq_answer(answer(item("probe-nmap"))), _groq_ok())
    )
    classifier, _ = make_classifier(router, taxonomy)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.result is not None
    assert single.result.provider == "groq"
    google = classifier.engine.provider_report()["google"]
    assert google["status"] == "down"
    assert "network_error" in google["reason"]
    assert google["failure_categories"] == {"network_error": 1}


def test_mode_ladder_steps_down_on_rejected_requests(taxonomy: Taxonomy) -> None:
    """INVALID_ARGUMENT on native modes steps down to prompt mode, which then serves."""
    rejected = google_error(400, "INVALID_ARGUMENT", "JSON mode is not enabled for this model")
    router = discovered_router().add("google:gemma-t-it", rejected, rejected, probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    model = _model(classifier, GEMMA)
    assert model["mode"] == "prompt"
    trail = model["validation"]
    assert [step.get("mode") for step in trail] == ["json_schema", "response_schema", "prompt"]
    assert trail[-1]["result"] == "validated"
    served = router.bodies("google:gemma-t-it")[-1]
    assert "responseMimeType" not in served["generationConfig"]
    assert classifier.engine.validations()[GEMMA].mode == "prompt"


def test_every_mode_rejected_fails_the_model_and_the_next_one_serves(taxonomy: Taxonomy) -> None:
    """A model that accepts no request mode is skipped; priority 2 takes over."""
    rejected = google_error(400, "INVALID_ARGUMENT", "bad")
    router = discovered_router().add("google:gemma-t-it", rejected, rejected, rejected)
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.result is not None
    assert single.result.model == "gemini-test-flash"
    gemma = _model(classifier, GEMMA)
    assert gemma["status"] == "failed"
    assert "every structured-output request mode was rejected" in gemma["reason"]


@pytest.mark.parametrize(
    ("response", "reason"),
    [
        (google_answer(answer(item("probe-nmap", summary="I'm sorry, I can't help."))), "refusal"),
        (google_answer(answer(item("probe-nmap", category="astrology"))), "unknown category"),
        (google_answer(answer(item("other-ref"))), "no classification for ref"),
        (google_answer({"nothing": True}), "no classifications"),
        (google_error(404, "NOT_FOUND", "gone"), "gone"),
    ],
)
def test_failed_validation_is_permanent_for_the_day(
    taxonomy: Taxonomy, response: HttpResponse, reason: str
) -> None:
    """Garbage, refusals and missing models fail validation and are cached as failed."""
    router = discovered_router().add("google:gemma-t-it", response)
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    gemma = _model(classifier, GEMMA)
    assert gemma["status"] == "failed"
    assert reason in gemma["reason"]
    cached = classifier.engine.validations()[GEMMA]
    assert cached.ok is False
    assert cached.day == DAY


def test_transient_validation_failure_is_not_cached(taxonomy: Taxonomy) -> None:
    """A 503 during validation skips the model now but is not remembered for the day."""
    router = discovered_router().add("google:gemma-t-it", google_error(503, "UNAVAILABLE", "busy"))
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert _status(classifier, GEMMA) == "failed"
    assert GEMMA not in classifier.engine.validations()


def test_rate_limited_validation_is_postponed_not_failed(taxonomy: Taxonomy) -> None:
    """A 429 during validation cools the model; it is validated later, not rejected."""
    limited = google_error(
        429, "RESOURCE_EXHAUSTED", "quota", quota_failure("PerMinute", retry="20s")
    )
    router = discovered_router().add("google:gemma-t-it", limited)
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, time = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert _status(classifier, GEMMA) == "unvalidated"
    time.t += 21
    router.add("google:gemma-t-it", probe_ok(), _ok("doc-2"))
    second = classifier.classify_one(_doc("doc-2"), deadline=None)
    assert second.result is not None
    assert second.result.model == "gemma-t-it"


def test_auth_failure_during_validation_takes_the_provider_out(taxonomy: Taxonomy) -> None:
    """A key that lists but cannot generate disables its provider; Groq serves."""
    router = discovered_router().add(
        "google:gemma-t-it", google_error(403, "PERMISSION_DENIED", "no")
    )
    router.add("groq:groq-a", groq_answer(answer(item("probe-nmap"))), _groq_ok())
    classifier, _ = make_classifier(router, taxonomy)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.result is not None
    assert single.result.provider == "groq"
    assert classifier.engine.provider_report()["google"]["status"] == "down"
    assert classifier.engine.retry_summary()["per_provider"] == 0


def test_cached_validation_skips_the_probe(taxonomy: Taxonomy) -> None:
    """A model validated earlier today serves at once in its recorded mode."""
    validations = {
        GEMMA: CachedValidation(DAY, ok=True, mode="response_schema", category=None, detail="")
    }
    router = discovered_router().add("google:gemma-t-it", _ok())
    classifier, _ = make_classifier(router, taxonomy, validations=validations)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    body = router.bodies("google:gemma-t-it")[0]
    assert "responseSchema" in body["generationConfig"]
    assert _model(classifier, GEMMA)["validation"][0]["result"] == "reused from earlier today"


def test_cached_failure_skips_the_model_and_stale_verdicts_are_ignored(taxonomy: Taxonomy) -> None:
    """Today's failure is honoured; yesterday's verdict is not."""
    validations = {
        GEMMA: CachedValidation(
            DAY, ok=False, mode=None, category="inference_error", detail="junk"
        ),
        FLASH: CachedValidation("2026-10-06", ok=True, mode="prompt", category=None, detail=""),
    }
    router = discovered_router().add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy, validations=validations)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert _model(classifier, GEMMA)["reason"] == "junk"
    assert _model(classifier, FLASH)["mode"] == "json_schema"


def test_rate_limit_moves_on_immediately_and_the_model_rejoins_after_cooling(
    taxonomy: Taxonomy,
) -> None:
    """A per-minute 429 is not retried in place: the next model serves, then priority returns."""
    limited = google_error(
        429,
        "RESOURCE_EXHAUSTED",
        "You exceeded your current quota",
        quota_failure("GenerateRequestsPerMinutePerProjectPerModel-FreeTier", retry="30s"),
    )
    router = discovered_router().add("google:gemma-t-it", probe_ok(), limited)
    router.add("google:gemini-test-flash", probe_ok(), _ok(), _ok("doc-2"))
    classifier, time = make_classifier(router, taxonomy)
    first = classifier.classify_one(_doc(), deadline=None)
    assert first.result is not None
    assert first.result.model == "gemini-test-flash"
    assert time.sleeps == []
    second = classifier.classify_one(_doc("doc-2"), deadline=None)
    assert second.result is not None
    assert second.result.model == "gemini-test-flash"
    time.t += 31
    router.add("google:gemma-t-it", _ok("doc-3"))
    third = classifier.classify_one(_doc("doc-3"), deadline=None)
    assert third.result is not None
    assert third.result.model == "gemma-t-it"
    assert _model(classifier, GEMMA)["failure_categories"] == {"rate_limit": 1}


def test_repeated_rate_limits_take_the_model_out_for_the_pass(taxonomy: Taxonomy) -> None:
    """Three rate limits without a success retire the model until the next list pass."""
    settings = RotationSettings(rate_limit_escalation=2, default_cooldown=1.0)
    limited = google_error(429, "RESOURCE_EXHAUSTED", "slow", [])
    router = discovered_router().add("google:gemma-t-it", probe_ok(), limited, limited)
    router.add("google:gemini-test-flash", probe_ok(), _ok(), _ok("doc-2"))
    classifier, time = make_classifier(router, taxonomy, settings=settings)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    time.t += 2
    assert classifier.classify_one(_doc("doc-2"), deadline=None).result is not None
    gemma = _model(classifier, GEMMA)
    assert gemma["status"] == "failed"
    assert "consecutive rate limits" in gemma["reason"]


def test_daily_quota_exhausts_the_model_and_is_persisted(taxonomy: Taxonomy) -> None:
    """A per-day 429 retires the model for the quota day, recorded in its usage."""
    daily = google_error(
        429,
        "RESOURCE_EXHAUSTED",
        "quota",
        quota_failure("GenerateRequestsPerDayPerProjectPerModel-FreeTier"),
    )
    router = discovered_router().add("google:gemma-t-it", probe_ok(), daily)
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert _status(classifier, GEMMA) == "exhausted"
    usage = classifier.engine.usage()[GEMMA]
    assert usage.exhausted is True
    assert usage.requests == 2
    assert usage.day == DAY


def test_declared_daily_limit_is_respected_without_asking(taxonomy: Taxonomy) -> None:
    """Usage carried in from an earlier run counts against today's RPD."""
    usage = {GEMMA: DailyUsage(DAY, requests=100)}
    router = discovered_router().add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy, usage=usage)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    gemma = _model(classifier, GEMMA)
    assert gemma["status"] == "exhausted"
    assert gemma["reason"] == "daily quota reached"


def test_groq_reporting_no_requests_left_exhausts_after_the_answer(taxonomy: Taxonomy) -> None:
    """x-ratelimit-remaining-requests: 0 retires the model without another call."""
    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"] = [doc["providers"][1]]
    router = Router().add("groq:list", groq_listing("groq-a"))
    router.add("groq:groq-a", groq_answer(answer(item("probe-nmap"))), _groq_ok(remaining=0))
    classifier, _ = make_classifier(router, taxonomy, catalog_doc=doc)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert classifier.classify_one(_doc("doc-2"), deadline=None).outcome.status == "exhausted"
    assert classifier.engine.exhausted


def test_errors_are_retried_on_the_same_model_with_backoff(taxonomy: Taxonomy) -> None:
    """Transient errors retry in place with jittered exponential backoff."""
    busy = google_error(503, "UNAVAILABLE", "high demand")
    router = discovered_router().add("google:gemma-t-it", probe_ok(), busy, busy, _ok())
    classifier, time = make_classifier(router, taxonomy)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.result is not None
    assert single.result.model == "gemma-t-it"
    assert time.sleeps == [1.0, 2.0]
    assert classifier.engine.retry_summary()["per_model"] == 2


def test_server_retry_hint_overrides_backoff(taxonomy: Taxonomy) -> None:
    """A retry delay from the provider is honoured instead of the backoff."""
    timeout = google_error(504, "DEADLINE_EXCEEDED", "slow", quota_failure(retry="4s"))
    router = discovered_router().add("google:gemma-t-it", probe_ok(), timeout, _ok())
    classifier, time = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert time.sleeps == [4.0]


def test_exhausted_retries_retire_the_model_revivably(taxonomy: Taxonomy) -> None:
    """After X retries a transient failure moves the request to the next model."""
    settings = RotationSettings(model_retries=1)
    busy = google_error(500, "INTERNAL", "boom")
    router = discovered_router().add("google:gemma-t-it", probe_ok(), busy, busy)
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy, settings=settings)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.result is not None
    assert single.result.model == "gemini-test-flash"
    gemma = _model(classifier, GEMMA)
    assert gemma["status"] == "failed"
    assert gemma["last_error_category"] == "server_error"


def test_bad_answers_skip_the_model_for_that_request_only(taxonomy: Taxonomy) -> None:
    """An answer rejected for one document moves that document on; others still use the model."""
    settings = RotationSettings(model_retries=0)
    bad = google_answer(answer(item("doc-1", confidence=0.1)))
    router = discovered_router().add("google:gemma-t-it", probe_ok(), bad, _ok("doc-2"))
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy, settings=settings)
    first = classifier.classify_one(_doc(), deadline=None)
    assert first.result is not None
    assert first.result.model == "gemini-test-flash"
    second = classifier.classify_one(_doc("doc-2"), deadline=None)
    assert second.result is not None
    assert second.result.model == "gemma-t-it"
    assert _model(classifier, GEMMA)["failure_categories"] == {"inference_error": 1}


def test_a_model_failing_consecutive_requests_is_retired(taxonomy: Taxonomy) -> None:
    """Repeated per-request failures mean the model is broken, not the documents."""
    settings = RotationSettings(model_retries=0, resource_failure_limit=2)
    bad = google_answer("not json")
    router = discovered_router().add("google:gemma-t-it", probe_ok(), bad, bad)
    router.add("google:gemini-test-flash", probe_ok(), _ok(), _ok("doc-2"))
    classifier, _ = make_classifier(router, taxonomy, settings=settings)
    classifier.classify_one(_doc(), deadline=None)
    classifier.classify_one(_doc("doc-2"), deadline=None)
    gemma = _model(classifier, GEMMA)
    assert gemma["status"] == "failed"
    assert "2 consecutive requests" in gemma["reason"]


def test_content_filter_moves_the_request_without_retrying(taxonomy: Taxonomy) -> None:
    """A safety block is specific to the document: no retry, next model."""
    blocked = google_answer(answer(), finish="SAFETY")
    router = discovered_router().add("google:gemma-t-it", probe_ok(), blocked)
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, time = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert time.sleeps == []
    assert _status(classifier, GEMMA) == "active"


def test_rejected_request_after_validation_skips_only_that_request(taxonomy: Taxonomy) -> None:
    """An INVALID_ARGUMENT for one document does not retire a validated model."""
    router = discovered_router().add(
        "google:gemma-t-it", probe_ok(), google_error(400, "INVALID_ARGUMENT", "input too long")
    )
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert _status(classifier, GEMMA) == "active"


def test_a_vanished_model_is_retired(taxonomy: Taxonomy) -> None:
    """A 404 after validation retires the model for the run."""
    router = discovered_router().add(
        "google:gemma-t-it", probe_ok(), google_error(404, "NOT_FOUND", "gone")
    )
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert _status(classifier, GEMMA) == "failed"


def test_auth_failure_while_serving_fails_over_to_the_next_provider(taxonomy: Taxonomy) -> None:
    """A revoked key mid-run takes Google out; Groq serves; the failover is counted."""
    validations = {
        GEMMA: CachedValidation(DAY, ok=True, mode="json_schema", category=None, detail=""),
    }
    router = discovered_router().add(
        "google:gemma-t-it", google_error(401, "UNAUTHENTICATED", "revoked")
    )
    router.add("groq:groq-a", groq_answer(answer(item("probe-nmap"))), _groq_ok())
    classifier, _ = make_classifier(router, taxonomy, validations=validations)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.result is not None
    assert single.result.provider == "groq"
    assert classifier.engine.retry_summary()["per_provider"] == 1
    assert classifier.engine.provider_report()["google"]["status"] == "down"


def test_persistent_network_failure_takes_the_provider_out_until_the_next_pass(
    taxonomy: Taxonomy,
) -> None:
    """Network failure on Google, then Groq fails too: the list is walked again."""
    settings = RotationSettings(model_retries=0, list_passes=2, list_backoff=45.0)
    validations = {
        GEMMA: CachedValidation(DAY, ok=True, mode="json_schema", category=None, detail=""),
        GROQ: CachedValidation(DAY, ok=True, mode="json_schema", category=None, detail=""),
    }
    router = discovered_router()
    router.add("google:gemma-t-it", HttpTransportError("reset", timeout=False), _ok())
    router.add("groq:groq-a", groq_error(500, "oops"))
    classifier, time = make_classifier(router, taxonomy, settings=settings, validations=validations)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.result is not None
    assert single.result.model == "gemma-t-it"
    assert time.sleeps == [45.0]
    assert classifier.engine.retry_summary()["per_list"] == 1
    assert router.pending() == {}


def test_list_passes_are_bounded_then_the_engine_is_exhausted(taxonomy: Taxonomy) -> None:
    """With no list retry allowed, a fully failed list exhausts the engine for good."""
    settings = RotationSettings(model_retries=0, list_passes=1)
    busy = google_error(503, "UNAVAILABLE", "busy")
    router = discovered_router().add("google:gemma-t-it", busy)
    router.add("google:gemini-test-flash", busy)
    router.add("groq:groq-a", groq_error(503, "busy"))
    classifier, _ = make_classifier(router, taxonomy, settings=settings)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.result is None
    assert single.outcome.status == "exhausted"
    assert "every model is exhausted or failed" in single.outcome.detail
    assert classifier.engine.exhausted
    assert not classifier.engine.has_capacity()
    again = classifier.classify_one(_doc("doc-2"), deadline=None)
    assert again.outcome.status == "exhausted"


def test_revival_is_skipped_when_nothing_failed_transiently(taxonomy: Taxonomy) -> None:
    """Exhausted and permanently failed models are not revived by a list pass."""
    daily = google_error(429, "RESOURCE_EXHAUSTED", "q", quota_failure("PerDayX"))
    router = discovered_router().add("google:gemma-t-it", daily)
    router.add("google:gemini-test-flash", google_error(404, "NOT_FOUND", "gone"))
    router.add("groq:groq-a", groq_error(429, "x (RPD)"))
    classifier, time = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).outcome.status == "exhausted"
    assert time.sleeps == []


def test_a_request_every_usable_model_fails_is_failed_not_exhausted(taxonomy: Taxonomy) -> None:
    """When only this document is the problem, the outcome is a per-request failure."""
    settings = RotationSettings(model_retries=0)
    blocked = google_answer(answer(), finish="SAFETY")
    router = discovered_router().add("google:gemma-t-it", probe_ok(), blocked)
    router.add("google:gemini-test-flash", probe_ok(), blocked)
    router.add(
        "groq:groq-a",
        groq_answer(answer(item("probe-nmap"))),
        groq_answer("{}", finish="content_filter"),
    )
    classifier, _ = make_classifier(router, taxonomy, settings=settings)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.outcome.status == "failed"
    assert single.outcome.category is FailureCategory.CONTENT_FILTER
    assert not classifier.engine.exhausted


def test_paced_models_are_waited_for_when_nothing_else_is_ready(taxonomy: Taxonomy) -> None:
    """With every model at its RPM, the engine sleeps until the first frees up."""
    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"] = [doc["providers"][0]]
    doc["providers"][0]["models"] = [doc["providers"][0]["models"][0]]
    doc["providers"][0]["models"][0]["limits"]["rpm"] = 3  # paced at 2/min (90% headroom)
    router = Router().add("google:list", default_google_listing())
    router.add("google:gemma-t-it", probe_ok(), _ok(), _ok("doc-2"))
    classifier, time = make_classifier(router, taxonomy, catalog_doc=doc)
    classifier.classify_one(_doc(), deadline=None)
    second = classifier.classify_one(_doc("doc-2"), deadline=None)
    assert second.result is not None
    assert time.sleeps == [60.0]


def test_deadlines_defer_instead_of_starting_work(taxonomy: Taxonomy) -> None:
    """A spent budget, a wait past the deadline, or a retry past it all defer."""
    router = discovered_router()
    classifier, time = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=0.0).outcome.detail == "run budget reached"

    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"] = [doc["providers"][0]]
    doc["providers"][0]["models"] = [doc["providers"][0]["models"][0]]
    doc["providers"][0]["models"][0]["limits"]["rpm"] = 3
    paced = Router().add("google:list", default_google_listing())
    paced.add("google:gemma-t-it", probe_ok(), _ok())
    slow, time = make_classifier(paced, taxonomy, catalog_doc=doc)
    slow.classify_one(_doc(), deadline=None)
    outcome = slow.classify_one(_doc("doc-2"), deadline=time.t + 10).outcome
    assert outcome.status == "deferred"
    assert "paced" in outcome.detail

    busy = google_error(503, "UNAVAILABLE", "busy", quota_failure(retry="100s"))
    retry = discovered_router().add("google:gemma-t-it", probe_ok(), busy)
    retrying, time = make_classifier(retry, taxonomy)
    outcome = retrying.classify_one(_doc(), deadline=50.0).outcome
    assert outcome.status == "deferred"
    assert "retry" in outcome.detail
    assert time.sleeps == []


def test_validation_that_cannot_continue_before_the_deadline_defers(taxonomy: Taxonomy) -> None:
    """A paced model stepping down its mode ladder defers if the next call misses the budget."""
    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"] = [doc["providers"][0]]
    doc["providers"][0]["models"] = [doc["providers"][0]["models"][0]]
    doc["providers"][0]["models"][0]["limits"]["rpm"] = 1
    router = Router().add("google:list", default_google_listing())
    router.add("google:gemma-t-it", google_error(400, "INVALID_ARGUMENT", "no JSON mode"))
    classifier, time = make_classifier(router, taxonomy, catalog_doc=doc)
    outcome = classifier.classify_one(_doc(), deadline=time.t + 30).outcome
    assert outcome.status == "deferred"
    assert outcome.detail == "run budget reached in validation"
    assert _status(classifier, GEMMA) == "unvalidated"


def test_small_context_models_get_a_shortened_document(taxonomy: Taxonomy) -> None:
    """A 4K-context model receives a cut document and a quarter-window answer budget."""
    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"] = [doc["providers"][1]]
    router = Router().add("groq:list", groq_listing("groq-a", context=4096))
    long_body = "nmap " * 3000
    router.add("groq:groq-a", groq_answer(answer(item("probe-nmap"))), _groq_ok())
    classifier, _ = make_classifier(router, taxonomy, catalog_doc=doc)
    assert classifier.classify_one(_doc(body=long_body), deadline=None).result is not None
    served = router.bodies("groq:groq-a")[-1]
    assert served["max_completion_tokens"] == 1024
    sent = sum(len(m["content"]) for m in served["messages"])
    assert estimate_tokens(" " * sent) <= 4096 - 1024


def test_a_document_that_cannot_fit_any_model_fails(taxonomy: Taxonomy) -> None:
    """When no model can take even the minimum excerpt, the request fails per-request."""
    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"] = [doc["providers"][1]]
    router = Router().add("groq:list", groq_listing("groq-a", context=2900))
    classifier, _ = make_classifier(router, taxonomy, catalog_doc=doc)
    single = classifier.classify_one(_doc(), deadline=None)
    assert single.outcome.status == "failed"
    assert router.bodies("groq:groq-a") == []


def test_a_probe_that_does_not_fit_fails_validation(taxonomy: Taxonomy) -> None:
    """Validation fails cleanly for a model too small for the probe itself."""
    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"] = [doc["providers"][1]]
    router = Router().add("groq:list", groq_listing("groq-a", context=2900))
    classifier, _ = make_classifier(router, taxonomy, catalog_doc=doc)
    classifier.engine.validate_all()
    assert "does not fit" in _model(classifier, GROQ)["reason"]


def test_validate_all_probes_every_resolved_model(taxonomy: Taxonomy) -> None:
    """Preflight validates everything up front and reports each verdict."""
    router = discovered_router().add("google:gemma-t-it", probe_ok())
    router.add("google:gemini-test-flash", google_error(404, "NOT_FOUND", "gone"))
    router.add("groq:groq-a", groq_answer(answer(item("probe-nmap"))))
    classifier, _ = make_classifier(router, taxonomy)
    classifier.engine.validate_all()
    statuses = {
        f"{m['provider']}:{m['api_id']}": m["status"] for m in classifier.engine.model_report()
    }
    assert statuses == {GEMMA: "active", FLASH: "failed", GROQ: "active"}
    assert classifier.engine.has_capacity()
    assert classifier.engine.logger.attempts[0].mode == "json_schema"


def test_a_batch_request_accepts_any_well_formed_answer(taxonomy: Taxonomy) -> None:
    """Batch answers are validated per document by the classifier, not the engine."""
    router = discovered_router().add("google:gemma-t-it", probe_ok(), _ok("a"))
    classifier, _ = make_classifier(router, taxonomy)
    results = classifier.classify_batch([_doc("a"), _doc("b")])
    assert results[0].method == "llm"
    assert results[1].method == "heuristic"


def test_settings_backoff_is_capped() -> None:
    """Full-jittered exponential backoff is capped."""
    settings = RotationSettings(backoff_base=2.0, backoff_cap=10.0)
    assert settings.delay(1, 1.0) == 2.0
    assert settings.delay(3, 0.5) == 4.0
    assert settings.delay(9, 1.0) == 10.0


def test_slot_status_values_are_stable() -> None:
    """Report values are part of the audit format."""
    assert [s.value for s in SlotStatus] == [
        "unresolved",
        "unvalidated",
        "active",
        "exhausted",
        "failed",
    ]


def test_cached_validation_serialises() -> None:
    """The ledger shape of a cached verdict."""
    verdict = CachedValidation(DAY, ok=True, mode="prompt", category=None, detail="")
    assert verdict.to_dict()["mode"] == "prompt"


def test_engine_without_matching_adapters_has_no_capacity(taxonomy: Taxonomy) -> None:
    """An engine built with no adapters simply has nothing to offer."""
    engine, _ = make_engine(Router())
    engine._providers = []  # noqa: SLF001 - simulate a catalog with no available adapter
    engine.discover(
        GenerationRequest(
            system="s", schema={}, prompt_for=lambda n: "p" * n, check=lambda _payload: None
        )
    )
    assert not engine.has_capacity()
    _ = taxonomy


def test_preflight_skips_models_already_validated_today(taxonomy: Taxonomy) -> None:
    """validate_all probes only what is still unvalidated."""
    router = discovered_router().add("google:gemini-test-flash", probe_ok())
    router.add("groq:groq-a", groq_answer(answer(item("probe-nmap"))))
    classifier, _ = make_classifier(router, taxonomy, validations=validated_today(GEMMA))
    classifier.engine.validate_all()
    assert router.bodies("google:gemma-t-it") == []
    assert router.pending() == {}


def test_models_without_listed_limits_and_answers_without_usage(taxonomy: Taxonomy) -> None:
    """No context window and no usage figures fall back to the declared limits and estimate."""
    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"] = [doc["providers"][1]]
    listing = http(200, {"data": [{"id": "groq-a", "active": True}]})
    router = Router().add("groq:list", listing)
    no_usage = http(
        200,
        {
            "choices": [
                {"finish_reason": "stop", "message": {"content": json.dumps(answer(item()))}}
            ]
        },
    )
    router.add("groq:groq-a", no_usage, _groq_ok())
    classifier, _ = make_classifier(router, taxonomy, catalog_doc=doc)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert router.bodies("groq:groq-a")[-1]["max_completion_tokens"] == 4096
    assert classifier.engine.usage()[GROQ].requests == 2


def _paced_gemma() -> dict[str, Any]:
    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"] = [doc["providers"][0]]
    doc["providers"][0]["models"] = [doc["providers"][0]["models"][0]]
    doc["providers"][0]["models"][0]["limits"]["rpm"] = 3  # paced at 2/min (90% headroom)
    return doc


def test_a_retry_waits_for_pacing_when_the_window_is_full(taxonomy: Taxonomy) -> None:
    """Retries respect the model's RPM too: backoff first, then the window."""
    busy = google_error(503, "UNAVAILABLE", "busy")
    router = Router().add("google:list", default_google_listing())
    router.add("google:gemma-t-it", probe_ok(), busy, _ok())
    classifier, time = make_classifier(router, taxonomy, catalog_doc=_paced_gemma())
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    assert time.sleeps == [1.0, 59.0]


def test_a_retry_that_would_wait_past_the_deadline_defers(taxonomy: Taxonomy) -> None:
    """If pacing would push a retry past the budget, the request is deferred."""
    busy = google_error(503, "UNAVAILABLE", "busy")
    router = Router().add("google:list", default_google_listing())
    router.add("google:gemma-t-it", probe_ok(), busy)
    classifier, time = make_classifier(router, taxonomy, catalog_doc=_paced_gemma())
    outcome = classifier.classify_one(_doc(), deadline=30.0).outcome
    assert outcome.status == "deferred"
    assert outcome.detail == "run budget reached in a retry"
    assert time.sleeps == [1.0]


def test_a_blocked_groq_model_does_not_take_the_provider_out(taxonomy: Taxonomy) -> None:
    """Live finding: allam-2-7b was blocked for the project; the next Groq model serves."""
    doc = copy.deepcopy(CATALOG_DOC)
    groq = doc["providers"][1]
    groq["models"].append(
        {"name": "groq-b", "limits": {"rpm": 30, "rpd": 100, "tpm": 60000}},
    )
    doc["providers"] = [groq]
    router = Router().add("groq:list", groq_listing("groq-a", "groq-b"))
    router.add(
        "groq:groq-a",
        groq_error(403, "blocked at the project level", code="model_permission_blocked_project"),
    )
    router.add("groq:groq-b", groq_answer(answer(item("probe-nmap"))))
    classifier, _ = make_classifier(router, taxonomy, catalog_doc=doc)
    classifier.engine.validate_all()
    statuses = [m["status"] for m in classifier.engine.model_report()]
    assert statuses == ["failed", "active"]
    assert classifier.engine.provider_report()["groq"]["status"] == "up"


def test_an_internal_error_in_one_mode_steps_down_the_ladder(taxonomy: Taxonomy) -> None:
    """Live finding: Gemma 4 31B answered 500 in native JSON mode; a simpler mode may work."""
    internal = google_error(500, "INTERNAL", "Internal error encountered.")
    router = discovered_router().add("google:gemma-t-it", internal, probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    gemma = _model(classifier, GEMMA)
    assert gemma["mode"] == "response_schema"
    assert classifier.engine.validations()[GEMMA].ok


def test_internal_errors_in_every_mode_leave_the_model_revivable(taxonomy: Taxonomy) -> None:
    """If every mode fails with a 500, the model is skipped now but not written off for the day."""
    internal = google_error(500, "INTERNAL", "Internal error encountered.")
    router = discovered_router().add("google:gemma-t-it", internal, internal, internal)
    router.add("google:gemini-test-flash", probe_ok(), _ok())
    classifier, _ = make_classifier(router, taxonomy)
    assert classifier.classify_one(_doc(), deadline=None).result is not None
    gemma = _model(classifier, GEMMA)
    assert gemma["status"] == "failed"
    assert "internal server error" in gemma["reason"]
    assert GEMMA not in classifier.engine.validations()
