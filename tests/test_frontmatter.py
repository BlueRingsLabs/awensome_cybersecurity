"""Tests for front matter parsing, validation and serialisation."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

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

if TYPE_CHECKING:
    from collections.abc import Callable

    from cyberkb.taxonomy import Taxonomy


def _valid_raw() -> dict[str, Any]:
    """Return a fully valid raw front-matter mapping."""
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


def test_parse_valid(taxonomy: Taxonomy) -> None:
    """A valid mapping parses into the typed front-matter model."""
    fm = parse_front_matter(_valid_raw(), taxonomy)
    assert fm.id == "ckb-0123456789ab"
    assert fm.category == "offensive-security"
    assert fm.tags == ("nmap",)
    assert fm.classification.method == "manual"


def test_roundtrip_render_and_split(taxonomy: Taxonomy) -> None:
    """Rendering then splitting a document reproduces the same front matter."""
    fm = parse_front_matter(_valid_raw(), taxonomy)
    doc = render_document(fm, "# Body\n\ntext\n")
    raw, body = split_front_matter(doc)
    assert raw is not None
    reparsed = parse_front_matter(raw, taxonomy)
    assert reparsed == fm
    assert body.startswith("# Body")


def test_to_dict_omits_empty_optionals() -> None:
    """Empty optional fields are omitted from the serialised mapping."""
    fm = make_front_matter(tags=(), summary="", authors=(), source_url=None)
    data = fm.to_dict()
    assert "tags" not in data
    assert "summary" not in data
    assert "authors" not in data
    assert "source_url" not in data


def test_to_dict_includes_llm_model() -> None:
    """An LLM classification serialises its model name."""
    fm = make_front_matter(classification=Classification("llm", 0.9, "gemini-x"))
    assert fm.to_dict()["classification"]["model"] == "gemini-x"


def test_to_dict_includes_reference_only() -> None:
    """A reference-only resource serialises the flag."""
    fm = make_front_matter(reference_only=True)
    assert fm.to_dict()["reference_only"] is True


def test_reference_only_defaults_false(taxonomy: Taxonomy) -> None:
    """Omitting reference_only yields False and no serialised key."""
    fm = parse_front_matter(_valid_raw(), taxonomy)
    assert fm.reference_only is False
    assert "reference_only" not in fm.to_dict()


def test_classified_by_valid_roundtrips(taxonomy: Taxonomy) -> None:
    """A well-formed provenance stamp parses, serialises and round-trips."""
    stamp = "gemini:gemini-2.5-flash@2026-10-05T14:23:11Z"
    raw = _valid_raw()
    raw["classified_by"] = stamp
    fm = parse_front_matter(raw, taxonomy)
    assert fm.classified_by == stamp
    assert fm.to_dict()["classified_by"] == stamp
    reparsed_raw, _ = split_front_matter(render_document(fm, "# b\n\nx\n"))
    assert reparsed_raw is not None
    assert parse_front_matter(reparsed_raw, taxonomy).classified_by == stamp


def test_classified_by_heuristic_stamp_without_model(taxonomy: Taxonomy) -> None:
    """A provider-only stamp (no model, e.g. the heuristic) is accepted."""
    raw = _valid_raw()
    raw["classified_by"] = "heuristic@2026-10-05T14:23:11Z"
    assert parse_front_matter(raw, taxonomy).classified_by == "heuristic@2026-10-05T14:23:11Z"


def test_classified_by_defaults_none_and_is_omitted(taxonomy: Taxonomy) -> None:
    """Omitting classified_by yields None and no serialised key."""
    fm = parse_front_matter(_valid_raw(), taxonomy)
    assert fm.classified_by is None
    assert "classified_by" not in fm.to_dict()


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
        lambda d: d.update(reference_only="yes"),
        lambda d: d.update(classified_by=123),
        lambda d: d.update(classified_by="not-a-stamp"),
        lambda d: d.update(classified_by="gemini:" + "m" * 250 + "@2026-10-05T14:23:11Z"),
        lambda d: d.update(classification={"method": "manual"}),
        lambda d: d.update(classification={"method": "llm", "confidence": 0.9}),
        lambda d: d.update(classification={"method": "bad", "confidence": 0.5}),
        lambda d: d.update(classification={"method": "manual", "confidence": 2}),
        lambda d: d.update(classification="notadict"),
        lambda d: d.update(unknown_key="x"),
    ],
)
def test_invalid_front_matter(
    taxonomy: Taxonomy,
    mutate: Callable[[dict[str, Any]], object],
) -> None:
    """Each individual front-matter defect is rejected."""
    raw = _valid_raw()
    mutate(raw)
    with pytest.raises(FrontMatterError):
        parse_front_matter(raw, taxonomy)


def test_multiple_problems_reported(taxonomy: Taxonomy) -> None:
    """Several defects are reported together, not just the first."""
    raw = _valid_raw()
    raw.update(title="", category="bad")
    with pytest.raises(FrontMatterError) as exc:
        parse_front_matter(raw, taxonomy)
    assert ";" in str(exc.value)


def test_classification_unknown_key(taxonomy: Taxonomy) -> None:
    """An unknown key inside classification is rejected."""
    raw = _valid_raw()
    raw["classification"] = {"method": "manual", "confidence": 1.0, "bogus": 1}
    with pytest.raises(FrontMatterError, match="unknown keys"):
        parse_front_matter(raw, taxonomy)


def test_classification_bool_confidence_rejected(taxonomy: Taxonomy) -> None:
    """A boolean confidence is not accepted as a number."""
    raw = _valid_raw()
    raw["classification"] = {"method": "manual", "confidence": True}
    with pytest.raises(FrontMatterError):
        parse_front_matter(raw, taxonomy)


def test_classification_bad_model_type(taxonomy: Taxonomy) -> None:
    """An empty model string is rejected."""
    raw = _valid_raw()
    raw["classification"] = {"method": "llm", "confidence": 0.9, "model": ""}
    with pytest.raises(FrontMatterError):
        parse_front_matter(raw, taxonomy)


# --- split_front_matter edge cases ---------------------------------------


def test_split_no_front_matter() -> None:
    """A document without a block returns no front matter and the full body."""
    raw, body = split_front_matter("# Just a doc\n")
    assert raw is None
    assert body == "# Just a doc\n"


def test_split_unterminated_is_thematic_break() -> None:
    """An unterminated leading '---' is treated as prose, not front matter."""
    raw, _body = split_front_matter("---\nkey: value\nno closing delimiter\n")
    assert raw is None


def test_split_lone_rule() -> None:
    """A lone '---' line is a thematic break, not front matter."""
    raw, _ = split_front_matter("---\n")
    assert raw is None


def test_split_empty_block() -> None:
    """An empty block parses to an empty mapping."""
    raw, body = split_front_matter("---\n---\nbody\n")
    assert raw == {}
    assert body == "body\n"


def test_split_dotdotdot_terminator() -> None:
    """A '...' terminator closes the front-matter block."""
    raw, _body = split_front_matter("---\nkey: v\n...\nbody\n")
    assert raw == {"key": "v"}


def test_split_too_large() -> None:
    """An oversized front-matter block is rejected."""
    big = "---\n" + ("k: " + "x" * 100 + "\n") * 200 + "---\n"
    with pytest.raises(FrontMatterError, match="exceeds"):
        split_front_matter(big)


def test_split_not_mapping() -> None:
    """A block that decodes to a non-mapping is rejected."""
    with pytest.raises(FrontMatterError, match="mapping"):
        split_front_matter("---\n- a\n- b\n---\n")


def test_split_bad_yaml() -> None:
    """A block that is not valid YAML is rejected."""
    with pytest.raises(FrontMatterError, match="valid YAML"):
        split_front_matter("---\n: ::\nbad\n---\n")


def test_dump_front_matter_flow_lists() -> None:
    """Scalar lists render in flow style inside a delimited block."""
    out = dump_front_matter({"tags": ["a", "b"], "title": "x"})
    assert "[a, b]" in out
    assert out.startswith("---\n")
    assert out.endswith("---\n")


# --- contributor hints ----------------------------------------------------


def test_contributor_hints_valid(taxonomy: Taxonomy) -> None:
    """Valid contributor hints are accepted and normalised."""
    hints, problems = validate_contributor_hints(
        {"category": "offensive-security", "tags": ["nmap"], "title": "T"},
        taxonomy,
    )
    assert not problems
    assert hints["category"] == "offensive-security"
    assert hints["tags"] == ("nmap",)


def test_contributor_hints_unknown_key(taxonomy: Taxonomy) -> None:
    """An unknown contributor key is reported as a problem."""
    _, problems = validate_contributor_hints({"bogus": 1}, taxonomy)
    assert any("unknown" in p for p in problems)


def test_contributor_hints_invalid_value_dropped(taxonomy: Taxonomy) -> None:
    """An invalid hint value is dropped and reported, not accepted."""
    hints, problems = validate_contributor_hints({"category": "nope"}, taxonomy)
    assert "category" not in hints
    assert problems


def test_single_line_non_string(taxonomy: Taxonomy) -> None:
    """A non-string single-line field is rejected."""
    raw = _valid_raw()
    raw["title"] = 123
    with pytest.raises(FrontMatterError, match="title"):
        parse_front_matter(raw, taxonomy)


def test_single_line_too_long(taxonomy: Taxonomy) -> None:
    """A single-line field over its length cap is rejected."""
    raw = _valid_raw()
    raw["title"] = "x" * 500
    with pytest.raises(FrontMatterError, match="exceeds"):
        parse_front_matter(raw, taxonomy)


def test_too_many_authors(taxonomy: Taxonomy) -> None:
    """More authors than the cap is rejected."""
    raw = _valid_raw()
    raw["authors"] = [f"Author {i}" for i in range(25)]
    with pytest.raises(FrontMatterError, match="at most"):
        parse_front_matter(raw, taxonomy)


def test_added_wrong_type(taxonomy: Taxonomy) -> None:
    """An 'added' value that is neither a date nor an ISO string is rejected."""
    raw = _valid_raw()
    raw["added"] = 20260101
    with pytest.raises(FrontMatterError, match="ISO date"):
        parse_front_matter(raw, taxonomy)
