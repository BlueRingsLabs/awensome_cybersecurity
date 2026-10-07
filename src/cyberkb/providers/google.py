"""Google AI Studio provider (Gemini API ``v1beta``): Gemini and Gemma models.

Contract verified against the official reference (ai.google.dev/api, 2026-10-07):

* ``GET /v1beta/models`` is paginated (``pageSize`` up to 1000, ``nextPageToken``);
  each ``Model`` has ``name`` (``models/{id}``), ``displayName``,
  ``inputTokenLimit``, ``outputTokenLimit`` and ``supportedGenerationMethods``.
  Only models offering ``generateContent`` are generative candidates.
* ``POST /v1beta/models/{id}:generateContent`` with the key in the
  ``x-goog-api-key`` header (never in the URL, so it cannot leak into logs).
* Structured output has three request modes, tried strongest first while a
  model is being validated: ``json_schema`` (``responseJsonSchema``, standard
  JSON Schema), ``response_schema`` (the older OpenAPI-subset
  ``responseSchema``) and ``prompt`` (schema embedded in the system prompt, JSON
  recovered from text) for models without native JSON mode. A mode the API
  rejects as ``INVALID_ARGUMENT`` is reported as ``request_rejected`` so the
  engine can step down; it never steps down silently.
* Errors use ``google.rpc.Status``: a 429 ``RESOURCE_EXHAUSTED`` carries a
  ``QuotaFailure`` whose ``quotaId`` names the window (``...PerMinute...`` vs
  ``...PerDay...``) and a ``RetryInfo.retryDelay`` such as ``"55s"``. An
  invalid key is ``400 INVALID_ARGUMENT`` with ``ErrorInfo.reason ==
  API_KEY_INVALID``, and an unsupported region/account is
  ``FAILED_PRECONDITION``; both are provider-fatal, not model problems.
"""

from __future__ import annotations

import json
import re
import urllib.parse
from typing import TYPE_CHECKING, Any, ClassVar, override

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.providers.base import (
    HttpProviderBase,
    ProviderResult,
    classify_http_status,
    render_schema_instruction,
)
from cyberkb.providers.catalog import ListedModel

if TYPE_CHECKING:
    from collections.abc import Mapping

    from cyberkb.providers.http import HttpResponse

__all__ = ["GOOGLE_MODES", "GoogleProvider", "parse_google_error"]

GOOGLE_MODES: tuple[str, ...] = ("json_schema", "response_schema", "prompt")
_OK = 200
_PAGE_SIZE = 1000
_MAX_PAGES = 20
_GENERATE = "generateContent"
_TEMPERATURE = 0.1
_OK_FINISH = frozenset({None, "STOP"})
_BLOCK_FINISH = frozenset(
    {"SAFETY", "RECITATION", "BLOCKLIST", "PROHIBITED_CONTENT", "SPII", "LANGUAGE"}
)
_DURATION_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)s\s*$")
_ZERO_LIMIT_RE = re.compile(r"\blimit:\s*0\b")
_QUOTA_FAILURE = "type.googleapis.com/google.rpc.QuotaFailure"
_RETRY_INFO = "type.googleapis.com/google.rpc.RetryInfo"
_ERROR_INFO = "type.googleapis.com/google.rpc.ErrorInfo"
_FATAL_REASONS = frozenset({"API_KEY_INVALID", "API_KEY_SERVICE_BLOCKED", "SERVICE_DISABLED"})


def _duration(value: object) -> float | None:
    """Parse a protobuf JSON ``Duration`` (``"55s"``, ``"1.5s"``) into seconds."""
    if not isinstance(value, str):
        return None
    match = _DURATION_RE.match(value)
    return float(match.group(1)) if match else None


def _details(error: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    details = error.get("details")
    if not isinstance(details, list):
        return []
    return [d for d in details if isinstance(d, dict)]


def _quota_ids(details: list[Mapping[str, Any]]) -> list[str]:
    ids: list[str] = []
    for detail in details:
        if detail.get("@type") != _QUOTA_FAILURE:
            continue
        violations = detail.get("violations")
        for violation in violations if isinstance(violations, list) else []:
            quota_id = violation.get("quotaId") if isinstance(violation, dict) else None
            if isinstance(quota_id, str):
                ids.append(quota_id)
    return ids


def parse_google_error(status: int, body: str) -> tuple[FailureCategory, float | None, bool]:
    """Categorise a ``google.rpc.Status`` error body.

    Returns ``(category, retry_after_seconds, request_rejected)``. Falls back to
    the provider-neutral mapping when the body is not the documented shape.
    """
    try:
        envelope = json.loads(body)
    except json.JSONDecodeError:
        envelope = None
    error = envelope.get("error") if isinstance(envelope, dict) else None
    if not isinstance(error, dict):
        return classify_http_status(status, body), None, False
    rpc_status = str(error.get("status", ""))
    message = str(error.get("message", ""))
    details = _details(error)
    retry_after = next(
        (
            d
            for d in (_duration(x.get("retryDelay")) for x in details if x.get("@type") == _RETRY_INFO)
            if d is not None
        ),
        None,
    )
    reasons = {str(d.get("reason")) for d in details if d.get("@type") == _ERROR_INFO}
    if reasons & _FATAL_REASONS or "api key not valid" in message.lower():
        return FailureCategory.AUTH_ERROR, None, False
    if rpc_status in {"PERMISSION_DENIED", "UNAUTHENTICATED", "FAILED_PRECONDITION"}:
        return FailureCategory.AUTH_ERROR, None, False
    if rpc_status == "RESOURCE_EXHAUSTED" or status == 429:  # noqa: PLR2004 - HTTP 429
        quota_ids = _quota_ids(details)
        daily = any("perday" in q.lower() for q in quota_ids) or (
            not quota_ids and "per day" in message.lower()
        )
        if daily or _ZERO_LIMIT_RE.search(message):
            return FailureCategory.QUOTA_EXCEEDED, retry_after, False
        return FailureCategory.RATE_LIMIT, retry_after, False
    if rpc_status == "INVALID_ARGUMENT":
        return FailureCategory.MODEL_UNAVAILABLE, None, True
    if rpc_status == "NOT_FOUND":
        return FailureCategory.MODEL_UNAVAILABLE, None, False
    if rpc_status == "DEADLINE_EXCEEDED":
        return FailureCategory.TIMEOUT, retry_after, False
    return classify_http_status(status, body), retry_after, False


def _json_schema(schema: Mapping[str, object]) -> dict[str, Any]:
    """Drop the Gemini-only ``propertyOrdering`` keyword for standard JSON Schema."""

    def clean(node: object) -> object:
        if isinstance(node, dict):
            return {k: clean(v) for k, v in node.items() if k != "propertyOrdering"}
        if isinstance(node, list):
            return [clean(v) for v in node]
        return node

    cleaned = clean(dict(schema))
    return cleaned if isinstance(cleaned, dict) else {}


class GoogleProvider(HttpProviderBase):
    """Gemini API ``generateContent`` for every Gemini and Gemma model the key reaches."""

    name: ClassVar[str] = "google"
    base_url: ClassVar[str] = "https://generativelanguage.googleapis.com/v1beta"

    def _headers(self, *, json_body: bool) -> dict[str, str]:
        headers = {"x-goog-api-key": self._api_key}
        if json_body:
            headers["Content-Type"] = "application/json"
        return headers

    @override
    def request_modes(self) -> tuple[str, ...]:
        """``json_schema`` → ``response_schema`` → ``prompt``."""
        return GOOGLE_MODES

    @override
    def _error(self, response: HttpResponse, *, model: str | None) -> ProviderError:
        category, retry_after, rejected = parse_google_error(response.status, response.text())
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
        """Walk every page of ``/models`` and keep the ``generateContent`` models."""
        listed: list[ListedModel] = []
        token = ""
        for _ in range(_MAX_PAGES):
            query = {"pageSize": str(_PAGE_SIZE)} | ({"pageToken": token} if token else {})
            url = f"{self.base_url}/models?{urllib.parse.urlencode(query)}"
            page = self._get_mapping(url, headers=self._headers(json_body=False))
            entries = page.get("models")
            for entry in entries if isinstance(entries, list) else []:
                model = _listed(entry)
                if model is not None:
                    listed.append(model)
            next_token = page.get("nextPageToken")
            if not isinstance(next_token, str) or not next_token:
                return listed
            token = next_token
        raise self._fail(
            FailureCategory.UNKNOWN, raw=f"model listing exceeded {_MAX_PAGES} pages"
        )

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
        """One ``generateContent`` call in ``mode``; failures are categorised."""
        body = json.dumps(_request_body(system, prompt, schema, mode, max_output_tokens))
        start = self._clock()
        url = f"{self.base_url}/models/{urllib.parse.quote(model, safe='-._')}:{_GENERATE}"
        response = self._send(
            "POST", url, headers=self._headers(json_body=True), body=body.encode(), model=model
        )
        if response.status != _OK:
            raise self._error(response, model=model)
        envelope = self._decode_object(response.text(), model=model)
        payload = self._decode_model_json(self._answer_text(envelope, model=model), model=model)
        usage = envelope.get("usageMetadata")
        usage = usage if isinstance(usage, dict) else {}
        return ProviderResult(
            payload,
            self.name,
            model,
            self._elapsed(start),
            mode=mode,
            input_tokens=_int(usage.get("promptTokenCount")),
            output_tokens=_sum(usage.get("candidatesTokenCount"), usage.get("thoughtsTokenCount")),
        )

    def _answer_text(self, envelope: Mapping[str, Any], *, model: str) -> str:
        candidates = envelope.get("candidates")
        if not isinstance(candidates, list) or not candidates:
            feedback = envelope.get("promptFeedback")
            block = feedback.get("blockReason") if isinstance(feedback, dict) else None
            category = FailureCategory.CONTENT_FILTER if block else FailureCategory.INFERENCE_ERROR
            raise self._fail(
                category, raw=f"no candidate returned (blockReason={block})", model=model, status=_OK
            )
        candidate = candidates[0] if isinstance(candidates[0], dict) else {}
        finish = candidate.get("finishReason")
        if finish not in _OK_FINISH:
            category = (
                FailureCategory.CONTENT_FILTER
                if finish in _BLOCK_FINISH
                else FailureCategory.INFERENCE_ERROR
            )
            raise self._fail(category, raw=f"finishReason={finish}", model=model, status=_OK)
        content = candidate.get("content")
        parts = content.get("parts") if isinstance(content, dict) else None
        texts = [
            part["text"]
            for part in (parts if isinstance(parts, list) else [])
            if isinstance(part, dict) and isinstance(part.get("text"), str) and not part.get("thought")
        ]
        if not texts:
            self._invalid_output("candidate had no answer text", model=model)
        return "".join(texts)


def _listed(entry: object) -> ListedModel | None:
    if not isinstance(entry, dict):
        return None
    name = entry.get("name")
    methods = entry.get("supportedGenerationMethods")
    if not isinstance(name, str) or not isinstance(methods, list) or _GENERATE not in methods:
        return None
    display = entry.get("displayName")
    return ListedModel(
        id=name.rsplit("/", 1)[-1],
        display_name=display if isinstance(display, str) else None,
        input_token_limit=_int(entry.get("inputTokenLimit")),
        output_token_limit=_int(entry.get("outputTokenLimit")),
    )


def _request_body(
    system: str,
    prompt: str,
    schema: Mapping[str, object],
    mode: str,
    max_output_tokens: int,
) -> dict[str, Any]:
    config: dict[str, Any] = {"temperature": _TEMPERATURE, "maxOutputTokens": max_output_tokens}
    instruction = system
    if mode == "json_schema":
        config |= {"responseMimeType": "application/json", "responseJsonSchema": _json_schema(schema)}
    elif mode == "response_schema":
        config |= {"responseMimeType": "application/json", "responseSchema": dict(schema)}
    elif mode == "prompt":
        instruction = render_schema_instruction(system, schema)
    else:
        msg = f"unknown Google request mode {mode!r}"
        raise ValueError(msg)
    return {
        "systemInstruction": {"parts": [{"text": instruction}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": config,
    }


def _int(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _sum(*values: object) -> int | None:
    numbers = [v for v in (_int(x) for x in values) if v is not None]
    return sum(numbers) if numbers else None
