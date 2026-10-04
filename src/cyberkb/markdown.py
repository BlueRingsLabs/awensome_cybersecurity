"""Fence-aware Markdown helpers.

The v1 pipeline treated every line starting with ``#`` as a heading, so
shell comments inside code blocks became document titles (``Scan a single
IP`` was the catalog title of a blue team toolkit). Everything here walks the
document line by line and tracks fenced code blocks per CommonMark: a fence
is three or more backticks or tildes, indented at most three spaces, closed
by a fence of the same character that is at least as long.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

__all__ = [
    "Line",
    "active_content",
    "escape_inline",
    "extract_h1",
    "first_text_line",
    "headings",
    "iter_lines",
]

_FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_ATX_RE = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*#*[ \t]*$")
_SETEXT_H1_RE = re.compile(r"^ {0,3}=+[ \t]*$")
_INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\1).)+?\1")
_ACTIVE_HTML_RE = re.compile(
    r"<\s*(script|iframe|object|embed|applet|frame|frameset|meta|base|form)\b", re.IGNORECASE
)
_ACTIVE_ATTR_RE = re.compile(r"<[^>]*\son[a-z]+\s*=", re.IGNORECASE)
_JS_LINK_RE = re.compile(r"\]\(\s*<?\s*(?:javascript|vbscript|data)\s*:", re.IGNORECASE)
_HTML_JS_HREF_RE = re.compile(
    r"(?:href|src)\s*=\s*[\"']?\s*(?:javascript|vbscript)\s*:", re.IGNORECASE
)
_LETTERS_RE = re.compile(r"[^\W\d_]", re.UNICODE)
_URLISH_RE = re.compile(r"^(?:https?://|www\.)\S+$", re.IGNORECASE)
_ESCAPE_RE = re.compile(r"([\\`*_\[\]<>|#])")


@dataclass(frozen=True, slots=True)
class Line:
    """One physical line with its 1-based number and fence state."""

    number: int
    text: str
    in_fence: bool


def iter_lines(text: str) -> Iterator[Line]:
    """Yield every line, flagging those inside fenced code blocks (fence lines included)."""
    fence_char = ""
    fence_len = 0
    for number, raw in enumerate(text.split("\n"), start=1):
        match = _FENCE_RE.match(raw)
        if fence_char:
            yield Line(number, raw, in_fence=True)
            if (
                match
                and match.group(1)[0] == fence_char
                and len(match.group(1)) >= fence_len
                and not match.group(2).strip()
            ):
                fence_char, fence_len = "", 0
            continue
        # Per CommonMark, a backtick fence's info string cannot contain backticks.
        if match and not (match.group(1)[0] == "`" and "`" in match.group(2)):
            fence_char, fence_len = match.group(1)[0], len(match.group(1))
            yield Line(number, raw, in_fence=True)
        else:
            yield Line(number, raw, in_fence=False)


def headings(text: str, *, max_lines: int | None = None) -> list[tuple[int, str]]:
    """Return ``(level, title)`` for ATX headings outside code fences."""
    found: list[tuple[int, str]] = []
    for line in iter_lines(text):
        if max_lines is not None and line.number > max_lines:
            break
        if line.in_fence:
            continue
        match = _ATX_RE.match(line.text)
        if match and match.group(2):
            found.append((len(match.group(1)), match.group(2).strip()))
    return found


def extract_h1(text: str, *, max_lines: int = 200) -> str | None:
    """First level-1 heading (ATX ``# x`` or setext ``x`` / ``===``) outside fences."""
    previous: Line | None = None
    for line in iter_lines(text):
        if line.number > max_lines:
            break
        if not line.in_fence:
            match = _ATX_RE.match(line.text)
            if match and len(match.group(1)) == 1 and match.group(2):
                return match.group(2).strip()
            if (
                _SETEXT_H1_RE.match(line.text)
                and previous is not None
                and not previous.in_fence
                and previous.text.strip()
                and not _ATX_RE.match(previous.text)
            ):
                return previous.text.strip()
        previous = line
    return None


def first_text_line(text: str, *, max_lines: int = 60, max_len: int = 140) -> str | None:
    """First prose-looking line outside fences, usable as a fallback title.

    Skips blank lines, bare URLs, page numbers and lines with fewer than three
    letters, which is what PDF-to-text conversions mostly start with.
    """
    for line in iter_lines(text):
        if line.number > max_lines:
            break
        candidate = line.text.strip().lstrip("#").strip()
        if (
            line.in_fence
            or not candidate
            or len(candidate) > max_len
            or _URLISH_RE.match(candidate)
            or len(_LETTERS_RE.findall(candidate)) < 3  # noqa: PLR2004
        ):
            continue
        return candidate
    return None


def active_content(text: str) -> list[tuple[int, str]]:
    """Locate executable HTML or script URLs outside code fences and inline code.

    Security tutorials legitimately show payloads; they belong in code fences,
    where renderers display them inertly. Returns ``(line_number, snippet)``.
    """
    hits: list[tuple[int, str]] = []
    for line in iter_lines(text):
        if line.in_fence:
            continue
        visible = _INLINE_CODE_RE.sub("", line.text)
        for pattern in (_ACTIVE_HTML_RE, _ACTIVE_ATTR_RE, _JS_LINK_RE, _HTML_JS_HREF_RE):
            match = pattern.search(visible)
            if match:
                hits.append(
                    (line.number, visible[max(0, match.start() - 20) : match.end() + 20].strip())
                )
                break
    return hits


def escape_inline(text: str) -> str:
    """Escape characters that would change the meaning of inline Markdown or table cells."""
    return _ESCAPE_RE.sub(r"\\\1", text)
