"""Assemble the multi-provider classifier from runtime configuration.

This is the one place that turns an :class:`~cyberkb.config.IngestConfig` into a
ready orchestrator: it builds each configured provider in order, runs the
pre-flight discovery + validation pass (so only models proven to return usable
cybersecurity classifications are used), and wraps the result in an
:class:`~cyberkb.classify.llm.LLMClassifier`. With no provider keys it returns
``(None, None)`` and the caller classifies with the heuristic.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cyberkb.classify.llm import LLMClassifier
from cyberkb.classify.schema import build_prompt, response_schema, system_instruction
from cyberkb.providers.orchestrator import Orchestrator, OrchestratorSettings
from cyberkb.providers.registry import PROVIDER_CLASSES

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from typing import Any

    from cyberkb.config import IngestConfig
    from cyberkb.obslog import StructuredLogger
    from cyberkb.taxonomy import Taxonomy

__all__ = ["VALIDATION_DOCS", "build_classifier", "build_orchestrator"]

# Representative cybersecurity documents used to validate candidate models:
# offensive, defensive/IR and governance/hardening, so a model is only accepted
# if it classifies across the breadth of the corpus, not one narrow slice.
VALIDATION_DOCS: tuple[tuple[str, str, str], ...] = (
    (
        "probe-offensive",
        "nmap-recon",
        (
            "# Nmap reconnaissance\n\nUsing nmap for host discovery, port scanning and "
            "service and version detection during an authorized penetration test."
        ),
    ),
    (
        "probe-defensive",
        "phishing-ir",
        (
            "# Responding to a phishing incident\n\nTriage, containment, eradication and "
            "recovery for a credential-phishing incident, with indicators of compromise."
        ),
    ),
    (
        "probe-governance",
        "tls-hardening",
        (
            "# Hardening TLS\n\nChoosing cipher suites, disabling legacy protocols and "
            "enabling HSTS to harden a web server's TLS configuration."
        ),
    ),
)


def _validator(taxonomy: Taxonomy) -> Callable[[Mapping[str, Any]], bool]:
    """A predicate that accepts a batch answer only if it is usable and on-taxonomy."""

    def validate(payload: Mapping[str, Any]) -> bool:
        items = payload.get("classifications")
        if not isinstance(items, list) or not items or not isinstance(items[0], dict):
            return False
        category = items[0].get("category")
        return (
            isinstance(category, str)
            and category in taxonomy.category_ids
            and not taxonomy.category(category).staging
            and bool(str(items[0].get("summary", "")).strip())
        )

    return validate


def build_orchestrator(
    config: IngestConfig,
    *,
    logger: StructuredLogger | None = None,
) -> Orchestrator:
    """Construct an orchestrator over the configured providers, in fallback order."""
    providers = [
        PROVIDER_CLASSES[name](key, timeout=config.timeout)
        for name, key in config.active_providers()
    ]
    settings = OrchestratorSettings(max_retries=config.max_retries)
    return Orchestrator(providers, logger=logger, settings=settings)


def build_classifier(
    taxonomy: Taxonomy,
    config: IngestConfig,
    *,
    logger: StructuredLogger | None = None,
) -> tuple[LLMClassifier | None, Orchestrator | None]:
    """Build the orchestrator, run pre-flight, and return the classifier if usable.

    Returns ``(None, None)`` when no provider is configured; ``(None,
    orchestrator)`` when providers are configured but none validated a model
    (so the caller uses the heuristic yet can still write the run report).
    """
    if not config.active_providers():
        return None, None
    orchestrator = build_orchestrator(config, logger=logger)
    orchestrator.preflight(
        system=system_instruction(taxonomy),
        schema=response_schema(taxonomy),
        samples=[build_prompt([doc]) for doc in VALIDATION_DOCS],
        validate=_validator(taxonomy),
    )
    classifier = LLMClassifier(orchestrator, taxonomy) if orchestrator.has_capacity() else None
    return classifier, orchestrator
