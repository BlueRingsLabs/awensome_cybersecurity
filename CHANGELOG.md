# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project aims to
follow [Semantic Versioning](https://semver.org/).

## [3.0.0] - 2026-10-07

Google AI Studio + Groq with per-model rotation, pre-flight verification and
resumable, self-reporting enrichment (ADR-0008).

### Breaking

- **Providers are Google AI Studio and Groq only, and both keys are required.**
  `GEMINI_API_KEY` and `GROQ_API_KEY` must be set in the `awesome-cyber`
  environment; a missing key fails the workflow before any work starts, and a
  rejected key fails it at model discovery. The OpenRouter and Hugging Face
  providers are removed (their free tiers cannot carry the corpus: 50 RPD and
  ~US$0.10/month respectively; Pollinations, Mistral and Cerebras were
  evaluated and rejected for the same reason). `OPENROUTER_API_KEY`,
  `HF_TOKEN`, `LLM_PROVIDER_ORDER`, `CYBERKB_MODELS` and `CYBERKB_MAX_RETRIES`
  are no longer read.
- **The `enrich` workflow input is replaced by `mode`** (`ingest`, `enrich`,
  `preflight`).
- `cyberkb ingest` and `cyberkb classify` need both keys unless `--heuristic`
  is given. `cyberkb enrich` exits `5` (budget ended, work left) or `6` (no
  capacity) when incomplete, instead of `0`.
- Invalid `CYBERKB_*` values now fail the run instead of being clamped.

### Added

- **Reviewed model catalog** (`schema/llm-models.yaml`): fourteen models in
  priority order — Gemma 4 31B/26B, Gemini 3.1/3.5 Flash Lite, Gemini
  3.8/3.6/3.7/3.5/2.5 Flash, Gemini 2.5 Flash Lite, then Groq `allam-2-7b`,
  `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `qwen/qwen3.8-27b` — with the
  free-tier RPM/RPD/TPM(/TPD) limits verified on 2026-10-07. API ids are never
  assumed: each name is resolved against the live `/models` listing and the
  rule used is reported. Groq's safety classifiers are excluded.
- **Rotation engine** (`cyberkb.providers.rotation`):
  - highest-priority ready model first, with client-side RPM/TPM pacing and
    RPD/TPD accounting per quota day;
  - errors retried in place with jittered backoff; rate limits move on at once
    and the model rejoins after its cooldown; daily quotas retire the model;
    auth failures take the provider out;
  - bounded list passes;
  - each prompt fitted to the model's context and token window.
- **Pre-flight verification:** lazy per-model validation with a real
  classification probe and a structured-output mode ladder, cached for the
  quota day; `cyberkb preflight` and `mode: preflight` validate everything and
  report declared name → API id, verdict and mode.
- **Enrichment ledger** (`docs/audit/enrich-state.json`): per-resource
  status/provider/model/failure cause, per-model usage and validation verdicts,
  last run, and write-ahead recovery of interrupted category moves.
- **Run reports** at `docs/audit/ingest-runs/<date>-<run-id>.json` for every
  run: final status and reason, per-provider and per-model statistics, the
  ten-category failure breakdown, retries per model/provider/list, and
  per-resource outcomes.
- `--run-id` and `--summary` (Markdown job summary) on `ingest`, `enrich`,
  `preflight`.

### Changed

- The workflow enriches in 20-minute chunks inside a 5.5-hour budget and
  commits and pushes after every chunk (`.github/scripts/commit-progress.sh`
  refuses to commit a library failing `cyberkb check`, and rebases and retries
  if the branch moved). An incomplete enrichment ends the job red, after its
  progress is committed.
- Each upgraded resource is written atomically and the ledger saved before the
  next request.

### Fixed

- **Gemini rate limits were treated as exhausted billing.** Gemini's
  per-minute 429 says "exceeded your current quota"; it is now classified from
  `QuotaFailure.quotaId` (per-minute vs per-day) with `RetryInfo.retryDelay`
  as the cooldown, instead of tripping the provider.
- **Groq was unreachable from urllib.** Cloudflare refuses urllib's default
  `Python-urllib` User-Agent with `403 error code: 1010`; the transport now
  sends `cyberkb/<version>`, and an edge block is reported as a network
  failure, never as a rejected key.
- Gemini model discovery now follows `nextPageToken`; thought parts are never
  parsed as the answer.
- Every captured provider error is redacted against its API key before it is
  logged or written to a committed report.

## [2.2.1] - 2026-10-07

Resumable, budget-bounded enrichment.

### Fixed

- **Enrichment can now complete.** A full backfill makes one slow LLM call per
  resource (~485 of them), which runs for hours — far past the ingest job's
  30-minute timeout. Because the job committed only at the very end, every run
  was cancelled mid-pass and committed nothing. `cyberkb enrich` is now bounded
  and resumable: `--limit N` caps resources per run and `--max-seconds S` stops
  starting new work in time to finish and commit, with the remainder reported as
  `deferred`; already-enriched resources are skipped, so re-running walks the
  whole corpus while each run commits real progress.
- **No pre-flight on content-free runs.** `cyberkb ingest` now builds the LLM
  classifier (and its provider pre-flight) only when `inbox/` actually has
  submissions, so a catalog-only rebuild never spends the provider rate-limit
  budget.

### Changed

- The **Ingest and index** workflow gains `limit` and `max_seconds` dispatch
  inputs (passed to `enrich` injection-safely via the environment), and its job
  `timeout-minutes` is raised to a high backstop (350) now that `max_seconds` is
  the real governor of a run's length. The operations runbook documents the
  batch/resume procedure, per-provider rate limits and throughput guidance.

## [2.2.0] - 2026-10-05

Multi-provider, self-validating LLM classification.

### Added

- **Multi-provider LLM layer** (`cyberkb.providers`): one interface with three
  interchangeable, hand-rolled providers — Gemini, OpenRouter and Hugging Face —
  selected by configured key and `LLM_PROVIDER_ORDER`, behind an orchestrator
  with per-model rotation, retry-with-backoff, a per-provider circuit breaker
  and a guaranteed heuristic fallback. An extensible registry makes a fourth
  provider a drop-in. (ADR-0007)
- **Runtime model discovery and validation**: each provider discovers models
  from its own catalog and a pre-flight pass validates the best candidates
  against representative offensive/defensive/governance prompts, so no model is
  used on the assumption it works; free-tier models and rate limits are handled
  explicitly.
- **Structured error taxonomy and run reports**: every provider attempt is
  logged as categorised JSON (ten `FailureCategory` values, never a generic
  "failed"), and each run writes `docs/audit/ingest-runs/<date>.json` with
  per-provider success rates, failure breakdowns, provider health and model
  selection.
- **`classified_by` provenance** on every resource and catalog entry:
  `<provider>:<model>@<ISO-8601 UTC>` (or `heuristic@…`).
- **`cyberkb enrich`** command and workflow input: re-classify the
  heuristically-filed corpus through the providers and backfill the empty
  summaries, idempotently and within free-tier limits.

### Changed

- The classifier is driven by the orchestrator instead of a single Gemini
  client; the ingestion workflow reads `GEMINI_API_KEY`, `OPENROUTER_API_KEY`
  and `HF_TOKEN` from the `awesome-cyber` deployment environment and can enrich
  existing resources on a manual run.
- **CodeQL advanced workflow now covers both `python` and `actions`** (matrix,
  `security-extended`), so that disabling the repository's CodeQL *default
  setup* — the one maintainer action needed to resolve the advanced/default
  mutual-exclusivity conflict — leaves no language unscanned. (ADR-0006)

## [2.1.0] - 2026-10-05

Curation and test-integrity follow-up.

### Added

- **Reference-only entries** (`reference_only` front matter): all-rights-reserved
  works are kept as capped, source-linked pointers that credit their authors
  without redistributing the text; the policy check enforces the cap and a
  mandatory source link.
- **Author extraction** (`cyberkb.authors`): bylines and LinkedIn slugs populate
  the `authors` field on ingestion; the catalog now always carries an explicit
  author list (`["unknown"]` when none is declared).
- The five previously excluded copyrighted works are reinstated as reference
  entries (Microsoft 365 Security Checklist, The Complete Active Directory
  Security Handbook, OffSec sample report, CSA 2025 data-security-risk report,
  Joas A. Santos career guide).
- Per-module **test report** (`docs/audit/2026-10-05-test-report.md`).

### Changed

- **Test suite hardened to the same standard as `src/`**: the `tests.*` mypy
  override and the stylistic ruff ignores were removed; every test is fully
  type-annotated and documented. Only `S101` and `PLR2004` remain as
  per-file exceptions (structural to assertion-based testing). 345 cases,
  100 % line+branch coverage, all genuinely behavioural.
- The threat model documents the explicit criterion that quoted security
  payloads are a warning, never a reason to exclude a resource.
- **Secret scanning** now runs a version-pinned, checksum-verified gitleaks CLI
  instead of the Action (which requires a paid licence for organisation-owned
  repositories). A new [`.gitleaks.toml`](.gitleaks.toml) keeps the full default
  ruleset and scopes the scan to the project's own code, CI and configuration,
  allow-listing only the curated educational corpus (`library/`) and audit prose
  (`docs/audit/`) whose subject matter is example credentials. ADR-0006 is
  amended with this and with the CodeQL default-setup interaction.

### Removed

- `library/uncategorized/sobrevivendo-a-um-ataque-escolar.md` (out of scope:
  personal physical-safety guidance, not cybersecurity).

## [2.0.0] - 2026-10-04

A ground-up overhaul of the knowledge base and its tooling.

### Added

- **`cyberkb` engine** (`src/cyberkb/`): a typed, dependency-light Python package
  that ingests, classifies, catalogs and validates the library, with a CLI
  (`build`, `check`, `ingest`, `classify`).
- **Faceted taxonomy** (`schema/taxonomy.yaml`): 18 CyBOK- and NICE-aligned
  categories plus a staging area, a closed format and language set, and a
  controlled tag vocabulary — one source of truth for every component.
- **Front-matter metadata** on every resource (stable content id, category,
  format, language, licence, tags, summary, classification provenance), so the
  catalog is a pure function of the tree and metadata survives moves.
- **Licence detection and policy**: automatic SPDX detection with a
  `redistribution` class; the policy check blocks all-rights-reserved content and
  flags undetermined licences.
- **Deterministic catalogs** (`index.json` / `index.yaml`) with a published
  [JSON Schema](schema/catalog.schema.json) and self-describing taxonomy block.
- **Generated browse pages**: a README index and one `README.md` per category.
- **100%-covered test suite** (unit, property-based and end-to-end) and strict
  `ruff` + `mypy` gates.
- **Hardened CI/CD**: SHA-pinned actions, least-privilege tokens, CodeQL,
  zizmor, gitleaks, OpenSSF Scorecard, dependency review, Dependabot, and a
  pre-commit configuration.
- **Documentation**: architecture, catalog schema, threat model, Architecture
  Decision Records, operational runbooks, an audit report and this changelog.

### Changed

- **Layout**: the `0X_domain/subdomain/` tree became `library/<category>/`.
- **Classification**: the Gemini call now uses a schema-constrained, model-
  fallback client with a deterministic offline heuristic as a guaranteed
  fallback; it no longer blocks a merge when the service is unavailable.
- **Ingestion input**: raw submissions now land in `inbox/` rather than the
  repository root, keeping the root clean.
- Repository name corrected from `awensome_cybersecurity` to
  `awesome_cybersecurity` throughout.

### Removed

- The v1 scripts (`.github/scripts/build_index.py`,
  `classify_and_index.py`) and the hidden `.ingest_metadata.json` sidecar;
  metadata now lives in each document's front matter.
- 19 legacy files were not migrated — 10 empty/image-only conversions, 4
  content duplicates, and 5 all-rights-reserved works that may not be
  redistributed. Each is recorded in
  [`docs/audit/2026-10-04-migration.md`](docs/audit/2026-10-04-migration.md).

### Fixed

- Code-fence-aware title and heading extraction (shell comments inside code
  blocks are no longer mistaken for document titles).
- URL tracking-parameter stripping no longer corrupts meaningful query strings.
- Language detection no longer conflates Spanish and Portuguese.
