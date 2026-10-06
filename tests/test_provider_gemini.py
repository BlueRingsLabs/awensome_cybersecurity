"""Tests for the Gemini provider: discovery ranking and structured calls."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.providers.gemini import GeminiProvider
from tests.conftest import FakeTransport, http_json, http_text

if TYPE_CHECKING:
    from collections.abc import Callable

    from cyberkb.providers.http import HttpResponse, HttpTransportError


def _clock() -> Callable[[], float]:
    state = {"v": 0.0}

    def tick() -> float:
        state["v"] += 1.0
        return state["v"]

    return tick


def _gemini(*items: HttpResponse | HttpTransportError) -> tuple[GeminiProvider, FakeTransport]:
    transport = FakeTransport(*items)
    return GeminiProvider("key", transport=transport, clock=_clock()), transport


def _model(name: str, methods: object = ("generateContent",), **extra: object) -> dict[str, object]:
    resolved = list(methods) if isinstance(methods, tuple) else methods
    return {"name": name, "supportedGenerationMethods": resolved, **extra}


def _envelope(text: str, finish: str = "STOP") -> dict[str, object]:
    return {"candidates": [{"finishReason": finish, "content": {"parts": [{"text": text}]}}]}


def test_discover_ranks_flash_first_and_filters_non_text() -> None:
    """Discovery keeps generateContent text models and ranks Flash/latest highest."""
    listing = {
        "models": [
            _model("models/gemini-2.5-pro"),
            _model("models/gemini-2.5-flash-lite", methods=["generateContent", "countTokens"]),
            _model("models/gemini-flash-latest", inputTokenLimit=1_000_000),
            _model("models/gemini-2.5-flash"),
            _model("models/gemini-exp-1206"),
            _model("models/gemini-embedding-001", methods=["embedContent"]),
            _model("models/text-bison-001"),
            _model("models/gemini-2.0-flash", methods=["generateText"]),
            _model("models/gemini-vision-pro"),
            "not-a-dict",
            {"supportedGenerationMethods": ["generateContent"]},
            {"name": 123, "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-x", "supportedGenerationMethods": "generateContent"},
        ],
    }
    provider, _ = _gemini(http_json(200, listing))
    candidates = provider.discover_models()
    assert [c.model_id for c in candidates] == [
        "gemini-flash-latest",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.5-pro",
        "gemini-exp-1206",
    ]
    by_id = {c.model_id: c for c in candidates}
    assert by_id["gemini-2.5-pro"].is_free is False
    assert by_id["gemini-2.5-flash"].is_free is True
    assert by_id["gemini-flash-latest"].context_window == 1_000_000
    assert by_id["gemini-2.5-flash"].context_window is None


def test_discover_handles_missing_models_key() -> None:
    """A listing without a models array yields no candidates, not an error."""
    provider, _ = _gemini(http_json(200, {}))
    assert provider.discover_models() == []


def test_complete_json_sends_schema_and_returns_payload() -> None:
    """A successful call sends a schema-constrained request and returns the JSON."""
    answer = {"classifications": [{"ref": "0", "category": "offensive-security"}]}
    provider, transport = _gemini(http_json(200, _envelope(json.dumps(answer))))
    result = provider.complete_json("gemini-2.5-flash", "sys", "prompt", {"type": "object"})
    assert result.payload == answer
    assert result.provider == "gemini"
    assert result.model == "gemini-2.5-flash"
    assert result.latency_s > 0
    sent = json.loads(transport.calls[0][2] or b"{}")
    assert sent["generationConfig"]["responseSchema"] == {"type": "object"}
    assert sent["systemInstruction"]["parts"][0]["text"] == "sys"
    assert transport.calls[0][1].endswith("/models/gemini-2.5-flash:generateContent")


def test_complete_json_maps_http_status() -> None:
    """A 429 with no quota hint is a rate-limit ProviderError."""
    provider, _ = _gemini(http_text(429, "slow down"))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.RATE_LIMIT


def test_complete_json_blocked_prompt_is_content_filter() -> None:
    """No candidate with a blockReason is a content-filter failure."""
    blocked = {"candidates": [], "promptFeedback": {"blockReason": "SAFETY"}}
    provider, _ = _gemini(http_json(200, blocked))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.CONTENT_FILTER


def test_complete_json_no_candidate_no_block_is_inference_error() -> None:
    """No candidate and no blockReason is an inference error."""
    provider, _ = _gemini(http_json(200, {"candidates": []}))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.INFERENCE_ERROR


def test_complete_json_safety_finish_is_content_filter() -> None:
    """A SAFETY finish reason is a content-filter failure."""
    provider, _ = _gemini(http_json(200, _envelope("{}", finish="SAFETY")))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.CONTENT_FILTER


def test_complete_json_truncated_finish_is_inference_error() -> None:
    """A MAX_TOKENS (non-block) finish reason is an inference error."""
    provider, _ = _gemini(http_json(200, _envelope("{}", finish="MAX_TOKENS")))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.INFERENCE_ERROR


def test_complete_json_missing_text_parts_is_inference_error() -> None:
    """A candidate with no usable text parts is an inference error."""
    envelope = {"candidates": [{"finishReason": "STOP", "content": {"parts": [{"inlineData": 1}]}}]}
    provider, _ = _gemini(http_json(200, envelope))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.INFERENCE_ERROR


def test_complete_json_non_json_content_is_inference_error() -> None:
    """Candidate text that is not a JSON object is an inference error."""
    provider, _ = _gemini(http_json(200, _envelope("this is not json")))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.INFERENCE_ERROR


def test_complete_json_candidate_not_a_mapping_is_inference_error() -> None:
    """A candidate that is not a mapping cannot yield parts and is an inference error."""
    provider, _ = _gemini(http_json(200, {"candidates": ["oops"]}))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.INFERENCE_ERROR


def test_complete_json_content_not_a_mapping_is_inference_error() -> None:
    """A candidate whose content is not a mapping yields no parts (inference error)."""
    envelope = {"candidates": [{"finishReason": "STOP", "content": "nope"}]}
    provider, _ = _gemini(http_json(200, envelope))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.INFERENCE_ERROR
