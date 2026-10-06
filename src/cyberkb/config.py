"""Runtime configuration from environment variables.

Classification is multi-provider and entirely optional: a provider is active
only when its key is present, and with no keys the pipeline classifies with the
deterministic heuristic, so the CI job never fails for a missing secret. The
fallback order is configurable (``LLM_PROVIDER_ORDER``); models are no longer
hard-coded but discovered and validated per provider at run time (ADR-0007),
with ``CYBERKB_MODELS`` kept only as an optional Gemini-preference hint.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from cyberkb.providers.registry import is_registered

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ["DEFAULT_MODELS", "DEFAULT_PROVIDER_ORDER", "IngestConfig"]

# A Gemini-preference hint retained for backward compatibility; discovery is
# dynamic, so this only nudges Gemini model choice when the API lists them.
DEFAULT_MODELS: tuple[str, ...] = (
    "gemini-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
)
DEFAULT_PROVIDER_ORDER: tuple[str, ...] = ("gemini", "openrouter", "huggingface")
_MIN_BATCH = 1
_MAX_BATCH = 50
_DEFAULT_BATCH = 10


def _int(env: Mapping[str, str], key: str, default: int, low: int, high: int) -> int:
    try:
        value = int(env.get(key, str(default)))
    except ValueError:
        return default
    return max(low, min(high, value))


def _csv(env: Mapping[str, str], key: str, default: tuple[str, ...]) -> tuple[str, ...]:
    parsed = tuple(item.strip() for item in (env.get(key) or "").split(",") if item.strip())
    return parsed or default


def _clean(value: str | None) -> str | None:
    return (value or "").strip() or None


@dataclass(frozen=True, slots=True)
class IngestConfig:
    """Resolved ingestion configuration."""

    api_key: str | None
    openrouter_key: str | None
    hf_key: str | None
    models: tuple[str, ...]
    provider_order: tuple[str, ...]
    batch_size: int
    max_retries: int
    timeout: float

    @property
    def use_llm(self) -> bool:
        """``True`` when at least one provider is configured with a key."""
        return bool(self.active_providers())

    def active_providers(self) -> tuple[tuple[str, str], ...]:
        """Configured providers as ``(name, api_key)`` in fallback order.

        Only names that are registered *and* have a key are included, so the
        order can safely name providers whose keys are absent this run.
        """
        keys: dict[str, str | None] = {
            "gemini": self.api_key,
            "openrouter": self.openrouter_key,
            "huggingface": self.hf_key,
        }
        return tuple(
            (name, key)
            for name in self.provider_order
            if is_registered(name) and (key := keys.get(name)) is not None
        )

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> IngestConfig:
        """Build configuration from ``env`` (defaults to :data:`os.environ`)."""
        env = os.environ if env is None else env
        return cls(
            api_key=_clean(env.get("GEMINI_API_KEY")),
            openrouter_key=_clean(env.get("OPENROUTER_API_KEY")),
            hf_key=_clean(env.get("HF_TOKEN")),
            models=_csv(env, "CYBERKB_MODELS", DEFAULT_MODELS),
            provider_order=_csv(env, "LLM_PROVIDER_ORDER", DEFAULT_PROVIDER_ORDER),
            batch_size=_int(env, "CYBERKB_BATCH_SIZE", _DEFAULT_BATCH, _MIN_BATCH, _MAX_BATCH),
            max_retries=_int(env, "CYBERKB_MAX_RETRIES", 5, 1, 10),
            timeout=float(_int(env, "CYBERKB_TIMEOUT", 60, 5, 300)),
        )
