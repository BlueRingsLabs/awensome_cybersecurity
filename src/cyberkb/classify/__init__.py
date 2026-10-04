"""Classification of resources into the taxonomy.

Two interchangeable engines share one result type:

* :mod:`cyberkb.classify.heuristic` -- deterministic, offline, explainable;
  always available, used for previews, as fallback and as a sanity check.
* :mod:`cyberkb.classify.llm` -- Gemini with schema-constrained output for
  higher accuracy and summaries when an API key is configured.
"""

from __future__ import annotations

from cyberkb.classify.base import ClassificationResult, Document

__all__ = ["ClassificationResult", "Document"]
