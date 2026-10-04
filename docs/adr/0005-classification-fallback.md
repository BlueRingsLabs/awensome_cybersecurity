# 5. Classification must degrade, never block

- Status: accepted
- Date: 2026-10-04

## Context

Classification quality is best with an LLM, but the model can be unavailable,
rate-limited, rotated out, or absent entirely (no API key, e.g. on a fork or in
local development). Google rotates model availability, so a single pinned model
id will eventually stop serving.

## Decision

Classification always produces a valid result. With a key, the LLM client tries
an ordered chain of models and, per document, falls back to a deterministic
offline heuristic whenever the model is unavailable or returns an invalid or
low-confidence answer. With no key, the heuristic runs directly. Weak evidence
routes a document to the staging category instead of guessing.

## Consequences

- A merge is never blocked by an external service outage.
- Forks and local runs work with zero configuration.
- The default model chain lists current Gemini Flash models newest-first and is
  overridable via `CYBERKB_MODELS`, so a retirement is a config change.
- Heuristic-only entries have empty summaries and lower confidence, which the
  catalog records honestly.
