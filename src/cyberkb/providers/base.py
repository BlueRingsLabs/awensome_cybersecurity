"""The common provider interface and the HTTP machinery every provider shares.

:class:`LLMProvider` is the contract the orchestrator talks to: discover usable
models, classify one batch to JSON, and report health. Every provider is
interchangeable behind it, so adding a fourth is implementing this class and
registering it — no orchestration change.

:class:`HttpProviderBase` supplies the parts that are identical across REST
providers: configuration check, a single guarded request, HTTP-status → failure
categorisation, JSON decoding, and a health probe built on ``complete_json``.
Each attempt is a *single* call: retries, backoff, model rotation and provider
fallback all live in the orchestrator, so this layer stays small and the
failure it raises is always one categorised :class:`cyberkb.errors.ProviderError`.
"""

from __future__ import annotations

import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, override

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.providers.http import HttpTransportError, UrllibTransport

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from typing import Any

    from cyberkb.providers.http import HttpResponse, Transport

__all__ = [
    "DEFAULT_TIMEOUT",
    "HealthResult",
    "HttpProviderBase",
    "LLMProvider",
    "ModelCandidate",
    "ProviderResult",
    "classify_http_status",
    "retry_after_seconds",
]

DEFAULT_TIMEOUT = 60.0

_OK = 200
_BAD_REQUEST = 400
_UNAUTHORIZED = 401
_PAYMENT_REQUIRED = 402
_FORBIDDEN = 403
_NOT_FOUND = 404
_REQUEST_TIMEOUT = 408
_TOO_MANY_REQUESTS = 429
_SERVER_ERROR_FLOOR = 500
_SERVER_ERROR_CEILING = 600
_QUOTA_HINTS = ("quota", "billing", "credit", "insufficient", "exceeded", "payment", "balance")
# Status codes whose category does not depend on the body text.
_SIMPLE_STATUS: dict[int, FailureCategory] = {
    _UNAUTHORIZED: FailureCategory.AUTH_ERROR,
    _PAYMENT_REQUIRED: FailureCategory.QUOTA_EXCEEDED,
    _REQUEST_TIMEOUT: FailureCategory.TIMEOUT,
    _BAD_REQUEST: FailureCategory.MODEL_UNAVAILABLE,
    _NOT_FOUND: FailureCategory.MODEL_UNAVAILABLE,
}

_HEALTH_SYSTEM = "You are a health probe. Return only the JSON object you are asked for."
_HEALTH_PROMPT = 'Return exactly this JSON and nothing else: {"status": "ok"}'
_HEALTH_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {"status": {"type": "string"}},
    "required": ["status"],
}


def classify_http_status(status: int, body: str) -> FailureCategory:
    """Map an HTTP error status (and its body) to a :class:`FailureCategory`.

    A 429 or 403 is read as a *quota* exhaustion rather than a plain rate limit
    or auth failure when the body mentions billing/credits, because those need
    different handling (a wait will not help). 400/404 are treated as the model
    being unavailable so the orchestrator rotates to the next model.
    """
    quota = any(hint in body.lower() for hint in _QUOTA_HINTS)
    if status == _FORBIDDEN:
        return FailureCategory.QUOTA_EXCEEDED if quota else FailureCategory.AUTH_ERROR
    if status == _TOO_MANY_REQUESTS:
        return FailureCategory.QUOTA_EXCEEDED if quota else FailureCategory.RATE_LIMIT
    if status in _SIMPLE_STATUS:
        return _SIMPLE_STATUS[status]
    if _SERVER_ERROR_FLOOR <= status < _SERVER_ERROR_CEILING:
        return FailureCategory.SERVER_ERROR
    return FailureCategory.UNKNOWN


def retry_after_seconds(headers: Mapping[str, str]) -> float | None:
    """Parse a ``Retry-After`` header (seconds form) into a float, or ``None``."""
    for key, value in headers.items():
        if key.lower() == "retry-after":
            try:
                return max(0.0, float(value))
            except ValueError:
                return None
    return None


@dataclass(frozen=True, slots=True)
class ModelCandidate:
    """A model a provider offers that passed discovery filtering.

    ``score`` is the provider's own preference (higher is better) used to order
    candidates for validation and rotation; ``rationale`` records why, for the
    run report.
    """

    provider: str
    model_id: str
    is_free: bool
    context_window: int | None
    score: float
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        """Serialise for the model-selection section of the run report."""
        return {
            "provider": self.provider,
            "model_id": self.model_id,
            "is_free": self.is_free,
            "context_window": self.context_window,
            "score": round(self.score, 3),
            "rationale": self.rationale,
        }


@dataclass(frozen=True, slots=True)
class ProviderResult:
    """A successful structured-output call: the parsed JSON plus provenance."""

    payload: dict[str, Any]
    provider: str
    model: str
    latency_s: float


@dataclass(frozen=True, slots=True)
class HealthResult:
    """The outcome of a pre-flight probe against one provider/model."""

    provider: str
    model: str | None
    ok: bool
    latency_s: float
    category: FailureCategory | None = None
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialise for the provider-health section of the run report."""
        return {
            "provider": self.provider,
            "model": self.model,
            "ok": self.ok,
            "latency_s": round(self.latency_s, 3),
            "category": self.category.value if self.category is not None else None,
            "detail": self.detail,
        }


class LLMProvider(ABC):
    """The interface the orchestrator depends on; every provider implements it."""

    name: ClassVar[str] = ""

    @abstractmethod
    def is_configured(self) -> bool:
        """Return ``True`` when this provider has the credentials it needs."""
        raise NotImplementedError

    @abstractmethod
    def discover_models(self) -> list[ModelCandidate]:
        """Query the provider's catalog and return usable candidates, best first."""
        raise NotImplementedError

    @abstractmethod
    def complete_json(
        self,
        model: str,
        system: str,
        prompt: str,
        schema: Mapping[str, object],
    ) -> ProviderResult:
        """Make one structured-output call and return the parsed JSON object.

        Raises:
            ProviderError: a single categorised failure (no retries here).
        """
        raise NotImplementedError

    @abstractmethod
    def available(self, model: str) -> bool:
        """Cheap pre-check that ``model`` can be called now (providers may assume yes)."""
        raise NotImplementedError

    @abstractmethod
    def health_check(self, model: str) -> HealthResult:
        """Probe ``model`` with a trivial request to confirm the key works."""
        raise NotImplementedError


class HttpProviderBase(LLMProvider):
    """Shared REST plumbing: one provider needs only discovery + one call shape."""

    name: ClassVar[str] = ""

    def __init__(
        self,
        api_key: str,
        *,
        transport: Transport | None = None,
        clock: Callable[[], float] = time.monotonic,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Store the key and injected collaborators (transport, clock, timeout)."""
        self._api_key = api_key
        self._transport: Transport = transport or UrllibTransport()
        self._clock = clock
        self._timeout = timeout

    @override
    def is_configured(self) -> bool:
        """Configured when an API key is present."""
        return bool(self._api_key)

    @override
    def available(self, model: str) -> bool:
        """Cheap pre-check that ``model`` can be called now (default: assume yes).

        Providers that expose a model-status endpoint (e.g. Hugging Face) override
        this so a cold or gated model is skipped before a full validation call.
        """
        return True

    @override
    def health_check(self, model: str) -> HealthResult:
        """Run a minimal ``complete_json`` and report success or the failure cause."""
        start = self._clock()
        try:
            result = self.complete_json(model, _HEALTH_SYSTEM, _HEALTH_PROMPT, _HEALTH_SCHEMA)
        except ProviderError as exc:
            return HealthResult(
                provider=self.name,
                model=model,
                ok=False,
                latency_s=round(self._clock() - start, 3),
                category=exc.category,
                detail=exc.raw.strip() or exc.category.value,
            )
        return HealthResult(provider=self.name, model=model, ok=True, latency_s=result.latency_s)

    # -- shared helpers for subclasses ------------------------------------

    def _fail(
        self,
        category: FailureCategory,
        *,
        raw: str,
        model: str | None = None,
        status: int | None = None,
        retry_after: float | None = None,
    ) -> ProviderError:
        """Build a categorised :class:`ProviderError` tagged with this provider."""
        return ProviderError(
            category,
            provider=self.name,
            model=model,
            status=status,
            raw=raw,
            retry_after=retry_after,
        )

    def _send(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        body: bytes | None = None,
        model: str | None = None,
    ) -> HttpResponse:
        """Send one request, turning a transport-level fault into a ProviderError."""
        try:
            return self._transport.request(
                method, url, headers=headers, body=body, timeout=self._timeout
            )
        except HttpTransportError as exc:
            category = FailureCategory.TIMEOUT if exc.timeout else FailureCategory.NETWORK_ERROR
            raise self._fail(category, raw=str(exc), model=model) from exc

    def _get_mapping(self, url: str, *, headers: Mapping[str, str]) -> dict[str, Any]:
        """GET ``url`` and return a decoded JSON object, or raise a ProviderError."""
        response = self._send("GET", url, headers=headers)
        if response.status != _OK:
            raise self._fail(
                classify_http_status(response.status, response.text()),
                raw=response.text(),
                status=response.status,
            )
        return self._decode_object(response.text())

    def _elapsed(self, start: float) -> float:
        """Seconds since ``start`` on the injected clock, rounded for logging."""
        return round(self._clock() - start, 3)

    def _decode_object(self, text: str, *, model: str | None = None) -> dict[str, Any]:
        """Parse ``text`` as a JSON object; a non-object or bad JSON is an inference error."""
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            raise self._fail(
                FailureCategory.INFERENCE_ERROR, raw=f"invalid JSON: {exc}", model=model
            ) from exc
        if not isinstance(value, dict):
            raise self._fail(
                FailureCategory.INFERENCE_ERROR, raw="response was not a JSON object", model=model
            )
        return value
