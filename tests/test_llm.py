"""Tests for the dependency-free Gemini client."""

from __future__ import annotations

import json

import pytest

from cyberkb.errors import LLMFatalError, LLMModelError, LLMResponseError, LLMRetryableError
from cyberkb.llm import GeminiClient, HttpResponse, UrllibTransport

SCHEMA = {"type": "object"}


class ScriptedTransport:
    """Transport returning queued responses, or raising queued exceptions."""

    def __init__(self, *responses: HttpResponse | Exception) -> None:
        self.queue = list(responses)
        self.urls: list[str] = []

    def post(self, url, payload, headers, timeout):
        self.urls.append(url)
        item = self.queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def _json_response(status: int = 200, obj: dict | None = None) -> HttpResponse:
    body = json.dumps(obj if obj is not None else _candidate({"ok": True})).encode()
    return HttpResponse(status, body)


def _candidate(payload: dict) -> dict:
    return {"candidates": [{"content": {"parts": [{"text": json.dumps(payload)}]}}]}


def _client(transport, **kwargs) -> GeminiClient:
    kwargs.setdefault("sleep", lambda _s: None)
    kwargs.setdefault("jitter", lambda: 1.0)
    return GeminiClient("key", kwargs.pop("models", ("m1",)), transport=transport, **kwargs)


def test_requires_api_key() -> None:
    with pytest.raises(LLMFatalError):
        GeminiClient("", ("m",))


def test_requires_models() -> None:
    with pytest.raises(LLMFatalError):
        GeminiClient("key", ())


def test_successful_call() -> None:
    transport = ScriptedTransport(_json_response(obj=_candidate({"classifications": []})))
    client = _client(transport)
    result = client.generate_json("sys", "prompt", SCHEMA)
    assert result == {"classifications": []}
    assert client.active_model == "m1"


def test_retry_then_success() -> None:
    transport = ScriptedTransport(
        HttpResponse(503, b"busy"),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, max_retries=3)
    assert client.generate_json("s", "p", SCHEMA) == {"ok": 1}
    assert len(transport.urls) == 2


def test_retry_exhausted() -> None:
    transport = ScriptedTransport(HttpResponse(429, b"x"), HttpResponse(429, b"x"))
    client = _client(transport, max_retries=2)
    with pytest.raises(LLMRetryableError):
        client.generate_json("s", "p", SCHEMA)


def test_retry_after_header_used() -> None:
    delays: list[float] = []
    transport = ScriptedTransport(
        HttpResponse(429, b"x", {"Retry-After": "2"}),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, sleep=delays.append, max_retries=3)
    client.generate_json("s", "p", SCHEMA)
    assert delays == [2.0]


def test_retry_after_header_invalid_falls_back_to_backoff() -> None:
    delays: list[float] = []
    transport = ScriptedTransport(
        HttpResponse(429, b"x", {"Retry-After": "soon"}),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, sleep=delays.append, max_retries=3)
    client.generate_json("s", "p", SCHEMA)
    assert delays and delays[0] > 0


def test_model_fallback() -> None:
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
    transport = ScriptedTransport(HttpResponse(400, b"bad"), HttpResponse(400, b"bad"))
    client = _client(transport, models=("a", "b"))
    with pytest.raises(LLMModelError):
        client.generate_json("s", "p", SCHEMA)


def test_fatal_status() -> None:
    transport = ScriptedTransport(HttpResponse(403, b"forbidden"))
    client = _client(transport)
    with pytest.raises(LLMFatalError):
        client.generate_json("s", "p", SCHEMA)


def test_unexpected_status() -> None:
    transport = ScriptedTransport(HttpResponse(204, b""))
    client = _client(transport)
    with pytest.raises(LLMResponseError):
        client.generate_json("s", "p", SCHEMA)


def test_invalid_json_body() -> None:
    transport = ScriptedTransport(HttpResponse(200, b"not json"))
    client = _client(transport)
    with pytest.raises(LLMResponseError):
        client.generate_json("s", "p", SCHEMA)


def test_blocked_no_candidates() -> None:
    body = json.dumps({"promptFeedback": {"blockReason": "SAFETY"}}).encode()
    transport = ScriptedTransport(HttpResponse(200, body))
    client = _client(transport)
    with pytest.raises(LLMResponseError, match="SAFETY"):
        client.generate_json("s", "p", SCHEMA)


def test_candidate_finished_early() -> None:
    body = json.dumps(
        {"candidates": [{"finishReason": "MAX_TOKENS", "content": {"parts": []}}]}
    ).encode()
    transport = ScriptedTransport(HttpResponse(200, body))
    client = _client(transport)
    with pytest.raises(LLMResponseError, match="early"):
        client.generate_json("s", "p", SCHEMA)


def test_candidate_bad_content() -> None:
    body = json.dumps({"candidates": [{"content": {"parts": [{"text": "not json"}]}}]}).encode()
    transport = ScriptedTransport(HttpResponse(200, body))
    client = _client(transport)
    with pytest.raises(LLMResponseError):
        client.generate_json("s", "p", SCHEMA)


def test_candidate_payload_not_object() -> None:
    body = json.dumps({"candidates": [{"content": {"parts": [{"text": "[1, 2]"}]}}]}).encode()
    transport = ScriptedTransport(HttpResponse(200, body))
    client = _client(transport)
    with pytest.raises(LLMResponseError, match="object"):
        client.generate_json("s", "p", SCHEMA)


def test_network_error_is_retryable() -> None:
    transport = ScriptedTransport(
        LLMRetryableError("boom"),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, max_retries=2)
    assert client.generate_json("s", "p", SCHEMA) == {"ok": 1}


def test_urllib_transport_network_error(monkeypatch) -> None:
    import urllib.error

    def boom(*_a: object, **_k: object) -> None:
        raise urllib.error.URLError("down")

    monkeypatch.setattr("urllib.request.urlopen", boom)
    with pytest.raises(LLMRetryableError):
        UrllibTransport().post("https://x.test", b"{}", {}, 1.0)


def test_urllib_transport_http_error(monkeypatch) -> None:
    import io
    import urllib.error

    def raise_http(*_a: object, **_k: object) -> None:
        from email.message import Message

        raise urllib.error.HTTPError("https://x.test", 500, "err", Message(), io.BytesIO(b"body"))

    monkeypatch.setattr("urllib.request.urlopen", raise_http)
    response = UrllibTransport().post("https://x.test", b"{}", {}, 1.0)
    assert response.status == 500
    assert response.body == b"body"


def test_retry_after_ignores_other_headers() -> None:
    delays: list[float] = []
    transport = ScriptedTransport(
        HttpResponse(503, b"x", {"Content-Type": "text/plain", "X-Other": "1"}),
        _json_response(obj=_candidate({"ok": 1})),
    )
    client = _client(transport, sleep=delays.append, max_retries=3)
    client.generate_json("s", "p", SCHEMA)
    # No Retry-After header: backoff delay is used, not a header value.
    assert delays and delays[0] > 0


def test_urllib_transport_success(monkeypatch) -> None:
    from typing import Self

    class FakeResp:
        status = 200
        headers = {"X": "y"}

        def read(self, _n: int) -> bytes:
            return b"{}"

        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_a: object) -> None:
            return None

    monkeypatch.setattr("urllib.request.urlopen", lambda *_a, **_k: FakeResp())
    response = UrllibTransport().post("https://x.test", b"{}", {"h": "v"}, 1.0)
    assert response.status == 200
    assert response.body == b"{}"
