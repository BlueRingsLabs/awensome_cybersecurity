# Threat model

This knowledge base ingests **untrusted contributor content** and processes it in
**CI that holds a write token and two LLM provider keys**. The model below
follows roughly the STRIDE prompts and states what is in scope, who the
adversary is, and which control answers each threat.

## Assets

- The integrity of `library/` and the generated catalogs.
- The CI write credential (`GITHUB_TOKEN`) and the `GEMINI_API_KEY` /
  `GROQ_API_KEY` secrets.
- The free-tier quotas those keys buy (an attacker who burns them stalls
  enrichment for a day).
- The enrichment ledger (`docs/audit/enrich-state.json`) and the run reports.
- The reputation of the catalog as a trustworthy, legally clean source.

## Trust boundaries

1. **Contributor → repository.** A pull request can contain arbitrary file
   content, filenames, front matter and symlinks.
2. **Repository → CI runner.** Workflows execute with tokens and secrets.
3. **CI → LLM providers.** Outbound HTTPS to exactly two hosts,
   `generativelanguage.googleapis.com` (key in the `x-goog-api-key` header) and
   `api.groq.com` (`Authorization: Bearer`). Requests carry a key; responses —
   model listings, answers and error bodies — are untrusted input.
4. **Repository → pipeline configuration.** `schema/llm-models.yaml` and the
   ledger are committed files a pull request can edit, so the pipeline treats
   them as data to validate, not as trusted configuration.

## Threats and controls

### Malicious submission content

| Threat | Control |
| --- | --- |
| Path traversal / symlink to read or overwrite files outside `library/` | `fsutil.read_text` opens with `O_NOFOLLOW`, rejects symlinks and non-regular files, and `ensure_within` refuses any path that escapes the repo root. |
| Oversized or binary "Markdown" exhausting the runner | Size cap (8 MiB) and NUL-byte rejection in `fsutil.read_text`; empty submissions rejected by `ingest`. |
| "Trojan Source" bidi/control-character deception (CVE-2021-42574) | `textutil.strip_unsafe_chars` removes C0/C1 controls, bidi overrides and BOMs during sanitisation. |
| Stored XSS via raw HTML/JS in a document rendered by a catalog viewer | GitHub sanitises rendered Markdown HTML; `markdown.active_content` additionally flags unfenced executable content in `cyberkb check`. **Criterion (deliberate):** this is a WARNING, never an error, and **never a reason to exclude a resource.** Security literature (OWASP, WSTG, XSS cheat sheets) legitimately quotes payloads; the corpus must stay complete. The warning simply nudges a maintainer to wrap a payload in a code fence, where renderers show it inertly. Rendered README/category tables additionally escape every interpolated value (title, tag, summary). A downstream viewer that renders raw Markdown is responsible for its own HTML sanitisation. |
| YAML "billion laughs" / object-construction via front matter or taxonomy | `yamlsafe.safe_load` uses `SafeLoader` (no object construction) **and** rejects anchors/aliases; front-matter size is capped. |
| Markdown-injection that breaks the generated tables | `render` passes every title/tag/summary through plain-text reduction and inline-Markdown escaping. |

### Classification and licensing integrity

| Threat | Control |
| --- | --- |
| LLM returns an invalid or hallucinated category/tag | Response schema is built from the live taxonomy (invalid labels impossible); every field is re-validated, and invalid/low-confidence results fall back to the heuristic. |
| Redistributing content whose licence forbids it | `licensing.detect_license` + `cyberkb check` block `restricted` licences unless kept as a capped reference stub; `noncommercial` terms are recorded and surfaced; unknowns are flagged. |
| Prompt injection in a document steering the classifier | The model only returns a constrained label set; a successful injection cannot produce an out-of-taxonomy result or any side effect, because classification output is pure data that is re-validated. |

### CI / supply chain

| Threat | Control |
| --- | --- |
| Compromised or re-tagged third-party action | Every action pinned to a full commit SHA; Dependabot proposes updates; zizmor enforces pinning. |
| Token overreach / privilege escalation | Workflow default `permissions: contents: read`; only the ingestion job gets `contents: write`; other scopes granted per-job. |
| Secret exfiltration via a crafted workflow or committed secret | `persist-credentials: false` on checkouts except the push job; a version-pinned, checksum-verified gitleaks CLI scans the working tree (scoped by `.gitleaks.toml` — see below); harden-runner audits egress; CodeQL and Scorecard run on a schedule. |
| Dependency vulnerability | Minimal runtime surface (PyYAML only); `pip`/`uv` lockfile; dependency review on PRs. |
| LLM provider key leakage / untrusted egress | `GEMINI_API_KEY` and `GROQ_API_KEY` live in the `awesome-cyber` environment and reach only the steps that call a provider. They are never printed (the presence check reports names only). Keys travel in request headers, never URLs. The provider text kept on an error is the response body, and every adapter additionally redacts its own key from that text before it is logged or written to a committed report. Egress is audited by harden-runner; the runtime stays stdlib `urllib` (ADR-0004). |
| A pull request redirecting a key via the model catalog | Adapters hard-code their verified endpoint; building a provider refuses a catalog whose `base_url` differs, so editing `schema/llm-models.yaml` cannot send a key to another host. The catalog loader rejects unknown keys, non-positive limits, duplicate models and the excluded safety-classifier models. |
| A tampered ledger deleting files through move recovery | Recovery acts only on `library/**.md` paths inside the repository (symlinks refused), and only when both documents carry the recorded resource id; anything else is an error or a no-op. A malformed ledger stops the run instead of resetting progress. |
| Path traversal through a run id | `--run-id` becomes part of a report file name, so it is restricted to 1–64 characters of `[A-Za-z0-9._-]` with no `..`. |
| Shell injection through workflow inputs | Dispatch inputs reach scripts only through environment variables; `limit`/`max_seconds` are validated as positive integers before use. |

Secret scanning keeps the full gitleaks default ruleset and scopes out only the
curated corpus (`library/`) and the audit prose that quotes scanner output
(`docs/audit/`). Those are third-party security write-ups whose subject matter
*is* example credentials — Basic-auth demo strings, textbook JWTs, the
empty-password NTLM hash, expired STS tokens copied from public reports — none
of them live secrets of this project. The threat the control defends against is
a real credential leaked into the project's **own** code, CI or configuration,
all of which remain scanned in full; a hit there fails the build. See
[`.gitleaks.toml`](../.gitleaks.toml) and ADR-0006.

### Availability

| Threat | Control |
| --- | --- |
| A provider is down, rate-limited or out of quota | Per-model pacing keeps calls under each declared RPM/TPM/RPD. A rate limit moves the request to the next model while the limited one cools down; a spent daily quota retires the model; auth or persistent network failure takes the provider out; transient failures are revived on a bounded second list pass. New inbox submissions always fall back to the heuristic, so a merge is never blocked. Enrichment leaves unprocessed resources `pending` and the job ends red with the reason. |
| A missing or rejected key silently degrading every run | Fail fast: the workflow's first step requires both secrets, and a key rejected at model discovery stops the run before any content is touched. An edge block (Cloudflare `403 error code: 1010`) is reported as a network failure, not as a bad key. |
| Quota burnt by retries or probes | Rate limits are never retried in place. Validation probes run once per model per quota day (cached in the ledger). Retries are capped per model and per list pass, and never sleep past the run deadline. |
| A long run lost to a timeout or cancellation | Each resource is written atomically and the ledger saved immediately; the workflow commits after every 20-minute chunk, so at most one chunk of work can be lost. |
| A model answering garbage, off-taxonomy labels or a refusal | Answers are schema-constrained where the model supports it, re-validated field by field, and refusals are detected; such an answer is an `inference_error`, retried and then routed to another model, and never written. |
| A single malformed document fails the whole build | `library` records per-document problems and continues; `build` refuses to write only when the library as a whole is invalid, with precise messages. |

## Residual risk / explicitly out of scope

- The library intentionally contains offensive-security techniques and PoCs.
  That is subject matter, not a vulnerability; payloads belong in code fences.
- `NOASSERTION` resources carry unconfirmed licences; commercial reuse requires
  confirmation (see the content-licensing runbook).
- Automated licence detection can miss or misread a notice; the review flow
  exists to correct it, and rights holders can request changes.
