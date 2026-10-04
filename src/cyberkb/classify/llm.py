"""LLM-backed classifier built on :class:`cyberkb.llm.GeminiClient`.

Each result is validated against the taxonomy; anything the model gets wrong
(unknown label, missing document, low confidence) falls back to the
deterministic heuristic for that single document, so the batch as a whole can
never produce an invalid classification or silently drop a file.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cyberkb.classify import heuristic
from cyberkb.classify.base import ClassificationResult, Document
from cyberkb.classify.schema import build_prompt, response_schema, system_instruction
from cyberkb.errors import LLMError
from cyberkb.textutil import plain_text, truncate

if TYPE_CHECKING:
    from collections.abc import Sequence

    from cyberkb.llm import GeminiClient
    from cyberkb.taxonomy import Taxonomy

__all__ = ["LLMClassifier"]

_MIN_CONFIDENCE = 0.35
_MAX_TITLE = 200
_MAX_SUMMARY = 300


class LLMClassifier:
    """Classify batches of documents with an LLM and a heuristic safety net."""

    def __init__(self, client: GeminiClient, taxonomy: Taxonomy) -> None:
        """Bind a client and the taxonomy it must obey."""
        self._client = client
        self._taxonomy = taxonomy
        self._schema = response_schema(taxonomy)
        self._system = system_instruction(taxonomy)

    def classify_batch(self, documents: Sequence[Document]) -> list[ClassificationResult]:
        """Classify ``documents``; fall back to the heuristic on any failure.

        If the whole request fails (network, auth, exhausted retries), every
        document in the batch is classified heuristically. If the request
        succeeds but omits or mis-answers some documents, only those fall
        back, so a partial model answer is still used where it is valid.
        """
        if not documents:
            return []
        prompt = build_prompt([(d.ref, d.stem, d.body) for d in documents])
        try:
            payload = self._client.generate_json(self._system, prompt, self._schema)
        except LLMError:
            return [self._fallback(d) for d in documents]
        model = self._client.active_model
        by_ref = {
            item.get("ref"): item
            for item in payload.get("classifications", [])
            if isinstance(item, dict)
        }
        results: list[ClassificationResult] = []
        for document in documents:
            validated = self._validate(document, by_ref.get(document.ref), model)
            results.append(validated or self._fallback(document))
        return results

    def _fallback(self, document: Document) -> ClassificationResult:
        return heuristic.classify(document, self._taxonomy)

    def _validate(
        self, document: Document, item: dict[str, Any] | None, model: str | None
    ) -> ClassificationResult | None:
        if not item:
            return None
        category = item.get("category")
        fmt = item.get("format")
        language = item.get("language")
        confidence = item.get("confidence")
        if (
            category not in self._taxonomy.category_ids
            or fmt not in self._taxonomy.format_ids
            or language not in self._taxonomy.language_ids
            or not isinstance(confidence, (int, float))
            or isinstance(confidence, bool)
            or not 0.0 <= float(confidence) <= 1.0
            or float(confidence) < _MIN_CONFIDENCE
            or self._taxonomy.category(category).staging
        ):
            return None
        title = plain_text(str(item.get("title", "")), _MAX_TITLE) or heuristic.infer_title(
            document.body, document.stem
        )
        tags = tuple(sorted({t for t in item.get("tags", []) if t in self._taxonomy.tag_ids}))
        summary = truncate(plain_text(str(item.get("summary", ""))), _MAX_SUMMARY)
        return ClassificationResult(
            ref=document.ref,
            category=category,
            format=fmt,
            language=language,
            title=title,
            confidence=round(float(confidence), 2),
            method="llm",
            tags=tags,
            summary=summary,
            model=model,
        )
