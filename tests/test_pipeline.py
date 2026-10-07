"""Tests for assembling the classifier from the catalog and the environment."""

from __future__ import annotations

import io
from typing import TYPE_CHECKING

import pytest

from cyberkb.config import IngestConfig
from cyberkb.errors import ModelCatalogError, ProviderConfigError
from cyberkb.obslog import StructuredLogger
from cyberkb.pipeline import PROBE_DOCUMENT, build_classifier
from tests.llmfakes import (
    KEYS,
    FakeTime,
    answer,
    discovered_router,
    google_answer,
    groq_answer,
    item,
    write_catalog,
)

if TYPE_CHECKING:
    from cyberkb.paths import RepoPaths
    from cyberkb.taxonomy import Taxonomy


def test_build_classifier_discovers_and_resolves(repo: RepoPaths, taxonomy: Taxonomy) -> None:
    """The classifier is built from the catalog and the live listing; nothing is probed yet."""
    write_catalog(repo.root)
    router = discovered_router()
    time = FakeTime()
    classifier, catalog = build_classifier(
        repo,
        taxonomy,
        IngestConfig.from_env({}),
        logger=StructuredLogger(io.StringIO()),
        env=KEYS,
        transport=router,
        clock=time.clock,
        sleep=time.sleep,
        now=time.now,
    )
    assert [p.id for p in catalog.providers] == ["google", "groq"]
    statuses = [m["status"] for m in classifier.engine.model_report()]
    assert statuses == ["unvalidated", "unvalidated", "unvalidated"]
    assert router.pending() == {}
    probe = answer(item(PROBE_DOCUMENT.ref))
    router.add("google:gemma-t-it", google_answer(probe))
    router.add("google:gemini-test-flash", google_answer(probe))
    router.add("groq:groq-a", groq_answer(probe))
    classifier.engine.validate_all()
    assert {m["status"] for m in classifier.engine.model_report()} == {"active"}


def test_missing_keys_fail_before_any_request(repo: RepoPaths, taxonomy: Taxonomy) -> None:
    """Both keys are required; the error names the missing variables, never values."""
    write_catalog(repo.root)
    with pytest.raises(ProviderConfigError, match="GROQ_API_KEY"):
        build_classifier(
            repo,
            taxonomy,
            IngestConfig.from_env({}),
            logger=StructuredLogger(io.StringIO()),
            env={"GEMINI_API_KEY": "x" * 20, "GROQ_API_KEY": "  "},
        )


def test_invalid_catalog_is_a_catalog_error(repo: RepoPaths, taxonomy: Taxonomy) -> None:
    """Without a valid catalog nothing is built."""
    with pytest.raises(ModelCatalogError):
        build_classifier(
            repo,
            taxonomy,
            IngestConfig.from_env({}),
            logger=StructuredLogger(io.StringIO()),
            env=KEYS,
        )
