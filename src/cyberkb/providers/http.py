"""The one HTTP boundary every provider shares.

A provider never touches the network directly; it goes through a
:class:`Transport`, which is injectable so the whole provider stack can be
unit-tested without a socket or an API key. The default :class:`UrllibTransport`
uses only the standard library (ADR-0004: no third-party HTTP client in a job
that holds repository write access and live API keys).

The transport returns an :class:`HttpResponse` for anything the server
answered — including 4xx/5xx, which are real responses the caller categorises —
and raises :class:`HttpTransportError` only when the request never completed
(DNS, TLS, connection refused, timeout).
"""

from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol

from cyberkb import __version__

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ["USER_AGENT", "HttpResponse", "HttpTransportError", "Transport", "UrllibTransport"]

MAX_RESPONSE_BYTES = 8 * 1024 * 1024
USER_AGENT = f"cyberkb/{__version__} (+https://github.com/BlueRingsLabs/awesome_cybersecurity)"


class HttpTransportError(Exception):
    """A request that never produced an HTTP response (network- or timeout-level)."""

    def __init__(self, message: str, *, timeout: bool) -> None:
        """Record whether the failure was a timeout (vs. another network fault)."""
        super().__init__(message)
        self.timeout = timeout


@dataclass(frozen=True, slots=True)
class HttpResponse:
    """A transport's view of an HTTP response (any status the server returned)."""

    status: int
    body: bytes
    headers: Mapping[str, str] = field(default_factory=dict)

    def text(self) -> str:
        """Best-effort UTF-8 decode of the body for error messages and parsing."""
        return self.body.decode("utf-8", errors="replace")


class Transport(Protocol):
    """Pluggable HTTP request primitive used by every provider."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout: float,
    ) -> HttpResponse:
        """Perform one request and return the response.

        Raises:
            HttpTransportError: the request did not complete (network/timeout).
        """
        ...


class UrllibTransport:
    """Default transport backed by :mod:`urllib`, honouring the agent proxy."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout: float,
    ) -> HttpResponse:
        """Send ``method`` ``url``; non-responses become :class:`HttpTransportError`.

        An explicit ``User-Agent`` is always sent. urllib's default
        (``Python-urllib/3.x``) is refused by Cloudflare-fronted APIs such as
        Groq with ``403 error code: 1010`` before the request reaches the API.
        """
        merged = {"User-Agent": USER_AGENT, **dict(headers)}
        request = urllib.request.Request(url, data=body, headers=merged, method=method)  # noqa: S310
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
                return HttpResponse(
                    response.status,
                    response.read(MAX_RESPONSE_BYTES),
                    dict(response.headers),
                )
        except urllib.error.HTTPError as exc:
            return HttpResponse(exc.code, exc.read(MAX_RESPONSE_BYTES), dict(exc.headers or {}))
        except urllib.error.URLError as exc:
            msg = f"network error: {exc.reason}"
            raise HttpTransportError(msg, timeout=isinstance(exc.reason, TimeoutError)) from exc
        except TimeoutError as exc:
            msg = f"request timed out after {timeout}s"
            raise HttpTransportError(msg, timeout=True) from exc
        except OSError as exc:
            msg = f"network error: {exc}"
            raise HttpTransportError(msg, timeout=False) from exc
