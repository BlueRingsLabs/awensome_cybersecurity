# Operations runbook

Day-to-day operation of the knowledge base.

## Accepting a contribution

1. A PR adds one or more files under `inbox/`. Review for topic fit, licence and
   the content rules in `CONTRIBUTING.md`.
2. Merge to `main`. The **Ingest and index** workflow runs automatically: it
   classifies and files each submission, rebuilds the catalogs, verifies with
   `cyberkb check`, and commits the result.
3. Confirm the follow-up commit landed and CI is green.

## Running the pipeline manually

```bash
uv sync
uv run cyberkb ingest     # classify + file inbox/, then rebuild
uv run cyberkb enrich     # backfill summaries/classification on existing resources
uv run cyberkb build      # just regenerate catalogs/pages from library/
uv run cyberkb check      # policy gate (what CI runs)
uv run cyberkb classify inbox/some-note.md   # preview, write nothing
```

With at least one provider key set, classification uses the LLM providers;
without any, the offline heuristic. Tune with `LLM_PROVIDER_ORDER`,
`CYBERKB_BATCH_SIZE`, `CYBERKB_MAX_RETRIES`, `CYBERKB_TIMEOUT`.

## LLM providers and the `awesome-cyber` environment

Classification is multi-provider (ADR-0007). A provider is used only when its
key is present; the fallback order is `LLM_PROVIDER_ORDER` (default
`gemini,openrouter,huggingface`).

| Provider | Secret |
| --- | --- |
| Google Gemini | `GEMINI_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Hugging Face | `HF_TOKEN` |

The **Ingest and index** workflow declares `environment: awesome-cyber`, so it
reads these from that deployment environment first and from repository secrets
as a fallback — keep the values identical in both, or rely on the environment
alone once environment protection rules are in place. To rotate a key, update
it in the `awesome-cyber` environment (Settings → Environments → awesome-cyber)
and/or repository secrets; no code change. Models are discovered and validated
at run time, so a retired model never breaks the pipeline — the run report
records which models were used or rejected.

Every run writes a dated report to `docs/audit/ingest-runs/<date>.json`
(per-provider success rates, failure categories, heuristic-fallback count,
provider health, model selection). Structured JSON attempt logs also go to
stdout for the workflow log.

## Enriching the corpus (backfilling summaries)

Most migrated resources were filed by the heuristic with an empty summary. To
upgrade them, run `cyberkb enrich` (locally, or the **Ingest and index**
workflow dispatched with `enrich: true`). It re-classifies each
heuristically-filed resource through the providers, adopts the LLM category,
tags and one-line summary, refreshes empty author lists, stamps `classified_by`,
and moves a file when its category changes. Manual classifications (including
the reference-only works) are never touched.

### Why it must run in batches

Enrichment makes **one LLM call per resource**, and free-tier models are slow
(tens of seconds to ~100 s each) and rate-limited. The full corpus is ~485
heuristic resources, so a single pass would take **hours** — longer than a
GitHub Actions job should run, and well past a free provider's daily request
cap. `enrich` is therefore **bounded and resumable**:

- `--limit N` processes at most `N` resources this run.
- `--max-seconds S` stops starting new work after `S` seconds, so the run always
  finishes and commits what it completed (enriched files are written as it goes).
- Resources left for later are reported as **deferred**; already-enriched ones
  are skipped on the next run. So you simply **re-run until `deferred` is 0**.

The **Ingest and index** workflow exposes both as dispatch inputs (`limit`,
`max_seconds`; `max_seconds` defaults to 1500 ≈ 25 min). Each dispatch commits
its progress, so firing it repeatedly walks the whole corpus. The job
`timeout-minutes` is a high backstop (350) — the `max_seconds` budget, not the
timeout, is what ends a run cleanly.

### Rate limits and throughput

- **OpenRouter free tier:** ~20 requests/minute and **50/day**, raised to
  **1,000/day with US$10 of credit**. The ~12 pre-flight validation calls count
  against this, so without the credit budget on ~35–40 enrichments per day.
- **Hugging Face:** a small monthly serverless credit (and many models are not
  on the free serverless tier — see note below).

**Recommended fastest path:** add the US$10 OpenRouter credit (lifts the daily
cap to 1,000), then dispatch with a large budget, e.g. `max_seconds: 18000`
(5 h). One or two such runs complete the corpus. **Free path (no credit):**
dispatch with the default `max_seconds` (or `limit: 35`) once per day and re-run
until `deferred` reaches 0 — roughly a dozen runs. Either way, **each run
commits real progress**, so interruptions never lose work.

### Provider availability note (observed 2026-10-06)

In the first live run, OpenRouter served (two NVIDIA Nemotron free models
validated), while **Gemini** returned `400 INVALID_ARGUMENT` / `503` on its
top discovered models and **Hugging Face** reported its candidates as not
available on the serverless tier. The orchestrator correctly fell over to the
working provider — this is the designed behaviour, not a failure — but it means
OpenRouter currently carries enrichment. If you want Gemini in the mix, confirm
the `awesome-cyber` `GEMINI_API_KEY` is valid for the `generateContent` API; to
drop a consistently-unavailable provider from the pre-flight entirely, set
`LLM_PROVIDER_ORDER` (e.g. `openrouter,gemini`) in the environment.

## Fixing a misclassification

Edit the file's front matter in `library/` (set `category`, `tags`, etc. and
`classification.method: manual`), move it to the correct `library/<category>/`
folder if the category changed so the folder matches, then:

```bash
uv run cyberkb build && uv run cyberkb check
```

Commit the file move plus the regenerated catalogs.

## "CI says the catalogs are out of date"

Someone changed content or the taxonomy without regenerating. Run
`uv run cyberkb build`, commit the changed `index.json`, `index.yaml`, README
block and category pages.

## Removing a resource

Delete the file under `library/`, run `uv run cyberkb build`, commit. If it was
removed for a licensing or rights-holder reason, record it in
`docs/audit/` and `NOTICE` as appropriate.

## One-time repository settings (maintainer)

These live in GitHub settings, not in the tree, so they must be set once by a
maintainer with admin rights. They are required for CI to be fully green.

- **Actions enabled.** The ingestion workflow commits regenerated catalogs, so
  Actions must be enabled for the repository.
- **Provider keys in the `awesome-cyber` environment.** Optional but needed for
  LLM classification and enrichment. Add `GEMINI_API_KEY`, `OPENROUTER_API_KEY`
  and/or `HF_TOKEN` under *Settings → Environments → awesome-cyber* (and, for
  parity, repository secrets). Any subset works; absent providers are skipped.
- **Disable CodeQL default setup.** Enabling GitHub Advanced Security turns on
  CodeQL *default setup*, which is mutually exclusive with this repository's
  committed, SHA-pinned advanced workflow (`.github/workflows/codeql.yml`).
  While default setup is on, GitHub rejects the advanced workflow's results and
  its *Analyze (python)* / *Analyze (actions)* checks fail with *"CodeQL
  analyses from advanced configurations cannot be processed when the default
  setup is enabled."* Turn default setup **off** under *Settings → Code security
  → Code scanning → CodeQL analysis* (switch to *Advanced*, or disable) so the
  advanced workflow — the version-controlled source of truth, running the
  `security-extended` suite over both `python` and `actions` — uploads its
  results. This repository's default setup scans `actions` only, so it is the
  advanced workflow that provides Python coverage; do **not** simply delete
  `codeql.yml` unless you first widen default setup to include Python, or Python
  loses CodeQL coverage entirely. The two configurations must not both be
  active. See ADR-0006.

## Secret scanning (gitleaks)

Secret scanning runs a version-pinned, checksum-verified gitleaks CLI (the
Action requires a paid licence for organisation-owned repositories; the CLI is
free). To reproduce a CI run locally:

```bash
uv run cyberkb check            # content/policy gate
gitleaks dir . --config .gitleaks.toml --redact   # same scan CI runs
```

A hit inside `library/` or `docs/audit/` is expected educational content and is
allow-listed in `.gitleaks.toml`; a hit anywhere else (code, CI, config) is a
real finding — rotate the exposed credential and purge it from history before
merging. To bump the pinned gitleaks version, update `GITLEAKS_VERSION` and
`GITLEAKS_SHA256` in `.github/workflows/security.yml` together (the SHA-256 of
the `linux_x64` tarball is published in the release's `checksums.txt`).
