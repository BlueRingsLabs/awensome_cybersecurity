"""The generated catalog must validate against the published JSON Schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import jsonschema

from cyberkb.catalog import build_catalog
from cyberkb.library import Resource
from tests.conftest import FIXED_NOW, make_front_matter

if TYPE_CHECKING:
    from cyberkb.taxonomy import Taxonomy

SCHEMA = json.loads(
    (Path(__file__).resolve().parents[1] / "schema" / "catalog.schema.json").read_text(
        encoding="utf-8",
    ),
)


def _resource(**fm: object) -> Resource:
    """Build a Resource wrapping front matter with the given overrides."""
    front_matter = make_front_matter(**fm)
    return Resource(
        front_matter=front_matter,
        path=f"library/{front_matter.category}/{front_matter.id}.md",
        size_bytes=100,
        word_count=50,
        body_sha256="b" * 64,
    )


def test_schema_itself_is_valid() -> None:
    """The catalog JSON Schema is itself a valid Draft 2020-12 schema."""
    jsonschema.Draft202012Validator.check_schema(SCHEMA)


def test_empty_catalog_validates(taxonomy: Taxonomy) -> None:
    """An empty catalog conforms to the schema."""
    catalog = build_catalog([], taxonomy, generated_at=FIXED_NOW)
    jsonschema.validate(catalog, SCHEMA)


def test_populated_catalog_validates(taxonomy: Taxonomy) -> None:
    """A catalog with varied entries (source_url, empty tags) conforms."""
    resources = [
        _resource(id="ckb-000000000001", title="One", source_url="https://example.test/a"),
        _resource(id="ckb-000000000002", title="Two", category="malware-analysis", tags=()),
    ]
    catalog = build_catalog(resources, taxonomy, generated_at=FIXED_NOW)
    jsonschema.validate(catalog, SCHEMA)


def test_reference_only_entry_validates(taxonomy: Taxonomy) -> None:
    """A reference-only entry serialises the flag and still conforms."""
    resource = _resource(
        id="ckb-000000000003",
        title="Ref",
        reference_only=True,
        license="LicenseRef-All-Rights-Reserved",
        source_url="https://example.test/ref",
    )
    catalog = build_catalog([resource], taxonomy, generated_at=FIXED_NOW)
    jsonschema.validate(catalog, SCHEMA)
    assert catalog["entries"][0]["reference_only"] is True


def test_classified_by_entry_validates(taxonomy: Taxonomy) -> None:
    """A provenance-stamped entry serialises classified_by and conforms."""
    stamp = "openrouter:meta-llama/llama-3.3-70b-instruct:free@2026-10-05T14:23:11Z"
    catalog = build_catalog([_resource(classified_by=stamp)], taxonomy, generated_at=FIXED_NOW)
    assert catalog["entries"][0]["classified_by"] == stamp
    jsonschema.validate(catalog, SCHEMA)


def test_empty_authors_emit_unknown(taxonomy: Taxonomy) -> None:
    """An entry with no declared authors serialises as ['unknown']."""
    catalog = build_catalog([_resource(authors=())], taxonomy, generated_at=FIXED_NOW)
    assert catalog["entries"][0]["authors"] == ["unknown"]
    jsonschema.validate(catalog, SCHEMA)


def test_real_taxonomy_catalog_block_validates(taxonomy: Taxonomy) -> None:
    """A catalog built from the shipped taxonomy conforms to the schema."""
    catalog = build_catalog([_resource()], taxonomy, generated_at=FIXED_NOW)
    jsonschema.validate(catalog, SCHEMA)
