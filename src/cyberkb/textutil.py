"""Text normalisation primitives shared by every stage of the pipeline.

All functions are pure, total (they never raise on arbitrary ``str`` input)
and linear-time, so they are safe to run on untrusted contributor content.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter

__all__ = [
    "BIDI_CONTROLS",
    "fold",
    "ngram_counts",
    "phrase_tokens",
    "plain_text",
    "slugify",
    "strip_unsafe_chars",
    "tokenize",
    "truncate",
    "unfence",
    "word_count",
]

# Explicit bidirectional formatting characters, listed by code point so the
# source itself stays free of control characters. They have no business in a
# technical knowledge base and are the vehicle of "Trojan Source" style
# deception (CVE-2021-42574), so they are removed from every stored text.
BIDI_CONTROLS = frozenset(
    chr(cp)
    for cp in (
        0x061C,
        0x200E,
        0x200F,
        0x202A,
        0x202B,
        0x202C,
        0x202D,
        0x202E,
        0x2066,
        0x2067,
        0x2068,
        0x2069,
    )
)
_UNSAFE_TRANSLATION = {ord(ch): None for ch in BIDI_CONTROLS} | {0xFEFF: None}
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
_TOKEN_RE = re.compile(r"[a-z0-9]+")
_WORD_RE = re.compile(r"\w+", re.UNICODE)
_SLUG_SEP_RE = re.compile(r"[^a-z0-9]+")
_WS_RE = re.compile(r"\s+")

# Inline Markdown / HTML constructs that must never leak into plain-text
# fields (titles, summaries) rendered inside tables or consumed by APIs.
_MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_HTML_TAG_RE = re.compile(r"<[^>]{0,500}>")
_URL_RE = re.compile(r"\b(?:https?|ftp)://\S+", re.IGNORECASE)
_MD_EMPHASIS_RE = re.compile(r"[*_`~#>|]+")


def strip_unsafe_chars(text: str) -> str:
    """Remove C0/C1 control characters (except tab/newline/CR), bidi controls and BOMs."""
    return _CONTROL_RE.sub("", text.translate(_UNSAFE_TRANSLATION))


def fold(text: str) -> str:
    """Accent-fold and case-fold ``text`` to lowercase ASCII."""
    decomposed = unicodedata.normalize("NFKD", text)
    return decomposed.encode("ascii", "ignore").decode("ascii").casefold()


def tokenize(text: str) -> list[str]:
    """Split folded text into ``[a-z0-9]+`` tokens.

    ``"Active_Directory"``, ``"active-directory"`` and ``"Active Directory"``
    all produce ``["active", "directory"]``.
    """
    return _TOKEN_RE.findall(fold(text))


def phrase_tokens(phrase: str) -> tuple[str, ...]:
    """Tokenise a keyword phrase into the tuple form used for n-gram lookups."""
    return tuple(tokenize(phrase))


def ngram_counts(tokens: list[str], max_n: int = 4) -> Counter[tuple[str, ...]]:
    """Count every n-gram of length ``1..max_n`` in ``tokens``."""
    counts: Counter[tuple[str, ...]] = Counter()
    length = len(tokens)
    for n in range(1, max_n + 1):
        for i in range(length - n + 1):
            counts[tuple(tokens[i : i + n])] += 1
    return counts


def slugify(text: str, max_len: int = 80) -> str:
    """Return a lowercase ASCII kebab-case slug, never empty, at most ``max_len`` chars."""
    slug = _SLUG_SEP_RE.sub("-", fold(text)).strip("-") or "untitled"
    if len(slug) > max_len:
        # ``slug`` starts with a non-separator, so ``cut`` does too; cutting at
        # a back-half word boundary (or hard-cutting) therefore stays non-empty.
        cut = slug[:max_len]
        boundary = cut.rfind("-")
        slug = (cut[:boundary] if boundary > max_len // 2 else cut).rstrip("-")
    return slug


def truncate(text: str, max_len: int) -> str:
    """Truncate at a word boundary, appending an ellipsis when shortened."""
    if len(text) <= max_len:
        return text
    cut = text[: max_len - 1]
    boundary = cut.rfind(" ")
    if boundary > max_len // 2:
        cut = cut[:boundary]
    return cut.rstrip(" ,;:.-") + "…"


def plain_text(text: str, max_len: int | None = None) -> str:
    """Reduce untrusted Markdown/HTML to a single safe line of plain text.

    Links keep their label, images keep their alt text, raw URLs, HTML tags,
    emphasis markers, table pipes, control and bidi characters are dropped,
    and whitespace collapses to single spaces.
    """
    out = strip_unsafe_chars(unicodedata.normalize("NFC", text))
    out = _MD_IMAGE_RE.sub(r"\1", out)
    out = _MD_LINK_RE.sub(r"\1", out)
    out = _HTML_TAG_RE.sub(" ", out)
    out = _URL_RE.sub(" ", out)
    out = _MD_EMPHASIS_RE.sub(" ", out)
    out = out.replace("[", " ").replace("]", " ")
    out = _WS_RE.sub(" ", out).strip()
    if max_len is not None:
        out = truncate(out, max_len)
    return out


def word_count(text: str) -> int:
    """Count Unicode word tokens (letters, digits, underscore runs)."""
    return len(_WORD_RE.findall(text))


def unfence(text: str) -> str:
    """Strip one surrounding Markdown code fence (```json ... ``` or ``` ... ```).

    Models asked for bare JSON still often wrap it in a fence. Only a fence
    that opens the (stripped) text is removed; the closing fence is optional
    so a truncated answer still yields its body.
    """
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    end = len(lines) - 1 if len(lines) > 1 and lines[-1].strip() == "```" else len(lines)
    return "\n".join(lines[1:end]).strip()
