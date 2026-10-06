"""Tests for the provider failure taxonomy and the structured provider error."""

from __future__ import annotations

from cyberkb.errors import FailureCategory, KBError, LLMError, ProviderError


def test_provider_error_is_a_catchable_llm_error() -> None:
    """ProviderError is an LLMError (and thus a KBError), so existing handlers catch it."""
    err = ProviderError(FailureCategory.AUTH_ERROR, provider="gemini")
    assert isinstance(err, LLMError)
    assert isinstance(err, KBError)


def test_provider_error_retains_full_context() -> None:
    """Every diagnostic field is stored verbatim for logging and the report."""
    err = ProviderError(
        FailureCategory.RATE_LIMIT,
        provider="openrouter",
        model="meta-llama/llama-3.3-70b-instruct:free",
        status=429,
        raw="rate limited, retry soon",
        retry_after=2.5,
    )
    assert err.category is FailureCategory.RATE_LIMIT
    assert err.provider == "openrouter"
    assert err.model == "meta-llama/llama-3.3-70b-instruct:free"
    assert err.status == 429
    assert err.raw == "rate limited, retry soon"
    assert err.retry_after == 2.5


def test_provider_error_message_includes_provider_category_and_raw() -> None:
    """The message carries provider, category and the verbatim provider text."""
    message = str(ProviderError(FailureCategory.SERVER_ERROR, provider="hf", raw="502 Bad Gateway"))
    assert "hf" in message
    assert "server_error" in message
    assert "502 Bad Gateway" in message


def test_provider_error_message_falls_back_to_category_when_raw_is_blank() -> None:
    """With no raw text the detail falls back to the category value, not an empty string."""
    err = ProviderError(FailureCategory.TIMEOUT, provider="hf", raw="   ")
    assert str(err) == "hf: timeout: timeout"
    assert err.model is None
    assert err.status is None
    assert err.retry_after is None


def test_failure_category_values_are_stable_strings() -> None:
    """The category values are the exact tokens the audit report and logs use."""
    assert FailureCategory.QUOTA_EXCEEDED.value == "quota_exceeded"
    assert FailureCategory.MODEL_UNAVAILABLE.value == "model_unavailable"
    assert {c.value for c in FailureCategory} == {
        "auth_error",
        "rate_limit",
        "quota_exceeded",
        "timeout",
        "server_error",
        "network_error",
        "inference_error",
        "content_filter",
        "model_unavailable",
        "unknown",
    }
