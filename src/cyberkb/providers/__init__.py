"""LLM provider layer: two verified adapters behind one interface, one rotation engine.

Public surface:

* :class:`LLMProvider` / :class:`HttpProviderBase` -- the adapter contract and
  its shared REST machinery.
* :class:`GoogleProvider` (Google AI Studio: Gemini and Gemma) and
  :class:`GroqProvider` -- the two shipped adapters (ADR-0008).
* :func:`load_model_catalog` / :func:`resolve_models` -- the reviewed model
  catalog (``schema/llm-models.yaml``) and its mapping onto live API ids.
* :class:`RotationEngine` -- per-model, per-provider routing with pacing,
  cooldowns, lazy validation, retries and list passes.
* :data:`PROVIDER_CLASSES` / :func:`build_providers` -- the adapter registry.
"""

from __future__ import annotations

from cyberkb.providers.base import (
    HttpProviderBase,
    LLMProvider,
    ProviderResult,
    classify_http_status,
    retry_after_seconds,
)
from cyberkb.providers.catalog import (
    ListedModel,
    ModelCatalog,
    load_model_catalog,
    resolve_models,
)
from cyberkb.providers.google import GoogleProvider
from cyberkb.providers.governor import DailyUsage, ModelGovernor
from cyberkb.providers.groq import GroqProvider
from cyberkb.providers.registry import PROVIDER_CLASSES, build_providers, provider_names
from cyberkb.providers.rotation import (
    GenerationOutcome,
    GenerationRequest,
    RotationEngine,
    RotationSettings,
)

__all__ = [
    "PROVIDER_CLASSES",
    "DailyUsage",
    "GenerationOutcome",
    "GenerationRequest",
    "GoogleProvider",
    "GroqProvider",
    "HttpProviderBase",
    "LLMProvider",
    "ListedModel",
    "ModelCatalog",
    "ModelGovernor",
    "ProviderResult",
    "RotationEngine",
    "RotationSettings",
    "build_providers",
    "classify_http_status",
    "load_model_catalog",
    "provider_names",
    "resolve_models",
    "retry_after_seconds",
]
