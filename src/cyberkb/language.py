"""Dependency-free language identification for en / es / pt.

The library is overwhelmingly English and Portuguese with some Spanish. A
stop-word profile is accurate for documents of this length, deterministic,
and needs no model download. v1 used a filename check that mapped ``_es``
to Portuguese and a handful of substrings shared by Spanish and Portuguese.
"""

from __future__ import annotations

import re

__all__ = ["detect_language"]

_WORD_RE = re.compile(r"[a-zà-öø-ÿ]+", re.IGNORECASE)

# High-frequency function words that are *distinctive* for each language.
# Words common to Spanish and Portuguese ("de", "que", "para", "como", "a")
# are intentionally excluded: they add mass but no signal.
_PROFILES: dict[str, frozenset[str]] = {
    "en": frozenset(
        [
            "the",
            "and",
            "of",
            "to",
            "is",
            "in",
            "that",
            "it",
            "for",
            "with",
            "as",
            "on",
            "are",
            "this",
            "be",
            "by",
            "you",
            "can",
            "from",
            "or",
            "an",
            "at",
            "not",
            "have",
            "will",
            "your",
            "which",
            "their",
            "they",
            "we",
            "these",
            "was",
            "has",
            "but",
            "if",
            "all",
            "more",
            "when",
            "how",
            "what",
            "use",
            "using",
            "also",
            "into",
            "such",
        ],
    ),
    "es": frozenset(
        [
            "el",
            "los",
            "las",
            "del",
            "y",
            "es",
            "en",
            "por",
            "una",
            "con",
            "se",
            "su",
            "al",
            "lo",
            "pero",
            "más",
            "son",
            "también",
            "puede",
            "sus",
            "hay",
            "muy",
            "desde",
            "cuando",
            "todo",
            "hasta",
            "donde",
            "nuestro",
            "usted",
            "ellos",
            "tiene",
            "sin",
            "otro",
        ],
    ),
    "pt": frozenset(
        [
            "o",
            "os",
            "do",
            "da",
            "dos",
            "das",
            "e",
            "é",
            "em",
            "um",
            "uma",
            "com",
            "não",
            "ao",
            "no",
            "na",
            "nos",
            "nas",
            "pelo",
            "pela",
            "mais",
            "também",
            "são",
            "você",
            "seu",
            "sua",
            "isso",
            "pode",
            "muito",
            "quando",
            "até",
            "onde",
            "nosso",
            "ele",
            "eles",
            "tem",
            "sem",
            "outro",
        ],
    ),
}
_MIN_HITS = 8
_MIN_SHARE = 0.45


def detect_language(text: str, *, sample_chars: int = 20_000) -> str:
    """Return ``"en"``, ``"es"``, ``"pt"`` or ``"und"`` for ``text``.

    The winner must have at least ``_MIN_HITS`` stop-word hits and at least
    ``_MIN_SHARE`` of all hits; otherwise the language is undetermined.
    """
    words = _WORD_RE.findall(text[:sample_chars].lower())
    scores = {lang: sum(1 for w in words if w in profile) for lang, profile in _PROFILES.items()}
    total = sum(scores.values())
    best = max(scores, key=lambda lang: (scores[lang], lang == "en"))
    if scores[best] < _MIN_HITS or scores[best] / total < _MIN_SHARE:
        return "und"
    return best
