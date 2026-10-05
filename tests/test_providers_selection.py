"""Tests for model discovery, validation and ranking (the pre-flight selection)."""

from __future__ import annotations

import io
import json
from typing import TYPE_CHECKING, Any

from cyberkb.obslog import StructuredLogger
from cyberkb.providers.gemini import GeminiProvider
from cyberkb.providers.huggingface import HuggingFaceProvider
from cyberkb.providers.openrouter import OpenRouterProvider
from cyberkb.providers.selection import (
    DEFAULT_MAX_CANDIDATES,
    DEFAULT_NEED,
    ValidationRequest,
    select_models,
)
from tests.conftest import FakeTransport, http_json, http_text

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from cyberkb.providers.http import HttpResponse, HttpTransportError

    _Item = HttpResponse | HttpTransportError


def _clock() -> Callable[[], float]:
    state = {"v": 0.0}

    def tick() -> float:
        state["v"] += 1.0
        return state["v"]

    return tick


def _openrouter(*items: _Item) -> OpenRouterProvider:
    return OpenRouterProvider("key", transport=FakeTransport(*items), clock=_clock())


def _hf(*items: _Item) -> HuggingFaceProvider:
    return HuggingFaceProvider("key", transport=FakeTransport(*items), clock=_clock())


def _gemini(*items: _Item) -> GeminiProvider:
    return GeminiProvider("key", transport=FakeTransport(*items), clock=_clock())


def _chat(content: str) -> dict[str, object]:
    return {"choices": [{"finish_reason": "stop", "message": {"content": content}}]}


def _request(
    samples: list[str],
    validate: Callable[[Mapping[str, Any]], bool],
    *,
    need: int = DEFAULT_NEED,
    max_candidates: int = DEFAULT_MAX_CANDIDATES,
) -> ValidationRequest:
    return ValidationRequest(
        system="sys",
        samples=samples,
        schema={"type": "object"},
        validate=validate,
        need=need,
        max_candidates=max_candidates,
    )


def _ok(_payload: Mapping[str, Any]) -> bool:
    return True


def test_discovery_failure_is_recorded_and_unhealthy() -> None:
    """A provider whose catalog call fails yields an error selection and bad health."""
    provider = _openrouter(http_text(401, "invalid key"))
    selection = select_models(provider, _request(["p"], _ok))
    assert selection.accepted_models() == []
    assert selection.error.startswith("discovery failed (auth_error)")
    assert selection.as_health().ok is False


def test_validates_and_accepts_a_good_model() -> None:
    """A discovered free model whose sample answer passes is accepted."""
    listing = {"data": [{"id": "qwen/qwen-2.5-7b-instruct:free", "context_length": 32_000}]}
    answer = _chat(json.dumps({"classifications": [{"category": "offensive-security"}]}))
    provider = _openrouter(http_json(200, listing), http_json(200, answer))
    request = _request(["p"], lambda p: bool(p.get("classifications")), need=1, max_candidates=1)
    selection = select_models(provider, request)
    assert selection.accepted_models() == ["qwen/qwen-2.5-7b-instruct:free"]
    health = selection.as_health()
    assert health.ok is True
    assert health.model == "qwen/qwen-2.5-7b-instruct:free"


def test_rejects_model_whose_validation_call_fails() -> None:
    """A model whose validation call errors is rejected with the categorised reason."""
    listing = {"data": [{"id": "qwen/qwen-2.5-7b-instruct:free"}]}
    provider = _openrouter(http_json(200, listing), http_text(429, "slow down"))
    selection = select_models(provider, _request(["p"], _ok, need=1, max_candidates=1))
    assert selection.accepted_models() == []
    assert "rate_limit" in selection.validations[0].reason
    assert selection.as_health().detail == selection.validations[0].reason


def test_rejects_model_with_poor_output() -> None:
    """A model whose output fails the quality predicate is rejected."""
    listing = {"data": [{"id": "qwen/qwen-2.5-7b-instruct:free"}]}
    provider = _openrouter(http_json(200, listing), http_json(200, _chat("{}")))
    request = _request(["p"], lambda p: "classifications" in p, need=1, max_candidates=1)
    selection = select_models(provider, request)
    assert selection.accepted_models() == []
    assert "format/quality" in selection.validations[0].reason


def test_multi_sample_requires_all_to_pass() -> None:
    """A model that passes one sample but fails another is rejected, counting passes."""
    listing = {"data": [{"id": "qwen/qwen-2.5-7b-instruct:free"}]}
    provider = _openrouter(
        http_json(200, listing),
        http_json(200, _chat('{"good": 1}')),
        http_json(200, _chat("{}")),
    )
    request = _request(["p1", "p2"], lambda p: "good" in p, need=1, max_candidates=1)
    selection = select_models(provider, request)
    validation = selection.validations[0]
    assert validation.accepted is False
    assert validation.samples_passed == 1
    assert validation.samples_total == 2
    assert validation.avg_latency_s is not None


def test_skips_model_reported_unavailable() -> None:
    """A Hugging Face model the status endpoint reports cold is skipped as unavailable."""
    listing = {"data": [{"id": "Qwen/Qwen2.5-7B-Instruct"}]}
    provider = _hf(http_json(200, listing), http_json(200, {"state": "TooBig"}))
    selection = select_models(provider, _request(["p"], _ok, need=1, max_candidates=1))
    assert selection.accepted_models() == []
    assert "not available" in selection.validations[0].reason


def test_empty_catalog_is_unhealthy_with_clear_detail() -> None:
    """A provider that discovers nothing reports 'no models discovered'."""
    provider = _gemini(http_json(200, {"models": []}))
    selection = select_models(provider, _request(["p"], _ok))
    assert selection.validations == ()
    assert selection.as_health().detail == "no models discovered"


def test_validation_attempts_are_logged() -> None:
    """Each validation call is emitted through the structured logger."""
    listing = {"data": [{"id": "qwen/qwen-2.5-7b-instruct:free"}]}
    answer = _chat('{"classifications": []}')
    provider = _openrouter(http_json(200, listing), http_json(200, answer))
    logger = StructuredLogger(io.StringIO())
    request = _request(["p"], lambda p: "classifications" in p, need=1, max_candidates=1)
    select_models(provider, request, logger=logger)
    assert [a.resource_id for a in logger.attempts] == ["__validation__"]
    assert logger.attempts[0].outcome == "success"


def test_selection_serialises_for_the_report() -> None:
    """ProviderSelection and ModelValidation serialise their fields for the report."""
    listing = {"data": [{"id": "qwen/qwen-2.5-7b-instruct:free"}]}
    answer = _chat('{"classifications": []}')
    provider = _openrouter(http_json(200, listing), http_json(200, answer))
    request = _request(["p"], lambda p: "classifications" in p, need=1, max_candidates=1)
    data = select_models(provider, request).to_dict()
    assert data["provider"] == "openrouter"
    assert data["accepted"] == ["qwen/qwen-2.5-7b-instruct:free"]
    assert data["validations"][0]["accepted"] is True
