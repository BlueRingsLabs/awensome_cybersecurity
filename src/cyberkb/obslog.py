"""Structured, parseable observability for the classification pipeline.

Every provider call emits one JSON object to stdout (``event: "llm_attempt"``)
carrying the provider, model, resource, outcome, categorised cause, HTTP
status, verbatim provider error, retry number, timing and whether a fallback
was triggered. The same records drive an end-of-run report
(:class:`RunReport`) written under ``docs/audit/ingest-runs/`` so a run can be
audited long after its logs have scrolled away.

The module deliberately depends only on :class:`cyberkb.errors.FailureCategory`
(not on the provider classes), so provider code can log without importing this
and this can summarise without importing providers. Health and model-selection
sections are handed in as already-serialised mappings for the same reason.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal

from cyberkb.fsutil import atomic_write_text

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from pathlib import Path
    from typing import Any, TextIO

    from cyberkb.errors import FailureCategory

__all__ = ["AttemptLog", "RunReport", "StructuredLogger", "utc_now_iso"]

Outcome = Literal["success", "failure"]
_ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def utc_now_iso(moment: datetime | None = None) -> str:
    """Render ``moment`` (default: now) as a second-precision UTC ISO-8601 stamp."""
    return (moment or datetime.now(UTC)).astimezone(UTC).strftime(_ISO_FORMAT)


@dataclass(frozen=True, slots=True)
class AttemptLog:
    """One provider call attempt, successful or not."""

    provider: str
    model: str | None
    resource_id: str | None
    attempt: int
    outcome: Outcome
    started_at: str
    ended_at: str
    duration_s: float
    category: FailureCategory | None = None
    status: int | None = None
    raw_error: str = ""
    fell_back: bool = False
    mode: str | None = None

    def to_json(self) -> dict[str, Any]:
        """Serialise to a flat, stable mapping for a JSON log line or the report."""
        return {
            "provider": self.provider,
            "model": self.model,
            "resource_id": self.resource_id,
            "attempt": self.attempt,
            "outcome": self.outcome,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "duration_s": round(self.duration_s, 3),
            "category": self.category.value if self.category is not None else None,
            "status": self.status,
            "raw_error": self.raw_error,
            "fell_back": self.fell_back,
            "mode": self.mode,
        }


class StructuredLogger:
    """Write one JSON line per attempt and retain the records for the report.

    The output stream is injectable (defaults to stdout) and so is the
    wall-clock, so tests observe exact lines and deterministic timestamps.
    """

    def __init__(
        self,
        stream: TextIO | None = None,
        *,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        """Bind an output stream and a clock; start with no recorded attempts."""
        self._stream = stream if stream is not None else sys.stdout
        self._now = now or (lambda: datetime.now(UTC))
        self.attempts: list[AttemptLog] = []

    def now_iso(self) -> str:
        """The current wall-clock as a UTC ISO-8601 stamp (shares the injected clock)."""
        return utc_now_iso(self._now())

    def record(self, log: AttemptLog) -> None:
        """Retain ``log`` and emit it as a single ``llm_attempt`` JSON line."""
        self.attempts.append(log)
        line = json.dumps({"event": "llm_attempt", **log.to_json()}, ensure_ascii=False)
        print(line, file=self._stream)


@dataclass(frozen=True, slots=True)
class RunReport:
    """An end-of-run summary of every provider attempt plus health and selection.

    ``attempts`` is the raw record; the aggregates (success rates, failure
    categories, per-provider breakdowns) are derived in :meth:`to_dict`, so the
    report cannot drift from the attempts it is built from.
    """

    generated_at: str
    attempts: tuple[AttemptLog, ...]
    heuristic_fallbacks: int = 0
    provider_health: tuple[Mapping[str, Any], ...] = ()
    model_selection: tuple[Mapping[str, Any], ...] = ()

    def _provider_names(self) -> list[str]:
        ordered: list[str] = []
        for attempt in self.attempts:
            if attempt.provider not in ordered:
                ordered.append(attempt.provider)
        return ordered

    def _provider_summary(self, provider: str) -> dict[str, Any]:
        calls = [a for a in self.attempts if a.provider == provider]
        successes = sum(1 for a in calls if a.outcome == "success")
        categories: dict[str, int] = {}
        for attempt in calls:
            if attempt.category is not None:
                categories[attempt.category.value] = categories.get(attempt.category.value, 0) + 1
        return {
            "calls": len(calls),
            "successes": successes,
            "failures": len(calls) - successes,
            "success_rate": _rate(successes, len(calls)),
            "failure_categories": dict(sorted(categories.items())),
        }

    def _failure_categories(self) -> dict[str, int]:
        totals: dict[str, int] = {}
        for attempt in self.attempts:
            if attempt.category is not None:
                totals[attempt.category.value] = totals.get(attempt.category.value, 0) + 1
        return dict(sorted(totals.items()))

    def to_dict(self) -> dict[str, Any]:
        """Build the full report mapping with totals and per-provider breakdowns."""
        total = len(self.attempts)
        successes = sum(1 for a in self.attempts if a.outcome == "success")
        return {
            "generated_at": self.generated_at,
            "totals": {
                "calls": total,
                "successes": successes,
                "failures": total - successes,
                "success_rate": _rate(successes, total),
                "heuristic_fallbacks": self.heuristic_fallbacks,
            },
            "failure_categories": self._failure_categories(),
            "per_provider": {name: self._provider_summary(name) for name in self._provider_names()},
            "provider_health": [dict(h) for h in self.provider_health],
            "model_selection": [dict(m) for m in self.model_selection],
            "attempts": [a.to_json() for a in self.attempts],
        }

    def write(self, directory: Path, *, today: str | None = None) -> Path:
        """Write the report as ``<directory>/<date>.json`` and return the path."""
        stamp = today or self.generated_at[:10]
        destination = directory / f"{stamp}.json"
        atomic_write_text(
            destination, json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n"
        )
        return destination


def _rate(part: int, whole: int) -> float:
    return round(part / whole, 4) if whole else 0.0
