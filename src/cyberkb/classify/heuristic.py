"""Deterministic, explainable offline classifier.

Every category in the taxonomy carries weighted keyword phrases. A document
is tokenised once into n-gram counts for four regions -- title, filename
stem, headings and body sample -- and each category scores::

    sum(weight * (4 * in_title + 3 * in_stem + 1.5 * log1p(heading_hits) + log1p(body_hits)))

Presence (not frequency) counts in the title and stem because they are short
and decisive; logarithmic damping stops a single keyword repeated on every
page of a book from dominating. Confidence combines the margin between the
two best categories with the absolute strength of the winner; weak evidence
routes the document to the staging category instead of guessing.
"""

from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING

from cyberkb.classify.base import ClassificationResult, Document
from cyberkb.language import detect_language
from cyberkb.markdown import extract_h1, headings
from cyberkb.textutil import ngram_counts, plain_text, tokenize, word_count

if TYPE_CHECKING:
    from collections import Counter

    from cyberkb.taxonomy import Taxonomy

__all__ = [
    "classify",
    "detect_format",
    "humanize_stem",
    "infer_title",
    "score_categories",
    "select_tags",
]

TITLE_WEIGHT = 4.0
STEM_WEIGHT = 3.0
HEADING_WEIGHT = 1.5
BODY_SAMPLE_CHARS = 60_000
MIN_SCORE = 8.0
STRONG_SCORE = 40.0
MAX_TAGS = 6
BOOK_MIN_WORDS = 40_000
# PDF-to-text conversions contain unfenced shell comments ("# scan a host")
# deep in the body; only a heading near the top can be the document title.
TITLE_H1_MAX_LINES = 30

_YEAR_PREFIX_RE = re.compile(r"^(?:19|20)\d{2}[-_ ]+")
_GENERIC_TITLES = frozenset(
    {
        "about",
        "abstract",
        "contents",
        "disclaimer",
        "index",
        "introduction",
        "overview",
        "preface",
        "summary",
        "table of contents",
        "untitled",
    },
)
# Canonical spelling for acronyms and brand names that title-casing would mangle.
_CANONICAL_WORDS = {
    word.lower(): word
    for word in [
        "AD",
        "ADCS",
        "AI",
        "API",
        "APT",
        "ARP",
        "AV",
        "AWS",
        "BAT",
        "BLE",
        "C2",
        "CEH",
        "CISO",
        "CMS",
        "CSA",
        "CSS",
        "CTF",
        "CTI",
        "CVE",
        "DFIR",
        "DLL",
        "DNS",
        "DHCP",
        "EDR",
        "EKS",
        "FTK",
        "FTP",
        "GCP",
        "GPG",
        "GPO",
        "HTML",
        "HTTP",
        "HTTPS",
        "IAM",
        "ICS",
        "IDS",
        "IOC",
        "IoT",
        "IPS",
        "IR",
        "ISO",
        "IT",
        "JS",
        "KVM",
        "LAN",
        "LDAP",
        "LEMP",
        "LLM",
        "LLMs",
        "MD5",
        "MFA",
        "MITM",
        "MS365",
        "NAS",
        "NIST",
        "NTLM",
        "O365",
        "OPSEC",
        "OSINT",
        "OSCP",
        "OT",
        "OWASP",
        "PDF",
        "PHP",
        "PMKID",
        "QA",
        "RAT",
        "RDP",
        "RTO",
        "SAM",
        "SCADA",
        "SIEM",
        "SMB",
        "SMTP",
        "SOC",
        "SQL",
        "SSH",
        "SSL",
        "TLS",
        "TTP",
        "URL",
        "USB",
        "VPN",
        "VPS",
        "WAF",
        "WPA",
        "WPA2",
        "XSS",
        "XXE",
        "YARA",
        "ChatGPT",
        "CompTIA",
        "CyBOK",
        "DefectDojo",
        "DevSecOps",
        "eCPPT",
        "eCPTX",
        "eJPT",
        "eLearnSecurity",
        "eWPT",
        "eWPTX",
        "FortiGate",
        "GitHub",
        "JavaScript",
        "Kerberos",
        "Linux",
        "macOS",
        "Maltego",
        "Metasploit",
        "MITRE",
        "MySQL",
        "Nmap",
        "PostgreSQL",
        "PowerShell",
        "pfSense",
        "Python",
        "Shodan",
        "Tor",
        "Ubuntu",
        "Whonix",
        "Windows",
        "WinRM",
        "Wireshark",
    ]
}
_LOWER_WORDS = frozenset(
    [
        "a",
        "an",
        "and",
        "as",
        "at",
        "by",
        "de",
        "do",
        "da",
        "e",
        "em",
        "for",
        "in",
        "of",
        "on",
        "or",
        "para",
        "the",
        "to",
        "vs",
        "with",
    ]
)

_FORMAT_RULES: tuple[tuple[str, frozenset[tuple[str, ...]]], ...] = (
    ("cheatsheet", frozenset({("cheat", "sheet"), ("cheatsheet",), ("cheat", "sheets")})),
    ("checklist", frozenset({("checklist",), ("check", "list")})),
    ("playbook", frozenset({("playbook",), ("playbooks",), ("runbook",)})),
    (
        "course-notes",
        frozenset(
            {
                ("notes",),
                ("exam",),
                ("study",),
                ("bootcamp",),
                ("course",),
                ("training",),
                ("studies",),
            },
        ),
    ),
    ("paper", frozenset({("paper",), ("whitepaper",), ("research",), ("journal",)})),
)
_REFERENCE_MARKERS = frozenset(
    {
        ("tools",),
        ("toolkit",),
        ("books",),
        ("resources",),
        ("labs",),
        ("collection",),
        ("list",),
        ("links",),
    },
)


def _counts(text: str) -> Counter[tuple[str, ...]]:
    return ngram_counts(tokenize(text))


def score_categories(
    taxonomy: Taxonomy,
    *,
    title: str,
    stem: str,
    heading_text: str,
    body: str,
) -> dict[str, float]:
    """Score every non-staging category for the given document regions."""
    title_c, stem_c = _counts(title), _counts(stem)
    head_c, body_c = _counts(heading_text), _counts(body[:BODY_SAMPLE_CHARS])
    scores: dict[str, float] = {}
    for cat in taxonomy.categories:
        if cat.staging:
            continue
        total = 0.0
        for phrase, weight in cat.keywords:
            evidence = (
                TITLE_WEIGHT * min(title_c[phrase], 1)
                + STEM_WEIGHT * min(stem_c[phrase], 1)
                + HEADING_WEIGHT * math.log1p(head_c[phrase])
                + math.log1p(body_c[phrase])
            )
            total += weight * evidence
        scores[cat.id] = round(total, 4)
    return scores


def _confidence(scores: dict[str, float]) -> tuple[str, float]:
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    best, top = ranked[0]
    runner_up = ranked[1][1] if len(ranked) > 1 else 0.0
    if top <= 0:
        return best, 0.0
    margin = (top - runner_up) / top
    strength = min(1.0, top / STRONG_SCORE)
    return best, round(min(1.0, 0.35 * strength + 0.65 * margin * strength + 0.15 * margin), 2)


def humanize_stem(stem: str) -> str:
    """Turn a filename stem into a readable title.

    ``2019_free-stellar-lumens`` becomes ``Free Stellar Lumens``.
    """
    words = [w for w in re.split(r"[-_\s]+", _YEAR_PREFIX_RE.sub("", stem)) if w]
    out: list[str] = []
    for index, word in enumerate(words):
        lowered = word.lower()
        if lowered in _CANONICAL_WORDS:
            out.append(_CANONICAL_WORDS[lowered])
        elif index > 0 and lowered in _LOWER_WORDS:
            out.append(lowered)
        else:
            out.append(word[:1].upper() + word[1:])
    return " ".join(out) or "Untitled"


def infer_title(body: str, stem: str) -> str:
    """Best title from the body's H1 (outside code fences) or the filename stem."""
    h1 = extract_h1(body, max_lines=TITLE_H1_MAX_LINES)
    if h1:
        cleaned = plain_text(h1, 160)
        if cleaned and cleaned.lower() not in _GENERIC_TITLES and tokenize(cleaned):
            return cleaned
    return humanize_stem(stem)


def detect_format(title: str, stem: str, body: str) -> str:
    """Infer the resource format from naming conventions and document size."""
    names = _counts(f"{title} {stem}")
    for fmt, markers in _FORMAT_RULES:
        if any(names[m] for m in markers):
            return fmt
    words = word_count(body)
    if words >= BOOK_MIN_WORDS:
        return "book"
    if any(names[m] for m in _REFERENCE_MARKERS):
        return "reference"
    if _YEAR_PREFIX_RE.match(stem) and extract_h1(body, max_lines=TITLE_H1_MAX_LINES):
        return "article"
    return "guide"


def select_tags(taxonomy: Taxonomy, *, title: str, stem: str, body: str) -> tuple[str, ...]:
    """Pick up to ``MAX_TAGS`` controlled-vocabulary tags by evidence strength."""
    name_c = _counts(f"{title} {stem}")
    tokens = tokenize(body[:BODY_SAMPLE_CHARS])
    body_c = ngram_counts(tokens)
    # Require repeated mentions, scaled to length, before a body-only tag sticks.
    threshold = max(3, len(tokens) // 2500)
    scored: list[tuple[float, str]] = []
    for tag in taxonomy.tags:
        in_name = any(name_c[p] for p in tag.patterns)
        hits = sum(body_c[p] for p in tag.patterns)
        if in_name or hits >= threshold:
            scored.append((10.0 * in_name + math.log1p(hits), tag.id))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return tuple(sorted(tag_id for _, tag_id in scored[:MAX_TAGS]))


def classify(
    document: Document, taxonomy: Taxonomy, *, title: str | None = None
) -> ClassificationResult:
    """Classify ``document`` without any network access."""
    resolved_title = title or infer_title(document.body, document.stem)
    heading_text = " ".join(text for _, text in headings(document.body, max_lines=4000))
    scores = score_categories(
        taxonomy,
        title=resolved_title,
        stem=document.stem,
        heading_text=heading_text,
        body=document.body,
    )
    best, confidence = _confidence(scores)
    category = best if scores[best] >= MIN_SCORE else taxonomy.staging.id
    return ClassificationResult(
        ref=document.ref,
        category=category,
        format=detect_format(resolved_title, document.stem, document.body),
        language=detect_language(document.body),
        title=resolved_title,
        confidence=confidence if category == best else 0.0,
        method="heuristic",
        tags=select_tags(taxonomy, title=resolved_title, stem=document.stem, body=document.body),
        scores=scores,
    )
