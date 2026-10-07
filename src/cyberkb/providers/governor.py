"""Client-side pacing for one model: RPM/TPM windows, daily RPD/TPD, cooldowns.

Free tiers are enforced by the provider, but discovering a limit by hitting it
wastes a request, a retry delay and — on Google — part of a quota that is
counted per *attempt*. The governor keeps the engine just under each declared
limit so a 429 is the exception, not the control loop:

* RPM and TPM are tracked over a sliding 60-second window of the requests this
  run actually sent (token counts are settled to the provider's own usage
  figures when it reports them);
* RPD and TPD are counted per *quota day* in the provider's quota time zone
  (Google resets at midnight Pacific) and survive across runs through the
  enrich state ledger, so a second run on the same day does not re-spend an
  exhausted model;
* a cooldown (from ``Retry-After``/``RetryInfo``) blocks the model until it
  elapses, after which it rejoins rotation at its priority position.

``headroom`` scales the per-minute limits (default 0.9) to absorb clock skew
between this runner and the provider's window.
"""

from __future__ import annotations

import itertools
import math
from collections import deque
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from cyberkb.providers.catalog import ModelLimits

__all__ = ["DailyUsage", "ModelGovernor"]

WINDOW_SECONDS = 60.0
DEFAULT_HEADROOM = 0.9


@dataclass(slots=True)
class DailyUsage:
    """Requests and tokens spent on one model during one quota day."""

    day: str
    requests: int = 0
    tokens: int = 0
    exhausted: bool = False

    def to_dict(self) -> dict[str, object]:
        """Serialise for the state ledger."""
        return {
            "day": self.day,
            "requests": self.requests,
            "tokens": self.tokens,
            "exhausted": self.exhausted,
        }


class ModelGovernor:
    """Decide when one model may next be called, and account for each call."""

    def __init__(
        self,
        limits: ModelLimits,
        *,
        day: Callable[[], str],
        clock: Callable[[], float],
        usage: DailyUsage | None = None,
        headroom: float = DEFAULT_HEADROOM,
    ) -> None:
        """Bind the limits, the quota-day function, the clock and any prior usage."""
        self._limits = limits
        self._day = day
        self._clock = clock
        self._rpm = max(1, math.floor(limits.rpm * headroom))
        self._tpm = max(1, math.floor(limits.tpm * headroom))
        today = day()
        self._usage = usage if usage is not None and usage.day == today else DailyUsage(today)
        self._window: deque[list[float]] = deque()
        self._cooldown_until = 0.0

    @property
    def usage(self) -> DailyUsage:
        """Today's usage (rolled over first if the quota day has changed)."""
        self._roll()
        return self._usage

    @property
    def token_capacity(self) -> int:
        """The largest single request (in tokens) the paced TPM window admits."""
        return self._tpm

    def _roll(self) -> None:
        today = self._day()
        if self._usage.day != today:
            self._usage = DailyUsage(today)

    def _trim(self, now: float) -> None:
        while self._window and now - self._window[0][0] >= WINDOW_SECONDS:
            self._window.popleft()

    def exhausted(self) -> bool:
        """Whether the model's daily allowance is spent (or the provider said so)."""
        usage = self.usage
        tpd = self._limits.tpd
        return (
            usage.exhausted
            or usage.requests >= self._limits.rpd
            or (tpd is not None and usage.tokens >= tpd)
        )

    def mark_exhausted(self) -> None:
        """Record that the provider reported the daily quota as spent."""
        self.usage.exhausted = True

    def tighten(self, factor: float = 0.8) -> None:
        """Shrink the per-minute pacing after a rate limit (multiplicative decrease).

        The declared limits come from a dashboard; if the provider still
        throttles, its real window is tighter than declared (shared project
        RPM, different token accounting), so the model is paced more gently for
        the rest of the run instead of hitting the same wall again.
        """
        self._rpm = max(1, math.floor(self._rpm * factor))
        self._tpm = max(1, math.floor(self._tpm * factor))

    def cool(self, seconds: float) -> None:
        """Block the model for ``seconds`` from now (never shortening a cooldown)."""
        self._cooldown_until = max(self._cooldown_until, self._clock() + max(0.0, seconds))

    def wait_for(self, tokens: int) -> float:
        """Seconds until a request of ``tokens`` fits every limit (``inf`` if never today).

        A request larger than the whole paced TPM window can never fit and is
        reported as ``inf`` so the caller shrinks it or uses another model.
        """
        if self.exhausted() or tokens > self._tpm:
            return math.inf
        now = self._clock()
        self._trim(now)
        waits = [max(0.0, self._cooldown_until - now)]
        if len(self._window) >= self._rpm:
            waits.append(self._window[len(self._window) - self._rpm][0] + WINDOW_SECONDS - now)
        need = sum(int(entry[1]) for entry in self._window) + tokens - self._tpm
        if need > 0:
            # Requests leave the window oldest first; wait for the one whose
            # departure frees enough. ``tokens <= tpm`` guarantees one exists.
            freed = itertools.accumulate(int(entry[1]) for entry in self._window)
            index = next(i for i, total in enumerate(freed) if total >= need)
            waits.append(self._window[index][0] + WINDOW_SECONDS - now)
        return max(0.0, *waits)

    def reserve(self, tokens: int) -> list[float]:
        """Account for a request of ``tokens`` sent now; returns its window entry."""
        entry = [self._clock(), float(tokens)]
        self._window.append(entry)
        usage = self.usage
        usage.requests += 1
        usage.tokens += tokens
        return entry

    def settle(self, entry: list[float], actual_tokens: int | None) -> None:
        """Replace a reservation's estimate with the provider-reported token count."""
        if actual_tokens is None:
            return
        delta = actual_tokens - int(entry[1])
        entry[1] = float(actual_tokens)
        usage = self.usage
        usage.tokens = max(0, usage.tokens + delta)
