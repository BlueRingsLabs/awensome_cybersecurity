# 4. Minimal runtime dependencies; hand-rolled Gemini client

- Status: accepted
- Date: 2026-10-04

## Context

The ingestion job runs in CI with `contents: write` and `GEMINI_API_KEY`. v1
depended on the `google-genai` SDK (and its transitive tree) at runtime. Every
such dependency is code that runs next to our token and secret.

## Decision

Keep the runtime dependency set to PyYAML alone. Talk to Gemini with a small
client built on the standard library (`urllib`) against the documented
`generateContent` JSON endpoint, with an injectable transport.

## Consequences

- Drastically smaller supply-chain attack surface for the privileged job.
- Every client branch — retries, backoff, model fallback, truncation, blocked
  responses, malformed JSON — is unit-tested without a network or a key.
- We own the request/response shape; a Gemini API change is a local edit.
- Trade-off: we maintain a little HTTP code instead of delegating to an SDK.
