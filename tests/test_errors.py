"""Tests for the provider failure taxonomy and the structured provider error."""

from __future__ import annotations

from cyberkb.errors import (
    FailureCategory,
    KBError,
    LLMError,
    ModelCatalogError,
    ProviderConfigError,
    ProviderError,
)


def test_provider_error_is_a_catchable_llm_error() -> None:
    """ProviderError is an LLMError (and thus a KBError), so existing handlers catch it."""
    err = ProviderError(FailureCategory.AUTH_ERROR, provider="google")
    assert isinstance(err, LLMError)
    assert isinstance(err, KBError)


def test_provider_error_retains_full_context() -> None:
    """Every diagnostic field is stored verbatim for logging and the report."""
    err = ProviderError(
        FailureCategory.RATE_LIMIT,
        provider="groq",
        model="openai/gpt-oss-120b",
        status=429,
        raw="rate limited, retry soon",
        retry_after=2.5,
    )
    assert err.category is FailureCategory.RATE_LIMIT
    assert err.provider == "groq"
    assert err.model == "openai/gpt-oss-120b"
    assert err.status == 429
    assert err.raw == "rate limited, retry soon"
    assert err.retry_after == 2.5
    assert err.request_rejected is False


def test_provider_error_message_includes_provider_category_and_raw() -> None:
    """The message carries provider, category and the verbatim provider text."""
    message = str(
        ProviderError(FailureCategory.SERVER_ERROR, provider="groq", raw="502 Bad Gateway")
    )
    assert "groq" in message
    assert "server_error" in message
    assert "502 Bad Gateway" in message


def test_provider_error_message_falls_back_to_category_when_raw_is_blank() -> None:
    """With no raw text the detail falls back to the category value, not an empty string."""
    err = ProviderError(FailureCategory.TIMEOUT, provider="groq", raw="   ")
    assert str(err) == "groq: timeout: timeout"
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


def test_request_rejection_and_config_errors() -> None:
    """A rejected request mode is flagged; config and catalog errors are KBErrors."""
    err = ProviderError(FailureCategory.MODEL_UNAVAILABLE, provider="google", request_rejected=True)
    assert err.request_rejected is True
    assert issubclass(ProviderConfigError, LLMError)
    assert issubclass(ModelCatalogError, KBError)
