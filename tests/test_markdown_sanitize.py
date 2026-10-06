"""Tests for fence-aware Markdown parsing and sanitisation."""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from cyberkb import markdown, sanitize


def test_headings_ignore_code_fences() -> None:
    """A '#' line inside a fenced block is not read as a heading."""
    text = "# Real Title\n\n```bash\n# not a heading\nnmap -sV\n```\n## Second\n"
    found = markdown.headings(text)
    assert found == [(1, "Real Title"), (2, "Second")]


def test_extract_h1_atx() -> None:
    """The first ATX level-1 heading is returned as the title."""
    assert markdown.extract_h1("intro\n# The Title\nmore") == "The Title"


def test_extract_h1_setext() -> None:
    """A setext level-1 heading (underlined with '=') is recognised."""
    assert markdown.extract_h1("The Title\n=====\n\nbody") == "The Title"


def test_extract_h1_setext_ignores_fenced() -> None:
    """A setext-looking line inside a fence does not become the title."""
    text = "```\nFake\n===\n```\n# Genuine\n"
    assert markdown.extract_h1(text) == "Genuine"


def test_extract_h1_none_when_absent() -> None:
    """Prose with no heading yields no H1."""
    assert markdown.extract_h1("just prose, no heading") is None


def test_extract_h1_respects_max_lines() -> None:
    """A heading beyond the scan window is not used as the title."""
    text = "\n" * 50 + "# Deep Title\n"
    assert markdown.extract_h1(text, max_lines=10) is None


def test_tilde_fence() -> None:
    """A tilde fence hides its contents just like a backtick fence."""
    text = "~~~\n# inside tilde fence\n~~~\n# outside\n"
    assert markdown.headings(text) == [(1, "outside")]


def test_backtick_info_string_with_backtick_is_not_a_fence() -> None:
    """Inline code (backticks with a backtick in the info string) is not a fence."""
    text = "`inline` text\n# Heading\n"
    assert markdown.headings(text) == [(1, "Heading")]


def test_longer_closing_fence_closes() -> None:
    """A closing fence at least as long as the opener closes the block."""
    text = "````\n# in\n````\n# out\n"
    assert markdown.headings(text) == [(1, "out")]


def test_shorter_fence_does_not_close() -> None:
    """A shorter fence inside a longer one does not close it."""
    text = "````\n```\n# still inside\n````\n# out\n"
    assert markdown.headings(text) == [(1, "out")]


def test_first_text_line_skips_noise() -> None:
    """The first prose line skips blanks, page numbers and bare URLs."""
    text = "\n12\nhttp://example.test\n# \nActual first line of prose here\n"
    assert markdown.first_text_line(text) == "Actual first line of prose here"


def test_first_text_line_none() -> None:
    """Numeric-only lines yield no usable first text line."""
    assert markdown.first_text_line("1\n2\n3\n") is None


def test_first_text_line_respects_max_lines() -> None:
    """Prose beyond the scan window is not returned."""
    assert markdown.first_text_line("\n\n\nText appears late", max_lines=2) is None


def test_active_content_detects_script_outside_fence() -> None:
    """An unfenced <script> tag is flagged with its line number."""
    hits = markdown.active_content("Hello <script>alert(1)</script> world")
    assert hits
    assert hits[0][0] == 1


def test_active_content_ignores_fenced_payload() -> None:
    """A payload inside a code fence is inert and not flagged."""
    text = "```html\n<script>alert(1)</script>\n```\n"
    assert markdown.active_content(text) == []


def test_active_content_ignores_inline_code() -> None:
    """A payload inside inline code is not flagged."""
    assert markdown.active_content("use `<script>` carefully") == []


def test_active_content_detects_js_link() -> None:
    """A javascript: Markdown link target is flagged."""
    assert markdown.active_content("[click](javascript:alert(1))")


def test_active_content_detects_event_handler() -> None:
    """An inline HTML event-handler attribute is flagged."""
    assert markdown.active_content('<div onclick="x()">')


def test_active_content_detects_js_href() -> None:
    """A javascript: href/src attribute is flagged."""
    assert markdown.active_content('<a href="javascript:x">')


def test_escape_inline() -> None:
    """Characters that would break inline Markdown or table cells are escaped."""
    assert markdown.escape_inline("a|b*c") == r"a\|b\*c"


def test_sanitize_removes_page_markers() -> None:
    """PDF '[[ PAGE n ]]' markers are stripped from the body."""
    assert "PAGE" not in sanitize.sanitize_markdown("[[ PAGE 1 ]]\nreal content\n[[ PAGE 2 ]]\n")


def test_sanitize_collapses_blank_runs_outside_fence() -> None:
    """Runs of blank lines collapse to a single blank line outside fences."""
    out = sanitize.sanitize_markdown("a\n\n\n\n\nb\n")
    assert out == "a\n\nb\n"


def test_sanitize_preserves_blank_lines_in_fence() -> None:
    """Blank lines inside a code fence are preserved byte for byte."""
    text = "```\na\n\n\n\nb\n```\n"
    out = sanitize.sanitize_markdown(text)
    assert "a\n\n\n\nb" in out


def test_sanitize_normalises_crlf() -> None:
    """CRLF and CR line endings are normalised to LF."""
    assert "\r" not in sanitize.sanitize_markdown("a\r\nb\r\n")


def test_sanitize_empty_is_empty() -> None:
    """Whitespace-only input sanitises to the empty string."""
    assert sanitize.sanitize_markdown("   \n\n  ") == ""


def test_sanitize_is_idempotent() -> None:
    """Sanitising twice equals sanitising once."""
    raw = "[[ PAGE 1 ]]\n# Title\n\n\n\nbody?utm_source=x\n"
    once = sanitize.sanitize_markdown(raw)
    assert sanitize.sanitize_markdown(once) == once


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("http://x.test/p?utm_source=a&id=5", "http://x.test/p?id=5"),
        ("http://x.test/p?fbclid=abc", "http://x.test/p"),
        ("http://x.test/p?ref=main", "http://x.test/p?ref=main"),
        ("http://x.test/p", "http://x.test/p"),
        ("http://x.test/p?a=1&utm_medium=x&b=2", "http://x.test/p?a=1&b=2"),
    ],
)
def test_strip_tracking_params(url: str, expected: str) -> None:
    """Tracking parameters are removed while meaningful query values are kept."""
    assert sanitize.strip_tracking_params(url) == expected


def test_strip_tracking_params_handles_invalid_url() -> None:
    """An unparseable URL is returned unchanged rather than raising."""
    bad = "http://[::1/bad?utm_source=x"
    assert sanitize.strip_tracking_params(bad) == bad


def test_sanitize_strips_tracking_in_body() -> None:
    """Tracking parameters inside body URLs are stripped during sanitisation."""
    out = sanitize.sanitize_markdown("link http://x.test/a?utm_source=news here\n")
    assert "utm_source" not in out


@given(st.text())
def test_sanitize_idempotent_property(text: str) -> None:
    """For any input, sanitising twice equals sanitising once."""
    once = sanitize.sanitize_markdown(text)
    assert sanitize.sanitize_markdown(once) == once


@given(st.text())
def test_sanitize_ends_cleanly(text: str) -> None:
    """Sanitised output is empty or ends in a single newline, never a CR."""
    out = sanitize.sanitize_markdown(text)
    assert out == "" or out.endswith("\n")
    assert "\r" not in out


def test_headings_respects_max_lines() -> None:
    """Headings past the scan window are excluded."""
    text = "# One\n" * 3 + "# Deep\n"
    found = markdown.headings(text, max_lines=2)
    assert all(level == 1 for level, _ in found)
    assert "Deep" not in [t for _, t in found]
