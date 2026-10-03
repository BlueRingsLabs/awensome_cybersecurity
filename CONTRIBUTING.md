# Contributing to awensome_cybersecurity

Thank you for helping build the most accessible community cybersecurity
knowledge base. This project was designed around one principle:

> **Sharing knowledge must cost you nothing but the knowledge itself.**

You never have to memorize our folder tree, choose a category, or format your
notes perfectly. You drop a raw Markdown file in the repository root; our
automated pipeline (GitHub Actions + Gemini AI) does the rest.

---

## The frictionless submission workflow

### 1. Write your note

Any Markdown content works: study notes, book summaries, tool cheat sheets,
blog archives, paper digests. No template required. One resource per file.

### 2. Upload it to the repository ROOT (`/`)

Two equivalent ways:

* **From the GitHub UI**: `Add file -> Upload files`, select your `.md`,
  create a new branch (`feature/<short-description>`), open a Pull Request
  against `main`.
* **From the CLI**:
  ```bash
  git checkout -b feature/my-new-note
  cp my-note.md .            # place it at the repository root
  git add my-note.md
  git commit -m "docs(ingest): add my new note"
  git push origin feature/my-new-note
  ```

That is all the classification you will ever have to do.

### 3. Open a Pull Request against `main`

Use [Conventional Commits](https://www.conventionalcommits.org/) titles:

| Prefix | When |
| --- | --- |
| `docs(ingest): ...` | new raw knowledge file added to `/` |
| `feat(...)` | pipeline / automation changes |
| `fix(...)` | bug fixes in scripts or workflows |
| `chore(...)` | maintenance, index regeneration, config |

### 4. A maintainer merges -- the machine takes over

On merge to `main`, the `Ingest, Classify & Index` workflow automatically:

1. **Sanitizes** your file (encoding cleanup, whitespace normalization,
   tracking-URL stripping, guaranteed H1 title).
2. **Classifies** it with Gemini 2.5 Flash into one domain
   (`01_literature`, `02_papers`, `03_web_and_posts`) and one subdomain
   (`blue_team`, `red_team`, `malware_analysis`, `reverse_engineering`,
   `threat_intelligence`).
3. **Renames** it to a clean `snake_case` filename, optionally year-prefixed.
4. **Routes** it into its final folder and **regenerates** `index.json`,
   `index.yaml` and the README Resource Index.
5. Commits everything back to `main` under the Actions bot account.

Your note appears in the catalog within minutes -- typically without a single
review comment about formatting.

---

## Content guidelines

* **Legal and ethical only.** No live exploit code targeting systems you do
  not own, no leaked credentials, no illegal content. Defensive research,
  CTF material and published PoCs with disclosure context are welcome.
* **Attribute sources.** If your note summarizes a book, paper or blog post,
  mention the author/title/URL inside the file. The pipeline preserves your
  text as-is.
* **Original or properly licensed content only** -- remember this repository
  is MIT-licensed and public.
* **One topic per file** keeps the catalog and search useful.
* Non-English content is welcome; the pipeline detects language metadata
  automatically.

---

## What the pipeline guarantees (and what it does not)

* Files that cannot be confidently classified land in
  `03_web_and_posts/unclassified/` and stay flagged in the catalog until a
  maintainer reruns classification (`workflow_dispatch` on the Actions tab).
* Filename collisions get a numeric suffix -- nothing is ever overwritten.
* If the AI service is unavailable, deterministic heuristics route the file so
  your contribution is never lost.

---

## Development contributions (scripts, workflows, schema)

Contributions to `.github/scripts/classify_and_index.py`,
`.github/scripts/build_index.py` or the CI workflow follow standard Gitflow:
feature branch, PR to `main`, Conventional Commit titles, and a description
linking the relevant issue (`Closes #N`). Run locally before pushing:

```bash
pip install google-genai pyyaml
python .github/scripts/build_index.py            # regenerate catalogs
KB_DRY_RUN=true python .github/scripts/classify_and_index.py  # test ingestion
```

---

## Code of Conduct

This project and everyone participating in it are governed by the
[Code of Conduct](CODE_OF_CONDUCT.md). Report unacceptable behavior to
`deeprat.tec@gmail.com`.

Happy indexing.
