"""Tests for the Google AI Studio adapter against the documented Gemini API shapes."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cyberkb.errors import FailureCategory, ProviderError
from cyberkb.providers.google import GoogleProvider, parse_google_error
from cyberkb.providers.http import HttpResponse, HttpTransportError
from tests.llmfakes import (
    GOOGLE_KEY,
    Router,
    answer,
    google_answer,
    google_error,
    google_listing,
    http,
    quota_failure,
)

SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {"classifications": {"type": "array", "items": {"type": "object"}}},
    "propertyOrdering": ["classifications"],
}

if TYPE_CHECKING:
    from cyberkb.providers.base import ProviderResult


def _provider(router: Router) -> GoogleProvider:
    return GoogleProvider(GOOGLE_KEY, transport=router)


def _call(router: Router, mode: str = "json_schema") -> ProviderResult:
    return _provider(router).complete_json(
        "gemma-t-it", "SYSTEM", "PROMPT", SCHEMA, mode=mode, max_output_tokens=512
    )


def test_listing_walks_every_page_and_keeps_generate_content_models() -> None:
    """Pagination is followed and only generateContent models are candidates."""
    router = Router().add(
        "google:list",
        google_listing(("gemma-t-it", "Gemma Test IT"), next_page="page-2"),
        http(
            200,
            {
                "models": [
                    {"name": "models/embed-1", "supportedGenerationMethods": ["embedContent"]},
                    {"name": "models/gemini-x", "supportedGenerationMethods": ["generateContent"]},
                    "not-a-model",
                    {"supportedGenerationMethods": ["generateContent"]},
                ],
            },
        ),
    )
    listed = _provider(router).list_models()
    assert [m.id for m in listed] == ["gemma-t-it", "gemini-x"]
    assert listed[0].display_name == "Gemma Test IT"
    assert listed[0].input_token_limit == 131072
    assert listed[1].display_name is None
    first_url, second_url = (call[1] for call in router.calls)
    assert "pageSize=1000" in first_url
    assert "pageToken" not in first_url
    assert "pageToken=page-2" in second_url
    headers = router.calls[0][2]
    assert headers == {"x-goog-api-key": GOOGLE_KEY}
    assert GOOGLE_KEY not in first_url


def test_listing_tolerates_a_page_without_models() -> None:
    """A page with no models list yields nothing rather than failing."""
    assert _provider(Router().add("google:list", http(200, {}))).list_models() == []


def test_listing_stops_after_the_page_cap() -> None:
    """A provider that never stops paginating cannot loop forever."""
    router = Router().add("google:list", *[google_listing(next_page="again")] * 20)
    with pytest.raises(ProviderError, match="exceeded 20 pages"):
        _provider(router).list_models()


def test_listing_rejected_key_is_an_auth_error() -> None:
    """An invalid key on the listing is a provider-fatal auth error."""
    router = Router().add(
        "google:list",
        google_error(
            400,
            "INVALID_ARGUMENT",
            "API key not valid. Please pass a valid API key.",
            [{"@type": "type.googleapis.com/google.rpc.ErrorInfo", "reason": "API_KEY_INVALID"}],
        ),
    )
    with pytest.raises(ProviderError) as info:
        _provider(router).list_models()
    assert info.value.category is FailureCategory.AUTH_ERROR


def test_request_modes_are_strongest_first() -> None:
    """Native JSON Schema, then the legacy schema field, then prompt-embedded."""
    assert _provider(Router()).request_modes() == ("json_schema", "response_schema", "prompt")


def test_json_schema_mode_body_and_usage() -> None:
    """json_schema mode sends responseJsonSchema without propertyOrdering."""
    router = Router().add("google:gemma-t-it", google_answer(answer(), output_tokens=60))
    result = _call(router)
    body = router.bodies("google:gemma-t-it")[0]
    config = body["generationConfig"]
    assert config["responseMimeType"] == "application/json"
    assert "propertyOrdering" not in config["responseJsonSchema"]
    assert "responseSchema" not in config
    assert config["maxOutputTokens"] == 512
    assert body["systemInstruction"] == {"parts": [{"text": "SYSTEM"}]}
    assert body["contents"] == [{"role": "user", "parts": [{"text": "PROMPT"}]}]
    assert router.calls[0][1].endswith("/models/gemma-t-it:generateContent")
    assert result.payload == answer()
    assert result.input_tokens == 900
    assert result.output_tokens == 60
    assert result.mode == "json_schema"


def test_response_schema_and_prompt_modes() -> None:
    """The legacy field keeps the schema as-is; prompt mode embeds it in the system text."""
    router = Router().add("google:gemma-t-it", google_answer(answer()), google_answer(answer()))
    _call(router, "response_schema")
    _call(router, "prompt")
    legacy, prompt = router.bodies("google:gemma-t-it")
    assert legacy["generationConfig"]["responseSchema"] == SCHEMA
    assert "responseMimeType" not in prompt["generationConfig"]
    assert '"propertyOrdering"' in prompt["systemInstruction"]["parts"][0]["text"]


def test_unknown_mode_is_a_programming_error() -> None:
    """A mode outside the ladder is rejected before any request is made."""
    router = Router()
    with pytest.raises(ValueError, match="unknown Google request mode"):
        _call(router, "telepathy")
    assert router.calls == []


def test_thought_parts_are_ignored_and_thinking_tokens_counted() -> None:
    """Only answer parts are parsed; thought tokens count as output."""
    envelope = {
        "candidates": [
            {
                "finishReason": "STOP",
                "content": {
                    "parts": [
                        {"text": "let me think {not json", "thought": True},
                        {"text": '{"classifications": []}'},
                    ],
                },
            },
        ],
        "usageMetadata": {
            "promptTokenCount": 10,
            "candidatesTokenCount": 5,
            "thoughtsTokenCount": 7,
        },
    }
    result = _call(Router().add("google:gemma-t-it", http(200, envelope)))
    assert result.payload == {"classifications": []}
    assert result.output_tokens == 12


def test_missing_usage_is_reported_as_unknown() -> None:
    """Absent usage metadata leaves token counts unknown, not zero."""
    result = _call(
        Router().add(
            "google:gemma-t-it", google_answer(answer(), input_tokens=None, output_tokens=None)
        )
    )
    assert result.input_tokens is None
    assert result.output_tokens is None


def test_fenced_and_prefixed_json_is_recovered() -> None:
    """Prompt-mode answers wrapped in a fence or led by prose still parse."""
    router = Router().add(
        "google:gemma-t-it",
        google_answer('```json\n{"classifications": []}\n```'),
        google_answer('Here you go: {"classifications": []} hope it helps'),
    )
    assert _call(router, "prompt").payload == {"classifications": []}
    assert _call(router, "prompt").payload == {"classifications": []}


@pytest.mark.parametrize(
    ("response", "category", "message"),
    [
        (
            http(200, {"promptFeedback": {"blockReason": "SAFETY"}}),
            FailureCategory.CONTENT_FILTER,
            "SAFETY",
        ),
        (http(200, {"candidates": []}), FailureCategory.INFERENCE_ERROR, "no candidate"),
        (google_answer(answer(), finish="SAFETY"), FailureCategory.CONTENT_FILTER, "SAFETY"),
        (
            google_answer(answer(), finish="MAX_TOKENS"),
            FailureCategory.INFERENCE_ERROR,
            "MAX_TOKENS",
        ),
        (http(200, {"candidates": ["junk"]}), FailureCategory.INFERENCE_ERROR, "no answer text"),
        (
            http(200, {"candidates": [{"finishReason": "STOP", "content": {"parts": "x"}}]}),
            FailureCategory.INFERENCE_ERROR,
            "no answer text",
        ),
        (google_answer("no json here"), FailureCategory.INFERENCE_ERROR, "no JSON object"),
        (
            google_answer("{ broken"),
            FailureCategory.INFERENCE_ERROR,
            "invalid JSON in model output",
        ),
        (google_answer("[1, 2]"), FailureCategory.INFERENCE_ERROR, "not a JSON object"),
        (HttpResponse(200, b"<html>"), FailureCategory.INFERENCE_ERROR, "invalid JSON"),
        (http(200, [1]), FailureCategory.INFERENCE_ERROR, "not a JSON object"),
    ],
)
def test_unusable_answers_are_categorised(
    response: HttpResponse, category: FailureCategory, message: str
) -> None:
    """Blocked, truncated or non-JSON answers raise the right category."""
    with pytest.raises(ProviderError, match=message) as info:
        _call(Router().add("google:gemma-t-it", response))
    assert info.value.category is category


def test_transport_faults_are_categorised() -> None:
    """A timeout and a network failure map to their categories."""
    router = Router().add(
        "google:gemma-t-it",
        HttpTransportError("timed out", timeout=True),
        HttpTransportError("refused", timeout=False),
    )
    with pytest.raises(ProviderError) as first:
        _call(router)
    with pytest.raises(ProviderError) as second:
        _call(router)
    assert first.value.category is FailureCategory.TIMEOUT
    assert second.value.category is FailureCategory.NETWORK_ERROR


def test_error_bodies_never_carry_the_key() -> None:
    """Even if a provider echoed the key, the captured error text is redacted."""
    router = Router().add(
        "google:gemma-t-it", google_error(500, "INTERNAL", f"key {GOOGLE_KEY} broke")
    )
    with pytest.raises(ProviderError) as info:
        _call(router)
    assert GOOGLE_KEY not in info.value.raw
    assert "[REDACTED]" in info.value.raw
    assert info.value.category is FailureCategory.SERVER_ERROR


@pytest.mark.parametrize(
    ("status", "rpc", "message", "details", "expected"),
    [
        (
            429,
            "RESOURCE_EXHAUSTED",
            "You exceeded your current quota",
            quota_failure("GenerateRequestsPerMinutePerProjectPerModel-FreeTier", retry="55s"),
            (FailureCategory.RATE_LIMIT, 55.0, False),
        ),
        (
            429,
            "RESOURCE_EXHAUSTED",
            "You exceeded your current quota",
            quota_failure(
                "GenerateRequestsPerMinutePerProjectPerModel-FreeTier",
                "GenerateRequestsPerDayPerProjectPerModel-FreeTier",
                retry="1.5s",
            ),
            (FailureCategory.QUOTA_EXCEEDED, 1.5, False),
        ),
        (
            429,
            "RESOURCE_EXHAUSTED",
            "Quota exceeded for metric x, limit: 0, model: gemini-x",
            quota_failure("GenerateContentInputTokensPerModelPerMinute-FreeTier"),
            (FailureCategory.QUOTA_EXCEEDED, None, False),
        ),
        (
            429,
            "RESOURCE_EXHAUSTED",
            "quota exceeded per day",
            (),
            (FailureCategory.QUOTA_EXCEEDED, None, False),
        ),
        (
            429,
            "RESOURCE_EXHAUSTED",
            "slow down",
            [{"@type": "x"}],
            (FailureCategory.RATE_LIMIT, None, False),
        ),
        (
            429,
            "RESOURCE_EXHAUSTED",
            "slow down",
            [{"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "soon"}],
            (FailureCategory.RATE_LIMIT, None, False),
        ),
        (
            429,
            "RESOURCE_EXHAUSTED",
            "slow down",
            [{"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": {"seconds": 5}}],
            (FailureCategory.RATE_LIMIT, None, False),
        ),
        (
            429,
            "RESOURCE_EXHAUSTED",
            "slow down",
            [{"@type": "type.googleapis.com/google.rpc.QuotaFailure", "violations": "x"}],
            (FailureCategory.RATE_LIMIT, None, False),
        ),
        (
            429,
            "RESOURCE_EXHAUSTED",
            "slow down",
            [{"@type": "type.googleapis.com/google.rpc.QuotaFailure", "violations": ["x", {}]}],
            (FailureCategory.RATE_LIMIT, None, False),
        ),
        (403, "PERMISSION_DENIED", "denied", (), (FailureCategory.AUTH_ERROR, None, False)),
        (
            400,
            "FAILED_PRECONDITION",
            "User location is not supported for the API use.",
            (),
            (FailureCategory.AUTH_ERROR, None, False),
        ),
        (
            403,
            "PERMISSION_DENIED",
            "blocked",
            [{"@type": "type.googleapis.com/google.rpc.ErrorInfo", "reason": "SERVICE_DISABLED"}],
            (FailureCategory.AUTH_ERROR, None, False),
        ),
        (
            400,
            "INVALID_ARGUMENT",
            "Request contains an invalid argument.",
            (),
            (FailureCategory.MODEL_UNAVAILABLE, None, True),
        ),
        (
            404,
            "NOT_FOUND",
            "models/x is not found",
            (),
            (FailureCategory.MODEL_UNAVAILABLE, None, False),
        ),
        (504, "DEADLINE_EXCEEDED", "deadline", (), (FailureCategory.TIMEOUT, None, False)),
        (503, "UNAVAILABLE", "high demand", (), (FailureCategory.SERVER_ERROR, None, False)),
    ],
)
def test_google_rpc_errors_are_categorised(
    status: int,
    rpc: str,
    message: str,
    details: list[dict[str, object]],
    expected: tuple[FailureCategory, float | None, bool],
) -> None:
    """Every documented error shape maps to the right category, delay and rejection flag."""
    body = google_error(status, rpc, message, details).text()
    assert parse_google_error(status, body) == expected


def test_non_rpc_error_bodies_fall_back_to_the_status() -> None:
    """A body that is not google.rpc.Status is categorised by HTTP status alone."""
    assert parse_google_error(503, "<html>busy</html>") == (
        FailureCategory.SERVER_ERROR,
        None,
        False,
    )
    assert parse_google_error(429, '{"error": "x"}') == (FailureCategory.RATE_LIMIT, None, False)
    assert parse_google_error(418, '{"error": {"details": "x"}}')[0] is FailureCategory.UNKNOWN


def test_rejected_request_is_flagged_on_the_raised_error() -> None:
    """An INVALID_ARGUMENT on a call marks the error as a rejected request mode."""
    router = Router().add("google:gemma-t-it", google_error(400, "INVALID_ARGUMENT", "bad field"))
    with pytest.raises(ProviderError) as info:
        _call(router)
    assert info.value.request_rejected is True
    assert info.value.status == 400
    assert info.value.model == "gemma-t-it"


def test_retry_delay_reaches_the_raised_error() -> None:
    """The RetryInfo delay is surfaced as retry_after."""
    router = Router().add(
        "google:gemma-t-it",
        google_error(429, "RESOURCE_EXHAUSTED", "q", quota_failure("PerMinute", retry="7s")),
    )
    with pytest.raises(ProviderError) as info:
        _call(router)
    assert info.value.retry_after == 7.0
    assert info.value.category is FailureCategory.RATE_LIMIT


def test_configured_only_with_a_key() -> None:
    """An empty key means not configured."""
    assert GoogleProvider(GOOGLE_KEY).is_configured()
    assert not GoogleProvider("").is_configured()


def test_short_keys_are_not_redacted() -> None:
    """Placeholder keys shorter than a real secret do not mangle error text."""
    provider = GoogleProvider("key", transport=Router())
    assert provider.redact("API key not valid") == "API key not valid"


def test_the_test_network_refuses_unknown_hosts() -> None:
    """The HTTP double only answers the two verified provider hosts."""
    with pytest.raises(AssertionError, match="unexpected host"):
        Router().request(
            "GET",
            "https://generativelanguage.googleapis.com.evil.example/v1beta/models",
            headers={},
            body=None,
            timeout=1,
        )
