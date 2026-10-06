"""Build the ``classified_by`` provenance stamp for a resource.

The stamp records which engine produced a classification and when, in the
format the front matter validates: ``<provider>[:<model>]@<ISO-8601 UTC>`` for
an LLM (e.g. ``gemini:gemini-2.5-flash@2026-10-05T14:23:11Z``), and
``<method>@<ISO-8601 UTC>`` for the heuristic or a manual decision.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cyberkb.obslog import utc_now_iso

if TYPE_CHECKING:
    from datetime import datetime

    from cyberkb.frontmatter import ClassificationMethod

__all__ = ["classified_by"]


def classified_by(
    method: ClassificationMethod,
    *,
    provider: str | None = None,
    model: str | None = None,
    moment: datetime | None = None,
) -> str | None:
    """Return the provenance stamp for a classification, or ``None`` if indeterminate."""
    stamp = utc_now_iso(moment)
    if method == "llm" and provider and model:
        return f"{provider}:{model}@{stamp}"
    if method in ("heuristic", "manual"):
        return f"{method}@{stamp}"
    return None
