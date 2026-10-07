"""Exception hierarchy.

Every error raised on purpose by cyberkb derives from :class:`KBError`, so the
CLI can tell expected failures (bad input, policy violations, unavailable
services) from programming errors and map them to stable exit codes.
"""

from __future__ import annotations

from enum import StrEnum


class KBError(Exception):
    """Base class for all expected cyberkb failures."""


class TaxonomyError(KBError):
    """The taxonomy file is missing or structurally invalid."""


class FrontMatterError(KBError):
    """A document's YAML front matter cannot be parsed or fails validation."""


class UnsafePathError(KBError):
    """A path is a symlink, escapes the repository, or is not a regular file."""


class ContentRejectedError(KBError):
    """A submission violates content policy (size, binary data, emptiness)."""


class LLMError(KBError):
    """Base class for classification-service failures (see :class:`ProviderError`)."""


class ModelCatalogError(KBError):
    """``schema/llm-models.yaml`` is missing, malformed or contradicts a provider."""


class ProviderConfigError(LLMError):
    """A required provider key is missing or rejected; the run must not start."""


class FailureCategory(StrEnum):
    """A categorised cause for a single provider failure.

    Every provider call that fails is tagged with exactly one of these, so the
    structured logs and the end-of-run report carry a precise cause rather than
    a generic "failed". The rotation engine routes on the category (ADR-0008):
    errors are retried on the same model, a rate limit moves the request to the
    next model while the limited one cools down, a spent daily quota retires
    the model for the day, and an auth failure takes the whole provider out.
    """

    AUTH_ERROR = "auth_error"
    """The account cannot use the API: rejected or revoked key, missing permission,
    disabled service or unsupported region (401/403, FAILED_PRECONDITION). Provider-fatal."""
    RATE_LIMIT = "rate_limit"
    """A short-window limit (RPM/TPM) was hit; clears within a minute (HTTP 429)."""
    QUOTA_EXCEEDED = "quota_exceeded"
    """A model's daily allowance (RPD/TPD) or plan allowance is spent; retired until reset."""
    TIMEOUT = "timeout"
    """The request exceeded the configured per-call timeout."""
    SERVER_ERROR = "server_error"
    """The provider returned a 5xx (or a capacity signal); the fault is on their side."""
    NETWORK_ERROR = "network_error"
    """DNS, TLS, connection refused or no route — the request never completed."""
    INFERENCE_ERROR = "inference_error"
    """The model answered, but not usably: unparseable, off-taxonomy or a refusal."""
    CONTENT_FILTER = "content_filter"
    """The model refused or blocked the content (safety filter)."""
    MODEL_UNAVAILABLE = "model_unavailable"
    """The model is missing or retired, rejects the request shape, or cannot take its size."""
    UNKNOWN = "unknown"
    """Anything else; the raw provider error is always retained for triage."""


class ProviderError(LLMError):
    """A categorised failure from one LLM provider call, with full context.

    Carries everything the structured logger and run report need: the category,
    the provider and model involved, the HTTP status (when there was one), the
    verbatim provider error text, and any server-advised retry delay. The raw
    text is the provider's own response body, never request headers, so an API
    key can never be captured here.
    """

    def __init__(
        self,
        category: FailureCategory,
        *,
        provider: str,
        model: str | None = None,
        status: int | None = None,
        raw: str = "",
        retry_after: float | None = None,
        request_rejected: bool = False,
    ) -> None:
        """Store the categorised failure and its diagnostic context.

        ``request_rejected`` marks a request the provider refused as malformed
        for this model (e.g. a structured-output field it does not support), as
        opposed to a model it does not serve: validation may then retry the
        same model with a simpler request mode.
        """
        detail = raw.strip() or category.value
        super().__init__(f"{provider}: {category.value}: {detail}")
        self.category = category
        self.provider = provider
        self.model = model
        self.status = status
        self.raw = raw
        self.retry_after = retry_after
        self.request_rejected = request_rejected
