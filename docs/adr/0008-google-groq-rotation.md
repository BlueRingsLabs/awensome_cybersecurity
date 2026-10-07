# 8. Google AI Studio and Groq with per-model rotation

- Status: accepted
- Date: 2026-10-07
- Supersedes: the provider set, model discovery/ranking, rotation and circuit
  breaker of [ADR-0007](0007-multi-provider-llm.md). Its structured error
  taxonomy, attempt logging and `classified_by` provenance stand.

## Context

ADR-0007 gave us three interchangeable providers and runtime model discovery.
Running it against the real corpus (485 heuristically-filed resources awaiting
enrichment) exposed three problems.

**The free tiers we relied on cannot carry a backfill.** I reviewed the actual
free-tier allowance of every candidate:

| Provider | Free-tier reality | Verdict |
| --- | --- | --- |
| Hugging Face | ~US$0.10/month of serverless credit; most instruct models not on the free serverless tier | dropped |
| OpenRouter | 50 requests/day without a US$10 top-up | dropped |
| Pollinations | ~1.5 requests/week on the free tier | dropped |
| Mistral | API access requires activating payment | dropped |
| Cerebras | API access requires activating payment | dropped |
| **Google AI Studio** | per-model daily quotas: 14,400 RPD on each Gemma 4 model, 500 on Flash-Lite, 20 on Flash | **kept (primary)** |
| **Groq** | per-model daily quotas: 7,000 RPD on allam-2-7b, 1,000 on gpt-oss and qwen3.8 | **kept (secondary)** |

Google and Groq together offer roughly 40,000 requests per day, spread over
fourteen per-model quotas.

**The bottleneck is tokens per minute, not requests per day.** One enrichment
request is about 4K input tokens (taxonomy, schema and a 6,000-character
excerpt). At Gemma's 16K TPM that is three or four requests a minute; at
allam-2-7b's 6K TPM, about one. Rotation that treats every 429 as "this model is
done" would burn through all fourteen models in minutes while the best one is
usable again 60 seconds later.

**ADR-0007 misread Gemini's 429s.** Gemini's per-minute 429 says "You exceeded
your current quota"; our generic classifier read the word *quota* as billing
exhaustion and tripped the provider's circuit breaker on every per-minute limit.
Gemini's model listing is also paginated, which discovery ignored.

## Decision

### Two providers, verified contracts

Both adapters were written against the official documentation (verified
2026-10-07) and are exercised in tests with responses in exactly those shapes.

**Google AI Studio** — `https://generativelanguage.googleapis.com/v1beta`, key
in the `x-goog-api-key` header (never in the URL).

- Discovery: `GET /models`, paginated with `pageSize=1000` and `nextPageToken`.
  Only models whose `supportedGenerationMethods` contains `generateContent` are
  candidates.
- Calls: `POST /models/{id}:generateContent`.
- Structured output is a ladder, tried strongest first while a model is being
  validated: `responseJsonSchema` → `responseSchema` → the schema embedded in
  the system prompt with JSON recovered from text (for models without a native
  JSON mode). A mode is abandoned only when the API rejects it as
  `INVALID_ARGUMENT`, and every step is recorded.
- Errors follow `google.rpc.Status`:
  - a 429 `RESOURCE_EXHAUSTED` whose `QuotaFailure.quotaId` contains `PerDay`
    (or whose message reports `limit: 0`) is `quota_exceeded`; otherwise it is
    `rate_limit`, with `RetryInfo.retryDelay` as the cooldown;
  - `API_KEY_INVALID`, `PERMISSION_DENIED` and `FAILED_PRECONDITION` (for
    example, an unsupported region) are `auth_error`;
  - thought parts are never parsed as the answer.

**Groq** — `https://api.groq.com/openai/v1`, `Authorization: Bearer`.

- Discovery: `GET /models`, keeping entries that are `active`; `context_window`
  is the shared input+output window.
- Calls: `POST /chat/completions`.
- Structured output: strict `json_schema` (every object
  `additionalProperties: false`), stepping down to `json_object`.
- 429 handling: Groq's `x-ratelimit-*-requests` headers are the RPD and
  `*-tokens` the TPM. A 429 with no requests left, or naming RPD/TPD, is
  `quota_exceeded`; otherwise it is `rate_limit`, with `retry-after` as the
  cooldown.
- Other codes: `json_validate_failed` is the model's bad output, not our
  request; 498 (flex capacity) is transient.
- `<think>` blocks are stripped before parsing.

The safety classifiers (`meta-llama/llama-prompt-guard-2-22m`, `-86m`,
`openai/gpt-oss-safeguard-20b`) are excluded and can never be declared.

HF, OpenRouter, the OpenAI-compatible base class, model ranking heuristics,
the eager selection pass and the circuit breaker are deleted, not disabled.

### The catalog is reviewed data

`schema/llm-models.yaml` lists the providers in fallback order, and each
provider's models in priority order. For every model it records the RPM, RPD,
TPM (and TPD) limits from the dashboards, the date they were read, and the
quota time zone (Google resets at midnight Pacific).

It never states an API id. Each declared name is resolved against the live
listing, in this order:

1. an id published in the docs (`gemma-4-31b-it`, `gemma-4-26b-a4b-it`);
2. the display name;
3. the normalised id.

Stable ids are preferred over preview aliases, and the rule used is reported.
A declared model the API does not list is skipped and reported.

The loader is strict, and building a provider refuses a `base_url` that differs
from the adapter's verified endpoint, so a pull request editing the catalog
cannot redirect a key.

Priority order, as verified on 2026-10-07:

| # | Provider | Declared model | RPM | RPD | TPM |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | Google | Gemma 4 31B | 30 | 14,400 | 16K |
| 2 | Google | Gemma 4 26B | 30 | 14,400 | 16K |
| 3 | Google | Gemini 3.1 Flash Lite | 15 | 500 | 250K |
| 4 | Google | Gemini 3.5 Flash Lite | 15 | 500 | 250K |
| 5 | Google | Gemini 3.8 Flash | 5 | 20 | 250K |
| 6 | Google | Gemini 3.6 Flash | 5 | 20 | 250K |
| 7 | Google | Gemini 3.7 Flash | 5 | 20 | 250K |
| 8 | Google | Gemini 3.5 Flash | 5 | 20 | 250K |
| 9 | Google | Gemini 2.5 Flash | 5 | 20 | 250K |
| 10 | Google | Gemini 2.5 Flash Lite | 10 | 20 | 250K |
| 11 | Groq | `allam-2-7b` | 30 | 7,000 | 6K (500K TPD) |
| 12 | Groq | `openai/gpt-oss-120b` | 30 | 1,000 | 8K (200K TPD) |
| 13 | Groq | `openai/gpt-oss-20b` | 30 | 1,000 | 8K (200K TPD) |
| 14 | Groq | `qwen/qwen3.8-27b` | 30 | 1,000 | 8K (200K TPD) |

### Pre-flight

Before any work, both keys must be present (the workflow fails first, and the
CLI refuses next) and both listings must succeed. A rejected key at listing is
a hard stop; any other listing failure takes that provider out for the run,
with the cause recorded.

Each model is validated **lazily**, on first use, with a real classification
probe. The answer must be schema-valid, on-taxonomy, carry a summary, and not
be a refusal. A failed validation is recorded with its category and the model
is skipped for the quota day. Verdicts are cached in the ledger for the day,
so later chunks and runs do not re-spend a 20-RPD model's quota on probes.

`cyberkb preflight` validates every model at once and prints the declared name,
API id, resolution rule, verdict and mode, without touching content.

### Rotation: priority with pacing, not "use until it breaks"

For every request the engine uses the **highest-priority model that is usable
and ready now**.

**Pacing.** A per-model governor keeps a sliding 60-second window of requests
and tokens, at 90% of the declared RPM/TPM. It counts RPD/TPD per quota day,
carried across runs in the ledger. Work therefore flows to Gemma whenever it
has capacity, spills to the next model while it does not, and returns as soon
as it does. 429s become the exception.

**Errors** (timeout, 5xx, network, unusable answer) are retried on the same
model: `CYBERKB_MODEL_RETRIES` (default 3) retries, with full-jittered
exponential backoff (base 2 s, cap 60 s, honouring server hints), never past
the run deadline. Then the request moves to the next model. A per-request
failure (content filter, bad output) skips that model for that document only;
three consecutive such failures retire the model.

**Rate limits** are not errors. The model cools down (`RetryInfo` /
`retry-after`, default 60 s), its pacing tightens by 20%, and the request
moves on at once. The model rejoins when cooled, and three consecutive rate
limits take it out until the next list pass.

**Quota exhaustion** retires the model until its quota day resets.

**Auth failures** take the whole provider out. A network failure that survives
the retries takes the provider out until the next list pass.

**List passes.** When nothing usable is left, models and providers that failed
only transiently are revived and the list is walked again after
`CYBERKB_LIST_BACKOFF` (60 s). This happens up to `CYBERKB_LIST_PASSES`
(default 2) times; then the engine is exhausted and says so.

**Fitting.** Each request is fitted to the model: a quarter of a shared context
window (at least 512 tokens) is reserved for the answer, and the excerpt is cut,
re-measuring each time, until the request fits the window and the paced TPM.
A model that would keep under 600 characters of the document is not used for
it.

### Persistence, resumability and reporting

`docs/audit/enrich-state.json` is the ledger:

- each resource's status (`pending`, `enriched`, `failed`), who enriched it,
  or why it failed;
- per-model daily usage and validation verdicts;
- the last run.

Front matter stays the source of truth: the ledger is reconciled from the
library on every run. Each upgraded document is written atomically and the
ledger saved before the next request. A category move is recorded before it
happens, and the next start completes or discards it; that recovery only ever
touches library documents that carry the recorded id, so a tampered ledger
cannot delete arbitrary files. A malformed ledger stops the run instead of
silently starting over.

Every run writes `docs/audit/ingest-runs/<date>-<run-id>.json`, complete or
not. It records:

- the final status (`complete` / `partial` / `failed`) and its reason;
- per provider and per model: attempts, successes, failures, the last error
  category and message, the resolution, the validation trail and today's
  usage;
- all ten failure categories, zero-filled;
- retries per model, per provider and per list pass;
- every resource attempted or left, with who processed it or why not;
- every failed attempt, verbatim and key-redacted.

The workflow enriches in 20-minute chunks within `max_seconds` (default
5.5 h) and commits after every chunk, refusing to commit anything that fails
`cyberkb check`. Exit 5 ("budget ended, continue") starts the next chunk. Exit
6 ("no capacity") or an incomplete final state ends the job red, after its
progress is committed.

## Consequences

- A full backfill fits in one dispatch. Gemma alone sustains about three
  requests a minute and Flash-Lite fifteen, so 485 resources take well under
  the 5.5 h budget while daily quotas are barely touched. A cancelled job
  loses at most one chunk.
- Every model choice is auditable: declared name, live id, resolution rule,
  validation trail, mode and usage are in every report.
- Two keys are now required, not optional. A missing key is a red job, not a
  silent heuristic run. Ingestion still files new submissions with the
  heuristic for any document the LLM cannot classify.
- Model churn (a renamed or retired model) is absorbed at run time and shows
  up as an `unresolved` row in the report. Changing priority or limits is a
  one-line data change to the catalog, reviewed like code.
- Dashboard limits can drift. The governor's headroom, multiplicative
  tightening and provider-reported exhaustion (Groq headers, Gemini
  `quotaId`) keep the engine safe when they do.
