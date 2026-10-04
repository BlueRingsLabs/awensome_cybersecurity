"""Tests for taxonomy parsing/validation and the hardened YAML loader."""

from __future__ import annotations

import pytest
import yaml

from cyberkb.errors import TaxonomyError
from cyberkb.taxonomy import Taxonomy, load_taxonomy, parse_taxonomy
from cyberkb.yamlsafe import YAMLAliasError, safe_load


def _minimal() -> dict:
    return {
        "version": 2,
        "cybok_knowledge_areas": {"NS": "Network Security"},
        "nice_categories": {"PD": "Protection and Defense"},
        "categories": [
            {
                "id": "offensive-security",
                "name": "Offensive",
                "description": "desc",
                "cybok": ["NS"],
                "nice": ["PD"],
                "keywords": {"strong": ["red team"], "medium": ["exploit"]},
            },
            {
                "id": "uncategorized",
                "name": "Staging",
                "description": "d",
                "staging": True,
                "keywords": {},
            },
        ],
        "formats": [{"id": "guide", "name": "Guide", "description": "a guide"}],
        "languages": [{"id": "en", "name": "English"}, {"id": "und", "name": "Undetermined"}],
        "tags": [{"id": "nmap", "patterns": ["nmap", "port scanning"]}],
    }


def test_parse_minimal_ok() -> None:
    tax = parse_taxonomy(_minimal())
    assert isinstance(tax, Taxonomy)
    assert tax.category_ids == ("offensive-security", "uncategorized")
    assert tax.staging.id == "uncategorized"
    assert tax.format_ids == ("guide",)
    assert tax.tag_ids == ("nmap",)


def test_real_taxonomy_loads(taxonomy: Taxonomy) -> None:
    assert taxonomy.version == 2
    assert "offensive-security" in taxonomy.category_ids
    assert taxonomy.staging.id == "uncategorized"
    # Every category's CyBOK/NICE codes resolve against the declared vocabularies.
    for cat in taxonomy.categories:
        for code in cat.cybok:
            assert code in taxonomy.cybok
        for code in cat.nice:
            assert code in taxonomy.nice


def test_category_lookup_and_error(taxonomy: Taxonomy) -> None:
    assert taxonomy.category("offensive-security").name == "Offensive Security"
    with pytest.raises(TaxonomyError):
        taxonomy.category("does-not-exist")


def test_language_ids_contains_und(taxonomy: Taxonomy) -> None:
    assert "und" in taxonomy.language_ids


@pytest.mark.parametrize(
    "mutate",
    [
        lambda d: d.update(version=1),
        lambda d: d.update(categories="nope"),
        lambda d: d.update(cybok_knowledge_areas={}),
        lambda d: d["categories"][0].update(cybok=["ZZ"]),
        lambda d: d["categories"][0].update(id="Bad Id"),
        lambda d: d["categories"][0].update(keywords={"weird": ["x"]}),
        lambda d: d["categories"][0].update(keywords={"strong": "notalist"}),
        lambda d: d["categories"][0].update(keywords={"strong": [""]}),
        lambda d: d["categories"].append(
            {
                "id": "offensive-security",
                "name": "Dup",
                "description": "d",
                "keywords": {"strong": ["x"]},
            },
        ),
        lambda d: d["tags"][0].update(patterns=[]),
        lambda d: d.update(formats=[]),
        lambda d: d["languages"].pop(1),
        lambda d: d["categories"][0].update(name=""),
        lambda d: d["categories"][0].update(cybok="notalist"),
    ],
)
def test_invalid_taxonomy_rejected(mutate) -> None:
    data = _minimal()
    mutate(data)
    with pytest.raises(TaxonomyError):
        parse_taxonomy(data)


def test_two_staging_categories_rejected() -> None:
    data = _minimal()
    data["categories"][0]["staging"] = True
    with pytest.raises(TaxonomyError, match="staging"):
        parse_taxonomy(data)


def test_non_staging_without_keywords_rejected() -> None:
    data = _minimal()
    data["categories"][0]["keywords"] = {}
    with pytest.raises(TaxonomyError, match="keywords"):
        parse_taxonomy(data)


def test_top_level_not_mapping() -> None:
    with pytest.raises(TaxonomyError):
        parse_taxonomy(["not", "a", "mapping"])


def test_load_taxonomy_missing(tmp_path, monkeypatch) -> None:
    from cyberkb.paths import RepoPaths

    repo = RepoPaths.at(tmp_path)
    with pytest.raises(TaxonomyError):
        load_taxonomy(repo.root)


def test_load_taxonomy_bad_yaml(repo) -> None:
    repo.taxonomy.write_text("::: not yaml :::\n", encoding="utf-8")
    with pytest.raises(TaxonomyError):
        load_taxonomy(repo.root)


# --- yamlsafe -------------------------------------------------------------


def test_safe_load_basic() -> None:
    assert safe_load("a: 1\nb: [x, y]\n") == {"a": 1, "b": ["x", "y"]}


def test_safe_load_rejects_alias() -> None:
    doc = "a: &anchor value\nb: *anchor\n"
    with pytest.raises(YAMLAliasError):
        safe_load(doc)


def test_safe_load_rejects_anchor_even_without_alias() -> None:
    with pytest.raises(YAMLAliasError):
        safe_load("a: &anchor 1\n")


def test_safe_load_is_yaml_error_subclass() -> None:
    assert issubclass(YAMLAliasError, yaml.YAMLError)


def test_safe_load_empty() -> None:
    assert safe_load("") is None


def test_keywords_not_a_mapping() -> None:
    data = _minimal()
    data["categories"][0]["keywords"] = "not a mapping"
    with pytest.raises(TaxonomyError, match="keywords"):
        parse_taxonomy(data)


def test_list_entry_not_mapping() -> None:
    data = _minimal()
    data["formats"] = ["not-a-mapping"]
    with pytest.raises(TaxonomyError, match="entry must be a mapping"):
        parse_taxonomy(data)
