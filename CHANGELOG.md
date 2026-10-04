# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project aims to
follow [Semantic Versioning](https://semver.org/).

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
