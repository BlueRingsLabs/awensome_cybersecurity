"""The enrichment state ledger: ``docs/audit/enrich-state.json``.

Enrichment of the whole corpus spans many runs (free-tier quotas, job time
limits), so progress must survive any of them ending early. The ledger records,
per resource, whether it is ``pending``, ``enriched`` or ``failed`` (and which
provider/model enriched it or why it failed); per model, how much of today's
quota is spent and whether it validated today; and the last run's outcome.
It is committed alongside the library after every run.

Three rules keep it trustworthy:

* **Front matter is the source of truth.** :func:`reconcile` rebuilds the
  resource view from the library on every run: an LLM-classified resource is
  enriched, a manual one is out of scope, everything else is pending unless the
  ledger already recorded a failure for it. The ledger can never claim work
  the library does not show.
* **Atomic writes, written as we go.** Every successful resource is persisted
  (document first, then ledger) before the next request, via
  :func:`cyberkb.fsutil.atomic_write_text`.
* **Write-ahead for moves.** When enrichment changes a resource's category the
  file moves. The intended move is recorded *before* it happens
  (``in_flight``); :func:`recover` completes or discards it at the next start,
  so a crash can never leave two copies of one resource.

A ledger that exists but cannot be parsed is an error, not an empty start:
silently starting over would re-spend quota on work already done.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal, NoReturn

from cyberkb.errors import KBError, UnsafePathError
from cyberkb.frontmatter import split_front_matter
from cyberkb.fsutil import atomic_write_text, ensure_within, read_text
from cyberkb.providers.governor import DailyUsage
from cyberkb.providers.rotation import CachedValidation

if TYPE_CHECKING:
    from pathlib import Path

    from cyberkb.library import LoadedLibrary
    from cyberkb.paths import RepoPaths

__all__ = [
    "STATE_VERSION",
    "EnrichState",
    "InFlightMove",
    "ResourceState",
    "StateError",
    "load_state",
    "reconcile",
    "recover",
    "save_state",
]

STATE_VERSION = 1
_MAX_DOC_BYTES = 8 * 1024 * 1024
ResourceStatus = Literal["pending", "enriched", "failed"]
_STATUSES: tuple[ResourceStatus, ...] = ("pending", "enriched", "failed")


class StateError(KBError):
    """The enrichment ledger exists but is unreadable or malformed."""


@dataclass(slots=True)
class ResourceState:
    """Where one resource stands."""

    status: ResourceStatus
    path: str
    provider: str | None = None
    model: str | None = None
    updated_at: str | None = None
    attempts: int = 0
    last_error_category: str | None = None
    last_error: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialise for the ledger."""
        return {
            "status": self.status,
            "path": self.path,
            "provider": self.provider,
            "model": self.model,
            "updated_at": self.updated_at,
            "attempts": self.attempts,
            "last_error_category": self.last_error_category,
            "last_error": self.last_error,
        }


@dataclass(frozen=True, slots=True)
class InFlightMove:
    """A category move that was announced but may not have completed."""

    resource_id: str
    source: str
    destination: str


@dataclass(slots=True)
class EnrichState:
    """The whole ledger."""

    resources: dict[str, ResourceState] = field(default_factory=dict)
    usage: dict[str, DailyUsage] = field(default_factory=dict)
    validations: dict[str, CachedValidation] = field(default_factory=dict)
    last_run: dict[str, Any] | None = None
    in_flight: InFlightMove | None = None
    updated_at: str | None = None

    def counts(self) -> dict[str, int]:
        """Resources per status."""
        totals: dict[str, int] = dict.fromkeys(_STATUSES, 0)
        for entry in self.resources.values():
            totals[entry.status] += 1
        return totals

    def to_dict(self) -> dict[str, Any]:
        """Serialise the ledger (keys sorted for stable diffs)."""
        return {
            "schema_version": STATE_VERSION,
            "updated_at": self.updated_at,
            "summary": self.counts(),
            "last_run": self.last_run,
            "in_flight": (
                {
                    "resource_id": self.in_flight.resource_id,
                    "source": self.in_flight.source,
                    "destination": self.in_flight.destination,
                }
                if self.in_flight
                else None
            ),
            "models": {
                key: {
                    "usage": self.usage[key].to_dict() if key in self.usage else None,
                    "validation": (
                        self.validations[key].to_dict() if key in self.validations else None
                    ),
                }
                for key in sorted(set(self.usage) | set(self.validations))
            },
            "resources": {rid: self.resources[rid].to_dict() for rid in sorted(self.resources)},
        }


def _reject(message: str, cause: BaseException | None = None) -> NoReturn:
    """Raise a :class:`StateError` describing what is malformed."""
    msg = f"enrichment ledger is malformed: {message}"
    raise StateError(msg) from cause


def _str(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _resource(rid: str, raw: object) -> ResourceState:
    if not isinstance(raw, dict) or raw.get("status") not in _STATUSES:
        _reject(f"resource {rid!r} has no valid status")
    path = raw.get("path")
    if not isinstance(path, str):
        _reject(f"resource {rid!r} has no path")
    attempts = raw.get("attempts", 0)
    return ResourceState(
        status=raw["status"],
        path=path,
        provider=_str(raw.get("provider")),
        model=_str(raw.get("model")),
        updated_at=_str(raw.get("updated_at")),
        attempts=attempts if isinstance(attempts, int) and attempts >= 0 else 0,
        last_error_category=_str(raw.get("last_error_category")),
        last_error=_str(raw.get("last_error")) or "",
    )


def _model(key: str, raw: object) -> tuple[DailyUsage | None, CachedValidation | None]:
    if not isinstance(raw, dict):
        _reject(f"model {key!r} is not an object")
    usage_raw, validation_raw = raw.get("usage"), raw.get("validation")
    usage = None
    if isinstance(usage_raw, dict) and isinstance(usage_raw.get("day"), str):
        usage = DailyUsage(
            day=usage_raw["day"],
            requests=int(usage_raw.get("requests") or 0),
            tokens=int(usage_raw.get("tokens") or 0),
            exhausted=bool(usage_raw.get("exhausted")),
        )
    validation = None
    if isinstance(validation_raw, dict) and isinstance(validation_raw.get("day"), str):
        validation = CachedValidation(
            day=validation_raw["day"],
            ok=bool(validation_raw.get("ok")),
            mode=_str(validation_raw.get("mode")),
            category=_str(validation_raw.get("category")),
            detail=_str(validation_raw.get("detail")) or "",
        )
    return usage, validation


def _in_flight(raw: object) -> InFlightMove | None:
    if raw is None:
        return None
    if not isinstance(raw, dict) or not all(
        isinstance(raw.get(k), str) for k in ("resource_id", "source", "destination")
    ):
        _reject("in_flight is not a complete move record")
    return InFlightMove(raw["resource_id"], raw["source"], raw["destination"])


def load_state(paths: RepoPaths) -> EnrichState:
    """Read the ledger; a missing file is an empty ledger, a broken one an error.

    Raises:
        StateError: the file exists but is not a valid ledger.
    """
    target = paths.enrich_state
    try:
        text = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return EnrichState()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        _reject(f"invalid JSON ({exc})", exc)
    if not isinstance(data, dict) or data.get("schema_version") != STATE_VERSION:
        _reject(f"schema_version must be {STATE_VERSION}")
    resources_raw = data.get("resources", {})
    models_raw = data.get("models", {})
    if not isinstance(resources_raw, dict) or not isinstance(models_raw, dict):
        _reject("resources and models must be objects")
    state = EnrichState(
        resources={rid: _resource(rid, raw) for rid, raw in resources_raw.items()},
        last_run=data.get("last_run") if isinstance(data.get("last_run"), dict) else None,
        in_flight=_in_flight(data.get("in_flight")),
        updated_at=_str(data.get("updated_at")),
    )
    for key, raw in models_raw.items():
        usage, validation = _model(key, raw)
        if usage is not None:
            state.usage[key] = usage
        if validation is not None:
            state.validations[key] = validation
    return state


def save_state(paths: RepoPaths, state: EnrichState, *, now_iso: str) -> Path:
    """Atomically write the ledger and return its path."""
    state.updated_at = now_iso
    target = paths.enrich_state
    atomic_write_text(target, json.dumps(state.to_dict(), indent=2, ensure_ascii=False) + "\n")
    return target


def recover(paths: RepoPaths, state: EnrichState) -> str | None:
    """Finish or discard an interrupted move; return what was done, if anything.

    The destination is written atomically before the source is removed, so:
    both present → the move completed but the source survived (remove it);
    only the destination → it completed; only the source → the write never
    landed (nothing to undo). Either way the record is cleared.

    The ledger is committed, so its move record is treated as untrusted: a file
    is only ever removed when both paths are library documents inside the
    repository (no symlinks) and *both* carry the recorded resource id.

    Raises:
        StateError: the move record points outside the library.
    """
    move = state.in_flight
    if move is None:
        return None
    source = _library_document(paths, move.source)
    destination = _library_document(paths, move.destination)
    state.in_flight = None
    if destination.is_file() and source.is_file():
        if _document_id(destination, paths) != move.resource_id or (
            _document_id(source, paths) != move.resource_id
        ):
            return f"interrupted move of {move.resource_id} left untouched: ids do not match"
        source.unlink()
        return f"completed interrupted move of {move.resource_id}: removed {move.source}"
    if destination.is_file():
        return f"interrupted move of {move.resource_id} had already completed"
    return f"interrupted move of {move.resource_id} never landed; {move.source} kept"


def _library_document(paths: RepoPaths, relative: str) -> Path:
    """Resolve a ledger path, refusing anything but a ``library/**.md`` file."""
    try:
        target = ensure_within(paths.root / relative, paths.root)
    except UnsafePathError as exc:
        _reject(f"in_flight path {relative!r} is unsafe ({exc})", exc)
    if not target.is_relative_to(paths.library) or target.suffix != ".md":
        _reject(f"in_flight path {relative!r} is not a library document")
    return target


def _document_id(path: Path, paths: RepoPaths) -> str | None:
    try:
        header, _ = split_front_matter(read_text(path, root=paths.root, max_bytes=_MAX_DOC_BYTES))
    except KBError:
        return None
    value = header.get("id") if header else None
    return value if isinstance(value, str) else None


def reconcile(state: EnrichState, library: LoadedLibrary, *, force: bool = False) -> None:
    """Rebuild the per-resource view from the library (front matter wins).

    With ``force``, LLM-classified resources are queued again too.
    """
    current: dict[str, ResourceState] = {}
    for resource in library.resources:
        fm = resource.front_matter
        method = fm.classification.method
        if method == "manual":
            continue
        previous = state.resources.get(fm.id)
        if method == "llm" and not force:
            provider, model = _provenance(fm.classified_by)
            current[fm.id] = ResourceState(
                status="enriched",
                path=resource.path,
                provider=previous.provider if previous and previous.provider else provider,
                model=previous.model if previous and previous.model else model,
                updated_at=previous.updated_at if previous else None,
                attempts=previous.attempts if previous else 0,
            )
            continue
        failed = previous is not None and previous.status == "failed"
        current[fm.id] = ResourceState(
            status="failed" if failed else "pending",
            path=resource.path,
            updated_at=previous.updated_at if previous else None,
            attempts=previous.attempts if previous else 0,
            last_error_category=previous.last_error_category if previous and failed else None,
            last_error=previous.last_error if previous and failed else "",
        )
    state.resources = current


def _provenance(stamp: str | None) -> tuple[str | None, str | None]:
    """Split ``provider:model@time`` into ``(provider, model)``."""
    if not stamp or ":" not in stamp.split("@", 1)[0]:
        return None, None
    provider, model = stamp.split("@", 1)[0].split(":", 1)
    return provider, model
