# 1. Treat all contributor content as hostile

- Status: accepted
- Date: 2026-10-04

## Context

The pipeline reads Markdown that anyone can submit and later runs in CI with a
write token and an API key. The v1 scripts read files with plain `read_text`,
did regex-only sanitisation, and used `yaml.safe_load` without alias guards.

## Decision

Every read of repository content goes through a guarded reader
(`fsutil.read_text`) that rejects symlinks (`O_NOFOLLOW`), non-regular files,
oversized files and binary (NUL-containing) content, and refuses any path that
escapes the repository root. Text is stripped of control and bidirectional
formatting characters. YAML is parsed with a loader that forbids object
construction *and* anchors/aliases. Generated output escapes all interpolated
contributor text.

## Consequences

- Trojan-source, path-traversal, zip-bomb-style and YAML-expansion attacks are
  closed by construction and covered by tests.
- A little extra ceremony around file access, centralised in one module.
- See `docs/threat-model.md`.
