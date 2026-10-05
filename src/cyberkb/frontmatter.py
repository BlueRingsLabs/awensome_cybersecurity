"""YAML front matter: the single source of truth for a resource's metadata.

v1 kept AI metadata in a hidden sidecar (``.ingest_metadata.json``) and in
the previous ``index.json``, which made the catalog depend on its own past
output. In v2 every library document carries its metadata in front matter,
so the catalog is a pure function of the tree, metadata survives moves and
renames, and a maintainer can fix a classification by editing one file.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING, Any, Literal, cast, override

import yaml

from cyberkb.errors import FrontMatterError
from cyberkb.yamlsafe import safe_load

if TYPE_CHECKING:
    from collections.abc import Mapping

    from cyberkb.taxonomy import Taxonomy

__all__ = [
    "CLASSIFICATION_METHODS",
    "CONTRIBUTOR_KEYS",
    "ID_RE",
    "LICENSE_RE",
    "Classification",
    "FrontMatter",
    "dump_front_matter",
    "parse_front_matter",
    "render_document",
    "split_front_matter",
    "validate_contributor_hints",
]

MAX_FRONT_MATTER_BYTES = 16_384
MAX_TITLE = 200
MAX_SUMMARY = 400
MAX_TAGS = 10
MAX_AUTHORS = 20
MAX_AUTHOR_LEN = 120
MAX_URL = 2048

ID_RE = re.compile(r"^ckb-[0-9a-f]{12}$")
LICENSE_RE = re.compile(r"^(?:NOASSERTION|LicenseRef-[A-Za-z0-9.-]+|[A-Za-z0-9][A-Za-z0-9.+-]*)$")
_URL_RE = re.compile(r"^https?://[^\s<>\"']+$", re.IGNORECASE)
_DELIM_RE = re.compile(r"^(?:---|\.\.\.)[ \t]*$")

ClassificationMethod = Literal["llm", "heuristic", "manual"]
CLASSIFICATION_METHODS: tuple[ClassificationMethod, ...] = ("llm", "heuristic", "manual")

#: Keys a contributor may set on a raw submission to steer ingestion.
CONTRIBUTOR_KEYS = frozenset(
    {
        "title",
        "category",
        "format",
        "language",
        "tags",
        "summary",
        "authors",
        "source_url",
        "license",
    },
)
# ``reference_only`` is a maintainer decision (it governs redistribution policy),
# so it is a library key but not a contributor-settable hint.
_LIBRARY_KEYS = CONTRIBUTOR_KEYS | {"id", "added", "classification", "reference_only"}
_REQUIRED_KEYS = frozenset(
    {"id", "title", "category", "format", "language", "license", "added", "classification"}
)


@dataclass(frozen=True, slots=True)
class Classification:
    """How (and how confidently) a resource was classified."""

    method: ClassificationMethod
    confidence: float
    model: str | None = None


@dataclass(frozen=True, slots=True)
class FrontMatter:
    """Validated metadata of one library resource."""

    id: str
    title: str
    category: str
    format: str
    language: str
    license: str
    added: date
    classification: Classification
    tags: tuple[str, ...] = ()
    summary: str = ""
    authors: tuple[str, ...] = ()
    source_url: str | None = None
    reference_only: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialisable mapping in canonical key order; empty optionals omitted."""
        data: dict[str, Any] = {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "format": self.format,
            "language": self.language,
        }
        if self.tags:
            data["tags"] = list(self.tags)
        if self.summary:
            data["summary"] = self.summary
        if self.authors:
            data["authors"] = list(self.authors)
        if self.source_url:
            data["source_url"] = self.source_url
        if self.reference_only:
            data["reference_only"] = True
        data["license"] = self.license
        data["added"] = self.added
        cls: dict[str, Any] = {"method": self.classification.method}
        if self.classification.model:
            cls["model"] = self.classification.model
        cls["confidence"] = round(self.classification.confidence, 2)
        data["classification"] = cls
        return data


class _Dumper(yaml.SafeDumper):
    """Deterministic, alias-free dumper; scalar lists render in flow style."""

    @override
    def ignore_aliases(self, data: object) -> bool:
        return True


def _represent_list(dumper: yaml.SafeDumper, data: list[Any]) -> yaml.Node:
    flow = all(isinstance(item, (str, int, float)) for item in data)
    return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=flow)


_Dumper.add_representer(list, _represent_list)


def dump_front_matter(data: Mapping[str, Any]) -> str:
    """Render a mapping as a ``---`` delimited front matter block."""
    body = yaml.dump(
        dict(data),
        Dumper=_Dumper,
        sort_keys=False,
        allow_unicode=True,
        width=4096,
        default_flow_style=False,
    )
    return f"---\n{body}---\n"


def split_front_matter(text: str) -> tuple[dict[str, Any] | None, str]:
    """Separate a leading front matter block from the Markdown body.

    Returns ``(None, text)`` when the document has no front matter (including
    a leading ``---`` that is never closed, which Markdown reads as a rule).

    Raises:
        FrontMatterError: the block is too large, not YAML,
            uses aliases or does not decode to a mapping.
    """
    if not text.startswith("---\n"):
        return None, text
    lines = text.split("\n")
    end = next((i for i in range(1, len(lines)) if _DELIM_RE.match(lines[i])), None)
    if end is None:
        # A lone leading '---' is a Markdown thematic break, not front matter.
        return None, text
    raw = "\n".join(lines[1:end])
    if len(raw.encode("utf-8")) > MAX_FRONT_MATTER_BYTES:
        msg = f"front matter exceeds {MAX_FRONT_MATTER_BYTES:,} bytes"
        raise FrontMatterError(msg)
    try:
        data = safe_load(raw) if raw.strip() else {}
    except yaml.YAMLError as exc:
        msg = f"front matter is not valid YAML: {exc}"
        raise FrontMatterError(msg) from exc
    if not isinstance(data, dict):
        msg = "front matter must be a YAML mapping"
        raise FrontMatterError(msg)
    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return {str(k): v for k, v in data.items()}, body


def render_document(front_matter: FrontMatter, body: str) -> str:
    """Serialise a resource: front matter block, blank line, body."""
    return dump_front_matter(front_matter.to_dict()) + "\n" + body.lstrip("\n")


# ---------------------------------------------------------------------------
# Field validators. Each returns the normalised value or appends a problem.
# ---------------------------------------------------------------------------


def _single_line(
    value: object, key: str, max_len: int, problems: list[str], *, allow_empty: bool
) -> str:
    if not isinstance(value, str):
        problems.append(f"'{key}' must be a string")
        return ""
    text = value.strip()
    if "\n" in text or "\r" in text:
        problems.append(f"'{key}' must be a single line")
    if not text and not allow_empty:
        problems.append(f"'{key}' must not be empty")
    if len(text) > max_len:
        problems.append(f"'{key}' exceeds {max_len} characters")
    return text


def _enum(value: object, key: str, allowed: tuple[str, ...], problems: list[str]) -> str:
    if not isinstance(value, str) or value not in allowed:
        problems.append(f"'{key}' must be one of: {', '.join(allowed)} (got {value!r})")
        return ""
    return value


def _str_list(value: object, key: str, max_items: int, problems: list[str]) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        problems.append(f"'{key}' must be a list of strings")
        return []
    items = [v.strip() for v in value]
    if len(items) > max_items:
        problems.append(f"'{key}' allows at most {max_items} items")
    if len(set(items)) != len(items):
        problems.append(f"'{key}' contains duplicates")
    return items


def _tags(value: object, taxonomy: Taxonomy, problems: list[str]) -> tuple[str, ...]:
    tags = _str_list(value, "tags", MAX_TAGS, problems)
    unknown = sorted(set(tags) - set(taxonomy.tag_ids))
    if unknown:
        problems.append(
            f"'tags' contains values outside the controlled vocabulary: {', '.join(unknown)}"
        )
    return tuple(sorted(set(tags) & set(taxonomy.tag_ids)))


def _authors(value: object, problems: list[str]) -> tuple[str, ...]:
    authors = _str_list(value, "authors", MAX_AUTHORS, problems)
    if any(not a or len(a) > MAX_AUTHOR_LEN or "\n" in a for a in authors):
        problems.append(
            f"each author must be a non-empty single line of at most {MAX_AUTHOR_LEN} characters"
        )
    return tuple(authors)


def _source_url(value: object, problems: list[str]) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or len(value) > MAX_URL or not _URL_RE.match(value):
        problems.append("'source_url' must be an http(s) URL without whitespace")
        return None
    return value


def _license(value: object, problems: list[str]) -> str:
    if not isinstance(value, str) or not LICENSE_RE.match(value):
        problems.append("'license' must be an SPDX identifier, a LicenseRef-* or NOASSERTION")
        return "NOASSERTION"
    return value


def _added(value: object, problems: list[str]) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
    problems.append("'added' must be an ISO date (YYYY-MM-DD)")
    return date(1970, 1, 1)


def _classification(value: object, problems: list[str]) -> Classification:
    if not isinstance(value, dict):
        problems.append("'classification' must be a mapping")
        return Classification("manual", 0.0)
    unknown = sorted(set(value) - {"method", "model", "confidence"})
    if unknown:
        problems.append(f"'classification' has unknown keys: {', '.join(map(str, unknown))}")
    method = value.get("method")
    if method not in CLASSIFICATION_METHODS:
        problems.append(
            f"'classification.method' must be one of: {', '.join(CLASSIFICATION_METHODS)}"
        )
        method = "manual"
    confidence = value.get("confidence")
    if (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not 0 <= confidence <= 1
    ):
        problems.append("'classification.confidence' must be a number between 0 and 1")
        confidence = 0.0
    model = value.get("model")
    if model is not None and (not isinstance(model, str) or not model.strip()):
        problems.append("'classification.model' must be a non-empty string")
        model = None
    if method == "llm" and model is None:
        problems.append("'classification.model' is required when method is 'llm'")
    return Classification(cast("ClassificationMethod", method), float(confidence), model)


def parse_front_matter(raw: Mapping[str, Any], taxonomy: Taxonomy) -> FrontMatter:
    """Strictly validate a library document's front matter.

    Raises:
        FrontMatterError: listing *every* problem found, not just the first.
    """
    problems: list[str] = []
    missing = sorted(_REQUIRED_KEYS - set(raw))
    if missing:
        problems.append(f"missing required keys: {', '.join(missing)}")
    unknown = sorted(set(raw) - _LIBRARY_KEYS)
    if unknown:
        problems.append(f"unknown keys: {', '.join(unknown)}")

    ident = raw.get("id")
    if not isinstance(ident, str) or not ID_RE.match(ident):
        problems.append("'id' must match ckb-<12 lowercase hex digits>")
    fm = FrontMatter(
        id=ident if isinstance(ident, str) else "",
        title=_single_line(raw.get("title", ""), "title", MAX_TITLE, problems, allow_empty=False),
        category=_enum(raw.get("category"), "category", taxonomy.category_ids, problems),
        format=_enum(raw.get("format"), "format", taxonomy.format_ids, problems),
        language=_enum(raw.get("language"), "language", taxonomy.language_ids, problems),
        license=_license(raw.get("license"), problems),
        added=_added(raw.get("added"), problems),
        classification=_classification(raw.get("classification"), problems),
        tags=_tags(raw.get("tags", []), taxonomy, problems),
        summary=_single_line(
            raw.get("summary", ""), "summary", MAX_SUMMARY, problems, allow_empty=True
        ),
        authors=_authors(raw.get("authors", []), problems),
        source_url=_source_url(raw.get("source_url"), problems),
        reference_only=_reference_only(raw.get("reference_only", False), problems),
    )
    if problems:
        raise FrontMatterError("; ".join(problems))
    return fm


def _reference_only(value: object, problems: list[str]) -> bool:
    if not isinstance(value, bool):
        problems.append("'reference_only' must be a boolean")
        return False
    return value


def validate_contributor_hints(
    raw: Mapping[str, Any], taxonomy: Taxonomy
) -> tuple[dict[str, Any], list[str]]:
    """Validate the optional front matter a contributor put on a raw submission.

    Returns the subset of valid hints and a list of problems. Ingestion uses
    the valid hints and logs the problems; the pull-request check reports
    the problems as errors so contributors can fix them before merge.
    """
    problems: list[str] = []
    unknown = sorted(set(raw) - CONTRIBUTOR_KEYS)
    if unknown:
        problems.append(f"unknown front matter keys: {', '.join(unknown)}")
    hints: dict[str, Any] = {}
    validators: dict[str, Any] = {
        "title": lambda v, p: _single_line(v, "title", MAX_TITLE, p, allow_empty=False),
        "category": lambda v, p: _enum(v, "category", taxonomy.category_ids, p),
        "format": lambda v, p: _enum(v, "format", taxonomy.format_ids, p),
        "language": lambda v, p: _enum(v, "language", taxonomy.language_ids, p),
        "tags": lambda v, p: _tags(v, taxonomy, p),
        "summary": lambda v, p: _single_line(v, "summary", MAX_SUMMARY, p, allow_empty=True),
        "authors": _authors,
        "source_url": _source_url,
        "license": _license,
    }
    for key in sorted(CONTRIBUTOR_KEYS & set(raw)):
        local: list[str] = []
        value = validators[key](raw[key], local)
        if local:
            problems.extend(local)
        else:
            hints[key] = value
    return hints, problems
