"""The orchestrator: one classification call across many providers and models.

It owns everything a single provider deliberately does not: the configured
provider order, per-model rotation, retry-with-backoff on transient failures, a
per-provider circuit breaker, structured logging of every attempt, and the
end-of-run report. A failure's :class:`FailureCategory` decides the route:

* transient (rate limit, timeout, 5xx, network) -> retry the same model with
  jittered backoff, honouring any ``Retry-After``; then rotate to the next model;
* model-level (unavailable, content filter, bad output, unknown) -> rotate to
  the next model immediately;
* provider-fatal (auth, quota exhausted) -> trip the breaker and skip the
  provider for the rest of the run.

When every provider and model is exhausted, :meth:`generate_json` returns
``None`` and the caller falls back to the deterministic heuristic; that count is
recorded in the report.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.obslog import AttemptLog, RunReport, StructuredLogger, utc_now_iso
from cyberkb.providers.circuit import (
    DEFAULT_FAILURE_THRESHOLD,
    DEFAULT_RESET_TIMEOUT,
    CircuitBreaker,
)
from cyberkb.providers.selection import (
    DEFAULT_MAX_CANDIDATES,
    DEFAULT_NEED,
    ValidationRequest,
    select_models,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from typing import Any

    from cyberkb.providers.base import HealthResult, LLMProvider, ProviderResult
    from cyberkb.providers.selection import ProviderSelection

__all__ = ["Orchestrator", "OrchestratorSettings"]

_TRANSIENT = frozenset(
    {
        FailureCategory.RATE_LIMIT,
        FailureCategory.TIMEOUT,
        FailureCategory.SERVER_ERROR,
        FailureCategory.NETWORK_ERROR,
    },
)
_PROVIDER_FATAL = frozenset({FailureCategory.AUTH_ERROR, FailureCategory.QUOTA_EXCEEDED})


def _default_sleep(seconds: float) -> None:  # pragma: no cover - thin wrapper over time.sleep
    """Real sleep; injected away in tests."""
    time.sleep(seconds)


@dataclass(frozen=True, slots=True)
class OrchestratorSettings:
    """Retry, backoff and circuit-breaker tuning for the orchestrator."""

    max_retries: int = 3
    backoff_base: float = 1.0
    backoff_cap: float = 30.0
    circuit_threshold: int = DEFAULT_FAILURE_THRESHOLD
    circuit_reset: float = DEFAULT_RESET_TIMEOUT

    def delay(self, attempt: int, jitter: float) -> float:
        """Full-jittered exponential backoff for a 1-based attempt."""
        ceiling = min(self.backoff_cap, self.backoff_base * 2 ** (attempt - 1))
        return float(round(ceiling * jitter, 3))


class Orchestrator:
    """Drive providers in order, rotating models and falling back on failure."""

    def __init__(
        self,
        providers: Sequence[LLMProvider],
        *,
        logger: StructuredLogger | None = None,
        sleep: Callable[[float], None] = _default_sleep,
        jitter: Callable[[], float] | None = None,
        clock: Callable[[], float] = time.monotonic,
        settings: OrchestratorSettings | None = None,
    ) -> None:
        """Bind providers and injected collaborators; one breaker per provider."""
        self._providers = list(providers)
        self._logger = logger if logger is not None else StructuredLogger()
        self._sleep = sleep
        self._jitter = jitter or (lambda: 1.0)
        self._clock = clock
        self._settings = settings or OrchestratorSettings()
        self._max_retries = max(1, self._settings.max_retries)
        self._breakers = {
            provider.name: CircuitBreaker(
                failure_threshold=self._settings.circuit_threshold,
                reset_timeout=self._settings.circuit_reset,
                clock=clock,
            )
            for provider in self._providers
        }
        self._selected: dict[str, tuple[str, ...]] = {}
        self._selections: list[ProviderSelection] = []
        self._heuristic_fallbacks = 0

    @property
    def logger(self) -> StructuredLogger:
        """The structured logger collecting every attempt."""
        return self._logger

    def preflight(
        self,
        *,
        system: str,
        samples: Sequence[str],
        schema: Mapping[str, object],
        validate: Callable[[Mapping[str, Any]], bool],
        need: int = DEFAULT_NEED,
        max_candidates: int = DEFAULT_MAX_CANDIDATES,
    ) -> list[ProviderSelection]:
        """Discover and validate each provider's models; record the accepted order."""
        request = ValidationRequest(
            system=system,
            samples=samples,
            schema=schema,
            validate=validate,
            need=need,
            max_candidates=max_candidates,
        )
        self._selections = []
        for provider in self._providers:
            selection = select_models(provider, request, logger=self._logger, clock=self._clock)
            self._selected[provider.name] = tuple(selection.accepted_models())
            self._selections.append(selection)
        return self._selections

    def health(self) -> list[HealthResult]:
        """Per-provider health derived from the pre-flight selection."""
        return [selection.as_health() for selection in self._selections]

    def has_capacity(self) -> bool:
        """Whether at least one provider has a validated model to use."""
        return any(self._selected.get(provider.name) for provider in self._providers)

    def generate_json(
        self,
        system: str,
        prompt: str,
        schema: Mapping[str, object],
        *,
        resource_ref: str | None = None,
    ) -> ProviderResult | None:
        """Classify one batch, rotating models and providers; ``None`` if all fail."""
        for provider in self._providers:
            breaker = self._breakers[provider.name]
            models = self._selected.get(provider.name, ())
            if not models or not breaker.allow():
                continue
            for model in models:
                result, error = self._try_model(
                    provider, model, system, prompt, schema, resource_ref
                )
                if result is not None:
                    breaker.record_success()
                    return result
                if error is not None and error.category in _PROVIDER_FATAL:
                    breaker.trip()
                    break
                breaker.record_failure()
        self._heuristic_fallbacks += 1
        return None

    def _try_model(
        self,
        provider: LLMProvider,
        model: str,
        system: str,
        prompt: str,
        schema: Mapping[str, object],
        resource_ref: str | None,
    ) -> tuple[ProviderResult | None, ProviderError | None]:
        attempt = 0
        while True:
            attempt += 1
            started = utc_now_iso()
            start = self._clock()
            try:
                result = provider.complete_json(model, system, prompt, schema)
            except ProviderError as exc:
                retry = exc.category in _TRANSIENT and attempt < self._max_retries
                self._logger.record(
                    AttemptLog(
                        provider=provider.name,
                        model=model,
                        resource_id=resource_ref,
                        attempt=attempt,
                        outcome="failure",
                        started_at=started,
                        ended_at=utc_now_iso(),
                        duration_s=self._clock() - start,
                        category=exc.category,
                        status=exc.status,
                        raw_error=exc.raw,
                        fell_back=not retry,
                    ),
                )
                if not retry:
                    return None, exc
                delay = (
                    exc.retry_after
                    if exc.retry_after is not None
                    else self._settings.delay(attempt, self._jitter())
                )
                self._sleep(delay)
                continue
            self._logger.record(
                AttemptLog(
                    provider=provider.name,
                    model=model,
                    resource_id=resource_ref,
                    attempt=attempt,
                    outcome="success",
                    started_at=started,
                    ended_at=utc_now_iso(),
                    duration_s=self._clock() - start,
                    category=None,
                    status=None,
                    raw_error="",
                    fell_back=False,
                ),
            )
            return result, None

    def run_report(self, *, now_iso: str | None = None) -> RunReport:
        """Build the end-of-run report from the collected attempts and selections."""
        return RunReport(
            generated_at=now_iso or self._logger.now_iso(),
            attempts=tuple(self._logger.attempts),
            heuristic_fallbacks=self._heuristic_fallbacks,
            provider_health=tuple(health.to_dict() for health in self.health()),
            model_selection=tuple(selection.to_dict() for selection in self._selections),
        )
