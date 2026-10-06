"""Tests for structured attempt logging and the end-of-run report."""

from __future__ import annotations

import io
import json
import re
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from cyberkb.errors import FailureCategory
from cyberkb.obslog import AttemptLog, RunReport, StructuredLogger, utc_now_iso

if TYPE_CHECKING:
    from pathlib import Path

FIXED = datetime(2026, 10, 5, 14, 23, 11, tzinfo=UTC)


def _attempt(
    *,
    provider: str = "gemini",
    model: str | None = "gemini-2.5-flash",
    outcome: str = "success",
    category: FailureCategory | None = None,
    status: int | None = 200,
    resource_id: str | None = "ckb-000000000001",
    attempt: int = 1,
    fell_back: bool = False,
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
        fell_back=fell_back,
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
    assert payload["provider"] == "gemini"
    assert logger.attempts == [_attempt()]


def test_logger_now_iso_uses_injected_clock() -> None:
    """now_iso() reflects the injected clock, not the wall clock."""
    logger = StructuredLogger(io.StringIO(), now=lambda: FIXED)
    assert logger.now_iso() == "2026-10-05T14:23:11Z"


def test_logger_defaults_to_stdout() -> None:
    """Constructed with no stream, the logger targets stdout without raising."""
    logger = StructuredLogger()
    assert logger.attempts == []


def test_run_report_empty_has_zero_rates() -> None:
    """An empty run reports zero calls and a 0.0 success rate, not a division error."""
    report = RunReport(generated_at="2026-10-05T14:23:11Z", attempts=())
    data = report.to_dict()
    assert data["totals"] == {
        "calls": 0,
        "successes": 0,
        "failures": 0,
        "success_rate": 0.0,
        "heuristic_fallbacks": 0,
    }
    assert data["per_provider"] == {}
    assert data["failure_categories"] == {}


def test_run_report_aggregates_per_provider_and_categories() -> None:
    """Per-provider counts, overall categories and success rate are derived from attempts."""
    attempts = (
        _attempt(provider="gemini", outcome="success"),
        _attempt(provider="gemini", outcome="failure", category=FailureCategory.RATE_LIMIT),
        _attempt(provider="openrouter", outcome="failure", category=FailureCategory.AUTH_ERROR),
        _attempt(provider="openrouter", outcome="success"),
    )
    report = RunReport(
        generated_at="2026-10-05T14:23:11Z",
        attempts=attempts,
        heuristic_fallbacks=3,
    )
    data = report.to_dict()
    assert data["totals"]["calls"] == 4
    assert data["totals"]["successes"] == 2
    assert data["totals"]["success_rate"] == 0.5
    assert data["totals"]["heuristic_fallbacks"] == 3
    assert data["failure_categories"] == {"auth_error": 1, "rate_limit": 1}
    assert list(data["per_provider"]) == ["gemini", "openrouter"]  # first-seen order
    assert data["per_provider"]["gemini"] == {
        "calls": 2,
        "successes": 1,
        "failures": 1,
        "success_rate": 0.5,
        "failure_categories": {"rate_limit": 1},
    }


def test_run_report_includes_health_and_selection() -> None:
    """Health and model-selection sections pass through as lists of mappings."""
    report = RunReport(
        generated_at="2026-10-05T14:23:11Z",
        attempts=(),
        provider_health=({"provider": "gemini", "ok": True},),
        model_selection=({"provider": "gemini", "chosen": "gemini-2.5-flash"},),
    )
    data = report.to_dict()
    assert data["provider_health"] == [{"provider": "gemini", "ok": True}]
    assert data["model_selection"] == [{"provider": "gemini", "chosen": "gemini-2.5-flash"}]


def test_run_report_write_creates_dated_file(tmp_path: Path) -> None:
    """write() lands a <date>.json file whose contents round-trip to the report."""
    report = RunReport(generated_at="2026-10-05T14:23:11Z", attempts=(_attempt(),))
    out = report.write(tmp_path / "ingest-runs")
    assert out.name == "2026-10-05.json"
    assert json.loads(out.read_text(encoding="utf-8")) == report.to_dict()


def test_run_report_write_honours_today_override(tmp_path: Path) -> None:
    """An explicit date overrides the one derived from generated_at."""
    report = RunReport(generated_at="2026-10-05T14:23:11Z", attempts=())
    out = report.write(tmp_path, today="2026-12-31")
    assert out.name == "2026-12-31.json"
