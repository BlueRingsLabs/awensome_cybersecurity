# Threat model

This knowledge base ingests **untrusted contributor content** and processes it in
**CI that holds a write token and (optionally) an API key**. The model below
follows roughly the STRIDE prompts and states what is in scope, who the
adversary is, and which control answers each threat.

## Assets

- The integrity of `library/` and the generated catalogs.
- The CI write credential (`GITHUB_TOKEN`) and the `GEMINI_API_KEY` secret.
- The reputation of the catalog as a trustworthy, legally clean source.

## Trust boundaries

1. **Contributor → repository.** A pull request can contain arbitrary file
   content, filenames, front matter and symlinks.
2. **Repository → CI runner.** Workflows execute with tokens and secrets.
3. **CI → Gemini API.** Outbound requests carry the API key; responses are
   untrusted input.

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
| LLM provider key leakage / untrusted egress | The three provider keys (`GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `HF_TOKEN`) live in the `awesome-cyber` environment, are read only by the ingestion job, and are never printed: keys go in request headers only, and the verbatim provider text retained on an error is the response body, never the request. Egress reaches only the documented provider hosts and is audited by harden-runner; the runtime stays stdlib `urllib` (ADR-0004), adding no HTTP dependency to that surface. |

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
| Gemini unavailable or rate-limited blocks merges | Deterministic offline heuristic is a guaranteed fallback; the client retries with jittered backoff and falls through a model chain. |
| A single malformed document fails the whole build | `library` records per-document problems and continues; `build` refuses to write only when the library as a whole is invalid, with precise messages. |

## Residual risk / explicitly out of scope

- The library intentionally contains offensive-security techniques and PoCs.
  That is subject matter, not a vulnerability; payloads belong in code fences.
- `NOASSERTION` resources carry unconfirmed licences; commercial reuse requires
  confirmation (see the content-licensing runbook).
- Automated licence detection can miss or misread a notice; the review flow
  exists to correct it, and rights holders can request changes.
