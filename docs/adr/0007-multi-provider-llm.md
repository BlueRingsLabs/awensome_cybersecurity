# 7. Multi-provider LLM classification with runtime model selection

- Status: accepted
- Date: 2026-10-05

## Context

v2 classified with a single provider (Gemini) and a hard-coded model chain
(ADR-0004, ADR-0005). That is fragile: a provider outage, an auth problem, a
retired model or an exhausted free-tier quota stalls the whole pipeline, and a
hard-coded model id silently stops working when the provider changes its
catalog. Free tiers in particular move constantly — Google has been narrowing
Gemini's free models, OpenRouter meters free models per minute and per day, and
Hugging Face's serverless credits are small — so *assuming* a named model is
available is unsafe.

We want resilience across providers, model choices that are discovered and
*proven* rather than assumed, honest failure accounting, and the ability to add
a fourth provider without touching the orchestration.

## Decision

### One interface, interchangeable providers

Every provider implements `cyberkb.providers.base.LLMProvider`: `is_configured`,
`discover_models`, `complete_json` (one structured-output call), `available` (a
cheap pre-check) and `health_check`. Shared REST/JSON machinery lives in
`HttpProviderBase` and `OpenAICompatProvider`; the single HTTP boundary
(`providers/http.py`) is injectable, so the whole stack is unit-tested without a
socket or a key. The registry (`providers/registry.py`) is the one place a
provider is listed — adding a fourth is implementing the class and registering
it; config, orchestration and tests need no change.

The shipped providers:

- **Gemini** — native `responseSchema` structured output.
- **OpenRouter** — OpenAI-compatible; broad catalog of free models.
- **Hugging Face** — OpenAI-compatible Inference router.

A provider is active only when its key is present (`GEMINI_API_KEY`,
`OPENROUTER_API_KEY`, `HF_TOKEN`). Fallback order is `LLM_PROVIDER_ORDER`
(default `gemini,openrouter,huggingface`).

### Discovery, filtering and a documented preference order

Each provider discovers models from its own catalog API and keeps only those
that are usable, accessible with our credentials, and suitable for
classification/summarisation. Candidates are ranked (higher is better); the
ranking is deliberate, not alphabetical, and not "cheapest first":

- **Gemini** keeps text models that support `generateContent`. Flash is
  preferred (0.90) for the best quality/latency balance on the free tier,
  Flash-Lite next (0.78) as the most free-tier-friendly, Pro last (0.60) because
  it is restricted or paid on the free tier; a small bonus favours the newer
  version or the `-latest` alias. `is_free` is true for everything but Pro.
- **OpenRouter** keeps only free models (`:free` suffix or zero prompt/
  completion pricing), ranked by family — the strongest open instruction-
  followers first (Llama-3.3 0.92, Qwen-2.5/Qwen3 0.90, DeepSeek 0.86, …) with a
  small bonus for a larger context window. The Free Models Router
  (`openrouter/auto`) is appended last as a documented safety net.
- **Hugging Face** keeps small instruction-tuned models (dropping 70B+ that
  exceed the serverless free tier), ranked by family (Qwen2.5-7B/14B, Llama-3.1-
  8B, Gemma-2-9B, …), and checks the model-status endpoint (`available`) before
  use so a cold or gated model is skipped rather than burning a call.

### Validation before the run (not assumption)

Pre-flight (`providers/selection.py`) *proves* candidates before the real run.
For each candidate (best first, up to a cap) it checks availability, then sends
a small set of representative cybersecurity prompts — one offensive, one
defensive/IR, one governance/hardening — and accepts the model only when every
answer is valid, well-formed JSON that is on-taxonomy and carries a summary.
Validation stops once enough models pass, to respect free-tier request caps.
Rejected models are recorded with the reason. This is the "don't assume
available; verify it can be called and returns usable output" requirement.

### Rotation, retry, circuit breaking

The orchestrator (`providers/orchestrator.py`) drives providers in order and
routes on the failure category:

- *transient* (rate limit, timeout, 5xx, network) → retry the same model with
  full-jittered exponential backoff (base 1s, cap 30s, honouring `Retry-After`),
  then rotate to the next model;
- *model-level* (unavailable, content filter, bad output, unknown) → rotate to
  the next model immediately;
- *provider-fatal* (auth, quota exhausted) → trip the provider's circuit
  breaker and skip it for the rest of the run.

The per-provider circuit breaker (threshold 3 failures, 30s cool-down,
half-open trial) stops a dead provider from wasting the run's rate-limit budget.
When every provider and model is exhausted the batch falls back to the
deterministic heuristic, and that count is recorded. Values are defaults in
`OrchestratorSettings`, chosen to be gentle on free tiers while still making
progress; they are adjustable without code changes.

### Structured error taxonomy and run report

Every attempt is logged as one JSON line (`cyberkb.obslog`) with the provider,
model, resource id, attempt number, outcome, categorised cause
(`cyberkb.errors.FailureCategory`: auth_error, rate_limit, quota_exceeded,
timeout, server_error, network_error, inference_error, content_filter,
model_unavailable, unknown), HTTP status, the provider's verbatim error, timing
and whether a fallback was triggered. There is no `except Exception: pass` and
no generic "failed". An end-of-run report is written to
`docs/audit/ingest-runs/<date>.json`: per-provider success rates, failure-
category breakdowns, heuristic-fallback count, provider health, and the model
selection/validation results.

### Provenance

Each resource records `classified_by` as `<provider>:<model>@<ISO-8601 UTC>`
(or `heuristic@…`/`manual@…`), so the catalog can be audited for cross-provider
consistency.

## Consequences

- A provider outage, bad key or exhausted quota degrades gracefully to the next
  provider and finally to the heuristic, rather than stalling ingestion.
- Model choice tracks each provider's live catalog and is validated, so a
  retired or cold model is never used blindly.
- Every failure has a cause and a category, and every run leaves an auditable
  report; the free-tier economics are explicit, not hidden.
- Secret surface grows to three keys; all are environment/secret-scoped, never
  logged (the raw text retained on errors is the provider's response body, never
  request headers), and the runtime stays dependency-free stdlib `urllib`.
- The pipeline is more moving parts than a single client; the circuit breaker,
  bounded validation and backoff keep it from hammering free tiers, and the
  100%-covered test suite exercises every rotation and fallback path.
- Backfilling the whole corpus is one slow LLM call per resource, so it cannot
  finish in a single CI job or a free provider's daily cap. Enrichment is
  therefore bounded per run (`--limit` / `--max-seconds`) and resumable:
  completed work is written and committed as it goes, deferred resources are
  skipped on the next run, and the operation converges by simply re-running.
  This keeps each run inside the job timeout and the rate limit while guaranteeing
  forward progress (see 2.2.1 and the operations runbook).
