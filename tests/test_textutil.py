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
    assert textutil.tokenize(raw) == expected


def test_strip_unsafe_chars_removes_controls_and_bidi() -> None:
    text = "a\x00b\x07‮c﻿d"
    assert textutil.strip_unsafe_chars(text) == "abcd"


def test_strip_unsafe_chars_keeps_tab_newline_cr() -> None:
    assert textutil.strip_unsafe_chars("a\tb\nc\rd") == "a\tb\nc\rd"


def test_fold_is_ascii_lowercase() -> None:
    # Accents fold to their base letter; characters with no ASCII base
    # (such as the sharp s) are dropped rather than transliterated.
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
    assert textutil.slugify(text) == expected


def test_slugify_max_len_cuts_on_word_boundary() -> None:
    slug = textutil.slugify("alpha beta gamma delta epsilon", max_len=14)
    assert len(slug) <= 14
    assert not slug.endswith("-")


def test_slugify_max_len_hard_cut_when_no_boundary() -> None:
    # No separators in the back half: a hard cut is used.
    assert textutil.slugify("aaaaaaaaaaaaaaaaaaoo", max_len=5) == "aaaaa"


@given(st.text(), st.integers(min_value=1, max_value=80))
def test_slugify_always_valid(text: str, max_len: int) -> None:
    slug = textutil.slugify(text, max_len=max_len)
    assert slug
    assert len(slug) <= max_len
    assert all(c.islower() or c.isdigit() or c == "-" for c in slug)
    assert not slug.startswith("-")
    assert not slug.endswith("-")


def test_ngram_counts() -> None:
    counts = textutil.ngram_counts(["a", "b", "c"], max_n=2)
    assert counts[("a",)] == 1
    assert counts[("a", "b")] == 1
    assert counts[("b", "c")] == 1
    assert counts[("a", "b", "c")] == 0
    assert isinstance(counts, Counter)


def test_ngram_counts_repeats() -> None:
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
    assert textutil.truncate(text, max_len) == expected


def test_truncate_hard_cut_without_boundary() -> None:
    out = textutil.truncate("abcdefghijklmnop", 6)
    assert out.endswith("…")
    assert len(out) <= 6


def test_plain_text_strips_markdown_and_links() -> None:
    raw = "See [the guide](http://x.test) and ![pic](p.png) `code` **bold** <b>x</b>"
    out = textutil.plain_text(raw)
    assert "http://x.test" not in out
    assert "the guide" in out
    assert "pic" in out
    assert "<b>" not in out


def test_plain_text_truncates() -> None:
    assert textutil.plain_text("a b c d e f g", max_len=5).endswith("…")


def test_phrase_tokens() -> None:
    assert textutil.phrase_tokens("Active Directory") == ("active", "directory")


@pytest.mark.parametrize(
    ("text", "expected"),
    [("one two three", 3), ("", 0), ("a_b c-d", 3)],
)
def test_word_count(text: str, expected: int) -> None:
    assert textutil.word_count(text) == expected


@given(st.text())
def test_strip_unsafe_chars_is_idempotent(text: str) -> None:
    once = textutil.strip_unsafe_chars(text)
    assert textutil.strip_unsafe_chars(once) == once
