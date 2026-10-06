"""Best-effort author extraction from resource bodies.

Authorship in this corpus is declared inconsistently: a byline ("By Jane Doe"),
a bare name under the title, a LinkedIn handle, or nothing at all. This module
extracts a credible author deterministically where the text states one, and
reports nothing when it does not, so the caller can record an explicit
``unknown`` rather than guess.

The heuristics are intentionally conservative: a false "unknown" is harmless,
a wrong attribution is not.
"""

from __future__ import annotations

import re

from cyberkb.markdown import iter_lines

__all__ = ["extract_authors"]

MAX_AUTHORS = 4
_MIN_NAME_LEN = 3
_MAX_NAME_LEN = 60
_SCAN_LINES = 40

# Matches an attribution line that opens with by / author(s) / written by /
# created by, optionally followed by a colon or dash, then one or more names.
_BYLINE_RE = re.compile(
    r"^\s*(?:by|author[s]?|written by|created by)\s*[:\-\u2013\u2014]?\s+(?P<names>[^\n]{3,120})$",
    re.IGNORECASE,
)
# A LinkedIn slug such as linkedin.com/in/joas-antonio-dos-santos
_LINKEDIN_RE = re.compile(r"linkedin\.com/in/([a-z0-9][a-z0-9\-]{2,60})", re.IGNORECASE)
_SPLIT_RE = re.compile(r"\s*(?:,|;|&|\band\b|\be\b|\by\b)\s*", re.IGNORECASE)
# A plausible human/organisation name: 2-5 capitalised words, no sentence punctuation.
_NAME_RE = re.compile(
    r"^(?:[A-Z][\w.'\-]+|[A-Z]\.?)(?:\s+(?:[A-Z][\w.'\-]+|[A-Z]\.?|de|da|dos|das|van|von|of)){1,4}$",
)
_BAD_TOKENS = frozenset(
    {
        "the",
        "introduction",
        "chapter",
        "table",
        "contents",
        "copyright",
        "version",
        "guide",
        "overview",
        "report",
        "security",
        "cyber",
        "cybersecurity",
    },
)


def _normalise_case(name: str) -> str:
    """Title-case an ALL-CAPS name (PDF headings), leaving mixed case untouched."""
    if name == name.upper():
        return " ".join(
            w if w in {"de", "da", "dos", "das"} else w.capitalize() for w in name.lower().split()
        )
    return name


def _clean_name(candidate: str) -> str | None:
    name = _normalise_case(candidate.strip().strip(".,;:-\u2013\u2014 ").strip())
    if not _MIN_NAME_LEN <= len(name) <= _MAX_NAME_LEN:
        return None
    if any(ch.isdigit() for ch in name):  # trailing IDs / handles are not names
        return None
    if not _NAME_RE.match(name):
        return None
    lowered = {w.lower() for w in name.split()}
    if lowered & _BAD_TOKENS:
        return None
    return name


def _canonicalise(names: list[str], reference: str | None) -> list[str]:
    """Replace a name with ``reference`` when it is a token-subset of it.

    Handles PDF line-break truncation ("Joas Antonio" / "Joas Antonio Dos")
    against the fuller name recovered from a LinkedIn slug.
    """
    if reference is None:
        return names
    ref_tokens = {t.lower() for t in reference.split()}
    out: list[str] = []
    for name in names:
        tokens = {t.lower() for t in name.split()}
        resolved = reference if tokens < ref_tokens or tokens == ref_tokens else name
        if resolved not in out:
            out.append(resolved)
    return out


def _slug_to_name(slug: str) -> str | None:
    parts = [p for p in slug.split("-") if p]
    if not 2 <= len(parts) <= 5:  # noqa: PLR2004 -- a plausible full-name length
        return None
    return " ".join(p.capitalize() for p in parts)


def _split_names(blob: str) -> list[str]:
    names: list[str] = []
    for piece in _SPLIT_RE.split(blob):
        cleaned = _clean_name(piece)
        if cleaned and cleaned not in names:
            names.append(cleaned)
    return names


def extract_authors(body: str) -> tuple[str, ...]:
    """Return credible author names stated in ``body``, or ``()`` when none are.

    Bylines win over LinkedIn slugs; both are checked only near the top of the
    document, where attribution lives, to avoid picking names out of prose.
    """
    # Heal hyphenated line breaks so a profile link split across lines
    # ("…/in/jane-\ndoe") rejoins, while real newlines stay as slug boundaries.
    healed = re.sub(r"-[ \t]*\n[ \t]*", "-", body[:4000])
    slug_match = _LINKEDIN_RE.search(healed)
    linkedin_name = _slug_to_name(slug_match.group(1)) if slug_match else None

    bylines: list[str] = []
    for line in iter_lines(body):
        if line.number > _SCAN_LINES:
            break
        if line.in_fence:
            continue
        match = _BYLINE_RE.match(line.text)
        if match:
            bylines.extend(_split_names(match.group("names")))
            if bylines:
                return tuple(_canonicalise(bylines, linkedin_name)[:MAX_AUTHORS])

    if linkedin_name:
        return (linkedin_name,)
    return ()
