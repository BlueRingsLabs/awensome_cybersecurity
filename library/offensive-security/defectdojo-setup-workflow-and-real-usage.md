---
id: ckb-c9479d64c5e5
title: DefectDojo – Setup, Workflow and Real Usage
category: offensive-security
format: article
language: en
tags: [bash, containers, fuzzing, nmap, tls, vulnerability-management]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.48
---

# DefectDojo – Setup, Workflow and Real Usage

I was looking for something to keep findings, scan results, and reports in one place instead of dumping everything into a notebook. For pure bug bounty work, I still think a normal notes app such as [Obsidian](https://obsidian.md/) is often enough. It is faster for testing, writing down ideas, storing screenshots, and preparing a quick report. I do not like wasting time on endless clicking, reporting workflows, and management-style dashboards when I am hunting alone.

That said, in a company environment the situation is different. There you usually need documentation, historical tracking, imported scan results, comparisons over time, dashboards, charts, status colors, and the ability to come back to something years later. In that context, [DefectDojo](https://defectdojo.com/) looks like a much better fit.

This is also why it helps to be precise about what DefectDojo actually is. It is much closer to a vulnerability management and scan aggregation platform than to a classic pentest project manager. DefectDojo is also described by its maintainers as an ASPM (Application Security Posture Management) platform, which fits the general idea of centralizing findings from multiple security tools and tracking them over time. In other words, it makes more sense as a central place for imported findings, triage, deduplication, tracking, and long-term evidence retention than as a full replacement for note-taking during hands-on testing.

This aligns with how the project itself is described by OWASP. DefectDojo is designed as a platform for orchestrating end-to-end security testing, vulnerability tracking, deduplication, remediation, and reporting, while aggregating data from many different security tools into a single place.

In practice, this means it works best as a central system for collecting and managing results over time rather than as a tool for conducting the tests themselves.

![defectdojo](defetdojo.webp)

At the time of writing, I am not using it heavily yet, only in a small lab at home, before proposing it as an improvement to management. I set it up, tested it, reviewed the workflow, and compared it with other platforms I had already evaluated, including [Dradis](https://dradisframework.com/reporting.html), [Faraday IDE](https://faradaysec.com/penetration-testing-reporting/), [Pentest Collaboration Framework](https://gitlab.com/invuls/pentest-projects/pcf), [ReconMap](https://reconmap.com/), [Reporter](https://securityreporter.app/), [PeTeReport](https://github.com/1modm/petereport), [WriteHat](https://github.com/blacklanternsecurity/writehat), and [PlexTrac](https://plextrac.com/platform/reports/). Most free editions of competing products feel too limited, some tools feel more like hobby projects than professional platforms, and in many cases something important is always missing. Paid versions are probably much better and often integrate a lot more, but if the main goal is importing scans, tracking findings, and keeping reports organized, DefectDojo looks like one of the strongest options. So this article is more about initial setup, workflow, and why the platform looks promising in practice than about years of production use.

It is not a lightweight toy. It is a fairly large platform, and you need to learn how to use it properly. But after getting familiar with Products, Engagements, findings, imports, and deduplication, it looks like something that can organize long-term results very well.

While writing this article I also came across [OWASP Cervantes](https://owasp.org/www-project-cervantes/), which looks closer to a pentest and engagement management platform with reporting workflow. I still need to test it properly, so I am not drawing final conclusions yet, but it may turn out to be a better fit for teams that care more about managing projects and writing client-facing pentest reports than about aggregating scanner output. I am waiting for a newer release before judging it more seriously, especially since the last version I saw was still marked as beta.

In the past I wrote an article [Penetration test report template](../../../../2023/01/29/pentest-report-template/index.html) (which I should update), so take a look — it might be useful too. I am trying to find a place for all outputs from various tools like [Practical Recon Automation with ReconFTW](../../../02/08/reconftw/index.html) and [ScopeWise - Yet Another Recon Script](../../../02/17/sopewise/index.html), that is why I wrote today’s article.

# Why this one looks more practical than many alternatives

One thing that matters here is category. Some tools focus on pentest project management and reporting workflow, while others focus on vulnerability management, scanner imports, deduplication, and long-term tracking. DefectDojo clearly belongs much more to the second group.

For me the main point is not replacing actual testing. It is having a place where imported scan results and validated findings can live in a structured way.

The free edition already gives quite a lot:

- core finding import and deduplication
- authentication
- role-based access control
- REST API and Swagger UI
- manual import and reimport
- basic dashboard and reporting

The Pro version adds things like rules engine automation, tunable deduplication, background imports, CLI and integrations, universal parsing, MFA, more advanced dashboards, hosted options, and broader enterprise features. So the free version is actually usable instead of being reduced to a demo. That is one of the reasons it stands out more than a lot of competing tools.

Another strong point is parser coverage. DefectDojo supports a very large number of report types, so you can realistically import outputs from many scanners instead of manually pasting everything into random notes.

## DefectDojo on Fedora 43 with Podman

Requirements

```bash
sudo dnf install -y podman podman-compose git python3
```

Create a directory for the stack

```bash
mkdir -p ~/Containers/defectdojo
cd ~/Containers/defectdojo
```

Clone DefectDojo from GitHub

```bash
git clone https://github.com/DefectDojo/django-DefectDojo.git .
```

Create the `.env` file. In my case, the repository did not include `.env.dist`, so I created `.env` manually:

```bash
cd ~/Containers/defectdojo
nano .env
```

Paste at least this minimum configuration:

```bash
DD_DEBUG=False
DD_ALLOWED_HOSTS=localhost,127.0.0.1
DD_CSRF_TRUSTED_ORIGINS=http://localhost:8080

DD_SECRET_KEY=CHANGE_ME_SUPER_LONG_RANDOM_SECRET

POSTGRES_USER=defectdojo
POSTGRES_PASSWORD=defectdojoStrongPass1234!
POSTGRES_DB=defectdojo
```

Generate a proper secret:

```bash
python3 -c 'import secrets; print(secrets.token_urlsafe(64))'
```

Replace `CHANGE_ME_SUPER_LONG_RANDOM_SECRET` with the generated value. Start the stack.

```bash
cd ~/Containers/defectdojo
podman-compose up -d
```

Sometimes Podman asks which registry to use for images such as `postgres`. Pick: `docker.io/library/postgres...` Check whether containers are running:

```bash
podman ps --format "{{.Names}}  {{.Image}}"
```

Typical containers:

- `defectdojo_postgres_1`
- `defectdojo_valkey_1`
- `defectdojo_uwsgi_1`
- `defectdojo_celerybeat_1`
- `defectdojo_celeryworker_1`
- `defectdojo_nginx_1`

Open the web UI. Default local URL:

- `http://localhost:8080`

Create the admin account. In my case the Django container was `defectdojo_uwsgi_1`, so:

```bash
podman exec -it defectdojo_uwsgi_1 python manage.py createsuperuser
```

Then provide:

- username
- email
- password

Log in to the UI using the account you created in the previous step.

### Useful commands

View logs

```bash
cd ~/Containers/defectdojo
podman-compose logs -f --tail=100
```

Stop and start

```bash
podman-compose down
podman-compose up -d
```

Update without losing data

```bash
cd ~/Containers/defectdojo
git pull
podman-compose pull
podman-compose up -d
```

Reset a password

```bash
podman exec -it defectdojo_uwsgi_1 python manage.py changepassword <username>
```

Simple database backup

```bash
podman exec -t defectdojo_postgres_1 pg_dump -U defectdojo defectdojo > ~/Containers/defectdojo_backup_$(date +%F).sql
```

Check volumes

```bash
podman volume ls | grep defectdojo
```

Do not remove DefectDojo volumes if you want to keep your data.

Start after reboot

```bash
cd ~/Containers/defectdojo && podman-compose up -d
```

## How to think about DefectDojo structure

This structure makes a lot more sense once you stop thinking about DefectDojo as a note-taking app or classic pentest report writer. It is better understood as a place where Products, Engagements, imported scans, and validated findings are organized over time.

This is the part that matters most. DefectDojo is not just “upload a file and forget it”. If you want it to be useful, you need to understand the core structure.

### Product

A **Product** is the main scope or target area.

Examples:

- `example.com`
- `Acme External Web`
- `Customer Portal`
- `Bug Bounty - Vendor X`

For example, if I were documenting one company’s external web surface, I would usually create one Product and keep using it long term.

Example:

- Name: `example.com`
- Type: `Web Application`
- Tags: `bugbounty, web, external`

### Engagement

An **Engagement** is one concrete testing cycle inside a Product.

Examples:

- `Recon - 2026-03-29`
- `Quarterly External Review - Q1 2026`
- `Retest After Fixes - April`

This is the practical model:

- same Product
- new Engagement for each run, retest, or reporting period

That way you keep history clean and can compare old vs new findings.

### Findings and imports

Inside an Engagement you can:

- import supported scan files
- manually add findings
- reimport updated scans
- track whether something is new, duplicate, accepted, mitigated, or resurfaced

That is where it becomes useful for internal work and long-term documentation.

## A simple DefectDojo workflow

### Create a Product

UI:

- `Products`
- `Add Product`

Example:

- Name: `example.com`
- Type: `Web Application`
- Tags: `bugbounty,web,external`

### Create an Engagement

Inside the Product:

- `Add Engagement`

Example:

- Name: `Recon - 2026-03-29`
- Status: `In Progress`
- Engagement Type: `Interactive`
- Deduplication: enabled

### Import supported scan files

The practical ones for a fast web workflow are:

- Nuclei
- Nmap
- Nikto
- SSLScan

Everything else can be reviewed manually and added only if it is validated and worth storing.

## What I would import automatically

For a web-focused workflow, the most useful imports are:

#### Nuclei

```bash
nuclei -l httpx.txt \
  -severity low,medium,high,critical \
  -stats \
  -jsonl -o nuclei.jsonl
```

Import as:

- `Nuclei Scan`

#### Nmap

```bash
nmap -sS -sV -sC -T3 \
  -p 80,443 \
  -oA nmap_web \
  example.com
```

Import:

- `Nmap Scan`
- file: `nmap_web.xml`

#### Nikto

If your build supports JSON output:

```bash
nikto -h https://example.com -Format json -output nikto.json
```

Then import as Nikto.

#### SSLScan

Use XML output:

```bash
sslscan --xml=sslscan.xml example.com
```

That gives you a structured file instead of raw terminal output.

## What I would usually review manually

Some outputs are better reviewed by hand first:

- `ffuf`
- `feroxbuster`
- `reconFTW`
- `httpx`
- miscellaneous recon tools

That is also the main reason why I would not treat DefectDojo as a replacement for a working notebook during testing. It is better as the destination for results that are already worth keeping, comparing, and presenting later.

That is because those tools often return useful leads, but not every hit should become a formal finding.

Examples of things I would review and then add manually:

- exposed admin panels
- backups
- `.git`
- internal files
- misconfigured directories
- old TLS support that actually matters
- suspicious endpoints confirmed by testing

### A minimal and practical tool set

If the goal is to move fast and not drown in noise, I would start with:

1. `httpx`
2. `nuclei`
3. `nmap`
4. `ffuf`
5. `sslscan`

Then only go deeper when something looks promising.

Example commands:

### httpx

```plaintext
httpx -u https://example.com \
  -status-code -title -tech-detect -ip -cdn \
  -o httpx.txt
```

Or with a list:

```bash
httpx -l subdomains.txt \
  -status-code -title -tech-detect \
  -o httpx.txt
```

### nuclei

```bash
nuclei -l httpx.txt \
  -severity low,medium,high,critical \
  -stats \
  -jsonl -o nuclei.jsonl
```

### nmap

```bash
nmap -sS -sV -sC -T3 \
  -p 80,443 \
  -oA nmap_web \
  example.com
```

### ffuf directories

```bash
ffuf -u https://example.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -mc 200,204,301,302,307,401,403 \
  -of csv -o ffuf_dirs.csv
```

### ffuf files

```bash
ffuf -u https://example.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/raft-small-files.txt \
  -mc 200,204,301,302 \
  -of csv -o ffuf_files.csv
```

### sslscan

```bash
sslscan --xml=sslscan.xml example.com
```

## Realistic usage examples

### Example 1: one bug bounty target

- Product: `example.com`
- Engagement: `Recon - 2026-03-29`

Run:

- httpx
- nuclei
- nmap
- ffuf
- sslscan

Import:

- `nuclei.jsonl`
- `nmap_web.xml`
- `sslscan.xml`
- optionally `nikto.json`

Then manually add only the FFUF and recon findings that actually matter.

### Example 2: retest after fixes

Same Product:

- `example.com`

New Engagement:

- `Retest - 2026-04-10`

Import the new scans and compare whether:

- findings are still present
- new issues appeared
- something previously fixed came back

### Example 3: company documentation over years

For a company environment, this is where the platform starts to make real sense.

Instead of random files and stale notes, you can keep:

- findings
- scan history
- imports
- manual analysis
- retests
- reporting snapshots

That is useful when you need to go back to something after one year or three years and explain exactly what was found, when, and whether it was ever fixed.

## Final thoughts

For solo bug bounty work, I still do not think a heavy platform always makes sense. A good notes app is usually faster for testing, storing evidence, and writing a report.

For company work, however, DefectDojo starts to make much more sense because it is not trying to be just a notebook. It is a vulnerability management platform for imported scanner output, triage, deduplication, historical tracking, and structured findings.

So at this stage I treat it less as “my daily bounty platform” and more as a serious candidate for structured internal documentation, scan imports, long-term evidence retention, and report organization.

At the same time, while writing this article I found OWASP Cervantes, which may be closer to the “pentest project management and reporting” side of the problem. I still want to test it properly, so I will probably come back to it in a future article if it turns out to be a better fit for that specific use case.
