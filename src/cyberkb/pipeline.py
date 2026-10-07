"""Assemble the LLM classifier from the reviewed catalog and the environment.

This is the one place that turns configuration into a ready classifier: load
``schema/llm-models.yaml``, build one adapter per declared provider (every key
is required — a missing one stops the run before any request), create the
rotation engine with any usage and validation verdicts carried over from
earlier runs today, and discover the live models. Validation itself is lazy:
each model is probed with :data:`PROBE_DOCUMENT` the first time the engine
wants to use it (or all at once by ``cyberkb preflight``).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cyberkb.classify.base import Document
from cyberkb.classify.llm import LLMClassifier
from cyberkb.providers.catalog import load_model_catalog
from cyberkb.providers.registry import build_providers
from cyberkb.providers.rotation import RotationEngine

if TYPE_CHECKING:
    from collections.abc import Mapping

    from cyberkb.config import IngestConfig
    from cyberkb.obslog import StructuredLogger
    from cyberkb.paths import RepoPaths
    from cyberkb.providers.catalog import ModelCatalog
    from cyberkb.providers.governor import DailyUsage
    from cyberkb.providers.http import Transport
    from cyberkb.providers.rotation import CachedValidation
    from cyberkb.taxonomy import Taxonomy

__all__ = ["PROBE_DOCUMENT", "build_classifier"]

# A short, unambiguous cybersecurity document: a model is accepted only if it
# returns a schema-valid, on-taxonomy classification with a real summary.
PROBE_DOCUMENT = Document(
    ref="probe-nmap",
    stem="nmap-reconnaissance",
    body=(
        "# Nmap reconnaissance\n\nUsing nmap for host discovery, TCP/UDP port "
        "scanning and service and version detection during an authorized "
        "penetration test, then reporting the exposed attack surface."
    ),
)


def build_classifier(  # noqa: PLR0913 - every collaborator explicit and injectable
    paths: RepoPaths,
    taxonomy: Taxonomy,
    config: IngestConfig,
    *,
    logger: StructuredLogger,
    env: Mapping[str, str] | None = None,
    usage: Mapping[str, DailyUsage] | None = None,
    validations: Mapping[str, CachedValidation] | None = None,
    transport: Transport | None = None,
) -> tuple[LLMClassifier, ModelCatalog]:
    """Build the engine-backed classifier and discover the live models.

    Raises:
        ModelCatalogError: the catalog is invalid or contradicts an adapter.
        ProviderConfigError: a key is missing, or a provider rejected its key.
    """
    catalog = load_model_catalog(paths.root)
    providers = build_providers(catalog, env, timeout=config.timeout, transport=transport)
    engine = RotationEngine(
        providers,
        catalog,
        settings=config.rotation,
        logger=logger,
        usage=usage,
        validations=validations,
    )
    classifier = LLMClassifier(engine, taxonomy)
    engine.discover(classifier.request([PROBE_DOCUMENT], single=True))
    return classifier, catalog
