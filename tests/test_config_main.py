"""Tests for configuration parsing and the module entry point."""

from __future__ import annotations

import runpy

import pytest

from cyberkb.config import DEFAULT_MODELS, IngestConfig


def test_config_defaults() -> None:
    config = IngestConfig.from_env({})
    assert config.api_key is None
    assert config.models == DEFAULT_MODELS
    assert config.use_llm is False
    assert config.batch_size == 10


def test_config_with_key_and_models() -> None:
    config = IngestConfig.from_env(
        {"GEMINI_API_KEY": "k", "CYBERKB_MODELS": "a, b , c", "CYBERKB_BATCH_SIZE": "5"},
    )
    assert config.use_llm is True
    assert config.models == ("a", "b", "c")
    assert config.batch_size == 5


def test_config_invalid_int_falls_back() -> None:
    config = IngestConfig.from_env({"CYBERKB_BATCH_SIZE": "not-a-number"})
    assert config.batch_size == 10


def test_config_clamps_out_of_range() -> None:
    assert IngestConfig.from_env({"CYBERKB_BATCH_SIZE": "9999"}).batch_size == 50
    assert IngestConfig.from_env({"CYBERKB_MAX_RETRIES": "0"}).max_retries == 1


def test_config_blank_models_uses_default() -> None:
    assert IngestConfig.from_env({"CYBERKB_MODELS": "  ,  "}).models == DEFAULT_MODELS


def test_module_entry_point_runs(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["cyberkb", "--version"])
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("cyberkb", run_name="__main__")
    assert exc.value.code == 0
    assert "cyberkb" in capsys.readouterr().out
