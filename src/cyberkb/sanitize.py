"""Normalisation of raw contributor Markdown into repository-grade Markdown.

Guarantees (all idempotent: ``sanitize(sanitize(x)) == sanitize(x)``):

* LF line endings, Unicode NFC, no BOM, no control or bidi-override chars;
* PDF-conversion page markers (``[[ PAGE 12 ]]``) removed;
* marketing/click-tracking query parameters stripped from URLs *without*
  touching meaningful parameters (v1 also removed ``ref=``, which broke
  GitHub links such as ``?ref=main``, and left dangling ``&`` separators);
* trailing whitespace trimmed and blank-line runs collapsed -- outside code
  fences only, so code samples are preserved byte for byte;
* exactly one trailing newline.
"""

from __future__ import annotations

import re
import unicodedata
from urllib.parse import urlsplit, urlunsplit

from cyberkb.markdown import iter_lines
from cyberkb.textutil import strip_unsafe_chars

__all__ = ["TRACKING_PARAMS", "sanitize_markdown", "strip_tracking_params"]

PAGE_MARKER_RE = re.compile(r"^[ \t]*\[\[[ \t]*PAGE[ \t]+\d+[ \t]*\]\][ \t]*$", re.IGNORECASE)
TRACKING_PARAMS = frozenset(
    {
        "_hsenc",
        "_hsmi",
        "dclid",
        "fbclid",
        "gbraid",
        "gclid",
        "igshid",
        "li_fat_id",
        "mc_cid",
        "mc_eid",
        "mkt_tok",
        "msclkid",
        "oly_anon_id",
        "oly_enc_id",
        "rb_clickid",
        "s_cid",
        "ttclid",
        "twclid",
        "vero_id",
        "wbraid",
        "yclid",
    },
)
_URL_RE = re.compile(r"https?://[^\s<>\"'`)\]]+", re.IGNORECASE)


def _is_tracking(key: str) -> bool:
    lowered = key.lower()
    return lowered.startswith("utm_") or lowered in TRACKING_PARAMS


def strip_tracking_params(url: str) -> str:
    """Remove tracking parameters from ``url``, preserving everything else verbatim."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return url
    if not parts.query:
        return url
    kept = [
        pair for pair in parts.query.split("&") if pair and not _is_tracking(pair.split("=", 1)[0])
    ]
    return urlunsplit(parts._replace(query="&".join(kept)))


def sanitize_markdown(text: str) -> str:
    """Return the normalised form of ``text`` (see module docstring)."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = strip_unsafe_chars(unicodedata.normalize("NFC", text))
    out: list[str] = []
    blank_run = 0
    for line in iter_lines(text):
        if line.in_fence:
            out.append(line.text)
            blank_run = 0
            continue
        if PAGE_MARKER_RE.match(line.text):
            continue
        cleaned = _URL_RE.sub(lambda m: strip_tracking_params(m.group(0)), line.text.rstrip())
        if not cleaned:
            blank_run += 1
            if blank_run > 1:
                continue
        else:
            blank_run = 0
        out.append(cleaned)
    body = "\n".join(out).strip("\n")
    return body + "\n" if body else ""
