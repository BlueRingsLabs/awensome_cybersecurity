# awesome_cybersecurity

**A curated, automatically indexed cybersecurity knowledge base — literature,
papers and web resources organised by a CyBOK- and NICE-aligned taxonomy and
published as machine-readable catalogs.**

[![CI](https://github.com/BlueRingsLabs/awesome_cybersecurity/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/BlueRingsLabs/awesome_cybersecurity/actions/workflows/ci.yml)
[![CodeQL](https://github.com/BlueRingsLabs/awesome_cybersecurity/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/BlueRingsLabs/awesome_cybersecurity/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Coverage: 100%](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](#quality-gates)

---

## What this is

A public library of cybersecurity knowledge you can both **read on GitHub** and
**consume as data**. Every resource is a Markdown document that carries its own
metadata in front matter — category, format, language, licence, tags, a stable
id — and the whole collection is published as `index.json` / `index.yaml` for
dashboards, search and agents.

Contributing is meant to cost nothing but the knowledge itself: you drop a raw
Markdown note into [`inbox/`](inbox/), and the `cyberkb` pipeline sanitises,
classifies, licence-checks and files it into the right place on merge. No one
has to learn the folder tree to share something.

> **Mission.** Be the most accessible, best-organised and most trustworthy
> community cybersecurity library — human-readable, machine-parsable, and
> defensible enough that a Tier-1 security team or an auditor can rely on it.

## How it is organised

Resources live under `library/<category>/`. The **category** is the single
primary axis and decides the folder; everything else is an orthogonal facet in
front matter. Categories are grounded in two public bodies of knowledge so the
library maps onto how the field already reasons:

- the **[CyBOK](https://www.cybok.org/) v1.1** Knowledge Areas, and
- the **[NICE Workforce Framework](https://niccs.cisa.gov/workforce-development/nice-framework)** (NIST SP 800-181r1) categories.

The taxonomy is defined once, in [`schema/taxonomy.yaml`](schema/taxonomy.yaml),
and every component — classifier, catalog, validator, these pages — reads it
from there.

| Facet | Where | Values |
| --- | --- | --- |
| **category** | folder + front matter | 18 topic categories + a staging area (see the table below) |
| **format** | front matter | book, guide, article, paper, course-notes, cheatsheet, checklist, playbook, reference |
| **language** | front matter | en, es, pt, und |
| **tags** | front matter | a controlled vocabulary (no free-form tags) |
| **licence** | front matter | SPDX id or `NOASSERTION`, with a derived `redistribution` class |

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md). The short version:

1. Add a Markdown file to [`inbox/`](inbox/) in a pull request (any name, any
   structure; one resource per file). Optionally hint `category`, `tags`,
   `source_url` or `license` in front matter — the pipeline honours valid hints.
2. A maintainer merges. The `Ingest and index` workflow files it into
   `library/<category>/…` with complete front matter and regenerates the
   catalogs.
3. Please only submit **openly licensed or original** content. For an
   all-rights-reserved work, contribute a summary and a link instead — the
   policy check blocks redistribution of restricted material.

Please also honour the [Code of Conduct](CODE_OF_CONDUCT.md).

## Programmatic access

Consume [`index.json`](index.json) / [`index.yaml`](index.yaml) directly. Each
entry has a stable `id`, `path`, `title`, `category`, `format`, `language`,
`tags`, `summary`, `authors`, `license`, `redistribution`, `word_count`,
`sha256` and a `classification` block. The schema is documented in
[`docs/catalog-schema.md`](docs/catalog-schema.md) and carried inside the
catalog itself (`schema_version`, `taxonomy`).

```bash
# Every openly redistributable red-team resource, newest first:
jq '.entries[]
    | select(.category=="offensive-security" and .redistribution=="permitted")
    | {title, path, added}' index.json
```

## The `cyberkb` engine

The pipeline is a small, dependency-light Python package ([`src/cyberkb/`](src/cyberkb/)).

```bash
uv sync                 # set up the environment
uv run cyberkb build    # regenerate catalogs, README index and category pages
uv run cyberkb check    # repository policy gate (used by CI)
uv run cyberkb ingest   # classify and file inbox/ submissions, then build
uv run cyberkb enrich   # classify pending library resources and backfill summaries
uv run cyberkb preflight   # verify every catalog model against the live APIs
uv run cyberkb classify inbox/note.md   # preview a classification, write nothing
```

LLM classification runs on **Google AI Studio** (Gemma and Gemini) and **Groq**,
both free tiers, through a per-model rotation engine. Models, their priority and
their limits are reviewed data in
[`schema/llm-models.yaml`](schema/llm-models.yaml), resolved to live API ids and
validated at run time. Every call is paced under each model's limits, and the
engine rotates on rate limits, quotas and failures. Enrichment is resumable and
commits as it goes, and every run leaves an audit report. New submissions still
fall back to a deterministic, offline heuristic, so a merge never blocks on a
provider. See [`docs/architecture.md`](docs/architecture.md) and
[ADR-0008](docs/adr/0008-google-groq-rotation.md).

## Quality gates

Every pull request must pass, and these run locally too:

| Gate | Command |
| --- | --- |
| Lint + format | `uv run ruff check . && uv run ruff format --check .` |
| Types (strict) | `uv run mypy` |
| Tests + 100% branch coverage | `uv run pytest` |
| Workflow lint | `uv run actionlint` |
| Repository policy | `uv run cyberkb check` |

Supply-chain and secret scanning (CodeQL, zizmor, gitleaks, Scorecard,
dependency review) run in [`.github/workflows/`](.github/workflows/); all
actions are pinned to commit SHAs. See
[`docs/threat-model.md`](docs/threat-model.md) and the
[Architecture Decision Records](docs/adr/).

## Repository map

```text
.
├── library/            curated resources, one folder per category  [library content]
├── inbox/              drop raw submissions here                   [contributor input]
├── schema/
│   ├── taxonomy.yaml   single source of truth for the taxonomy
│   └── catalog.schema.json  JSON Schema for index.json
├── src/cyberkb/        the ingestion / catalog / policy engine
├── tests/              100%-covered test suite
├── docs/               architecture, catalog schema, threat model, ADRs, runbooks, audit
├── index.json / .yaml  machine-readable catalogs                  [generated]
└── .github/workflows/  CI, ingestion, CodeQL, security, scorecard
```

---

## Resource index

*This section is generated by `cyberkb build`. Do not edit between the markers.*

<!-- BEGIN AUTO-INDEX -->
> Catalog regenerated **2026-10-08T00:27:58Z** | **490** resources across **18** categories. Machine-readable: [`index.json`](index.json) / [`index.yaml`](index.yaml).

| Category | Count | Most recent additions |
| --- | ---: | --- |
| [Offensive Security](library/offensive-security/README.md) | 152 | [eLearnSecurity eCPPT Notes Exam](library/offensive-security/elearnsecurity-ecppt-notes-exam.md); [eLearnSecurity Ecptxv2 Notes](library/offensive-security/elearnsecurity-ecptxv2-notes.md); [Worth checking ep.3](library/offensive-security/worth-checking-ep-3.md) |
| [Identity & Access Security](library/identity-and-access/README.md) | 7 | [The Complete Active Directory Security Handbook](library/identity-and-access/the-complete-active-directory-security-handbook.md); [Pwning the Domain Series with Credentials](library/identity-and-access/pwning-the-domain-series-with-credentials.md); [Nsa and Cisa Top 10](library/identity-and-access/nsa-and-cisa-top-10.md) |
| [Security Operations & Defense](library/security-operations/README.md) | 28 | [Windows security and privacy](library/security-operations/windows-security-and-privacy.md); [Windows Event Log Analysis IR Guide](library/security-operations/windows-event-log-analysis-ir-guide.md); [Windows Defender is enough, if you harden it](library/security-operations/windows-defender-is-enough-if-you-harden-it.md) |
| [Incident Response & Forensics](library/incident-response-and-forensics/README.md) | 12 | [Threat Hunting Playbooks](library/incident-response-and-forensics/threat-hunting-playbooks.md); [Memory Forensics](library/incident-response-and-forensics/memory-forensics.md); [Incident Response Simulation 1](library/incident-response-and-forensics/incident-response-simulation-1.md) |
| [Malware Analysis](library/malware-analysis/README.md) | 7 | [Yet Another Ridiculous Acronym](library/malware-analysis/yet-another-ridiculous-acronym.md); [Ransomware simulation](library/malware-analysis/ransomware-simulation.md); [Open Source Rats](library/malware-analysis/open-source-rats.md) |
| [Reverse Engineering & Exploit Development](library/reverse-engineering-and-exploit-development/README.md) | 22 | [eLearnSecurity Exploit Development Student Notes by Joas](library/reverse-engineering-and-exploit-development/elearnsecurity-exploit-development-student-notes-by-joas.md); [eLearnSecurity Ecxd Preparation](library/reverse-engineering-and-exploit-development/elearnsecurity-ecxd-preparation.md); [Shellcode Development 2](library/reverse-engineering-and-exploit-development/shellcode-development-2.md) |
| [Threat Intelligence & OSINT](library/threat-intelligence-and-osint/README.md) | 20 | [eLearnSecurity Certified Threat Hunting Introduction Pt 1](library/threat-intelligence-and-osint/elearnsecurity-certified-threat-hunting-introduction-pt-1.md); [Using OSINT to Investigate School Shooters](library/threat-intelligence-and-osint/using-osint-to-investigate-school-shooters.md); [Using OSINT to Investigate Human Trafficking and Missing Persons](library/threat-intelligence-and-osint/using-osint-to-investigate-human-trafficking-and-missing-persons.md) |
| [Application Security](library/application-security/README.md) | 38 | [eLearnSecurity eWPTX Notes Basic by Joas](library/application-security/elearnsecurity-ewptx-notes-basic-by-joas.md); [eLearnSecurity eWPT Notes](library/application-security/elearnsecurity-ewpt-notes.md); [eLearnSecurity Mobile Application Penetration Testing](library/application-security/elearnsecurity-mobile-application-penetration-testing.md) |
| [Cloud & Container Security](library/cloud-and-container-security/README.md) | 6 | [Understanding your EKS environment - The reconnaissance phase](library/cloud-and-container-security/understanding-your-eks-environment-the-reconnaissance-phase.md); [Microsoft 365 Security Checklist](library/cloud-and-container-security/microsoft-365-security-checklist.md); [Kubernetes Exploitation Introduction Cheatsheet](library/cloud-and-container-security/kubernetes-exploitation-introduction-cheatsheet.md) |
| [Network & Wireless Security](library/network-and-wireless-security/README.md) | 34 | [eLearnSecurity Certified Incident Response Ecir Guide Study to Exam](library/network-and-wireless-security/elearnsecurity-certified-incident-response-ecir-guide-study-to-exam.md); [Wireless Penetration Testing PMKID Attack](library/network-and-wireless-security/wireless-penetration-testing-pmkid-attack.md); [Wireless Penetration Testing Fluxion](library/network-and-wireless-security/wireless-penetration-testing-fluxion.md) |
| [IoT, OT & Hardware Security](library/iot-ot-and-hardware-security/README.md) | 4 | [Pentest IoT and OT Overview](library/iot-ot-and-hardware-security/pentest-iot-and-ot-overview.md); [IoT Use Cases and Technologies](library/iot-ot-and-hardware-security/iot-use-cases-and-technologies.md); [IoT Security Guide](library/iot-ot-and-hardware-security/iot-security-guide.md) |
| [AI Security](library/ai-security/README.md) | 9 | [The Hackers Guide to LLMs](library/ai-security/the-hackers-guide-to-llms.md); [Prompt Engineering Google](library/ai-security/prompt-engineering-google.md); [LLM AI Security and Governance Checklist](library/ai-security/llm-ai-security-and-governance-checklist.md) |
| [Cryptography, Privacy & Anonymity](library/cryptography-and-privacy/README.md) | 20 | [Xubuntu as custom Whonix workstation](library/cryptography-and-privacy/xubuntu-as-custom-whonix-workstation.md); [Whonix for KVM](library/cryptography-and-privacy/whonix-for-kvm.md); [Toryfikator](library/cryptography-and-privacy/toryfikator.md) |
| [Governance, Risk & Compliance](library/governance-risk-and-compliance/README.md) | 19 | [Zero Trust Testing Checklist](library/governance-risk-and-compliance/zero-trust-testing-checklist.md); [Understanding Data Security Risk - 2025 Survey Report](library/governance-risk-and-compliance/understanding-data-security-risk-2025-survey-report.md); [Threats and Risk Management in the Health Sector](library/governance-risk-and-compliance/threats-and-risk-management-in-the-health-sector.md) |
| [Security Awareness & Online Safety](library/security-awareness-and-online-safety/README.md) | 20 | [Top security browser plugins](library/security-awareness-and-online-safety/top-security-browser-plugins.md); [Social Engineering Practical Overview](library/security-awareness-and-online-safety/social-engineering-practical-overview.md); [Segurana Na Internet para Crianas](library/security-awareness-and-online-safety/segurana-na-internet-para-crianas.md) |
| [Careers & Certifications](library/careers-and-certifications/README.md) | 22 | [The Complete Guide for Cyber Security Career English](library/careers-and-certifications/the-complete-guide-for-cyber-security-career-english.md); [The Complete Guide for Cyber Security Career](library/careers-and-certifications/the-complete-guide-for-cyber-security-career.md); [Starting Your Cybersecurity Career - Complete Guide](library/careers-and-certifications/starting-your-cybersecurity-career-complete-guide.md) |
| [Foundations & Systems](library/foundations-and-systems/README.md) | 53 | [Your first VPS server](library/foundations-and-systems/your-first-vps-server.md); [Windows software on Linux](library/foundations-and-systems/windows-software-on-linux.md); [Windows 11 virtual machine on KVM](library/foundations-and-systems/windows-11-virtual-machine-on-kvm.md) |
| [General Technology (out of scope)](library/general-technology/README.md) | 17 | [Warez](library/general-technology/warez.md); [Small and powerful gaming PC](library/general-technology/small-and-powerful-gaming-pc.md); [Short story about my Steam Deck](library/general-technology/short-story-about-my-steam-deck.md) |
<!-- END AUTO-INDEX -->

---

## Licence

Tooling and the compilation are released under the [MIT License](LICENSE),
© 2026 Gonzalo Romero / Blue Rings Labs. **Individual resources retain their
upstream licences**, recorded per file and surfaced in the catalog
(`license` / `redistribution`); see [`NOTICE`](NOTICE).
