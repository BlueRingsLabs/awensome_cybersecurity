"""Types shared by the classification engines."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cyberkb.frontmatter import ClassificationMethod

__all__ = ["ClassificationResult", "Document"]


@dataclass(frozen=True, slots=True)
class Document:
    """A sanitised document handed to a classifier.

    Attributes:
        ref: opaque identifier used to match results to inputs; never the
            contributor-controlled filename.
        stem: original filename without extension (a useful title signal).
        body: sanitised Markdown body without front matter.
    """

    ref: str
    stem: str
    body: str


@dataclass(frozen=True, slots=True)
class ClassificationResult:
    """Outcome of classifying one document."""

    ref: str
    category: str
    format: str
    language: str
    title: str
    confidence: float
    method: ClassificationMethod
    tags: tuple[str, ...] = ()
    summary: str = ""
    model: str | None = None
    scores: dict[str, float] = field(default_factory=dict, compare=False)
