"""Tests for the urllib-backed HTTP transport at the provider boundary."""

from __future__ import annotations

import email.message
import io
import urllib.error
import urllib.request
from typing import TYPE_CHECKING, Self

import pytest

from cyberkb.providers.http import HttpResponse, HttpTransportError, UrllibTransport

if TYPE_CHECKING:
    from collections.abc import Mapping


class _FakeResponse:
    """A minimal stand-in for an http.client.HTTPResponse context manager."""

    def __init__(self, status: int, body: bytes, headers: Mapping[str, str]) -> None:
        self.status = status
        self._body = body
        self.headers = headers

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_exc: object) -> None:
        """Do not suppress exceptions."""

    def read(self, _amt: int) -> bytes:
        return self._body


def _http_error(status: int, body: bytes) -> urllib.error.HTTPError:
    headers = email.message.Message()
    headers["Content-Type"] = "application/json"
    return urllib.error.HTTPError("https://x", status, "err", headers, io.BytesIO(body))


def test_response_text_decodes_body() -> None:
    """HttpResponse.text decodes bytes as UTF-8, replacing bad sequences."""
    assert HttpResponse(200, b'{"a": 1}').text() == '{"a": 1}'


def test_response_defaults_to_empty_headers() -> None:
    """A response built without headers exposes an empty mapping, not None."""
    assert HttpResponse(200, b"x").headers == {}


def test_request_success_returns_status_body_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    """A 2xx response is returned verbatim with its headers."""
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda _req, timeout: _FakeResponse(200, b'{"ok": true}', {"X-Test": "1"}),  # noqa: ARG005
    )
    response = UrllibTransport().request("GET", "https://x", headers={}, body=None, timeout=5)
    assert response.status == 200
    assert response.text() == '{"ok": true}'
    assert response.headers["X-Test"] == "1"


def test_request_http_error_becomes_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """A 4xx/5xx is a real response the caller categorises, not an exception."""

    def _raise(_req: object, timeout: float) -> _FakeResponse:
        _ = timeout
        raise _http_error(503, b"overloaded")

    monkeypatch.setattr(urllib.request, "urlopen", _raise)
    response = UrllibTransport().request("POST", "https://x", headers={}, body=b"{}", timeout=5)
    assert response.status == 503
    assert response.text() == "overloaded"


def test_request_urlerror_timeout_reason_is_a_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """A URLError wrapping a TimeoutError is reported as a timeout."""

    def _raise(_req: object, timeout: float) -> _FakeResponse:
        _ = timeout
        raise urllib.error.URLError(TimeoutError("timed out"))

    monkeypatch.setattr(urllib.request, "urlopen", _raise)
    with pytest.raises(HttpTransportError) as exc:
        UrllibTransport().request("GET", "https://x", headers={}, body=None, timeout=5)
    assert exc.value.timeout is True


def test_request_urlerror_other_reason_is_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """A URLError with a non-timeout reason is a network error."""

    def _raise(_req: object, timeout: float) -> _FakeResponse:
        _ = timeout
        msg = "name resolution failed"
        raise urllib.error.URLError(msg)

    monkeypatch.setattr(urllib.request, "urlopen", _raise)
    with pytest.raises(HttpTransportError) as exc:
        UrllibTransport().request("GET", "https://x", headers={}, body=None, timeout=5)
    assert exc.value.timeout is False


def test_request_bare_timeout_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """A bare TimeoutError from urlopen is reported as a timeout."""

    def _raise(_req: object, timeout: float) -> _FakeResponse:
        _ = timeout
        raise TimeoutError

    monkeypatch.setattr(urllib.request, "urlopen", _raise)
    with pytest.raises(HttpTransportError) as exc:
        UrllibTransport().request("GET", "https://x", headers={}, body=None, timeout=5)
    assert exc.value.timeout is True


def test_request_oserror_is_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """A generic OSError (e.g. connection refused) is a non-timeout network error."""

    def _raise(_req: object, timeout: float) -> _FakeResponse:
        _ = timeout
        msg = "refused"
        raise ConnectionRefusedError(msg)

    monkeypatch.setattr(urllib.request, "urlopen", _raise)
    with pytest.raises(HttpTransportError) as exc:
        UrllibTransport().request("GET", "https://x", headers={}, body=None, timeout=5)
    assert exc.value.timeout is False
