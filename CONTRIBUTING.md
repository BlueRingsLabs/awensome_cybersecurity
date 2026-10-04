# Contributing to awesome_cybersecurity

This project is built around one principle:

> **Sharing knowledge should cost you nothing but the knowledge itself.**

You never have to learn the folder tree, pick a category, or format your notes
perfectly. You drop a Markdown file into `inbox/`; the `cyberkb` pipeline
sanitises, classifies, licence-checks and files it for you.

---

## Adding a resource (the frictionless path)

1. **Write a Markdown note.** Any structure. One resource per file. Give it a
   clear `# Title` on the first line if you can — it makes classification better.

2. **Put it in `inbox/`** through a pull request:

   ```bash
   git switch -c resource/my-note
   cp my-note.md inbox/
   git add inbox/my-note.md
   git commit -m "docs(inbox): add my note on <topic>"
   git push -u origin resource/my-note
   ```

3. **(Optional) steer the pipeline** with front matter. Valid hints win over the
   classifier; anything you omit is inferred:

   ```markdown
   ---
   title: A practical guide to Kerberoasting
   category: identity-and-access
   tags: [active-directory, credential-access]
   source_url: https://example.test/kerberoasting
   license: CC-BY-4.0
   ---

   # A practical guide to Kerberoasting
   ...
   ```

   Valid keys: `title`, `category`, `format`, `language`, `tags`, `summary`,
   `authors`, `source_url`, `license`. Categories, formats, languages and tags
   must come from [`schema/taxonomy.yaml`](schema/taxonomy.yaml).

4. **A maintainer merges.** The `Ingest and index` workflow files your note into
   `library/<category>/…` with complete front matter and regenerates the
   catalogs. Your resource appears in `index.json`, `index.yaml`, the README and
   its category page within minutes.

## Content rules (please read)

- **Licensing.** Submit **openly licensed** (Creative Commons, public domain,
  permissive) or **your own original** content. For an all-rights-reserved work,
  contribute an original summary and a link — do **not** paste the full text. The
  policy check (`cyberkb check`) blocks redistribution-restricted licences and
  flags undetermined ones for review.
- **Legal and ethical only.** No live credentials, no content whose purpose is
  to harm specific real systems or people. Defensive research, CTF material and
  responsibly disclosed PoCs with context are welcome. Payloads belong inside
  fenced code blocks.
- **Attribute sources.** Name the author, title and URL inside the note.
- **One topic per file**, so the catalog and search stay useful.
- Non-English content is welcome; language is detected automatically.

## Changing the engine, taxonomy or workflows

Development contributions follow a standard pull-request flow with
[Conventional Commits](https://www.conventionalcommits.org/) titles. Everything
CI enforces, you can run locally:

```bash
uv sync                               # set up the environment (needs uv + Python 3.12+)
uv run ruff check . && uv run ruff format --check .
uv run mypy                           # strict type-checking
uv run pytest                         # tests at 100% branch coverage (hard gate)
uv run actionlint                     # lint workflows
uv run cyberkb check                  # repository policy gate

uv run pre-commit install             # optional: run the gates on every commit
```

The taxonomy is the single source of truth in
[`schema/taxonomy.yaml`](schema/taxonomy.yaml): add a category, format or tag
there and everything downstream (classifier, catalog, schema, README) follows.
After any change that affects content or the taxonomy, run `uv run cyberkb build`
and commit the regenerated `index.json`, `index.yaml`, README block and category
pages — CI fails if they drift.

New behaviour needs tests; coverage must stay at 100%. Architectural changes
should come with (or update) an [ADR](docs/adr/).

## Commit and PR conventions

| Prefix | When |
| --- | --- |
| `docs(inbox): …` | a new raw resource in `inbox/` |
| `feat(…)` / `fix(…)` | engine, taxonomy or workflow changes |
| `chore(…)` | maintenance, dependency bumps, regenerated catalogs |

## Code of Conduct

Everyone participating is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
Report concerns to `deeprat.tec@gmail.com`.

Happy indexing.
