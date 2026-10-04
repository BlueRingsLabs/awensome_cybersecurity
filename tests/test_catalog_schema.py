"""The generated catalog must validate against the published JSON Schema."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from cyberkb.catalog import build_catalog
from cyberkb.library import Resource
from tests.conftest import FIXED_NOW, make_front_matter

SCHEMA = json.loads(
    (Path(__file__).resolve().parents[1] / "schema" / "catalog.schema.json").read_text()
)


def _resource(**fm: object) -> Resource:
    front_matter = make_front_matter(**fm)
    return Resource(
        front_matter=front_matter,
        path=f"library/{front_matter.category}/{front_matter.id}.md",
        size_bytes=100,
        word_count=50,
        body_sha256="b" * 64,
    )


def test_schema_itself_is_valid() -> None:
    jsonschema.Draft202012Validator.check_schema(SCHEMA)


def test_empty_catalog_validates(taxonomy) -> None:
    catalog = build_catalog([], taxonomy, generated_at=FIXED_NOW)
    jsonschema.validate(catalog, SCHEMA)


def test_populated_catalog_validates(taxonomy) -> None:
    resources = [
        _resource(id="ckb-000000000001", title="One", source_url="https://example.test/a"),
        _resource(id="ckb-000000000002", title="Two", category="malware-analysis", tags=()),
    ]
    catalog = build_catalog(resources, taxonomy, generated_at=FIXED_NOW)
    jsonschema.validate(catalog, SCHEMA)


def test_real_taxonomy_catalog_block_validates(taxonomy) -> None:
    # The taxonomy block derived from the shipped taxonomy must satisfy the schema.
    catalog = build_catalog([_resource()], taxonomy, generated_at=FIXED_NOW)
    jsonschema.validate(catalog, SCHEMA)
