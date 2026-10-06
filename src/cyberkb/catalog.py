"""Deterministic catalog construction and serialisation.

The catalog is a pure function of the library tree and the taxonomy: given
the same inputs it always produces byte-identical ``index.json`` and
``index.yaml``, so CI diffs only ever reflect real content changes. It
carries a ``schema_version`` and a self-describing ``taxonomy`` block so a
consumer can interpret it without reading this repository's source.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, override

import yaml

from cyberkb.licensing import redistribution_class

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from cyberkb.library import Resource
    from cyberkb.taxonomy import Taxonomy

__all__ = [
    "CATALOG_SCHEMA_VERSION",
    "build_catalog",
    "catalog_json",
    "catalog_yaml",
    "strip_volatile_lines",
]

#: Substrings marking the single wall-clock line in each generated artefact.
_VOLATILE_MARKERS = ('"generated_at"', "generated_at:", "Catalog regenerated")


def strip_volatile_lines(text: str) -> str:
    """Drop the timestamp line so a timestamp-only change is not treated as a change."""
    return "\n".join(
        line for line in text.split("\n") if not any(marker in line for marker in _VOLATILE_MARKERS)
    )


CATALOG_SCHEMA_VERSION = "2.0.0"
_REPOSITORY = {
    "name": "awesome_cybersecurity",
    "organization": "BlueRingsLabs",
    "url": "https://github.com/BlueRingsLabs/awesome_cybersecurity",
    "license": "MIT",
    "description": (
        "Open, curated and automatically indexed cybersecurity knowledge base: "
        "literature, papers and web resources organised by a CyBOK- and "
        "NICE-aligned taxonomy and published as machine-readable catalogs."
    ),
}


def _entry(resource: Resource) -> dict[str, Any]:
    front_matter = resource.front_matter
    entry: dict[str, Any] = {
        "id": front_matter.id,
        "title": front_matter.title,
        "category": front_matter.category,
        "format": front_matter.format,
        "language": front_matter.language,
        "path": resource.path,
        "tags": list(front_matter.tags),
        "summary": front_matter.summary,
        # The catalog always carries an explicit author list: "unknown" makes
        # "searched, none declared" unambiguous versus an empty field.
        "authors": list(front_matter.authors) or ["unknown"],
        "license": front_matter.license,
        "redistribution": redistribution_class(front_matter.license).value,
        "added": front_matter.added.isoformat(),
        "word_count": resource.word_count,
        "size_bytes": resource.size_bytes,
        "sha256": resource.body_sha256,
        "classification": {
            "method": front_matter.classification.method,
            "confidence": round(front_matter.classification.confidence, 2),
        },
    }
    if front_matter.source_url:
        entry["source_url"] = front_matter.source_url
    if front_matter.reference_only:
        entry["reference_only"] = True
    if front_matter.classification.model:
        entry["classification"]["model"] = front_matter.classification.model
    if front_matter.classified_by:
        entry["classified_by"] = front_matter.classified_by
    return entry


def _taxonomy_block(taxonomy: Taxonomy) -> dict[str, Any]:
    return {
        "version": taxonomy.version,
        "categories": [
            {
                "id": cat.id,
                "name": cat.name,
                "description": cat.description,
                "cybok": list(cat.cybok),
                "nice": list(cat.nice),
                "staging": cat.staging,
            }
            for cat in taxonomy.categories
        ],
        "formats": [{"id": f.id, "name": f.name} for f in taxonomy.formats],
        "languages": [{"id": lang.id, "name": lang.name} for lang in taxonomy.languages],
        "tags": list(taxonomy.tag_ids),
        "cybok_knowledge_areas": dict(taxonomy.cybok),
        "nice_categories": dict(taxonomy.nice),
    }


def _counts(entries: Sequence[Mapping[str, Any]], taxonomy: Taxonomy) -> dict[str, Any]:
    def tally(key: str, keys: Sequence[str]) -> dict[str, int]:
        counts = dict.fromkeys(keys, 0)
        for entry in entries:
            counts[str(entry[key])] += 1
        return counts

    redistribution: dict[str, int] = {}
    for entry in entries:
        redistribution[str(entry["redistribution"])] = (
            redistribution.get(str(entry["redistribution"]), 0) + 1
        )
    return {
        "total": len(entries),
        "by_category": tally("category", taxonomy.category_ids),
        "by_format": tally("format", taxonomy.format_ids),
        "by_language": tally("language", taxonomy.language_ids),
        "by_redistribution": dict(sorted(redistribution.items())),
    }


def build_catalog(
    resources: Sequence[Resource],
    taxonomy: Taxonomy,
    *,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build the catalog mapping from loaded resources.

    ``generated_at`` is injected for reproducible builds; when omitted the
    current UTC time is used. Entries are ordered by category, then title,
    then id, matching the library loader.
    """
    moment = (generated_at or datetime.now(UTC)).astimezone(UTC)
    entries = [_entry(r) for r in resources]
    return {
        "schema_version": CATALOG_SCHEMA_VERSION,
        "generated_at": moment.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "cyberkb",
        "repository": dict(_REPOSITORY),
        "taxonomy": _taxonomy_block(taxonomy),
        "counts": _counts(entries, taxonomy),
        "entries": entries,
    }


def catalog_json(catalog: Mapping[str, Any]) -> str:
    """Serialise the catalog as pretty, stable JSON with a trailing newline."""
    return json.dumps(catalog, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


class _CatalogDumper(yaml.SafeDumper):
    """YAML dumper that never emits anchors/aliases, for stable diffs."""

    @override
    def ignore_aliases(self, data: object) -> bool:
        return True


def _represent_str(dumper: yaml.SafeDumper, data: str) -> yaml.ScalarNode:
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_CatalogDumper.add_representer(str, _represent_str)


def catalog_yaml(catalog: Mapping[str, Any]) -> str:
    """Serialise the catalog as YAML with a provenance header."""
    header = (
        "# awesome_cybersecurity machine-readable catalog.\n"
        "# Generated by cyberkb -- do not edit by hand; run `cyberkb build`.\n"
    )
    body = yaml.dump(
        dict(catalog),
        Dumper=_CatalogDumper,
        sort_keys=False,
        allow_unicode=True,
        width=100,
        default_flow_style=False,
    )
    return header + body
