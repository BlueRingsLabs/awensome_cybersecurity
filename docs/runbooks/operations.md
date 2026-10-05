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
uv run cyberkb build      # just regenerate catalogs/pages from library/
uv run cyberkb check      # policy gate (what CI runs)
uv run cyberkb classify inbox/some-note.md   # preview, write nothing
```

With `GEMINI_API_KEY` set, ingestion uses the LLM; without it, the offline
heuristic. Tune with `CYBERKB_MODELS`, `CYBERKB_BATCH_SIZE`, `CYBERKB_MAX_RETRIES`,
`CYBERKB_TIMEOUT`.

## Rotating the Gemini key or model

- Key: update the `GEMINI_API_KEY` repository secret. No code change.
- Model: the default chain is newest-first in `src/cyberkb/config.py`; override
  per-run with `CYBERKB_MODELS="model-a,model-b"`. The client tries each in order
  and falls back to the heuristic if all are rejected, so a retirement never
  breaks the pipeline — but update the default when you notice a model is gone.

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
- **`GEMINI_API_KEY` secret.** Optional. Without it, ingestion uses the offline
  heuristic; with it, the Gemini classifier. Set it under
  *Settings → Secrets and variables → Actions*.
- **Disable CodeQL default setup.** Enabling GitHub Advanced Security turns on
  CodeQL *default setup*, which is mutually exclusive with this repository's
  committed, SHA-pinned advanced workflow (`.github/workflows/codeql.yml`).
  While default setup is on, GitHub rejects the advanced workflow's results and
  the *Analyze (python)* check fails with *"CodeQL analyses from advanced
  configurations cannot be processed when the default setup is enabled."* Turn
  default setup **off** under *Settings → Code security → Code scanning* so the
  advanced workflow — the version-controlled source of truth, running the
  `security-extended` suite — uploads its results. (If you would rather keep the
  zero-maintenance default setup, delete `codeql.yml` instead; the two must not
  both be active. See ADR-0006.)

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
