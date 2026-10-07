# Test suite report

Author: Gonzalo Romero (@glromero)

This report audits the `cyberkb` test suite: what each area tests, what is
deliberately **not** covered, the result of a critical self-audit, and why the
100 % line-and-branch coverage is meaningful rather than cosmetic. It covers the
multi-provider LLM layer added in 2.2.0 and supersedes the 2.1.0 edition.

## Headline

- **479 executed cases across 26 test modules.**
- **100 % line and branch coverage**, enforced as a hard gate
  (`--cov-fail-under=100 --cov-branch`).
- Tests are **fully type-checked** under the same strict `mypy` as `src/`, and
  linted under the same `ruff` ruleset. The only two per-file exceptions are
  `S101` (pytest *is* assertions) and `PLR2004` (expected values in assertions
  are literals) — both structural to assertion-based testing, not relaxations to
  get green.
- **The only test doubles are at true external boundaries.** The HTTP transport
  to every LLM provider (`providers/http.py` / `urllib.urlopen`), `os.fsync`
  (crash-safety), and `sys.argv` (the module entry point). No `cyberkb` logic —
  validation, discovery, selection, rotation, parsing, catalog building, policy
  checks — is ever mocked; it all runs for real against those boundaries.

## Coverage philosophy (why 100 % here is real)

Coverage is necessary, not sufficient, so the suite exercises *behaviour and
branches*, not just lines:

- **Property-based tests** (Hypothesis) assert invariants over random input for
  the text primitives and the sanitiser. These found two real bugs during
  development (the `slugify` length-cap fallback and the ES/PT language
  conflation).
- **Adversarial/hostile-input tests** drive the security controls with the
  attacks they claim to stop (symlinks, traversal, oversized/binary files,
  bidi/control characters, YAML aliases, path-escaping).
- **Provider tests run the real provider stack** (request building, status →
  category mapping, discovery filtering/ranking, JSON-mode parsing, model
  validation, rotation, retry, circuit breaking) against a fake HTTP transport
  that only returns bytes — so the logic under test is genuinely executed.
- **End-to-end tests** run the real CLI (`build`, `check`, `ingest`, `enrich`,
  `classify`) against a temporary repository and assert on exit codes, generated
  files and the run report.

## Per-area map

| Area | Test module(s) | What is tested |
| --- | --- | --- |
| text / markdown / sanitize | `test_textutil`, `test_markdown_sanitize` | tokenising, slugify, truncation, fence-aware headings, active-content detection, idempotent sanitising; **property**: slug always valid, sanitise idempotent |
| taxonomy / yamlsafe | `test_taxonomy_yaml` | model parsing/validation; alias/anchor rejection; 14 malformed documents |
| front matter | `test_frontmatter` | parse/validate/render/round-trip; `reference_only`; `classified_by` (valid, heuristic-stamp, bad-format, over-long, absent) |
| ids / language / licensing | `test_ids_language_licensing` | stable ids & collision salting; en/es/pt/und; SPDX + redistribution class |
| authors | `test_authors` | byline + LinkedIn-slug extraction, canonicalisation, rejections |
| fsutil | `test_fsutil` | guarded reads; atomic writes; cleanup on fsync failure |
| errors / provenance | `test_errors`, `test_provenance` | the ten `FailureCategory` values; `ProviderError` context & message; `classified_by` stamp (llm/heuristic/manual/indeterminate) |
| obslog | `test_obslog` | attempt serialisation; one JSON line per attempt; run-report aggregation & file write |
| providers: transport | `test_providers_http` | urllib success / HTTPError / URLError(timeout vs not) / bare timeout / OSError |
| providers: base | `test_providers_base` | status→category table (12 cases); Retry-After parsing; health check ok/fail; `_send`/`_get_mapping`/`_decode_object` guards |
| providers: Gemini | `test_provider_gemini` | discovery ranking & filtering; schema-constrained call; content-filter / truncation / missing-parts / bad-JSON paths |
| providers: OpenRouter/HF | `test_providers_openai_compat` | free-model filtering, family ranking, router fallback; HF size filter & model-status availability; JSON-mode parsing, fence stripping, content-filter; registry |
| providers: circuit | `test_providers_circuit` | closed → open → half-open → closed; trip; success reset; half-open re-open |
| providers: selection | `test_providers_selection` | discovery failure; accept a validated model; reject on call failure / poor output / unavailability; multi-sample; logging; serialisation |
| providers: orchestrator | `test_providers_orchestrator` | success; transient retry then success; exhaust → rotate model; model-unavailable rotate; provider-fatal → trip & fall over; breaker persists across calls; all-fail → None + heuristic count; preflight + run report |
| pipeline | `test_pipeline` | validator accept/reject branches; no-provider; provider order; validated vs no-capacity |
| config / entry point | `test_config_main` | env parsing; provider order & active-provider filtering; `python -m cyberkb` |
| catalog / render / schema | `test_catalog_render`, `test_catalog_schema` | catalog build/serialise; README/category rendering; JSON-Schema conformance incl. `classified_by` |
| library / build / checks | `test_library_build_checks` | load/validate; build idempotency; policy gate (specific messages asserted) |
| ingest / enrich | `test_ingest`, `test_enrich` | end-to-end filing with provenance; enrich upgrade/in-place/unchanged/skip/collision |
| cli | `test_cli` | every subcommand & exit code; LLM path, no-capacity, run-report, enrich, real taxonomy-error mapping |

## Self-audit (2026-10-06)

A critical pass for the four classic coverage-theater defects:

- **Over-mocking.** One test (`test_config_error_exit`) monkeypatched
  `cli.load_taxonomy` to force an error; it now writes a genuinely invalid
  taxonomy and exercises the real `KBError → exit-code` path. No remaining test
  mocks `cyberkb` logic.
- **Dead code.** The legacy single-provider `cyberkb.llm` client and four unused
  exception subclasses (`LLMRetryableError`, `LLMModelError`, `LLMFatalError`,
  `LLMResponseError`) were superseded by `providers/` and deleted, along with
  their test module — no untested or redundant code remains.
- **Weak assertions.** A static scan flagged assertions built on predicate
  calls (`any("category folder" in msg …)`, `isinstance(...)`, `re.fullmatch`);
  review confirmed these assert specific message content or a type contract, not
  mere existence.
- **Missing edge case.** Added a test that the circuit breaker's open state
  **persists across batch calls** — a tripped provider is skipped on later calls
  without being re-contacted.

## What is deliberately NOT covered (honest limitations)

- **The real provider network calls.** Every provider is driven through a fake
  HTTP transport; the live endpoints are never contacted in tests. A live smoke
  test needs real keys and network and belongs in a manual/integration run, not
  the unit gate.
- **Real wall-clock backoff and circuit cool-down.** `sleep`, `jitter` and the
  clock are injected, so retry/backoff and breaker timing are tested as control
  flow without awaiting real delays.
- **Classification *accuracy*** on the full corpus — a quality metric, not a
  correctness invariant. The mechanics (validation, routing, fallback) are
  tested; accuracy is validated per-model at run time by the pre-flight pass and
  recorded in the run report.
- **Windows path semantics.** Symlink tests are `skipif`-guarded off Windows;
  CI targets POSIX runners.

## How to reproduce

```bash
uv sync
uv run pytest                 # 479 cases, 100% line+branch coverage gate
uv run ruff check . && uv run ruff format --check .
uv run mypy                   # strict, src and tests
```
