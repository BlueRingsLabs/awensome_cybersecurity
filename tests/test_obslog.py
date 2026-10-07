"""Tests for structured attempt logging."""

from __future__ import annotations

import io
import json
import re
from datetime import UTC, datetime

from cyberkb.errors import FailureCategory
from cyberkb.obslog import AttemptLog, StructuredLogger, utc_now_iso

FIXED = datetime(2026, 10, 5, 14, 23, 11, tzinfo=UTC)


def _attempt(
    *,
    provider: str = "google",
    model: str | None = "gemma-4-31b-it",
    outcome: str = "success",
    category: FailureCategory | None = None,
    status: int | None = 200,
    resource_id: str | None = "ckb-000000000001",
    attempt: int = 1,
    mode: str | None = None,
) -> AttemptLog:
    """Build an AttemptLog with sensible defaults for tests."""
    return AttemptLog(
        provider=provider,
        model=model,
        resource_id=resource_id,
        attempt=attempt,
        outcome=outcome,  # type: ignore[arg-type]
        started_at="2026-10-05T14:23:10Z",
        ended_at="2026-10-05T14:23:11Z",
        duration_s=1.2345,
        category=category,
        status=status,
        raw_error="" if category is None else "boom",
        mode=mode,
    )


def test_utc_now_iso_formats_given_moment() -> None:
    """A supplied moment is rendered at second precision in UTC."""
    assert utc_now_iso(FIXED) == "2026-10-05T14:23:11Z"


def test_utc_now_iso_without_argument_is_well_formed() -> None:
    """Called with no moment it still returns a Z-suffixed UTC stamp."""
    stamp = utc_now_iso()
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", stamp)


def test_attempt_to_json_success_has_no_category() -> None:
    """A successful attempt serialises a null category and rounds the duration."""
    data = _attempt().to_json()
    assert data["category"] is None
    assert data["outcome"] == "success"
    assert data["duration_s"] == 1.234  # rounded to 3 dp


def test_attempt_to_json_failure_carries_category_and_raw() -> None:
    """A failed attempt serialises its category value and verbatim raw error."""
    data = _attempt(outcome="failure", category=FailureCategory.RATE_LIMIT, status=429).to_json()
    assert data["category"] == "rate_limit"
    assert data["status"] == 429
    assert data["raw_error"] == "boom"


def test_logger_writes_one_json_line_and_retains_record() -> None:
    """record() emits a single parseable llm_attempt line and stores the record."""
    stream = io.StringIO()
    logger = StructuredLogger(stream, now=lambda: FIXED)
    logger.record(_attempt())
    lines = stream.getvalue().splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["event"] == "llm_attempt"
    assert payload["provider"] == "google"
    assert logger.attempts == [_attempt()]


def test_logger_now_iso_uses_injected_clock() -> None:
    """now_iso() reflects the injected clock, not the wall clock."""
    logger = StructuredLogger(io.StringIO(), now=lambda: FIXED)
    assert logger.now_iso() == "2026-10-05T14:23:11Z"


def test_logger_defaults_to_stdout() -> None:
    """Constructed with no stream, the logger targets stdout without raising."""
    logger = StructuredLogger()
    assert logger.attempts == []
