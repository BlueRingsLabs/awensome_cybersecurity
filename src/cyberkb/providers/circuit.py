"""A small per-provider circuit breaker.

When a provider keeps failing in a way no retry will fix (bad key, exhausted
quota, sustained 5xx), continuing to call it wastes the run's rate-limit budget
and slows every remaining document. The breaker trips after a threshold of
failures and then short-circuits that provider until a cool-down elapses, at
which point a single trial is allowed (half-open). One breaker is held per
provider by the orchestrator; the clock is injected so the behaviour is
deterministic under test.
"""

from __future__ import annotations

import time
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

__all__ = ["CircuitBreaker", "CircuitState"]

DEFAULT_FAILURE_THRESHOLD = 3
DEFAULT_RESET_TIMEOUT = 30.0


class CircuitState(StrEnum):
    """The three states of the breaker."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Trips open after repeated failures; allows a trial after a cool-down."""

    def __init__(
        self,
        *,
        failure_threshold: int = DEFAULT_FAILURE_THRESHOLD,
        reset_timeout: float = DEFAULT_RESET_TIMEOUT,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        """Configure the trip threshold, cool-down and (injected) clock."""
        self._threshold = max(1, failure_threshold)
        self._reset_timeout = reset_timeout
        self._clock = clock
        self._failures = 0
        self._opened_at: float | None = None

    @property
    def state(self) -> CircuitState:
        """The current state, deriving half-open from the elapsed cool-down."""
        if self._opened_at is None:
            return CircuitState.CLOSED
        if self._clock() - self._opened_at >= self._reset_timeout:
            return CircuitState.HALF_OPEN
        return CircuitState.OPEN

    def allow(self) -> bool:
        """Whether a call may be attempted now (blocked only while fully open)."""
        return self.state is not CircuitState.OPEN

    def record_success(self) -> None:
        """Reset the breaker: failures cleared, circuit closed."""
        self._failures = 0
        self._opened_at = None

    def record_failure(self) -> None:
        """Count a failure and open the circuit once the threshold is reached."""
        self._failures += 1
        if self._failures >= self._threshold:
            self._opened_at = self._clock()

    def trip(self) -> None:
        """Open the circuit immediately (for an unrecoverable provider fault)."""
        self._failures = self._threshold
        self._opened_at = self._clock()
