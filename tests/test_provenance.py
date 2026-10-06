"""Tests for the classified_by provenance stamp builder."""

from __future__ import annotations

from datetime import UTC, datetime

from cyberkb.provenance import classified_by

FIXED = datetime(2026, 10, 5, 14, 23, 11, tzinfo=UTC)


def test_llm_stamp_includes_provider_and_model() -> None:
    """An LLM classification stamps provider, model and time."""
    assert (
        classified_by("llm", provider="gemini", model="gemini-2.5-flash", moment=FIXED)
        == "gemini:gemini-2.5-flash@2026-10-05T14:23:11Z"
    )


def test_heuristic_stamp_has_no_model() -> None:
    """The heuristic stamps the method and time, with no model."""
    assert classified_by("heuristic", moment=FIXED) == "heuristic@2026-10-05T14:23:11Z"


def test_manual_stamp_has_no_model() -> None:
    """A manual classification stamps the method and time."""
    assert classified_by("manual", moment=FIXED) == "manual@2026-10-05T14:23:11Z"


def test_llm_without_provider_or_model_is_indeterminate() -> None:
    """An LLM method lacking provider/model yields no stamp rather than a bad one."""
    assert classified_by("llm", moment=FIXED) is None
    assert classified_by("llm", provider="gemini", moment=FIXED) is None
