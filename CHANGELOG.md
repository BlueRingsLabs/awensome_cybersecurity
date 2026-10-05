# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project aims to
follow [Semantic Versioning](https://semver.org/).

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
