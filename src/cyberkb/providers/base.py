"""The common provider interface and the HTTP machinery every provider shares.

:class:`LLMProvider` is the contract the rotation engine talks to: list the
models the key can reach, name the structured-output request modes the
provider offers (best first), and make one categorised structured-output call.
Every provider is interchangeable behind it.

:class:`HttpProviderBase` supplies what is identical across REST providers:
one guarded request, key redaction, JSON decoding and recovery of a JSON object
from free text. Each call is a *single* attempt: pacing, retries, cooldowns and
model/provider rotation all live in the engine, so the only thing a provider
ever raises is one categorised :class:`cyberkb.errors.ProviderError`.
"""

from __future__ import annotations

import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, NoReturn, override

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.providers.http import HttpTransportError, UrllibTransport
from cyberkb.textutil import unfence

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from typing import Any

    from cyberkb.providers.catalog import ListedModel
    from cyberkb.providers.http import HttpResponse, Transport

__all__ = [
    "DEFAULT_TIMEOUT",
    "HttpProviderBase",
    "LLMProvider",
    "ProviderResult",
    "classify_http_status",
    "render_schema_instruction",
    "retry_after_seconds",
]

DEFAULT_TIMEOUT = 60.0
REDACTED = "[REDACTED]"
# Keys shorter than this are test placeholders, not secrets; redacting them
# would only mangle ordinary words in error text.
_MIN_REDACT_LEN = 8

_OK = 200
_BAD_REQUEST = 400
_UNAUTHORIZED = 401
_PAYMENT_REQUIRED = 402
_FORBIDDEN = 403
_NOT_FOUND = 404
_REQUEST_TIMEOUT = 408
_PAYLOAD_TOO_LARGE = 413
_UNPROCESSABLE = 422
_TOO_MANY_REQUESTS = 429
_GATEWAY_TIMEOUT = 504
_SERVER_ERROR_FLOOR = 500
_SERVER_ERROR_CEILING = 600
_DAILY_HINTS = ("per day", "perday", "daily", "rpd", "tpd")
_SIMPLE_STATUS: dict[int, FailureCategory] = {
    _UNAUTHORIZED: FailureCategory.AUTH_ERROR,
    _FORBIDDEN: FailureCategory.AUTH_ERROR,
    _PAYMENT_REQUIRED: FailureCategory.QUOTA_EXCEEDED,
    _REQUEST_TIMEOUT: FailureCategory.TIMEOUT,
    _GATEWAY_TIMEOUT: FailureCategory.TIMEOUT,
    _BAD_REQUEST: FailureCategory.MODEL_UNAVAILABLE,
    _NOT_FOUND: FailureCategory.MODEL_UNAVAILABLE,
    _PAYLOAD_TOO_LARGE: FailureCategory.MODEL_UNAVAILABLE,
    _UNPROCESSABLE: FailureCategory.INFERENCE_ERROR,
}


def classify_http_status(status: int, body: str) -> FailureCategory:
    """Map an HTTP error status (and its body) to a :class:`FailureCategory`.

    This is the provider-neutral baseline; providers refine it with the
    structured error details they expose. A 429 is a short-window
    ``rate_limit`` unless the body names a *daily* window, in which case the
    model's quota for the day is spent (``quota_exceeded``) and waiting a
    minute will not help. 400/404/413 mean this model cannot serve the request
    as sent, so the engine moves on to another model.
    """
    if status == _TOO_MANY_REQUESTS:
        daily = any(hint in body.lower() for hint in _DAILY_HINTS)
        return FailureCategory.QUOTA_EXCEEDED if daily else FailureCategory.RATE_LIMIT
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


def render_schema_instruction(system: str, schema: Mapping[str, object]) -> str:
    """Append the exact JSON schema to a system prompt for non-native JSON modes."""
    return (
        f"{system}\n\nReturn a single JSON object and nothing else: no prose, no "
        f"Markdown. It must conform to this JSON schema:\n{json.dumps(dict(schema))}"
    )


@dataclass(frozen=True, slots=True)
class ProviderResult:
    """A successful structured-output call: the parsed JSON plus provenance.

    ``input_tokens``/``output_tokens`` are the provider's own usage counts when
    it reports them; the engine uses them to keep its token pacing honest.
    ``remaining_requests`` is the provider-reported requests left in the
    model's daily window, when it exposes one (Groq does, in headers).
    """

    payload: dict[str, Any]
    provider: str
    model: str
    latency_s: float
    mode: str = ""
    input_tokens: int | None = None
    output_tokens: int | None = None
    remaining_requests: int | None = None


class LLMProvider(ABC):
    """The interface the rotation engine depends on; every provider implements it."""

    name: ClassVar[str] = ""
    base_url: ClassVar[str] = ""

    @abstractmethod
    def is_configured(self) -> bool:
        """Return ``True`` when this provider has the credentials it needs."""
        raise NotImplementedError

    @abstractmethod
    def list_models(self) -> list[ListedModel]:
        """Return every generative model the key can call, from the live listing.

        Raises:
            ProviderError: the listing failed (``auth_error`` for a rejected key).
        """
        raise NotImplementedError

    @abstractmethod
    def request_modes(self) -> tuple[str, ...]:
        """Structured-output request modes, strongest guarantee first."""
        raise NotImplementedError

    @abstractmethod
    def complete_json(
        self,
        model: str,
        system: str,
        prompt: str,
        schema: Mapping[str, object],
        *,
        mode: str,
        max_output_tokens: int,
    ) -> ProviderResult:
        """Make one structured-output call in ``mode`` and return the parsed object.

        Raises:
            ProviderError: a single categorised failure (no retries here).
        """
        raise NotImplementedError


class HttpProviderBase(LLMProvider):
    """Shared REST plumbing for providers that speak JSON over HTTPS."""

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

    # -- shared helpers for subclasses ------------------------------------

    def redact(self, text: str) -> str:
        """Remove the API key from ``text`` before it is logged or persisted.

        Provider error bodies never echo the key today, but the raw text ends
        up in committed run reports, so this is enforced rather than assumed.
        """
        if len(self._api_key) >= _MIN_REDACT_LEN:
            return text.replace(self._api_key, REDACTED)
        return text

    def _fail(
        self,
        category: FailureCategory,
        *,
        raw: str,
        model: str | None = None,
        status: int | None = None,
        retry_after: float | None = None,
        request_rejected: bool = False,
    ) -> ProviderError:
        """Build a categorised, key-redacted :class:`ProviderError` for this provider."""
        return ProviderError(
            category,
            provider=self.name,
            model=model,
            status=status,
            raw=self.redact(raw),
            retry_after=retry_after,
            request_rejected=request_rejected,
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

    @abstractmethod
    def _error(self, response: HttpResponse, *, model: str | None) -> ProviderError:
        """Categorise a non-200 response using the provider's own error details."""
        raise NotImplementedError

    def _get_mapping(self, url: str, *, headers: Mapping[str, str]) -> dict[str, Any]:
        """GET ``url`` and return a decoded JSON object, or raise a ProviderError."""
        response = self._send("GET", url, headers=headers)
        if response.status != _OK:
            raise self._error(response, model=None)
        return self._decode_object(response.text())

    def _elapsed(self, start: float) -> float:
        """Seconds since ``start`` on the injected clock, rounded for logging."""
        return round(self._clock() - start, 3)

    def _invalid_output(self, reason: str, *, model: str | None) -> NoReturn:
        raise self._fail(FailureCategory.INFERENCE_ERROR, raw=reason, model=model, status=_OK)

    def _decode_object(self, text: str, *, model: str | None = None) -> dict[str, Any]:
        """Parse ``text`` as a JSON object; a non-object or bad JSON is an inference error."""
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            self._invalid_output(f"invalid JSON: {exc}", model=model)
        if not isinstance(value, dict):
            self._invalid_output("response was not a JSON object", model=model)
        return value

    def _decode_model_json(self, text: str, *, model: str) -> dict[str, Any]:
        """Recover the JSON object a model returned as text.

        Tries the text as-is, then without a Markdown fence, then from the
        first ``{`` (models in prompt mode sometimes lead with a sentence).
        Anything else is an ``inference_error`` carrying the decoder's reason.
        """
        body = unfence(text)
        try:
            value = json.loads(body)
        except json.JSONDecodeError as exc:
            start = body.find("{")
            if start < 0:
                self._invalid_output(f"no JSON object in model output: {exc}", model=model)
            try:
                value, _ = json.JSONDecoder().raw_decode(body, start)
            except json.JSONDecodeError as inner:
                self._invalid_output(f"invalid JSON in model output: {inner}", model=model)
        if not isinstance(value, dict):
            self._invalid_output("model output was not a JSON object", model=model)
        return value
