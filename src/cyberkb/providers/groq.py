"""Groq provider (OpenAI-compatible ``/openai/v1``).

Contract verified against the official docs (console.groq.com/docs, 2026-10-07):

* ``GET /openai/v1/models`` returns ``{"object": "list", "data": [...]}`` whose
  items carry ``id``, ``active`` and ``context_window``. Only ``active`` models
  are candidates; the catalog decides which ones may be used.
* ``POST /openai/v1/chat/completions`` with ``Authorization: Bearer <key>``.
* Structured output: ``json_schema`` with ``strict: true`` (constrained
  decoding; documented for the gpt-oss and qwen3.8 models) and ``json_object``
  (JSON mode, documented for all models). Validation tries strict first and
  steps down only when the API rejects the request (``request_rejected``).
  Strict mode requires every object to set ``additionalProperties: false``
  and list all properties as required, so the schema is adapted here.
* Rate limits: ``x-ratelimit-limit-requests`` is the RPD, ``*-tokens`` the
  TPM; a 429 carries ``retry-after``. A 429 with no requests left for the day,
  or whose message names a daily window (RPD/TPD), is ``quota_exceeded``;
  otherwise it is a short-window ``rate_limit``.
* Errors are ``{"error": {"message", "type", "code"}}``; ``json_validate_failed``
  means the *model's* output was not valid JSON (an inference error), not that
  our request was malformed.
"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any, ClassVar, override

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.providers.base import (
    HttpProviderBase,
    ProviderResult,
    classify_http_status,
    render_schema_instruction,
    retry_after_seconds,
)
from cyberkb.providers.catalog import ListedModel

if TYPE_CHECKING:
    from collections.abc import Mapping

    from cyberkb.providers.http import HttpResponse

__all__ = ["GROQ_MODES", "GroqProvider", "strict_schema"]

GROQ_MODES: tuple[str, ...] = ("json_schema", "json_object")
_OK = 200
_TOO_MANY_REQUESTS = 429
_BAD_REQUEST = 400
_FORBIDDEN = 403
_FLEX_CAPACITY = 498  # Groq-specific: "Flex tier at capacity, try again later"
_TEMPERATURE = 0.1
_SCHEMA_NAME = "classifications"
_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_STRICT_DROP = frozenset({"propertyOrdering", "maxItems", "minItems"})
_OUTPUT_ERRORS = frozenset({"json_validate_failed", "output_parse_failed"})
# Errors about one model, not the key or the account: that model is out of
# rotation, the rest of the provider keeps serving. Groq answers a model that a
# project admin has not enabled with 403 `model_permission_blocked_project`.
_MODEL_CODES = frozenset(
    {
        "model_not_found",
        "model_decommissioned",
        "model_terminated",
        "model_permission_blocked_project",
        "model_permission_blocked_org",
    },
)


def strict_schema(schema: Mapping[str, object]) -> dict[str, Any]:
    """Adapt a JSON schema to Groq strict mode.

    Every object gains ``additionalProperties: false`` and keywords outside the
    documented strict subset are dropped; the caller still validates every
    field against the taxonomy, so nothing the schema loses is unchecked.
    """

    def adapt(node: object) -> object:
        if isinstance(node, list):
            return [adapt(v) for v in node]
        if not isinstance(node, dict):
            return node
        out = {k: adapt(v) for k, v in node.items() if k not in _STRICT_DROP}
        if out.get("type") == "object":
            out["additionalProperties"] = False
        return out

    adapted = adapt(dict(schema))
    return adapted if isinstance(adapted, dict) else {}


def _header(headers: Mapping[str, str], name: str) -> str | None:
    for key, value in headers.items():
        if key.lower() == name:
            return value
    return None


def _remaining_requests(headers: Mapping[str, str]) -> int | None:
    value = _header(headers, "x-ratelimit-remaining-requests")
    try:
        return int(value) if value is not None else None
    except ValueError:
        return None


def _error_fields(body: str) -> tuple[str, str]:
    try:
        envelope = json.loads(body)
    except json.JSONDecodeError:
        return "", body
    error = envelope.get("error") if isinstance(envelope, dict) else None
    if not isinstance(error, dict):
        return "", body
    return str(error.get("code") or ""), str(error.get("message") or "")


def _is_api_error(body: str) -> bool:
    """Whether ``body`` is Groq's own ``{"error": {...}}`` JSON (not an edge page)."""
    try:
        envelope = json.loads(body)
    except json.JSONDecodeError:
        return False
    return isinstance(envelope, dict) and isinstance(envelope.get("error"), dict)


class GroqProvider(HttpProviderBase):
    """Groq chat completions in strict JSON-schema or JSON-object mode."""

    name: ClassVar[str] = "groq"
    base_url: ClassVar[str] = "https://api.groq.com/openai/v1"

    def _headers(self, *, json_body: bool) -> dict[str, str]:
        headers = {"Authorization": f"Bearer {self._api_key}"}
        if json_body:
            headers["Content-Type"] = "application/json"
        return headers

    @override
    def request_modes(self) -> tuple[str, ...]:
        """``json_schema`` (strict) → ``json_object``."""
        return GROQ_MODES

    @override
    def _error(self, response: HttpResponse, *, model: str | None) -> ProviderError:
        code, message = _error_fields(response.text())
        retry_after = retry_after_seconds(response.headers)
        rejected = False
        if response.status == _TOO_MANY_REQUESTS:
            daily = _remaining_requests(response.headers) == 0 or any(
                window in message for window in ("(RPD)", "(TPD)", "per day")
            )
            category = FailureCategory.QUOTA_EXCEEDED if daily else FailureCategory.RATE_LIMIT
        elif code in _OUTPUT_ERRORS:
            category = FailureCategory.INFERENCE_ERROR
        elif code in _MODEL_CODES or code.startswith("model_permission_blocked"):
            category = FailureCategory.MODEL_UNAVAILABLE
        elif response.status == _FLEX_CAPACITY:
            category = FailureCategory.SERVER_ERROR
        elif response.status == _FORBIDDEN and not _is_api_error(response.text()):
            # Groq's own errors are JSON. A bare 403 ("error code: 1010") comes
            # from the Cloudflare edge in front of it: the request never reached
            # the API, so it says nothing about the key.
            category = FailureCategory.NETWORK_ERROR
        else:
            category = classify_http_status(response.status, response.text())
            rejected = response.status == _BAD_REQUEST
        return self._fail(
            category,
            raw=response.text(),
            model=model,
            status=response.status,
            retry_after=retry_after,
            request_rejected=rejected,
        )

    @override
    def list_models(self) -> list[ListedModel]:
        """List ``/models`` and keep the active entries."""
        data = self._get_mapping(f"{self.base_url}/models", headers=self._headers(json_body=False))
        entries = data.get("data")
        listed: list[ListedModel] = []
        for entry in entries if isinstance(entries, list) else []:
            if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
                continue
            if entry.get("active") is False:
                continue
            window = entry.get("context_window")
            completion = entry.get("max_completion_tokens")
            listed.append(
                ListedModel(
                    id=entry["id"],
                    input_token_limit=window if isinstance(window, int) else None,
                    output_token_limit=completion if isinstance(completion, int) else None,
                    shared_context=True,
                ),
            )
        return listed

    @override
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
        """One chat/completions call in ``mode``; failures are categorised."""
        if mode == "json_schema":
            response_format: dict[str, Any] = {
                "type": "json_schema",
                "json_schema": {
                    "name": _SCHEMA_NAME,
                    "strict": True,
                    "schema": strict_schema(schema),
                },
            }
            instruction = system
        elif mode == "json_object":
            response_format = {"type": "json_object"}
            instruction = render_schema_instruction(system, schema)
        else:
            msg = f"unknown Groq request mode {mode!r}"
            raise ValueError(msg)
        body = json.dumps(
            {
                "model": model,
                "messages": [
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": prompt},
                ],
                "temperature": _TEMPERATURE,
                "max_completion_tokens": max_output_tokens,
                "response_format": response_format,
            },
        ).encode("utf-8")
        start = self._clock()
        response = self._send(
            "POST",
            f"{self.base_url}/chat/completions",
            headers=self._headers(json_body=True),
            body=body,
            model=model,
        )
        if response.status != _OK:
            raise self._error(response, model=model)
        envelope = self._decode_object(response.text(), model=model)
        payload = self._decode_model_json(self._content(envelope, model=model), model=model)
        usage = envelope.get("usage")
        usage = usage if isinstance(usage, dict) else {}
        prompt_tokens = usage.get("prompt_tokens")
        completion_tokens = usage.get("completion_tokens")
        return ProviderResult(
            payload,
            self.name,
            model,
            self._elapsed(start),
            mode=mode,
            input_tokens=prompt_tokens if isinstance(prompt_tokens, int) else None,
            output_tokens=completion_tokens if isinstance(completion_tokens, int) else None,
            remaining_requests=_remaining_requests(response.headers),
        )

    def _content(self, envelope: Mapping[str, Any], *, model: str) -> str:
        choices = envelope.get("choices")
        if not isinstance(choices, list) or not choices:
            self._invalid_output("response had no choices", model=model)
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
            self._invalid_output("message had no content", model=model)
        return _THINK_RE.sub("", content)
