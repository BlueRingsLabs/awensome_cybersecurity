#!/usr/bin/env python3
"""
catalog_lib.py — Shared catalog engine for the BlueRingsLabs/awensome_cybersecurity pipeline.

Single source of truth used by BOTH:
  * ``generate_catalog.py``        (one-off / local regeneration of index.json, index.yaml and README)
  * ``classify_and_index.py``      (CI/CD ingestion + AI classification + auto-indexing)

Responsibilities
----------------
  - Discover every Markdown resource inside the domain folders.
  - Derive human-friendly titles (H1 > filename), publication years (filename prefix > content scan).
  - Emit a versioned, machine-parsable catalog (schema v1.0.0).
  - Render index.json (canonical JSON), index.yaml (compact YAML) and the
    README.md resource index between managed AUTO-INDEX markers.

Zero third-party dependencies except PyYAML (already required by the pipeline).
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from zoneinfo import ZoneInfo  # tz-aware build timestamps in CI (ubuntu-latest)

    _TZ = ZoneInfo("Etc/UTC")
except Exception:  # pragma: no cover - platform without tzdata
    try:
        from backports.zoneinfo import ZoneInfo as _BZ  # type: ignore

        _TZ = _BZ("Etc/UTC")
    except Exception:
        _TZ = timezone.utc

REPO_ROOT = Path(__file__).resolve().parents[2]

SCHEMA_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Taxonomy (mirrors index.json -> taxonomy.domains; keep both in sync)
# ---------------------------------------------------------------------------
DOMAINS: Dict[str, str] = {
    "01_literature": "Books, summaries and theoretical notes",
    "02_papers": "Technical research papers and whitepapers",
    "03_web_and_posts": "Articles, blog posts and web resources",
}

SUBDOMAINS: List[str] = [
    "blue_team",
    "red_team",
    "malware_analysis",
    "reverse_engineering",
    "threat_intelligence",
]

SUBDOMAIN_LABELS: Dict[str, str] = {
    "blue_team": "Blue Team · Defense, Detection & Response",
    "red_team": "Red Team · Offensive Security & Pentesting",
    "malware_analysis": "Malware Analysis · Malware, Forensics & SOC Operations",
    "reverse_engineering": "Reverse Engineering · Exploit Dev & RE",
    "threat_intelligence": "Threat Intelligence · OSINT, Threat Hunting & CTI",
    "unclassified": "Unclassified · Awaiting Pipeline Classification",
}

VALID_TARGET_DOMAINS: List[str] = list(DOMAINS.keys())
VALID_TARGET_SUBDOMAINS: List[str] = SUBDOMAINS + ["unclassified"]

README_START_MARKER = "<!-- AUTO-INDEX:START -->"
README_END_MARKER = "<!-- AUTO-INDEX:END -->"

README_INTRO = """\
## 📚 Resource Index

The tables below are **generated automatically** by the ingestion pipeline on every
merge to `main` — please do not edit them by hand (see
[`CONTRIBUTING.md`](CONTRIBUTING.md)). The canonical machine-readable catalogs live in
[`index.json`](index.json) and [`index.yaml`](index.yaml).
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def slugify(text: str, max_len: int = 80) -> str:
    """ASCII, kebab-case slug usable as a safe file name."""
    text = unicodedata.normalize("NFKD", text or "")
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return (text[:max_len].rstrip("-")) or "untitled"


def smart_unlink(path: Path) -> None:
    """Delete a file if it exists (idempotent cleanup helper)."""
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def _title_from_filename(stem: str) -> str:
    s = re.sub(r"^(\d{4})[-_ ]+", "", stem)          # leading year prefix
    s = s.replace("_", " ").replace("-", " ")         # separators -> spaces
    s = re.sub(r"\s+", " ", s).strip()
    words = []
    for w in s.split(" "):
        if w and (w.isupper() and len(w) <= 6):       # keep acronyms: AD, CVE, TLS...
            words.append(w)
        elif w and re.match(r"^[A-Z]", w):            # already capitalized
            words.append(w)
        else:
            words.append(w.capitalize())
    return " ".join(words)


def _extract_h1(text: str) -> Optional[str]:
    m = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if not m:
        m = re.search(r"\n#\s+(.+?)\n", "\n" + text)
    if not m:
        return None
    title = _clean_prose(m.group(1))
    title = re.sub(r"\[.*?\]\((.*?)\)", r"\1", title)  # markdown links -> target text
    title = re.sub(r"[`*_>#]", "", title)
    title = re.sub(r"\s+", " ", title).strip(" -–—:.")
    return title if len(title) >= 3 else None


def _extract_year(name: str, text: str) -> Optional[int]:
    m = re.match(r"^(19|20)\d{2}(?=[-_])", name)      # YYYY- or YYYY_ prefix
    if m:
        return int(m.group(0))
    for pat in (r"\b(?:19|20)\d{2}\b",):
        found = re.findall(pat, text[:2500])
        years = [int(y) for y in found if 1980 <= int(y) <= 2030]
        if years:
            return max(years)                          # most recent mention ~ publish year
    return None


_LANG_RE = re.compile(
    r"(?:^|[_\-])(pt[-_]?br|pt|por|es|esp|fr|fra|de|ger|it|ita|en|eng)(?:$|[_\-\.])",
    re.IGNORECASE,
)


def _guess_lang(name: str) -> str:
    m = _LANG_RE.search(name)
    if not m:
        return "en"
    tag = m.group(1).lower().replace("_", "-")
    if tag.startswith("pt"):
        return "pt"
    return {"por": "pt", "esp": "es", "fra": "fr", "ger": "de",
            "ita": "it", "eng": "en"}.get(tag, tag if tag in ("es", "fr", "de", "it", "en") else "en")


def _parse_front_matter(text: str) -> Dict[str, Any]:
    """Parse a leading YAML front-matter block into a dict (empty dict if absent/invalid)."""
    m = re.match(r"^\ufeff?---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)", text)
    if not m:
        return {}
    try:
        import yaml
        data = yaml.safe_load(m.group(1))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _strip_front_matter(text: str) -> str:
    return re.sub(r"^\ufeff?---[ \t]*\r?\n[\s\S]*?\r?\n---[ \t]*(?:\r?\n|$)", "", text, count=1)


def _clean_prose(text: str) -> str:
    """Drop PDF-extraction artifacts so descriptions/titles read like prose."""
    t = re.sub(r"\[\s*PAGE\s+\d+\s*\]", " ", text, flags=re.IGNORECASE)
    t = re.sub(r"(?:\b[A-Z]\b[ \t]+){2,}[A-Z]\b", " ", t)   # spaced-caps: "C O M P L E T E" → ""
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()


def _extract_description(text: str, limit: int = 240) -> str:
    body = _clean_prose(text)
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)     # fenced code
    body = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", body)       # links / images
    body = re.sub(r"<[^>]+>", " ", body)                         # raw html
    lines = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if re.match(r"^[-=*|:>]{3,}$", s):
            continue
        lines.append(s)
        if sum(len(x) for x in lines) > limit:
            break
    desc = re.sub(r"\s+", " ", " ".join(lines)).strip()
    if len(desc) > limit:
        cut = desc[:limit].rsplit(" ", 1)[0]
        desc = cut + "…"
    return desc


def _tags_for(title: str, path: str) -> List[str]:
    blob = f"{title} {path}".lower().replace("_", " ").replace("-", " ")
    vocab = [
        "active directory", "adversary emulation", "ai security", "api security",
        "appsec", "azure", "bash", "bug bounty", "cloud security", "cobalt strike",
        "cve", "cybersecurity career", "devsecops", "dns", "edr", "exploit development",
        "firewall", "forensics", "gcp", "hardening", "honeypot", "ics/ot", "incident response",
        "iot", "kerberos", "kubernetes", "linux", "llm", "malware analysis", "metasploit",
        "mitre att&ck", "network security", "nmap", "oscp", "osint", "owasp", "pentest report",
        "persistence", "privilege escalation", "purple team", "python", "ransomware", "red team",
        "recon", "reverse engineering", "shellcode", "soc", "sql injection", "ssh",
        "threat hunting", "tls", "tor", "vulnerability management", "web security",
        "windows", "wireshark", "wstg", "yara",
    ]
    tags = [v for v in vocab if v in blob][:8]
    sub = Path(path).parent.name
    label = {"blue_team": "blue-team", "red_team": "red-team",
             "malware_analysis": "malware-analysis", "reverse_engineering": "reverse-engineering",
             "threat_intelligence": "threat-intelligence", "unclassified": "unclassified"}.get(sub)
    if label and label not in " ".join(tags):
        tags.insert(0, label)
    return tags


# ---------------------------------------------------------------------------
# Catalog builder
# ---------------------------------------------------------------------------
def build_catalog(repo_root: Path = REPO_ROOT, generated_at: Optional[str] = None) -> Dict[str, Any]:
    """Walk the domain folders and produce the full catalog dictionary (schema v1.0.0).

    ``generated_at`` allows CI to pin a deterministic build timestamp; if omitted it is
    reused from an existing index.json when present, so pure re-indexes don't churn.
    """
    if generated_at is None:
        existing = repo_root / "index.json"
        if existing.exists():
            try:
                generated_at = json.loads(existing.read_text(encoding="utf-8")).get("generated_at")
            except Exception:
                generated_at = None
    now = generated_at or datetime.now(_TZ).isoformat(timespec="seconds")
    resources: List[Dict[str, Any]] = []
    counters = {d: {s: 0 for s in SUBDOMAINS + ["unclassified"]} for d in DOMAINS}

    for domain in DOMAINS:
        domain_dir = repo_root / domain
        if not domain_dir.is_dir():
            continue
        for md in sorted(domain_dir.rglob("*.md")):
            rel = md.relative_to(repo_root).as_posix()
            sub = md.parent.name
            if sub not in counters[domain]:
                sub = "unclassified"
            try:
                text = md.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            stat = md.stat()
            fm = _parse_front_matter(text)
            body = _strip_front_matter(text)

            def _fm(key: str, cast):
                """Return a validated front-matter override for `key`, else None."""
                val = fm.get(key)
                return val if isinstance(val, cast) and val else None

            title = _fm("title", str) or _extract_h1(body) or _title_from_filename(md.stem)
            year = _fm("year", int) or _extract_year(md.name, body)
            entry = {
                "id": hashlib.sha1(rel.encode()).hexdigest()[:12],
                "title": title,
                "path": rel,
                "domain": domain,
                "subdomain": sub,
                "type": "book" if domain == "01_literature" else ("paper" if domain == "02_papers" else "article"),
                "year": year,
                "language": (fm.get("language") if isinstance(fm.get("language"), str) else None)
                    or _guess_lang(md.stem),
                "description": (fm.get("description") if isinstance(fm.get("description"), str) else None)
                    or _extract_description(body),
                "tags": (fm.get("tags") if isinstance(fm.get("tags"), list) and fm.get("tags"))
                    or _tags_for(title, rel),
                "size_bytes": stat.st_size,
                "updated_at": datetime.fromtimestamp(stat.st_mtime, _TZ).isoformat(timespec="seconds"),
            }
            resources.append(entry)
            counters[domain][sub] += 1

    resources.sort(key=lambda r: (r["domain"], r["subdomain"], -(r["year"] or 0), r["title"].lower()))

    stats = {
        "total_resources": len(resources),
        "by_domain": {d: sum(c.values()) for d, c in counters.items()},
        "by_subdomain": {s: sum(counters[d][s] for d in DOMAINS) for s in SUBDOMAINS + ["unclassified"]},
    }

    return {
        "$schema_version": SCHEMA_VERSION,
        "repository": "BlueRingsLabs/awensome_cybersecurity",
        "organization": "BlueRingsLabs",
        "license": "MIT",
        "generated_at": now,
        "generator": "BlueRingsLabs Ingestion Pipeline (.github/scripts)",
        "taxonomy": {
            "domains": [
                {
                    "id": d,
                    "label": DOMAINS[d],
                    "subdomains": [
                        {"id": s, "label": SUBDOMAIN_LABELS[s], "count": counters[d][s]}
                        for s in SUBDOMAINS
                    ],
                }
                for d in DOMAINS
            ],
            "fallback_subdomain": "unclassified",
        },
        "stats": stats,
        "resources": resources,
    }


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------
def render_json(catalog: Dict[str, Any]) -> str:
    return json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"


class _LiteralStr(str):
    """Marker type: force YAML literal-block (|) style for long prose fields."""


def render_yaml(catalog: Dict[str, Any]) -> str:
    import yaml

    class _CatalogDumper(yaml.SafeDumper):
        """SafeDumper subclass: compact block style + literal blocks for descriptions."""

        def ignore_aliases(self, data):  # avoid anchor noise in generated files
            return True

    def _represent_dict(dumper, data):
        return dumper.represent_mapping("tag:yaml.org,2002:map", data, flow_style=False)

    def _represent_list(dumper, data):
        flow = len(data) <= 6 and all(isinstance(x, (str, int, float)) for x in data)
        return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=flow)

    def _represent_str(dumper, data):
        if isinstance(data, _LiteralStr) or len(data) > 72:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    # Register dict/list/str on the base SafeDumper as well: PyYAML resolves an
    # object's type via ``type(data).__mro__``, but *exact-type* wins first; our
    # _LiteralStr marker subclass must still find the plain `str` representer.
    yaml.SafeDumper.add_representer(dict, _represent_dict)
    yaml.SafeDumper.add_representer(list, _represent_list)
    yaml.SafeDumper.add_representer(str, _represent_str)
    _CatalogDumper.add_representer(dict, _represent_dict)
    _CatalogDumper.add_representer(list, _represent_list)
    _CatalogDumper.add_representer(str, _represent_str)
    _CatalogDumper.add_representer(_LiteralStr, _represent_str)

    doc = dict(catalog)
    doc["resources"] = [
        {**r, "description": _LiteralStr(r["description"] or "~")} for r in catalog["resources"]
    ]
    header = (
        "# ─────────────────────────────────────────────────────────────\n"
        "# BlueRingsLabs · awensome_cybersecurity — machine-readable catalog\n"
        "# ⚠️  GENERATED FILE — DO NOT EDIT BY HAND.\n"
        "#     Regenerated automatically by .github/scripts on every merge.\n"
        "# ─────────────────────────────────────────────────────────────\n"
    )
    body = yaml.dump(doc, Dumper=_CatalogDumper, sort_keys=False,
                     allow_unicode=True, default_flow_style=None, width=100)
    return header + body


def _escape_cell(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def render_readme_table(catalog: Dict[str, Any]) -> str:
    rows = [
        "| Subdomain | Title | Year | Language | Link |",
        "| :-------- | :---- | :--: | :------: | :--- |",
    ]
    for r in catalog["resources"]:
        year = str(r["year"]) if r["year"] else "—"
        href = "".join(
            f"%{ord(c):02X}" if c in "() " else c for c in r["path"]
        )
        rows.append(
            f"| `{r['subdomain']}` | {_escape_cell(r['title'])} | {year} | {r['language']} "
            f"| [📄 view]({href}) |"
        )
    total = catalog["stats"]["total_resources"]
    counts = ", ".join(f"**{v}** {k}" for k, v in catalog["stats"]["by_domain"].items())
    block = [
        README_INTRO.rstrip(),
        "",
        f"> **{total} curated resources** indexed — {counts}.",
        f"> Last automated update: `{catalog['generated_at']}`.",
        "",
        *rows,
    ]
    return "\n".join(block)


def inject_into_readme(table_md: str, readme_path: Path) -> bool:
    """Replace (or append) the managed AUTO-INDEX block in README.md. Returns changed flag."""
    original = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    replacement = f"{README_START_MARKER}\n{table_md}\n{README_END_MARKER}"
    if README_START_MARKER in original and README_END_MARKER in original:
        pre, rest = original.split(README_START_MARKER, 1)
        _, post = rest.split(README_END_MARKER, 1)
        updated = pre + replacement + post
    else:
        sep = "" if original.endswith("\n") or not original else "\n"
        updated = original + sep + "\n---\n\n" + replacement + "\n"
    if updated != original:
        readme_path.write_text(updated, encoding="utf-8")
        return True
    return False


def write_catalogs(catalog: Dict[str, Any], repo_root: Path = REPO_ROOT) -> Dict[str, bool]:
    """Write index.json + index.yaml and refresh the README table. Returns change flags."""
    changed: Dict[str, bool] = {}

    json_path = repo_root / "index.json"
    new_json = render_json(catalog)
    changed["index.json"] = (
        (not json_path.exists()) or json_path.read_text(encoding="utf-8") != new_json
    )
    if changed["index.json"]:
        json_path.write_text(new_json, encoding="utf-8")

    yaml_path = repo_root / "index.yaml"
    new_yaml = render_yaml(catalog)
    changed["index.yaml"] = (
        (not yaml_path.exists()) or yaml_path.read_text(encoding="utf-8") != new_yaml
    )
    if changed["index.yaml"]:
        yaml_path.write_text(new_yaml, encoding="utf-8")

    changed["README.md"] = inject_into_readme(render_readme_table(catalog), repo_root / "README.md")
    return changed


if __name__ == "__main__":  # quick manual smoke test: python3 catalog_lib.py
    cat = build_catalog()
    print(json.dumps(cat["stats"], indent=2))
    print(f"resources: {len(cat['resources'])}")
