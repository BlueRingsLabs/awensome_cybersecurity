"""The structured end-of-run report: ``docs/audit/ingest-runs/<date>-<run-id>.json``.

Every ``ingest`` (that used an LLM), ``enrich`` and ``preflight`` run writes one,
complete or not, so the record of what was attempted — and why anything did not
happen — outlives the workflow logs. It carries:

* the final status (``complete`` / ``partial`` / ``failed``) and its reason;
* the catalog version used, and per provider: listing size, status, attempts,
  successes, failures and failure categories;
* per model: declared name → API id and the resolution rule, validation trail
  and request mode, declared limits, today's usage, attempts, successes,
  failures and the last error (category and message);
* a failure breakdown over all ten categories (zeros included, so an absent
  category is visibly zero rather than silently missing);
* retries spent per model, per provider and per list pass;
* per resource (enrich): who enriched it, or why it was not;
* every failed attempt verbatim (successes are counted, not listed, to keep the
  committed report proportionate).

Error text is the provider's own response body with the API key redacted at the
adapter; request headers are never captured.
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter
from typing import TYPE_CHECKING, Any

from cyberkb.config import ConfigError
from cyberkb.errors import FailureCategory
from cyberkb.fsutil import atomic_write_text

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence
    from datetime import datetime
    from pathlib import Path

    from cyberkb.obslog import AttemptLog
    from cyberkb.paths import RepoPaths
    from cyberkb.providers.catalog import ModelCatalog
    from cyberkb.providers.rotation import RotationEngine

__all__ = [
    "REPORT_VERSION",
    "build_run_report",
    "default_run_id",
    "failure_breakdown",
    "safe_run_id",
    "write_run_report",
]

REPORT_VERSION = 2
_RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def safe_run_id(raw: str) -> str:
    """Validate a run id: it becomes part of a file name, so it must be inert.

    Raises:
        ConfigError: anything but 1-64 characters of ``[A-Za-z0-9._-]`` (no
            leading dot or dash), which also rules out any path traversal.
    """
    if not _RUN_ID_RE.match(raw) or ".." in raw:
        msg = f"run id {raw!r} must be 1-64 characters of [A-Za-z0-9._-] starting alphanumeric"
        raise ConfigError(msg)
    return raw


def default_run_id(now: datetime, env: Mapping[str, str] | None = None) -> str:
    """``gh<run>-<attempt>`` inside GitHub Actions, else a UTC timestamp."""
    env = os.environ if env is None else env
    run, attempt = env.get("GITHUB_RUN_ID", ""), env.get("GITHUB_RUN_ATTEMPT", "1")
    if run.isdigit() and attempt.isdigit():
        return f"gh{run}-{attempt}"
    return f"local-{now.strftime('%Y%m%dT%H%M%SZ')}"


def failure_breakdown(attempts: Iterable[AttemptLog]) -> dict[str, int]:
    """Failed attempts per category, every category present (zero-filled)."""
    counted = Counter(a.category.value for a in attempts if a.category is not None)
    return {category.value: counted.get(category.value, 0) for category in FailureCategory}


def build_run_report(  # noqa: PLR0913 - every section is explicit
    *,
    command: str,
    run_id: str,
    started_at: str,
    finished_at: str,
    status: str,
    reason: str,
    catalog: ModelCatalog | None = None,
    engine: RotationEngine | None = None,
    work: Mapping[str, Any] | None = None,
    resources: Sequence[Mapping[str, Any]] = (),
    notes: Sequence[str] = (),
) -> dict[str, Any]:
    """Assemble the report mapping (pure: no I/O)."""
    attempts = list(engine.logger.attempts) if engine is not None else []
    successes = sum(1 for a in attempts if a.outcome == "success")
    return {
        "schema_version": REPORT_VERSION,
        "command": command,
        "run_id": run_id,
        "started_at": started_at,
        "finished_at": finished_at,
        "final_status": {"status": status, "reason": reason},
        "catalog": (
            {"verified_on": catalog.verified_on.isoformat(), "source": catalog.source}
            if catalog is not None
            else None
        ),
        "work": dict(work) if work is not None else None,
        "attempts": {
            "total": len(attempts),
            "successes": successes,
            "failures": len(attempts) - successes,
        },
        "failure_breakdown": failure_breakdown(attempts),
        "retries": engine.retry_summary() if engine is not None else None,
        "providers": engine.provider_report() if engine is not None else {},
        "models": engine.model_report() if engine is not None else [],
        "resources": [dict(r) for r in resources],
        "failed_attempts": [a.to_json() for a in attempts if a.outcome == "failure"],
        "notes": list(notes),
    }


def write_run_report(paths: RepoPaths, report: Mapping[str, Any]) -> Path:
    """Write ``report`` as ``<date>-<run-id>.json`` (date from ``finished_at``)."""
    run_id = safe_run_id(str(report["run_id"]))
    destination = paths.ingest_runs / f"{str(report['finished_at'])[:10]}-{run_id}.json"
    atomic_write_text(destination, json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return destination
