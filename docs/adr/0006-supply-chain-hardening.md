# 6. Supply-chain hardening for CI/CD

- Status: accepted
- Date: 2026-10-04

## Context

GitHub Actions is a common software-supply-chain entry point: mutable action
tags, over-broad tokens, and script injection via untrusted context are the
usual culprits. v1 used floating tags (`actions/checkout@v4`) and a workflow
with `contents: write` as the default.

## Decision

- Pin every action to a full commit SHA with a version comment.
- Default `permissions: contents: read`; grant wider scopes per job only where
  needed (ingestion gets `contents: write`; CodeQL/Scorecard get
  `security-events: write`).
- `persist-credentials: false` on checkouts except the push job.
- Run CodeQL, zizmor, gitleaks, OpenSSF Scorecard and dependency review; lint
  workflows with actionlint; keep actions and deps current with Dependabot.

## Consequences

- A re-tagged or compromised action cannot silently change behaviour.
- Token blast radius is minimised.
- Workflow security is enforced in CI (zizmor), not left to review.
- Pinning means updates are explicit PRs — the intended trade-off.

## Amendment — 2026-10-05

Two operational realities of running these controls under a GitHub
*organisation* account surfaced once the checks ran against the real repository.

### gitleaks runs as a pinned CLI, not the Action

`gitleaks/gitleaks-action` now requires a paid licence key (`GITLEAKS_LICENSE`)
for any repository owned by an organisation, and fails closed without one. The
gitleaks scanner itself is MIT-licensed and free. We therefore drop the Action
and run a **version-pinned, checksum-verified** gitleaks binary directly from
its release tarball (SHA-256 asserted in the workflow before execution), which
preserves the pinning guarantee without a paid dependency or an extra
third-party Action in the trust chain.

The scan targets the working tree (`gitleaks dir`) and is scoped by
[`.gitleaks.toml`](../../.gitleaks.toml): the full default ruleset is kept
(`useDefault = true`) and only the curated educational corpus (`library/`) and
the audit prose that quotes scanner output (`docs/audit/`) are allow-listed.
That corpus is third-party security write-ups whose subject matter *is* example
credentials and payloads; the project's own code, CI and configuration are
scanned in full, so a real credential leak still fails the build. The scoping
rationale lives in the config header and in the threat model.

### CodeQL: advanced workflow is the source of truth

Enabling GitHub Advanced Security switched on CodeQL **default setup** for the
repository. Observed on PR #16, default setup runs a single `Analyze (actions)`
job — it covers the workflow files but **not** the Python engine. GitHub refuses
to ingest results from an *advanced* configuration (this committed
[`codeql.yml`](../../.github/workflows/codeql.yml)) while default setup is
enabled; the two are mutually exclusive per repository. The advanced run
completes the full `security-extended` Python analysis and only the final upload
is rejected, with the verbatim error:

> Code Scanning could not process the submitted SARIF file: CodeQL analyses from
> advanced configurations cannot be processed when the default setup is enabled

We keep the advanced workflow as the source of truth because it is
version-controlled, SHA-pinned, least-privilege, and runs the stronger
`security-extended` query suite over **both** languages present in the
repository (`python` and `actions`, via a matrix) — all reviewable in a PR,
unlike the opaque default setup, which here leaves Python unscanned. The
required one-time maintainer action is therefore to **disable CodeQL default
setup** in *Settings → Code security → Code scanning → CodeQL analysis*
(switch it to *Advanced*, or disable it). Once disabled, this workflow's
results upload and it covers Python and Actions with no gap. Until then its
jobs report a *configuration error*, which is the conflict above and not a code
defect. This is recorded in the operations runbook as a maintainer action.
