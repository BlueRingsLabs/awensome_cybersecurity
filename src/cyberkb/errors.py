"""Exception hierarchy.

Every error raised on purpose by cyberkb derives from :class:`KBError`, so the
CLI can tell expected failures (bad input, policy violations, unavailable
services) from programming errors and map them to stable exit codes.
"""

from __future__ import annotations


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
    """Base class for classification-service failures."""


class LLMRetryableError(LLMError):
    """Transient failure: rate limit, overload, timeout or network error."""

    def __init__(self, message: str, *, retry_after: float | None = None) -> None:
        """Store an optional server-provided retry delay (seconds)."""
        super().__init__(message)
        self.retry_after = retry_after


class LLMModelError(LLMError):
    """The model rejected the request (unknown model, unsupported feature).

    The next model in the fallback chain may still succeed.
    """


class LLMFatalError(LLMError):
    """Failure that no retry or model switch can fix (auth, exhausted daily quota)."""


class LLMResponseError(LLMError):
    """The model answered, but the answer is unusable (truncated, blocked, invalid JSON)."""
