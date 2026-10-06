"""Typed, validated view of ``schema/taxonomy.yaml``."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

from cyberkb.errors import KBError, TaxonomyError
from cyberkb.fsutil import read_text
from cyberkb.textutil import phrase_tokens
from cyberkb.yamlsafe import safe_load

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = [
    "KEYWORD_WEIGHTS",
    "TAXONOMY_RELPATH",
    "Category",
    "Facet",
    "Tag",
    "Taxonomy",
    "load_taxonomy",
]

TAXONOMY_RELPATH = Path("schema") / "taxonomy.yaml"
KEYWORD_WEIGHTS: Mapping[str, int] = {"strong": 5, "medium": 2, "weak": 1}
_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_MAX_TAXONOMY_BYTES = 1_000_000


@dataclass(frozen=True, slots=True)
class Category:
    """A primary category; it decides the folder a resource lives in."""

    id: str
    name: str
    description: str
    cybok: tuple[str, ...]
    nice: tuple[str, ...]
    keywords: tuple[tuple[tuple[str, ...], int], ...]
    staging: bool = False


@dataclass(frozen=True, slots=True)
class Facet:
    """A value of a closed facet (format or language)."""

    id: str
    name: str
    description: str = ""


@dataclass(frozen=True, slots=True)
class Tag:
    """A controlled-vocabulary tag and the phrases that evidence it."""

    id: str
    patterns: tuple[tuple[str, ...], ...]


@dataclass(frozen=True, slots=True)
class Taxonomy:
    """The complete, validated taxonomy."""

    version: int
    categories: tuple[Category, ...]
    formats: tuple[Facet, ...]
    languages: tuple[Facet, ...]
    tags: tuple[Tag, ...]
    cybok: Mapping[str, str]
    nice: Mapping[str, str]

    @property
    def category_ids(self) -> tuple[str, ...]:
        """Category identifiers in display order."""
        return tuple(c.id for c in self.categories)

    @property
    def format_ids(self) -> tuple[str, ...]:
        """Format identifiers in display order."""
        return tuple(f.id for f in self.formats)

    @property
    def language_ids(self) -> tuple[str, ...]:
        """Language identifiers in display order."""
        return tuple(lang.id for lang in self.languages)

    @property
    def tag_ids(self) -> tuple[str, ...]:
        """Tag identifiers in alphabetical order."""
        return tuple(t.id for t in self.tags)

    @property
    def staging(self) -> Category:
        """The staging category that receives low-confidence classifications."""
        return next(c for c in self.categories if c.staging)

    def category(self, category_id: str) -> Category:
        """Look up a category by id.

        Raises:
            TaxonomyError: if the id is unknown.
        """
        for cat in self.categories:
            if cat.id == category_id:
                return cat
        msg = f"unknown category {category_id!r}"
        raise TaxonomyError(msg)


def _require(condition: object, message: str) -> None:
    if not condition:
        raise TaxonomyError(message)


def _str_field(node: Mapping[str, Any], key: str, where: str) -> str:
    value = node.get(key)
    _require(
        isinstance(value, str) and value.strip(), f"{where}: '{key}' must be a non-empty string"
    )
    return str(value).strip()


def _code_list(
    node: Mapping[str, Any], key: str, where: str, known: Mapping[str, str]
) -> tuple[str, ...]:
    value = node.get(key, [])
    _require(isinstance(value, list), f"{where}: '{key}' must be a list")
    codes = tuple(str(v) for v in value)
    unknown = [c for c in codes if c not in known]
    _require(not unknown, f"{where}: unknown {key} code(s) {unknown}")
    return codes


def _unique_ids(items: list[Any], where: str) -> None:
    ids: list[str] = []
    for item in items:
        ident = getattr(item, "id", None)
        _require(
            isinstance(ident, str) and _ID_RE.fullmatch(ident), f"{where}: invalid id {ident!r}"
        )
        ids.append(str(ident))
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    _require(not dupes, f"{where}: duplicate id(s) {dupes}")


def _parse_keywords(node: Mapping[str, Any], where: str) -> tuple[tuple[tuple[str, ...], int], ...]:
    raw = node.get("keywords", {})
    if not isinstance(raw, dict):
        msg = f"{where}: 'keywords' must be a mapping"
        raise TaxonomyError(msg)
    out: list[tuple[tuple[str, ...], int]] = []
    for level, phrases in raw.items():
        _require(level in KEYWORD_WEIGHTS, f"{where}: unknown keyword level {level!r}")
        _require(isinstance(phrases, list), f"{where}: keywords.{level} must be a list")
        for phrase in phrases:
            tokens = phrase_tokens(str(phrase))
            _require(tokens, f"{where}: empty keyword phrase {phrase!r}")
            out.append((tokens, KEYWORD_WEIGHTS[level]))
    return tuple(out)


def _parse_mapping(data: Mapping[str, Any], key: str) -> dict[str, str]:
    raw = data.get(key)
    if not isinstance(raw, dict) or not raw:
        msg = f"taxonomy: '{key}' must be a non-empty mapping"
        raise TaxonomyError(msg)
    return {str(k): str(v) for k, v in raw.items()}


def _parse_list(data: Mapping[str, Any], key: str) -> list[dict[str, Any]]:
    raw = data.get(key)
    if not isinstance(raw, list) or not raw:
        msg = f"taxonomy: '{key}' must be a non-empty list"
        raise TaxonomyError(msg)
    if not all(isinstance(i, dict) for i in raw):
        msg = f"taxonomy: every '{key}' entry must be a mapping"
        raise TaxonomyError(msg)
    return list(raw)


def parse_taxonomy(data: object) -> Taxonomy:
    """Validate a decoded taxonomy document and build the typed model.

    Raises:
        TaxonomyError: on any structural problem, with a precise message.
    """
    _require(isinstance(data, dict), "taxonomy: top level must be a mapping")
    assert isinstance(data, dict)  # noqa: S101 -- narrowing for the type checker
    _require(data.get("version") == 2, "taxonomy: only version 2 is supported")  # noqa: PLR2004
    cybok = _parse_mapping(data, "cybok_knowledge_areas")
    nice = _parse_mapping(data, "nice_categories")

    categories = []
    for node in _parse_list(data, "categories"):
        where = f"category {node.get('id')!r}"
        categories.append(
            Category(
                id=_str_field(node, "id", where),
                name=_str_field(node, "name", where),
                description=_str_field(node, "description", where),
                cybok=_code_list(node, "cybok", where, cybok),
                nice=_code_list(node, "nice", where, nice),
                keywords=_parse_keywords(node, where),
                staging=bool(node.get("staging", False)),
            ),
        )
    _unique_ids(categories, "categories")
    staging = [c.id for c in categories if c.staging]
    _require(len(staging) == 1, f"taxonomy: exactly one staging category required, found {staging}")
    _require(
        all(c.keywords for c in categories if not c.staging),
        "taxonomy: every non-staging category needs keywords",
    )

    formats = [
        Facet(
            _str_field(n, "id", "format"),
            _str_field(n, "name", "format"),
            str(n.get("description", "")),
        )
        for n in _parse_list(data, "formats")
    ]
    _unique_ids(formats, "formats")
    languages = [
        Facet(_str_field(n, "id", "language"), _str_field(n, "name", "language"))
        for n in _parse_list(data, "languages")
    ]
    _unique_ids(languages, "languages")
    _require("und" in {lang.id for lang in languages}, "taxonomy: language 'und' is required")

    tags = []
    for node in _parse_list(data, "tags"):
        tag_id = _str_field(node, "id", "tag")
        patterns = node.get("patterns")
        _require(
            isinstance(patterns, list) and patterns,
            f"tag {tag_id!r}: 'patterns' must be a non-empty list",
        )
        assert isinstance(patterns, list)  # noqa: S101 -- narrowing for the type checker
        parsed = tuple(phrase_tokens(str(p)) for p in patterns)
        _require(all(parsed), f"tag {tag_id!r}: empty pattern")
        tags.append(Tag(tag_id, parsed))
    _unique_ids(tags, "tags")
    tags.sort(key=lambda t: t.id)

    return Taxonomy(
        version=2,
        categories=tuple(categories),
        formats=tuple(formats),
        languages=tuple(languages),
        tags=tuple(tags),
        cybok=cybok,
        nice=nice,
    )


def load_taxonomy(repo_root: Path) -> Taxonomy:
    """Load and validate ``<repo_root>/schema/taxonomy.yaml``.

    Raises:
        TaxonomyError: if the file is missing, unreadable, not YAML or invalid.
    """
    path = repo_root / TAXONOMY_RELPATH
    try:
        text = read_text(path, root=repo_root, max_bytes=_MAX_TAXONOMY_BYTES)
        data = safe_load(text)
    except (KBError, yaml.YAMLError) as exc:
        msg = f"cannot load taxonomy from {TAXONOMY_RELPATH.as_posix()}: {exc}"
        raise TaxonomyError(msg) from exc
    return parse_taxonomy(data)
