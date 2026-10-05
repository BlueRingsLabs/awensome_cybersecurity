"""Tests for the per-provider circuit breaker."""

from __future__ import annotations

from cyberkb.providers.circuit import CircuitBreaker


def _breaker(now: list[float], **kw: object) -> CircuitBreaker:
    return CircuitBreaker(clock=lambda: now[0], **kw)  # type: ignore[arg-type]


def _state(breaker: CircuitBreaker) -> str:
    # Return the state as a plain string so sequential assertions over time do
    # not trip mypy's literal narrowing of the enum property.
    return breaker.state.value


def test_starts_closed_and_allows() -> None:
    """A fresh breaker is closed and permits calls."""
    breaker = _breaker([0.0])
    assert _state(breaker) == "closed"
    assert breaker.allow() is True


def test_opens_after_threshold_failures() -> None:
    """Reaching the failure threshold opens the circuit and blocks calls."""
    now = [0.0]
    breaker = _breaker(now, failure_threshold=2, reset_timeout=10.0)
    breaker.record_failure()
    assert breaker.allow() is True  # one failure, still closed
    breaker.record_failure()
    assert _state(breaker) == "open"
    assert breaker.allow() is False


def test_half_opens_after_cooldown_then_closes_on_success() -> None:
    """After the cool-down the breaker half-opens, and a success closes it."""
    now = [0.0]
    breaker = _breaker(now, failure_threshold=1, reset_timeout=10.0)
    breaker.record_failure()
    assert _state(breaker) == "open"
    now[0] = 10.0
    assert _state(breaker) == "half_open"
    assert breaker.allow() is True
    breaker.record_success()
    assert _state(breaker) == "closed"


def test_half_open_trial_failure_reopens() -> None:
    """A failure during the half-open trial re-opens the circuit."""
    now = [0.0]
    breaker = _breaker(now, failure_threshold=1, reset_timeout=10.0)
    breaker.record_failure()
    now[0] = 10.0
    assert _state(breaker) == "half_open"
    breaker.record_failure()
    assert _state(breaker) == "open"  # opened_at reset to now


def test_trip_opens_immediately() -> None:
    """trip() opens the circuit without waiting for the threshold."""
    breaker = _breaker([0.0], failure_threshold=5, reset_timeout=10.0)
    breaker.trip()
    assert _state(breaker) == "open"
    assert breaker.allow() is False


def test_success_resets_failure_count() -> None:
    """A success clears accumulated failures so the breaker stays closed."""
    breaker = _breaker([0.0], failure_threshold=2, reset_timeout=10.0)
    breaker.record_failure()
    breaker.record_success()
    breaker.record_failure()
    assert _state(breaker) == "closed"  # not two consecutive failures
