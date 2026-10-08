"""LLM-backed classifier built on the rotation engine.

Two entry points share one validation path:

* :meth:`LLMClassifier.classify_batch` (ingest) sends a batch and validates
  each returned item against the taxonomy. Anything the model gets wrong
  (unknown label, missing document, low confidence, a refusal) falls back to
  the deterministic heuristic for that single document, and if the engine
  cannot serve the batch at all the whole batch falls back — new submissions
  are always filed.
* :meth:`LLMClassifier.classify_one` (enrich) sends one document and hands the
  engine a check that rejects an unusable answer *with its reason*, so the
  engine retries or rotates instead of accepting garbage, and the caller learns
  exactly why a resource was not enriched. It never falls back to the
  heuristic: an enrichment either upgrades a resource or leaves it untouched.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from cyberkb.classify import heuristic
from cyberkb.classify.base import ClassificationResult, Document
from cyberkb.classify.schema import (
    MAX_SAMPLE_CHARS,
    MAX_TAGS,
    build_prompt,
    response_schema,
    system_instruction,
)
from cyberkb.providers.rotation import GenerationRequest
from cyberkb.textutil import plain_text, truncate

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping, Sequence

    from cyberkb.providers.rotation import GenerationOutcome, RotationEngine
    from cyberkb.taxonomy import Taxonomy

__all__ = ["MIN_CONFIDENCE", "LLMClassifier", "SingleClassification"]

MIN_CONFIDENCE = 0.35
_MAX_TITLE = 200
_MAX_SUMMARY = 300
_MIN_DOC_CHARS = 600
# Openings of a refusal or meta-answer instead of a summary of the document
# (matched after typographic apostrophes are folded to ASCII).
_REFUSAL_RE = re.compile(
    r"^\s*(i\s*'?m\s+sorry|i\s+am\s+sorry|sorry,|i\s+can(?:not|'t)|"
    r"i\s+(?:am|'m)\s+unable|as\s+an\s+ai\b|i\s+won't)",
    re.IGNORECASE,
)
_APOSTROPHES = str.maketrans({"\u2019": "'", "\u2018": "'"})


@dataclass(frozen=True, slots=True)
class SingleClassification:
    """The result of classifying one document for enrichment."""

    result: ClassificationResult | None
    outcome: GenerationOutcome


class LLMClassifier:
    """Classify through the rotation engine, validating every answer."""

    def __init__(self, engine: RotationEngine, taxonomy: Taxonomy) -> None:
        """Bind the rotation engine and the taxonomy it must obey."""
        self._engine = engine
        self._taxonomy = taxonomy
        self._schema = response_schema(taxonomy)
        self._system = system_instruction(taxonomy)

    @property
    def engine(self) -> RotationEngine:
        """The rotation engine serving this classifier."""
        return self._engine

    def request(
        self,
        documents: Sequence[Document],
        *,
        single: bool,
        deadline: float | None = None,
    ) -> GenerationRequest:
        """Build the engine request for ``documents``.

        With ``single`` the answer must contain a valid classification of the
        one document; otherwise any well-formed batch answer is accepted and
        validated per document afterwards.
        """
        triples = [(d.ref, d.stem, d.body) for d in documents]
        count = max(1, len(documents))

        def prompt_for(body_chars: int) -> str:
            return build_prompt(triples, max_chars=max(1, body_chars // count))

        def check(payload: Mapping[str, Any]) -> str | None:
            items = payload.get("classifications")
            if not isinstance(items, list) or not items:
                return "the answer has no classifications"
            if not single:
                return None
            return self.problem(documents[0], _item_for(documents[0].ref, items))

        return GenerationRequest(
            system=self._system,
            schema=self._schema,
            prompt_for=prompt_for,
            check=check,
            ref=",".join(d.ref for d in documents),
            max_body_chars=MAX_SAMPLE_CHARS * count,
            min_body_chars=_MIN_DOC_CHARS * count,
            deadline=deadline,
        )

    def classify_batch(self, documents: Sequence[Document]) -> list[ClassificationResult]:
        """Classify ``documents``; fall back to the heuristic wherever the LLM cannot."""
        if not documents:
            return []
        outcome = self._engine.generate(self.request(documents, single=False))
        if outcome.result is None:
            return [heuristic.classify(d, self._taxonomy) for d in documents]
        items = outcome.result.payload.get("classifications", [])
        return [
            self.interpret(
                d, _item_for(d.ref, items), outcome.result.provider, outcome.result.model
            )
            or heuristic.classify(d, self._taxonomy)
            for d in documents
        ]

    def classify_one(self, document: Document, *, deadline: float | None) -> SingleClassification:
        """Classify one document; ``result`` is ``None`` unless the engine succeeded."""
        outcome = self._engine.generate(self.request([document], single=True, deadline=deadline))
        if outcome.result is None:
            return SingleClassification(None, outcome)
        item = _item_for(document.ref, outcome.result.payload.get("classifications", []))
        result = self.interpret(document, item, outcome.result.provider, outcome.result.model)
        return SingleClassification(result, outcome)

    def problem(self, document: Document, item: Mapping[str, Any] | None) -> str | None:
        """Why ``item`` is not a usable classification of ``document`` (``None`` if it is)."""
        if not item:
            return f"no classification for ref {document.ref!r}"
        return next(self._problems(item), None)

    def _problems(self, item: Mapping[str, Any]) -> Iterator[str]:
        """Every defect of ``item``, in check order (consumed lazily: first one wins)."""
        category = item.get("category")
        confidence = item.get("confidence")
        if category not in self._taxonomy.category_ids:
            yield f"unknown category {category!r}"
        if item.get("format") not in self._taxonomy.format_ids:
            yield "unknown format"
        if item.get("language") not in self._taxonomy.language_ids:
            yield "unknown language"
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            yield "confidence is not a number"
        elif not 0.0 <= float(confidence) <= 1.0:
            yield f"confidence {confidence} is outside [0, 1]"
        elif float(confidence) < MIN_CONFIDENCE:
            yield f"confidence {float(confidence):.2f} is below {MIN_CONFIDENCE}"
        if self._taxonomy.category(str(category)).staging:
            yield "the staging category is not a classification"
        summary = plain_text(str(item.get("summary", "")))
        if not summary:
            yield "empty summary"
        if _REFUSAL_RE.match(summary.translate(_APOSTROPHES)):
            yield "the summary is a refusal, not a description of the document"

    def interpret(
        self,
        document: Document,
        item: Mapping[str, Any] | None,
        provider: str,
        model: str,
    ) -> ClassificationResult | None:
        """Turn a validated answer item into a result, or ``None`` if it is unusable."""
        if item is None or self.problem(document, item) is not None:
            return None
        title = plain_text(str(item.get("title", "")), _MAX_TITLE) or heuristic.infer_title(
            document.body, document.stem
        )
        raw_tags = item.get("tags")
        listed = raw_tags if isinstance(raw_tags, list) else []
        tags = tuple(sorted({t for t in listed if t in self._taxonomy.tag_ids}))[:MAX_TAGS]
        return ClassificationResult(
            ref=document.ref,
            category=str(item["category"]),
            format=str(item["format"]),
            language=str(item["language"]),
            title=title,
            confidence=round(float(item["confidence"]), 2),
            method="llm",
            tags=tags,
            summary=truncate(plain_text(str(item.get("summary", ""))), _MAX_SUMMARY),
            model=model,
            provider=provider,
        )


def _item_for(ref: str, items: object) -> dict[str, Any] | None:
    """The answer item echoing ``ref`` (first match wins), if any."""
    for item in items if isinstance(items, list) else []:
        if isinstance(item, dict) and item.get("ref") == ref:
            return item
    return None
