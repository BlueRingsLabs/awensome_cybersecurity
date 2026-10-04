"""Licence detection and redistribution policy for library content.

A knowledge base that republishes third-party works must know, per work,
under which terms it may do so. Detection is evidence-based: it only
recognises explicit licence *grants* (Creative Commons deeds and URLs, the
UK Open Government Licence, the GNU FDL, public-domain dedications) and
"all rights reserved" notices, searched in the parts of a document where
publishers put them (the opening pages and the colophon). Anything else is
``NOASSERTION`` -- unknown is reported as unknown, never guessed.

Detected values are written to front matter at ingestion time, where a
maintainer can correct them; see docs/runbooks/content-licensing.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

__all__ = [
    "LicenseFinding",
    "Redistribution",
    "detect_license",
    "redistribution_class",
]

_HEAD_CHARS = 30_000
_TAIL_CHARS = 12_000
_WS_RE = re.compile(r"\s+")

_CC_URL_RE = re.compile(
    r"creativecommons\.org/licenses/(by(?:-nc)?(?:-sa|-nd)?)/(\d\.\d)",
    re.IGNORECASE,
)
_CC0_URL_RE = re.compile(r"creativecommons\.org/publicdomain/zero/1\.0", re.IGNORECASE)
_CC_TEXT_RE = re.compile(
    r"(?:licen[cs]ed|released|available|distributed|published|provided)\b[^.]{0,80}?\bunder\s+(?:a|an|the)?\s*"
    r"(?:terms\s+of\s+(?:a|the)\s+)?creative\s+commons\s+"
    r"(attribution(?:[\s-]+non[\s-]?commercial)?(?:[\s-]+(?:share[\s-]?alike|no[\s-]?deriv\w*))?)"
    r"(?:\s+(?:international\s+)?(?:licen[cs]e\s+)?)?\s*\(?(?:v(?:ersion)?\s*)?(\d\.\d)",
    re.IGNORECASE,
)
# Upper-case "CC" only: lower-case "cc" collides with hex dumps in exploit write-ups.
_CC_ABBR_RE = re.compile(r"\bCC[\s-]BY((?:[\s-]NC)?(?:[\s-](?:SA|ND))?)[\s-]+(\d\.\d)\b")
# A bare "CC BY-NC-SA 4.0" often names the licence of a *cited tool*; it only
# counts when a grant phrase precedes it ("... is licensed under ..., CC BY 4.0").
_GRANT_CONTEXT_RE = re.compile(
    r"(?:licen[cs]ed|released|available|distributed|provided)\b[^.]{0,60}?\bunder\b|licen[cs]e\s*:",
    re.IGNORECASE,
)
_GRANT_WINDOW = 100
_OGL_RE = re.compile(
    r"open\s+government\s+licen[cs]e(?:\s*(?:v|version)\s*(\d\.\d|\d))?", re.IGNORECASE
)
_GFDL_RE = re.compile(
    r"GNU\s+Free\s+Documentation\s+Licen[cs]e,?\s*(?:Version\s*)?(\d\.\d)?(.{0,80})",
    re.IGNORECASE,
)
_PD_RE = re.compile(
    r"(?:(?:placed|released|dedicated|granted)\s+(?:in|into|to)\s+the\s+public\s+domain"
    r"|not\s+subject\s+to\s+copyright(?:\s+protection)?\s+in\s+the\s+united\s+states)",
    re.IGNORECASE,
)
_ARR_RE = re.compile(r"all\s+rights\s+reserved", re.IGNORECASE)


class Redistribution(StrEnum):
    """What the detected licence allows this repository to do with a work."""

    PERMITTED = "permitted"
    NONCOMMERCIAL = "noncommercial"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class LicenseFinding:
    """A detected licence identifier and the text that evidences it."""

    license: str
    evidence: str


def _cc_id(kind: str, version: str) -> str:
    parts = [p for p in re.split(r"[\s-]+", kind.upper()) if p]
    return "CC-" + "-".join(parts) + f"-{version}"


def _cc_text_kind(phrase: str) -> str:
    folded = phrase.lower()
    kind = "BY"
    if "commercial" in folded:
        kind += "-NC"
    if "share" in folded:
        kind += "-SA"
    elif "deriv" in folded:
        kind += "-ND"
    return kind


def _snippet(text: str, match: re.Match[str]) -> str:
    start = max(0, match.start() - 40)
    return text[start : match.end() + 40].strip()


def _cc_url_id(match: re.Match[str]) -> str:
    return _cc_id(match.group(1), match.group(2))


def _cc_text_id(match: re.Match[str]) -> str:
    return _cc_id(_cc_text_kind(match.group(1)), match.group(2))


def _ogl_id(match: re.Match[str]) -> str:
    version = match.group(1) or "3.0"
    return f"OGL-UK-{version if '.' in version else f'{version}.0'}"


def _gfdl_id(match: re.Match[str]) -> str:
    version = match.group(1) or "1.3"
    suffix = "or-later" if "later" in match.group(2).lower() else "only"
    return f"GFDL-{version}-{suffix}"


# Each rule turns a match into a licence id. The CC-abbreviation rule also
# requires a nearby grant phrase, supplied via ``needs_context``.
_GRANT_RULES: tuple[tuple[re.Pattern[str], Any, bool], ...] = (
    (_CC_URL_RE, _cc_url_id, False),
    (_CC0_URL_RE, lambda _m: "CC0-1.0", False),
    (_CC_TEXT_RE, _cc_text_id, False),
    (_CC_ABBR_RE, lambda m: _cc_id("BY" + m.group(1), m.group(2)), True),
    (_OGL_RE, _ogl_id, False),
    (_GFDL_RE, _gfdl_id, False),
    (_PD_RE, lambda _m: "LicenseRef-Public-Domain", False),
)


def _has_grant_context(region: str, match: re.Match[str]) -> bool:
    window = region[max(0, match.start() - _GRANT_WINDOW) : match.start()]
    return bool(_GRANT_CONTEXT_RE.search(window))


def detect_license(text: str) -> LicenseFinding:
    """Detect the licence a document is distributed under.

    Open licence grants take precedence over "all rights reserved" notices,
    because the latter frequently refer to embedded third-party material
    (videos, logos) inside an otherwise openly licensed work. Among grants,
    the earliest occurrence wins.
    """
    region = _WS_RE.sub(" ", text[:_HEAD_CHARS] + " \n " + text[-_TAIL_CHARS:])
    grants: list[tuple[int, LicenseFinding]] = []
    for pattern, id_fn, needs_context in _GRANT_RULES:
        for match in pattern.finditer(region):
            if needs_context and not _has_grant_context(region, match):
                continue
            grants.append((match.start(), LicenseFinding(id_fn(match), _snippet(region, match))))

    if grants:
        return min(grants, key=lambda item: item[0])[1]
    arr = _ARR_RE.search(region)
    if arr:
        return LicenseFinding("LicenseRef-All-Rights-Reserved", _snippet(region, arr))
    return LicenseFinding("NOASSERTION", "")


_PERMISSIVE_PREFIXES = ("CC-BY-", "CC0-", "OGL-", "GFDL-", "MIT", "Apache-", "BSD-")


def redistribution_class(license_id: str) -> Redistribution:
    """Classify a licence identifier by what it permits for a public, non-commercial library."""
    if license_id == "LicenseRef-All-Rights-Reserved":
        return Redistribution.RESTRICTED
    if license_id == "LicenseRef-Public-Domain":
        return Redistribution.PERMITTED
    if license_id.startswith("CC-BY-NC"):
        return Redistribution.NONCOMMERCIAL
    if license_id.startswith(_PERMISSIVE_PREFIXES):
        return Redistribution.PERMITTED
    return Redistribution.UNKNOWN
