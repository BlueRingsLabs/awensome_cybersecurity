"""Tests for the heuristic and LLM classifiers."""

from __future__ import annotations

import json

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


def test_classify_offensive_document(taxonomy) -> None:
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


def test_classify_routes_to_staging_when_weak(taxonomy) -> None:
    result = classify(
        Document("1", "misc", "Some unrelated prose with no security terms at all here."), taxonomy
    )
    assert result.category == taxonomy.staging.id
    assert result.confidence == 0.0


def test_score_categories_all_zero(taxonomy) -> None:
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
    assert humanize_stem(stem) == expected


def test_infer_title_from_h1(taxonomy) -> None:
    assert infer_title("# Real Title\n\nbody", "fallback-stem") == "Real Title"


def test_infer_title_skips_generic_h1() -> None:
    assert infer_title("# Introduction\n\nbody", "my-doc-stem") == "My Doc Stem"


def test_infer_title_fallback_to_stem() -> None:
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
    assert detect_format(title, stem, body) == expected


def test_detect_format_book_by_length() -> None:
    big = " ".join(["word"] * 50_000)
    assert detect_format("Title", "stem", big) == "book"


def test_select_tags_from_title(taxonomy) -> None:
    tags = select_tags(taxonomy, title="Nmap scanning", stem="nmap", body="port scanning details")
    assert "nmap" in tags


def test_select_tags_empty(taxonomy) -> None:
    assert select_tags(taxonomy, title="", stem="", body="nothing notable") == ()


# --- schema ---------------------------------------------------------------


def test_response_schema_enums(taxonomy) -> None:
    schema = response_schema(taxonomy)
    item = schema["properties"]["classifications"]["items"]
    assert item["properties"]["category"]["enum"] == list(taxonomy.category_ids)


def test_system_instruction_mentions_categories(taxonomy) -> None:
    text = system_instruction(taxonomy)
    assert "offensive-security" in text


def test_build_prompt(taxonomy) -> None:
    prompt = build_prompt([("r1", "stem", "body text")])
    assert "r1" in prompt
    assert "body text" in prompt


# --- LLM classifier with a fake transport --------------------------------


class FakeTransport:
    def __init__(self, response: HttpResponse) -> None:
        self.response = response
        self.calls = 0

    def post(self, url, payload, headers, timeout):
        self.calls += 1
        return self.response


def _ok_response(items: list[dict]) -> HttpResponse:
    payload = {
        "candidates": [{"content": {"parts": [{"text": json.dumps({"classifications": items})}]}}]
    }
    return HttpResponse(200, json.dumps(payload).encode())


def _client(response: HttpResponse, taxonomy) -> LLMClassifier:
    transport = FakeTransport(response)
    client = GeminiClient("key", ("gemini-test",), transport=transport, sleep=lambda _s: None)
    return LLMClassifier(client, taxonomy)


def test_llm_classifier_valid(taxonomy) -> None:
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


def test_llm_classifier_empty_input(taxonomy) -> None:
    classifier = _client(_ok_response([]), taxonomy)
    assert classifier.classify_batch([]) == []


def test_llm_classifier_falls_back_on_missing_doc(taxonomy) -> None:
    classifier = _client(_ok_response([]), taxonomy)
    body = "red team exploitation and metasploit payloads for penetration testing"
    results = classifier.classify_batch([Document("0", "pentest", body)])
    assert results[0].method == "heuristic"


@pytest.mark.parametrize(
    "bad_item",
    [
        {
            "ref": "0",
            "category": "nonexistent",
            "format": "guide",
            "language": "en",
            "confidence": 0.9,
        },
        {
            "ref": "0",
            "category": "offensive-security",
            "format": "bad",
            "language": "en",
            "confidence": 0.9,
        },
        {
            "ref": "0",
            "category": "offensive-security",
            "format": "guide",
            "language": "xx",
            "confidence": 0.9,
        },
        {
            "ref": "0",
            "category": "offensive-security",
            "format": "guide",
            "language": "en",
            "confidence": 0.1,
        },
        {
            "ref": "0",
            "category": "offensive-security",
            "format": "guide",
            "language": "en",
            "confidence": "x",
        },
        {
            "ref": "0",
            "category": "uncategorized",
            "format": "guide",
            "language": "en",
            "confidence": 0.9,
        },
    ],
)
def test_llm_classifier_rejects_invalid_item(taxonomy, bad_item: dict) -> None:
    classifier = _client(_ok_response([bad_item]), taxonomy)
    body = "red team exploitation metasploit payload penetration testing privilege escalation"
    results = classifier.classify_batch([Document("0", "pentest", body)])
    assert results[0].method == "heuristic"


def test_llm_classifier_fallback_on_llm_error(taxonomy) -> None:
    # HTTP 500 is retryable; with retries exhausted the whole batch falls back.
    transport = FakeTransport(HttpResponse(500, b"err"))
    client = GeminiClient("key", ("m",), transport=transport, sleep=lambda _s: None, max_retries=2)
    classifier = LLMClassifier(client, taxonomy)
    body = "red team exploitation metasploit penetration testing"
    results = classifier.classify_batch([Document("0", "pentest", body)])
    assert results[0].method == "heuristic"


def test_llm_classifier_missing_title_uses_inferred(taxonomy) -> None:
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
