"""Tests for the adapter registry and its catalog cross-checks."""

from __future__ import annotations

import copy

import pytest

from cyberkb.errors import ModelCatalogError, ProviderConfigError
from cyberkb.providers.catalog import load_model_catalog, parse_model_catalog
from cyberkb.providers.google import GoogleProvider
from cyberkb.providers.groq import GroqProvider
from cyberkb.providers.registry import build_providers, missing_keys, provider_names
from tests.conftest import PROJECT_ROOT
from tests.llmfakes import CATALOG_DOC, GOOGLE_KEY, KEYS


def test_registry_knows_exactly_the_two_adapters() -> None:
    """Google AI Studio and Groq are the only providers."""
    assert provider_names() == ("google", "groq")


def test_shipped_catalog_matches_the_adapters() -> None:
    """The committed catalog builds cleanly against the verified endpoints."""
    providers = build_providers(load_model_catalog(PROJECT_ROOT), KEYS, timeout=10.0)
    assert [type(p) for p in providers] == [GoogleProvider, GroqProvider]
    assert all(p.is_configured() for p in providers)


def test_missing_keys_are_named() -> None:
    """Blank and absent keys are both reported, by variable name."""
    catalog = parse_model_catalog(CATALOG_DOC)
    assert missing_keys(catalog, {"GEMINI_API_KEY": " "}) == ["GEMINI_API_KEY", "GROQ_API_KEY"]
    assert missing_keys(catalog, KEYS) == []
    with pytest.raises(ProviderConfigError, match="GEMINI_API_KEY, GROQ_API_KEY"):
        build_providers(catalog, {}, timeout=10.0)


def test_a_redirected_endpoint_is_refused() -> None:
    """Editing base_url in the catalog cannot send a key to another host."""
    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"][1]["base_url"] = "https://evil.example/openai/v1"
    with pytest.raises(ModelCatalogError, match="refusing to send the key elsewhere"):
        build_providers(parse_model_catalog(doc), KEYS, timeout=10.0)


def test_an_unknown_provider_has_no_adapter() -> None:
    """A provider without an adapter is a catalog error, not a silent skip."""
    doc = copy.deepcopy(CATALOG_DOC)
    doc["providers"][0]["id"] = "mystery"
    with pytest.raises(ModelCatalogError, match="has no adapter"):
        build_providers(parse_model_catalog(doc), {"GEMINI_API_KEY": GOOGLE_KEY}, timeout=10.0)


def test_os_environ_is_the_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without an explicit mapping the process environment is read."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("GROQ_API_KEY", "g" * 20)
    catalog = parse_model_catalog(CATALOG_DOC)
    assert missing_keys(catalog) == ["GEMINI_API_KEY"]
    with pytest.raises(ProviderConfigError):
        build_providers(catalog, timeout=10.0)
