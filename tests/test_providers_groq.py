"""Tests for the Groq adapter against the documented OpenAI-compatible shapes."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.providers.groq import GroqProvider, strict_schema
from cyberkb.providers.http import HttpResponse
from tests.llmfakes import GROQ_KEY, Router, answer, groq_answer, groq_error, http

SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "classifications": {
            "type": "array",
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    "tags": {"type": "array", "items": {"type": "string"}, "maxItems": 6}
                },
                "propertyOrdering": ["tags"],
            },
        },
    },
}

if TYPE_CHECKING:
    from cyberkb.providers.base import ProviderResult


def _provider(router: Router) -> GroqProvider:
    return GroqProvider(GROQ_KEY, transport=router)


def _call(router: Router, mode: str = "json_schema") -> ProviderResult:
    return _provider(router).complete_json(
        "groq-a", "SYSTEM", "PROMPT", SCHEMA, mode=mode, max_output_tokens=256
    )


def test_listing_keeps_active_models_with_their_context_window() -> None:
    """Inactive and malformed entries are dropped; the context window is shared."""
    router = Router().add(
        "groq:list",
        http(
            200,
            {
                "data": [
                    {
                        "id": "groq-a",
                        "active": True,
                        "context_window": 4096,
                        "max_completion_tokens": 1024,
                    },
                    {"id": "retired", "active": False},
                    {"id": "no-window"},
                    {"active": True},
                    "junk",
                ],
            },
        ),
    )
    listed = _provider(router).list_models()
    assert [m.id for m in listed] == ["groq-a", "no-window"]
    assert listed[0].input_token_limit == 4096
    assert listed[0].output_token_limit == 1024
    assert listed[0].shared_context is True
    assert listed[1].input_token_limit is None
    assert router.calls[0][2] == {"Authorization": f"Bearer {GROQ_KEY}"}


def test_listing_without_data_is_empty() -> None:
    """A listing with no data array yields no models."""
    assert _provider(Router().add("groq:list", http(200, {"object": "list"}))).list_models() == []


def test_listing_auth_failure() -> None:
    """A rejected key on the listing is an auth error."""
    router = Router().add("groq:list", groq_error(401, "Invalid API Key", code="invalid_api_key"))
    with pytest.raises(ProviderError) as info:
        _provider(router).list_models()
    assert info.value.category is FailureCategory.AUTH_ERROR


def test_strict_schema_closes_objects_and_drops_unsupported_keywords() -> None:
    """Strict mode needs additionalProperties: false everywhere and no maxItems."""
    adapted = strict_schema(SCHEMA)
    assert adapted["additionalProperties"] is False
    array = adapted["properties"]["classifications"]
    assert "maxItems" not in array
    inner = array["items"]
    assert inner["additionalProperties"] is False
    assert "propertyOrdering" not in inner
    assert "maxItems" not in inner["properties"]["tags"]


def test_strict_json_schema_mode_request() -> None:
    """json_schema mode sends a strict, named schema and the plain system prompt."""
    router = Router().add("groq:groq-a", groq_answer(answer(), remaining=41))
    result = _call(router)
    body = router.bodies("groq:groq-a")[0]
    assert body["response_format"]["type"] == "json_schema"
    assert body["response_format"]["json_schema"]["strict"] is True
    assert body["messages"][0] == {"role": "system", "content": "SYSTEM"}
    assert body["max_completion_tokens"] == 256
    assert result.payload == answer()
    assert result.input_tokens == 900
    assert result.output_tokens == 80
    assert result.remaining_requests == 41
    assert result.mode == "json_schema"


def test_json_object_mode_embeds_the_schema() -> None:
    """json_object mode asks for JSON in the system prompt, with the schema inline."""
    router = Router().add("groq:groq-a", groq_answer(answer()))
    result = _call(router, "json_object")
    body = router.bodies("groq:groq-a")[0]
    assert body["response_format"] == {"type": "json_object"}
    assert "JSON schema" in body["messages"][0]["content"]
    assert result.remaining_requests is None


def test_unknown_mode_is_a_programming_error() -> None:
    """A mode outside the ladder is rejected before any request."""
    with pytest.raises(ValueError, match="unknown Groq request mode"):
        _call(Router(), "xml")


def test_reasoning_blocks_are_stripped_before_parsing() -> None:
    """A <think> block (raw reasoning) never reaches the JSON parser."""
    content = '<think>maybe {"classifications": "no"}</think>\n{"classifications": []}'
    result = _call(Router().add("groq:groq-a", groq_answer(content)))
    assert result.payload == {"classifications": []}


def test_usage_and_rate_headers_are_optional() -> None:
    """Missing usage or a malformed header leaves the values unknown."""
    response = http(
        200,
        {"choices": [{"message": {"content": "{}"}}]},
        {"X-RateLimit-Remaining-Requests": "lots"},
    )
    result = _call(Router().add("groq:groq-a", response))
    assert result.input_tokens is None
    assert result.output_tokens is None
    assert result.remaining_requests is None


@pytest.mark.parametrize(
    ("response", "category", "message"),
    [
        (http(200, {"choices": []}), FailureCategory.INFERENCE_ERROR, "no choices"),
        (http(200, {"choices": ["x"]}), FailureCategory.INFERENCE_ERROR, "no content"),
        (groq_answer("{}", finish="content_filter"), FailureCategory.CONTENT_FILTER, "filtered"),
        (
            http(200, {"choices": [{"message": {"content": "  "}}]}),
            FailureCategory.INFERENCE_ERROR,
            "no content",
        ),
    ],
)
def test_unusable_answers(response: HttpResponse, category: FailureCategory, message: str) -> None:
    """Empty, filtered or choice-less answers raise the right category."""
    with pytest.raises(ProviderError, match=message) as info:
        _call(Router().add("groq:groq-a", response))
    assert info.value.category is category


def _error(response: HttpResponse) -> ProviderError:
    with pytest.raises(ProviderError) as info:
        _call(Router().add("groq:groq-a", response))
    return info.value


def test_per_minute_rate_limit_carries_retry_after() -> None:
    """A TPM 429 is a short-window rate limit with the server's delay."""
    error = _error(
        groq_error(
            429,
            "Rate limit reached for model `groq-a` on tokens per minute (TPM): Limit 6000",
            code="rate_limit_exceeded",
            headers={"retry-after": "7", "x-ratelimit-remaining-requests": "500"},
        ),
    )
    assert error.category is FailureCategory.RATE_LIMIT
    assert error.retry_after == 7.0


@pytest.mark.parametrize(
    ("message", "headers"),
    [
        ("Rate limit reached on requests per day (RPD): Limit 1000", {}),
        ("Rate limit reached on tokens per day (TPD): Limit 200000", {}),
        ("Rate limit reached", {"x-ratelimit-remaining-requests": "0"}),
    ],
)
def test_daily_limits_are_quota_exhaustion(message: str, headers: dict[str, str]) -> None:
    """RPD/TPD windows (by message or by an empty request allowance) exhaust the model."""
    error = _error(groq_error(429, message, code="rate_limit_exceeded", headers=headers))
    assert error.category is FailureCategory.QUOTA_EXCEEDED


def test_json_validation_failure_is_an_inference_error() -> None:
    """json_validate_failed is the model's bad output, not a malformed request."""
    error = _error(groq_error(400, "Failed to generate JSON", code="json_validate_failed"))
    assert error.category is FailureCategory.INFERENCE_ERROR
    assert error.request_rejected is False


def test_decommissioned_model_is_unavailable_not_rejected() -> None:
    """A retired model is unavailable; no mode change can help."""
    error = _error(groq_error(400, "decommissioned", code="model_decommissioned"))
    assert error.category is FailureCategory.MODEL_UNAVAILABLE
    assert error.request_rejected is False


def test_other_bad_requests_are_rejected_request_modes() -> None:
    """A plain 400 (e.g. unsupported response_format) lets validation step down."""
    error = _error(groq_error(400, "response_format json_schema is not supported"))
    assert error.category is FailureCategory.MODEL_UNAVAILABLE
    assert error.request_rejected is True


@pytest.mark.parametrize(
    ("status", "body", "category"),
    [
        (
            404,
            '{"error": {"message": "x", "code": "model_not_found"}}',
            FailureCategory.MODEL_UNAVAILABLE,
        ),
        (413, "too large", FailureCategory.MODEL_UNAVAILABLE),
        (422, '{"error": "x"}', FailureCategory.INFERENCE_ERROR),
        (498, '"flex"', FailureCategory.SERVER_ERROR),
        (418, "teapot", FailureCategory.UNKNOWN),
        (503, '{"error": {"message": null}}', FailureCategory.SERVER_ERROR),
    ],
)
def test_remaining_statuses(status: int, body: str, category: FailureCategory) -> None:
    """Other statuses use the provider-neutral mapping, whatever the body shape."""
    assert _error(HttpResponse(status, body.encode())).category is category


def test_an_edge_block_is_not_a_key_rejection() -> None:
    """Cloudflare's bare 403 (error 1010) never reached the API: network, not auth."""
    error = _error(HttpResponse(403, b"error code: 1010\n"))
    assert error.category is FailureCategory.NETWORK_ERROR
    api = _error(groq_error(403, "Organization restricted", code="permission_denied"))
    assert api.category is FailureCategory.AUTH_ERROR
