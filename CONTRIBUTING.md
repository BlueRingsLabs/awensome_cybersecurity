# 🤝 Contributing to awensome_cybersecurity

First off — **thank you**! This knowledge base only exists because practitioners like you share what they learn.
We designed the contribution flow around one principle:

> **You write. The pipeline organizes.**

No folder trees to memorize, no naming conventions, no index files to touch. Ever.

---

## ⚡ The 60-second workflow (recommended)

1. **Drop your raw file into the repository root (`/`)** — a Markdown note, literature summary,
   cheat sheet or reference export. GitHub UI: *Add file → Upload files* on a new branch, or add it
   in your fork/clone.
2. **Open a Pull Request against `main`.** Title it freely (`docs: <your topic>` is nice but not required).
3. **Done.** On merge, our CI/CD pipeline automatically:
   - 🧹 **Sanitizes** the file (UTF-8 normalization, HTML comment & tracking-parameter scrubbing, whitespace cleanup),
   - 🤖 **Classifies** it with Gemini 2.5 Flash into the right domain/subdomain
     (`01_literature`, `02_papers`, `03_web_and_posts` × `blue_team`, `red_team`, `malware_analysis`,
     `reverse_engineering`, `threat_intelligence`),
   - 📁 **Moves & renames** it to `domain/subdomain/<YYYY>_<clean-slug>.md`,
   - 🏷️ **Injects YAML front-matter** (title, tags, description, classifier confidence) for auditability,
   - 📑 **Regenerates** [`README.md`](README.md)'s resource table plus [`index.json`](index.json) and [`index.yaml`](index.yaml).

If the AI can't confidently classify your file, it lands in `unclassified/` for maintainer review —
it will **never** be rejected or lost.

### What counts as a good submission?

| ✅ Encouraged | ❌ Please avoid |
| :------------ | :-------------- |
| Your own notes, summaries & study material | Copyrighted books/PDFs you don't have rights to share |
| Links + commentary on public resources | Malicious payloads hosted as "documentation" (code fences for defense research are fine) |
| Cheat sheets, tool guides, IR playbooks | Pure spam / marketing brochures |
| Papers & whitepapers you authored or that are openly licensed | Binary-only uploads without context (we index Markdown/text) |

---

## 🌿 Gitflow for larger changes

The root-drop flow above covers ~95% of contributions. For structural changes (schema edits,
pipeline logic, taxonomy updates) we follow strict Gitflow:

```bash
git checkout -b feature/issue-6-json-yaml-indexes   # feature/* branches only
# … atomic commits, Conventional Commits …
git commit -m "feat(index): add language detection to catalog schema"
git push origin feature/issue-6-json-yaml-indexes    # then open a PR → main
```

Commit types: `feat(...)`, `fix(...)`, `docs(...)`, `chore(...)`, `refactor(...)`, `ci(...)`.
Keep each PR focused on **one task** from the
[Cybersecurity Knowledge Base Roadmap](https://github.com/orgs/BlueRingsLabs/projects) Kanban board.

> ⚠️ Never hand-edit the generated blocks: the README table between the
> `<!-- AUTO-INDEX:START/END -->` markers, `index.json`, or `index.yaml`.
> They are overwritten by the pipeline on every merge. To change them, change the
> content or the scripts under `.github/scripts/`.

---

## 🧪 Testing locally

Want to preview what the bot will do to your file before opening the PR?

```bash
pip install -r .github/scripts/requirements-pipeline.txt

# Dry-run the whole ingestion (offline heuristic — no API key needed):
python3 .github/scripts/classify_and_index.py --offline --dry-run

# Or regenerate the catalogs yourself:
python3 .github/scripts/generate_catalog.py
python3 .github/scripts/generate_catalog.py --check   # CI-style drift gate
```

With a Google AI Studio key you can test real classification:

```bash
export GEMINI_API_KEY="your-key"
python3 .github/scripts/classify_and_index.py --verbose
```

---

## 🗺️ Taxonomy cheat-sheet (FYI only — the bot handles this!)

| Domain | Contents |
| :----- | :------- |
| `01_literature` | Books, long-form summaries, theoretical/certification study notes |
| `02_papers` | Research papers, whitepapers, formal reports & frameworks |
| `03_web_and_posts` | Blog posts, articles, quick guides, cheat sheets, tool write-ups |

| Subdomain | Focus |
| :-------- | :---- |
| `blue_team` | Defense, detection & response, SOC/SIEM, hardening, GRC |
| `red_team` | Pentesting, adversary emulation, privilege escalation, bug bounty |
| `malware_analysis` | Malware research, ransomware, DFIR, YARA, sandboxing |
| `reverse_engineering` | Binary RE, exploit development, shellcode, buffer overflows |
| `threat_intelligence` | OSINT, CTI, threat hunting, APT profiling, ATT&CK |

---

## 📜 Governance

- By contributing you confirm you have the right to share the material under the
  [MIT License](LICENSE).
- All participants agree to the [Code of Conduct](CODE_OF_CONDUCT.md)
  (Contributor Covenant 2.1, contact: `deeprat.tec@gmail.com`).
- Maintainers triage new PRs weekly; merged = published within minutes thanks to automation.

Happy hacking, and welcome to **BlueRingsLabs**. 🛡️
