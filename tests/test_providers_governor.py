"""Tests for client-side pacing: RPM/TPM windows, daily quotas, cooldowns."""

from __future__ import annotations

import math

from cyberkb.providers.catalog import ModelLimits
from cyberkb.providers.governor import DailyUsage, ModelGovernor
from tests.llmfakes import FakeTime


def _governor(
    limits: ModelLimits,
    *,
    time: FakeTime | None = None,
    day: list[str] | None = None,
    usage: DailyUsage | None = None,
) -> tuple[ModelGovernor, FakeTime, list[str]]:
    clock = time or FakeTime()
    today = day or ["2026-10-07"]
    governor = ModelGovernor(
        limits, day=lambda: today[0], clock=clock.clock, usage=usage, headroom=1.0
    )
    return governor, clock, today


def test_rpm_window_admits_until_full_then_waits_for_the_oldest() -> None:
    """The (rpm+1)-th request waits until the oldest leaves the 60 s window."""
    governor, time, _ = _governor(ModelLimits(rpm=2, rpd=100, tpm=10_000))
    assert governor.wait_for(10) == 0.0
    governor.reserve(10)
    time.t = 5.0
    governor.reserve(10)
    time.t = 10.0
    assert governor.wait_for(10) == 50.0
    time.t = 60.0
    assert governor.wait_for(10) == 0.0


def test_tpm_window_waits_until_enough_tokens_free_up() -> None:
    """A request that would overflow the token window waits for older spend to expire."""
    governor, time, _ = _governor(ModelLimits(rpm=100, rpd=100, tpm=1000))
    governor.reserve(600)
    time.t = 20.0
    governor.reserve(300)
    time.t = 30.0
    assert governor.wait_for(200) == 30.0
    assert governor.wait_for(100) == 0.0


def test_oversized_request_can_never_fit() -> None:
    """A single request larger than the TPM window is reported as never."""
    governor, _, _ = _governor(ModelLimits(rpm=10, rpd=10, tpm=100))
    assert math.isinf(governor.wait_for(101))
    assert governor.token_capacity == 100


def test_headroom_scales_per_minute_limits() -> None:
    """The default 10% headroom keeps pacing below the declared limits."""
    time = FakeTime()
    governor = ModelGovernor(
        ModelLimits(rpm=10, rpd=10, tpm=1000), day=lambda: "d", clock=time.clock
    )
    assert governor.token_capacity == 900


def test_daily_requests_and_tokens_exhaust_the_model() -> None:
    """RPD and TPD are enforced from the reservations."""
    governor, _, _ = _governor(ModelLimits(rpm=100, rpd=2, tpm=10_000))
    governor.reserve(10)
    governor.reserve(10)
    assert governor.exhausted()
    assert math.isinf(governor.wait_for(1))
    tokens, _, _ = _governor(ModelLimits(rpm=100, rpd=100, tpm=10_000, tpd=15))
    tokens.reserve(10)
    assert not tokens.exhausted()
    tokens.reserve(10)
    assert tokens.exhausted()


def test_usage_rolls_over_with_the_quota_day() -> None:
    """A new quota day resets the daily counters (and a provider-reported exhaustion)."""
    governor, _, day = _governor(ModelLimits(rpm=100, rpd=1, tpm=10_000))
    governor.reserve(5)
    governor.mark_exhausted()
    assert governor.exhausted()
    day[0] = "2026-10-08"
    assert not governor.exhausted()
    assert governor.usage == DailyUsage("2026-10-08")


def test_prior_usage_is_kept_only_for_the_same_day() -> None:
    """Usage carried from an earlier run counts today; yesterday's is discarded."""
    today, _, _ = _governor(
        ModelLimits(rpm=10, rpd=3, tpm=100), usage=DailyUsage("2026-10-07", requests=3)
    )
    assert today.exhausted()
    stale, _, _ = _governor(
        ModelLimits(rpm=10, rpd=3, tpm=100), usage=DailyUsage("2026-10-06", requests=3)
    )
    assert not stale.exhausted()


def test_settle_replaces_the_estimate_with_actual_usage() -> None:
    """Provider-reported tokens correct both the window and the daily count."""
    governor, _, _ = _governor(ModelLimits(rpm=10, rpd=10, tpm=1000))
    entry = governor.reserve(500)
    governor.settle(entry, 200)
    assert governor.usage.tokens == 200
    assert governor.wait_for(800) == 0.0
    governor.settle(entry, None)
    assert governor.usage.tokens == 200


def test_cooldown_blocks_until_it_elapses_and_never_shrinks() -> None:
    """A cooldown delays the model; a shorter later cooldown does not shorten it."""
    governor, time, _ = _governor(ModelLimits(rpm=10, rpd=10, tpm=1000))
    governor.cool(30)
    governor.cool(5)
    assert governor.wait_for(1) == 30.0
    time.t = 30.0
    assert governor.wait_for(1) == 0.0


def test_tighten_reduces_per_minute_pacing() -> None:
    """After a rate limit the model is paced more gently, never below one."""
    governor, _, _ = _governor(ModelLimits(rpm=1, rpd=10, tpm=1000))
    governor.tighten()
    assert governor.token_capacity == 800
    governor.reserve(1)
    assert governor.wait_for(1) > 0


def test_daily_usage_serialises() -> None:
    """DailyUsage round-trips to the ledger shape."""
    assert DailyUsage("d", 1, 2, exhausted=True).to_dict() == {
        "day": "d",
        "requests": 1,
        "tokens": 2,
        "exhausted": True,
    }


def test_tpm_wait_skips_entries_that_free_too_little() -> None:
    """The wait is until enough *cumulative* spend leaves, not just the oldest entry."""
    governor, time, _ = _governor(ModelLimits(rpm=100, rpd=100, tpm=1000))
    governor.reserve(100)
    time.t = 10.0
    governor.reserve(600)
    time.t = 20.0
    assert governor.wait_for(900) == 50.0
