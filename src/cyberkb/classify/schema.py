"""The structured-output schema and prompt handed to the LLM classifier.

Building the schema from the live taxonomy guarantees the model can only
return categories, formats and languages that actually exist, so a
hallucinated label is impossible by construction rather than caught after
the fact.

Tags are the exception, deliberately. The Gemini API rejects the schema with
``400 INVALID_ARGUMENT`` when the tag array's items carry the full vocabulary
as an ``enum`` (verified against the live API on 2026-10-07: the identical
schema without that one enum is accepted, in both ``responseSchema`` and
``responseJsonSchema``). The vocabulary is therefore given in the system
instruction instead, and every returned tag is filtered against the taxonomy
by the classifier, so an invented tag is still dropped, never stored.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from cyberkb.taxonomy import Taxonomy

__all__ = ["MAX_SAMPLE_CHARS", "MAX_TAGS", "build_prompt", "response_schema", "system_instruction"]

MAX_SAMPLE_CHARS = 6000
MAX_TAGS = 6


def response_schema(taxonomy: Taxonomy) -> dict[str, Any]:
    """The JSON schema every provider is asked to answer in (see the module docstring)."""
    item = {
        "type": "object",
        "properties": {
            "ref": {"type": "string"},
            "title": {"type": "string"},
            "category": {"type": "string", "enum": list(taxonomy.category_ids)},
            "format": {"type": "string", "enum": list(taxonomy.format_ids)},
            "language": {"type": "string", "enum": list(taxonomy.language_ids)},
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": MAX_TAGS,
            },
            "summary": {"type": "string"},
            "confidence": {"type": "number"},
        },
        "required": [
            "ref",
            "title",
            "category",
            "format",
            "language",
            "tags",
            "summary",
            "confidence",
        ],
        "propertyOrdering": [
            "ref",
            "title",
            "category",
            "format",
            "language",
            "tags",
            "summary",
            "confidence",
        ],
    }
    return {
        "type": "object",
        "properties": {"classifications": {"type": "array", "items": item}},
        "required": ["classifications"],
    }


def system_instruction(taxonomy: Taxonomy) -> str:
    """System prompt describing the taxonomy and the librarian's rules."""
    categories = "\n".join(
        f"- {c.id}: {c.name} -- {c.description.strip()}"
        for c in taxonomy.categories
        if not c.staging
    )
    formats = "\n".join(f"- {f.id}: {f.description or f.name}" for f in taxonomy.formats)
    return (
        "You are the cataloguing librarian of the BlueRingsLabs "
        "awesome_cybersecurity knowledge base. Classify each cybersecurity "
        "document into exactly one category and one format, detect its "
        "language, write a concise neutral one-sentence summary and choose up "
        f"to {MAX_TAGS} tags from the controlled vocabulary.\n\n"
        f"CATEGORIES:\n{categories}\n\n"
        f"FORMATS:\n{formats}\n\n"
        "RULES:\n"
        "- Echo each document's ref exactly as given.\n"
        "- title: the document's real title, max 200 characters, no Markdown.\n"
        "- summary: one neutral sentence, max 300 characters, no marketing tone.\n"
        "- language: en, es, pt, or und when undetermined.\n"
        "- tags: only ids from the provided vocabulary; pick the most specific.\n"
        "- confidence: your calibrated certainty in the category, 0.0 to 1.0.\n"
        "- Classify only from the provided text; never invent facts.\n"
        f"TAG VOCABULARY: {', '.join(taxonomy.tag_ids)}"
    )


def build_prompt(
    documents: list[tuple[str, str, str]], *, max_chars: int = MAX_SAMPLE_CHARS
) -> str:
    """Render the user prompt for a batch of ``(ref, stem, body)`` documents.

    Each body is cut to ``max_chars`` (at most :data:`MAX_SAMPLE_CHARS`), so the
    rotation engine can shrink a request to fit a small model's limits.
    """
    limit = min(max_chars, MAX_SAMPLE_CHARS)
    parts = [
        "Classify these documents. Return one object per document, echoing ref exactly.",
        "",
    ]
    for ref, stem, body in documents:
        parts.append(f"<document ref={json.dumps(ref)} filename={json.dumps(stem)}>")
        parts.append(body[:limit])
        parts.append("</document>")
        parts.append("")
    return "\n".join(parts)
