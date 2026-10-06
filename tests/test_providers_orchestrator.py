"""Tests for the multi-provider orchestrator: routing, retry, rotation, fallback."""

from __future__ import annotations

import io
import json
from typing import TYPE_CHECKING

from cyberkb.obslog import StructuredLogger
from cyberkb.providers.huggingface import HuggingFaceProvider
from cyberkb.providers.openrouter import OpenRouterProvider
from cyberkb.providers.orchestrator import Orchestrator, OrchestratorSettings
from tests.conftest import FakeTransport, http_json, http_text

if TYPE_CHECKING:
    from collections.abc import Callable

    from cyberkb.providers.base import LLMProvider
    from cyberkb.providers.http import HttpResponse, HttpTransportError

    _Item = HttpResponse | HttpTransportError


def _clock() -> Callable[[], float]:
    state = {"v": 0.0}

    def tick() -> float:
        state["v"] += 1.0
        return state["v"]

    return tick


def _chat(content: str) -> dict[str, object]:
    return {"choices": [{"finish_reason": "stop", "message": {"content": content}}]}


_ANSWER = _chat(json.dumps({"classifications": []}))


def _provider(cls: type[LLMProvider], *items: _Item) -> LLMProvider:
    return cls("key", transport=FakeTransport(*items), clock=_clock())  # type: ignore[call-arg]


def _orch(
    providers: list[LLMProvider],
    *,
    max_retries: int = 2,
    sleeps: list[float] | None = None,
) -> Orchestrator:
    settings = OrchestratorSettings(
        max_retries=max_retries, circuit_threshold=10, circuit_reset=100.0
    )
    return Orchestrator(
        providers,
        logger=StructuredLogger(io.StringIO()),
        sleep=(sleeps.append if sleeps is not None else (lambda _s: None)),
        jitter=lambda: 1.0,
        clock=_clock(),
        settings=settings,
    )


def _seed(orch: Orchestrator, mapping: dict[str, tuple[str, ...]]) -> None:
    orch._selected = mapping  # noqa: SLF001 - seed validated models without a full preflight


def test_settings_delay_is_capped_jittered_backoff() -> None:
    """Backoff grows exponentially, scales by jitter and is capped."""
    settings = OrchestratorSettings(backoff_base=1.0, backoff_cap=30.0)
    assert settings.delay(1, 1.0) == 1.0
    assert settings.delay(3, 0.5) == 2.0
    assert settings.delay(10, 1.0) == 30.0


def test_default_logger_is_created_when_omitted() -> None:
    """Omitting the logger still gives the orchestrator a working one."""
    orch = Orchestrator([])
    assert isinstance(orch.logger, StructuredLogger)
    assert orch.generate_json("s", "p", {}) is None


def test_success_on_first_model() -> None:
    """A clean call returns the parsed payload and logs one success."""
    provider = _provider(OpenRouterProvider, http_json(200, _ANSWER))
    orch = _orch([provider])
    _seed(orch, {"openrouter": ("model-a",)})
    result = orch.generate_json("s", "p", {}, resource_ref="ckb-1")
    assert result is not None
    assert result.model == "model-a"
    assert [a.outcome for a in orch.logger.attempts] == ["success"]


def test_transient_failure_is_retried_then_succeeds() -> None:
    """A 503 is retried with backoff on the same model, then succeeds."""
    provider = _provider(OpenRouterProvider, http_text(503, "busy"), http_json(200, _ANSWER))
    sleeps: list[float] = []
    orch = _orch([provider], max_retries=2, sleeps=sleeps)
    _seed(orch, {"openrouter": ("model-a",)})
    result = orch.generate_json("s", "p", {})
    assert result is not None
    assert sleeps == [1.0]  # one backoff between the two attempts
    assert [a.outcome for a in orch.logger.attempts] == ["failure", "success"]


def test_exhausted_transient_rotates_to_next_model() -> None:
    """When retries are spent on one model, the next model is tried."""
    provider = _provider(OpenRouterProvider, http_text(503, "busy"), http_json(200, _ANSWER))
    orch = _orch([provider], max_retries=1)
    _seed(orch, {"openrouter": ("model-a", "model-b")})
    result = orch.generate_json("s", "p", {})
    assert result is not None
    assert result.model == "model-b"


def test_model_unavailable_rotates_without_retry() -> None:
    """A 404 rotates straight to the next model with no backoff."""
    provider = _provider(
        OpenRouterProvider, http_text(404, "no such model"), http_json(200, _ANSWER)
    )
    sleeps: list[float] = []
    orch = _orch([provider], max_retries=3, sleeps=sleeps)
    _seed(orch, {"openrouter": ("model-a", "model-b")})
    result = orch.generate_json("s", "p", {})
    assert result is not None
    assert result.model == "model-b"
    assert sleeps == []


def test_provider_fatal_trips_breaker_and_falls_to_next_provider() -> None:
    """An auth failure skips the whole provider and the next one serves the call."""
    first = _provider(OpenRouterProvider, http_text(401, "invalid key"))
    second = _provider(HuggingFaceProvider, http_json(200, _ANSWER))
    orch = _orch([first, second])
    _seed(orch, {"openrouter": ("model-a",), "huggingface": ("model-b",)})
    result = orch.generate_json("s", "p", {})
    assert result is not None
    assert result.provider == "huggingface"
    assert orch._breakers["openrouter"].allow() is False  # noqa: SLF001 - breaker tripped


def test_tripped_breaker_persists_across_calls() -> None:
    """Once a provider's breaker trips, later calls skip it without touching it."""
    first = _provider(OpenRouterProvider, http_text(401, "invalid key"))
    second = _provider(HuggingFaceProvider, http_json(200, _ANSWER), http_json(200, _ANSWER))
    orch = _orch([first, second])
    _seed(orch, {"openrouter": ("model-a",), "huggingface": ("model-b",)})
    # First call trips openrouter (auth) and huggingface serves it.
    assert orch.generate_json("s", "p", {}, resource_ref="r1").provider == "huggingface"  # type: ignore[union-attr]
    # Second call must skip openrouter entirely: its transport has no second
    # response queued, so a call to it would raise IndexError. huggingface serves.
    assert orch.generate_json("s", "p", {}, resource_ref="r2").provider == "huggingface"  # type: ignore[union-attr]


def test_all_failures_return_none_and_count_heuristic_fallback() -> None:
    """When every provider/model fails, the call returns None and is counted."""
    provider = _provider(OpenRouterProvider, http_text(500, "boom"))
    orch = _orch([provider], max_retries=1)
    _seed(orch, {"openrouter": ("model-a",)})
    assert orch.generate_json("s", "p", {}) is None
    assert orch.run_report().to_dict()["totals"]["heuristic_fallbacks"] == 1


def test_open_circuit_skips_provider() -> None:
    """A provider whose breaker is open is skipped entirely."""
    provider = _provider(OpenRouterProvider, http_json(200, _ANSWER))
    orch = _orch([provider])
    _seed(orch, {"openrouter": ("model-a",)})
    orch._breakers["openrouter"].trip()  # noqa: SLF001 - force the breaker open
    assert orch.generate_json("s", "p", {}) is None


def test_provider_without_selected_models_is_skipped() -> None:
    """A provider with no validated models contributes nothing."""
    provider = _provider(OpenRouterProvider, http_json(200, _ANSWER))
    orch = _orch([provider])
    _seed(orch, {})
    assert orch.generate_json("s", "p", {}) is None


def test_preflight_selects_models_and_reports_health() -> None:
    """Pre-flight discovers, validates and records the usable models and health."""
    listing = {"data": [{"id": "qwen/qwen-2.5-7b-instruct:free"}]}
    provider = _provider(OpenRouterProvider, http_json(200, listing), http_json(200, _ANSWER))
    orch = _orch([provider])
    selections = orch.preflight(
        system="s",
        samples=["p"],
        schema={"type": "object"},
        validate=lambda payload: "classifications" in payload,
        need=1,
        max_candidates=1,
    )
    assert selections[0].accepted_models() == ["qwen/qwen-2.5-7b-instruct:free"]
    assert orch.has_capacity() is True
    assert orch.health()[0].ok is True


def test_run_report_includes_attempts_health_and_selection() -> None:
    """The run report carries attempts, per-provider health and selection."""
    listing = {"data": [{"id": "qwen/qwen-2.5-7b-instruct:free"}]}
    provider = _provider(OpenRouterProvider, http_json(200, listing), http_json(200, _ANSWER))
    orch = _orch([provider])
    orch.preflight(
        system="s",
        samples=["p"],
        schema={},
        validate=lambda payload: "classifications" in payload,
        need=1,
        max_candidates=1,
    )
    report = orch.run_report(now_iso="2026-10-05T14:23:11Z").to_dict()
    assert report["generated_at"] == "2026-10-05T14:23:11Z"
    assert report["model_selection"][0]["provider"] == "openrouter"
    assert report["provider_health"][0]["ok"] is True
    assert report["totals"]["calls"] >= 1
