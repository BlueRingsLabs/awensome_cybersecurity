# BlueRingsLabs / awensome_cybersecurity

**An open, curated and fully automated cybersecurity knowledge base.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ingest, Classify & Index](https://github.com/BlueRingsLabs/awensome_cybersecurity/actions/workflows/ingest_and_index.yml/badge.svg?branch=main)](https://github.com/BlueRingsLabs/awensome_cybersecurity/actions/workflows/ingest_and_index.yml)

---

## Mission

BlueRingsLabs builds and maintains a public repository of cybersecurity
knowledge -- literature, research papers and web resources -- organized by
threat subdomain (blue team, red team, malware analysis, reverse engineering
and threat intelligence).

Our core value proposition is a **frictionless contribution workflow**: no one
should have to learn our directory tree to share knowledge. Contributors drop
raw Markdown notes anywhere in the repository root; an automated CI/CD
pipeline (GitHub Actions + Gemini AI) sanitizes, classifies, renames, routes
and indexes every submission the moment it is merged into `main`.

**Vision**: become the most accessible, best-organized community security
library -- human-readable on GitHub, machine-parsable via API-friendly
catalogs (`index.json` / `index.yaml`).

---

## Repository map

```text
.
├── README.md               <- you are here (index block auto-updated by CI)
├── LICENSE                 <- MIT, Blue Rings Labs (2026)
├── CONTRIBUTING.md         <- frictionless /root submission workflow
├── CODE_OF_CONDUCT.md      <- Contributor Covenant, contact: deeprat.tec@gmail.com
├── index.json              <- machine-readable catalog (schema v1)   [auto]
├── index.yaml              <- machine-readable catalog (YAML form)   [auto]
│
├── 01_literature/          <- books, summaries, theoretical notes
│   ├── blue_team/
│   ├── red_team/
│   ├── malware_analysis/
│   ├── reverse_engineering/
│   └── threat_intelligence/
├── 02_papers/              <- technical papers and whitepapers
│   └── (same five subdomains)
├── 03_web_and_posts/       <- articles, blog posts, web resources
│   └── (five subdomains + unclassified/ staging area)
│
└── .github/
    ├── scripts/
    │   ├── classify_and_index.py   <- AI ingestion pipeline (Gemini 2.5 Flash)
    │   └── build_index.py          <- deterministic catalog generator
    └── workflows/
        └── ingest_and_index.yml    <- CI/CD triggered on push to main
```

| Axis | Values | Meaning |
| --- | --- | --- |
| **Domain** (top level) | `01_literature`, `02_papers`, `03_web_and_posts` | Resource type / depth |
| **Subdomain** | `blue_team`, `red_team`, `malware_analysis`, `reverse_engineering`, `threat_intelligence`, `unclassified` | Threat topic |

---

## How automation works

```text
Contributor PR (raw .md in /)  ->  Merge to main  ->  GitHub Actions
        -> Gemini 2.5 Flash classification (batched, rate-limited, retried)
        -> Sanitization + snake_case renaming + routing to domain/subdomain
        -> Regeneration of index.json, index.yaml and this AUTO-INDEX block
        -> Bot commit back to main
```

* Structured JSON output guarantees only valid taxonomy destinations.
* Batch processing (12 files per request) with client-side pacing respects the
  Google AI Studio free tier (15 requests/minute); HTTP 429 triggers
  exponential backoff with jitter.
* If the model is unavailable, deterministic keyword heuristics route files so
  the pipeline never blocks a merge.

---

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md). The short version:

1. Create your raw Markdown note (any format, any name).
2. Add it to the **repository root** `/` through a Pull Request.
3. A maintainer merges. Done -- the pipeline does the rest.

Please also honor [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
(contact: `deeprat.tec@gmail.com`).

---

## Programmatic access

Every resource is described in [`index.json`](index.json) /
[`index.yaml`](index.yaml) with a stable `id`, `path`, `title`, `domain`,
`subdomain`, `tags`, `language`, `summary` and classification `confidence`.
Consume them from scripts, dashboards or your own agents -- they are
regenerated atomically on every pipeline run.

---

## Resource Index

*This section is managed automatically by the CI/CD pipeline. Do not edit
between the markers.*

<!-- BEGIN AUTO-INDEX -->
> Catalog regenerated: **2026-10-04T00:40:26Z** | **505 resources** indexed. Machine-readable catalogs: [`index.json`](index.json) / [`index.yaml`](index.yaml).

### 01_literature -- Literature (291 resources)

| Subdomain | Count | Highlights |
| --- | ---: | --- |
| `blue_team` | 42 | [Send emails by local applications only](01_literature/blue_team/2018_send-emails-by-local-applications-only.md); [Pentest of an FTP Server](01_literature/blue_team/2019_ftp-testing.md); [Top security browser plugins](01_literature/blue_team/2020_top-security-browser-plugins.md) · [+39 more](/01_literature/blue_team/) |
| `red_team` | 54 | [Website analysis](01_literature/red_team/2019_website-analysis.md); [I am not that hacker you are looking for](01_literature/red_team/2022_i-am-not.md); [Let's hack some SMB](01_literature/red_team/2022_smb-hacking.md) · [+51 more](/01_literature/red_team/) |
| `malware_analysis` | 29 | [100 Security Operation Center Tools](01_literature/malware_analysis/100_security_operation_center_tools.md); [Malware analysis](01_literature/malware_analysis/2019_malware-analysis.md); [8BitDo gamepads](01_literature/malware_analysis/2020_8bitdo-gamepads.md) · [+26 more](/01_literature/malware_analysis/) |
| `reverse_engineering` | 20 | [Easy GPG](01_literature/reverse_engineering/2019_easy-gpg.md); [Windows post-exploitation](01_literature/reverse_engineering/2019_windows-post-exploitation.md); [Miyoo Mini Plus](01_literature/reverse_engineering/2023_miyoo-mini-plus.md) · [+17 more](/01_literature/reverse_engineering/) |
| `threat_intelligence` | 146 | [Debian LEMP stack](01_literature/threat_intelligence/2018_debian-lemp-stack.md); [MD5 calculator in powershell](01_literature/threat_intelligence/2018_md5-calculator-in-powershell.md); [PortSentry - stealth scan detection](01_literature/threat_intelligence/2018_portsentry-stealth-scan-detection.md) · [+143 more](/01_literature/threat_intelligence/) |

### 02_papers -- Papers (41 resources)

| Subdomain | Count | Highlights |
| --- | ---: | --- |
| `blue_team` | 12 | [Security Roadmap](02_papers/blue_team/2022_security-roadmap.md); [Cyber Security Career In 2024](02_papers/blue_team/cyber_security_career_in_2024.md); [Cyberbullying And Its Consequences](02_papers/blue_team/cyberbullying_and_its_consequences.md) · [+9 more](/02_papers/blue_team/) |
| `red_team` | 6 | [CVE-2021-4034 - gimme root](02_papers/red_team/2022_cve-2021-4034.md); [30 Days Of Practice Pentest 2](02_papers/red_team/30_days_of_practice_pentest_2.md); [Adversary Emulation Matrix By Joas](02_papers/red_team/adversary_emulation_matrix_by_joas.md) · [+3 more](/02_papers/red_team/) |
| `malware_analysis` | 4 | [Cybersec Certifications 2023](02_papers/malware_analysis/cybersec_certifications_2023.md); [Malware And Reverse Engineering Complete Collect](02_papers/malware_analysis/malware_and_reverse_engineering_complete_collection_by_joas.md); [Python Libs For Security Pt 1](02_papers/malware_analysis/python_libs_for_security_pt_1.md) · [+1 more](/02_papers/malware_analysis/) |
| `reverse_engineering` | 2 | [Chatgpt For Cybersecurity 3](02_papers/reverse_engineering/chatgpt_for_cybersecurity_3.md); [Offensive Security Mac Control Bypass Notes Pt 1](02_papers/reverse_engineering/offensive_security_mac_control_bypass_notes_pt_1.md) |
| `threat_intelligence` | 17 | [100 Free Security Tools](02_papers/threat_intelligence/100_free_security_tools.md); [12 Best Career In Cyber Security 2023](02_papers/threat_intelligence/12_best_career_in_cyber_security_2023.md); [title inside <title>](02_papers/threat_intelligence/2018_devices-search.md) · [+14 more](/02_papers/threat_intelligence/) |

### 03_web_and_posts -- Web & Posts (173 resources)

| Subdomain | Count | Highlights |
| --- | ---: | --- |
| `blue_team` | 39 | [Safe social networking](03_web_and_posts/blue_team/2018_safe-social-networking.md); [Secure email services](03_web_and_posts/blue_team/2018_secure-email-services.md); [AbuseIPDB with Fail2Ban](03_web_and_posts/blue_team/2019_abuseipdb.md) · [+36 more](/03_web_and_posts/blue_team/) |
| `red_team` | 66 | [Ethical Hacking - How to start](03_web_and_posts/red_team/2019_ethical-hacking.md); [Runas in Powershell for Windows 10](03_web_and_posts/red_team/2019_runas-powershell.md); [CVE attack](03_web_and_posts/red_team/2021_cve-attack.md) · [+63 more](/03_web_and_posts/red_team/) |
| `malware_analysis` | 13 | [Open Source Rats](03_web_and_posts/malware_analysis/2020_opensource-rats.md); [Hacker news](03_web_and_posts/malware_analysis/2021_hacker-news.md); [Scan a single IP](03_web_and_posts/malware_analysis/blue_team_toolkit.md) · [+10 more](/03_web_and_posts/malware_analysis/) |
| `reverse_engineering` | 15 | [Black Friday - Cyber Monday](03_web_and_posts/reverse_engineering/2021_black-friday.md); [SMTP Hack](03_web_and_posts/reverse_engineering/2024_smtp-hack.md); [Carreira Em Desenvolvimento Mobile](03_web_and_posts/reverse_engineering/carreira_em_desenvolvimento_mobile.md) · [+12 more](/03_web_and_posts/reverse_engineering/) |
| `threat_intelligence` | 39 | [19 Joassantos Gerenciando Sua Superficie De Ataq](03_web_and_posts/threat_intelligence/19_joassantos_gerenciando_sua_superficie_de_ataques.md); [Fail2Ban - best jail](03_web_and_posts/threat_intelligence/2018_fail2ban-best-jail.md); [Let’s Encrypt SSL Cert for Nginx](03_web_and_posts/threat_intelligence/2018_lets-encrypt-ssl-cert-for-nginx.md) · [+36 more](/03_web_and_posts/threat_intelligence/) |
| `unclassified` | 1 | [Mining cryptocurrency - don't do it at home](03_web_and_posts/unclassified/2023_minig-cryptocurrency.md) |

_Note: 1 resource(s) are pending automated classification and will be routed by the next pipeline run._
<!-- END AUTO-INDEX -->

---

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Blue Rings Labs.
