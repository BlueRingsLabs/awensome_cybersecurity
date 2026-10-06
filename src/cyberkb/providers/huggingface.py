"""Hugging Face provider via the OpenAI-compatible Inference router.

The router at ``router.huggingface.co/v1`` speaks the same dialect as
OpenRouter, so the call path is inherited. Discovery keeps conversational /
instruction-tuned models and drops ones too large for the serverless free tier
(about US$0.10/month of credit, models under ~10 GB), ranking small, strong
instruction-followers first. Before a model is used, :meth:`available` consults
the model-status endpoint so a cold or gated model is skipped rather than
burning a call on a 503.
"""

from __future__ import annotations

from typing import ClassVar, override

from cyberkb.errors import ProviderError
from cyberkb.providers.base import ModelCandidate
from cyberkb.providers.openai_compat import OpenAICompatProvider

__all__ = ["HuggingFaceProvider"]

_STATUS_ROOT = "https://api-inference.huggingface.co/status"
# Too large for the serverless free tier; skipped at discovery.
_TOO_LARGE = ("70b", "72b", "123b", "141b", "180b", "405b", "8x22")
# Small, strong instruction-followers ranked for classification/summarisation.
_GOOD_FAMILIES: tuple[tuple[str, float], ...] = (
    ("qwen2.5-14b", 0.88),
    ("qwen2.5-7b", 0.86),
    ("llama-3.1-8b", 0.86),
    ("gemma-2-9b", 0.82),
    ("gemma-3", 0.82),
    ("llama-3.3", 0.80),
    ("mistral-nemo", 0.80),
    ("phi-4", 0.80),
    ("mistral-7b", 0.78),
    ("llama-3.2-3b", 0.76),
    ("qwen2.5", 0.78),
)
_BASE_SCORE = 0.60
_INSTRUCT_HINTS = ("instruct", "-it", "chat")
_LOADABLE_STATES = frozenset({"loadable", "loaded", "warm"})


def _looks_instruct(model_id: str) -> bool:
    lowered = model_id.lower()
    return any(hint in lowered for hint in _INSTRUCT_HINTS)


def _family_score(model_id: str) -> tuple[float, str]:
    lowered = model_id.lower()
    for needle, score in _GOOD_FAMILIES:
        if needle in lowered:
            return score, f"free-tier Hugging Face model ({needle})"
    return _BASE_SCORE, "instruction-tuned Hugging Face model"


class HuggingFaceProvider(OpenAICompatProvider):
    """Free-tier Hugging Face Inference models via the OpenAI-compatible router."""

    name: ClassVar[str] = "huggingface"
    base_url: ClassVar[str] = "https://router.huggingface.co/v1"

    @override
    def available(self, model: str) -> bool:
        """Consult the model-status endpoint; ``True`` only when loadable/loaded."""
        try:
            status = self._get_mapping(
                f"{_STATUS_ROOT}/{model}", headers=self._auth_headers(json_body=False)
            )
        except ProviderError:
            return False
        if status.get("loaded") is True:
            return True
        state = status.get("state")
        return isinstance(state, str) and state.lower() in _LOADABLE_STATES

    @override
    def _candidate(self, entry: object) -> ModelCandidate | None:
        if not isinstance(entry, dict):
            return None
        model_id = entry.get("id")
        if not isinstance(model_id, str):
            return None
        lowered = model_id.lower()
        if any(big in lowered for big in _TOO_LARGE) or not _looks_instruct(model_id):
            return None
        score, rationale = _family_score(model_id)
        return ModelCandidate(
            provider=self.name,
            model_id=model_id,
            is_free=True,
            context_window=None,
            score=score,
            rationale=rationale,
        )
