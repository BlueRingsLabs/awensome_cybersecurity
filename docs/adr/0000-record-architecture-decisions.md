# 0. Record architecture decisions

- Status: accepted
- Date: 2026-10-04

## Context

The repository was overhauled from a thin script-based indexer into a tested,
hardened engine with a faceted taxonomy. Decisions with long-lived consequences
should be written down where a future contributor (or auditor) can find the
reasoning, not just the result.

## Decision

Use lightweight Architecture Decision Records (ADRs), one Markdown file per
decision under `docs/adr/`, numbered sequentially. Each records context, the
decision, and its consequences. ADRs are immutable once accepted; a reversal is
a new ADR that supersedes the old one.

## Consequences

- The "why" behind the taxonomy, metadata model, dependency posture and
  classification fallback is discoverable and reviewable.
- Pull requests that change architecture are expected to add or update an ADR.
