"""Shared base for OpenAI-compatible chat providers (OpenRouter, HF router).

Both speak the same ``/chat/completions`` and ``/models`` dialect, so the call
shape, JSON-mode handling and response parsing live here once; a concrete
provider supplies only its base URL, auth, model-discovery filter and ranking.

Free and open models vary in how strictly they honour JSON mode, so two
defences are layered: the exact response schema is embedded in the system
message (not just set as ``response_format``), and a Markdown code fence around
the answer is stripped before parsing. Every field is still validated against
the taxonomy downstream, so a sloppy answer degrades to a per-document
heuristic fallback rather than a bad classification.
"""

from __future__ import annotations

import json
from abc import abstractmethod
from typing import TYPE_CHECKING, ClassVar, override

from cyberkb.errors import FailureCategory
from cyberkb.providers.base import (
    HttpProviderBase,
    ModelCandidate,
    ProviderResult,
    classify_http_status,
    retry_after_seconds,
)

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any

__all__ = ["OpenAICompatProvider"]

_OK = 200
_TEMPERATURE = 0.1


def _render_system(system: str, schema: Mapping[str, object]) -> str:
    """Append the exact JSON schema to the system message for non-native JSON modes."""
    return (
        f"{system}\n\nReturn a single JSON object and nothing else. It must conform "
        f"to this JSON schema:\n{json.dumps(dict(schema))}"
    )


def _unfence(text: str) -> str:
    """Strip a surrounding ```json ... ``` (or ``` ... ```) code fence, if present."""
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    body = lines[1:-1] if len(lines) >= 2 and lines[-1].strip() == "```" else lines[1:]  # noqa: PLR2004
    return "\n".join(body).strip()


class OpenAICompatProvider(HttpProviderBase):
    """A provider that speaks the OpenAI ``/chat/completions`` + ``/models`` dialect."""

    name: ClassVar[str] = ""
    base_url: ClassVar[str] = ""

    def _extra_headers(self) -> dict[str, str]:
        """Provider-specific headers beyond the bearer token (default: none)."""
        return {}

    def _auth_headers(self, *, json_body: bool) -> dict[str, str]:
        headers = {"Authorization": f"Bearer {self._api_key}", **self._extra_headers()}
        if json_body:
            headers["Content-Type"] = "application/json"
        return headers

    @override
    def discover_models(self) -> list[ModelCandidate]:
        """List models from ``/models`` and keep the ones ``_candidate`` accepts."""
        data = self._get_mapping(
            f"{self.base_url}/models", headers=self._auth_headers(json_body=False)
        )
        listed = data.get("data")
        entries = listed if isinstance(listed, list) else []
        candidates = [c for e in entries if (c := self._candidate(e)) is not None]
        candidates.sort(key=lambda c: c.score, reverse=True)
        return candidates

    @abstractmethod
    def _candidate(self, entry: object) -> ModelCandidate | None:
        """Turn one catalog entry into a ranked candidate, or ``None`` to drop it."""
        raise NotImplementedError

    @override
    def complete_json(
        self,
        model: str,
        system: str,
        prompt: str,
        schema: Mapping[str, object],
    ) -> ProviderResult:
        """One chat/completions call in JSON mode; failures are categorised."""
        body = json.dumps(
            {
                "model": model,
                "messages": [
                    {"role": "system", "content": _render_system(system, schema)},
                    {"role": "user", "content": prompt},
                ],
                "temperature": _TEMPERATURE,
                "response_format": {"type": "json_object"},
            },
        ).encode("utf-8")
        start = self._clock()
        response = self._send(
            "POST",
            f"{self.base_url}/chat/completions",
            headers=self._auth_headers(json_body=True),
            body=body,
            model=model,
        )
        if response.status != _OK:
            raise self._fail(
                classify_http_status(response.status, response.text()),
                raw=response.text(),
                status=response.status,
                model=model,
                retry_after=retry_after_seconds(response.headers),
            )
        payload = self._extract(self._decode_object(response.text(), model=model), model=model)
        return ProviderResult(payload, self.name, model, self._elapsed(start))

    def _extract(self, envelope: dict[str, Any], *, model: str) -> dict[str, Any]:
        choices = envelope.get("choices")
        if not isinstance(choices, list) or not choices:
            raise self._fail(
                FailureCategory.INFERENCE_ERROR,
                raw="response had no choices",
                model=model,
                status=_OK,
            )
        choice = choices[0] if isinstance(choices[0], dict) else {}
        if choice.get("finish_reason") == "content_filter":
            raise self._fail(
                FailureCategory.CONTENT_FILTER,
                raw="content filtered by model",
                model=model,
                status=_OK,
            )
        message = choice.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, str) or not content.strip():
            raise self._fail(
                FailureCategory.INFERENCE_ERROR,
                raw="message had no content",
                model=model,
                status=_OK,
            )
        return self._decode_object(_unfence(content), model=model)
