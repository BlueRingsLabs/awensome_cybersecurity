# Content migration and exclusions — 2026-10-04

The legacy `01_literature/ 02_papers/ 03_web_and_posts/` tree was migrated into
the `library/<category>/` layout by a deterministic, reproducible pass
(sanitise → deduplicate → classify → licence-detect → file with front matter).

- **Legacy files scanned:** 505
- **Filed as full resources:** 486
- **Re-added as reference-only entries:** 5 (all rights reserved; see below)
- **Excluded (with cause):** 14 (10 empty/broken + 4 duplicates)
- **Removed as out of scope:** 1 (`sobrevivendo-a-um-ataque-escolar.md`, personal
  physical-safety guidance, not cybersecurity)

Every decision below is deliberate and recoverable from version control; none
is a silent drop. Causes are enforced in code, not by hand: `cyberkb` rejects
empty submissions, and the policy check blocks redistribution of all-rights-
reserved works unless they are reference-only stubs under a strict word cap.

## Follow-up decision: all-rights-reserved works kept by reference (5)

Owner decision (2026-10-05): rather than drop these outright, keep each as a
**reference-only entry** (`reference_only: true`) — a title, an author credit, a
source link and a short original summary, with the full text **not** hosted. The
policy check caps a reference stub at 400 words so the work itself cannot be
smuggled in. Permission to host the full text is being sought from each author.

| Reference entry | Author / publisher | Original legacy source |
| --- | --- | --- |
| Microsoft 365 Security Checklist | Paul Schnackenburg (Hornetsecurity) | `01_literature/malware_analysis/ms365_security_checklist.md` |
| The Complete Active Directory Security Handbook | Picus Security | `01_literature/red_team/activate_directory_security_guide.md` |
| Penetration Testing Sample Report (MegaCorp One) | Offensive Security (OffSec) | `01_literature/red_team/penetration_testing_report.md` |
| Understanding Data Security Risk - 2025 Survey Report | Cloud Security Alliance | `01_literature/threat_intelligence/understanding_data_0asecurity_risk.md` |
| Starting Your Cybersecurity Career - Complete Guide | Joas A. Santos / Red Team Leaders | `02_papers/threat_intelligence/starting_your_cybersecurity_career_complete_guide.md` |

## Excluded: insufficient content (10)

These files carried no extractable prose — they are image-only PDF conversions
that produced nothing but page markers. They should be re-captured from a
text source before re-submission.

| Source | Cause |
| --- | --- |
| `01_literature/threat_intelligence/cyberwarfare_books_1.md` | insufficient content (6 words |
| `03_web_and_posts/blue_team/dicas_básicas_para_ingressar_no_mercado_de_segurança.md` | insufficient content (0 words |
| `03_web_and_posts/blue_team/email_header_analysis.md` | insufficient content (0 words |
| `03_web_and_posts/red_team/c_for_pentest.md` | insufficient content (9 words |
| `03_web_and_posts/red_team/low_cost_red_team_tools_v2.md` | insufficient content (0 words |
| `03_web_and_posts/red_team/malicious_group_c2_automation_build.md` | insufficient content (0 words |
| `03_web_and_posts/red_team/red_team_macos_att_ck_overview.md` | insufficient content (0 words |
| `03_web_and_posts/red_team/top_candc_methods.md` | insufficient content (0 words |
| `03_web_and_posts/red_team/wifi_hacking_handbook.md` | insufficient content (0 words |
| `03_web_and_posts/threat_intelligence/redes_sociais_o_lado_sombrio_do_discord.md` | insufficient content (3 words |

## Excluded: duplicate content (4)

Byte-for-byte (content-signature) duplicates of another retained resource.

| Source | Kept copy |
| --- | --- |
| `03_web_and_posts/malware_analysis/blue_team_toolkit2.md` | `03_web_and_posts/malware_analysis/blue_team_toolkit.md` |
| `03_web_and_posts/red_team/av_edr_bypass_red_team_village_pt_br_2.md` | `03_web_and_posts/red_team/av_edr_bypass_red_team_village_pt_br.md` |
| `03_web_and_posts/red_team/windows_server_and_active_directory_pentest.md` | `03_web_and_posts/red_team/windows_server_ad_and_o365_advanced_pentest.md` |
| `03_web_and_posts/reverse_engineering/introduo_a_network_security_e_firewall.md` | `03_web_and_posts/reverse_engineering/introduo_a_network_security_1_0.md` |

## Reviewed licence override

`pwning_the_domain_series_with_credentials.md` was initially flagged
"all rights reserved", but its only such notice is a quoted Windows PowerShell
console banner (`Copyright (C) Microsoft Corporation`), not the document's own
licence. It is a community-authored walkthrough and was retained with
`license: NOASSERTION`.

## Filed library — licence distribution

| Licence | Count | Redistribution |
| --- | ---: | --- |
| `NOASSERTION` | 458 | unknown |
| `CC-BY-NC-SA-4.0` | 7 | noncommercial |
| `CC-BY-4.0` | 6 | permitted |
| `CC-BY-SA-4.0` | 5 | permitted |
| `CC-BY-NC-SA-3.0` | 2 | noncommercial |
| `LicenseRef-Public-Domain` | 2 | permitted |
| `CC-BY-SA-3.0` | 2 | permitted |
| `OGL-UK-3.0` | 2 | permitted |
| `CC-BY-NC-3.0` | 1 | noncommercial |
| `GFDL-1.3-or-later` | 1 | permitted |

`NOASSERTION` means the upstream licence could not be detected automatically and
must be confirmed before any commercial reuse; see
[`content-licensing.md`](../runbooks/content-licensing.md). Non-commercial
(`CC-BY-NC*`) resources keep their upstream terms; the repository's own MIT
licence covers the tooling and the compilation, never the third-party content.

## Filed library — category distribution

| Category | Count |
| --- | ---: |
| `ai-security` | 12 |
| `application-security` | 52 |
| `careers-and-certifications` | 22 |
| `cloud-and-container-security` | 7 |
| `cryptography-and-privacy` | 22 |
| `foundations-and-systems` | 64 |
| `general-technology` | 12 |
| `governance-risk-and-compliance` | 18 |
| `identity-and-access` | 5 |
| `incident-response-and-forensics` | 12 |
| `iot-ot-and-hardware-security` | 4 |
| `malware-analysis` | 7 |
| `network-and-wireless-security` | 34 |
| `offensive-security` | 133 |
| `reverse-engineering-and-exploit-development` | 22 |
| `security-awareness-and-online-safety` | 19 |
| `security-operations` | 22 |
| `threat-intelligence-and-osint` | 18 |
| `uncategorized` | 1 |
