# 3. Keep resource metadata in front matter

- Status: accepted
- Date: 2026-10-04

## Context

v1 stored AI metadata in a hidden `.ingest_metadata.json` sidecar keyed by path,
and also recovered metadata from the previous `index.json`. The catalog depended
on its own prior output, metadata broke on rename, and a maintainer could not
see or fix a classification by reading the file.

## Decision

Every library document carries its metadata in YAML front matter: stable id,
category, format, language, licence, tags, summary, authors, source and
classification provenance. The catalog is a pure function of the tree.

## Consequences

- The catalog is reproducible from the library alone; no hidden state.
- Metadata survives moves and renames; a human can audit and correct one file.
- A stable, content-derived id (ADR via `ids.py`) lets downstream consumers
  reference resources across reorganisations.
- Front matter is validated strictly; an invalid block fails the policy check.
