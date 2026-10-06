# Repository audit and SOTA remediation — 2026-10-04

Author: Gonzalo Romero (@glromero)

This report records the audit of `awesome_cybersecurity` as it stood after its
initial build-out, and the remediation that followed. It covers two layers the
brief asked for: the **objectives/idea** of the project, and the
**implementation**. Companion documents: the
[migration and exclusions record](2026-10-04-migration.md), the
[threat model](../threat-model.md), the [architecture](../architecture.md) and
the [ADRs](../adr/).

## 1. Scope and method

- Full read of the repository: the two Python scripts, the workflow, the
  community docs, the catalogs, and all 505 content files.
- Static review of the pipeline for correctness, security and supply-chain
  exposure; profiling of the corpus for titles, languages, licences, duplicates
  and empty/broken ingestions.
- Research into current Gemini model availability and current GitHub Actions
  releases to avoid pinning to retired versions.

## 2. Audit of the objectives

The original idea — a frictionless, automatically indexed community library,
human-readable on GitHub and machine-parsable via catalogs — is sound and worth
keeping. The objectives were nonetheless raised in three ways:

1. **From a folksonomy to a grounded taxonomy.** The original two axes conflated
   resource *type* with *depth* and forced a single offensive/defensive label
   onto cross-cutting material. Replaced with one primary **category** plus
   orthogonal **format/language/tag** facets, grounded in **CyBOK** and the
   **NICE** framework (ADR-0002). This is what makes the library legible to a
   Tier-1 team and an auditor, not just browsable.
2. **From "indexed" to "trustworthy".** "Best-organised" is not enough for a
   library that *republishes third-party work*. Added first-class **licence
   detection, a redistribution policy, and a content-provenance trail** so the
   collection is legally defensible, not just tidy.
3. **From a script to an engine.** "Fully automated" was asserted but untested
   and unhardened. Re-grounded on a typed, 100%-covered engine with a CI policy
   gate, so automation is *provable*, not aspirational.

## 3. Findings (as audited) and remediation

Severity: **High** = correctness/security/legal risk; **Medium** = reliability or
maintainability; **Low** = hygiene.

| # | Sev | Finding (v1) | Remediation |
| --- | --- | --- | --- |
| 1 | High | `yaml` alias expansion and unbounded front matter were possible; no guard against "billion laughs". | `yamlsafe` forbids object construction **and** anchors/aliases; front-matter size capped. (ADR-0001) |
| 2 | High | File reads followed symlinks and had no size/binary guard; model-provided filenames were path-joined. | `fsutil.read_text` uses `O_NOFOLLOW`, rejects non-regular/oversized/binary files; `ensure_within` blocks traversal; ids/slugs are engine-derived. |
| 3 | High | No licence awareness: all-rights-reserved books were redistributed in an MIT repo. | Licence detection + `redistribution` class; `cyberkb check` blocks `restricted`; 5 such works excluded and recorded; `NOTICE` documents content vs. code licensing. |
| 4 | High | Workflow used floating action tags and a default `contents: write` token. | All actions SHA-pinned; default `contents: read`; write scoped to the ingestion job; CodeQL/zizmor/gitleaks/Scorecard/dependency-review added. (ADR-0006) |
| 5 | High | Zero tests; no type checking; correctness unverifiable. | 314 tests at **100% line and branch coverage**; strict `mypy`; `ruff` with broad rule set. |
| 6 | Medium | Titles were taken from any `#` line, so shell comments inside code blocks became catalog titles. | Fence-aware `markdown` parsing for titles, headings and active-content detection. |
| 7 | Medium | Catalog depended on a hidden sidecar and its own previous output; metadata broke on rename. | Metadata moved into per-document front matter; catalog is a pure function of the tree; stable content-derived ids. (ADR-0003) |
| 8 | Medium | Pinned to `gemini-2.5-flash`, which Google is retiring; outage blocked the merge path. | Model-chain client with retries/backoff and a guaranteed offline heuristic fallback; `CYBERKB_MODELS` override. (ADR-0004, ADR-0005) |
| 9 | Medium | URL "tracking" stripping removed meaningful params (`ref=`) and left dangling separators. | Precise tracking-param stripping that preserves meaningful query strings; idempotent sanitiser. |
| 10 | Medium | Language detection mapped `_es` to Portuguese and conflated ES/PT. | Stop-word language profiles with distinctive-word sets and a confidence floor. |
| 11 | Medium | Large runtime dependency (`google-genai`) ran next to the CI token/secret. | Runtime deps reduced to PyYAML; hand-rolled stdlib Gemini client. (ADR-0004) |
| 12 | Low | 10 empty/image-only files and 4 duplicates sat in the catalog as noise. | Excluded with recorded causes; dedup by content signature; empties rejected by policy. |
| 13 | Low | Repository name misspelled (`awensome_cybersecurity`) throughout. | Corrected across code, catalog and docs. |
| 14 | Low | Committed `__pycache__`; no `.gitignore`/`.gitattributes`/`.editorconfig`. | Added; generated artefacts marked; LF normalised. |

## 4. What was built

- **`cyberkb` engine** (~4,000 LOC) across 20 focused modules with a CLI
  (`build`, `check`, `ingest`, `classify`) and stable exit codes.
- **Taxonomy** of 18 CyBOK/NICE-aligned categories + staging, closed
  format/language sets and a controlled tag vocabulary — one source of truth.
- **Catalogs** (`index.json`/`index.yaml`) with a published JSON Schema and a
  self-describing taxonomy block; **generated** README index and per-category
  pages.
- **Test suite**: 314 tests (unit, property-based with Hypothesis, end-to-end
  CLI) at 100% branch coverage (~2,300 LOC).
- **CI/CD**: `ci` (lint, format, types, tests, actionlint, policy), `ingest`,
  `codeql`, `security` (zizmor, gitleaks, dependency review), `scorecard`;
  Dependabot; pre-commit; issue/PR templates; `SECURITY.md`; `CODEOWNERS`.
- **Docs**: architecture, catalog schema, threat model, 7 ADRs, 2 runbooks,
  `NOTICE`, `CHANGELOG`, and this audit + the migration record.

## 5. Content migration result

505 legacy files → **486 filed**, **19 excluded** (10 empty/broken, 4 duplicates,
5 all-rights-reserved). One resource remains in staging for a human topic
decision. Full detail and the per-file causes are in
[`2026-10-04-migration.md`](2026-10-04-migration.md).

## 6. Verification status

At the close of this work, on the development branch:

- `ruff check` / `ruff format --check`: clean.
- `mypy` (strict): clean.
- `pytest`: 314 passed, **100%** line + branch coverage.
- `actionlint`: clean. `zizmor` (offline): no findings.
- `cyberkb check`: **0 errors** across 486 resources (advisory warnings only:
  undetermined licences and quoted payloads, both expected and documented).

## 7. Honest limitations and residual items

These do not block the gate but are recorded for transparency:

- **Classification is heuristic-sourced for the migration.** No `GEMINI_API_KEY`
  was available in the build environment, so the 486 resources were classified by
  the deterministic offline engine. It is good and reproducible, but an LLM pass
  (just set the secret and re-run `cyberkb ingest` on re-staged content, or a
  one-off reclassification) would add summaries and refine edge cases. ~458
  resources have `summary: ""` for this reason.
- **458 resources are `NOASSERTION`.** Many are short original community posts
  that are fine to include; each should still have its licence confirmed before
  commercial reuse (content-licensing runbook).
- **Authorship is not populated.** Much of the corpus is by a few known authors;
  `authors` was left empty rather than guessed. A pass could populate it.
- **Online supply-chain audits** (zizmor's GitHub API checks, Scorecard) run in
  CI, not in this offline environment; they are configured and SHA-pinned.
