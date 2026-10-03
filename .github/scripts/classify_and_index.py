#!/usr/bin/env python3
"""
classify_and_index.py -- AI ingestion pipeline for the
BlueRingsLabs/awensome_cybersecurity knowledge base.

Workflow (runs in GitHub Actions on every push to `main`):

    1. Discover raw Markdown files uploaded by contributors to the repository
       ROOT directory (excluding managed files such as README.md, LICENSE,
       CONTRIBUTING.md, CODE_OF_CONDUCT.md and the catalogs themselves).
    2. Sanitize each file: strip control characters, normalize whitespace,
       fix broken heading levels, remove tracking junk and binary noise.
    3. Batch the files (default 12 per request) and ask Gemini 2.5 Flash
       (official `google-genai` SDK) to classify each one using STRICT JSON
       structured output: target domain, subdomain, sanitized filename,
       title, tags, language and a short summary.
    4. Validate the model response against the taxonomy, move the files into
       their destination folders (`0X_domain/subdomain/sanitized_filename.md`)
       and persist the AI metadata so the catalog generator can pick it up.
    5. Regenerate index.json, index.yaml and the AUTO-INDEX block of README.md
       via the shared `build_index.py` module.

Resiliency:
    * Client-side pacing (~5 s between calls, i.e. <= 12 req/min) to respect
      the Google AI Studio free tier (15 RPM).
    * Exponential backoff + jitter retries on HTTP 429 / transient errors.
    * Per-batch fallback: if a batch fails after all retries, its files are
      routed with deterministic keyword heuristics instead of blocking the run.
    * Idempotent: safe to re-run; collisions get a numeric suffix.

Configuration (environment variables):
    GEMINI_API_KEY            required when raw files exist in root
    GEMINI_MODEL              default: gemini-2.5-flash
    KB_BATCH_SIZE             files per LLM call          (default 12)
    KB_MIN_CALL_INTERVAL_SEC  pacing between LLM calls    (default 5.0)
    KB_MAX_RETRIES            retry attempts per batch    (default 5)
    KB_DRY_RUN                classify but do not move/write (default false)
    KB_REPO_ROOT              repository root             (default: detected)

Author: Blue Rings Labs
License: MIT
"""

from __future__ import annotations

import json
import logging
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

# Make the sibling module importable both locally and inside GitHub Actions.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_index as bi  # noqa: E402  (shared taxonomy + catalog generator)

REPO_ROOT = Path(os.environ.get("KB_REPO_ROOT", SCRIPT_DIR.parents[1])).resolve()

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
BATCH_SIZE = max(1, int(os.environ.get("KB_BATCH_SIZE", "12")))
MIN_CALL_INTERVAL_SEC = float(os.environ.get("KB_MIN_CALL_INTERVAL_SEC", "5.0"))
MAX_RETRIES = max(1, int(os.environ.get("KB_MAX_RETRIES", "5")))
DRY_RUN = os.environ.get("KB_DRY_RUN", "false").lower() in ("1", "true", "yes")
CONTENT_SAMPLE_CHARS = 4000

# Managed root files that must never be treated as raw submissions.
PROTECTED_ROOT_FILES = {
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "LICENSE",
    "index.json",
    "index.yaml",
}

RAW_METADATA_FILE = REPO_ROOT / ".github" / "scripts" / ".ingest_metadata.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("ingest")


# ---------------------------------------------------------------------------
# Discovery & sanitization
# ---------------------------------------------------------------------------

def find_raw_files(repo_root: Path) -> list[Path]:
    """Markdown files sitting directly in the repository root."""
    candidates = [
        p
        for p in sorted(repo_root.glob("*.md"))
        if p.is_file() and p.name not in PROTECTED_ROOT_FILES
    ]
    return candidates


_CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_TRAILING_WS_RE = re.compile(r"[ \t]+$", re.MULTILINE)
_MULTI_BLANK_RE = re.compile(r"\n{4,}")
_PAGE_NOISE_RE = re.compile(r"^\s*\[\[\s*PAGE\s+\d+\s*\]\]\s*$", re.IGNORECASE | re.MULTILINE)
_TRACKING_QUERY_RE = re.compile(
    r"(\?|&)(utm_[a-z]+|fbclid|gclid|ref)=[^\s)\]]+", re.IGNORECASE
)


def sanitize_markdown(text: str) -> str:
    """Normalize raw contributor notes into clean repository Markdown."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _CONTROL_CHARS_RE.sub("", text)
    text = _PAGE_NOISE_RE.sub("", text)
    text = _TRACKING_QUERY_RE.sub("", text)
    text = _TRAILING_WS_RE.sub("", text)
    text = _MULTI_BLANK_RE.sub("\n\n", text)
    return text.strip() + "\n"


def ensure_title(text: str, fallback_stem: str) -> str:
    """Guarantee the document starts with an H1 title for catalog extraction."""
    if re.search(r"^\s{0,3}#\s+\S", text, re.MULTILINE):
        return text
    title = bi._humanize(fallback_stem)
    return f"# {title}\n\n{text.lstrip()}"


# ---------------------------------------------------------------------------
# Structured-output schema (Gemini responseSchema)
# ---------------------------------------------------------------------------

RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "OBJECT",
    "properties": {
        "classifications": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "source_filename": {"type": "STRING"},
                    "domain": {
                        "type": "STRING",
                        "enum": list(bi.VALID_DOMAINS),
                    },
                    "subdomain": {
                        "type": "STRING",
                        "enum": list(bi.VALID_SUBDOMAINS),
                    },
                    "filename": {
                        "type": "STRING",
                        "description": (
                            "Sanitized snake_case ASCII slug ending in .md, "
                            "derived from the resource title, optionally "
                            "prefixed with a 4-digit year."
                        ),
                    },
                    "title": {"type": "STRING"},
                    "tags": {"type": "ARRAY", "items": {"type": "STRING"}},
                    "language": {"type": "STRING", "enum": ["en", "es", "pt", "other"]},
                    "summary": {"type": "STRING"},
                    "confidence": {"type": "NUMBER"},
                },
                "required": [
                    "source_filename",
                    "domain",
                    "subdomain",
                    "filename",
                    "title",
                    "tags",
                    "language",
                    "summary",
                    "confidence",
                ],
            },
        }
    },
    "required": ["classifications"],
}

SYSTEM_PROMPT = f"""You are the automated librarian of the BlueRingsLabs
"awensome_cybersecurity" knowledge base. For every raw Markdown submission you
must classify it into the fixed taxonomy below and propose a sanitized
snake_case filename ending in .md.

DOMAINS (resource type):
{json.dumps(bi.DOMAINS, indent=2)}

SUBDOMAINS (threat topic):
{json.dumps({k: v['description'] for k, v in bi.SUBDOMAINS.items()}, indent=2)}

Rules:
- Pick exactly one domain and one subdomain per file. Use "unclassified" only
  when the content is genuinely off-topic for cybersecurity.
- Heuristic for domain: books/long theoretical notes -> 01_literature;
  research papers/whitepapers/framework studies -> 02_papers;
  blog posts/tutorials/short web notes/tool usage guides -> 03_web_and_posts.
- filename: lowercase ASCII, digits and underscores only, max 60 chars,
  descriptive, ends with ".md". If the document states a publication year,
  prefix it (e.g. 2024_linux_privilege_escalation.md).
- tags: 3 to 8 concise kebab-case topics.
- summary: one sentence, max 200 chars, neutral tone.
- confidence: your self-assessed certainty between 0.0 and 1.0.
- Never invent content; classify strictly from what is provided.
"""


def build_batch_prompt(files: list[tuple[str, str]]) -> str:
    parts = [
        "Classify the following raw Markdown submissions. Return one "
        "classification object per file, echoing each source_filename exactly.",
        "",
    ]
    for name, content in files:
        sample = content[:CONTENT_SAMPLE_CHARS]
        parts.append(f"--- BEGIN FILE: {name} ---")
        parts.append(sample)
        parts.append(f"--- END FILE: {name} ---")
        parts.append("")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Gemini client (official google-genai SDK)
# ---------------------------------------------------------------------------

def create_client():
    """Instantiate the google-genai Client. Raises ImportError if missing."""
    from google import genai  # imported lazily so --check works without SDK

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it as a repository secret."
        )
    return genai.Client(api_key=api_key)


def _is_retryable(exc: Exception) -> bool:
    text = f"{type(exc).__name__}: {exc}".lower()
    markers = (
        "429",
        "rate limit",
        "quota",
        "resource exhausted",
        "unavailable",
        "deadline exceeded",
        "timeout",
        "timed out",
        "connection reset",
        "connection aborted",
        "server error",
        "internal error",
        "overloaded",
        "500",
        "502",
        "503",
    )
    return any(m in text for m in markers)


_last_call_ts = 0.0


def _pace() -> None:
    """Client-side rate limiting: enforce MIN_CALL_INTERVAL_SEC between calls."""
    global _last_call_ts
    elapsed = time.monotonic() - _last_call_ts
    wait = MIN_CALL_INTERVAL_SEC - elapsed
    if wait > 0:
        log.info("Pacing: sleeping %.1fs (free-tier rate limit)", wait)
        time.sleep(wait)
    _last_call_ts = time.monotonic()


def generate_classifications(client, files: list[tuple[str, str]]) -> list[dict[str, Any]]:
    """Call Gemini with structured output; retry with exponential backoff."""
    from google.genai import types

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.1,
        max_output_tokens=8192,
        response_mime_type="application/json",
        response_schema=RESPONSE_SCHEMA,
    )
    prompt = build_batch_prompt(files)

    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            _pace()
            response = client.models.generate_content(
                model=GEMINI_MODEL, contents=prompt, config=config
            )
            payload = response.parsed if hasattr(response, "parsed") else None
            if payload is None:  # fall back to raw text JSON
                payload = json.loads(response.text)
            items = payload.get("classifications", [])
            if isinstance(items, list) and items:
                return items
            raise ValueError("empty classifications array in model response")
        except Exception as exc:  # noqa: BLE001 - we filter by retryability
            last_error = exc
            if _is_retryable(exc):
                backoff = min(60.0, (2 ** (attempt - 1)) + random.uniform(0, 2))
                log.warning(
                    "Batch attempt %d/%d failed (retryable: %s); backing off %.1fs",
                    attempt, MAX_RETRIES, exc, backoff,
                )
                time.sleep(backoff)
                continue
            # Non-retryable (auth, bad request...) - no point retrying.
            log.error("Batch attempt %d failed (non-retryable): %s", attempt, exc)
            break

    raise RuntimeError(f"Gemini batch failed after {MAX_RETRIES} attempts: {last_error}")


# ---------------------------------------------------------------------------
# Validation & routing
# ---------------------------------------------------------------------------

_SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9._\- ]+\.md$")


def validate_result(item: dict[str, Any], expected_names: set[str]) -> dict[str, Any] | None:
    """Hard-validate one classification object; returns None when unusable."""
    try:
        name = str(item.get("source_filename", "")).strip()
        domain = str(item.get("domain", "")).strip()
        subdomain = str(item.get("subdomain", "")).strip()
        filename = str(item.get("filename", "")).strip()
        title = str(item.get("title", "")).strip()
        if name not in expected_names:
            return None
        if domain not in bi.VALID_DOMAINS:
            domain = "03_web_and_posts"
        if subdomain not in bi.VALID_SUBDOMAINS or subdomain == "unclassified":
            subdomain = "unclassified" if subdomain not in bi.VALID_SUBDOMAINS else subdomain
        if not _SAFE_NAME_RE.match(filename):
            filename = bi.slugify(title or Path(name).stem) + ".md"
        # Defensive: never allow path traversal through model-provided names.
        if "/" in filename or ".." in filename:
            filename = bi.slugify(Path(filename).stem) + ".md"
        tags = item.get("tags", [])
        if not isinstance(tags, list):
            tags = []
        tags = [bi.slugify(str(t), 30) for t in tags][:8]
        try:
            confidence = max(0.0, min(1.0, float(item.get("confidence", 0.5))))
        except (TypeError, ValueError):
            confidence = 0.5
        language = str(item.get("language", "en")).strip().lower()
        if language not in ("en", "es", "pt", "other"):
            language = "other"
        return {
            "source_filename": name,
            "domain": domain,
            "subdomain": subdomain,
            "filename": filename.lower(),
            "title": title[:160],
            "tags": tags,
            "language": language,
            "summary": str(item.get("summary", "")).strip()[:280],
            "confidence": confidence,
        }
    except Exception:  # noqa: BLE001
        return None


def heuristic_fallback(path: Path) -> dict[str, Any]:
    """Deterministic routing when the LLM cannot classify a file."""
    stem = path.stem
    title = bi.extract_title(path)
    tags = bi.derive_tags(stem, title)
    haystack = f"{stem} {title} {' '.join(tags)}".lower()
    if any(t in haystack for t in ("red-team", "penetration-testing", "exploit")):
        sub = "red_team"
    elif "malware" in haystack or "forensics" in haystack:
        sub = "malware_analysis"
    elif "reverse-engineering" in haystack:
        sub = "reverse_engineering"
    elif "osint" in haystack or "threat-intelligence" in haystack:
        sub = "threat_intelligence"
    elif "blue-team" in haystack:
        sub = "blue_team"
    else:
        sub = "unclassified"
    # Preserve a leading publication year (e.g. "2024 - ...") in the slug.
    year_prefix = ""
    year_match = re.match(r"(19|20)\d{2}", stem)
    if year_match:
        year_prefix = year_match.group(0) + "_"
    return {
        "source_filename": path.name,
        "domain": "03_web_and_posts",
        "subdomain": sub,
        "filename": year_prefix + bi.slugify(stem, 60) + ".md",
        "title": title[:160],
        "tags": tags,
        "language": bi.detect_language(path),
        "summary": "",
        "confidence": 0.0,
    }


def unique_destination(dest_dir: Path, filename: str) -> Path:
    """Avoid clobbering existing resources: append -1, -2 ... on collision."""
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate
    stem, dot, ext = filename.rpartition(".")
    for i in range(1, 1000):
        candidate = dest_dir / f"{stem}-{i}.{ext}"
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not allocate unique name for {filename}")


# ---------------------------------------------------------------------------
# Metadata persistence (bridges AI results into build_index.py)
# ---------------------------------------------------------------------------

def load_ingest_metadata() -> dict[str, dict[str, Any]]:
    if RAW_METADATA_FILE.is_file():
        try:
            return json.loads(RAW_METADATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_ingest_metadata(meta: dict[str, dict[str, Any]]) -> None:
    RAW_METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    RAW_METADATA_FILE.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def apply_ai_metadata(catalog: dict[str, Any]) -> dict[str, Any]:
    """Overlay stored AI metadata onto freshly scanned catalog entries."""
    meta = load_ingest_metadata()
    enriched = 0
    for entry in catalog["entries"]:
        m = meta.get(entry["path"])
        if not m:
            continue
        if m.get("title"):
            entry["title"] = m["title"]
        if m.get("tags"):
            entry["tags"] = m["tags"]
        if m.get("language"):
            entry["language"] = m["language"]
        if m.get("summary"):
            entry["summary"] = m["summary"]
        entry["classification_confidence"] = m.get("confidence", 0.0)
        entry["source"] = "ai-pipeline"
        enriched += 1
    catalog["counts"]["ai_enriched"] = enriched
    return catalog


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def process_batch(client, batch: list[Path], expected: set[str]) -> list[dict[str, Any]]:
    pairs = [(p.name, sanitize_markdown(p.read_text(encoding="utf-8", errors="ignore"))) for p in batch]
    try:
        raw_items = generate_classifications(client, pairs)
    except RuntimeError as exc:
        log.error("Falling back to heuristics for batch of %d files: %s", len(batch), exc)
        return [heuristic_fallback(p) for p in batch]

    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    by_name = {p.name: p for p in batch}
    for item in raw_items:
        validated = validate_result(item, expected)
        if validated and validated["source_filename"] in by_name:
            # Duplicate hallucinations: keep first occurrence.
            if validated["source_filename"] in seen:
                continue
            seen.add(validated["source_filename"])
            results.append(validated)
    # Any file the model forgot gets the deterministic fallback.
    for p in batch:
        if p.name not in seen:
            log.warning("Model omitted %s; using heuristic fallback", p.name)
            results.append(heuristic_fallback(p))
    return results


def move_and_record(src: Path, result: dict[str, Any], repo_root: Path,
                    ingest_meta: dict[str, dict[str, Any]]) -> None:
    dest_dir = repo_root / result["domain"] / result["subdomain"]
    dest_dir.mkdir(parents=True, exist_ok=True)

    content = sanitize_markdown(src.read_text(encoding="utf-8", errors="ignore"))
    content = ensure_title(content, Path(result["filename"]).stem)

    dest = unique_destination(dest_dir, result["filename"])
    dest.write_text(content, encoding="utf-8")
    if not DRY_RUN:
        src.unlink()

    rel = dest.relative_to(repo_root).as_posix()
    ingest_meta[rel] = {
        "original_filename": src.name,
        "title": result["title"],
        "tags": result["tags"],
        "language": result["language"],
        "summary": result["summary"],
        "confidence": result["confidence"],
        "classified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    log.info("Routed %s -> %s (%.0f%% confidence)", src.name, rel,
             result["confidence"] * 100)


def main() -> int:
    log.info("Repository root: %s (dry_run=%s)", REPO_ROOT, DRY_RUN)
    raw_files = find_raw_files(REPO_ROOT)
    log.info("Raw submissions found in root: %d", len(raw_files))

    if raw_files:
        try:
            client = create_client()
        except (ImportError, RuntimeError) as exc:
            log.error(
                "Cannot initialize Gemini client (%s). Files remain in root; "
                "the next pipeline run will retry them.", exc
            )
            # Still regenerate indexes so README/catalogs reflect current tree.
            catalog = bi.scan_repository(REPO_ROOT)
            catalog = apply_ai_metadata(catalog)
            if not DRY_RUN:
                bi.write_catalog(catalog, REPO_ROOT)
            return 1

        ingest_meta = load_ingest_metadata()
        moved = 0
        for i in range(0, len(raw_files), BATCH_SIZE):
            batch = raw_files[i : i + BATCH_SIZE]
            expected = {p.name for p in batch}
            log.info("Processing batch %d-%d of %d files",
                     i + 1, i + len(batch), len(raw_files))
            results = process_batch(client, batch, expected)
            for p in batch:
                match = next((r for r in results if r["source_filename"] == p.name), None)
                if match is None:
                    match = heuristic_fallback(p)
                if DRY_RUN:
                    log.info("[dry-run] would route %s -> %s/%s/%s",
                             p.name, match["domain"], match["subdomain"],
                             match["filename"])
                    continue
                move_and_record(p, match, REPO_ROOT, ingest_meta)
                moved += 1

        if not DRY_RUN:
            save_ingest_metadata(ingest_meta)
            log.info("Classified and moved %d file(s)", moved)

    if DRY_RUN:
        log.info("Dry run complete; indexes untouched.")
        return 0

    catalog = bi.scan_repository(REPO_ROOT)
    catalog = apply_ai_metadata(catalog)
    bi.write_catalog(catalog, REPO_ROOT)
    log.info(
        "Indexes regenerated: %d total resources (%d AI-enriched).",
        catalog["counts"]["total_resources"],
        catalog["counts"].get("ai_enriched", 0),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
