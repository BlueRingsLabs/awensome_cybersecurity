"""Runtime configuration from environment variables.

Only the ingestion path needs configuration, and all of it is optional: with
no API key the pipeline classifies heuristically, so the CI job never fails
for a missing secret. The default model chain lists a current Gemini Flash
model first and falls back through older ones, because Google rotates model
availability (ADR-0005); the client tries each in order.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ["DEFAULT_MODELS", "IngestConfig"]

# Ordered newest-to-oldest; the client uses the first that is served.
DEFAULT_MODELS: tuple[str, ...] = (
    "gemini-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
)
_MIN_BATCH = 1
_MAX_BATCH = 50
_DEFAULT_BATCH = 10


def _int(env: Mapping[str, str], key: str, default: int, low: int, high: int) -> int:
    try:
        value = int(env.get(key, str(default)))
    except ValueError:
        return default
    return max(low, min(high, value))


@dataclass(frozen=True, slots=True)
class IngestConfig:
    """Resolved ingestion configuration."""

    api_key: str | None
    models: tuple[str, ...]
    batch_size: int
    max_retries: int
    timeout: float

    @property
    def use_llm(self) -> bool:
        """``True`` when an API key is present, enabling LLM classification."""
        return bool(self.api_key)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> IngestConfig:
        """Build configuration from ``env`` (defaults to :data:`os.environ`)."""
        env = os.environ if env is None else env
        key = (env.get("GEMINI_API_KEY") or "").strip() or None
        models_raw = (env.get("CYBERKB_MODELS") or "").strip()
        models = tuple(m.strip() for m in models_raw.split(",") if m.strip()) or DEFAULT_MODELS
        return cls(
            api_key=key,
            models=models,
            batch_size=_int(env, "CYBERKB_BATCH_SIZE", _DEFAULT_BATCH, _MIN_BATCH, _MAX_BATCH),
            max_retries=_int(env, "CYBERKB_MAX_RETRIES", 5, 1, 10),
            timeout=float(_int(env, "CYBERKB_TIMEOUT", 60, 5, 300)),
        )
