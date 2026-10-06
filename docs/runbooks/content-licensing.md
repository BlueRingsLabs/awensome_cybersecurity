# Content licensing runbook

The library republishes third-party material, so licence handling is a
first-class, auditable process.

## How licences are determined

On ingestion, `cyberkb` scans each document for explicit licence grants
(Creative Commons deeds and URLs, the UK Open Government Licence, the GNU FDL,
public-domain dedications) and "all rights reserved" notices, and records the
result in front matter as an SPDX-style id. The catalog derives a
`redistribution` class from it:

| Class | Meaning | Action |
| --- | --- | --- |
| `permitted` | openly redistributable | ship it |
| `noncommercial` | CC-BY-NC* — non-commercial reuse only | ship it; listed in `NOTICE` |
| `restricted` | all rights reserved | **do not host the work**; keep only a reference stub |
| `unknown` | `NOASSERTION`, undetermined | ship as a curated note; confirm before commercial reuse |

`cyberkb check` fails the build on any `restricted` resource that is not a
reference stub, and warns on every `NOASSERTION`.

## Keeping a restricted work by reference

When a work is all-rights-reserved but worth pointing to, keep a **reference
stub** instead of its text:

1. Create `library/<category>/<slug>.md` with front matter
   `reference_only: true`, `format: reference`, the real `license`
   (`LicenseRef-All-Rights-Reserved`), an `authors` credit and a `source_url`.
2. The body is your own short notice (title, what it covers, a link) — **never**
   the original text. The policy check rejects a reference stub over 400 words
   or without a `source_url`, so the work itself cannot slip in.
3. `uv run cyberkb build && uv run cyberkb check`; the entry becomes a warning
   ("included by reference only"), not an error. Record it in `NOTICE`.

## Confirming an undetermined licence

1. Open the resource and find the authoritative source (`source_url` or the
   attribution in the text).
2. Determine the real licence.
3. Set `license:` in the file's front matter to the SPDX id (or `NOASSERTION` if
   genuinely unknown and you are keeping it as a summary).
4. `uv run cyberkb build && uv run cyberkb check`; commit.

## Handling a false-positive detection

Detection is deliberately conservative: a quoted console banner (e.g. a Windows
PowerShell "Copyright (C) Microsoft Corporation. All rights reserved" line) can
trip the `restricted` heuristic even though it is not the document's own licence.
When you have reviewed and confirmed this, set the file's `license:` explicitly
(usually `NOASSERTION`) and note the review in the PR. The 2026-10-04 migration
did exactly this for `pwning-the-domain-series-with-credentials.md`.

## A rights holder asks for removal or correction

Treat it as high priority. Correct the `license`, replace the content with a
summary-plus-link, or remove the file (`docs/runbooks/operations.md` → "Removing
a resource"). Record the change in `docs/audit/` and update `NOTICE`.

## Adding restricted material the right way

Do not paste an all-rights-reserved work. Instead add an **original summary** and
a link to the source; that is openly shareable and still useful.
