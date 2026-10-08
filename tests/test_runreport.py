"""Tests for the structured end-of-run report."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest

from cyberkb.config import ConfigError
from cyberkb.errors import FailureCategory
from cyberkb.obslog import AttemptLog
from cyberkb.runreport import (
    build_run_report,
    default_run_id,
    failure_breakdown,
    safe_run_id,
    write_run_report,
)

if TYPE_CHECKING:
    from cyberkb.paths import RepoPaths


def _attempt(category: FailureCategory | None) -> AttemptLog:
    return AttemptLog(
        provider="google",
        model="m",
        resource_id="r",
        attempt=1,
        outcome="success" if category is None else "failure",
        started_at="t",
        ended_at="t",
        duration_s=0.0,
        category=category,
    )


@pytest.mark.parametrize("run_id", ["gh123-1", "local-20261007T120000Z", "gh1-2-enrich-c3", "a"])
def test_safe_run_ids_pass(run_id: str) -> None:
    """Workflow and local ids are accepted unchanged."""
    assert safe_run_id(run_id) == run_id


@pytest.mark.parametrize("run_id", ["", "../x", "a/b", ".hidden", "-x", "a..b", "x" * 65, "a b"])
def test_unsafe_run_ids_are_refused(run_id: str) -> None:
    """A run id becomes a file name: traversal and odd characters are refused."""
    with pytest.raises(ConfigError):
        safe_run_id(run_id)


def test_default_run_id_prefers_the_workflow_run() -> None:
    """Inside Actions the id is the run and attempt; locally a UTC stamp."""
    now = datetime(2026, 10, 7, 12, 0, 0, tzinfo=UTC)
    assert default_run_id(now, {"GITHUB_RUN_ID": "42", "GITHUB_RUN_ATTEMPT": "3"}) == "gh42-3"
    assert default_run_id(now, {"GITHUB_RUN_ID": "x"}) == "local-20261007T120000Z"
    assert default_run_id(now, {}) == "local-20261007T120000Z"
    assert default_run_id(now).startswith(("gh", "local-"))


def test_failure_breakdown_lists_every_category() -> None:
    """All ten categories appear, zero-filled, so absence is visible."""
    breakdown = failure_breakdown(
        [
            _attempt(None),
            _attempt(FailureCategory.RATE_LIMIT),
            _attempt(FailureCategory.RATE_LIMIT),
        ],
    )
    assert list(breakdown) == [c.value for c in FailureCategory]
    assert breakdown["rate_limit"] == 2
    assert breakdown["auth_error"] == 0


def test_report_without_an_engine_is_well_formed(repo: RepoPaths) -> None:
    """A report can be written even when no provider was involved."""
    report = build_run_report(
        command="enrich",
        run_id="gh1-1",
        started_at="2026-10-07T11:00:00Z",
        finished_at="2026-10-07T12:00:00Z",
        status="failed",
        reason="why",
        notes=["recovered"],
    )
    assert report["final_status"] == {"status": "failed", "reason": "why"}
    assert report["providers"] == {}
    assert report["catalog"] is None
    assert report["work"] is None
    path = write_run_report(repo, report)
    assert path.name == "2026-10-07-gh1-1.json"
    assert json.loads(path.read_text(encoding="utf-8"))["notes"] == ["recovered"]


def test_write_refuses_an_unsafe_run_id(repo: RepoPaths) -> None:
    """The file name is validated at write time too."""
    report = build_run_report(
        command="enrich",
        run_id="../../x",
        started_at="t",
        finished_at="2026-10-07T00:00:00Z",
        status="failed",
        reason="r",
    )
    with pytest.raises(ConfigError):
        write_run_report(repo, report)
