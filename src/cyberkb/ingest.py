"""Ingestion: turn raw ``inbox/`` submissions into curated library resources.

A submission is a Markdown file a contributor dropped in ``inbox/``. For each
one the pipeline:

1. safely reads and sanitises it (symlink/size/binary guards);
2. rejects empties and oversized blobs with an explicit reason;
3. honours any valid front matter hints the contributor supplied;
4. classifies it (LLM when configured, heuristic otherwise), letting hints
   win over the classifier;
5. detects a redistribution licence from the text;
6. mints a stable content id, builds front matter and writes the final
   document to ``library/<category>/<slug>.md`` without ever overwriting an
   existing file.

The function is pure with respect to its inputs except for the writes it is
asked to perform, and returns a structured outcome per file so the CLI and
tests can assert on exactly what happened.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import TYPE_CHECKING

from cyberkb.authors import extract_authors
from cyberkb.classify.base import Document
from cyberkb.classify.heuristic import classify as heuristic_classify
from cyberkb.errors import ContentRejectedError, FrontMatterError, KBError, UnsafePathError
from cyberkb.frontmatter import (
    Classification,
    FrontMatter,
    render_document,
    split_front_matter,
    validate_contributor_hints,
)
from cyberkb.fsutil import read_text, relpath
from cyberkb.ids import mint_id
from cyberkb.licensing import detect_license
from cyberkb.sanitize import sanitize_markdown
from cyberkb.textutil import slugify, word_count

if TYPE_CHECKING:
    from pathlib import Path

    from cyberkb.classify.base import ClassificationResult
    from cyberkb.classify.llm import LLMClassifier
    from cyberkb.paths import RepoPaths
    from cyberkb.taxonomy import Taxonomy

__all__ = ["IngestOutcome", "IngestReport", "IngestStatus", "ingest_inbox"]

MIN_WORDS = 20
MAX_SUBMISSION_BYTES = 8 * 1024 * 1024


class IngestStatus(StrEnum):
    """What happened to one submission."""

    FILED = "filed"
    REJECTED = "rejected"
    STAGED = "staged"


@dataclass(frozen=True, slots=True)
class IngestOutcome:
    """Result of processing one submission."""

    source: str
    status: IngestStatus
    reason: str = ""
    destination: str | None = None
    resource_id: str | None = None
    category: str | None = None


@dataclass(frozen=True, slots=True)
class IngestReport:
    """Aggregate outcome of an ingestion run."""

    outcomes: tuple[IngestOutcome, ...]

    @property
    def filed(self) -> int:
        """Count of submissions filed into the library."""
        return sum(1 for o in self.outcomes if o.status is IngestStatus.FILED)

    @property
    def staged(self) -> int:
        """Count routed to the staging category for review."""
        return sum(1 for o in self.outcomes if o.status is IngestStatus.STAGED)

    @property
    def rejected(self) -> int:
        """Count rejected by content policy."""
        return sum(1 for o in self.outcomes if o.status is IngestStatus.REJECTED)


def discover_submissions(paths: RepoPaths) -> list[Path]:
    """Return raw Markdown submissions in ``inbox/`` (sorted, top level only)."""
    if not paths.inbox.is_dir():
        return []
    return sorted(p for p in paths.inbox.glob("*.md") if p.is_file())


def _prepare(path: Path, paths: RepoPaths) -> tuple[dict[str, object], str] | IngestOutcome:
    rel = relpath(path, paths.root)
    try:
        text = read_text(path, root=paths.root, max_bytes=MAX_SUBMISSION_BYTES)
    except (UnsafePathError, ContentRejectedError) as exc:
        return IngestOutcome(rel, IngestStatus.REJECTED, reason=str(exc))
    try:
        raw, body = split_front_matter(text)
    except FrontMatterError as exc:
        return IngestOutcome(rel, IngestStatus.REJECTED, reason=str(exc))
    clean = sanitize_markdown(body)
    if word_count(clean) < MIN_WORDS:
        return IngestOutcome(
            rel,
            IngestStatus.REJECTED,
            reason=f"document has fewer than {MIN_WORDS} words of content",
        )
    return (raw or {}), clean


def _unique_destination(directory: Path, slug: str) -> Path:
    candidate = directory / f"{slug}.md"
    index = 2
    while candidate.exists():
        candidate = directory / f"{slug}-{index}.md"
        index += 1
    return candidate


def ingest_inbox(
    paths: RepoPaths,
    taxonomy: Taxonomy,
    *,
    classifier: LLMClassifier | None = None,
    today: date | None = None,
    taken_ids: frozenset[str] = frozenset(),
    batch_size: int = 10,
) -> IngestReport:
    """Ingest every submission in ``inbox/`` and return a per-file report.

    ``classifier`` enables LLM classification; when ``None`` the deterministic
    heuristic is used. ``taken_ids`` seeds collision avoidance with the ids
    already present in the library. ``batch_size`` bounds how many documents
    are sent to the LLM per request.
    """
    today = today or date.today()  # noqa: DTZ011 -- a calendar date, not a timestamp
    taken = set(taken_ids)
    submissions = discover_submissions(paths)
    prepared: list[tuple[Path, dict[str, object], str]] = []
    outcomes: list[IngestOutcome] = []

    for path in submissions:
        prepared_or_rejected = _prepare(path, paths)
        if isinstance(prepared_or_rejected, IngestOutcome):
            outcomes.append(prepared_or_rejected)
            continue
        raw, body = prepared_or_rejected
        prepared.append((path, raw, body))

    documents = [Document(ref=str(i), stem=p.stem, body=b) for i, (p, _, b) in enumerate(prepared)]
    results = _classify(documents, taxonomy, classifier, batch_size)

    for (path, raw, body), result in zip(prepared, results, strict=True):
        outcomes.append(_file_one(path, raw, body, result, paths, taxonomy, today, taken))
    return IngestReport(tuple(outcomes))


def _classify(
    documents: list[Document],
    taxonomy: Taxonomy,
    classifier: LLMClassifier | None,
    batch_size: int,
) -> list[ClassificationResult]:
    if not documents:
        return []
    if classifier is None:
        return [heuristic_classify(d, taxonomy) for d in documents]
    results: list[ClassificationResult] = []
    step = max(1, batch_size)
    for start in range(0, len(documents), step):
        results.extend(classifier.classify_batch(documents[start : start + step]))
    return results


def _file_one(
    path: Path,
    raw: dict[str, object],
    body: str,
    result: ClassificationResult,
    paths: RepoPaths,
    taxonomy: Taxonomy,
    today: date,
    taken: set[str],
) -> IngestOutcome:
    rel = relpath(path, paths.root)
    hints, _ = validate_contributor_hints(raw, taxonomy)
    category = str(hints.get("category", result.category))
    fmt = str(hints.get("format", result.format))
    language = str(hints.get("language", result.language))
    title = str(hints.get("title", result.title))
    tags = tuple(hints["tags"]) if "tags" in hints else result.tags
    summary = str(hints.get("summary", result.summary))
    authors = tuple(hints["authors"]) if "authors" in hints else extract_authors(body)
    source_url = hints.get("source_url") or None
    license_id = str(hints["license"]) if "license" in hints else detect_license(body).license
    confidence = 1.0 if "category" in hints else result.confidence
    method = "manual" if "category" in hints else result.method

    resource_id = mint_id(body, taken=frozenset(taken))
    taken.add(resource_id)
    try:
        front_matter = FrontMatter(
            id=resource_id,
            title=title,
            category=category,
            format=fmt,
            language=language,
            license=license_id,
            added=today,
            classification=Classification(
                method, confidence, result.model if method == "llm" else None
            ),
            tags=tags,
            summary=summary,
            authors=authors,
            source_url=source_url if isinstance(source_url, str) else None,
        )
    except KBError as exc:  # pragma: no cover - defensive; inputs are pre-validated
        return IngestOutcome(rel, IngestStatus.REJECTED, reason=str(exc))

    directory = paths.library / category
    directory.mkdir(parents=True, exist_ok=True)
    destination = _unique_destination(directory, slugify(title or path.stem))
    destination.write_text(render_document(front_matter, body), encoding="utf-8")
    path.unlink()

    status = IngestStatus.STAGED if taxonomy.category(category).staging else IngestStatus.FILED
    return IngestOutcome(
        source=rel,
        status=status,
        destination=relpath(destination, paths.root),
        resource_id=resource_id,
        category=category,
    )
