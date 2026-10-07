"""Tests for the heuristic and LLM classifiers."""

from __future__ import annotations

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
from cyberkb.classify.schema import build_prompt, response_schema, system_instruction
from cyberkb.providers.rotation import RotationSettings
from tests.llmfakes import (
    Router,
    answer,
    default_google_listing,
    google_answer,
    google_error,
    item,
    make_classifier,
    single_model_catalog,
    validated_today,
)

if TYPE_CHECKING:
    from cyberkb.classify.llm import LLMClassifier
    from cyberkb.providers.http import HttpResponse
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
    """Category, format and language are closed enums; tags are filtered after the fact."""
    schema = response_schema(taxonomy)
    item = schema["properties"]["classifications"]["items"]
    assert item["properties"]["category"]["enum"] == list(taxonomy.category_ids)
    assert item["properties"]["format"]["enum"] == list(taxonomy.format_ids)
    assert item["properties"]["language"]["enum"] == list(taxonomy.language_ids)
    # Gemini rejects the schema with the 80+ tag ids as an enum (live-verified),
    # so the vocabulary lives in the system instruction instead.
    assert "enum" not in item["properties"]["tags"]["items"]
    assert all(tag in system_instruction(taxonomy) for tag in taxonomy.tag_ids)


def test_system_instruction_mentions_categories(taxonomy: Taxonomy) -> None:
    """The system instruction lists the real category ids."""
    text = system_instruction(taxonomy)
    assert "offensive-security" in text


def test_build_prompt() -> None:
    """The batch prompt echoes each document's ref and body."""
    prompt = build_prompt([("r1", "stem", "body text")])
    assert "r1" in prompt
    assert "body text" in prompt


# --- LLM classifier over the rotation engine (faked HTTP boundary) --------


def _classifier(taxonomy: Taxonomy, *responses: HttpResponse) -> LLMClassifier:
    """A classifier whose first model is already validated, answering ``responses``."""
    router = Router().add("google:list", default_google_listing())
    router.add("google:gemma-t-it", *responses)
    classifier, _ = make_classifier(
        router,
        taxonomy,
        catalog_doc=single_model_catalog(),
        validations=validated_today(),
        settings=RotationSettings(model_retries=0, list_passes=1),
    )
    return classifier


def test_llm_classifier_valid(taxonomy: Taxonomy) -> None:
    """A valid LLM response is used as the classification, with provenance."""
    classifier = _classifier(taxonomy, google_answer(answer(item("0", title="Nmap Guide"))))
    results = classifier.classify_batch([Document("0", "nmap", "body about nmap scanning")])
    assert results[0].category == "offensive-security"
    assert results[0].method == "llm"
    assert results[0].model == "gemma-t-it"
    assert results[0].provider == "google"
    assert results[0].tags == ("nmap",)
    assert results[0].title == "Nmap Guide"


def test_llm_classifier_empty_input(taxonomy: Taxonomy) -> None:
    """Classifying no documents returns no results and makes no call."""
    classifier = _classifier(taxonomy)
    assert classifier.classify_batch([]) == []


def test_llm_classifier_falls_back_on_missing_doc(taxonomy: Taxonomy) -> None:
    """A document the model omitted falls back to the heuristic."""
    classifier = _classifier(taxonomy, google_answer(answer(item("someone-else"))))
    body = "red team exploitation and metasploit payloads for penetration testing"
    results = classifier.classify_batch([Document("0", "pentest", body)])
    assert results[0].method == "heuristic"


def test_llm_classifier_ignores_non_list_answers(taxonomy: Taxonomy) -> None:
    """A malformed classifications value is an unusable answer for every document."""
    classifier = _classifier(taxonomy)
    assert classifier.problem(Document("0", "s", "b"), None) == "no classification for ref '0'"


@pytest.mark.parametrize(
    ("overrides", "reason"),
    [
        pytest.param({"category": "nonexistent"}, "unknown category", id="unknown-category"),
        pytest.param({"format": "bad"}, "unknown format", id="unknown-format"),
        pytest.param({"language": "xx"}, "unknown language", id="unknown-language"),
        pytest.param({"confidence": 0.1}, "below", id="below-confidence-floor"),
        pytest.param({"confidence": 1.5}, "outside", id="confidence-above-one"),
        pytest.param({"confidence": "x"}, "not a number", id="non-numeric-confidence"),
        pytest.param({"confidence": True}, "not a number", id="boolean-confidence"),
        pytest.param({"category": "uncategorized"}, "staging", id="staging-category"),
        pytest.param({"summary": "  "}, "empty summary", id="empty-summary"),
        pytest.param(
            {"summary": "I\u2019m sorry, but I can\u2019t do that."}, "refusal", id="refusal"
        ),
        pytest.param({"summary": "As an AI model I won't."}, "refusal", id="as-an-ai"),
    ],
)
def test_llm_classifier_rejects_invalid_item(
    taxonomy: Taxonomy, overrides: dict[str, Any], reason: str
) -> None:
    """Any invalid field makes the item unusable, with a precise reason."""
    classifier = _classifier(taxonomy, google_answer(answer(item("0", **overrides))))
    document = Document("0", "pentest", "red team exploitation metasploit penetration testing")
    problem = classifier.problem(document, item("0", **overrides))
    assert problem is not None
    assert reason in problem
    assert classifier.classify_batch([document])[0].method == "heuristic"


def test_llm_classifier_fallback_on_llm_error(taxonomy: Taxonomy) -> None:
    """When the service fails, the whole batch falls back to the heuristic."""
    classifier = _classifier(taxonomy, google_error(500, "INTERNAL", "err"))
    body = "red team exploitation metasploit penetration testing"
    results = classifier.classify_batch([Document("0", "pentest", body)])
    assert results[0].method == "heuristic"


def test_llm_classifier_missing_title_and_odd_tags(taxonomy: Taxonomy) -> None:
    """An empty title is inferred; unknown or non-list tags are dropped and capped."""
    many = ["nmap", "metasploit", "burp-suite", "wireshark", "osint", "phishing", "yara", "bogus"]
    classifier = _classifier(
        taxonomy,
        google_answer(answer(item("0", title="", tags=many))),
        google_answer(answer(item("1", tags="nmap"))),
    )
    first = classifier.classify_batch([Document("0", "my-pentest-notes", "# Real H1\n\nbody")])[0]
    assert first.title == "Real H1"
    assert len(first.tags) <= 6
    assert "bogus" not in first.tags
    second = classifier.classify_batch([Document("1", "notes", "body")])[0]
    assert second.tags == ()


def test_classify_one_reports_why_nothing_was_produced(taxonomy: Taxonomy) -> None:
    """A single-document request carries the engine's outcome when it fails."""
    classifier = _classifier(taxonomy, google_error(500, "INTERNAL", "err"))
    single = classifier.classify_one(Document("0", "s", "body"), deadline=None)
    assert single.result is None
    assert single.outcome.status == "exhausted"
