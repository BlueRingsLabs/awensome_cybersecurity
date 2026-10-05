# Test suite report — 2026-10-05

Author: Gonzalo Romero (@glromero)

This report audits the `cyberkb` test suite: what each module tests, which edge
cases are covered, what is deliberately **not** covered, and why the 100 %
line-and-branch coverage is meaningful rather than cosmetic.

## Headline

- **265 test functions → 345 executed cases** (parametrisation expands them).
- **100 % line and branch coverage**, enforced as a hard gate
  (`--cov-fail-under=100 --cov-branch`).
- Tests are **fully type-checked** under the same strict `mypy` as `src/`, and
  linted under the same `ruff` ruleset. The only two per-file exceptions are
  `S101` (pytest *is* assertions) and `PLR2004` (expected values in assertions
  are literals) — both structural to assertion-based testing, not relaxations to
  get green. The earlier `tests.*` mypy override and the stylistic ruff ignores
  were removed.
- **No mocks stand in for the code under test.** The only test doubles are at
  the true process boundary — the HTTP transport to the Gemini API — which
  cannot be called from a unit test. Everything our code actually does
  (validation, fallback, parsing, routing) runs for real against those doubles.

## Coverage philosophy (why 100 % here is real)

Coverage is necessary, not sufficient, so the suite is written to exercise
*behaviour and branches*, not just lines:

- **Property-based tests** (Hypothesis) assert invariants over random input for
  the text primitives and the sanitiser — e.g. "a slug is always non-empty,
  bounded and well-formed for any string and any length", "sanitising is
  idempotent for any input". These found two real bugs during development
  (the `slugify` length-cap fallback and the ES/PT language conflation).
- **Adversarial/hostile-input tests** drive the security controls with the
  attacks they claim to stop (symlinks, traversal, oversized/binary files,
  bidi/control characters, YAML aliases, path-escaping).
- **End-to-end tests** run the real CLI (`build`, `check`, `ingest`,
  `classify`) against a temporary repository and assert on exit codes and
  generated files.
- **Branch coverage** is on, so every `if`/`except`/fallback edge is taken by a
  test, not just every line.

## Per-module map

| Source module | Test module | Cases | What is tested | Notable edge cases |
| --- | --- | ---: | --- | --- |
| `textutil` | `test_textutil` | 17 | tokenising, folding, slugify, truncate, plain-text reduction, n-grams, word count | bidi/BOM/control stripping; slug length-cap on word boundary and hard cut; **property**: slug always valid, strip idempotent |
| `markdown` | `test_markdown_sanitize` | 32 | fence-aware headings/H1/first-line; active-content detection; escaping; sanitiser | tilde vs backtick fences; longer/shorter closing fences; setext headings; payload inside fence/inline-code ignored; **property**: sanitise idempotent, ends cleanly |
| `sanitize` | `test_markdown_sanitize` | (above) | page-marker removal, blank-run collapse, CRLF, tracking-param stripping | blank lines preserved inside fences; `ref=` kept, `utm_*`/`fbclid` dropped; invalid URL left intact |
| `taxonomy` | `test_taxonomy_yaml` | 17 | parsing/validation of the taxonomy model; category lookup | 14 distinct malformed documents rejected; two-staging, missing-keywords, bad codes, duplicate ids |
| `yamlsafe` | `test_taxonomy_yaml` | (above) | safe load; alias/anchor rejection | anchor without alias still rejected; `YAMLAliasError` is a `yaml.YAMLError` |
| `frontmatter` | `test_frontmatter` | 27 | parse/validate/render/round-trip; contributor hints; `reference_only` | 21 field-level defects; multiple problems reported together; empty/`...`/oversized/non-mapping blocks |
| `ids` | `test_ids_language_licensing` | 13 (shared) | stable content id; collision salting; signature | reorder-invariance; different content differs; taken-set avoidance |
| `language` | `test_ids_language_licensing` | (shared) | en/es/pt/und detection | confidence floor → `und`; ES vs PT separation |
| `licensing` | `test_ids_language_licensing` | (shared) | SPDX detection + redistribution class | grant beats "all rights reserved"; bare CC needs grant context; CC-BY-ND text form; OGL default version |
| `authors` | `test_authors` | 19 | byline + LinkedIn-slug extraction, canonicalisation | all-caps title-casing; hyphen-linebreak heal; digit/generic/single-word rejection; fence & scan-window skips; dedupe of collapsed names |
| `fsutil` | `test_fsutil` | 15 | guarded reads; atomic writes | symlink (file and intermediate dir), traversal, oversize, binary, directory; write skip-unchanged; cleanup on fsync failure |
| `llm` | `test_llm` | 21 | Gemini client retries/backoff/fallback/parsing | retryable vs fatal vs model status; Retry-After honoured/ignored; blocked response; truncated finish; non-object payload; urllib success/HTTPError/URLError |
| `classify.heuristic` | `test_classify` | 20 (shared) | scoring, title/format/tag inference, staging | all-zero scores; generic-H1 skip; format rules + book-by-length; staging on weak evidence |
| `classify.llm` + `classify.schema` | `test_classify` | (shared) | schema from taxonomy; per-item validation + heuristic fallback | 6 invalid-item shapes each fall back; empty batch; missing-title inference; whole-batch fallback on error |
| `catalog` + `render` | `test_catalog_render` | 14 | catalog build/serialise; README/category rendering | optional fields; default timestamp; pipe-in-title neutralised; corrupt/missing README markers; empty-facet page |
| `catalog` (schema) | `test_catalog_schema` | 6 | generated catalog validates against the JSON Schema | empty, populated, reference-only, unknown-authors, real-taxonomy catalogs |
| `library` + `build` + `checks` | `test_library_build_checks` | 28 | load/validate; build idempotency; policy gate | stray file, unknown category, category mismatch, duplicate id/body; restricted vs reference-stub (too-long, no-source); NOASSERTION & active-content as warnings; drift of catalogs/README/category pages |
| `ingest` | `test_ingest` | 14 | end-to-end filing from `inbox/` | reject empty/binary/bad-FM; contributor hints win; licence + author extraction; filename-collision and id-collision; staging; LLM path |
| `config` + `__main__` | `test_config_main` | 6 | env parsing; module entry point | invalid/out-of-range ints; blank model list; `python -m cyberkb` |
| `cli` | `test_cli` | 17 | every subcommand and exit code | version/usage; build/check/ingest/classify happy and failure paths; `--heuristic`; LLM-path via faked transport; config-error mapping |

## What is deliberately NOT covered (honest limitations)

- **The real Gemini network call.** `llm.UrllibTransport` is driven through a
  faked `urllib.request.urlopen` (success, `HTTPError`, `URLError`); the live
  endpoint is never contacted in tests. The client *logic* around it is fully
  covered. A live smoke test would require an API key and network and belongs
  in a manual/integration run, not the unit gate.
- **Real wall-clock timing / backoff sleep durations.** `sleep` and `jitter`
  are injected, so retry/backoff *control flow* is tested but real delays are
  not awaited (by design — fast, deterministic tests).
- **Concurrency.** The pipeline is single-process and the one concurrency
  concern (two ingestion runs racing the catalog) is handled at the CI level by
  the `ingest` workflow's `concurrency` group, not in code, so there is no
  in-process locking to unit-test. Atomic, rename-based writes
  (`fsutil.atomic_write_text`) are tested for the crash-safety property instead.
- **Windows path semantics.** Symlink tests are `skipif`-guarded off Windows;
  the project targets POSIX CI runners.
- **Classification *accuracy*** (as opposed to mechanics) is not asserted on the
  full corpus — accuracy is a quality metric, not a correctness invariant. The
  heuristic's decisions are validated on representative documents and the whole
  corpus was reviewed during migration (see the migration audit).

## How to reproduce

```bash
uv sync
uv run pytest                 # 345 cases, 100% line+branch coverage gate
uv run ruff check . && uv run ruff format --check .
uv run mypy                   # strict, src and tests
```
