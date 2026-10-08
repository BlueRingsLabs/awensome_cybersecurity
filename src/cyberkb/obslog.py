"""Structured, parseable observability for the classification pipeline.

Every provider call emits one JSON object to stdout (``event: "llm_attempt"``)
carrying the provider, model, request mode, resource, outcome, categorised
cause, HTTP status, verbatim (key-redacted) provider error, attempt number and
timing. The same records feed the end-of-run report (:mod:`cyberkb.runreport`)
written under ``docs/audit/ingest-runs/``, so a run can be audited long after
its logs have scrolled away.

The module depends only on :class:`cyberkb.errors.FailureCategory`, so the
provider layer can log through it without an import cycle.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, TextIO

    from cyberkb.errors import FailureCategory

__all__ = ["AttemptLog", "StructuredLogger", "utc_now_iso"]

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
