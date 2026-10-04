"""Minimal, dependency-free client for the Gemini generateContent API.

Why hand-rolled rather than the ``google-genai`` SDK (ADR-0004): the pipeline
runs in CI with repository write access and a live API key, so every third-
party dependency is attack surface we cannot fully audit. One HTTPS POST to a
documented JSON endpoint needs only the standard library, which keeps the
runtime dependency set at PyYAML alone.

The transport is injectable, so tests exercise every branch -- retryable
errors, model fallback, truncation, blocked responses, malformed JSON --
without a network or an API key.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Protocol

from cyberkb.errors import (
    LLMFatalError,
    LLMModelError,
    LLMResponseError,
    LLMRetryableError,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

__all__ = [
    "GeminiClient",
    "HttpResponse",
    "Transport",
    "UrllibTransport",
    "default_sleep",
]

_API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"
_RETRYABLE_STATUS = frozenset({408, 429, 500, 502, 503, 504})
_MODEL_STATUS = frozenset({400, 404})
_FATAL_STATUS = frozenset({401, 403})
_MAX_RESPONSE_BYTES = 4 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class HttpResponse:
    """A transport's view of an HTTP response."""

    status: int
    body: bytes
    headers: Mapping[str, str] = field(default_factory=dict)


class Transport(Protocol):
    """Pluggable HTTP POST used by :class:`GeminiClient`."""

    def post(
        self, url: str, payload: bytes, headers: Mapping[str, str], timeout: float
    ) -> HttpResponse:
        """Perform a POST and return the response.

        Raises:
            LLMRetryableError: on a network-level fault.
        """
        ...


class UrllibTransport:
    """Default transport backed by :mod:`urllib`, honouring the agent proxy."""

    def post(
        self, url: str, payload: bytes, headers: Mapping[str, str], timeout: float
    ) -> HttpResponse:
        """POST ``payload`` to ``url``; network-level faults become retryable errors."""
        request = urllib.request.Request(url, data=payload, headers=dict(headers), method="POST")  # noqa: S310
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
                return HttpResponse(
                    response.status, response.read(_MAX_RESPONSE_BYTES), dict(response.headers)
                )
        except urllib.error.HTTPError as exc:
            return HttpResponse(exc.code, exc.read(_MAX_RESPONSE_BYTES), dict(exc.headers or {}))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            msg = f"network error calling Gemini: {exc}"
            raise LLMRetryableError(msg) from exc


def default_sleep(seconds: float) -> None:  # pragma: no cover - thin wrapper over time.sleep
    """Sleep helper; injected in tests to avoid real delays."""
    time.sleep(seconds)


@dataclass(frozen=True, slots=True)
class _Backoff:
    base: float = 1.0
    cap: float = 60.0

    def delay(self, attempt: int, jitter: float) -> float:
        """Full-jittered exponential backoff for a 1-based ``attempt``."""
        ceiling = min(self.cap, self.base * 2 ** (attempt - 1))
        return float(round(ceiling * jitter, 3))


class GeminiClient:
    """Classify-oriented wrapper over Gemini ``generateContent``.

    Args:
        api_key: Gemini API key.
        models: ordered fallback chain of model ids; the first that is not
            rejected with a model error is used for the whole run.
        transport: HTTP transport (injectable for tests).
        sleep: sleep function (injectable for tests).
        jitter: returns a value in ``[0, 1]`` for backoff jitter (injectable).
        max_retries: retry budget per request for retryable failures.
        timeout: per-request timeout in seconds.
    """

    def __init__(
        self,
        api_key: str,
        models: tuple[str, ...],
        *,
        transport: Transport | None = None,
        sleep: Callable[[float], None] = default_sleep,
        jitter: Callable[[], float] | None = None,
        max_retries: int = 5,
        timeout: float = 60.0,
    ) -> None:
        """Store configuration and injected collaborators."""
        if not api_key:
            msg = "a Gemini API key is required"
            raise LLMFatalError(msg)
        if not models:
            msg = "at least one model id is required"
            raise LLMFatalError(msg)
        self._api_key = api_key
        self._models = models
        self._transport = transport or UrllibTransport()
        self._sleep = sleep
        self._jitter = jitter or (lambda: 1.0)
        self._max_retries = max(1, max_retries)
        self._timeout = timeout
        self._backoff = _Backoff()
        self._active_model: str | None = None

    @property
    def active_model(self) -> str | None:
        """The model id that last served a successful request."""
        return self._active_model

    def generate_json(
        self, system_instruction: str, prompt: str, response_schema: Mapping[str, object]
    ) -> dict[str, Any]:
        """Return the parsed JSON object for one structured-output request.

        Tries each configured model in order; a model-level rejection moves to
        the next model, a retryable failure is retried with backoff, and a
        fatal failure aborts immediately.

        Raises:
            LLMModelError: every model was rejected.
            LLMFatalError: authentication or quota failure.
            LLMResponseError: the final response could not be parsed.
            LLMRetryableError: retries were exhausted.
        """
        body = json.dumps(
            {
                "systemInstruction": {"parts": [{"text": system_instruction}]},
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.1,
                    "responseMimeType": "application/json",
                    "responseSchema": dict(response_schema),
                },
            },
        ).encode("utf-8")
        last_model_error: LLMModelError | None = None
        for model in self._models:
            try:
                parsed = self._call_model(model, body)
            except LLMModelError as exc:
                last_model_error = exc
                continue
            self._active_model = model
            return parsed
        assert last_model_error is not None  # noqa: S101 -- models is non-empty, so loop ran
        raise last_model_error

    def _call_model(self, model: str, body: bytes) -> dict[str, Any]:
        url = f"{_API_ROOT}/{model}:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": self._api_key}
        last_retryable: LLMRetryableError | None = None
        for attempt in range(1, self._max_retries + 1):
            try:
                response = self._transport.post(url, body, headers, self._timeout)
                return self._handle(response)
            except LLMRetryableError as exc:
                last_retryable = exc
                if attempt < self._max_retries:
                    self._sleep(exc.retry_after or self._backoff.delay(attempt, self._jitter()))
        assert last_retryable is not None  # noqa: S101 -- loop runs at least once
        raise last_retryable

    def _handle(self, response: HttpResponse) -> dict[str, Any]:
        if response.status in _RETRYABLE_STATUS:
            msg = f"Gemini returned retryable status {response.status}"
            raise LLMRetryableError(msg, retry_after=_retry_after(response.headers))
        if response.status in _FATAL_STATUS:
            msg = f"Gemini authentication/quota failure (status {response.status})"
            raise LLMFatalError(msg)
        if response.status in _MODEL_STATUS:
            msg = f"Gemini rejected the model/request (status {response.status})"
            raise LLMModelError(msg)
        if response.status != 200:  # noqa: PLR2004 -- 200 is the one success code
            msg = f"Gemini returned unexpected status {response.status}"
            raise LLMResponseError(msg)
        return _extract_json(response.body)


def _retry_after(headers: Mapping[str, str]) -> float | None:
    for key, value in headers.items():
        if key.lower() == "retry-after":
            try:
                return max(0.0, float(value))
            except ValueError:
                return None
    return None


def _extract_json(raw: bytes) -> dict[str, Any]:
    try:
        envelope = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        msg = "Gemini response was not valid JSON"
        raise LLMResponseError(msg) from exc
    candidates = envelope.get("candidates") if isinstance(envelope, dict) else None
    if not candidates:
        feedback = envelope.get("promptFeedback", {}) if isinstance(envelope, dict) else {}
        reason = feedback.get("blockReason", "no candidates returned")
        msg = f"Gemini returned no usable candidate ({reason})"
        raise LLMResponseError(msg)
    candidate = candidates[0]
    if candidate.get("finishReason") not in (None, "STOP"):
        msg = f"Gemini stopped early: {candidate.get('finishReason')}"
        raise LLMResponseError(msg)
    try:
        text = "".join(part["text"] for part in candidate["content"]["parts"])
        payload = json.loads(text)
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        msg = "Gemini candidate did not contain parseable JSON content"
        raise LLMResponseError(msg) from exc
    if not isinstance(payload, dict):
        msg = "Gemini JSON payload was not an object"
        raise LLMResponseError(msg)
    return payload
