"""Tests for assembling the multi-provider classifier from configuration."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from cyberkb.config import IngestConfig
from cyberkb.pipeline import _validator, build_classifier, build_orchestrator
from cyberkb.providers.http import HttpResponse, UrllibTransport

if TYPE_CHECKING:
    from collections.abc import Mapping

    from cyberkb.taxonomy import Taxonomy

_GEMINI_LISTING = {
    "models": [
        {"name": "models/gemini-2.5-flash", "supportedGenerationMethods": ["generateContent"]},
        {"name": "models/gemini-2.5-flash-lite", "supportedGenerationMethods": ["generateContent"]},
    ],
}


def _envelope_bytes() -> bytes:
    item = {
        "ref": "probe",
        "title": "T",
        "category": "offensive-security",
        "format": "guide",
        "language": "en",
        "tags": [],
        "summary": "ok",
        "confidence": 0.9,
    }
    text = json.dumps({"classifications": [item]})
    return json.dumps({"candidates": [{"content": {"parts": [{"text": text}]}}]}).encode()


def _fake_request(
    valid: bool,  # noqa: FBT001 - internal test helper flag
) -> object:
    def request(
        _self: UrllibTransport,
        method: str,
        _url: str,
        *,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout: float,
    ) -> HttpResponse:
        _ = (headers, body, timeout)
        if method == "GET":
            return HttpResponse(200, json.dumps(_GEMINI_LISTING).encode())
        return HttpResponse(200, _envelope_bytes()) if valid else HttpResponse(500, b"boom")

    return request


def test_validator_accepts_a_usable_on_taxonomy_answer(taxonomy: Taxonomy) -> None:
    """A batch answer with a real category and a non-empty summary is accepted."""
    validate = _validator(taxonomy)
    payload = {"classifications": [{"category": "offensive-security", "summary": "s"}]}
    assert validate(payload) is True


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"classifications": "nope"},
        {"classifications": []},
        {"classifications": ["not-a-dict"]},
        {"classifications": [{"category": "does-not-exist", "summary": "s"}]},
        {"classifications": [{"category": "uncategorized", "summary": "s"}]},
        {"classifications": [{"category": "offensive-security", "summary": "  "}]},
    ],
)
def test_validator_rejects_unusable_answers(taxonomy: Taxonomy, payload: dict[str, object]) -> None:
    """Malformed, off-taxonomy, staging or empty-summary answers are rejected."""
    assert _validator(taxonomy)(payload) is False


def test_build_classifier_without_providers_is_heuristic(taxonomy: Taxonomy) -> None:
    """With no provider keys the pipeline returns no classifier and no orchestrator."""
    assert build_classifier(taxonomy, IngestConfig.from_env({})) == (None, None)


def test_build_orchestrator_builds_providers_in_order(taxonomy: Taxonomy) -> None:
    """Providers are constructed in the configured fallback order."""
    _ = taxonomy
    config = IngestConfig.from_env(
        {
            "GEMINI_API_KEY": "g",
            "OPENROUTER_API_KEY": "o",
            "LLM_PROVIDER_ORDER": "openrouter,gemini",
        },
    )
    orchestrator = build_orchestrator(config)
    assert [p.name for p in orchestrator._providers] == ["openrouter", "gemini"]  # noqa: SLF001


def test_build_classifier_validates_and_reports_capacity(
    taxonomy: Taxonomy,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A provider whose models pass validation yields a usable classifier."""
    monkeypatch.setattr(UrllibTransport, "request", _fake_request(valid=True))
    config = IngestConfig.from_env({"GEMINI_API_KEY": "k"})
    classifier, orchestrator = build_classifier(taxonomy, config)
    assert classifier is not None
    assert orchestrator is not None
    assert orchestrator.has_capacity() is True
    assert orchestrator.health()[0].ok is True


def test_build_classifier_no_capacity_when_models_fail(
    taxonomy: Taxonomy,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When validation calls fail, no model is usable and the heuristic is used."""
    monkeypatch.setattr(UrllibTransport, "request", _fake_request(valid=False))
    config = IngestConfig.from_env({"GEMINI_API_KEY": "k"})
    classifier, orchestrator = build_classifier(taxonomy, config)
    assert classifier is None
    assert orchestrator is not None
    assert orchestrator.has_capacity() is False
