"""Tests for text normalisation primitives."""

from __future__ import annotations

from collections import Counter

import pytest
from hypothesis import given
from hypothesis import strategies as st

from cyberkb import textutil


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Active Directory", ["active", "directory"]),
        ("active_directory", ["active", "directory"]),
        ("active-directory", ["active", "directory"]),
        ("Kerberoasting!!!", ["kerberoasting"]),
        ("", []),
        ("Café São 2024", ["cafe", "sao", "2024"]),
    ],
)
def test_tokenize(raw: str, expected: list[str]) -> None:
    """Separators, punctuation and accents all reduce to lowercase ASCII tokens."""
    assert textutil.tokenize(raw) == expected


def test_strip_unsafe_chars_removes_controls_and_bidi() -> None:
    """Control characters, a bidi override (U+202E) and a BOM (U+FEFF) are removed.

    The hostile characters are built with ``chr`` so the test source itself stays
    free of control characters.
    """
    text = "a" + chr(0x00) + "b" + chr(0x07) + chr(0x202E) + "c" + chr(0xFEFF) + "d"
    assert textutil.strip_unsafe_chars(text) == "abcd"


def test_strip_unsafe_chars_keeps_tab_newline_cr() -> None:
    """Whitespace control characters that structure text are preserved."""
    assert textutil.strip_unsafe_chars("a\tb\nc\rd") == "a\tb\nc\rd"


def test_fold_is_ascii_lowercase() -> None:
    """Accents fold to their base letter; a character with no ASCII base is dropped."""
    assert textutil.fold("ÄÖÜ Ç") == "aou c"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello World", "hello-world"),
        ("  spaced  out  ", "spaced-out"),
        ("***", "untitled"),
        ("C++ for Hackers", "c-for-hackers"),
    ],
)
def test_slugify(text: str, expected: str) -> None:
    """Slugs are lowercase kebab-case, and an empty result falls back to 'untitled'."""
    assert textutil.slugify(text) == expected


def test_slugify_max_len_cuts_on_word_boundary() -> None:
    """A length-limited slug is cut at a separator and never ends with one."""
    slug = textutil.slugify("alpha beta gamma delta epsilon", max_len=14)
    assert len(slug) <= 14
    assert not slug.endswith("-")


def test_slugify_max_len_hard_cut_when_no_boundary() -> None:
    """With no separator in the back half, the slug is hard-cut to the limit."""
    assert textutil.slugify("aaaaaaaaaaaaaaaaaaoo", max_len=5) == "aaaaa"


@given(st.text(), st.integers(min_value=1, max_value=80))
def test_slugify_always_valid(text: str, max_len: int) -> None:
    """For any input and limit, a slug is non-empty, bounded and well-formed."""
    slug = textutil.slugify(text, max_len=max_len)
    assert slug
    assert len(slug) <= max_len
    assert all(c.islower() or c.isdigit() or c == "-" for c in slug)
    assert not slug.startswith("-")
    assert not slug.endswith("-")


def test_ngram_counts() -> None:
    """N-grams of length 1..max_n are counted; longer spans are absent."""
    counts = textutil.ngram_counts(["a", "b", "c"], max_n=2)
    assert counts[("a",)] == 1
    assert counts[("a", "b")] == 1
    assert counts[("b", "c")] == 1
    assert counts[("a", "b", "c")] == 0
    assert isinstance(counts, Counter)


def test_ngram_counts_repeats() -> None:
    """Repeated tokens accumulate their n-gram counts."""
    counts = textutil.ngram_counts(["x", "x", "x"], max_n=2)
    assert counts[("x",)] == 3
    assert counts[("x", "x")] == 2


@pytest.mark.parametrize(
    ("text", "max_len", "expected"),
    [
        ("short", 10, "short"),
        ("exactly-ten", 11, "exactly-ten"),
        ("one two three four", 12, "one two…"),
    ],
)
def test_truncate(text: str, max_len: int, expected: str) -> None:
    """Truncation keeps whole words and appends an ellipsis only when shortened."""
    assert textutil.truncate(text, max_len) == expected


def test_truncate_hard_cut_without_boundary() -> None:
    """A single long word is hard-cut and still bounded by the limit."""
    out = textutil.truncate("abcdefghijklmnop", 6)
    assert out.endswith("…")
    assert len(out) <= 6


def test_plain_text_strips_markdown_and_links() -> None:
    """Links/images keep their label, while URLs, emphasis and HTML tags are dropped."""
    raw = "See [the guide](http://x.test) and ![pic](p.png) `code` **bold** <b>x</b>"
    out = textutil.plain_text(raw)
    assert "http://x.test" not in out
    assert "the guide" in out
    assert "pic" in out
    assert "<b>" not in out


def test_plain_text_truncates() -> None:
    """plain_text honours the optional length cap."""
    assert textutil.plain_text("a b c d e f g", max_len=5).endswith("…")


def test_phrase_tokens() -> None:
    """A keyword phrase tokenises to a tuple for n-gram lookups."""
    assert textutil.phrase_tokens("Active Directory") == ("active", "directory")


@pytest.mark.parametrize(
    ("text", "expected"),
    [("one two three", 3), ("", 0), ("a_b c-d", 3)],
)
def test_word_count(text: str, expected: int) -> None:
    """Word counting treats underscore/hyphen groups as the expected token count."""
    assert textutil.word_count(text) == expected


@given(st.text())
def test_strip_unsafe_chars_is_idempotent(text: str) -> None:
    """Stripping unsafe characters twice equals stripping once, for any input."""
    once = textutil.strip_unsafe_chars(text)
    assert textutil.strip_unsafe_chars(once) == once


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ('{"a": 1}', '{"a": 1}'),
        ('  ```json\n{"a": 1}\n```  ', '{"a": 1}'),
        ('```\n{"a": 1}\n```', '{"a": 1}'),
        ('```json\n{"a": 1}', '{"a": 1}'),
        ("```", ""),
    ],
)
def test_unfence(text: str, expected: str) -> None:
    """A surrounding code fence is removed; a missing closing fence is tolerated."""
    assert textutil.unfence(text) == expected
