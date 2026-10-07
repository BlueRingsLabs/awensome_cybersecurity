"""The registry of provider adapters — the one place a provider class is listed.

The catalog (``schema/llm-models.yaml``) decides which providers and models are
*used*; this registry decides which adapters *exist*. Building a provider
cross-checks the two: the catalog's ``base_url`` must equal the endpoint the
adapter was written and verified against, so editing the catalog can never send
an API key to another host.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from cyberkb.errors import ModelCatalogError, ProviderConfigError
from cyberkb.providers.google import GoogleProvider
from cyberkb.providers.groq import GroqProvider

if TYPE_CHECKING:
    from collections.abc import Mapping

    from cyberkb.providers.base import HttpProviderBase
    from cyberkb.providers.catalog import ModelCatalog, ProviderSpec
    from cyberkb.providers.http import Transport

__all__ = ["PROVIDER_CLASSES", "build_providers", "missing_keys", "provider_names"]

PROVIDER_CLASSES: dict[str, type[HttpProviderBase]] = {
    GoogleProvider.name: GoogleProvider,
    GroqProvider.name: GroqProvider,
}


def provider_names() -> tuple[str, ...]:
    """Registered provider names, in registration order."""
    return tuple(PROVIDER_CLASSES)


def _adapter(spec: ProviderSpec) -> type[HttpProviderBase]:
    cls = PROVIDER_CLASSES.get(spec.id)
    if cls is None:
        msg = f"catalog provider {spec.id!r} has no adapter (known: {', '.join(PROVIDER_CLASSES)})"
        raise ModelCatalogError(msg)
    if spec.base_url != cls.base_url:
        msg = (
            f"catalog base_url for {spec.id!r} is {spec.base_url!r}, but the adapter is "
            f"verified against {cls.base_url!r}; refusing to send the key elsewhere"
        )
        raise ModelCatalogError(msg)
    return cls


def missing_keys(catalog: ModelCatalog, env: Mapping[str, str] | None = None) -> list[str]:
    """Names of the catalog's API-key variables that are unset or blank."""
    env = os.environ if env is None else env
    return [s.api_key_env for s in catalog.providers if not (env.get(s.api_key_env) or "").strip()]


def build_providers(
    catalog: ModelCatalog,
    env: Mapping[str, str] | None = None,
    *,
    timeout: float,
    transport: Transport | None = None,
) -> list[HttpProviderBase]:
    """Instantiate one adapter per catalog provider, in catalog (fallback) order.

    Every declared provider is required: a missing key is a configuration error
    that stops the run before any request is made, never a silent skip.

    Raises:
        ModelCatalogError: a provider has no adapter or a mismatched endpoint.
        ProviderConfigError: one or more API keys are missing.
    """
    env = os.environ if env is None else env
    adapters = [(_adapter(spec), spec) for spec in catalog.providers]
    missing = missing_keys(catalog, env)
    if missing:
        msg = f"missing API key(s): {', '.join(missing)} (set them as secrets; values are never logged)"
        raise ProviderConfigError(msg)
    return [
        cls(env[spec.api_key_env].strip(), timeout=timeout, transport=transport)
        for cls, spec in adapters
    ]
