"""Discover, validate and rank a provider's models before the real run.

Discovery proposes candidates; this module *proves* them. For each candidate
(best first, up to a cap) it first asks the provider whether the model is
available, then sends a few representative cybersecurity prompts and checks the
answers are real, well-formed and usable via an injected ``validate`` predicate.
A model is accepted only when every sample passes; validation stops once enough
good models are found, to respect free-tier rate limits.

The result (:class:`ProviderSelection`) records exactly which models were
accepted or rejected and why, feeding both the orchestrator's rotation order
and the run report's model-selection section. Every validation call is logged
through the same structured logger as the real run.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.obslog import AttemptLog, utc_now_iso
from cyberkb.providers.base import HealthResult

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from typing import Any

    from cyberkb.obslog import StructuredLogger
    from cyberkb.providers.base import LLMProvider, ModelCandidate

__all__ = ["ModelValidation", "ProviderSelection", "ValidationRequest", "select_models"]

DEFAULT_NEED = 2
DEFAULT_MAX_CANDIDATES = 4
_VALIDATION_REF = "__validation__"
_OK_STATUS = 200


@dataclass(frozen=True, slots=True)
class ModelValidation:
    """The validation outcome for one candidate model."""

    model_id: str
    accepted: bool
    reason: str
    samples_passed: int
    samples_total: int
    avg_latency_s: float | None

    def to_dict(self) -> dict[str, Any]:
        """Serialise for the model-selection section of the run report."""
        return {
            "model_id": self.model_id,
            "accepted": self.accepted,
            "reason": self.reason,
            "samples_passed": self.samples_passed,
            "samples_total": self.samples_total,
            "avg_latency_s": self.avg_latency_s,
        }


@dataclass(frozen=True, slots=True)
class ProviderSelection:
    """Everything learned about one provider during pre-flight."""

    provider: str
    discovered: int
    validations: tuple[ModelValidation, ...]
    error: str = ""

    def accepted_models(self) -> list[str]:
        """The accepted model ids, in validated (preference) order."""
        return [v.model_id for v in self.validations if v.accepted]

    def as_health(self) -> HealthResult:
        """Summarise the selection as a provider-health record for the report."""
        accepted = [v for v in self.validations if v.accepted]
        if accepted:
            first = accepted[0]
            return HealthResult(
                provider=self.provider,
                model=first.model_id,
                ok=True,
                latency_s=first.avg_latency_s or 0.0,
                detail=f"{len(accepted)} model(s) validated",
            )
        detail = self.error or (
            self.validations[-1].reason if self.validations else "no models discovered"
        )
        return HealthResult(
            provider=self.provider,
            model=None,
            ok=False,
            latency_s=0.0,
            category=FailureCategory.MODEL_UNAVAILABLE,
            detail=detail,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialise the whole selection for the run report."""
        return {
            "provider": self.provider,
            "discovered": self.discovered,
            "accepted": self.accepted_models(),
            "error": self.error,
            "validations": [v.to_dict() for v in self.validations],
        }


@dataclass(frozen=True, slots=True)
class ValidationRequest:
    """The inputs a validation pass needs, bundled so callers pass one object."""

    system: str
    samples: Sequence[str]
    schema: Mapping[str, object]
    validate: Callable[[Mapping[str, Any]], bool]
    need: int = DEFAULT_NEED
    max_candidates: int = DEFAULT_MAX_CANDIDATES


def _avg(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 3) if values else None


def _emit(logger: StructuredLogger | None, log: AttemptLog) -> None:
    if logger is not None:
        logger.record(log)


def select_models(
    provider: LLMProvider,
    request: ValidationRequest,
    *,
    logger: StructuredLogger | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> ProviderSelection:
    """Discover and validate ``provider`` models; return the ranked selection."""
    try:
        candidates = provider.discover_models()
    except ProviderError as exc:
        reason = exc.raw.strip() or exc.category.value
        return ProviderSelection(
            provider=provider.name,
            discovered=0,
            validations=(),
            error=f"discovery failed ({exc.category.value}): {reason}",
        )
    validations: list[ModelValidation] = []
    accepted = 0
    for candidate in candidates:
        if accepted >= request.need or len(validations) >= request.max_candidates:
            break
        result = _validate_candidate(provider, candidate, request, logger=logger, clock=clock)
        validations.append(result)
        accepted += int(result.accepted)
    return ProviderSelection(provider.name, len(candidates), tuple(validations))


def _validate_candidate(
    provider: LLMProvider,
    candidate: ModelCandidate,
    request: ValidationRequest,
    *,
    logger: StructuredLogger | None,
    clock: Callable[[], float],
) -> ModelValidation:
    model = candidate.model_id
    total = len(request.samples)
    if not provider.available(model):
        return ModelValidation(
            model_id=model,
            accepted=False,
            reason="model not available",
            samples_passed=0,
            samples_total=total,
            avg_latency_s=None,
        )
    latencies: list[float] = []
    for index, sample in enumerate(request.samples, start=1):
        started = utc_now_iso()
        start = clock()
        try:
            result = provider.complete_json(model, request.system, sample, request.schema)
        except ProviderError as exc:
            _emit(
                logger,
                AttemptLog(
                    provider=provider.name,
                    model=model,
                    resource_id=_VALIDATION_REF,
                    attempt=index,
                    outcome="failure",
                    started_at=started,
                    ended_at=utc_now_iso(),
                    duration_s=clock() - start,
                    category=exc.category,
                    status=exc.status,
                    raw_error=exc.raw,
                ),
            )
            return ModelValidation(
                model_id=model,
                accepted=False,
                reason=f"validation call failed ({exc.category.value})",
                samples_passed=index - 1,
                samples_total=total,
                avg_latency_s=_avg(latencies),
            )
        duration = clock() - start
        latencies.append(duration)
        ok = request.validate(result.payload)
        _emit(
            logger,
            AttemptLog(
                provider=provider.name,
                model=model,
                resource_id=_VALIDATION_REF,
                attempt=index,
                outcome="success" if ok else "failure",
                started_at=started,
                ended_at=utc_now_iso(),
                duration_s=duration,
                category=None if ok else FailureCategory.INFERENCE_ERROR,
                status=_OK_STATUS,
                raw_error="" if ok else "output failed validation",
            ),
        )
        if not ok:
            return ModelValidation(
                model_id=model,
                accepted=False,
                reason="output failed format/quality check",
                samples_passed=index - 1,
                samples_total=total,
                avg_latency_s=_avg(latencies),
            )
    return ModelValidation(
        model_id=model,
        accepted=True,
        reason="validated",
        samples_passed=total,
        samples_total=total,
        avg_latency_s=_avg(latencies),
    )
