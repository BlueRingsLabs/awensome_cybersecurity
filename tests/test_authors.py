"""Tests for best-effort author extraction."""

from __future__ import annotations

import pytest

from cyberkb.authors import extract_authors


def test_byline_single_author() -> None:
    """A simple 'By Name' byline yields that author."""
    assert extract_authors("# Title\n\nBy Jane Roe\n\nbody") == ("Jane Roe",)


def test_byline_author_colon() -> None:
    """An 'Author:' byline is recognised."""
    assert extract_authors("Author: John Smith\n") == ("John Smith",)


def test_byline_multiple_authors_split() -> None:
    """Several names joined by commas/and are split into separate authors."""
    assert extract_authors("By Alice Adams, Bob Brown and Carol Clark\n") == (
        "Alice Adams",
        "Bob Brown",
        "Carol Clark",
    )


def test_byline_all_caps_is_title_cased() -> None:
    """An all-caps byline name is normalised to title case."""
    assert extract_authors("By HARSH PATEL\n") == ("Harsh Patel",)


def test_byline_capped_at_max() -> None:
    """No more than the maximum number of authors is returned."""
    names = ", ".join(f"Aa{i}x Bb{i}y" for i in "abcdef")  # six name-like pieces
    result = extract_authors(f"By {names}\n")
    assert 0 < len(result) <= 4


def test_linkedin_slug_used_when_no_byline() -> None:
    """A LinkedIn slug provides the author when there is no byline."""
    assert extract_authors("Notes\nhttps://www.linkedin.com/in/jane-mary-roe\n") == (
        "Jane Mary Roe",
    )


def test_linkedin_slug_heals_hyphen_linebreak() -> None:
    """A profile link split across a hyphenated line break is rejoined."""
    body = "Guide\nhttps://www.linkedin.com/in/joas-antonio-dos-\nsantos\nWarning\n"
    assert extract_authors(body) == ("Joas Antonio Dos Santos",)


def test_byline_canonicalised_against_linkedin() -> None:
    """A truncated byline is upgraded to the fuller LinkedIn-derived name."""
    body = "By Joas Antonio\nhttps://www.linkedin.com/in/joas-antonio-dos-santos\n"
    assert extract_authors(body) == ("Joas Antonio Dos Santos",)


def test_canonicalisation_dedupes_collapsed_names() -> None:
    """Two truncated bylines collapsing to the same full name are de-duplicated."""
    body = (
        "By Joas Antonio, Joas Antonio Dos\nhttps://www.linkedin.com/in/joas-antonio-dos-santos\n"
    )
    assert extract_authors(body) == ("Joas Antonio Dos Santos",)


def test_name_with_digits_rejected() -> None:
    """A byline token containing digits is not treated as a name."""
    assert extract_authors("By Ahmed Allam 42950622b\n") == ()


def test_generic_token_rejected() -> None:
    """A heading-like phrase sharing a banned word is not an author."""
    assert extract_authors("By Security Overview\n") == ()


def test_single_word_rejected() -> None:
    """A single word is not accepted as a full name."""
    assert extract_authors("By Madonna\n") == ()


def test_overlong_name_rejected() -> None:
    """A name longer than the length cap is rejected."""
    long_name = " ".join(["Verylongword"] * 8)
    assert extract_authors(f"By {long_name}\n") == ()


def test_byline_inside_code_fence_ignored() -> None:
    """A byline inside a code fence is not treated as attribution."""
    body = "```\nBy Not Anauthor\n```\n\nplain body text here\n"
    assert extract_authors(body) == ()


def test_byline_beyond_scan_window_ignored() -> None:
    """A byline far below the top of the document is not scanned."""
    body = "x\n" * 60 + "By Jane Roe\n"
    assert extract_authors(body) == ()


def test_linkedin_slug_too_short_rejected() -> None:
    """A one-token LinkedIn slug does not yield a name."""
    assert extract_authors("https://www.linkedin.com/in/madonna\n") == ()


def test_no_author_returns_empty() -> None:
    """Prose with no byline or profile link yields no authors."""
    assert extract_authors("Just some prose about security with no attribution.\n") == ()


@pytest.mark.parametrize(
    "prefix",
    ["By", "Author:", "Authors -", "Written by", "Created by"],
)
def test_byline_prefixes(prefix: str) -> None:
    """Each supported byline prefix is recognised."""
    assert extract_authors(f"{prefix} Jane Roe\n") == ("Jane Roe",)
