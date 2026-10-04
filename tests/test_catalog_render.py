"""Tests for catalog construction, serialisation and rendering."""

from __future__ import annotations

import json

import yaml

from cyberkb.catalog import (
    CATALOG_SCHEMA_VERSION,
    build_catalog,
    catalog_json,
    catalog_yaml,
    strip_volatile_lines,
)
from cyberkb.frontmatter import Classification
from cyberkb.library import Resource
from cyberkb.render import (
    README_END,
    README_START,
    render_category_page,
    render_index_block,
    splice_readme,
)
from tests.conftest import FIXED_NOW, make_front_matter


def _resource(**fm: object) -> Resource:
    front_matter = make_front_matter(**fm)
    return Resource(
        front_matter=front_matter,
        path=f"library/{front_matter.category}/{front_matter.id}.md",
        size_bytes=1234,
        word_count=321,
        body_sha256="a" * 64,
    )


def test_build_catalog_shape(taxonomy) -> None:
    resources = [_resource(id="ckb-000000000001", title="Alpha")]
    catalog = build_catalog(resources, taxonomy, generated_at=FIXED_NOW)
    assert catalog["schema_version"] == CATALOG_SCHEMA_VERSION
    assert catalog["generated_at"] == "2026-01-02T03:04:05Z"
    assert catalog["counts"]["total"] == 1
    assert catalog["counts"]["by_category"]["offensive-security"] == 1
    entry = catalog["entries"][0]
    assert entry["id"] == "ckb-000000000001"
    assert entry["redistribution"] == "permitted"


def test_build_catalog_includes_optional_fields(taxonomy) -> None:
    resources = [
        _resource(
            source_url="https://example.test/x",
            classification=Classification("llm", 0.8, "gemini-x"),
        ),
    ]
    entry = build_catalog(resources, taxonomy, generated_at=FIXED_NOW)["entries"][0]
    assert entry["source_url"] == "https://example.test/x"
    assert entry["classification"]["model"] == "gemini-x"


def test_catalog_json_is_valid_and_stable(taxonomy) -> None:
    catalog = build_catalog([_resource()], taxonomy, generated_at=FIXED_NOW)
    text = catalog_json(catalog)
    assert text.endswith("\n")
    assert json.loads(text)["schema_version"] == CATALOG_SCHEMA_VERSION
    assert catalog_json(catalog) == text


def test_catalog_yaml_round_trips(taxonomy) -> None:
    catalog = build_catalog([_resource()], taxonomy, generated_at=FIXED_NOW)
    text = catalog_yaml(catalog)
    assert text.startswith("# awesome_cybersecurity")
    loaded = yaml.safe_load(text)
    assert loaded["counts"]["total"] == 1


def test_build_catalog_default_timestamp(taxonomy) -> None:
    catalog = build_catalog([], taxonomy)
    assert catalog["generated_at"].endswith("Z")
    assert catalog["counts"]["total"] == 0


def test_strip_volatile_lines() -> None:
    text = 'a\n"generated_at": "x"\nb\n'
    assert "generated_at" not in strip_volatile_lines(text)


# --- render ---------------------------------------------------------------


def test_render_index_block(taxonomy) -> None:
    resources = [_resource(title="Alpha Guide")]
    catalog = build_catalog(resources, taxonomy, generated_at=FIXED_NOW)
    block = render_index_block(catalog, resources, taxonomy)
    assert "Alpha Guide" in block
    assert "Offensive Security" in block
    assert "| Category | Count |" in block


def test_render_index_block_neutralises_pipe(taxonomy) -> None:
    # A raw pipe in a title would break the Markdown table; plain_text drops it.
    resources = [_resource(title="A | B danger")]
    catalog = build_catalog(resources, taxonomy, generated_at=FIXED_NOW)
    block = render_index_block(catalog, resources, taxonomy)
    row = next(line for line in block.splitlines() if "danger" in line)
    assert "A B danger" in row
    # The cell content carries no bare pipe, so the row still has 4 separators.
    assert row.count("|") == 4


def test_splice_readme_replaces_block() -> None:
    readme = f"# Title\n\n{README_START}\nOLD\n{README_END}\n\nFooter\n"
    out = splice_readme(readme, "NEW")
    assert "NEW" in out
    assert "OLD" not in out
    assert "Footer" in out


def test_splice_readme_appends_when_missing() -> None:
    out = splice_readme("# Title\n", "BLOCK")
    assert README_START in out
    assert "BLOCK" in out


def test_splice_readme_empty_input() -> None:
    out = splice_readme("", "BLOCK")
    assert out.startswith(README_START)


def test_splice_readme_corrupt_markers_unchanged() -> None:
    readme = f"# Title\n{README_END}\nonly end marker\n"
    assert splice_readme(readme, "NEW") == readme


def test_render_category_page(taxonomy) -> None:
    resources = [_resource(title="A Guide", tags=("nmap",), summary="Scanning.")]
    page = render_category_page("offensive-security", resources, taxonomy)
    assert page.startswith("# Offensive Security")
    assert "A Guide" in page
    assert "CyBOK knowledge areas" in page
    assert "nmap" in page


def test_render_category_page_empty_facets(taxonomy) -> None:
    # ai-security has no CyBOK codes, exercising the "--" branch.
    resources = [_resource(category="ai-security", title="LLM Risks", tags=(), summary="")]
    page = render_category_page("ai-security", resources, taxonomy)
    assert "--" in page
