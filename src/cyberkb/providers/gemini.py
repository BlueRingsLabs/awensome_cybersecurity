"""Google Gemini provider (``generateContent`` with native structured output).

Gemini constrains output with a ``responseSchema`` built from the live
taxonomy, so a hallucinated label is impossible by construction. Discovery
reads the ``models`` listing and keeps only text models that support
``generateContent``, ranking the Flash family first (best quality/latency on
the free tier) ahead of Pro (higher quality but restricted or paid). The free
tier moves over time, so discovery never assumes a model works — it only
proposes; the orchestrator's validation pass confirms it.
"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, ClassVar, override

from cyberkb.errors import FailureCategory
from cyberkb.providers.base import (
    HttpProviderBase,
    ModelCandidate,
    ProviderResult,
    classify_http_status,
)

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any

__all__ = ["GeminiProvider"]

_API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
_OK = 200
_GENERATE_METHOD = "generateContent"
_EXCLUDE = ("embedding", "aqa", "imagen", "vision", "tts", "image-", "-image")
_BLOCK_FINISH = frozenset({"SAFETY", "RECITATION", "BLOCKLIST", "PROHIBITED_CONTENT", "SPII"})
_VERSION_RE = re.compile(r"(\d+(?:\.\d+)?)")
_TEMPERATURE = 0.1


def _rank(model_id: str) -> tuple[float, bool, str]:
    """Score a Gemini model for classification, returning (score, is_free, why)."""
    mid = model_id.lower()
    free = "pro" not in mid
    if "flash-lite" in mid:
        base, note = 0.78, "Flash-Lite: fast, free-tier friendly, solid instruction-following"
    elif "flash" in mid:
        base, note = 0.90, "Flash: best quality/latency balance for classification on the free tier"
    elif "pro" in mid:
        base, note = 0.60, "Pro: highest quality but restricted or paid on the free tier"
    else:
        base, note = 0.50, "general-purpose Gemini text model"
    match = _VERSION_RE.search(mid)
    version = float(match.group(1)) if match else 0.0
    bonus = 0.05 if "latest" in mid else min(version, 9.9) * 0.01
    return round(base + bonus, 3), free, note


class GeminiProvider(HttpProviderBase):
    """Classify batches with Gemini's schema-constrained ``generateContent``."""

    name: ClassVar[str] = "gemini"

    def _headers(self, *, json_body: bool) -> dict[str, str]:
        headers = {"x-goog-api-key": self._api_key}
        if json_body:
            headers["Content-Type"] = "application/json"
        return headers

    @override
    def discover_models(self) -> list[ModelCandidate]:
        """List text models that support generateContent, Flash-family first."""
        data = self._get_mapping(f"{_API_ROOT}/models", headers=self._headers(json_body=False))
        listed = data.get("models")
        entries = listed if isinstance(listed, list) else []
        candidates = [c for e in entries if (c := self._candidate(e)) is not None]
        candidates.sort(key=lambda c: c.score, reverse=True)
        return candidates

    def _candidate(self, entry: object) -> ModelCandidate | None:
        if not isinstance(entry, dict):
            return None
        name = entry.get("name")
        methods = entry.get("supportedGenerationMethods")
        if not isinstance(name, str) or not isinstance(methods, list):
            return None
        if _GENERATE_METHOD not in methods:
            return None
        model_id = name.rsplit("/", 1)[-1]
        if not model_id.startswith("gemini") or any(token in model_id for token in _EXCLUDE):
            return None
        score, free, rationale = _rank(model_id)
        context = entry.get("inputTokenLimit")
        return ModelCandidate(
            provider=self.name,
            model_id=model_id,
            is_free=free,
            context_window=context if isinstance(context, int) else None,
            score=score,
            rationale=rationale,
        )

    @override
    def complete_json(
        self,
        model: str,
        system: str,
        prompt: str,
        schema: Mapping[str, object],
    ) -> ProviderResult:
        """One schema-constrained generateContent call; failures are categorised."""
        body = json.dumps(
            {
                "systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": _TEMPERATURE,
                    "responseMimeType": "application/json",
                    "responseSchema": dict(schema),
                },
            },
        ).encode("utf-8")
        start = self._clock()
        url = f"{_API_ROOT}/models/{model}:{_GENERATE_METHOD}"
        response = self._send(
            "POST", url, headers=self._headers(json_body=True), body=body, model=model
        )
        if response.status != _OK:
            raise self._fail(
                classify_http_status(response.status, response.text()),
                raw=response.text(),
                status=response.status,
                model=model,
            )
        payload = self._extract(self._decode_object(response.text(), model=model), model=model)
        return ProviderResult(payload, self.name, model, self._elapsed(start))

    def _extract(self, envelope: dict[str, Any], *, model: str) -> dict[str, Any]:
        candidates = envelope.get("candidates")
        if not isinstance(candidates, list) or not candidates:
            feedback = envelope.get("promptFeedback")
            block = feedback.get("blockReason") if isinstance(feedback, dict) else None
            category = FailureCategory.CONTENT_FILTER if block else FailureCategory.INFERENCE_ERROR
            raise self._fail(
                category, raw=f"no usable candidate (blockReason={block})", model=model, status=_OK
            )
        candidate = candidates[0]
        finish = candidate.get("finishReason") if isinstance(candidate, dict) else None
        if finish not in (None, "STOP"):
            category = (
                FailureCategory.CONTENT_FILTER
                if finish in _BLOCK_FINISH
                else FailureCategory.INFERENCE_ERROR
            )
            raise self._fail(category, raw=f"finishReason={finish}", model=model, status=_OK)
        text = _join_parts(candidate)
        if text is None:
            raise self._fail(
                FailureCategory.INFERENCE_ERROR, raw="candidate had no text parts", model=model
            )
        return self._decode_object(text, model=model)


def _join_parts(candidate: object) -> str | None:
    if not isinstance(candidate, dict):
        return None
    content = candidate.get("content")
    parts = content.get("parts") if isinstance(content, dict) else None
    if not isinstance(parts, list):
        return None
    texts = [p["text"] for p in parts if isinstance(p, dict) and isinstance(p.get("text"), str)]
    return "".join(texts) if texts else None
