# Architecture

`cyberkb` turns raw Markdown contributions into a curated, faceted, machine-
readable library. It is a small set of pure-ish modules with a thin CLI; the
only I/O is reading the repository tree and writing generated artefacts.

## Data flow

```text
inbox/*.md ─┐
            │  ingest
            ▼
   sanitize ──► classify ──► licence-detect ──► mint id ──► write
   (fence-aware) (LLM or       (SPDX +           (stable,    library/<category>/<slug>.md
                 heuristic)     redistribution)   content-    with YAML front matter
                                                  derived)
                                                               │
                                                               │ build (pure function of the tree)
                                                               ▼
                                 index.json · index.yaml · README index · category pages
                                                               │
                                                               │ check (CI gate)
                                                               ▼
                                     valid front matter · folder==category · unique ids/bodies ·
                                     no restricted licences · no drift
```

## Modules

| Module | Responsibility |
| --- | --- |
| `taxonomy` | Load and validate `schema/taxonomy.yaml` into a typed model; the one source of truth. |
| `textutil` | Pure text primitives: Unicode/control/bidi stripping, tokenising, slugs. |
| `markdown` | Fence-aware heading/title extraction and active-content detection. |
| `sanitize` | Normalise raw Markdown (page markers, tracking params, whitespace), idempotent. |
| `language` | Stop-word language identification (en/es/pt/und). |
| `licensing` | Evidence-based SPDX detection and the `redistribution` classification. |
| `frontmatter` | Parse, validate and render the per-document metadata block. |
| `ids` | Stable content-derived resource ids (`ckb-…`) with collision avoidance. |
| `fsutil` | Hostile-input-safe reads (symlink/size/binary guards) and atomic writes. |
| `yamlsafe` | YAML loading that refuses object construction *and* aliases. |
| `classify/` | `heuristic` (offline, deterministic) and `llm` (multi-provider, schema-constrained) engines sharing one result type. |
| `providers/` | Interchangeable LLM providers (Gemini, OpenRouter, Hugging Face) behind one interface, plus discovery/validation, a circuit breaker and the orchestrator (ADR-0007). |
| `obslog` | Structured JSON attempt logging and the end-of-run report. |
| `pipeline` | Assemble the provider orchestrator and classifier from configuration. |
| `provenance` | Build the `classified_by` stamp. |
| `library` | Load and validate the on-disk library; detect duplicate ids/bodies. |
| `catalog` | Build the deterministic catalog and serialise it (JSON/YAML). |
| `render` | README index block and per-category pages (escaped, injection-safe). |
| `build` | Regenerate every derived artefact, idempotently. |
| `checks` | The repository policy gate used by CI. |
| `ingest` | Orchestrate discovery → classify → file for `inbox/`. |
| `enrich` | Backfill summaries/classification on existing resources via the LLM. |
| `cli` | `cyberkb build|check|ingest|enrich|classify` with stable exit codes. |

## Design principles

- **One source of truth.** The taxonomy defines categories, formats, languages
  and tags; the classifier's response schema, the catalog, the JSON Schema and
  the generated pages all derive from it (ADR-0002).
- **Metadata lives with the document.** Front matter, not a sidecar or the
  previous catalog, so the catalog is reproducible and metadata survives
  renames (ADR-0003).
- **Deterministic and idempotent.** Same inputs → byte-identical outputs; a
  rebuild of an unchanged tree produces no diff. The only volatile field is the
  build timestamp, which the build and check both neutralise.
- **Degrade, never block.** No API key → heuristic classification; model
  unavailable → retries then fallback; a malformed document → recorded as a
  problem, not a crash (ADR-0005).
- **Hostile input by default.** Contributor content is untrusted: symlinks,
  oversized blobs, binary data, bidi/control characters, YAML aliases and
  path traversal are all refused (ADR-0001, `docs/threat-model.md`).
- **Minimal runtime surface.** PyYAML is the only runtime dependency; every LLM
  provider is hand-rolled on the standard library (ADR-0004).

## Classification

A document is classified by one of two interchangeable engines:

- **Heuristic** — weighted keyword n-grams over title, filename, headings and
  body, with logarithmic damping and a confidence from the margin between the
  top two categories. Fully offline, deterministic and explainable; weak
  evidence routes to the staging category rather than guessing.
- **LLM** — the multi-provider orchestrator, with a response schema built from
  the live taxonomy so a hallucinated label is impossible by construction. Each
  result is validated; anything invalid or low-confidence falls back to the
  heuristic for that one document, so a batch can never emit an invalid
  classification or drop a file.

## The multi-provider LLM layer

`providers/` presents one interface (`LLMProvider`) with three interchangeable
implementations — Gemini, OpenRouter and Hugging Face — selected by configured
key and `LLM_PROVIDER_ORDER`. Before a run, each provider *discovers* models
from its own catalog and *validates* the best candidates against representative
cybersecurity prompts, so no model is used on the assumption it works. During a
run the orchestrator rotates models and providers on failure, retries transient
errors with jittered backoff, trips a circuit breaker on provider-fatal errors,
and finally falls back to the heuristic — logging every attempt as structured
JSON and writing a per-run audit report. Each resource records which provider
and model classified it (`classified_by`). The full rationale, ranking and
failure taxonomy are in ADR-0007.

## Why hand-rolled provider clients

The ingestion job runs in CI with repository write access and live API keys, so
every third-party dependency is attack surface. Each provider is one HTTPS call
to a documented JSON endpoint and needs only the standard library; an injectable
transport makes every branch (retryable errors, rotation, truncation, blocked
responses, malformed JSON) testable without a network. See ADR-0004 and
ADR-0007.
