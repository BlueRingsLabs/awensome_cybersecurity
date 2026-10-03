#!/usr/bin/env python3
"""
classify_and_index.py — BlueRingsLabs automated ingestion pipeline.

Pipeline stages (run on every push to ``main`` by .github/workflows/ingest_and_index.yml):

  1. DISCOVER   – find raw Markdown submissions dropped in the repository root (/).
  2. SANITIZE   – strip HTML comments / tracking junk, normalize whitespace, enforce UTF-8.
  3. CLASSIFY   – batch files into chunks and ask Gemini 2.5 Flash (official ``google-genai``
                  SDK) for a structured decision per file:
                  { domain, subdomain, title, year, language, description, tags }.
                  JSON-schema structured output + strict server-side validation; any rejected
                  item is retried once as an individual call before falling back to
                  ``03_web_and_posts/unclassified`` (never blocks the pipeline).
  4. ROUTE      – move each file to ``<domain>/<subdomain>/<YYYY>_<slug>.md`` with collision-safe
                  suffixes (_2, _3 …) and LLM-suggested renames when the original name is meaningless.
  5. INDEX      – regenerate index.json, index.yaml and the README.md AUTO-INDEX block
                  via the shared catalog_lib engine.

Resiliency & free-tier friendliness:
  * Hard cap of MAX_BATCH_FILES (default 12) resources per request → few requests, small prompts.
  * MIN_REQUEST_INTERVAL (default 5 s) between API calls → stays below 15 req/min RPM limits.
  * Exponential backoff with jitter on HTTP 429 / 503 / 500 / transport errors (up to 6 retries).
  * Fully deterministic offline mode (--offline) using a keyword classifier — used for local
    testing and as the ultimate safety net if the API is unreachable.

Usage:
    python3 classify_and_index.py [--offline] [--dry-run] [--limit N] [--verbose]

Environment:
    GEMINI_API_KEY   required for AI classification (falls back to offline mode if absent)
    GEMINI_MODEL     optional override (default: gemini-2.5-flash)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import re
import shutil
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

# Make sibling modules importable regardless of CWD (CI runs from repo root).
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import catalog_lib as lib  # noqa: E402  (shared taxonomy + catalog engine)

log = logging.getLogger("ingest")

REPO_ROOT = lib.REPO_ROOT
PROMPTS_DIR = SCRIPT_DIR / "prompts"

# ---------------------------------------------------------------------------
# Tunables (free-tier friendly)
# ---------------------------------------------------------------------------
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
MAX_BATCH_FILES = int(os.environ.get("MAX_BATCH_FILES", "12"))       # 10–15 files / call
SNIPPET_CHARS = int(os.environ.get("SNIPPET_CHARS", "1400"))          # prompt budget per file
MIN_REQUEST_INTERVAL = float(os.environ.get("MIN_REQUEST_INTERVAL", "5.0"))  # ≥12 RPM ceiling
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "6"))
BACKOFF_BASE = 2.0                                                   # 2s,4s,8s… capped at 60s + jitter
MAX_FILE_BYTES = 2_000_000                                          # skip absurdly large uploads
PROTECTED_ROOT_FILES = {"README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
                        "LICENSE", "CHANGELOG.md", "SECURITY.md"}


# ---------------------------------------------------------------------------
# Sanitization
# ---------------------------------------------------------------------------
_TRACKING_PATTERNS = [
    re.compile(r"utm_source=[^&\s\"'>]+", re.I),
    re.compile(r"utm_medium=[^&\s\"'>]+", re.I),
    re.compile(r"utm_campaign=[^&\s\"'>]+", re.I),
    re.compile(r"[?&](?:fbclid|gclid|mc_cid|mc_eid|ref=\w+)[^&\s\"'>]*", re.I),
]


def sanitize_markdown(raw: str) -> str:
    """Normalize a raw submission: encoding hygiene, comment/tracking scrub, whitespace."""
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    text = unicodedata.normalize("NFC", text)
    text = text.encode("utf-8", "ignore").decode("utf-8")
    text = re.sub(r"<!--[\s\S]*?-->", "", text)                       # HTML comments
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", "", text, flags=re.I)
    for pat in _TRACKING_PATTERNS:
        text = pat.sub("", text)
    text = re.sub(r"[ \t]+\n", "\n", text)                             # trailing spaces
    text = re.sub(r"\n{4,}", "\n\n\n", text)                           # collapse blank floods
    text = re.sub(r"\u200b|\ufeff", "", text)                          # zero-width chars
    return text.strip() + "\n"


def ensure_h1(text: str, fallback_title: str) -> str:
    """Guarantee the document opens with a single H1 so downstream indexing always has a title."""
    if re.search(r"^#\s+\S", text, re.MULTILINE):
        return text
    title = fallback_title.strip() or "Untitled resource"
    return f"# {title}\n\n{text}"


# ---------------------------------------------------------------------------
# Offline keyword classifier (fallback + local testing)
# ---------------------------------------------------------------------------
_KEYWORDS: Dict[str, List[str]] = {
    "blue_team": ["defense", "detection", "incident response", "soc", "siem", "hardening",
                  "security operation center", "monitoring", "log analysis", "dfir",
                  "firewall", "zero trust", "governance", "compliance", "risk management"],
    "red_team": ["pentest", "penetration test", "red team", "exploit", "privilege escalation",
                 "lateral movement", "bug bounty", "oscp", "metasploit", "cobalt strike",
                 "adversary simulation", "kerberoast", "c2 ", "payload", "evasion"],
    "malware_analysis": ["malware", "ransomware", "reverse engineering malware", "yara",
                         "sandbox", "static analysis", "dynamic analysis", "trojan", "rootkit",
                         "botnet", "forensic", "memory analysis"],
    "reverse_engineering": ["reverse engineer", "disassembl", "decompil", "shellcode",
                            "buffer overflow", "assembly", "gdb", "ida pro", "ghidra",
                            "binary analysis", "ollydbg", "x64dbg", "crackme"],
    "threat_intelligence": ["threat intel", "osint", "apt ", "threat hunt", "cti",
                            "dark web", "tor ", "anonymity", "privacy", "maltego",
                            "shodan", "recon", "att&ck", "mitre", "indicator of compromise"],
}


def offline_classify(filename: str, text: str) -> Dict[str, Any]:
    blob = (filename + " " + text[:4000]).lower().replace("_", " ").replace("-", " ")
    scores = {k: sum(blob.count(t) for t in v) for k, v in _KEYWORDS.items()}
    sub = max(scores, key=scores.get) if max(scores.values()) > 0 else "unclassified"
    words = re.sub(r"\.(md|markdown)$", "", filename)
    words = re.sub(r"^\d{4}[-_]", "", words).replace("_", " ").replace("-", " ").strip()
    m = re.match(r"^(19|20)\d{2}(?=[-_])", filename)
    year = int(m.group(0)) if m else None
    return {
        "domain": "03_web_and_posts",
        "subdomain": sub,
        "title": words.title() if words else "Untitled resource",
        "year": year,
        "language": "pt" if re.search(r"\b(pt|br|portugu[eê]s)\b", blob) else "en",
        "description": " ".join(blob.split())[:200],
        "tags": [sub.replace("_", "-")],
        "confidence": 0.3,
        "rename_recommended": False,
    }


# ---------------------------------------------------------------------------
# Gemini client (official google-genai SDK)
# ---------------------------------------------------------------------------
_RESPONSE_SCHEMA = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "file_id": {"type": "INTEGER"},
            "domain": {"type": "STRING", "enum": lib.VALID_TARGET_DOMAINS},
            "subdomain": {"type": "STRING", "enum": lib.VALID_TARGET_SUBDOMAINS},
            "title": {"type": "STRING"},
            "year": {"type": "INTEGER"},
            "language": {"type": "STRING"},
            "description": {"type": "STRING"},
            "tags": {"type": "ARRAY", "items": {"type": "STRING"}},
            "confidence": {"type": "NUMBER"},
            "rename_recommended": {"type": "BOOLEAN"},
        },
        "required": ["file_id", "domain", "subdomain", "title", "language", "description", "tags"],
    },
}


class GeminiClassifier:
    """Thin, resilient wrapper around Gemini 2.5 Flash with structured JSON output."""

    def __init__(self, system_prompt: str) -> None:
        from google import genai  # deferred: allows --offline runs without the SDK installed

        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        self.client = genai.Client(api_key=api_key)
        self.system_prompt = system_prompt
        self._last_call_ts = 0.0

    # -- rate limiting ------------------------------------------------------
    def _throttle(self) -> None:
        wait = MIN_REQUEST_INTERVAL - (time.monotonic() - self._last_call_ts)
        if wait > 0:
            time.sleep(wait)
        self._last_call_ts = time.monotonic()

    # -- retry w/ exponential backoff ---------------------------------------
    @staticmethod
    def _is_retryable(exc: Exception) -> bool:
        status = getattr(exc, "code", None) or getattr(getattr(exc, "response", None), "status_code", None)
        try:
            status = int(status)
        except (TypeError, ValueError):
            status = None
        if status in (429, 500, 502, 503, 504):
            return True
        msg = str(exc).lower()
        return any(h in msg for h in ("429", "rate limit", "resource exhausted",
                                      "quota", "unavailable", "deadline exceeded",
                                      "timed out", "timeout", "connection reset"))

    def _call_with_retry(self, contents: str) -> Optional[str]:
        from google.genai import types

        for attempt in range(1, MAX_RETRIES + 1):
            self._throttle()
            try:
                resp = self.client.models.generate_content(
                    model=MODEL_NAME,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_prompt,
                        response_mime_type="application/json",
                        response_schema=_RESPONSE_SCHEMA,
                        temperature=0.1,
                        max_output_tokens=8192,
                    ),
                )
                text = (resp.text or "").strip()
                if text.startswith("```"):                      # defensive: fenced JSON
                    text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", text)
                return text
            except Exception as exc:  # noqa: BLE001 - we classify below
                if not self._is_retryable(exc) or attempt == MAX_RETRIES:
                    log.warning("Gemini call failed permanently: %s", exc)
                    return None
                delay = min(BACKOFF_BASE * (2 ** (attempt - 1)), 60) + random.uniform(0, 1.5)
                log.warning("Transient API error (attempt %d/%d): %s — backing off %.1fs",
                            attempt, MAX_RETRIES, exc, delay)
                time.sleep(delay)
        return None

    # -- public API ----------------------------------------------------------
    def classify_batch(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        payload = json.dumps(
            [{"file_id": it["file_id"], "filename": it["filename"], "snippet": it["snippet"]}
             for it in items],
            ensure_ascii=False,
        )
        raw = self._call_with_retry(payload)
        return self._parse_response(raw, items)

    @staticmethod
    def _parse_response(raw: Optional[str], items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not raw:
            return []
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            m = re.search(r"\[[\s\S]*\]", raw)
            if not m:
                return []
            try:
                data = json.loads(m.group(0))
            except json.JSONDecodeError:
                return []
        if isinstance(data, dict):                              # tolerate {"classifications":[...]}
            data = data.get("classifications") or data.get("results") or [data]
        if not isinstance(data, list):
            return []
        by_id = {it["file_id"]: it for it in items}
        out = []
        for obj in data:
            if not isinstance(obj, dict):
                continue
            fid = obj.get("file_id")
            if fid not in by_id:                                # hallucinated id → drop, will fall back
                continue
            out.append(validate_decision(obj, by_id[fid]["filename"]))
        return out


# ---------------------------------------------------------------------------
# Strict validation of one LLM decision
# ---------------------------------------------------------------------------
_YEAR_RE = re.compile(r"^(19|20)\d{2}")


def validate_decision(obj: Dict[str, Any], original_filename: str) -> Optional[Dict[str, Any]]:
    """Return a sanitized decision dict or None if unusable."""
    domain = str(obj.get("domain", "")).strip()
    subdomain = str(obj.get("subdomain", "")).strip()
    if domain not in lib.VALID_TARGET_DOMAINS:
        domain = "03_web_and_posts"
    if subdomain not in lib.VALID_TARGET_SUBDOMAINS:
        subdomain = "unclassified"
    title = str(obj.get("title", "")).strip() or lib._title_from_filename(
        Path(original_filename).stem)
    lang = str(obj.get("language", "en")).strip().lower()[:5] or "en"

    year = obj.get("year")
    if isinstance(year, str):
        m = _YEAR_RE.match(year.strip())
        year = int(m.group(0)) if m else None
    if isinstance(year, int) and not (1980 <= year <= 2030):
        year = None
    if year is None:                                            # salvage year from the filename
        m = re.match(r"^(19|20)\d{2}(?=[-_])", original_filename)
        year = int(m.group(0)) if m else None

    tags = obj.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    tags = [str(t).strip().lower().replace(" ", "-") for t in tags if str(t).strip()][:10]

    desc = re.sub(r"\s+", " ", str(obj.get("description", ""))).strip()[:280]

    try:
        conf = float(obj.get("confidence", 0.5))
    except (TypeError, ValueError):
        conf = 0.5
    conf = max(0.0, min(conf, 1.0))

    return {
        "domain": domain,
        "subdomain": subdomain,
        "title": title[:160],
        "year": year,
        "language": lang,
        "description": desc,
        "tags": tags,
        "confidence": conf,
        "rename_recommended": bool(obj.get("rename_recommended", False)),
    }


# ---------------------------------------------------------------------------
# Routing / file placement
# ---------------------------------------------------------------------------
def unique_destination(dest_dir: Path, base_name: str, ext: str) -> Path:
    """Collision-safe path: foo.md → foo_2.md → foo_3.md …"""
    candidate = dest_dir / f"{base_name}{ext}"
    n = 2
    while candidate.exists():
        candidate = dest_dir / f"{base_name}_{n}{ext}"
        n += 1
    return candidate


def build_base_name(decision: Dict[str, Any], original_path: Path) -> str:
    stem = original_path.stem
    slug = lib.slugify(stem)
    meaningful = len(re.sub(r"^\d{4}[-_]?", "", stem).strip("-_ ")) >= 6 and slug != "untitled"
    if not meaningful or decision.get("rename_recommended"):
        slug = lib.slugify(decision["title"])
    year = decision.get("year")
    prefix = f"{year}_" if year else ""
    return f"{prefix}{slug}"


def route_file(src: Path, decision: Dict[str, Any], dry_run: bool = False) -> Optional[Path]:
    dest_dir = REPO_ROOT / decision["domain"] / decision["subdomain"]
    ext = src.suffix.lower() or ".md"
    if dry_run:
        return dest_dir / f"{build_base_name(decision, src)}{ext}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = unique_destination(dest_dir, build_base_name(decision, src), ext)
    shutil.move(str(src), str(dest))
    return dest


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------
def discover_root_submissions() -> List[Path]:
    """Raw Markdown files sitting directly in the repository root (excluding protected docs)."""
    out = []
    for p in sorted(REPO_ROOT.iterdir()):
        if not p.is_file():
            continue
        if p.name in PROTECTED_ROOT_FILES or p.name.startswith("."):
            continue
        if p.suffix.lower() in (".md", ".markdown", ".txt"):
            out.append(p)
    return out


def load_snippet(path: Path) -> Optional[str]:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            log.warning("Skipping oversized file %s (%d bytes)", path.name, path.stat().st_size)
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        log.error("Cannot read %s: %s", path, exc)
        return None


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run_pipeline(offline: bool, dry_run: bool, limit: Optional[int], verbose: bool) -> int:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
    )

    submissions = discover_root_submissions()
    if limit:
        submissions = submissions[:limit]

    print(f"🔎 Found {len(submissions)} raw submission(s) in repository root")
    for p in submissions:
        print(f"   • {p.name}")

    summary: Counter = Counter()
    moved: List[Path] = []

    if submissions:
        # ---- Stage 1+2: sanitize in place ---------------------------------
        work_items: List[Dict[str, Any]] = []
        for fid, path in enumerate(submissions):
            text = load_snippet(path)
            if text is None:
                summary["skipped"] += 1
                continue
            clean = sanitize_markdown(text)
            clean = ensure_h1(clean, lib._title_from_filename(path.stem))
            if not dry_run:
                path.write_text(clean, encoding="utf-8")
            snippet = re.sub(r"\s+", " ", clean)[:SNIPPET_CHARS]
            work_items.append({"file_id": fid, "path": path, "filename": path.name,
                               "text": clean, "snippet": snippet})

        # ---- Stage 3: classify --------------------------------------------
        decisions: Dict[int, Dict[str, Any]] = {}
        classifier: Optional[GeminiClassifier] = None
        use_ai = not offline and bool(os.environ.get("GEMINI_API_KEY", "").strip())
        if use_ai:
            try:
                system_prompt = (PROMPTS_DIR / "classification_prompt.md").read_text(encoding="utf-8")
                classifier = GeminiClassifier(system_prompt)
            except Exception as exc:  # missing SDK / bad key → deterministic fallback
                log.error("Gemini init failed (%s) — switching to offline classifier", exc)
                classifier = None
        if classifier is None:
            print("🧠 Classification backend: OFFLINE keyword heuristic"
                  if offline or not os.environ.get("GEMINI_API_KEY")
                  else "🧠 Classification backend: OFFLINE keyword heuristic (AI unavailable)")

        batches = [work_items[i:i + MAX_BATCH_FILES] for i in range(0, len(work_items), MAX_BATCH_FILES)]
        for bi, batch in enumerate(batches, 1):
            got: Dict[int, Dict[str, Any]] = {}
            if classifier:
                print(f"🤖 Batch {bi}/{len(batches)} → Gemini ({len(batch)} files)")
                for d in classifier.classify_batch(batch):
                    got[d["file_id"]] = d
                # Re-query individually anything missing/rejected (one extra chance)
                leftovers = [it for it in batch if it["file_id"] not in got]
                for it in leftovers:
                    for d in classifier.classify_batch([it]):
                        got.setdefault(d["file_id"], d)
            for it in batch:
                dec = got.get(it["file_id"])
                if dec is None:
                    dec = offline_classify(it["filename"], it["text"])
                    dec["_source"] = "offline-fallback"
                    summary["offline_fallback"] += 1
                else:
                    dec["_source"] = "gemini"
                    summary["ai_classified"] += 1
                decisions[it["file_id"]] = dec

        # ---- Stage 4: route + metadata front-matter -----------------------
        for it in work_items:
            dec = decisions[it["file_id"]]
            dest = route_file(it["path"], dec, dry_run=dry_run)
            if dest is None:
                summary["failed"] += 1
                continue
            if not dry_run:
                fm = {
                    "title": dec["title"],
                    "domain": dec["domain"],
                    "subdomain": dec["subdomain"],
                    "year": dec.get("year"),
                    "language": dec["language"],
                    "description": dec["description"],
                    "tags": dec["tags"],
                    "confidence": dec["confidence"],
                    "classifier": dec["_source"],
                    "original_filename": it["filename"],
                }
                body = it["text"]
                # yaml-safe front-matter serialization (PyYAML is a pipeline dependency)
                import yaml
                front = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                                                 default_flow_style=False) + "---\n\n"
                dest.write_text(front + body, encoding="utf-8")
                moved.append(dest.relative_to(REPO_ROOT))
            summary["routed"] += 1
            print(f"   ➜ {it['filename']}  ⇒  {dest.relative_to(REPO_ROOT)} "
                  f"[{dec['subdomain']}] ({dec['_source']}, conf={dec['confidence']:.2f})")

    # ---- Stage 5: rebuild catalogs ----------------------------------------
    catalog = lib.build_catalog(REPO_ROOT)
    if dry_run:
        print(f"🗂️  Dry-run: would rewrite index.json/index.yaml/README for {catalog['stats']['total_resources']} resources")
    else:
        changed = lib.write_catalogs(catalog, REPO_ROOT)
        print("🗂️  Catalog regenerated:",
              ", ".join(f"{k}:{'updated' if v else 'unchanged'}" for k, v in changed.items()))

    print("\n📊 Pipeline summary:", dict(summary) or "nothing to ingest")
    if moved:
        print("✅ Files organized:")
        for m in moved:
            print(f"   {m}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest, classify and index root submissions.")
    parser.add_argument("--offline", action="store_true", help="skip Gemini, use keyword classifier")
    parser.add_argument("--dry-run", action="store_true", help="no writes/moves, preview only")
    parser.add_argument("--limit", type=int, default=None, help="max files to process this run")
    parser.add_argument("--verbose", action="store_true", help="debug logging")
    args = parser.parse_args()
    return run_pipeline(args.offline, args.dry_run, args.limit, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
