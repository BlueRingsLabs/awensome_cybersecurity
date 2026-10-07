"""Tests for the reviewed model catalog and live-id resolution."""

from __future__ import annotations

import copy
from datetime import date
from typing import TYPE_CHECKING, Any

import pytest

from cyberkb.errors import ModelCatalogError
from cyberkb.providers.catalog import (
    CATALOG_RELPATH,
    ListedModel,
    load_model_catalog,
    normalise_name,
    parse_model_catalog,
    resolve_models,
)
from tests.conftest import PROJECT_ROOT

if TYPE_CHECKING:
    from pathlib import Path


def _doc() -> dict[str, Any]:
    return {
        "version": 1,
        "verified_on": date(2026, 10, 7),
        "source": "dashboards",
        "providers": [
            {
                "id": "google",
                "name": "Google AI Studio",
                "base_url": "https://generativelanguage.googleapis.com/v1beta/",
                "api_key_env": "GEMINI_API_KEY",
                "docs": "https://ai.google.dev",
                "match": "display_name",
                "quota_timezone": "America/Los_Angeles",
                "tpm_counts_completion": False,
                "models": [
                    {
                        "name": "Gemma 4 31B",
                        "id_hints": ["gemma-4-31b-it"],
                        "limits": {"rpm": 30, "rpd": 14400, "tpm": 16000},
                    },
                    {"name": "Gemini 3.5 Flash", "limits": {"rpm": 5, "rpd": 20, "tpm": 250000}},
                ],
            },
            {
                "id": "groq",
                "name": "Groq",
                "base_url": "https://api.groq.com/openai/v1",
                "api_key_env": "GROQ_API_KEY",
                "docs": "https://console.groq.com/docs",
                "match": "id",
                "quota_timezone": "UTC",
                "tpm_counts_completion": True,
                "exclude": ["openai/gpt-oss-safeguard-20b"],
                "models": [
                    {
                        "name": "allam-2-7b",
                        "limits": {"rpm": 30, "rpd": 7000, "tpm": 6000, "tpd": 500000},
                    },
                ],
            },
        ],
    }


def test_shipped_catalog_loads_with_the_verified_priority_order() -> None:
    """The committed catalog is valid and keeps the maintainer's priority order."""
    catalog = load_model_catalog(PROJECT_ROOT)
    assert [p.id for p in catalog.providers] == ["google", "groq"]
    google, groq = catalog.providers
    assert google.models[0].name == "Gemma 4 31B"
    assert google.models[0].id_hints == ("gemma-4-31b-it",)
    assert google.models[0].priority == 1
    assert groq.models[0].priority == len(google.models) + 1
    assert [m.name for m in groq.models] == [
        "allam-2-7b",
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "qwen/qwen3.8-27b",
    ]
    assert "meta-llama/llama-prompt-guard-2-22m" in groq.exclude
    assert google.base_url == "https://generativelanguage.googleapis.com/v1beta"
    assert catalog.provider("groq") is groq


def test_parse_strips_trailing_slash_and_records_limits() -> None:
    """Base URLs are normalised and optional limits default to None."""
    catalog = parse_model_catalog(_doc())
    google = catalog.provider("google")
    assert google.base_url.endswith("/v1beta")
    assert google.models[1].limits.tpd is None
    assert catalog.provider("groq").models[0].limits.to_dict() == {
        "rpm": 30,
        "rpd": 7000,
        "tpm": 6000,
        "tpd": 500000,
    }
    assert catalog.verified_on == date(2026, 10, 7)


def test_unknown_provider_lookup_is_an_error() -> None:
    """Asking for an undeclared provider fails loudly."""
    with pytest.raises(ModelCatalogError, match="not declared"):
        parse_model_catalog(_doc()).provider("mistral")


def _mutate(path: list[Any], value: object) -> dict[str, Any]:
    doc = copy.deepcopy(_doc())
    target: Any = doc
    for key in path[:-1]:
        target = target[key]
    if value is _DELETE:
        del target[path[-1]]
    else:
        target[path[-1]] = value
    return doc


_DELETE = object()


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (["version"], 2, "version must be 1"),
        (["verified_on"], "yesterday", "verified_on"),
        (["providers"], [], "providers must be a non-empty list"),
        (["extra"], 1, "unknown key"),
        (["providers", 0], "nope", "must be a mapping"),
        (["providers", 0, "match"], "fuzzy", "match must be one of"),
        (["providers", 0, "tpm_counts_completion"], "no", "must be a boolean"),
        (["providers", 0, "quota_timezone"], "Mars/Olympus", "not a known IANA zone"),
        (["providers", 0, "models"], [], "models must be a non-empty list"),
        (["providers", 0, "exclude"], "x", "must be a list"),
        (["providers", 0, "name"], "  ", "must be a non-empty string"),
        (["providers", 0, "models", 0, "limits", "rpm"], 0, "positive integer"),
        (["providers", 0, "models", 0, "limits", "rpd"], True, "positive integer"),
        (["providers", 0, "models", 0, "limits", "tpd"], -1, "positive integer"),
        (["providers", 0, "models", 0, "limits", "tpm"], _DELETE, "missing tpm"),
        (["providers", 0, "models", 1, "name"], "Gemma 4 31B", "declared twice"),
        (["providers", 1, "id"], "google", "declared twice"),
        (["providers", 1, "models", 0, "name"], "openai/gpt-oss-safeguard-20b", "excluded"),
    ],
)
def test_invalid_catalogs_are_rejected(path: list[Any], value: object, message: str) -> None:
    """Every structural or semantic defect is a ModelCatalogError, never a guess."""
    with pytest.raises(ModelCatalogError, match=message):
        parse_model_catalog(_mutate(path, value))


def test_load_reports_unreadable_or_invalid_yaml(tmp_path: Path) -> None:
    """A missing file and broken YAML are both catalog errors."""
    with pytest.raises(ModelCatalogError, match="cannot load"):
        load_model_catalog(tmp_path)
    target = tmp_path / CATALOG_RELPATH
    target.parent.mkdir(parents=True)
    target.write_text("providers: [unclosed\n", encoding="utf-8")
    with pytest.raises(ModelCatalogError, match="cannot load"):
        load_model_catalog(tmp_path)


def test_normalise_name_folds_display_names_onto_ids() -> None:
    """Display names and ids compare equal once punctuation and case are dropped."""
    assert normalise_name("Gemini 3.5 Flash") == normalise_name("gemini-3.5-flash")
    assert normalise_name("Gemma 4 31B") != normalise_name("gemma-4-31b-it")


def test_resolution_rules_for_display_name_providers() -> None:
    """Hints win, then display name (most stable first), then the normalised id."""
    google = parse_model_catalog(_doc()).provider("google")
    listed = [
        ListedModel("gemma-4-31b-it", "Gemma 4 31B IT", 262144, 8192),
        ListedModel("gemini-3.5-flash-preview-09", "Gemini 3.5 Flash"),
        ListedModel("gemini-3.5-flash", "Gemini 3.5 Flash"),
    ]
    first, second = resolve_models(google, listed)
    assert first.model is not None
    assert first.model.id == "gemma-4-31b-it"
    assert first.rule == "documented id hint"
    assert second.model is not None
    assert second.model.id == "gemini-3.5-flash"
    assert second.rule == "display name"
    assert second.alternatives == ("gemini-3.5-flash-preview-09",)
    assert second.to_dict()["api_id"] == "gemini-3.5-flash"


def test_resolution_falls_back_to_normalised_id_and_reports_missing() -> None:
    """Without a display name the id is matched; an absent model is reported."""
    google = parse_model_catalog(_doc()).provider("google")
    first, second = resolve_models(google, [ListedModel("gemini-3.5-flash")])
    assert first.model is None
    assert first.rule == "not listed by the provider"
    assert first.to_dict()["api_id"] is None
    assert second.model is not None
    assert second.rule == "normalised id"


def test_resolution_never_maps_two_declarations_to_one_id() -> None:
    """A second name that lands on an already-taken id is reported, not reused."""
    doc = _doc()
    doc["providers"][0]["models"][1]["id_hints"] = ["gemma-4-31b-it"]
    google = parse_model_catalog(doc).provider("google")
    first, second = resolve_models(google, [ListedModel("gemma-4-31b-it")])
    assert first.model is not None
    assert second.model is None
    assert "duplicate" in second.rule


def test_id_providers_need_an_exact_id_and_ignore_excluded_models() -> None:
    """Groq ids must match verbatim, and excluded classifiers are never candidates."""
    groq = parse_model_catalog(_doc()).provider("groq")
    (hit,) = resolve_models(groq, [ListedModel("allam-2-7b"), ListedModel("Allam-2-7B")])
    assert hit.model is not None
    assert hit.rule == "exact id"
    (miss,) = resolve_models(groq, [ListedModel("allam-2-7b-v2")])
    assert miss.model is None
