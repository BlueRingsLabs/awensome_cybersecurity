"""Tests for configuration parsing and the module entry point."""

from __future__ import annotations

import runpy

import pytest

from cyberkb.config import ConfigError, IngestConfig


def test_config_defaults() -> None:
    """With an empty environment every knob takes its documented default."""
    config = IngestConfig.from_env({})
    assert config.batch_size == 10
    assert config.timeout == 60.0
    assert config.rotation.model_retries == 3
    assert config.rotation.list_passes == 2
    assert config.rotation.list_backoff == 60.0


def test_config_reads_every_variable() -> None:
    """Each variable overrides its knob; blank values mean the default."""
    config = IngestConfig.from_env(
        {
            "CYBERKB_BATCH_SIZE": "5",
            "CYBERKB_TIMEOUT": " 90 ",
            "CYBERKB_MODEL_RETRIES": "0",
            "CYBERKB_LIST_PASSES": "3",
            "CYBERKB_LIST_BACKOFF": "",
        },
    )
    assert config.batch_size == 5
    assert config.timeout == 90.0
    assert config.rotation.model_retries == 0
    assert config.rotation.list_passes == 3
    assert config.rotation.list_backoff == 60.0


@pytest.mark.parametrize(
    ("key", "value", "message"),
    [
        ("CYBERKB_BATCH_SIZE", "not-a-number", "is not an integer"),
        ("CYBERKB_BATCH_SIZE", "9999", "outside the allowed range 1..50"),
        ("CYBERKB_LIST_PASSES", "0", "outside the allowed range 1..5"),
        ("CYBERKB_MODEL_RETRIES", "-1", "outside the allowed range 0..10"),
    ],
)
def test_bad_values_fail_loudly(key: str, value: str, message: str) -> None:
    """A malformed or out-of-range value stops the run instead of being clamped."""
    with pytest.raises(ConfigError, match=message):
        IngestConfig.from_env({key: value})


def test_module_entry_point_runs(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`python -m cyberkb --version` runs the CLI and exits cleanly."""
    monkeypatch.setattr("sys.argv", ["cyberkb", "--version"])
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("cyberkb", run_name="__main__")
    assert exc.value.code == 0
    assert "cyberkb" in capsys.readouterr().out
