"""The registry of known providers — the one place a new provider is listed.

Adding a fourth provider is: implement :class:`cyberkb.providers.base.LLMProvider`
(usually via ``HttpProviderBase`` or ``OpenAICompatProvider``) and add it to
:data:`PROVIDER_CLASSES`. The orchestrator and config need no change; they build
whatever is registered and configured.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cyberkb.providers.gemini import GeminiProvider
from cyberkb.providers.huggingface import HuggingFaceProvider
from cyberkb.providers.openrouter import OpenRouterProvider

if TYPE_CHECKING:
    from cyberkb.providers.base import HttpProviderBase

__all__ = ["PROVIDER_CLASSES", "is_registered", "provider_names"]

PROVIDER_CLASSES: dict[str, type[HttpProviderBase]] = {
    GeminiProvider.name: GeminiProvider,
    OpenRouterProvider.name: OpenRouterProvider,
    HuggingFaceProvider.name: HuggingFaceProvider,
}


def provider_names() -> tuple[str, ...]:
    """Registered provider names, in registration order."""
    return tuple(PROVIDER_CLASSES)


def is_registered(name: str) -> bool:
    """Whether ``name`` is a known provider."""
    return name in PROVIDER_CLASSES
