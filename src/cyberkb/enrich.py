"""Enrich existing library resources with LLM classification and summaries.

Most of the migrated corpus was filed by the offline heuristic with an empty
summary. :func:`enrich_library` re-runs each heuristically-classified resource
through the multi-provider classifier and, when a provider returns a valid
answer, adopts its category, format, language, tags and one-line summary,
refreshes empty author lists from the body, and stamps the provenance. Manual
classifications (including the reference-only works) are never touched, and a
resource whose providers are all unavailable is left exactly as it was, so the
command is safe to re-run until the whole library is enriched.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, replace
from enum import StrEnum
from typing import TYPE_CHECKING

from cyberkb.authors import extract_authors
from cyberkb.classify.base import Document
from cyberkb.frontmatter import Classification, FrontMatter, render_document, split_front_matter
from cyberkb.fsutil import read_text, relpath
from cyberkb.library import MAX_RESOURCE_BYTES, load_library
from cyberkb.provenance import classified_by
from cyberkb.textutil import slugify

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from cyberkb.classify.llm import LLMClassifier
    from cyberkb.library import Resource
    from cyberkb.paths import RepoPaths
    from cyberkb.taxonomy import Taxonomy

__all__ = ["EnrichOutcome", "EnrichReport", "EnrichStatus", "enrich_library"]


class EnrichStatus(StrEnum):
    """What happened to one resource during enrichment."""

    ENRICHED = "enriched"
    UNCHANGED = "unchanged"
    SKIPPED = "skipped"
    DEFERRED = "deferred"


@dataclass(frozen=True, slots=True)
class EnrichOutcome:
    """Result of considering one resource for enrichment."""

    resource_id: str
    path: str
    status: EnrichStatus
    detail: str = ""
    destination: str | None = None


@dataclass(frozen=True, slots=True)
class EnrichReport:
    """Aggregate outcome of an enrichment run."""

    outcomes: tuple[EnrichOutcome, ...]

    @property
    def enriched(self) -> int:
        """Count of resources whose classification was upgraded by a provider."""
        return sum(1 for o in self.outcomes if o.status is EnrichStatus.ENRICHED)

    @property
    def unchanged(self) -> int:
        """Count left as-is (already LLM-classified, or no provider available)."""
        return sum(1 for o in self.outcomes if o.status is EnrichStatus.UNCHANGED)

    @property
    def skipped(self) -> int:
        """Count deliberately skipped (manual classifications)."""
        return sum(1 for o in self.outcomes if o.status is EnrichStatus.SKIPPED)

    @property
    def deferred(self) -> int:
        """Count needing enrichment but left for a later run (run budget reached)."""
        return sum(1 for o in self.outcomes if o.status is EnrichStatus.DEFERRED)


def _unique_destination(directory: Path, slug: str) -> Path:
    candidate = directory / f"{slug}.md"
    index = 2
    while candidate.exists():
        candidate = directory / f"{slug}-{index}.md"
        index += 1
    return candidate


def _needs_llm(fm: FrontMatter, *, force: bool) -> bool:
    """Whether this resource would consume an LLM call.

    Mirrors the early-return guards in :func:`_enrich_one`: manual
    classifications are preserved and already-LLM ones are left alone unless
    ``force``. Only resources for which this is ``True`` count against the run
    budget, so skips never consume the ``limit`` or the time budget.
    """
    method = fm.classification.method
    if method == "manual":
        return False
    return not (method == "llm" and not force)


def _budget_reached(
    attempted: int,
    *,
    limit: int | None,
    start: float,
    clock: Callable[[], float],
    max_seconds: float | None,
) -> bool:
    """Whether the per-run budget (resource count or wall-clock time) is spent."""
    if limit is not None and attempted >= limit:
        return True
    return max_seconds is not None and clock() - start >= max_seconds


def enrich_library(
    paths: RepoPaths,
    taxonomy: Taxonomy,
    classifier: LLMClassifier,
    *,
    force: bool = False,
    limit: int | None = None,
    max_seconds: float | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> EnrichReport:
    """Enrich heuristically-classified resources; return a per-resource report.

    With ``force``, resources already classified by an LLM are re-processed too;
    manual classifications are always preserved.

    ``limit`` caps how many resources are sent to the LLM this run and
    ``max_seconds`` caps the wall-clock time spent starting new work; resources
    that still need enrichment past either budget are reported as ``DEFERRED``
    rather than processed. Because enriched files are written as the loop runs
    and already-classified resources are skipped, a bounded run commits real
    progress and the command can simply be re-run to continue — which is what
    makes backfilling the whole corpus possible within a CI time limit and a
    provider's free-tier rate cap.
    """
    library = load_library(paths, taxonomy)
    outcomes: list[EnrichOutcome] = []
    attempted = 0
    start = clock()
    for resource in library.resources:
        fm = resource.front_matter
        needs = _needs_llm(fm, force=force)
        if needs and _budget_reached(
            attempted, limit=limit, start=start, clock=clock, max_seconds=max_seconds
        ):
            outcomes.append(
                EnrichOutcome(fm.id, resource.path, EnrichStatus.DEFERRED, "run budget reached")
            )
            continue
        outcomes.append(_enrich_one(resource, paths, classifier, force=force))
        if needs:
            attempted += 1
    return EnrichReport(tuple(outcomes))


def _enrich_one(
    resource: Resource,
    paths: RepoPaths,
    classifier: LLMClassifier,
    *,
    force: bool,
) -> EnrichOutcome:
    fm = resource.front_matter
    if fm.classification.method == "manual":
        return EnrichOutcome(
            fm.id, resource.path, EnrichStatus.SKIPPED, "manual classification kept"
        )
    if fm.classification.method == "llm" and not force:
        return EnrichOutcome(fm.id, resource.path, EnrichStatus.UNCHANGED, "already LLM-classified")

    source = paths.root / resource.path
    _, body = split_front_matter(read_text(source, root=paths.root, max_bytes=MAX_RESOURCE_BYTES))
    result = classifier.classify_batch([Document(ref=fm.id, stem=slugify(fm.title), body=body)])[0]
    if result.method != "llm":
        return EnrichOutcome(fm.id, resource.path, EnrichStatus.UNCHANGED, "no provider available")

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
    destination = _write(updated, body, source, paths, previous_category=fm.category)
    detail = f"{fm.category} -> {result.category} via {result.provider}:{result.model}"
    return EnrichOutcome(
        fm.id, resource.path, EnrichStatus.ENRICHED, detail, relpath(destination, paths.root)
    )


def _write(
    updated: FrontMatter,
    body: str,
    source: Path,
    paths: RepoPaths,
    *,
    previous_category: str,
) -> Path:
    directory = paths.library / updated.category
    directory.mkdir(parents=True, exist_ok=True)
    if updated.category == previous_category:
        destination = source
    else:
        destination = _unique_destination(directory, slugify(updated.title))
    destination.write_text(render_document(updated, body), encoding="utf-8")
    if destination != source:
        source.unlink()
    return destination
