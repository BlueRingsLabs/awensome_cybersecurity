---
id: ckb-ff8fff25b2c9
title: WebSurface - web attack surface discovery
category: application-security
format: article
language: en
tags: [api-security, cloud, osint, vulnerability-management, web-security]
summary: An article discussing the importance of Attack Surface Management (ASM) and the introduction of a tool called WebSurface for discovering web-based exposures.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-26b-a4b-it
  confidence: 0.9
classified_by: google:gemma-4-26b-a4b-it@2026-10-08T00:02:47Z
---

# WebSurface - web attack surface discovery

This month, I am organising my scripts for various automations, tweaking them up and sharing - maybe someone will find them useful. The impetus for this came from a project in a large organisation that had no [ASM (attack surface management)](https://www.rapid7.com/fundamentals/attack-surface-management/) tools in place. The company relied solely on a CMDB containing a list of main domains and wanted to answer some simple yet uncomfortable questions: how many domains and subdomains do they actually have? How messy are they? What lies behind the web firewall? What is exposed to the internet? And does this exposure pose any specific threats?

As is often the case, large organisations do not invest in professional tools until someone demonstrates their measurable value to them. The opposite situation also occurs: an expensive tool is purchased and implemented by an external consultant, the project is formally successful, but after handover, nobody analyses the alerts or responds to the results. Often, the problem is not a lack of technology, but a lack of process and ownership. The tool generates data, but the organisation lacks the means to translate it into real action.

This is where the concept of attack surface management comes in. ASM involves continuously identifying, taking an inventory of, and monitoring all external resources - and often internal ones as well - from an attacker’s perspective. The aim is not only to identify vulnerabilities, but also to answer the fundamental question: what does the internet see when it looks at our organisation?

![websurface](websurface.webp)

The greatest value of ASM lies not in vulnerability detection itself, but in identifying exposure. Many security incidents originate from a ‘forgotten’ admin panel, an old test server, a public cloud bucket or a host with outdated software. These aren’t sophisticated zero-day exploits; they are simply pieces of infrastructure that have slipped through organisational oversight. ASM works like radar - it detects new subdomains, changes to IP addresses, open ports, new certificates or the appearance of a resource in another cloud. This enables organisations to quickly determine whether a given exposure is justified by business needs or constitutes an unnecessary risk.

ASM is also important in a regulatory and audit context. Standards such as ISO 27001, NIS2 and SOC 2 require asset management and exposure control. However, without a technical mechanism for continuous asset identification, declarations of ‘full inventory’ often fall short of reality. ASM can provide a practical basis for maintaining up-to-date external asset records, provided the data is fed into management processes and does not remain solely within the tool.

So why does an ASM project so often end in formal success without anyone actually using it? The most common reason is the absence of operational ownership and clearly defined remediation workflow. The tool is implemented, an initial report is generated, management receives a presentation, and then responsibility for analysing alerts is not clearly assigned. Without integration with a ticketing system or a link to the CMDB, and without specific SLAs for handling detected exposures, ASM becomes just another dashboard that no one looks at after a few months. Large organisations also generate a huge number of signals, so without risk-based prioritisation and alert deduplication, the team quickly stops responding.

When implemented properly, ASM can really help with inventorying and organising the environment. It enables you to identify unused subdomains, obsolete DNS records, redundant servers and unnecessary business services. In many cases, reducing the attack surface is not about ‘patching everything’, but about deactivating what no longer exists. From an operational perspective, ASM can serve as a reliable source of information about an organisation’s external exposure and provide a foundation for infrastructure rationalisation.

However, it is important to recognise that ASM is not a one-off technology project, but an ongoing process. It requires assigned responsibilities, clear prioritisation criteria, integration with vulnerability management and a tangible impact on the activities of infrastructure and DevOps teams. Without these elements, even the best tool will only describe risk, rather than reducing it.

Sometimes, it is easiest to illustrate the scale of a problem visually. One tool that has helped me greatly in this regard is [Gowitness](https://github.com/sensepost/gowitness) – a simple yet highly effective mechanism for taking screenshots of web interfaces using headless Chrome. In practice, it enables you to swiftly ascertain an organisation’s actual exposure from the browser perspective.

When scanning domains and reviewing reports, it is easy to come across developer backends, forgotten login panels, test environments, applications with configuration errors and old system versions that are publicly available. This method is often more effective than using an Excel spreadsheet as it reveals the true extent of the chaos.

This article was originally meant to focus purely on my solution, but it naturally merged with the broader ASM discussion. In practice, the two topics are inseparable. What I wanted to demonstrate is that you can achieve meaningful visibility without million-dollar enterprise tooling. And yes – the same pipeline works extremely well in bounty hunting, where we often look for low-hanging fruits. Usually, the tastiest ones.

In the project I mentioned earlier, however, simply generating screenshots was not enough. I needed a process that would:

- discover subdomains,
- resolve them to IP addresses,
- distinguish CDN/WAF infrastructure from potential backends,
- indicate possible exposure of origins,
- scan them for open ports and services,
- and finally enable a quick visual overview.

This is how [WebSurface](https://github.com/h0ek/WebSurface) was created – a script that combines existing, proven tools into a single pipeline and automates the entire process of discovery and triage of origin exposure (Cloudflare/CDN-aware).

WebSurface does not attempt to reinvent the wheel. It uses mature open-source projects, such as [subfinder](https://github.com/projectdiscovery/subfinder), [dnsx](https://github.com/projectdiscovery/dnsx), [httpx](https://github.com/projectdiscovery/httpx), [naabu](https://github.com/projectdiscovery/naabu), [nmap](https://github.com/nmap/nmap), and [gowitness](https://github.com/sensepost/gowitness) and combines them into a logical sequence of actions. It starts with passive subdomain discovery, then resolves A/AAAA records, classifies addresses in terms of their belonging to Cloudflare ranges, performs HTTP/HTTPS probing with enrichment (status, title, IP, CNAME, CDN signals), and then selectively chooses candidates for potential origins.

Not every IP address is a candidate. Only those that:

- are web-alive,
- do not belong to CDN ranges,
- do not have “cdnish” infrastructure characteristics (based on flags, CNAME, fingerprints) are considered.

Only on this selected list is the next stage performed: scanning top ports (excluding 80/443), fingerprinting services using Nmap, and generating screenshots for visual triage. Each run creates a separate directory with results – from raw data to a summary report and an SQLite database from gowitness.

The key point in this approach is that WebSurface is not just another “vulnerability scanner.” It is a tool for a structured view of the attack surface and potential exposure of backends. It provides a quick overview: which IPs actually look like real origins, which ports are open, and whether services and certificates indicate a connection to a public service.

In practice, this allows us to answer the question of whether there is actually infrastructure hidden behind the CDN or whether there is a direct path to the backend. At the same time, it is important to remember that CDN detection is based on heuristics and each result requires manual verification – the tool indicates signals, but does not replace analysis.

For me, it was a way to show the organization in a very tangible way what their real exposure looks like. Instead of an abstract discussion about the “attack surface,” you could open the report, see specific IPs, ports, and screenshots of panels. Often, it is only such an image that triggers real action.

In this sense, WebSurface is a practical complement to the ASM concept - not as a large, corporate product, but as a technical pipeline that allows you to quickly inventory, visualize, and organize what is actually exposed to the world.

To illustrate the scale of the problem, I ran a full scan on a list of 1,992 domains from the CMDB. The result was more telling than any PowerPoint presentation.

From less than two thousand input domains, the pipeline generated over 8,000 unique hosts. Nearly 7,000 of them resolved to IP addresses. After HTTP verification, it turned out that over 3,000 URLs corresponded publicly. After filtering out the CDN infrastructure and applying restrictive “origin candidate” selection criteria, 97 IPv4 and 18 IPv6 addresses remained that looked like real backends, unprotected by Cloudflare or other CDNs.

The next stage revealed 189 open endpoints (IP:PORT) at these addresses. Nmap performed an in-depth analysis of 44 unique IPs that actually had open ports after filtering out 80/443. The whole process took less than four hours.

However, what was most important was not the numbers themselves, but the quality of the findings. The results included:

- publicly available developer backends,
- administration panels with default or weak passwords,
- test environments with active forms,
- outdated services with publicly known vulnerabilities,
- API endpoints that should never be exposed directly,
- systems bypassing CDN and visible at the origin address.

The report did not surprise only the IT team. It surprised regional managers, domain administrators, and business application owners. Many of them were unaware of what was actually hidden behind “their” domains. It turned out that the problem was not a single configuration error, but systemic lack of attack surface ownership.

It is in moments like these that the practical value of ASM becomes apparent—not as a marketing slogan, but as a tool for confronting the reality of an organization. Data from the pipeline became the starting point for:

- reviewing and cleaning up DNS,
- disabling unused services,
- introducing strict rules for publishing resources,
- defining responsibility for domains and subdomains,
- implementing cyclical monitoring.

The most important thing, however, was that the conversation ceased to be theoretical. Instead of general statements about “too large an attack surface,” specific IP addresses, specific ports, and specific screenshots of login panels appeared.

And that is precisely what a technical approach to ASM is all about – not generating noise, but providing evidence that triggers real corrective action.

The most interesting part was not that something was exposed. The interesting part was that nobody knew it was.

Finding things is the easy part. The real challenge begins afterwards - analysing the results, validating exposure, understanding context and separating noise from actual risk. That phase always takes the longest and requires the most focus. This time I tried to approach the topic on my blog a bit more professionally than usual - which does not mean I’m suddenly becoming formal and stiff. Don’t worry, I’ll still keep it my way next time.

I’m also experimenting with automating parts of my writing workflow. Let’s just say this article is part of that experiment. But don’t worry - there’s a limit to automation. Some things still require manual analysis, real thinking, and a bit of human chaos.
