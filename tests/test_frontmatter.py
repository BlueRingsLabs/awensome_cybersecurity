"""Tests for front matter parsing, validation and serialisation."""

from __future__ import annotations

from datetime import date

import pytest

from cyberkb.errors import FrontMatterError
from cyberkb.frontmatter import (
    Classification,
    dump_front_matter,
    parse_front_matter,
    render_document,
    split_front_matter,
    validate_contributor_hints,
)
from tests.conftest import make_front_matter


def _valid_raw() -> dict:
    return {
        "id": "ckb-0123456789ab",
        "title": "A Guide",
        "category": "offensive-security",
        "format": "guide",
        "language": "en",
        "license": "CC-BY-4.0",
        "added": date(2026, 1, 1),
        "classification": {"method": "manual", "confidence": 1.0},
        "tags": ["nmap"],
        "summary": "A short summary.",
        "authors": ["Alice"],
        "source_url": "https://example.test/a",
    }


def test_parse_valid(taxonomy) -> None:
    fm = parse_front_matter(_valid_raw(), taxonomy)
    assert fm.id == "ckb-0123456789ab"
    assert fm.category == "offensive-security"
    assert fm.tags == ("nmap",)
    assert fm.classification.method == "manual"


def test_roundtrip_render_and_split(taxonomy) -> None:
    fm = parse_front_matter(_valid_raw(), taxonomy)
    doc = render_document(fm, "# Body\n\ntext\n")
    raw, body = split_front_matter(doc)
    assert raw is not None
    reparsed = parse_front_matter(raw, taxonomy)
    assert reparsed == fm
    assert body.startswith("# Body")


def test_to_dict_omits_empty_optionals() -> None:
    fm = make_front_matter(tags=(), summary="", authors=(), source_url=None)
    data = fm.to_dict()
    assert "tags" not in data
    assert "summary" not in data
    assert "authors" not in data
    assert "source_url" not in data


def test_to_dict_includes_llm_model() -> None:
    fm = make_front_matter(classification=Classification("llm", 0.9, "gemini-x"))
    assert fm.to_dict()["classification"]["model"] == "gemini-x"


@pytest.mark.parametrize(
    "mutate",
    [
        lambda d: d.pop("id"),
        lambda d: d.update(id="bad-id"),
        lambda d: d.update(title=""),
        lambda d: d.update(title="x\ny"),
        lambda d: d.update(category="nonexistent"),
        lambda d: d.update(format="nonexistent"),
        lambda d: d.update(language="fr"),
        lambda d: d.update(license="not a spdx id!!"),
        lambda d: d.update(added="not-a-date"),
        lambda d: d.update(tags=["nmap", "nmap"]),
        lambda d: d.update(tags=["not-a-real-tag"]),
        lambda d: d.update(tags="notalist"),
        lambda d: d.update(authors=["x" * 200]),
        lambda d: d.update(source_url="ftp://x"),
        lambda d: d.update(classification={"method": "manual"}),
        lambda d: d.update(classification={"method": "llm", "confidence": 0.9}),
        lambda d: d.update(classification={"method": "bad", "confidence": 0.5}),
        lambda d: d.update(classification={"method": "manual", "confidence": 2}),
        lambda d: d.update(classification="notadict"),
        lambda d: d.update(unknown_key="x"),
    ],
)
def test_invalid_front_matter(taxonomy, mutate) -> None:
    raw = _valid_raw()
    mutate(raw)
    with pytest.raises(FrontMatterError):
        parse_front_matter(raw, taxonomy)


def test_multiple_problems_reported(taxonomy) -> None:
    raw = _valid_raw()
    raw.update(title="", category="bad")
    with pytest.raises(FrontMatterError) as exc:
        parse_front_matter(raw, taxonomy)
    assert ";" in str(exc.value)


def test_classification_unknown_key(taxonomy) -> None:
    raw = _valid_raw()
    raw["classification"] = {"method": "manual", "confidence": 1.0, "bogus": 1}
    with pytest.raises(FrontMatterError, match="unknown keys"):
        parse_front_matter(raw, taxonomy)


def test_classification_bool_confidence_rejected(taxonomy) -> None:
    raw = _valid_raw()
    raw["classification"] = {"method": "manual", "confidence": True}
    with pytest.raises(FrontMatterError):
        parse_front_matter(raw, taxonomy)


def test_classification_bad_model_type(taxonomy) -> None:
    raw = _valid_raw()
    raw["classification"] = {"method": "llm", "confidence": 0.9, "model": ""}
    with pytest.raises(FrontMatterError):
        parse_front_matter(raw, taxonomy)


# --- split_front_matter edge cases ---------------------------------------


def test_split_no_front_matter() -> None:
    raw, body = split_front_matter("# Just a doc\n")
    assert raw is None
    assert body == "# Just a doc\n"


def test_split_unterminated_is_thematic_break() -> None:
    raw, _body = split_front_matter("---\nkey: value\nno closing delimiter\n")
    assert raw is None


def test_split_lone_rule() -> None:
    raw, _ = split_front_matter("---\n")
    assert raw is None


def test_split_empty_block() -> None:
    raw, body = split_front_matter("---\n---\nbody\n")
    assert raw == {}
    assert body == "body\n"


def test_split_dotdotdot_terminator() -> None:
    raw, _body = split_front_matter("---\nkey: v\n...\nbody\n")
    assert raw == {"key": "v"}


def test_split_too_large() -> None:
    big = "---\n" + ("k: " + "x" * 100 + "\n") * 200 + "---\n"
    with pytest.raises(FrontMatterError, match="exceeds"):
        split_front_matter(big)


def test_split_not_mapping() -> None:
    with pytest.raises(FrontMatterError, match="mapping"):
        split_front_matter("---\n- a\n- b\n---\n")


def test_split_bad_yaml() -> None:
    with pytest.raises(FrontMatterError, match="valid YAML"):
        split_front_matter("---\n: ::\nbad\n---\n")


def test_dump_front_matter_flow_lists() -> None:
    out = dump_front_matter({"tags": ["a", "b"], "title": "x"})
    assert "[a, b]" in out
    assert out.startswith("---\n")
    assert out.endswith("---\n")


# --- contributor hints ----------------------------------------------------


def test_contributor_hints_valid(taxonomy) -> None:
    hints, problems = validate_contributor_hints(
        {"category": "offensive-security", "tags": ["nmap"], "title": "T"},
        taxonomy,
    )
    assert not problems
    assert hints["category"] == "offensive-security"
    assert hints["tags"] == ("nmap",)


def test_contributor_hints_unknown_key(taxonomy) -> None:
    _, problems = validate_contributor_hints({"bogus": 1}, taxonomy)
    assert any("unknown" in p for p in problems)


def test_contributor_hints_invalid_value_dropped(taxonomy) -> None:
    hints, problems = validate_contributor_hints({"category": "nope"}, taxonomy)
    assert "category" not in hints
    assert problems


def test_single_line_non_string(taxonomy) -> None:
    raw = _valid_raw()
    raw["title"] = 123
    with pytest.raises(FrontMatterError, match="title"):
        parse_front_matter(raw, taxonomy)


def test_single_line_too_long(taxonomy) -> None:
    raw = _valid_raw()
    raw["title"] = "x" * 500
    with pytest.raises(FrontMatterError, match="exceeds"):
        parse_front_matter(raw, taxonomy)


def test_too_many_authors(taxonomy) -> None:
    raw = _valid_raw()
    raw["authors"] = [f"Author {i}" for i in range(25)]
    with pytest.raises(FrontMatterError, match="at most"):
        parse_front_matter(raw, taxonomy)


def test_added_wrong_type(taxonomy) -> None:
    raw = _valid_raw()
    raw["added"] = 20260101
    with pytest.raises(FrontMatterError, match="ISO date"):
        parse_front_matter(raw, taxonomy)
