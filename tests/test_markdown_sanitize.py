"""Tests for fence-aware Markdown parsing and sanitisation."""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from cyberkb import markdown, sanitize


def test_headings_ignore_code_fences() -> None:
    text = "# Real Title\n\n```bash\n# not a heading\nnmap -sV\n```\n## Second\n"
    found = markdown.headings(text)
    assert found == [(1, "Real Title"), (2, "Second")]


def test_extract_h1_atx() -> None:
    assert markdown.extract_h1("intro\n# The Title\nmore") == "The Title"


def test_extract_h1_setext() -> None:
    assert markdown.extract_h1("The Title\n=====\n\nbody") == "The Title"


def test_extract_h1_setext_ignores_fenced() -> None:
    text = "```\nFake\n===\n```\n# Genuine\n"
    assert markdown.extract_h1(text) == "Genuine"


def test_extract_h1_none_when_absent() -> None:
    assert markdown.extract_h1("just prose, no heading") is None


def test_extract_h1_respects_max_lines() -> None:
    text = "\n" * 50 + "# Deep Title\n"
    assert markdown.extract_h1(text, max_lines=10) is None


def test_tilde_fence() -> None:
    text = "~~~\n# inside tilde fence\n~~~\n# outside\n"
    assert markdown.headings(text) == [(1, "outside")]


def test_backtick_info_string_with_backtick_is_not_a_fence() -> None:
    # A line like ``` `code` ``` is inline code, not an opening fence.
    text = "`inline` text\n# Heading\n"
    assert markdown.headings(text) == [(1, "Heading")]


def test_longer_closing_fence_closes() -> None:
    text = "````\n# in\n````\n# out\n"
    assert markdown.headings(text) == [(1, "out")]


def test_shorter_fence_does_not_close() -> None:
    text = "````\n```\n# still inside\n````\n# out\n"
    assert markdown.headings(text) == [(1, "out")]


def test_first_text_line_skips_noise() -> None:
    text = "\n12\nhttp://example.test\n# \nActual first line of prose here\n"
    assert markdown.first_text_line(text) == "Actual first line of prose here"


def test_first_text_line_none() -> None:
    assert markdown.first_text_line("1\n2\n3\n") is None


def test_first_text_line_respects_max_lines() -> None:
    assert markdown.first_text_line("\n\n\nText appears late", max_lines=2) is None


def test_active_content_detects_script_outside_fence() -> None:
    hits = markdown.active_content("Hello <script>alert(1)</script> world")
    assert hits
    assert hits[0][0] == 1


def test_active_content_ignores_fenced_payload() -> None:
    text = "```html\n<script>alert(1)</script>\n```\n"
    assert markdown.active_content(text) == []


def test_active_content_ignores_inline_code() -> None:
    assert markdown.active_content("use `<script>` carefully") == []


def test_active_content_detects_js_link() -> None:
    assert markdown.active_content("[click](javascript:alert(1))")


def test_active_content_detects_event_handler() -> None:
    assert markdown.active_content('<div onclick="x()">')


def test_active_content_detects_js_href() -> None:
    assert markdown.active_content('<a href="javascript:x">')


def test_escape_inline() -> None:
    assert markdown.escape_inline("a|b*c") == r"a\|b\*c"


def test_sanitize_removes_page_markers() -> None:
    assert "PAGE" not in sanitize.sanitize_markdown("[[ PAGE 1 ]]\nreal content\n[[ PAGE 2 ]]\n")


def test_sanitize_collapses_blank_runs_outside_fence() -> None:
    out = sanitize.sanitize_markdown("a\n\n\n\n\nb\n")
    assert out == "a\n\nb\n"


def test_sanitize_preserves_blank_lines_in_fence() -> None:
    text = "```\na\n\n\n\nb\n```\n"
    out = sanitize.sanitize_markdown(text)
    assert "a\n\n\n\nb" in out


def test_sanitize_normalises_crlf() -> None:
    assert "\r" not in sanitize.sanitize_markdown("a\r\nb\r\n")


def test_sanitize_empty_is_empty() -> None:
    assert sanitize.sanitize_markdown("   \n\n  ") == ""


def test_sanitize_is_idempotent() -> None:
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
    assert sanitize.strip_tracking_params(url) == expected


def test_strip_tracking_params_handles_invalid_url() -> None:
    bad = "http://[::1/bad?utm_source=x"
    assert sanitize.strip_tracking_params(bad) == bad


def test_sanitize_strips_tracking_in_body() -> None:
    out = sanitize.sanitize_markdown("link http://x.test/a?utm_source=news here\n")
    assert "utm_source" not in out


@given(st.text())
def test_sanitize_idempotent_property(text: str) -> None:
    once = sanitize.sanitize_markdown(text)
    assert sanitize.sanitize_markdown(once) == once


@given(st.text())
def test_sanitize_ends_cleanly(text: str) -> None:
    out = sanitize.sanitize_markdown(text)
    assert out == "" or out.endswith("\n")
    assert "\r" not in out


def test_headings_respects_max_lines() -> None:
    text = "# One\n" * 3 + "# Deep\n"
    found = markdown.headings(text, max_lines=2)
    assert all(level == 1 for level, _ in found)
    assert "Deep" not in [t for _, t in found]
