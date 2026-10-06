"""OpenRouter provider: a broad catalog of free, OpenAI-compatible models.

Discovery keeps only models that are free to call — either the ``:free`` id
suffix or zero prompt/completion pricing — because the pipeline must run on the
free tier. Candidates are ranked by model family (the strongest open
instruction-followers for classification first) with a small bonus for a larger
context window. As a documented last resort the Free Models Router is appended
at the lowest priority, so if every explicitly chosen model is unavailable the
provider can still auto-select something free.

Free-tier limits apply (about 20 requests/minute and 50/day, or 1,000/day once
US$10 of credit has been purchased); the orchestrator rotates on a 429 and the
run report records how often that happened.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, override

from cyberkb.providers.base import ModelCandidate
from cyberkb.providers.openai_compat import OpenAICompatProvider

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ["OpenRouterProvider"]

# Model families ranked by their fit for cybersecurity classification and
# summarisation (strongest instruction-followers first). Justified in ADR-0007.
_FAMILY_SCORES: tuple[tuple[str, float], ...] = (
    ("llama-3.3", 0.92),
    ("llama-3.1", 0.88),
    ("qwen2.5", 0.90),
    ("qwen-2.5", 0.90),
    ("qwen3", 0.90),
    ("deepseek", 0.86),
    ("gemma-3", 0.84),
    ("mixtral", 0.82),
    ("llama-3", 0.82),
    ("gemma-2", 0.80),
    ("mistral", 0.80),
    ("qwen", 0.80),
    ("phi-4", 0.80),
    ("nemotron", 0.80),
    ("gemma", 0.76),
    ("phi-3", 0.74),
)
_BASE_SCORE = 0.60
_CONTEXT_FULL = 200_000
_CONTEXT_BONUS = 0.05
_FREE_ROUTER_ID = "openrouter/auto"
_FREE_ROUTER_SCORE = 0.40


def _zero_price(value: object) -> bool:
    try:
        return float(value) == 0.0  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return False


def _is_free(entry: Mapping[str, object]) -> bool:
    model_id = entry.get("id")
    if isinstance(model_id, str) and model_id.endswith(":free"):
        return True
    pricing = entry.get("pricing")
    return (
        isinstance(pricing, dict)
        and _zero_price(pricing.get("prompt"))
        and _zero_price(pricing.get("completion"))
    )


def _family_score(model_id: str) -> tuple[float, str]:
    lowered = model_id.lower()
    for needle, score in _FAMILY_SCORES:
        if needle in lowered:
            return score, f"free OpenRouter model ({needle} family)"
    return _BASE_SCORE, "free OpenRouter model"


class OpenRouterProvider(OpenAICompatProvider):
    """Free OpenAI-compatible models routed through openrouter.ai."""

    name: ClassVar[str] = "openrouter"
    base_url: ClassVar[str] = "https://openrouter.ai/api/v1"

    @override
    def _extra_headers(self) -> dict[str, str]:
        return {
            "HTTP-Referer": "https://github.com/BlueRingsLabs/awesome_cybersecurity",
            "X-Title": "awesome_cybersecurity",
        }

    @override
    def discover_models(self) -> list[ModelCandidate]:
        """Discovered free models, best first, with the Free Models Router last."""
        candidates = super().discover_models()
        candidates.append(
            ModelCandidate(
                provider=self.name,
                model_id=_FREE_ROUTER_ID,
                is_free=True,
                context_window=None,
                score=_FREE_ROUTER_SCORE,
                rationale="OpenRouter Free Models Router (auto-selects a free model) — last resort",
            ),
        )
        return candidates

    @override
    def _candidate(self, entry: object) -> ModelCandidate | None:
        if not isinstance(entry, dict):
            return None
        model_id = entry.get("id")
        if not isinstance(model_id, str) or "-base" in model_id or not _is_free(entry):
            return None
        score, rationale = _family_score(model_id)
        context = entry.get("context_length")
        context_window = context if isinstance(context, int) else None
        if context_window:
            score = round(score + min(context_window / _CONTEXT_FULL, 1.0) * _CONTEXT_BONUS, 3)
        return ModelCandidate(
            provider=self.name,
            model_id=model_id,
            is_free=True,
            context_window=context_window,
            score=score,
            rationale=rationale,
        )
