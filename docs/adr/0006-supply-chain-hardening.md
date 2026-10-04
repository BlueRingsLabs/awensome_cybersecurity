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
