---
id: ckb-13ca6fb3c5de
title: Threat Modeling in Modern Security Programs
category: governance-risk-and-compliance
format: article
language: en
tags: [mitre-attack, nist, owasp, risk-management, threat-intelligence, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.68
---

# Threat Modeling in Modern Security Programs

I created this based on various internet sources for a company that is planning to carry out threat modelling. It is a general outline and preliminary proposal that you can adapt to your needs. Hopefully someone will find it useful.

Experts in this field may be able to provide more information, but it seems to me that this is not yet a popular solution among smaller companies or those with a young security posture. In my experience, most people mainly have it on paper and do not use it in practice.

As with most security-related projects, I strongly encourage you to develop a process, implement it, and then refine it, ensuring that threat models are up to date and tailored to your company and the threats you face. Once it is working effectively, implement it as standard practice.

I encourage you to read the sources on which this text is based, which can be found in point 8.

Everything is written from the perspective of a Red Teamer, Pentester and Vulnerability Manager, showing where these teams, which are close to my heart, should be placed in the process.

Please let me know if you would like to see more articles on professional work from the cybersecurity department on the blog.

Enjoy reading.

![Threat Modeling](threatmodeling.webp)

## Threat Modeling in Modern Security Programs

### 1. Definition & Purpose

> **Threat Modeling** is a **systematic analysis of a system, application, or service** to:

1. Identify what we protect (**assets**).
2. Understand potential **threat actors** (attackers), their motivation and capabilities.
3. Analyze **attack vectors** and misuse scenarios (e.g., STRIDE categories, MITRE ATT&CK techniques).
4. Assess **business, technical, and operational impact**.
5. Define or improve **security controls** to reduce risk and strengthen resilience.

It complements but is **not the same as** penetration testing or vulnerability scanning. It focuses on **design-time risk** and drives secure architecture and development choices.

---

### 2. Key Principles (from Threat Modeling Manifesto)

#### Values

| We Value… | Over… |
| --- | --- |
| **A** **culture of finding and fixing design issues early** | Checkbox-style compliance |
| **People and collaboration** | Processes, methodologies, and tools alone |
| **A** **journey of continuous understanding** | A one-time “security snapshot” |
| **Doing threat modeling in practice** | Merely talking about threat modeling |
| **Continuous refinement and iteration** | A single, final delivery |

#### Principles

| Principle | Explanation |
| --- | --- |
| **Early and frequent analysis** | Best use of threat modeling is to improve security & privacy by doing it early in design and repeating as the system evolves. |
| **Align with development practices SDLC** | Must integrate with how the organization builds software / systems, not be an isolated exercise. |
| **Scoped and iterative** | Follow design changes in manageable increments rather than huge one-off efforts. |
| **Value-driven outcomes** | Results are meaningful only when they deliver value to stakeholders. |
| **Dialogue over documents** | Collaboration builds common understanding; documents record and support measurement. |

### 3. Common Methods & Tools

- **STRIDE** (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) – Microsoft.
- **DREAD** (Damage, Reproducibility, Exploitability, Affected users, Discoverability) – risk scoring.
- **PASTA** (Process for Attack Simulation and Threat Analysis) – 7-stage, risk-centric methodology.
- **OCTAVE** (Operationally Critical Threat, Asset, and Vulnerability Evaluation) – focuses on organizational risk.
- **Attack Trees** – hierarchical attack scenario diagrams.
- **DFDs (Data Flow Diagrams)** and **Trust Boundary Analysis** – core techniques for visualizing assets and exposure.

Typical tools:

- [Microsoft Threat Modeling Tool](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool)
- [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/)
- [IriusRisk](https://www.iriusrisk.com/) (commercial)

---

### 4. Where Threat Modeling Fits

- **Primarily at the project/system level:** performed during **design/architecture phase** of each new product, service, or major change.
- **Also at enterprise level:** for major technology domains (e.g., cloud platform, API ecosystem, supply chain).
- **Lifecycle:** repeated as part of change management and SDLC (Software Development Life Cycle) – e.g., after major releases, architecture refactors, new integration points.

---

## 5. Roles and Responsibilities

> **Ownership typically lies with Security Architecture / Application Security teams.** Other teams provide data, context, and validation.

| Function | Responsibilities in TM |
| --- | --- |
| **Security Architecture / AppSec (primary owners)** | • Facilitate & lead TM workshops • Choose methodology (DFD, STRIDE, PASTA, etc.) • Maintain TM repository • Coordinate updates during design changes |
| **Product / Development / IT Owners** | • Provide system knowledge, architecture diagrams, data flows • Implement mitigations defined from TM |
| **Offensive Security (Red Team / Pen Test)** | • Advise on realistic attack paths (aligned to MITRE ATT&CK) • Validate that modeled threats are realistic • Test effectiveness of selected mitigations |
| **Vulnerability Management (VM)** | • Map modeled threats to actual vulnerabilities and exposures in production • Prioritize remediation efforts • Feed real-world findings back into TM |
| **Cyber Threat Intelligence (CTI)** | • Supply up-to-date threat actor profiles, Tactics/Techniques/Procedures (TTPs), sector-specific intel • Help assess likelihood of threats |
| **Security Advisory / GRC / Risk Management** | • Use TM results for compliance mapping and risk registers • Ensure business accepts and manages residual risk |
| **Operations / SOC (Blue Team)** | • Use TM outputs to prioritize detections, logging, response playbooks |
| **Business / Product Management** | • Provide input on most critical assets & business impact |
| **Security Champions (within dev/IT)** | • Act as local liaisons, ensuring TM guidance is understood and applied in engineering teams |

**Important:**

- **Red Team / Pentesters and VM are *contributors*, not owners.**
- They bring **realistic attacker perspective** and **operational feedback**, but TM is primarily a **design-phase exercise** led by architecture/AppSec.

---

## 6. Example Process Flow (Best Practice)

```plaintext
[1] Initiate TM
      - Security Architect / AppSec lead
      - Product Owner, Project Manager

[2] Scope & Identify Assets
      - Product & Dev teams provide business context
      - CTI supplies threat landscape

[3] Diagram the System (DFD, Trust Boundaries)
      - Architect & Devs create and review diagrams

[4] Identify Threats
      - AppSec facilitates
      - CTI supplies attacker perspective
      - OffSec contributes attack vectors

[5] Assess & Prioritize Risks
      - AppSec + Risk/GRC + Business impact assessment

[6] Define & Track Mitigations
      - Dev teams implement
      - VM maps to existing exposures

[7] Validate & Test
      - Red Team / Pentesters verify real-world exploitability
      - SOC tunes detection / response

[8] Maintain & Update
      - AppSec / Architect own the TM repository
      - CTI & VM feed new intelligence and exposures
```

---

## 7. Recommended Best Practices

- Integrate TM into **SDLC** (e.g., at design gates, major architectural change, and release retrospectives).
- Maintain a **central TM repository** (linked to issue tracker/backlog for traceability).
- Include **Security Champions** in dev/IT for smoother collaboration.
- Involve **CTI early** to prioritize realistic threats.
- Use **Red Team / Pentest for validation** – don’t confuse it with owning the process.
- Provide **management visibility**: TM reduces late-stage defects, saves remediation cost, and improves compliance & resilience.

---

## 8. Authoritative Sources

- [OWASP Threat Modeling Project](https://owasp.org/www-project-threat-model/)
- [OWASP Threat Modeling Process](https://owasp.org/www-community/Threat_Modeling_Process)
- [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/)
- [Microsoft Security Development Lifecycle (SDL) – Threat Modeling](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
- [NIST SP 800-154 – Guide to Data-Centric System Threat Modeling](https://csrc.nist.gov/pubs/sp/800/154/ipd)
- [MITRE ATT&CK Framework – mapping threats to adversary TTPs.](https://attack.mitre.org/)

---

## Key Takeaways for Organizational Discussion

- Threat Modeling is **primarily a design-time activity**; it informs architecture and control selection.
- **Owner:** Security Architecture / AppSec.
- **Offensive Security & VM:** crucial advisors and validators.
- **CTI:** brings context for likelihood and relevance of threats.
- TM is done **per project/system** and **revisited throughout its lifecycle**, and can be done at **enterprise level** for strategic domains.
- Align TM with **SDLC** and feed results into **risk management and defensive operations**.
