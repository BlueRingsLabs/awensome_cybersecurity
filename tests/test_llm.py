"""Tests for the dependency-free Gemini client."""

from __future__ import annotations

import io
import json
import urllib.error
from email.message import Message
from typing import TYPE_CHECKING, Any, ClassVar, Self

import pytest

from cyberkb.errors import LLMFatalError, LLMModelError, LLMResponseError, LLMRetryableError
from cyberkb.llm import GeminiClient, HttpResponse, UrllibTransport

if TYPE_CHECKING:
    from collections.abc import Mapping

    from cyberkb.llm import Transport

SCHEMA: dict[str, Any] = {"type": "object"}


class ScriptedTransport:
    """Transport returning queued responses in order, or raising queued exceptions."""

    def __init__(self, *responses: HttpResponse | Exception) -> None:
        """Queue the responses/exceptions to return on successive calls."""
        self.queue: list[HttpResponse | Exception] = list(responses)
        self.urls: list[str] = []

    def post(
        self,
        url: str,
        _payload: bytes,
        _headers: Mapping[str, str],
        _timeout: float,
    ) -> HttpResponse:
        """Record the URL and return (or raise) the next queued item."""
        self.urls.append(url)
        item = self.queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def _candidate(payload: dict[str, Any]) -> dict[str, Any]:
    """Wrap a JSON payload in a Gemini candidate envelope."""
    return {"candidates": [{"content": {"parts": [{"text": json.dumps(payload)}]}}]}


def _json_response(status: int = 200, obj: dict[str, Any] | None = None) -> HttpResponse:
    """Build an HttpResponse whose body is a JSON candidate envelope."""
    body = json.dumps(obj if obj is not None else _candidate({"ok": True})).encode()
    return HttpResponse(status, body)


def _client(transport: Transport, **kwargs: Any) -> GeminiClient:  # noqa: ANN401 -- forwards kwargs
    """Build a GeminiClient with fast, deterministic sleep/jitter by default."""
    kwargs.setdefault("sleep", lambda _s: None)
    kwargs.setdefault("jitter", lambda: 1.0)
    models: tuple[str, ...] = kwargs.pop("models", ("m1",))
    return GeminiClient("key", models, transport=transport, **kwargs)


def test_requires_api_key() -> None:
    """Constructing a client without an API key is a fatal error."""
    with pytest.raises(LLMFatalError):
        GeminiClient("", ("m",))


def test_requires_models() -> None:
    """Constructing a client with no models is a fatal error."""
    with pytest.raises(LLMFatalError):
        GeminiClient("key", ())


def test_successful_call() -> None:
    """A 200 response is parsed and the active model recorded."""
    transport = ScriptedTransport(_json_response(obj=_candidate({"classifications": []})))
    client = _client(transport)
    result = client.generate_json("sys", "prompt", SCHEMA)
    assert result == {"classifications": []}
    assert client.active_model == "m1"


def test_retry_then_success() -> None:
    """A retryable 503 is retried and the subsequent success returned."""
    transport = ScriptedTransport(
        HttpResponse(503, b"busy"),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, max_retries=3)
    assert client.generate_json("s", "p", SCHEMA) == {"ok": 1}
    assert len(transport.urls) == 2


def test_retry_exhausted() -> None:
    """Exhausting the retry budget on 429s raises a retryable error."""
    transport = ScriptedTransport(HttpResponse(429, b"x"), HttpResponse(429, b"x"))
    client = _client(transport, max_retries=2)
    with pytest.raises(LLMRetryableError):
        client.generate_json("s", "p", SCHEMA)


def test_retry_after_header_used() -> None:
    """A numeric Retry-After header sets the backoff delay."""
    delays: list[float] = []
    transport = ScriptedTransport(
        HttpResponse(429, b"x", {"Retry-After": "2"}),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, sleep=delays.append, max_retries=3)
    client.generate_json("s", "p", SCHEMA)
    assert delays == [2.0]


def test_retry_after_header_invalid_falls_back_to_backoff() -> None:
    """A non-numeric Retry-After header falls back to computed backoff."""
    delays: list[float] = []
    transport = ScriptedTransport(
        HttpResponse(429, b"x", {"Retry-After": "soon"}),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, sleep=delays.append, max_retries=3)
    client.generate_json("s", "p", SCHEMA)
    assert delays
    assert delays[0] > 0


def test_model_fallback() -> None:
    """A model-level rejection moves on to the next model in the chain."""
    transport = ScriptedTransport(
        HttpResponse(404, b"no such model"),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, models=("bad", "good"))
    assert client.generate_json("s", "p", SCHEMA) == {"ok": 1}
    assert client.active_model == "good"
    assert "bad" in transport.urls[0]
    assert "good" in transport.urls[1]


def test_all_models_rejected() -> None:
    """When every model is rejected, a model error is raised."""
    transport = ScriptedTransport(HttpResponse(400, b"bad"), HttpResponse(400, b"bad"))
    client = _client(transport, models=("a", "b"))
    with pytest.raises(LLMModelError):
        client.generate_json("s", "p", SCHEMA)


def test_fatal_status() -> None:
    """A 403 is a fatal authentication/quota failure."""
    transport = ScriptedTransport(HttpResponse(403, b"forbidden"))
    client = _client(transport)
    with pytest.raises(LLMFatalError):
        client.generate_json("s", "p", SCHEMA)


def test_unexpected_status() -> None:
    """An unexpected status code is a response error."""
    transport = ScriptedTransport(HttpResponse(204, b""))
    client = _client(transport)
    with pytest.raises(LLMResponseError):
        client.generate_json("s", "p", SCHEMA)


def test_invalid_json_body() -> None:
    """A non-JSON body is a response error."""
    transport = ScriptedTransport(HttpResponse(200, b"not json"))
    client = _client(transport)
    with pytest.raises(LLMResponseError):
        client.generate_json("s", "p", SCHEMA)


def test_blocked_no_candidates() -> None:
    """A safety block with no candidates surfaces the block reason."""
    body = json.dumps({"promptFeedback": {"blockReason": "SAFETY"}}).encode()
    transport = ScriptedTransport(HttpResponse(200, body))
    client = _client(transport)
    with pytest.raises(LLMResponseError, match="SAFETY"):
        client.generate_json("s", "p", SCHEMA)


def test_candidate_finished_early() -> None:
    """A non-STOP finish reason (e.g. MAX_TOKENS) is a response error."""
    body = json.dumps(
        {"candidates": [{"finishReason": "MAX_TOKENS", "content": {"parts": []}}]},
    ).encode()
    transport = ScriptedTransport(HttpResponse(200, body))
    client = _client(transport)
    with pytest.raises(LLMResponseError, match="early"):
        client.generate_json("s", "p", SCHEMA)


def test_candidate_bad_content() -> None:
    """A candidate whose text is not JSON is a response error."""
    body = json.dumps({"candidates": [{"content": {"parts": [{"text": "not json"}]}}]}).encode()
    transport = ScriptedTransport(HttpResponse(200, body))
    client = _client(transport)
    with pytest.raises(LLMResponseError):
        client.generate_json("s", "p", SCHEMA)


def test_candidate_payload_not_object() -> None:
    """A candidate JSON payload that is not an object is a response error."""
    body = json.dumps({"candidates": [{"content": {"parts": [{"text": "[1, 2]"}]}}]}).encode()
    transport = ScriptedTransport(HttpResponse(200, body))
    client = _client(transport)
    with pytest.raises(LLMResponseError, match="object"):
        client.generate_json("s", "p", SCHEMA)


def test_network_error_is_retryable() -> None:
    """A transport-raised retryable error is retried, not propagated."""
    transport = ScriptedTransport(
        LLMRetryableError("boom"),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, max_retries=2)
    assert client.generate_json("s", "p", SCHEMA) == {"ok": 1}


def test_urllib_transport_network_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """A urllib URLError is translated into a retryable error."""

    def boom(*_a: object, **_k: object) -> None:
        msg = "down"
        raise urllib.error.URLError(msg)

    monkeypatch.setattr("urllib.request.urlopen", boom)
    with pytest.raises(LLMRetryableError):
        UrllibTransport().post("https://x.test", b"{}", {}, 1.0)


def test_urllib_transport_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """A urllib HTTPError is captured as an HttpResponse with its status/body."""

    def raise_http(*_a: object, **_k: object) -> None:
        url, reason = "https://x.test", "err"
        raise urllib.error.HTTPError(url, 500, reason, Message(), io.BytesIO(b"body"))

    monkeypatch.setattr("urllib.request.urlopen", raise_http)
    response = UrllibTransport().post("https://x.test", b"{}", {}, 1.0)
    assert response.status == 500
    assert response.body == b"body"


def test_retry_after_ignores_other_headers() -> None:
    """Without a Retry-After header, the computed backoff delay is used."""
    delays: list[float] = []
    transport = ScriptedTransport(
        HttpResponse(503, b"x", {"Content-Type": "text/plain", "X-Other": "1"}),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, sleep=delays.append, max_retries=3)
    client.generate_json("s", "p", SCHEMA)
    assert delays
    assert delays[0] > 0


class _FakeResponse:
    """A minimal urlopen context manager for the success path."""

    status: ClassVar[int] = 200
    headers: ClassVar[dict[str, str]] = {"X": "y"}

    def read(self, _n: int) -> bytes:
        """Return a fixed JSON body."""
        return b"{}"

    def __enter__(self) -> Self:
        """Enter the context manager."""
        return self

    def __exit__(self, *_a: object) -> None:
        """Exit without suppressing exceptions."""
        return


def test_urllib_transport_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """A successful urlopen is wrapped into an HttpResponse."""
    monkeypatch.setattr("urllib.request.urlopen", lambda *_a, **_k: _FakeResponse())
    response = UrllibTransport().post("https://x.test", b"{}", {"h": "v"}, 1.0)
    assert response.status == 200
    assert response.body == b"{}"
