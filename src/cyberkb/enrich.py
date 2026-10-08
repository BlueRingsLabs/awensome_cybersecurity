"""Enrich existing library resources with LLM classification and summaries.

Most of the migrated corpus was filed by the offline heuristic with an empty
summary. :func:`enrich_library` sends every resource the ledger marks
``pending`` (then the ``failed`` ones, for another chance) through the rotation
engine, one document per request, and on success adopts the model's category,
format, language, tags and one-line summary, refreshes empty author lists from
the body and stamps the provenance.

Progress is durable at resource granularity: each upgraded document is written
atomically and the ledger saved before the next request, a category change is
announced in the ledger before the file moves, and a run that stops early — run
budget, exhausted quotas, a cancelled job — leaves everything it finished on
disk for the workflow to commit. Manual classifications are never touched, and
a resource the providers could not classify is left byte-for-byte unchanged
with the reason recorded.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, replace
from enum import StrEnum
from typing import TYPE_CHECKING, Literal

from cyberkb.authors import extract_authors
from cyberkb.classify.base import Document
from cyberkb.enrich_state import InFlightMove, ResourceState, reconcile, save_state
from cyberkb.frontmatter import Classification, FrontMatter, render_document, split_front_matter
from cyberkb.fsutil import atomic_write_text, read_text, relpath
from cyberkb.library import MAX_RESOURCE_BYTES, load_library
from cyberkb.obslog import utc_now_iso
from cyberkb.provenance import classified_by
from cyberkb.textutil import slugify

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime
    from pathlib import Path

    from cyberkb.classify.base import ClassificationResult
    from cyberkb.classify.llm import LLMClassifier
    from cyberkb.enrich_state import EnrichState
    from cyberkb.library import Resource
    from cyberkb.paths import RepoPaths
    from cyberkb.taxonomy import Taxonomy

__all__ = ["EnrichOutcome", "EnrichReport", "EnrichStatus", "FinalStatus", "enrich_library"]

FinalStatus = Literal["complete", "partial", "failed"]


class EnrichStatus(StrEnum):
    """What happened to one resource during this run."""

    ENRICHED = "enriched"
    """Upgraded by a provider and written to disk."""
    FAILED = "failed"
    """Every usable model failed it; left unchanged, cause recorded."""
    DEFERRED = "deferred"
    """Still needs enrichment; not attempted (run budget or no model capacity)."""
    UNCHANGED = "unchanged"
    """Already LLM-classified; nothing to do."""
    SKIPPED = "skipped"
    """Manually classified; never re-classified."""


@dataclass(frozen=True, slots=True)
class EnrichOutcome:
    """Result of considering one resource for enrichment."""

    resource_id: str
    path: str
    status: EnrichStatus
    detail: str = ""
    destination: str | None = None
    provider: str | None = None
    model: str | None = None
    category: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        """Serialise for the run report."""
        return {
            "id": self.resource_id,
            "path": self.path,
            "status": self.status.value,
            "provider": self.provider,
            "model": self.model,
            "failure_category": self.category,
            "detail": self.detail,
            "destination": self.destination,
        }


@dataclass(frozen=True, slots=True)
class EnrichReport:
    """Aggregate outcome of an enrichment run."""

    outcomes: tuple[EnrichOutcome, ...]
    final_status: FinalStatus
    reason: str
    capacity_exhausted: bool
    budget_reached: bool = False

    def count(self, status: EnrichStatus) -> int:
        """Number of resources that ended this run with ``status``."""
        return sum(1 for o in self.outcomes if o.status is status)

    @property
    def enriched(self) -> int:
        """Resources upgraded this run."""
        return self.count(EnrichStatus.ENRICHED)

    @property
    def failed(self) -> int:
        """Resources every usable model failed this run."""
        return self.count(EnrichStatus.FAILED)

    @property
    def deferred(self) -> int:
        """Resources still needing enrichment that were not attempted."""
        return self.count(EnrichStatus.DEFERRED)

    @property
    def unchanged(self) -> int:
        """Resources already LLM-classified."""
        return self.count(EnrichStatus.UNCHANGED)

    @property
    def skipped(self) -> int:
        """Manually-classified resources."""
        return self.count(EnrichStatus.SKIPPED)


def _unique_destination(directory: Path, slug: str) -> Path:
    candidate = directory / f"{slug}.md"
    index = 2
    while candidate.exists():
        candidate = directory / f"{slug}-{index}.md"
        index += 1
    return candidate


def _queue(library_resources: tuple[Resource, ...], state: EnrichState) -> list[Resource]:
    """Resources to attempt: pending first (fresh work), then failed (another chance)."""
    pending = [r for r in library_resources if _status(state, r) == "pending"]
    failed = [r for r in library_resources if _status(state, r) == "failed"]
    return pending + failed


def _status(state: EnrichState, resource: Resource) -> str | None:
    entry = state.resources.get(resource.front_matter.id)
    return entry.status if entry else None


def enrich_library(  # noqa: PLR0913 - every budget and collaborator explicit
    paths: RepoPaths,
    taxonomy: Taxonomy,
    classifier: LLMClassifier,
    state: EnrichState,
    *,
    force: bool = False,
    limit: int | None = None,
    max_seconds: float | None = None,
    clock: Callable[[], float] = time.monotonic,
    now: Callable[[], datetime] | None = None,
) -> EnrichReport:
    """Enrich pending/failed resources until done, out of budget or out of capacity.

    ``limit`` caps how many resources are attempted; ``max_seconds`` is a
    wall-clock budget after which no new request starts. ``force`` re-queues
    resources already classified by an LLM (manual ones are never touched).
    """
    library = load_library(paths, taxonomy)
    reconcile(state, library, force=force)
    deadline = None if max_seconds is None else clock() + max_seconds
    stamp = (lambda: utc_now_iso(now())) if now else utc_now_iso
    outcomes: dict[str, EnrichOutcome] = {}
    for resource in library.resources:
        fm = resource.front_matter
        entry = state.resources.get(fm.id)
        if entry is None:
            outcomes[fm.id] = EnrichOutcome(
                fm.id, resource.path, EnrichStatus.SKIPPED, "manual classification kept"
            )
        elif entry.status == "enriched":
            outcomes[fm.id] = EnrichOutcome(
                fm.id,
                resource.path,
                EnrichStatus.UNCHANGED,
                "already LLM-classified",
                provider=entry.provider,
                model=entry.model,
            )
    attempted = 0
    stop: str | None = None
    for resource in _queue(library.resources, state):
        fm = resource.front_matter
        entry = state.resources[fm.id]
        if stop is None and (
            (limit is not None and attempted >= limit)
            or (deadline is not None and clock() >= deadline)
        ):
            stop = "run budget reached"
        if stop is not None:
            outcomes[fm.id] = _deferred(resource, entry, stop)
            continue
        attempted += 1
        outcome = _enrich_one(resource, paths, classifier, state, deadline=deadline, stamp=stamp)
        outcomes[fm.id] = outcome
        if outcome.status is EnrichStatus.DEFERRED:
            stop = outcome.detail
    exhausted = classifier.engine.exhausted
    budget_hit = stop is not None and not exhausted
    ordered = tuple(outcomes[r.front_matter.id] for r in library.resources)
    final, reason = _final(state, ordered, exhausted=exhausted, budget_hit=budget_hit)
    return EnrichReport(ordered, final, reason, exhausted, budget_hit)


def _deferred(resource: Resource, entry: ResourceState, reason: str) -> EnrichOutcome:
    fm = resource.front_matter
    return EnrichOutcome(
        fm.id,
        resource.path,
        EnrichStatus.DEFERRED,
        reason,
        category=entry.last_error_category if entry.status == "failed" else None,
    )


def _final(
    state: EnrichState,
    outcomes: tuple[EnrichOutcome, ...],
    *,
    exhausted: bool,
    budget_hit: bool,
) -> tuple[FinalStatus, str]:
    counts = state.counts()
    remaining = counts["pending"] + counts["failed"]
    if remaining == 0:
        return "complete", f"all {counts['enriched']} eligible resources are enriched"
    enriched_now = sum(1 for o in outcomes if o.status is EnrichStatus.ENRICHED)
    parts = [f"{counts['pending']} pending", f"{counts['failed']} failed"]
    if exhausted:
        cause = "every model is exhausted or failed"
    elif budget_hit:
        cause = "the run budget was reached"
    else:
        cause = "some resources could not be classified by any usable model"
    status: FinalStatus = "partial" if enriched_now or budget_hit else "failed"
    return status, f"{cause}; {', '.join(parts)} remain ({enriched_now} enriched this run)"


def _enrich_one(
    resource: Resource,
    paths: RepoPaths,
    classifier: LLMClassifier,
    state: EnrichState,
    *,
    deadline: float | None,
    stamp: Callable[[], str],
) -> EnrichOutcome:
    fm = resource.front_matter
    entry = state.resources[fm.id]
    source = paths.root / resource.path
    _, body = split_front_matter(read_text(source, root=paths.root, max_bytes=MAX_RESOURCE_BYTES))
    single = classifier.classify_one(
        Document(ref=fm.id, stem=slugify(fm.title), body=body), deadline=deadline
    )
    outcome = single.outcome
    if single.result is None:
        if outcome.status in ("deferred", "exhausted"):
            return _deferred(resource, entry, outcome.detail)
        category = outcome.category.value if outcome.category else "unknown"
        entry.status = "failed"
        entry.attempts += 1
        entry.last_error_category = category
        entry.last_error = outcome.detail[:1000]
        entry.provider, entry.model = outcome.provider, outcome.model
        entry.updated_at = stamp()
        save_state(paths, state, now_iso=entry.updated_at)
        return EnrichOutcome(
            fm.id,
            resource.path,
            EnrichStatus.FAILED,
            outcome.detail[:500],
            provider=outcome.provider,
            model=outcome.model,
            category=category,
        )
    destination = _write(single.result, fm, body, source, paths, state, stamp=stamp)
    entry.status = "enriched"
    entry.path = relpath(destination, paths.root)
    entry.provider, entry.model = single.result.provider, single.result.model
    entry.attempts += 1
    entry.last_error_category, entry.last_error = None, ""
    entry.updated_at = stamp()
    state.in_flight = None
    save_state(paths, state, now_iso=entry.updated_at)
    detail = f"{fm.category} -> {single.result.category}"
    return EnrichOutcome(
        fm.id,
        resource.path,
        EnrichStatus.ENRICHED,
        detail,
        destination=entry.path,
        provider=entry.provider,
        model=entry.model,
    )


def _write(
    result: ClassificationResult,
    fm: FrontMatter,
    body: str,
    source: Path,
    paths: RepoPaths,
    state: EnrichState,
    *,
    stamp: Callable[[], str],
) -> Path:
    """Write the upgraded document; announce a category move before making it."""
    updated = replace(
        fm,
        category=result.category,
        format=result.format,
        language=result.language,
        tags=result.tags,
        summary=result.summary,
        authors=fm.authors or extract_authors(body),
        classification=Classification("llm", result.confidence, result.model),
        classified_by=classified_by("llm", provider=result.provider, model=result.model),
    )
    text = render_document(updated, body)
    if updated.category == fm.category:
        atomic_write_text(source, text)
        return source
    directory = paths.library / updated.category
    directory.mkdir(parents=True, exist_ok=True)
    destination = _unique_destination(directory, slugify(updated.title))
    state.in_flight = InFlightMove(
        fm.id, relpath(source, paths.root), relpath(destination, paths.root)
    )
    save_state(paths, state, now_iso=stamp())
    atomic_write_text(destination, text)
    source.unlink()
    return destination
