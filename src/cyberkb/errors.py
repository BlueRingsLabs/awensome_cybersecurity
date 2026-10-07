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
    a generic "failed". The orchestrator also routes on the category: some are
    transient (retry the same model), some mean the model is unusable (rotate to
    the next model), and some are provider-fatal (skip the provider entirely).
    """

    AUTH_ERROR = "auth_error"
    """Invalid or expired key, or missing scope (HTTP 401/403 without a quota signal)."""
    RATE_LIMIT = "rate_limit"
    """Too many requests in a window; usually clears after a short wait (HTTP 429)."""
    QUOTA_EXCEEDED = "quota_exceeded"
    """Billing or plan allowance exhausted; a wait will not help this run."""
    TIMEOUT = "timeout"
    """The request exceeded the configured per-call timeout."""
    SERVER_ERROR = "server_error"
    """The provider returned a 5xx; the fault is on their side."""
    NETWORK_ERROR = "network_error"
    """DNS, TLS, connection refused or no route — the request never completed."""
    INFERENCE_ERROR = "inference_error"
    """The model returned an internal error or output we could not parse."""
    CONTENT_FILTER = "content_filter"
    """The model refused or blocked the content (safety filter)."""
    MODEL_UNAVAILABLE = "model_unavailable"
    """The requested model is missing, deprecated, gated or not yet loaded."""
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
    ) -> None:
        """Store the categorised failure and its diagnostic context."""
        detail = raw.strip() or category.value
        super().__init__(f"{provider}: {category.value}: {detail}")
        self.category = category
        self.provider = provider
        self.model = model
        self.status = status
        self.raw = raw
        self.retry_after = retry_after
