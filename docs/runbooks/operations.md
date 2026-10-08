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
export GEMINI_API_KEY=... GROQ_API_KEY=...   # both required for any LLM command
uv run cyberkb preflight  # discover + validate every catalog model; changes no content
uv run cyberkb ingest     # classify + file inbox/, then rebuild
uv run cyberkb enrich     # classify pending library resources, backfill summaries
uv run cyberkb build      # just regenerate catalogs/pages from library/
uv run cyberkb check      # policy gate (what CI runs)
uv run cyberkb classify inbox/some-note.md   # preview, write nothing
```

`ingest --heuristic` and `classify --heuristic` work offline without keys.
Operational knobs (each fails the run if malformed, rather than being clamped):

| Variable | Default | Range | Meaning |
| --- | ---: | --- | --- |
| `CYBERKB_MODEL_RETRIES` | 3 | 0–10 | same-model retries after an error (never after a rate limit) |
| `CYBERKB_LIST_PASSES` | 2 | 1–5 | walks of the whole model list before giving up |
| `CYBERKB_LIST_BACKOFF` | 60 | 0–900 s | pause before re-walking the list |
| `CYBERKB_TIMEOUT` | 60 | 5–300 s | per HTTP request |
| `CYBERKB_BATCH_SIZE` | 10 | 1–50 | inbox documents per ingest request |

## LLM providers and the `awesome-cyber` environment

Classification uses **Google AI Studio** (primary) and **Groq** (secondary)
behind a per-model rotation engine (ADR-0008). Both keys are **required**:

| Provider | Secret | Endpoint | Auth |
| --- | --- | --- | --- |
| Google AI Studio | `GEMINI_API_KEY` | `https://generativelanguage.googleapis.com/v1beta` | `x-goog-api-key` header |
| Groq | `GROQ_API_KEY` | `https://api.groq.com/openai/v1` | `Authorization: Bearer` |

The **Ingest and index** workflow declares `environment: awesome-cyber` and
fails its first step if either secret is missing; a key the provider rejects
fails the run at model discovery. Keys are never printed or written to a report
(error text is the provider's response body, redacted against the key). To
rotate a key, update it under *Settings → Environments → awesome-cyber* (and
the repository secret, if you keep one); no code change.

### Models and their order

Which models may be used, in which order, and under which free-tier limits is
reviewed data in `schema/llm-models.yaml`, not code. The current order
(verified against the dashboards on 2026-10-07):

1. Gemma 4 31B · 2. Gemma 4 26B — 30 RPM, 14,400 RPD, 16K TPM each
3. Gemini 3.1 Flash Lite · 4. Gemini 3.5 Flash Lite — 15 RPM, 500 RPD, 250K TPM
5. Gemini 3.8 Flash · 6. 3.6 Flash · 7. 3.7 Flash · 8. 3.5 Flash · 9. 2.5 Flash
   — 5 RPM, 20 RPD · 10. Gemini 2.5 Flash Lite — 10 RPM, 20 RPD
11. Groq `allam-2-7b` — 30 RPM, 7,000 RPD, 6K TPM
12. `openai/gpt-oss-120b` · 13. `openai/gpt-oss-20b` · 14. `qwen/qwen3.8-27b`
    — 30 RPM, 1,000 RPD, 8K TPM

Groq's safety classifiers (`llama-prompt-guard-2-*`, `gpt-oss-safeguard-20b`)
are excluded and cannot be declared. Observed on 2026-10-07: `allam-2-7b` is
blocked for the Groq project until enabled under *console.groq.com → Settings →
Project → Limits*, and Google reports `gemini-2.5-flash` /
`gemini-2.5-flash-lite` as no longer available to new users; validation retires
them automatically and the reports say why. To change a limit or the order, edit the
catalog and update `verified_on`; to add a model, add its display name (Google)
or exact id (Groq). The API id is always resolved from the live `/models`
listing, so a name the API does not list shows up as `unresolved` in the
preflight and run report rather than being guessed.

### Pre-flight verification

Run **Actions → Ingest and index → Run workflow → mode: preflight** (safe on
any branch; nothing is committed), or `uv run cyberkb preflight` locally. It
lists both providers' models, resolves every catalog entry to its API id and
validates each one with a real classification probe, trying the strongest
structured-output mode first (Google: `responseJsonSchema` →
`responseSchema` → schema-in-prompt; Groq: strict `json_schema` →
`json_object`). The job summary and log show, per model: declared name → API
id, how it was resolved, verdict and mode, or the categorised reason it was
rejected. Verdicts are cached in the ledger for the quota day.

### Rotation and retry semantics

For each request the engine uses the highest-priority model that is usable and
ready now:

- **Pacing:** each model is kept under 90% of its declared RPM/TPM (sliding
  60 s window) and within its RPD/TPD for the quota day (Google resets at
  midnight Pacific; counts persist across runs in the ledger).
- **Errors** (timeout, 5xx, network, unusable answer) retry on the same model
  `CYBERKB_MODEL_RETRIES` times with jittered exponential backoff, then the
  request moves to the next model. A transient failure that outlives the
  retries benches the model for 5 minutes (a "strike"); three strikes without
  a success retire it until the next list pass.
- **Rate limits** (per-minute 429) move the request on immediately; the model
  cools down for the provider's advised delay and rejoins at its priority.
- **Daily quota** (per-day 429, or Groq reporting no requests left) retires the
  model until its quota day resets.
- **Auth failure** takes the provider out; a persistent network failure takes
  it out until the next list pass.
- **List passes:** when no model is left, transiently-failed ones are revived
  and the list is walked again, up to `CYBERKB_LIST_PASSES`; then the run stops
  as "no capacity".

Every run writes `docs/audit/ingest-runs/<date>-<run-id>.json` (final status
and reason, per-provider and per-model statistics, the ten-category failure
breakdown, retries per level, per-resource outcomes, every failed attempt).
Structured JSON attempt logs also go to stdout.

## Enriching the corpus (backfilling summaries)

Dispatch **Ingest and index** with **mode: enrich**. It ingests the inbox, then
sends every resource the ledger marks `pending` (then those marked `failed`,
for another chance) through the rotation, one document per request. A
successful answer upgrades the resource's category, format, language, tags and
summary, refreshes empty author lists and stamps `classified_by`; a category
change moves the file. Manual classifications are never touched.

### Progress is never lost

- Each upgraded document is written atomically and the ledger
  (`docs/audit/enrich-state.json`) saved before the next request.
- The job works in 20-minute chunks within `max_seconds` (default 19,800 s =
  5.5 h, under the 350-minute job timeout) and **commits and pushes after every
  chunk**; a cancelled job loses at most the chunk in progress.
- The next run reads the ledger and continues where it stopped; finished
  resources are never re-sent. A category move interrupted mid-way is completed
  automatically at the next start.
- `limit` caps one chunk (the run stops after it) for a cautious first pass.
- Dispatched on a pull-request branch, the run commits to that branch. GitHub
  does not start workflows from the job's own `GITHUB_TOKEN` pushes, so CI
  re-validates the enriched library on the next regular push to the branch.

### Outcomes

| Exit | Meaning | Job |
| ---: | --- | --- |
| 0 | every eligible resource is enriched | green |
| 5 | the time/resource budget ended with work left | red — re-dispatch to continue |
| 6 | no capacity left (quotas exhausted, models failing) or the remaining resources failed on every usable model | red — see the run report |

A resource that every usable model fails (for example, a content filter) stays
`failed` in the ledger with its cause and is retried on the next run. If it
keeps failing, classify it by hand (`classification.method: manual`) to take it
out of scope.

### Throughput

The binding limit is tokens per minute, not requests per day: one request is
about 4K input tokens. Gemma alone sustains roughly three requests a minute and
each Flash-Lite model fifteen, while the daily quotas (about 40,000 requests in
total) are barely touched, so the full corpus (~485 resources) completes within
one dispatch.

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
- **Provider keys in the `awesome-cyber` environment.** Required. Add
  `GEMINI_API_KEY` (Google AI Studio) and `GROQ_API_KEY` under *Settings →
  Environments → awesome-cyber*. Remove the retired `OPENROUTER_API_KEY` and
  `HF_TOKEN` secrets and the `LLM_PROVIDER_ORDER` variable; nothing reads them.
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
