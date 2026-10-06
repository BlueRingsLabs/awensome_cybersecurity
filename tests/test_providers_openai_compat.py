"""Tests for the OpenAI-compatible providers (OpenRouter, Hugging Face) + registry."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.providers.huggingface import HuggingFaceProvider
from cyberkb.providers.openai_compat import _unfence
from cyberkb.providers.openrouter import OpenRouterProvider
from cyberkb.providers.registry import PROVIDER_CLASSES, is_registered, provider_names
from tests.conftest import FakeTransport, http_json, http_text

if TYPE_CHECKING:
    from collections.abc import Callable

    from cyberkb.providers.http import HttpResponse, HttpTransportError

    _Item = HttpResponse | HttpTransportError


def _clock() -> Callable[[], float]:
    state = {"v": 0.0}

    def tick() -> float:
        state["v"] += 1.0
        return state["v"]

    return tick


def _openrouter(*items: _Item) -> tuple[OpenRouterProvider, FakeTransport]:
    transport = FakeTransport(*items)
    return OpenRouterProvider("key", transport=transport, clock=_clock()), transport


def _hf(*items: _Item) -> tuple[HuggingFaceProvider, FakeTransport]:
    transport = FakeTransport(*items)
    return HuggingFaceProvider("key", transport=transport, clock=_clock()), transport


def _chat(content: str, finish: str = "stop") -> dict[str, object]:
    return {"choices": [{"finish_reason": finish, "message": {"content": content}}]}


# --- _unfence -------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ('{"a": 1}', '{"a": 1}'),
        ('```json\n{"a": 1}\n```', '{"a": 1}'),
        ('```\n{"a": 1}', '{"a": 1}'),
        ("```", ""),
    ],
)
def test_unfence(raw: str, expected: str) -> None:
    """Code fences are stripped; plain text and odd fences are handled."""
    assert _unfence(raw) == expected


# --- OpenRouter -----------------------------------------------------------


def test_openrouter_discovers_free_models_and_appends_router() -> None:
    """Only free models are kept, ranked by family+context, with the router last."""
    listing = {
        "data": [
            {"id": "meta-llama/llama-3.3-70b-instruct:free", "context_length": 128_000},
            {
                "id": "qwen/qwen-2.5-7b-instruct",
                "pricing": {"prompt": "0", "completion": "0"},
                "context_length": 32_768,
            },
            {"id": "openai/gpt-4o", "pricing": {"prompt": "0.0000025", "completion": "0.00001"}},
            {"id": "some/model-base:free"},
            "not-a-dict",
            {"id": 123},
            {"id": "cohere/command-r:free"},
            {"id": "mystery/thing", "pricing": {}},
        ],
    }
    provider, _ = _openrouter(http_json(200, listing))
    candidates = provider.discover_models()
    assert [c.model_id for c in candidates] == [
        "meta-llama/llama-3.3-70b-instruct:free",
        "qwen/qwen-2.5-7b-instruct",
        "cohere/command-r:free",
        "openrouter/auto",
    ]
    assert all(c.is_free for c in candidates)
    assert "last resort" in candidates[-1].rationale


def test_openrouter_complete_json_sends_json_mode_and_schema() -> None:
    """A successful call embeds the schema in the system message and requests JSON mode."""
    answer: dict[str, object] = {"classifications": []}
    provider, transport = _openrouter(http_json(200, _chat(json.dumps(answer))))
    result = provider.complete_json(
        "qwen/qwen-2.5-7b-instruct", "sys", "prompt", {"type": "object"}
    )
    assert result.payload == answer
    assert result.provider == "openrouter"
    sent = json.loads(transport.calls[0][2] or b"{}")
    assert sent["model"] == "qwen/qwen-2.5-7b-instruct"
    assert sent["response_format"] == {"type": "json_object"}
    assert '"type": "object"' in sent["messages"][0]["content"]
    assert sent["messages"][1]["content"] == "prompt"


def test_openrouter_complete_json_unfences_content() -> None:
    """A fenced JSON answer is unwrapped before parsing."""
    provider, _ = _openrouter(http_json(200, _chat('```json\n{"classifications": []}\n```')))
    result = provider.complete_json("m", "s", "p", {})
    assert result.payload == {"classifications": []}


def test_openrouter_rate_limit_carries_retry_after() -> None:
    """A 429 maps to RATE_LIMIT and preserves the Retry-After hint."""
    provider, _ = _openrouter(http_text(429, "slow down", {"Retry-After": "5"}))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.RATE_LIMIT
    assert exc.value.retry_after == 5.0


def test_openrouter_no_choices_is_inference_error() -> None:
    """A response with no choices is an inference error."""
    provider, _ = _openrouter(http_json(200, {"choices": []}))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.INFERENCE_ERROR


def test_openrouter_content_filter_finish() -> None:
    """A content_filter finish reason is a content-filter failure."""
    provider, _ = _openrouter(http_json(200, _chat("{}", finish="content_filter")))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.CONTENT_FILTER


def test_openrouter_choice_not_mapping_is_inference_error() -> None:
    """A non-mapping choice has no content and is an inference error."""
    provider, _ = _openrouter(http_json(200, {"choices": ["oops"]}))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.INFERENCE_ERROR


def test_openrouter_blank_content_is_inference_error() -> None:
    """A blank message content is an inference error."""
    provider, _ = _openrouter(http_json(200, _chat("   ")))
    with pytest.raises(ProviderError) as exc:
        provider.complete_json("m", "s", "p", {})
    assert exc.value.category is FailureCategory.INFERENCE_ERROR


# --- Hugging Face ---------------------------------------------------------


def test_huggingface_discovers_small_instruct_models() -> None:
    """Discovery keeps small instruct models, drops oversized and non-instruct ones."""
    listing = {
        "data": [
            {"id": "meta-llama/Llama-3.1-8B-Instruct"},
            {"id": "Qwen/Qwen2.5-7B-Instruct"},
            {"id": "meta-llama/Llama-3.1-70B-Instruct"},
            {"id": "some/base-model"},
            {"id": "mistralai/Mistral-7B-Instruct-v0.3"},
            "not-a-dict",
            {"id": 123},
            {"id": "google/gemma-2-9b-it"},
            {"id": "foo/bar-instruct"},
        ],
    }
    provider, _ = _hf(http_json(200, listing))
    assert [c.model_id for c in provider.discover_models()] == [
        "meta-llama/Llama-3.1-8B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "google/gemma-2-9b-it",
        "mistralai/Mistral-7B-Instruct-v0.3",
        "foo/bar-instruct",
    ]


def test_huggingface_available_when_loaded() -> None:
    """A loaded model reports available."""
    provider, _ = _hf(http_json(200, {"loaded": True}))
    assert provider.available("m") is True


def test_huggingface_available_when_loadable_state() -> None:
    """A 'Loadable' state reports available."""
    provider, _ = _hf(http_json(200, {"state": "Loadable"}))
    assert provider.available("m") is True


def test_huggingface_unavailable_when_cold() -> None:
    """A model in a non-loadable state reports unavailable."""
    provider, _ = _hf(http_json(200, {"state": "TooBig"}))
    assert provider.available("m") is False


def test_huggingface_unavailable_on_status_error() -> None:
    """A failing status endpoint reports unavailable rather than raising."""
    provider, _ = _hf(http_text(404, "not found"))
    assert provider.available("m") is False


# --- registry -------------------------------------------------------------


def test_registry_lists_all_three_providers() -> None:
    """The registry knows exactly the three shipped providers."""
    assert set(provider_names()) == {"gemini", "openrouter", "huggingface"}
    assert PROVIDER_CLASSES["gemini"].name == "gemini"


def test_registry_membership() -> None:
    """is_registered reflects whether a name is known."""
    assert is_registered("openrouter") is True
    assert is_registered("nonesuch") is False
