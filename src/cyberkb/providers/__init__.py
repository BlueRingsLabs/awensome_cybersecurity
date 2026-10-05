"""Multi-provider LLM layer: interchangeable providers behind one interface.

Public surface:

* :class:`LLMProvider` -- the contract (discover models, classify to JSON,
  health-check); every provider is swappable behind it.
* :class:`HttpProviderBase` / :class:`OpenAICompatProvider` -- shared REST and
  OpenAI-dialect machinery a new provider builds on.
* :class:`GeminiProvider`, :class:`OpenRouterProvider`,
  :class:`HuggingFaceProvider` -- the three shipped providers.
* :data:`PROVIDER_CLASSES` / :func:`provider_names` -- the extensible registry.
* :class:`ModelCandidate`, :class:`ProviderResult`, :class:`HealthResult` --
  the value types the orchestrator exchanges with providers.
"""

from __future__ import annotations

from cyberkb.providers.base import (
    HealthResult,
    HttpProviderBase,
    LLMProvider,
    ModelCandidate,
    ProviderResult,
    classify_http_status,
    retry_after_seconds,
)
from cyberkb.providers.circuit import CircuitBreaker, CircuitState
from cyberkb.providers.gemini import GeminiProvider
from cyberkb.providers.huggingface import HuggingFaceProvider
from cyberkb.providers.openai_compat import OpenAICompatProvider
from cyberkb.providers.openrouter import OpenRouterProvider
from cyberkb.providers.orchestrator import Orchestrator, OrchestratorSettings
from cyberkb.providers.registry import PROVIDER_CLASSES, is_registered, provider_names
from cyberkb.providers.selection import ModelValidation, ProviderSelection, select_models

__all__ = [
    "PROVIDER_CLASSES",
    "CircuitBreaker",
    "CircuitState",
    "GeminiProvider",
    "HealthResult",
    "HttpProviderBase",
    "HuggingFaceProvider",
    "LLMProvider",
    "ModelCandidate",
    "ModelValidation",
    "OpenAICompatProvider",
    "OpenRouterProvider",
    "Orchestrator",
    "OrchestratorSettings",
    "ProviderResult",
    "ProviderSelection",
    "classify_http_status",
    "is_registered",
    "provider_names",
    "retry_after_seconds",
    "select_models",
]
