"""The rotation engine: per-model, per-provider routing under free-tier limits.

One :class:`RotationEngine` serves every LLM call of a run. Its model list is the
reviewed catalog (``schema/llm-models.yaml``) in priority order — every Google
model, then every Groq model — resolved to live API ids at start-up
(:meth:`RotationEngine.discover`). For each request it uses the
highest-priority model that is usable *and* ready now, so work always flows to
the preferred model whenever that model has capacity:

* a model is validated lazily, on first use, with a real classification probe;
  a structured-output mode the API rejects steps down the provider's mode
  ladder (logged); any other validation failure skips the model for the run;
* an *error* — timeout, 5xx, network, or an answer that fails the caller's
  checks — is retried on the same model up to ``model_retries`` times with
  full-jittered exponential backoff, then the request moves to the next model;
* a short-window ``rate_limit`` is *not* an error: the model cools down
  (``Retry-After``/``RetryInfo``) and the request moves on at once; the model
  rejoins at its priority position once cooled. Repeated rate limits with no
  success in between are treated as exhaustion;
* ``quota_exceeded`` retires the model for the quota day;
* ``auth_error`` takes the whole provider out; a network failure that outlives
  the retries takes it out until the next list pass;
* when no usable model is left, the list is walked again (``list_passes``)
  after reviving models that failed only transiently; when that is spent the
  engine reports itself *exhausted*.

Every attempt is recorded through :class:`~cyberkb.obslog.StructuredLogger`;
per-model and per-provider statistics and the retry counters feed the run
report.
"""

from __future__ import annotations

import functools
import json
import math
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Literal
from zoneinfo import ZoneInfo

from cyberkb.errors import FailureCategory, ProviderConfigError, ProviderError
from cyberkb.obslog import AttemptLog, StructuredLogger, utc_now_iso
from cyberkb.providers.catalog import resolve_models
from cyberkb.providers.governor import ModelGovernor

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence

    from cyberkb.providers.base import LLMProvider, ProviderResult
    from cyberkb.providers.catalog import (
        DeclaredModel,
        ListedModel,
        ModelCatalog,
        ProviderSpec,
        Resolution,
    )
    from cyberkb.providers.governor import DailyUsage

__all__ = [
    "CHARS_PER_TOKEN",
    "VALIDATION_REF",
    "CachedValidation",
    "GenerationOutcome",
    "GenerationRequest",
    "RotationEngine",
    "RotationSettings",
    "SlotStatus",
    "estimate_tokens",
]

CHARS_PER_TOKEN = 3.0
"""Conservative characters-per-token ratio used to estimate request size."""
VALIDATION_REF = "__validation__"
_MIN_OUTPUT_TOKENS = 512
_INTERNAL_ERROR = 500
_TRANSIENT = frozenset(
    {FailureCategory.TIMEOUT, FailureCategory.SERVER_ERROR, FailureCategory.NETWORK_ERROR},
)
_RETRYABLE = _TRANSIENT | {FailureCategory.INFERENCE_ERROR, FailureCategory.UNKNOWN}

OutcomeStatus = Literal["ok", "deferred", "failed", "exhausted"]
_Verdict = Literal["ok", "failed", "postponed", "deferred"]


def _default_sleep(seconds: float) -> None:  # pragma: no cover - thin wrapper over time.sleep
    time.sleep(seconds)


def estimate_tokens(*texts: str) -> int:
    """Conservative token estimate for ``texts`` (the runtime ships no tokenizer)."""
    return math.ceil(sum(len(t) for t in texts) / CHARS_PER_TOKEN)


class SlotStatus(StrEnum):
    """Where one catalog model stands in this run."""

    UNRESOLVED = "unresolved"
    """Declared, but absent from the provider's live listing."""
    UNVALIDATED = "unvalidated"
    """Resolved; not yet probed (validation happens on first use)."""
    ACTIVE = "active"
    """Validated and serving."""
    EXHAUSTED = "exhausted"
    """Daily quota spent (declared RPD/TPD reached or reported by the provider)."""
    FAILED = "failed"
    """Failed validation or kept failing; out of rotation for the run."""


@dataclass(frozen=True, slots=True)
class RotationSettings:
    """Retry, backoff and pacing knobs (each overridable from the environment)."""

    model_retries: int = 3
    """Same-model retries after an error (never after a rate limit), per request."""
    list_passes: int = 2
    """Walks of the whole model list before giving up (1 = never re-walk)."""
    backoff_base: float = 2.0
    backoff_cap: float = 60.0
    list_backoff: float = 60.0
    """Pause before re-walking the list after models failed transiently."""
    default_cooldown: float = 60.0
    """Cooldown after a rate limit that carried no retry hint."""
    rate_limit_escalation: int = 3
    """Consecutive rate limits without a success that mean the model is spent."""
    resource_failure_limit: int = 3
    """Consecutive requests a model failed after retries before it is retired."""
    max_output_tokens: int = 4096
    headroom: float = 0.9

    def delay(self, attempt: int, jitter: float) -> float:
        """Full-jittered exponential backoff for a 1-based attempt."""
        ceiling = min(self.backoff_cap, self.backoff_base * 2 ** (attempt - 1))
        return float(round(ceiling * jitter, 3))


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    """One structured-output request, independent of the model that will serve it.

    ``prompt_for(body_chars)`` renders the user prompt with the document text
    cut to ``body_chars``, so the engine can fit it to a small model's limits.
    ``check(payload)`` returns ``None`` when an answer is usable, else why not.
    """

    system: str
    schema: Mapping[str, object]
    prompt_for: Callable[[int], str]
    check: Callable[[Mapping[str, Any]], str | None]
    ref: str | None = None
    max_body_chars: int = 6000
    min_body_chars: int = 600
    """A model whose limits leave less document text than this is not used."""
    deadline: float | None = None


@dataclass(frozen=True, slots=True)
class GenerationOutcome:
    """What happened to one request."""

    status: OutcomeStatus
    result: ProviderResult | None = None
    category: FailureCategory | None = None
    detail: str = ""
    provider: str | None = None
    model: str | None = None


@dataclass(frozen=True, slots=True)
class CachedValidation:
    """A validation verdict reused within the same quota day (saves probe quota)."""

    day: str
    ok: bool
    mode: str | None
    category: str | None
    detail: str

    def to_dict(self) -> dict[str, object]:
        """Serialise for the state ledger."""
        return {
            "day": self.day,
            "ok": self.ok,
            "mode": self.mode,
            "category": self.category,
            "detail": self.detail,
        }


@dataclass(slots=True)
class _Stats:
    attempts: int = 0
    successes: int = 0
    failures: int = 0
    categories: Counter[str] = field(default_factory=Counter)
    last_category: str | None = None
    last_error: str = ""

    def success(self) -> None:
        self.attempts += 1
        self.successes += 1

    def failure(self, category: FailureCategory, detail: str) -> None:
        self.attempts += 1
        self.failures += 1
        self.categories[category.value] += 1
        self.last_category = category.value
        self.last_error = detail

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempts": self.attempts,
            "successes": self.successes,
            "failures": self.failures,
            "failure_categories": dict(sorted(self.categories.items())),
            "last_error_category": self.last_category,
            "last_error_message": self.last_error[:2000],
        }


@dataclass(slots=True)
class _Provider:
    adapter: LLMProvider
    spec: ProviderSpec
    listed: tuple[ListedModel, ...] = ()
    down: bool = False
    revivable: bool = False
    reason: str = ""
    stats: _Stats = field(default_factory=_Stats)


@dataclass(slots=True)
class _Slot:
    provider: _Provider
    declared: DeclaredModel
    resolution: Resolution
    governor: ModelGovernor
    status: SlotStatus
    mode: str | None = None
    revivable: bool = False
    reason: str = ""
    rate_limits: int = 0
    resource_failures: int = 0
    validation: list[dict[str, Any]] = field(default_factory=list)
    stats: _Stats = field(default_factory=_Stats)

    @property
    def model_id(self) -> str:
        model = self.resolution.model
        return model.id if model else self.declared.name

    @property
    def key(self) -> str:
        return f"{self.provider.spec.id}:{self.model_id}"

    @property
    def provider_id(self) -> str:
        return self.provider.spec.id

    def usable(self) -> bool:
        if self.provider.down or self.status not in (SlotStatus.UNVALIDATED, SlotStatus.ACTIVE):
            return False
        if self.governor.exhausted():
            self.status = SlotStatus.EXHAUSTED
            self.reason = "daily quota reached"
            return False
        return True


@dataclass(frozen=True, slots=True)
class _Fit:
    prompt: str
    tokens: int
    max_output: int


@dataclass(slots=True)
class _Progress:
    """Per-request routing memory: models to skip, the last failure, the last provider."""

    skip: set[str] = field(default_factory=set)
    last: GenerationOutcome = field(
        default_factory=lambda: GenerationOutcome(
            "failed", detail="no model could serve this request"
        ),
    )
    provider: str | None = None


@dataclass(frozen=True, slots=True)
class _Call:
    result: ProviderResult | None
    error: ProviderError | None
    started: str
    start: float


class RotationEngine:
    """Route structured-output requests across the catalog's models."""

    def __init__(  # noqa: PLR0913 - collaborators are injected for deterministic tests
        self,
        providers: Sequence[LLMProvider],
        catalog: ModelCatalog,
        *,
        settings: RotationSettings | None = None,
        logger: StructuredLogger | None = None,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = _default_sleep,
        jitter: Callable[[], float] | None = None,
        now: Callable[[], datetime] | None = None,
        usage: Mapping[str, DailyUsage] | None = None,
        validations: Mapping[str, CachedValidation] | None = None,
    ) -> None:
        """Bind adapters (in catalog order) and collaborators; no request is made yet."""
        self._settings = settings or RotationSettings()
        self._logger = logger if logger is not None else StructuredLogger()
        self._clock = clock
        self._sleep = sleep
        self._jitter = jitter or (lambda: 1.0)
        self._now = now or (lambda: datetime.now(UTC))
        self._usage = dict(usage or {})
        self._cached = dict(validations or {})
        by_name = {p.name: p for p in providers}
        self._providers = [
            _Provider(by_name[spec.id], spec) for spec in catalog.providers if spec.id in by_name
        ]
        self._slots: list[_Slot] = []
        self._probe: GenerationRequest | None = None
        self._list_failures = 0
        self._exhausted = False
        self._retries: Counter[str] = Counter()

    # -- set-up ----------------------------------------------------------

    @property
    def logger(self) -> StructuredLogger:
        """The structured logger collecting every attempt."""
        return self._logger

    def quota_day(self, spec: ProviderSpec) -> str:
        """Today's quota-day key in the provider's quota time zone."""
        return self._now().astimezone(ZoneInfo(spec.quota_timezone)).date().isoformat()

    def discover(self, probe: GenerationRequest) -> None:
        """List every provider's models and resolve the catalog onto live ids.

        ``probe`` is the request a model must answer correctly before it serves.
        A rejected key fails fast; a listing that fails for any other reason
        takes that provider out of rotation for the run, with the cause recorded.

        Raises:
            ProviderConfigError: a provider rejected its API key.
        """
        self._probe = probe
        for provider in self._providers:
            try:
                provider.listed = tuple(provider.adapter.list_models())
            except ProviderError as exc:
                detail = exc.raw.strip() or exc.category.value
                provider.stats.failure(exc.category, detail)
                if exc.category is FailureCategory.AUTH_ERROR:
                    msg = (
                        f"{provider.spec.name} rejected {provider.spec.api_key_env} "
                        f"while listing models: {detail[:300]}"
                    )
                    raise ProviderConfigError(msg) from exc
                provider.down = True
                provider.reason = f"model listing failed ({exc.category.value}): {detail[:300]}"
            self._slots.extend(
                self._slot(provider, resolution)
                for resolution in resolve_models(provider.spec, provider.listed)
            )

    def _slot(self, provider: _Provider, resolution: Resolution) -> _Slot:
        spec = provider.spec
        day = functools.partial(self.quota_day, spec)
        model_id = resolution.model.id if resolution.model else resolution.declared.name
        key = f"{spec.id}:{model_id}"
        governor = ModelGovernor(
            resolution.declared.limits,
            day=day,
            clock=self._clock,
            usage=self._usage.get(key),
            headroom=self._settings.headroom,
        )
        if resolution.model is None:
            return _Slot(
                provider,
                resolution.declared,
                resolution,
                governor,
                SlotStatus.UNRESOLVED,
                reason=resolution.rule,
            )
        slot = _Slot(provider, resolution.declared, resolution, governor, SlotStatus.UNVALIDATED)
        cached = self._cached.get(key)
        if cached is not None and cached.day == day():
            slot.status = SlotStatus.ACTIVE if cached.ok else SlotStatus.FAILED
            slot.mode = cached.mode
            slot.reason = "" if cached.ok else cached.detail
            slot.validation.append({"result": "reused from earlier today", **cached.to_dict()})
        return slot

    # -- public queries --------------------------------------------------

    @property
    def exhausted(self) -> bool:
        """Whether no model can serve any further request this run."""
        return self._exhausted

    def has_capacity(self) -> bool:
        """Whether at least one model could still be tried."""
        return not self._exhausted and any(slot.usable() for slot in self._slots)

    def usage(self) -> dict[str, DailyUsage]:
        """Per-model daily usage, for persistence in the state ledger."""
        merged = dict(self._usage)
        merged.update(
            {slot.key: slot.governor.usage for slot in self._slots if slot.resolution.model},
        )
        return merged

    def validations(self) -> dict[str, CachedValidation]:
        """Validation verdicts, for reuse by later runs on the same quota day."""
        return dict(self._cached)

    def retry_summary(self) -> dict[str, int]:
        """How many retries were spent, by level."""
        return {
            "per_model": self._retries["model"],
            "per_provider": self._retries["provider"],
            "per_list": self._retries["list"],
        }

    def provider_report(self) -> dict[str, dict[str, Any]]:
        """Per-provider listing, status and attempt statistics."""
        report: dict[str, dict[str, Any]] = {}
        for provider in self._providers:
            used = {s.model_id for s in self._slots if s.provider is provider}
            report[provider.spec.id] = {
                "name": provider.spec.name,
                "base_url": provider.spec.base_url,
                "status": "down" if provider.down else "up",
                "reason": provider.reason,
                "listed_models": len(provider.listed),
                "listed_not_in_catalog": sorted(m.id for m in provider.listed if m.id not in used),
                **provider.stats.to_dict(),
            }
        return report

    def model_report(self) -> list[dict[str, Any]]:
        """Per-model resolution, validation, limits, usage and statistics."""
        return [
            {
                **slot.resolution.to_dict(),
                "status": slot.status.value,
                "reason": slot.reason,
                "mode": slot.mode,
                "limits": slot.declared.limits.to_dict(),
                "usage_today": slot.governor.usage.to_dict() if slot.resolution.model else None,
                "validation": list(slot.validation),
                **slot.stats.to_dict(),
            }
            for slot in self._slots
        ]

    # -- validation -------------------------------------------------------

    def validate_all(self, *, deadline: float | None = None) -> None:
        """Probe every resolved, still-unvalidated model now (``cyberkb preflight``)."""
        for slot in self._slots:
            if slot.usable() and slot.status is SlotStatus.UNVALIDATED:
                self._validate(slot, deadline)

    def _validate(self, slot: _Slot, deadline: float | None) -> _Verdict:
        """Run the probe down the provider's mode ladder."""
        probe = self._probe
        assert probe is not None  # noqa: S101 - slots exist only after discover(probe)
        fit = self._fit(slot, probe)
        if fit is None:
            return self._settle(
                slot,
                None,
                FailureCategory.MODEL_UNAVAILABLE,
                "the validation probe does not fit the model's limits",
            )
        for mode in slot.provider.adapter.request_modes():
            if not self._await(slot, fit.tokens, deadline):
                return "deferred"
            verdict = self._probe_mode(slot, probe, fit, mode)
            if verdict is not None:
                return verdict
        if slot.revivable:
            return self._settle(
                slot,
                None,
                FailureCategory.SERVER_ERROR,
                "every structured-output request mode failed with an internal server error",
            )
        return self._settle(
            slot,
            None,
            FailureCategory.MODEL_UNAVAILABLE,
            "every structured-output request mode was rejected",
        )

    def _probe_mode(
        self, slot: _Slot, probe: GenerationRequest, fit: _Fit, mode: str
    ) -> _Verdict | None:
        """One validation call in ``mode``; ``None`` means "try the next mode"."""
        call = self._call(slot, probe, fit, mode, VALIDATION_REF, attempt=1)
        if call.result is not None:
            problem = probe.check(call.result.payload)
            self._record(slot, call, mode, VALIDATION_REF, 1, problem)
            if problem is None:
                slot.mode = mode
                return self._settle(slot, mode, None, f"validated in {mode} mode")
            return self._settle(slot, mode, FailureCategory.INFERENCE_ERROR, problem)
        error = call.error
        assert error is not None  # noqa: S101 - a call yields a result or an error
        slot.validation.append(
            {"mode": mode, "category": error.category.value, "detail": error.raw.strip()[:500]},
        )
        if self._steps_down(slot, error):
            return None
        if self._route_quota(slot, error):
            return "postponed"
        if error.category is FailureCategory.AUTH_ERROR:
            self._provider_down(
                slot.provider, f"auth_error: {error.raw.strip()[:300]}", revivable=False
            )
            return "postponed"
        slot.revivable = error.category in _TRANSIENT
        return self._settle(slot, mode, error.category, error.raw.strip() or error.category.value)

    @staticmethod
    def _steps_down(slot: _Slot, error: ProviderError) -> bool:
        """Whether a validation failure should move on to the next request mode.

        A rejected request shape obviously does. So does a 500 INTERNAL: one
        specific to a structured-output path (observed live: Gemma 4 31B in
        native JSON mode) must not disqualify a model a simpler mode serves; if
        every mode fails that way, the model stays revivable rather than being
        written off for the day.
        """
        if error.request_rejected:
            return True
        if error.category is FailureCategory.SERVER_ERROR and error.status == _INTERNAL_ERROR:
            slot.revivable = True
            return True
        return False

    def _settle(
        self, slot: _Slot, mode: str | None, category: FailureCategory | None, detail: str
    ) -> _Verdict:
        ok = category is None
        if ok:
            slot.revivable = False
        slot.status = SlotStatus.ACTIVE if ok else SlotStatus.FAILED
        slot.reason = "" if ok else f"validation failed ({category}): {detail[:300]}"
        slot.validation.append(
            {
                "result": "validated" if ok else "failed",
                "mode": mode,
                "category": category.value if category else None,
                "detail": detail[:500],
            },
        )
        if not slot.revivable:
            self._cached[slot.key] = CachedValidation(
                day=self.quota_day(slot.provider.spec),
                ok=ok,
                mode=mode if ok else None,
                category=category.value if category else None,
                detail=detail[:500],
            )
        return "ok" if ok else "failed"

    # -- generation -------------------------------------------------------

    def generate(self, request: GenerationRequest) -> GenerationOutcome:
        """Serve ``request`` from the best available model (see the module docstring)."""
        progress = _Progress()
        while True:
            outcome = self._step(request, progress)
            if outcome is not None:
                return outcome

    def _step(self, request: GenerationRequest, progress: _Progress) -> GenerationOutcome | None:
        """Advance ``request`` by one decision; ``None`` means "keep going"."""
        stop = self._stopped(request)
        if stop is not None:
            return stop
        candidates = [s for s in self._slots if s.key not in progress.skip and s.usable()]
        if not candidates:
            return self._out_of_candidates(progress.last)
        choice = self._choose(candidates, request, progress.skip)
        if choice is None:
            return None
        if isinstance(choice, float):
            return self._pause(choice, request)
        slot, fit = choice
        if slot.status is SlotStatus.UNVALIDATED:
            return self._validate_first(slot, request)
        return self._dispatch(slot, request, fit, progress)

    def _stopped(self, request: GenerationRequest) -> GenerationOutcome | None:
        """The run-level reasons to stop before choosing a model, if any."""
        if self._exhausted:
            return GenerationOutcome("exhausted", detail="every model is exhausted or failed")
        if request.deadline is not None and self._clock() >= request.deadline:
            return GenerationOutcome("deferred", detail="run budget reached")
        return None

    def _validate_first(self, slot: _Slot, request: GenerationRequest) -> GenerationOutcome | None:
        """Validate ``slot`` before it may serve; only a missed deadline ends the request."""
        if self._validate(slot, request.deadline) == "deferred":
            return GenerationOutcome("deferred", detail="run budget reached in validation")
        return None

    def _pause(self, wait: float, request: GenerationRequest) -> GenerationOutcome | None:
        """Every candidate is paced: wait for the first, unless that misses the deadline."""
        if request.deadline is not None and self._clock() + wait >= request.deadline:
            return GenerationOutcome("deferred", detail="run budget reached while paced")
        self._sleep(wait)
        return None

    def _dispatch(
        self, slot: _Slot, request: GenerationRequest, fit: _Fit, progress: _Progress
    ) -> GenerationOutcome | None:
        """Serve the request on ``slot``; a failure updates the routing memory."""
        if progress.provider is not None and progress.provider != slot.provider_id:
            self._retries["provider"] += 1
        progress.provider = slot.provider_id
        outcome, request_scoped = self._serve(slot, request, fit)
        if outcome.status == "ok":
            self._list_failures = 0
        if outcome.status in ("ok", "deferred"):
            return outcome
        progress.last = outcome
        if request_scoped:
            progress.skip.add(slot.key)
        return None

    def _out_of_candidates(self, last: GenerationOutcome) -> GenerationOutcome | None:
        """No model is left for this request: fail it, re-walk the list, or give up."""
        if any(s.usable() for s in self._slots):
            return last
        if self._revive():
            return None
        self._exhausted = True
        return GenerationOutcome(
            "exhausted",
            category=last.category,
            detail=f"every model is exhausted or failed; last: {last.detail}",
            provider=last.provider,
            model=last.model,
        )

    def _choose(
        self, candidates: list[_Slot], request: GenerationRequest, skip: set[str]
    ) -> tuple[_Slot, _Fit] | float | None:
        """The best candidate callable now; else the shortest wait.

        A candidate the request cannot fit is skipped for this request (and
        ``None`` returned so the caller re-evaluates). Waits are always finite:
        exhausted models are not candidates, and a fitted request never exceeds
        the model's paced token window.
        """
        waits: list[float] = []
        for slot in candidates:
            fit = self._fit(slot, request)
            if fit is None:
                skip.add(slot.key)
                return None
            wait = slot.governor.wait_for(fit.tokens)
            if wait == 0:
                return slot, fit
            waits.append(wait)
        return min(waits)

    def _fit(self, slot: _Slot, request: GenerationRequest) -> _Fit | None:
        """Render the prompt to fit the model's context and paced TPM, or ``None``.

        The answer's token reservation comes first (a quarter of a shared
        context window, at least 512 tokens); the document text is then cut,
        measuring the rendered prompt each time, until the request fits — or
        would keep less than ``min_body_chars`` of the document, in which case
        this model is not used for it.
        """
        listed = slot.resolution.model
        assert listed is not None  # noqa: S101 - only resolved models are ever usable
        spec = slot.provider.spec
        max_output = self._settings.max_output_tokens
        window: int | None = None
        if listed.output_token_limit:
            max_output = min(max_output, listed.output_token_limit)
        if listed.input_token_limit and listed.shared_context:
            max_output = min(max_output, max(_MIN_OUTPUT_TOKENS, listed.input_token_limit // 4))
            window = listed.input_token_limit - max_output
        elif listed.input_token_limit:
            window = listed.input_token_limit
        reserve = max_output if spec.tpm_counts_completion else 0
        budget = slot.governor.token_capacity - reserve
        if window is not None:
            budget = min(budget, window)
        overhead = request.system + json.dumps(dict(request.schema))
        prompt = request.prompt_for(request.max_body_chars)
        limit = min(request.max_body_chars, len(prompt))
        tokens = estimate_tokens(overhead, prompt)
        while tokens > budget:
            limit -= math.ceil((tokens - budget) * CHARS_PER_TOKEN)
            if limit < request.min_body_chars:
                return None
            prompt = request.prompt_for(limit)
            tokens = estimate_tokens(overhead, prompt)
        return _Fit(prompt, tokens + reserve, max_output)

    def _await(self, slot: _Slot, tokens: int, deadline: float | None) -> bool:
        """Sleep until ``slot`` admits ``tokens``; ``False`` if that misses the deadline."""
        wait = slot.governor.wait_for(tokens)
        if wait > 0:
            if not math.isfinite(wait) or (
                deadline is not None and self._clock() + wait >= deadline
            ):
                return False
            self._sleep(wait)
        return True

    def _serve(
        self, slot: _Slot, request: GenerationRequest, fit: _Fit
    ) -> tuple[GenerationOutcome, bool]:
        """Try one model with same-model retries.

        Returns the outcome and whether the failure is specific to this request
        (so the request should skip this model while others keep using it).
        """
        mode = slot.mode or slot.provider.adapter.request_modes()[0]
        attempt = 0
        while True:
            attempt += 1
            if attempt > 1 and not self._await(slot, fit.tokens, request.deadline):
                return self._outcome("deferred", slot, None, "run budget reached in a retry"), False
            call = self._call(slot, request, fit, mode, request.ref, attempt=attempt)
            if call.result is not None:
                problem = request.check(call.result.payload)
                self._record(slot, call, mode, request.ref, attempt, problem)
                if problem is None:
                    slot.rate_limits = 0
                    slot.resource_failures = 0
                    return GenerationOutcome(
                        "ok", result=call.result, provider=slot.provider_id, model=slot.model_id
                    ), False
                category, detail, retry_after = FailureCategory.INFERENCE_ERROR, problem, None
            else:
                error = call.error
                assert error is not None  # noqa: S101 - a call yields a result or an error
                category, detail = error.category, error.raw.strip() or error.category.value
                retry_after = error.retry_after
                routed = self._route(slot, error)
                if routed is not None:
                    return self._outcome("failed", slot, category, detail), routed
            if category in _RETRYABLE and attempt <= self._settings.model_retries:
                delay = (
                    retry_after
                    if retry_after is not None
                    else self._settings.delay(attempt, self._jitter())
                )
                if request.deadline is not None and self._clock() + delay >= request.deadline:
                    return self._outcome(
                        "deferred", slot, None, "run budget reached in a retry"
                    ), False
                self._retries["model"] += 1
                self._sleep(delay)
                continue
            return self._outcome("failed", slot, category, detail), self._spent(
                slot, category, detail
            )

    def _route(self, slot: _Slot, error: ProviderError) -> bool | None:
        """Route a non-retryable failure; ``None`` means "retry it like an error".

        The returned flag says whether the failure is specific to this request.
        """
        if self._route_quota(slot, error):
            return False
        category = error.category
        if category is FailureCategory.AUTH_ERROR:
            self._provider_down(
                slot.provider, f"auth_error: {error.raw.strip()[:300]}", revivable=False
            )
            return False
        if category is FailureCategory.CONTENT_FILTER:
            return True
        if category is FailureCategory.MODEL_UNAVAILABLE:
            if error.request_rejected:
                # A validated mode rejected for this one request (e.g. an input the
                # model cannot take): skip the model for this request only.
                return True
            self._retire(slot, category, error.raw.strip(), revivable=False)
            return False
        return None

    def _spent(self, slot: _Slot, category: FailureCategory, detail: str) -> bool:
        """Same-model retries are spent: take the model or provider out, or skip it."""
        if category is FailureCategory.NETWORK_ERROR:
            self._provider_down(
                slot.provider, f"persistent network failure: {detail[:300]}", revivable=True
            )
            return False
        if category in _TRANSIENT:
            self._retire(slot, category, detail, revivable=True)
            return False
        slot.resource_failures += 1
        if slot.resource_failures >= self._settings.resource_failure_limit:
            self._retire(
                slot,
                category,
                f"failed {slot.resource_failures} consecutive requests: {detail}",
                revivable=False,
            )
        return True

    def _route_quota(self, slot: _Slot, error: ProviderError) -> bool:
        """Apply a rate limit or quota exhaustion; ``True`` when one applied."""
        if error.category is FailureCategory.QUOTA_EXCEEDED:
            slot.governor.mark_exhausted()
            slot.status = SlotStatus.EXHAUSTED
            slot.reason = "daily quota exhausted (reported by the provider)"
            return True
        if error.category is not FailureCategory.RATE_LIMIT:
            return False
        slot.rate_limits += 1
        if slot.rate_limits >= self._settings.rate_limit_escalation:
            # Rate limited again and again despite pacing and cooldowns: out of
            # rotation for this list pass (a later pass may bring it back).
            self._retire(
                slot,
                FailureCategory.RATE_LIMIT,
                f"{slot.rate_limits} consecutive rate limits without a success",
                revivable=True,
            )
        else:
            cooldown = error.retry_after
            slot.governor.tighten()
            slot.governor.cool(self._settings.default_cooldown if cooldown is None else cooldown)
        return True

    def _revive(self) -> bool:
        """Start another list pass if allowed and something failed only transiently."""
        if self._list_failures + 1 >= self._settings.list_passes:
            return False
        slots = [s for s in self._slots if s.status is SlotStatus.FAILED and s.revivable]
        providers = [p for p in self._providers if p.down and p.revivable]
        if not slots and not providers:
            return False
        self._list_failures += 1
        self._retries["list"] += 1
        for provider in providers:
            provider.down = False
            provider.revivable = False
            provider.reason = ""
        for slot in slots:
            slot.status = SlotStatus.ACTIVE if slot.mode else SlotStatus.UNVALIDATED
            slot.revivable = False
            slot.resource_failures = 0
            slot.reason = ""
        self._sleep(self._settings.list_backoff)
        return True

    def _retire(
        self, slot: _Slot, category: FailureCategory, detail: str, *, revivable: bool
    ) -> None:
        slot.status = SlotStatus.FAILED
        slot.revivable = revivable
        slot.reason = f"{category.value}: {detail[:300]}"

    def _provider_down(self, provider: _Provider, reason: str, *, revivable: bool) -> None:
        provider.down = True
        provider.revivable = revivable
        provider.reason = reason

    def _outcome(
        self, status: OutcomeStatus, slot: _Slot, category: FailureCategory | None, detail: str
    ) -> GenerationOutcome:
        return GenerationOutcome(
            status, category=category, detail=detail, provider=slot.provider_id, model=slot.model_id
        )

    # -- one call ---------------------------------------------------------

    def _call(
        self,
        slot: _Slot,
        request: GenerationRequest,
        fit: _Fit,
        mode: str,
        ref: str | None,
        *,
        attempt: int,
    ) -> _Call:
        """Make exactly one provider call; failures are logged here, answers by the caller."""
        entry = slot.governor.reserve(fit.tokens)
        started = utc_now_iso(self._now())
        start = self._clock()
        try:
            result = slot.provider.adapter.complete_json(
                slot.model_id,
                request.system,
                fit.prompt,
                request.schema,
                mode=mode,
                max_output_tokens=fit.max_output,
            )
        except ProviderError as error:
            call = _Call(None, error, started, start)
            self._log(slot, call, mode, ref, attempt, error.category, error.raw, error.status)
            return call
        actual = None
        if result.input_tokens is not None:
            completion = result.output_tokens or 0
            counts = slot.provider.spec.tpm_counts_completion
            actual = result.input_tokens + (completion if counts else 0)
        slot.governor.settle(entry, actual)
        if result.remaining_requests == 0:
            slot.governor.mark_exhausted()
        return _Call(result, None, started, start)

    def _record(
        self,
        slot: _Slot,
        call: _Call,
        mode: str,
        ref: str | None,
        attempt: int,
        problem: str | None,
    ) -> None:
        """Log an answered call as a success, or as an inference error if it was unusable."""
        if problem is None:
            self._log(slot, call, mode, ref, attempt, None, "", None)
        else:
            self._log(
                slot,
                call,
                mode,
                ref,
                attempt,
                FailureCategory.INFERENCE_ERROR,
                f"answer rejected: {problem}",
                200,
            )

    def _log(
        self,
        slot: _Slot,
        call: _Call,
        mode: str,
        ref: str | None,
        attempt: int,
        category: FailureCategory | None,
        raw: str,
        status: int | None,
    ) -> None:
        detail = raw.strip() or (category.value if category else "")
        for stats in (slot.stats, slot.provider.stats):
            if category is None:
                stats.success()
            else:
                stats.failure(category, detail)
        self._logger.record(
            AttemptLog(
                provider=slot.provider_id,
                model=slot.model_id,
                resource_id=ref,
                attempt=attempt,
                outcome="success" if category is None else "failure",
                started_at=call.started,
                ended_at=utc_now_iso(self._now()),
                duration_s=self._clock() - call.start,
                category=category,
                status=status,
                raw_error=raw,
                mode=mode,
            ),
        )
