#!/usr/bin/env python3
"""
build_index.py -- Deterministic catalog generator for the
BlueRingsLabs/awensome_cybersecurity knowledge base.

Scans the repository domain tree (01_literature/, 02_papers/, 03_web_and_posts/)
and regenerates:

    * index.json   (machine-parsable catalog, schema v1)
    * index.yaml   (identical data in YAML form)
    * README.md    (only the block between the AUTO-INDEX markers)

This module is dependency-free besides PyYAML and is shared by:
    * the CI/CD ingestion pipeline (.github/scripts/classify_and_index.py)
    * manual/local regeneration:  python3 .github/scripts/build_index.py

Design notes:
    * Titles are extracted from the first ATX level-1 heading (# ...) of each
      Markdown file, falling back to a humanized version of the filename.
    * Tags are derived from lightweight keyword heuristics over the
      filename/title, keeping the catalog useful even without LLM enrichment.
      Files previously classified by the AI pipeline keep their richer
      metadata (summary/tags/language/confidence) if present in an existing
      index.json.
    * Output is fully deterministic (sorted entries) so CI diffs stay clean.

Author: Blue Rings Labs
License: MIT
"""

from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

# ---------------------------------------------------------------------------
# Taxonomy
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1.0.0"

REPO_ROOT = Path(os.environ.get("KB_REPO_ROOT", Path(__file__).resolve().parents[2]))

DOMAINS: dict[str, dict[str, Any]] = {
    "01_literature": {
        "name": "Literature",
        "description": "Books, summaries and theoretical notes.",
    },
    "02_papers": {
        "name": "Papers",
        "description": "Technical research papers and whitepapers.",
    },
    "03_web_and_posts": {
        "name": "Web & Posts",
        "description": "Articles, blog posts and web resources.",
    },
}

SUBDOMAINS: dict[str, dict[str, str]] = {
    "blue_team": {
        "name": "Blue Team",
        "description": "Defense, detection, SOC, incident response and hardening.",
    },
    "red_team": {
        "name": "Red Team",
        "description": "Offensive security, penetration testing and adversary simulation.",
    },
    "malware_analysis": {
        "name": "Malware Analysis",
        "description": "Malware research, hunting, forensics and defensive tooling.",
    },
    "reverse_engineering": {
        "name": "Reverse Engineering",
        "description": "Binary analysis, exploit development and internals.",
    },
    "threat_intelligence": {
        "name": "Threat Intelligence",
        "description": "OSINT, threat hunting, frameworks and intelligence operations.",
    },
    "unclassified": {
        "name": "Unclassified",
        "description": "Pending automated classification by the ingestion pipeline.",
    },
}

VALID_DOMAINS = tuple(DOMAINS)
VALID_SUBDOMAINS = tuple(SUBDOMAINS)

DOMAIN_TO_FORMAT = {
    "01_literature": "literature",
    "02_papers": "paper",
    "03_web_and_posts": "post",
}

README_NAME = "README.md"
INDEX_JSON_NAME = "index.json"
INDEX_YAML_NAME = "index.yaml"

README_START_MARKER = "<!-- BEGIN AUTO-INDEX -->"
README_END_MARKER = "<!-- END AUTO-INDEX -->"

_H1_RE = re.compile(r"^\s{0,3}#\s+(.+?)\s*$", re.MULTILINE)
_FM_TITLE_RE = re.compile(r"^title\s*:\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)
_YEAR_PREFIX_RE = re.compile(r"^(19|20)\d{2}[-_]")
_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")

# Keyword heuristics -> tags (kept intentionally small and fast).
_TAG_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bactive[_ -]?directory\b|\bkerbero?st\b|\bsmb\b"), "active-directory"),
    (re.compile(r"\bosint?\b|\bmaltego\b|\bdark[_ -]?web\b"), "osint"),
    (re.compile(r"\bpentest|\bpenetration[_ -]?testing\b"), "penetration-testing"),
    (re.compile(r"\bred[_ -]?team|\boffensive\b|\bevasion\b|\bbypass\b"), "red-team"),
    (re.compile(r"\bblue[_ -]?team\b|\bsoc\b|\bdefensive\b|\bhardening\b|\bfirewall\b"), "blue-team"),
    (re.compile(r"\bmalware\b|\bransomware\b|\byara\b|\bedr\b"), "malware"),
    (re.compile(r"\bforensic|\bincident[_ -]?response\b"), "forensics"),
    (re.compile(r"\breverse[_ -]?engineering|\bshellcode\b|\bexploit|\bbuffer[_ -]?overflow\b"), "reverse-engineering"),
    (re.compile(r"\bthreat[_ -]?(hunt|intel)|\batt[_ -]?ck\b|honey"), "threat-intelligence"),
    (re.compile(r"\bcloud\b|\baws\b|\bazure\b|\bgcp\b|\bkubernetes\b|\bcontainer\b"), "cloud"),
    (re.compile(r"\blinux\b|\bkali\b|\bbash\b"), "linux"),
    (re.compile(r"\bwindows\b|\bpowershell\b|\bwinrm\b"), "windows"),
    (re.compile(r"\bweb\b|\bxss\b|\bsql[_ -]?injection\b|\bowasp\b"), "web-security"),
    (re.compile(r"\bwireless\b|\bwifi\b|\b802\.11\b"), "wireless"),
    (re.compile(r"\biot\b|\bics\b|\bembedded\b"), "iot"),
    (re.compile(r"\bai\b|\bllm\b|\bchatgpt\b|\bgpt\b|\bgemini\b"), "ai-security"),
    (re.compile(r"\bcrypto|\bbitcoin\b|\bblockchain\b|\bsmart[_ -]?contract\b"), "cryptography"),
    (re.compile(r"\bcertification|\boscp\b|\bceh\b|\becptx|\bcomptia\b"), "certifications"),
    (re.compile(r"\bpython\b|\bscripting\b"), "python"),
    (re.compile(r"\bsocial[_ -]?engineering\b|\bphishing\b"), "social-engineering"),
]


def slugify(text: str, max_len: int = 80) -> str:
    """Normalize arbitrary text into a lowercase ASCII snake_case slug."""
    norm = unicodedata.normalize("NFKD", text)
    ascii_text = norm.encode("ascii", "ignore").decode("ascii").lower()
    slug = _NON_ALNUM_RE.sub("_", ascii_text).strip("_")
    return (slug[:max_len].rstrip("_")) or "untitled"


def _humanize(stem: str) -> str:
    """Turn a file stem into a readable title fallback."""
    cleaned = _YEAR_PREFIX_RE.sub("", stem)
    words = [w for w in re.split(r"[-_\s]+|[^\w\s]", cleaned) if w]
    out: list[str] = []
    for w in words:
        if re.fullmatch(r"[A-Z0-9]{1,6}", w):  # acronyms stay uppercase (SOC, AD...)
            out.append(w)
        else:
            out.append(w.capitalize())
    return " ".join(out) or stem.replace("_", " ").replace("-", " ").title()


def extract_title(path: Path) -> str:
    """Best-effort document title: front-matter, first H1, or humanized stem."""
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:8000]
    except OSError:
        return _humanize(path.stem)

    m = _FM_TITLE_RE.search(head)
    if m:
        return m.group(1).strip().strip("\"'")

    for match in _H1_RE.finditer(head):
        candidate = match.group(1).strip().strip("#").strip()
        # Skip page-marker noise like "[[ PAGE 1 ]]" converted to H1 headers.
        if candidate and not re.fullmatch(r"[\[\]\s\dPAGE]+", candidate.upper()):
            return candidate
    return _humanize(path.stem)


def derive_tags(stem: str, title: str) -> list[str]:
    haystack = f"{stem} {title}".lower().replace("_", " ")
    tags = [tag for pattern, tag in _TAG_RULES if pattern.search(haystack)]
    return sorted(set(tags))[:8]


def detect_language(path: Path) -> str:
    """Very light heuristic on filename + opening content."""
    name = path.name.lower()
    if any(marker in name for marker in ("_pt", "portugues", "portuguese", "_es", "espanol")):
        return "pt"
    try:
        sample = path.read_text(encoding="utf-8", errors="ignore")[:1500].lower()
    except OSError:
        return "en"
    pt_markers = ("ção", "segurança", "você", "não ", "como ", "para ", "é um")
    hits = sum(1 for mk in pt_markers if mk in sample)
    return "pt" if hits >= 3 else "en"


def load_previous_metadata(repo_root: Path) -> dict[str, dict[str, Any]]:
    """Preserve AI-enriched metadata (summary/tags/language/confidence) keyed by path."""
    previous: dict[str, dict[str, Any]] = {}
    idx_file = repo_root / INDEX_JSON_NAME
    if idx_file.is_file():
        try:
            data = json.loads(idx_file.read_text(encoding="utf-8"))
            for entry in data.get("entries", []):
                if isinstance(entry, dict) and entry.get("path"):
                    previous[entry["path"]] = entry
        except (json.JSONDecodeError, OSError):
            pass
    return previous


def scan_repository(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Walk the domain tree and build the full catalog structure."""
    repo_root = Path(repo_root)
    previous = load_previous_metadata(repo_root)
    entries: list[dict[str, Any]] = []

    for domain in VALID_DOMAINS:
        domain_dir = repo_root / domain
        if not domain_dir.is_dir():
            continue
        for sub in sorted(p.name for p in domain_dir.iterdir() if p.is_dir()):
            sub_dir = domain_dir / sub
            for md in sorted(sub_dir.glob("*.md")):
                rel_path = md.relative_to(repo_root).as_posix()
                title = extract_title(md)
                old = previous.get(rel_path, {})

                tags = old.get("tags") or derive_tags(md.stem, title)
                language = old.get("language") or detect_language(md)
                summary = old.get("summary", "")
                confidence = old.get("classification_confidence")
                source = old.get("source", "seed")

                stat = md.stat()
                modified = datetime.fromtimestamp(
                    stat.st_mtime, tz=timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ")

                entry: dict[str, Any] = {
                    "id": f"{domain}.{sub}.{md.stem}",
                    "title": title,
                    "path": rel_path,
                    "filename": md.name,
                    "domain": domain,
                    "subdomain": sub,
                    "format": DOMAIN_TO_FORMAT.get(domain, "note"),
                    "tags": tags,
                    "language": language,
                    "summary": summary,
                    "size_bytes": stat.st_size,
                    "modified_at": modified,
                    "source": source,
                }
                if confidence is not None:
                    entry["classification_confidence"] = confidence
                entries.append(entry)

    counts = {
        "total_resources": len(entries),
        "by_domain": {
            d: sum(1 for e in entries if e["domain"] == d) for d in VALID_DOMAINS
        },
        "by_subdomain": {
            s: sum(1 for e in entries if e["subdomain"] == s) for s in SUBDOMAINS
        },
    }

    catalog = {
        "schema_version": SCHEMA_VERSION,
        "repository": {
            "name": "awensome_cybersecurity",
            "organization": "BlueRingsLabs",
            "url": "https://github.com/BlueRingsLabs/awensome_cybersecurity",
            "license": "MIT",
            "description": (
                "Open, curated and fully automated cybersecurity knowledge base. "
                "Raw contributions land in the repository root and are classified, "
                "sanitized and indexed automatically on merge."
            ),
        },
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "build_index.py (classify_and_index.py pipeline)",
        "taxonomy": {
            "domains": {
                d: {**meta, "subdirectories": list(SUBDOMAINS)}
                for d, meta in DOMAINS.items()
            },
            "subdomains": SUBDOMAINS,
        },
        "counts": counts,
        "entries": sorted(
            entries, key=lambda e: (e["domain"], e["subdomain"], e["filename"])
        ),
    }
    return catalog


def quote_rel(path: str) -> str:
    """Percent-safe relative link for markdown (spaces, unicode etc.)."""
    return quote(path, safe="/_.-")


def render_index_block(catalog: dict[str, Any]) -> str:
    """Render the auto-updated Resource Index section for README.md."""
    lines: list[str] = []
    counts = catalog["counts"]
    lines.append(
        f"> Catalog regenerated: **{catalog['generated_at']}** | "
        f"**{counts['total_resources']} resources** indexed. "
        f"Machine-readable catalogs: [`index.json`]({INDEX_JSON_NAME}) / "
        f"[`index.yaml`]({INDEX_YAML_NAME})."
    )
    lines.append("")

    for domain, meta in catalog["taxonomy"]["domains"].items():
        domain_entries = [e for e in catalog["entries"] if e["domain"] == domain]
        if not domain_entries:
            continue
        lines.append(
            f"### {domain} -- {meta['name']} ({len(domain_entries)} resources)"
        )
        lines.append("")
        lines.append("| Subdomain | Count | Highlights |")
        lines.append("| --- | ---: | --- |")
        for sub in catalog["taxonomy"]["domains"][domain]["subdirectories"]:
            subset = [e for e in domain_entries if e["subdomain"] == sub]
            if not subset:
                continue
            top = subset[:3]
            links = "; ".join(
                f"[{e['title'][:48].strip()}]({quote_rel(e['path'])})" for e in top
            )
            more = (
                f" \u00b7 [+{len(subset) - 3} more](/{domain}/{sub}/)"
                if len(subset) > 3
                else ""
            )
            lines.append(f"| `{sub}` | {len(subset)} | {links}{more} |")
        lines.append("")

    unclassified = counts["by_subdomain"].get("unclassified", 0)
    if unclassified:
        lines.append(
            f"_Note: {unclassified} resource(s) are pending automated "
            "classification and will be routed by the next pipeline run._"
        )
        lines.append("")

    return "\n".join(lines).rstrip()


def update_readme_index(catalog: dict[str, Any], repo_root: Path = REPO_ROOT) -> None:
    """Replace only the marked block inside README.md, preserving everything else."""
    readme = Path(repo_root) / README_NAME
    block = render_index_block(catalog)
    new_section = f"{README_START_MARKER}\n{block}\n{README_END_MARKER}"

    if readme.is_file():
        content = readme.read_text(encoding="utf-8")
        start = content.find(README_START_MARKER)
        end = content.find(README_END_MARKER)
        if start != -1 and end != -1 and end > start:
            merged = (
                content[:start] + new_section + content[end + len(README_END_MARKER):]
            )
            readme.write_text(merged, encoding="utf-8")
            return
        # Markers missing: append the managed block at the end.
        readme.write_text(content.rstrip() + "\n\n" + new_section + "\n", encoding="utf-8")
        return

    readme.write_text(
        "# BlueRingsLabs / awensome_cybersecurity\n\n" + new_section + "\n",
        encoding="utf-8",
    )


def write_catalog(catalog: dict[str, Any], repo_root: Path = REPO_ROOT) -> None:
    repo_root = Path(repo_root)
    json_path = repo_root / INDEX_JSON_NAME
    json_path.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if yaml is not None:
        yaml_path = repo_root / INDEX_YAML_NAME
        header = (
            "# awensome_cybersecurity machine-readable catalog.\n"
            "# Generated automatically -- do not edit by hand.\n"
            "# See .github/scripts/build_index.py\n"
        )
        body = yaml.safe_dump(
            catalog, sort_keys=False, allow_unicode=True, width=100
        )
        yaml_path.write_text(header + body, encoding="utf-8")
    else:  # pragma: no cover
        print("warning: PyYAML not installed; skipping index.yaml", file=sys.stderr)

    update_readme_index(catalog, repo_root)


def main() -> int:
    repo_root = Path(os.environ.get("KB_REPO_ROOT", REPO_ROOT))
    catalog = scan_repository(repo_root)
    write_catalog(catalog, repo_root)
    print(
        f"Catalog regenerated: {catalog['counts']['total_resources']} resources "
        f"-> {INDEX_JSON_NAME}, {INDEX_YAML_NAME}, {README_NAME}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
