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
| `restricted` | all rights reserved | **do not ship**; summary + link instead |
| `unknown` | `NOASSERTION`, undetermined | ship as a curated note; confirm before commercial reuse |

`cyberkb check` fails the build on any `restricted` resource and warns on every
`NOASSERTION`.

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
