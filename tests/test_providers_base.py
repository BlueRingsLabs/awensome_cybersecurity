"""Tests for the provider-neutral helpers in the shared provider base."""

from __future__ import annotations

import pytest

from cyberkb.errors import FailureCategory
from cyberkb.providers.base import (
    classify_http_status,
    render_schema_instruction,
    retry_after_seconds,
)


@pytest.mark.parametrize(
    ("status", "body", "expected"),
    [
        (401, "", FailureCategory.AUTH_ERROR),
        (403, "forbidden", FailureCategory.AUTH_ERROR),
        (429, "slow down", FailureCategory.RATE_LIMIT),
        (429, "You exceeded your current quota", FailureCategory.RATE_LIMIT),
        (429, "Limit reached on requests per day (RPD)", FailureCategory.QUOTA_EXCEEDED),
        (429, "daily allowance spent", FailureCategory.QUOTA_EXCEEDED),
        (402, "", FailureCategory.QUOTA_EXCEEDED),
        (408, "", FailureCategory.TIMEOUT),
        (504, "", FailureCategory.TIMEOUT),
        (400, "bad model", FailureCategory.MODEL_UNAVAILABLE),
        (404, "no such model", FailureCategory.MODEL_UNAVAILABLE),
        (413, "too large", FailureCategory.MODEL_UNAVAILABLE),
        (422, "", FailureCategory.INFERENCE_ERROR),
        (500, "", FailureCategory.SERVER_ERROR),
        (503, "", FailureCategory.SERVER_ERROR),
        (418, "teapot", FailureCategory.UNKNOWN),
    ],
)
def test_classify_http_status(status: int, body: str, expected: FailureCategory) -> None:
    """A per-minute 429 is a rate limit even when it says "quota"; a daily one is not."""
    assert classify_http_status(status, body) is expected


def test_retry_after_parses_seconds() -> None:
    """A numeric Retry-After header is parsed to a float, case-insensitively."""
    assert retry_after_seconds({"Retry-After": "12"}) == 12.0
    assert retry_after_seconds({"retry-after": "-3"}) == 0.0


def test_retry_after_invalid_or_absent_is_none() -> None:
    """The HTTP-date form or no header yields None rather than raising."""
    assert retry_after_seconds({"retry-after": "Wed, 21 Oct 2026 07:28:00 GMT"}) is None
    assert retry_after_seconds({"Content-Type": "application/json"}) is None


def test_schema_instruction_embeds_the_exact_schema() -> None:
    """Prompt-mode instructions demand bare JSON and carry the schema verbatim."""
    text = render_schema_instruction("SYSTEM", {"type": "object"})
    assert text.startswith("SYSTEM\n\n")
    assert "no prose" in text
    assert text.endswith('{"type": "object"}')
