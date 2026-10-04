# Security Policy

## Reporting a vulnerability

Please report security issues **privately**, not as public issues or pull
requests.

- Preferred: open a private advisory via
  **GitHub Security Advisories** →
  <https://github.com/BlueRingsLabs/awesome_cybersecurity/security/advisories/new>
- Or email **deeprat.tec@gmail.com**.

Include enough to reproduce: the affected file or workflow, the commit, and the
impact you observed. You will get an acknowledgement within a few days.

## Scope

This repository is a knowledge base plus the `cyberkb` tooling that indexes it.
Relevant classes of issue include:

- a flaw in the ingestion pipeline that lets untrusted contributor content
  execute code, exfiltrate secrets, or write outside `library/`;
- a GitHub Actions workflow weakness (privilege escalation, secret exposure,
  script injection);
- redistribution of content whose licence forbids it.

See [`docs/threat-model.md`](docs/threat-model.md) for the full model and the
controls in place.

## What is *not* a vulnerability here

- The presence of offensive security techniques, payloads or PoCs **inside
  fenced code blocks** — that is the subject matter of the library, and GitHub
  renders Markdown with HTML sanitisation.
- A classification or licence-detection miss on a single document; those are
  corrected through the normal review flow
  ([`docs/runbooks/content-licensing.md`](docs/runbooks/content-licensing.md)).

## Supply-chain posture

- All GitHub Actions are pinned to commit SHAs; Dependabot proposes updates.
- The default `GITHUB_TOKEN` is read-only; only the ingestion job is granted
  `contents: write`.
- CodeQL, zizmor, gitleaks, OpenSSF Scorecard and dependency review run in CI.
- Runtime dependencies are deliberately minimal (PyYAML only) to shrink the
  attack surface; see [ADR-0004](docs/adr/0004-minimal-runtime-dependencies.md).
