"""Tests for the heuristic and LLM classifiers."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import pytest

from cyberkb.classify.base import Document
from cyberkb.classify.heuristic import (
    classify,
    detect_format,
    humanize_stem,
    infer_title,
    score_categories,
    select_tags,
)
from cyberkb.classify.llm import LLMClassifier
from cyberkb.classify.schema import build_prompt, response_schema, system_instruction
from cyberkb.llm import GeminiClient, HttpResponse

if TYPE_CHECKING:
    from collections.abc import Mapping

    from cyberkb.taxonomy import Taxonomy


def test_classify_offensive_document(taxonomy: Taxonomy) -> None:
    """An offensive-security document is classified with a confident heuristic result."""
    body = (
        "# Penetration Testing with Metasploit\n\n"
        "This red team guide covers exploitation, meterpreter payloads, privilege escalation "
        "and post exploitation during an authorized penetration testing engagement.\n"
    )
    result = classify(Document("1", "metasploit-guide", body), taxonomy)
    assert result.category == "offensive-security"
    assert result.method == "heuristic"
    assert 0.0 < result.confidence <= 1.0
    assert result.title == "Penetration Testing with Metasploit"


def test_classify_routes_to_staging_when_weak(taxonomy: Taxonomy) -> None:
    """Weak evidence routes a document to the staging category with zero confidence."""
    result = classify(
        Document("1", "misc", "Some unrelated prose with no security terms at all here."),
        taxonomy,
    )
    assert result.category == taxonomy.staging.id
    assert result.confidence == 0.0


def test_score_categories_all_zero(taxonomy: Taxonomy) -> None:
    """Empty input scores every non-staging category at zero."""
    scores = score_categories(taxonomy, title="", stem="", heading_text="", body="")
    assert set(scores) == {c.id for c in taxonomy.categories if not c.staging}
    assert all(v == 0.0 for v in scores.values())


@pytest.mark.parametrize(
    ("stem", "expected"),
    [
        ("2019_free-stellar-lumens", "Free Stellar Lumens"),
        ("windows_api_for_red_team", "Windows API for Red Team"),
        ("osint_overview", "OSINT Overview"),
        ("", "Untitled"),
    ],
)
def test_humanize_stem(stem: str, expected: str) -> None:
    """A filename stem becomes a readable title with year prefixes and acronyms handled."""
    assert humanize_stem(stem) == expected


def test_infer_title_from_h1() -> None:
    """A document's H1 is preferred as the title."""
    assert infer_title("# Real Title\n\nbody", "fallback-stem") == "Real Title"


def test_infer_title_skips_generic_h1() -> None:
    """A generic H1 ('Introduction') is skipped in favour of the humanised stem."""
    assert infer_title("# Introduction\n\nbody", "my-doc-stem") == "My Doc Stem"


def test_infer_title_fallback_to_stem() -> None:
    """With no heading, the humanised filename stem is the title."""
    assert infer_title("no heading here", "the-file-name") == "The File Name"


@pytest.mark.parametrize(
    ("title", "stem", "body", "expected"),
    [
        ("SQL Cheat Sheet", "sql_cheatsheet", "x", "cheatsheet"),
        ("Hardening Checklist", "checklist", "x", "checklist"),
        ("IR Playbook", "playbook", "x", "playbook"),
        ("Exam Notes", "notes", "x", "course-notes"),
        ("A Whitepaper", "paper", "x", "paper"),
        ("Tools Collection", "tools", "x", "reference"),
        ("2020 Something", "2020_something", "# H\n\nbody", "article"),
        ("Generic Doc", "generic", "short body", "guide"),
    ],
)
def test_detect_format(title: str, stem: str, body: str, expected: str) -> None:
    """Format is inferred from naming conventions and, failing those, document shape."""
    assert detect_format(title, stem, body) == expected


def test_detect_format_book_by_length() -> None:
    """A very long document is classified as a book."""
    big = " ".join(["word"] * 50_000)
    assert detect_format("Title", "stem", big) == "book"


def test_select_tags_from_title(taxonomy: Taxonomy) -> None:
    """A tag evidenced by the title is selected."""
    tags = select_tags(taxonomy, title="Nmap scanning", stem="nmap", body="port scanning details")
    assert "nmap" in tags


def test_select_tags_empty(taxonomy: Taxonomy) -> None:
    """Text with no vocabulary evidence selects no tags."""
    assert select_tags(taxonomy, title="", stem="", body="nothing notable") == ()


# --- schema ---------------------------------------------------------------


def test_response_schema_enums(taxonomy: Taxonomy) -> None:
    """The response schema constrains category to the taxonomy's ids."""
    schema = response_schema(taxonomy)
    item = schema["properties"]["classifications"]["items"]
    assert item["properties"]["category"]["enum"] == list(taxonomy.category_ids)


def test_system_instruction_mentions_categories(taxonomy: Taxonomy) -> None:
    """The system instruction lists the real category ids."""
    text = system_instruction(taxonomy)
    assert "offensive-security" in text


def test_build_prompt() -> None:
    """The batch prompt echoes each document's ref and body."""
    prompt = build_prompt([("r1", "stem", "body text")])
    assert "r1" in prompt
    assert "body text" in prompt


# --- LLM classifier with a fake transport --------------------------------


class FakeTransport:
    """A transport that returns one canned response and counts calls."""

    def __init__(self, response: HttpResponse) -> None:
        """Store the canned response."""
        self.response = response
        self.calls = 0

    def post(
        self,
        _url: str,
        _payload: bytes,
        _headers: Mapping[str, str],
        _timeout: float,
    ) -> HttpResponse:
        """Return the canned response, recording the call."""
        self.calls += 1
        return self.response


def _ok_response(items: list[dict[str, Any]]) -> HttpResponse:
    """Wrap classification items in a well-formed Gemini success envelope."""
    payload = {
        "candidates": [{"content": {"parts": [{"text": json.dumps({"classifications": items})}]}}],
    }
    return HttpResponse(200, json.dumps(payload).encode())


def _client(response: HttpResponse, taxonomy: Taxonomy) -> LLMClassifier:
    """Build an LLM classifier whose transport returns ``response``."""
    transport = FakeTransport(response)
    client = GeminiClient("key", ("gemini-test",), transport=transport, sleep=lambda _s: None)
    return LLMClassifier(client, taxonomy)


def test_llm_classifier_valid(taxonomy: Taxonomy) -> None:
    """A valid LLM response is used as the classification."""
    item = {
        "ref": "0",
        "title": "Nmap Guide",
        "category": "offensive-security",
        "format": "guide",
        "language": "en",
        "tags": ["nmap"],
        "summary": "A guide.",
        "confidence": 0.9,
    }
    classifier = _client(_ok_response([item]), taxonomy)
    results = classifier.classify_batch([Document("0", "nmap", "body about nmap scanning")])
    assert results[0].category == "offensive-security"
    assert results[0].method == "llm"
    assert results[0].model == "gemini-test"
    assert results[0].tags == ("nmap",)


def test_llm_classifier_empty_input(taxonomy: Taxonomy) -> None:
    """Classifying no documents returns no results and makes no call."""
    classifier = _client(_ok_response([]), taxonomy)
    assert classifier.classify_batch([]) == []


def test_llm_classifier_falls_back_on_missing_doc(taxonomy: Taxonomy) -> None:
    """A document the model omitted falls back to the heuristic."""
    classifier = _client(_ok_response([]), taxonomy)
    body = "red team exploitation and metasploit payloads for penetration testing"
    results = classifier.classify_batch([Document("0", "pentest", body)])
    assert results[0].method == "heuristic"


def _item(**overrides: Any) -> dict[str, Any]:  # noqa: ANN401 -- heterogeneous LLM-item fields
    """A valid LLM classification item with the given fields overridden."""
    base = {
        "ref": "0",
        "category": "offensive-security",
        "format": "guide",
        "language": "en",
        "tags": [],
        "summary": "s",
        "confidence": 0.9,
    }
    return {**base, **overrides}


@pytest.mark.parametrize(
    "bad_item",
    [
        pytest.param(_item(category="nonexistent"), id="unknown-category"),
        pytest.param(_item(format="bad"), id="unknown-format"),
        pytest.param(_item(language="xx"), id="unknown-language"),
        pytest.param(_item(confidence=0.1), id="below-confidence-floor"),
        pytest.param(_item(confidence="x"), id="non-numeric-confidence"),
        pytest.param(_item(category="uncategorized"), id="staging-category"),
    ],
)
def test_llm_classifier_rejects_invalid_item(taxonomy: Taxonomy, bad_item: dict[str, Any]) -> None:
    """Any invalid field in an LLM item forces that document to the heuristic."""
    classifier = _client(_ok_response([bad_item]), taxonomy)
    body = "red team exploitation metasploit payload penetration testing privilege escalation"
    results = classifier.classify_batch([Document("0", "pentest", body)])
    assert results[0].method == "heuristic"


def test_llm_classifier_fallback_on_llm_error(taxonomy: Taxonomy) -> None:
    """When the service keeps failing, the whole batch falls back to the heuristic."""
    transport = FakeTransport(HttpResponse(500, b"err"))
    client = GeminiClient("key", ("m",), transport=transport, sleep=lambda _s: None, max_retries=2)
    classifier = LLMClassifier(client, taxonomy)
    body = "red team exploitation metasploit penetration testing"
    results = classifier.classify_batch([Document("0", "pentest", body)])
    assert results[0].method == "heuristic"


def test_llm_classifier_missing_title_uses_inferred(taxonomy: Taxonomy) -> None:
    """An empty LLM title is replaced by the document's inferred title."""
    item = {
        "ref": "0",
        "title": "",
        "category": "offensive-security",
        "format": "guide",
        "language": "en",
        "tags": [],
        "summary": "s",
        "confidence": 0.9,
    }
    classifier = _client(_ok_response([item]), taxonomy)
    results = classifier.classify_batch([Document("0", "my-pentest-notes", "# Real H1\n\nbody")])
    assert results[0].title == "Real H1"
