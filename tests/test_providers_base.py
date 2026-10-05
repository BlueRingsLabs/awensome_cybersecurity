"""Tests for the shared provider base: status mapping and HTTP helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, override

import pytest

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.providers.base import (
    HealthResult,
    HttpProviderBase,
    ModelCandidate,
    ProviderResult,
    classify_http_status,
    retry_after_seconds,
)
from cyberkb.providers.http import HttpResponse, HttpTransportError
from tests.conftest import FakeTransport, http_json, http_text

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping


def _ticking_clock() -> Callable[[], float]:
    state = {"t": 0.0}

    def tick() -> float:
        state["t"] += 1.0
        return state["t"]

    return tick


class _StubProvider(HttpProviderBase):
    """A concrete provider that drives the shared helpers against a fake transport."""

    name: ClassVar[str] = "stub"

    @override
    def discover_models(self) -> list[ModelCandidate]:
        return []

    @override
    def complete_json(
        self, model: str, system: str, prompt: str, schema: Mapping[str, object]
    ) -> ProviderResult:
        _ = (system, prompt, schema)
        start = self._clock()
        response = self._send("POST", "https://stub/call", headers={}, body=b"{}", model=model)
        if response.status != 200:
            raise self._fail(
                classify_http_status(response.status, response.text()),
                raw=response.text(),
                status=response.status,
                model=model,
            )
        payload = self._decode_object(response.text(), model=model)
        return ProviderResult(payload, self.name, model, self._elapsed(start))


def _stub(*items: HttpResponse | HttpTransportError) -> _StubProvider:
    return _StubProvider("key", transport=FakeTransport(*items), clock=_ticking_clock())


@pytest.mark.parametrize(
    ("status", "body", "expected"),
    [
        (401, "", FailureCategory.AUTH_ERROR),
        (403, "forbidden", FailureCategory.AUTH_ERROR),
        (403, "billing quota exceeded", FailureCategory.QUOTA_EXCEEDED),
        (429, "slow down", FailureCategory.RATE_LIMIT),
        (429, "you have exceeded your credit balance", FailureCategory.QUOTA_EXCEEDED),
        (402, "", FailureCategory.QUOTA_EXCEEDED),
        (408, "", FailureCategory.TIMEOUT),
        (400, "bad model", FailureCategory.MODEL_UNAVAILABLE),
        (404, "no such model", FailureCategory.MODEL_UNAVAILABLE),
        (500, "", FailureCategory.SERVER_ERROR),
        (503, "", FailureCategory.SERVER_ERROR),
        (418, "teapot", FailureCategory.UNKNOWN),
    ],
)
def test_classify_http_status(status: int, body: str, expected: FailureCategory) -> None:
    """Each status (and quota hint) maps to the documented failure category."""
    assert classify_http_status(status, body) is expected


def test_retry_after_parses_seconds() -> None:
    """A numeric Retry-After header is parsed to a float."""
    assert retry_after_seconds({"Retry-After": "12"}) == 12.0


def test_retry_after_invalid_is_none() -> None:
    """A non-numeric Retry-After (HTTP-date form) yields None rather than raising."""
    assert retry_after_seconds({"retry-after": "Wed, 21 Oct 2026 07:28:00 GMT"}) is None


def test_retry_after_absent_is_none() -> None:
    """No Retry-After header yields None."""
    assert retry_after_seconds({"Content-Type": "application/json"}) is None


def test_model_candidate_to_dict_rounds_score() -> None:
    """ModelCandidate serialises its fields and rounds the score."""
    candidate = ModelCandidate(
        provider="gemini",
        model_id="gemini-2.5-flash",
        is_free=True,
        context_window=1_000_000,
        score=0.90123,
        rationale="why",
    )
    assert candidate.to_dict() == {
        "provider": "gemini",
        "model_id": "gemini-2.5-flash",
        "is_free": True,
        "context_window": 1_000_000,
        "score": 0.901,
        "rationale": "why",
    }


def test_health_result_to_dict_serialises_category() -> None:
    """HealthResult serialises an enum category to its string value."""
    result = HealthResult(
        provider="gemini",
        model="m",
        ok=False,
        latency_s=0.5,
        category=FailureCategory.AUTH_ERROR,
    )
    assert result.to_dict()["category"] == "auth_error"
    assert result.to_dict()["ok"] is False


def test_is_configured_tracks_api_key() -> None:
    """A provider is configured iff it has a non-empty API key."""
    assert _StubProvider("key").is_configured() is True
    assert _StubProvider("").is_configured() is False


def test_available_defaults_to_true() -> None:
    """The base availability pre-check assumes a model is callable."""
    assert _StubProvider("key").available("anything") is True


def test_health_check_success_reports_latency() -> None:
    """A healthy probe returns ok with a measured latency."""
    provider = _stub(http_json(200, {"status": "ok"}))
    result = provider.health_check("m")
    assert result.ok is True
    assert result.provider == "stub"
    assert result.latency_s > 0


def test_health_check_failure_carries_category_and_detail() -> None:
    """A failed probe reports the categorised cause and the provider's text."""
    provider = _stub(http_text(401, "invalid api key"))
    result = provider.health_check("m")
    assert result.ok is False
    assert result.category is FailureCategory.AUTH_ERROR
    assert result.detail == "invalid api key"


def test_send_maps_timeout_fault() -> None:
    """A transport timeout becomes a TIMEOUT ProviderError."""
    provider = _stub(HttpTransportError("timed out", timeout=True))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.TIMEOUT


def test_send_maps_network_fault() -> None:
    """A non-timeout transport fault becomes a NETWORK_ERROR ProviderError."""
    provider = _stub(HttpTransportError("refused", timeout=False))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.NETWORK_ERROR


def test_get_mapping_non_200_raises_categorised() -> None:
    """A non-200 on a GET is raised as a categorised ProviderError."""
    provider = _stub(http_text(503, "overloaded"))
    with pytest.raises(ProviderError) as exc:
        provider._get_mapping("https://stub/models", headers={})  # noqa: SLF001
    assert exc.value.category is FailureCategory.SERVER_ERROR


def test_decode_object_rejects_non_json() -> None:
    """A 200 body that is not JSON is an inference error."""
    provider = _stub(http_text(200, "not json at all"))
    with pytest.raises(ProviderError) as exc:
        provider._get_mapping("https://stub/models", headers={})  # noqa: SLF001
    assert exc.value.category is FailureCategory.INFERENCE_ERROR


def test_decode_object_rejects_non_object() -> None:
    """A 200 body that is valid JSON but not an object is an inference error."""
    provider = _stub(http_json(200, [1, 2, 3]))
    with pytest.raises(ProviderError) as exc:
        provider._get_mapping("https://stub/models", headers={})  # noqa: SLF001
    assert exc.value.category is FailureCategory.INFERENCE_ERROR


def test_complete_json_success_returns_payload() -> None:
    """The stub's happy path returns the decoded payload and provenance."""
    provider = _stub(http_json(200, {"classifications": []}))
    result = provider.complete_json("m", "s", "p", {})
    assert result.payload == {"classifications": []}
    assert result.provider == "stub"
    assert result.model == "m"
    assert result.latency_s > 0
