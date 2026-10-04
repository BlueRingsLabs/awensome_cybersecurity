---
id: ckb-df7171bc8e9a
title: HexStrike AI on Kali with Roo Code
category: ai-security
format: article
language: en
tags: [bash, git, linux, privilege-escalation, python, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.46
---

# HexStrike AI on Kali with Roo Code

This article is about building a HexStrike AI Lab with Kali, Fedora, Roo Code and DeepSeek. Enjoy!

HexStrike AI popped up in the [Parrot 7.0 release](https://www.parrotsec.org/blog/2025-12-24-parrot-7.0-release-notes/) notes as a new “AI Tool” category.

> We are known to have very strong opinions on artificial intelligence, machine learning and LLMs, and Parrot 7 represents our chance to define a clear roadmap for AI.
>
> We can not stand idle as this technological leap unfolds, which is why we decided to add this category to our set. The first tool we included is Hexstrike AI, and we plan to continue to integrate MCP powered tools. But our mission remains to include and sponsor the development of tools designed to test the security of LLM prompts and play with prompt engineering techniques.
>
> AI driven automation might seem handy, but the actual “Cybersecurity AI Revolution” will only come from the proper strategies and tools to secure such family of technologies.
>
> *– ParrotSec Blog*

So I thought, okay, I’ll try it out, see how it works and what can be achieved with it.

This post is a step-by-step guide to:

- running HexStrike server on a Kali VM,
- exposing it to the Fedora host,
- using Roo Code in VS Code as the AI orchestrator,
- combining local Ollama models for cheap/lightweight tasks,
- and DeepSeek API for heavier reasoning.

At the end I also show what a real test against my own domain (`0ut3r.space`)

Cost: about **$0.04** for a full basic recon + vuln check and report.

![hexstrikeai](hexstrikeai.webp)

Of course, you can try out this solution directly on Parrot OS, but I use Kali Linux for everything. For a long time, I was torn between Kali and Parrot. I used Kali on a daily basis and used Parrot for other tasks. Over time, I was getting closer and closer to switching completely to Parrot OS, but Parrot’s decision to switch to KDE as the default graphical environment and abandon MATE completely changed my approach to it. For pentesting systems, Mate or XFCE have become the obvious choice, with Gnome or KDE as alternatives. Although hardware has long been capable of handling demanding systems as virtual machines, I am a proponent of lightweight environments out of habit, or perhaps minimalism and innate thriftiness. I know you can install and configure whatever you want, but simple, small, fast out-of-the-box solutions appeal to me more. KDE in Parrot makes perfect sense for the Home version on modern laptops and desktops for everyday use. However, after installing 7.0, many tools did not work for me. Various types of error appeared when launching some of them and, in general, the extended KDE looked like Mate. Perhaps I’ll change my mind over time, but for now, due to not having enough time to customise it to my liking, I prefer classic Kali with XFCE.

So if you would like to set up AI for automated testing on Kali and control everything from your host, you may find the following instructions useful.

## Architecture Overview

High level design:

- **Kali VM**
  - HexStrike AI installed under `/opt/hexstrike-ai`
  - Python virtualenv managed by `virtualenvwrapper`
  - Small shell script to start the HexStrike server
  - Desktop shortcut on Kali to launch the server in a terminal
- **Fedora host**
  - Same HexStrike repo cloned under `/opt/hexstrike-ai`
  - Separate virtualenv used only for the MCP client (`hexstrike_mcp.py`)
  - VS Code with Roo Code extension
  - Roo configured with:
    - Ollama (local models) for lightweight HexStrike tasks
    - DeepSeek API for deeper analysis
    - MCP server entry pointing to the Kali HexStrike instance
    - custom Modes for:
      - HexStrike Light (Ollama)
      - HexStrike (normal with DeepSeek)
      - HexStrike Deep Analysis (DeepSeek Reasoner)

## Kali: installing HexStrike server

I installed the server on Kali ([Virt-Manager](https://virt-manager.org/)) because most of the necessary tools were already available, and any missing ones could easily be installed. Alternatively, you can create your own virtual machine - for example, a clean Debian - and only install the tools required by HexStrike on it. This takes a little more time, but ultimately you will have a setup that is solely for AI.

### Requirements

On Kali you’ll want the usual tooling HexStrike can use, e.g.:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip virtualenvwrapper nmap nuclei gobuster wafw00f git
```

Install any other tools HexStrike mentions in its [README](https://github.com/0x4m4/hexstrike-ai/blob/master/README.md) as you go.

### Clone HexStrike under /opt

```bash
sudo mkdir -p /opt/hexstrike-ai
sudo chown -R "$USER:$USER" /opt/hexstrike-ai
cd /opt/hexstrike-ai

git clone https://github.com/0x4m4/hexstrike-ai.git .
```

### Create virtualenv with virtualenvwrapper

Assuming `virtualenvwrapper` is installed and sourced from your shell init (`.bashrc` / `.zshrc`):

```bash
# create env
mkvirtualenv hexstrike-ai

# link project directory to env (so workon jumps into /opt/hexstrike-ai)
setvirtualenvproject ~/.virtualenvs/hexstrike-ai /opt/hexstrike-ai

# activate
workon hexstrike-ai

# install deps
pip install --upgrade pip
pip install -r requirements.txt
```

From now on `workon hexstrike-ai` drops you into `/opt/hexstrike-ai` with the venv active.

### Server start script

Create a small script under `/opt/hexstrike-ai`:

```bash
cat << 'EOF' | sudo tee /opt/hexstrike-ai/start_hexstrike.sh >/dev/null
#!/bin/bash
# Load virtualenvwrapper
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh

# Activate env + cd to /opt/hexstrike-ai (because of setvirtualenvproject)
workon hexstrike-ai

# Start HexStrike server
/home/kali/.virtualenvs/hexstrike-ai/bin/python3 hexstrike_server.py
EOF

sudo chmod +x /opt/hexstrike-ai/start_hexstrike.sh
```

Replace `kali` with your username if different.

### Desktop launcher on Kali

Create a `.desktop` file, e.g.:

```bash
cat << 'EOF' > ~/Desktop/HexStrike.desktop
[Desktop Entry]
Type=Application
Name=HexStrike Server
Comment=Start HexStrike MCP server on Kali
Exec=/opt/hexstrike-ai/start_hexstrike.sh
Icon=/opt/hexstrike-ai/assets/hexstrike-logo.png
Terminal=true
Categories=Utility;
EOF

chmod +x ~/Desktop/HexStrike.desktop
```

Now on Kali you just double-click **HexStrike Server** and it opens a terminal, activates the venv and starts `hexstrike_server.py`.

You can verify it’s running with:

```bash
curl http://127.0.0.1:8888/health
```

## Exposing Kali to Fedora

On Kali, get the VM IP:

```bash
ip addr show
# or shorter:
hostname -I
```

Assume it’s:

```bash
192.168.122.211
```

From the **Fedora host** you should be able to reach the health endpoint:

```bash
curl http://192.168.122.211:8888/health
```

If this fails, fix your VM networking (bridge / NAT+port forward) or firewall first. It all depends on which virtualisation tool you are using. I am using Virt-Manager with KVM, so it works out of the box.

## Fedora: MCP client setup for HexStrike

On Fedora (in my case, but this applies to any Linux distribution that you use as your main operating system) we don’t need the full HexStrike toolchain, only the MCP client script.

### Clone the repo

```bash
sudo mkdir -p /opt/hexstrike-ai
sudo chown -R "$USER:$USER" /opt/hexstrike-ai
cd /opt/hexstrike-ai

git clone https://github.com/0x4m4/hexstrike-ai.git .
```

### Create a separate MCP venv

You can use `virtualenvwrapper` again or a plain venv. Below with `virtualenvwrapper`:

```bash
mkvirtualenv hexstrike-mpc
setvirtualenvproject ~/.virtualenvs/hexstrike-mpc /opt/hexstrike-ai

workon hexstrike-mpc
pip install --upgrade pip
pip install -r requirements.txt
```

This env is **only** for `hexstrike_mcp.py` on Fedora.

You can test manually that MCP can talk to the Kali server:

```bash
workon hexstrike-mpc
cd /opt/hexstrike-ai

python3 hexstrike_mcp.py --server http://192.168.122.211:8888 --debug
```

If this connects and stays running (or shows reasonable logs), the MCP side is ok.

## VS Code + Roo Code configuration

Install [Roo Code](https://roocode.com/) extension in [VS Code](https://code.visualstudio.com/) on Fedora.

### MCP server config (HexStrike)

Open Roo’s MCP config file (Command Palette → search for “Roo: Open MCP Config”) and add:

```bash
{
  "mcpServers": {
    "hexstrike-ai": {
      "command": "/home/user/.virtualenvs/hexstrike-mpc/bin/python3",
      "args": [
        "/opt/hexstrike-ai/hexstrike_mcp.py",
        "--server",
        "http://192.168.122.211:8888"
      ],
      "env": {},
      "disabled": false,
      "timeout": 300,
      "alwaysAllow": []
    }
  }
}
```

Adjust the username and IP if needed.

Roo will now be able to spawn `hexstrike_mcp.py` as a local MCP server that talks to HexStrike on Kali.

## Providers in Roo: DeepSeek + Ollama

If you haven’t set up your local AI using Ollama, you can skip the Ollama configuration and focus solely on the API solution. However, if you’re interested in setting up a local AI environment, read the article ‘[Building a Local AI Environment](https://0ut3r.space/2025/08/22/building-local-ai-environment/)‘, in which I explain how I did it.

In addition, I used DeepSeek’s API for the test. It is currently the cheapest on the market. I know that DeepSeek is Chinese and that everyone is spying on me. However, for the sake of testing, I am willing to accept this risk and remove my tinfoil hat. The same applies to VS Code. If you don’t want to do this, use VS Codium instead. Alternatively, follow HexStrike’s advice and use 5ire, Cursor, Claude Desktop or any other MCP-compatible agent.

Always adapt the guide to your environment, and decide when you can compromise and when you cannot. While I don’t recommend commenting in a disparaging manner, I do encourage feedback on your approach and reasoning.

Without further ado, start using the API from your favourite, trusted provider.

### DeepSeek API provider

In Roo’s Providers:

- API Provider: `DeepSeek`
- API Key: your DeepSeek key
- Model: `deepseek-chat` (for normal use)
- Context window: 128k (default)
- Prompt cache: enabled (this dramatically cuts cost)

DeepSeek pricing at the time of writing is roughly:

- Input: $0.28 / 1M tokens
- Output: $0.42 / 1M tokens
- Cache hits: ~$0.03 / 1M tokens

In my test, a full recon/vuln check task consumed about 1M input tokens and ~3.2k output, landing around **$0.04** total thanks to caching.

You can later add a second API config with `deepseek-reasoner` for heavy analysis.

### Ollama provider

If you run Ollama, Roo can use it too:

- Provider: `Ollama`
- Base URL: `http://localhost:11434`
- Model ID: e.g. `chat-ai:latest` (Qwen2.5-based chat model)

This becomes your cheap, local brain for lighter HexStrike tasks.

## Roo Modes for HexStrike

To keep things clean I created three dedicated Modes:

### HexStrike (normal)

**Name:** `HexStrike`
**Slug:** `hexstrike`
**API Configuration:** DeepSeek `deepseek-chat`

**Role Definition:**

```html
You are an AI pentesting orchestrator specializing in using tools via MCP, especially HexStrike.

Primary objectives:
1) Plan, step-by-step reconnaissance and vulnerability analysis.
2) Use tools instead of guessing. Always prefer running HexStrike tools over speculation.
3) Summarize results clearly and propose next actions.
4) Avoid modifying code unless explicitly asked.
5) Explain your reasoning concisely, not verbosely.
6) Never run intrusive or destructive actions without explicit permission and confirmed scope.
```

**Short description (for humans):**

```html
Plan and automate pentests using HexStrike + MCP.
```

**When to use:**

```html
Use this mode when performing security assessments, reconnaissance, analysis of scan results,
or orchestrating external security tools. Avoid code changes unless explicitly requested.
```

**Available Tools:**

- ☑ Read Files
- ☐ Edit Files
- ☑ Run Commands
- ☑ Use MCP
- ☑ Use Browser (optional; you can leave it off if you want everything through HexStrike)

**Custom Instructions:**

```html
Prefer minimal, targeted scans instead of noisy full-scope scans.

When reporting results, always include:
- What was found
- Why it matters (risk level + business impact)
- Evidence (screenshots, URLs, response snippets when possible)
- Suggested next step (what to run next)

Do not spam with unnecessary scans.
Explain if data is insufficient instead of hallucinating.
```

### HexStrike Light (Ollama)

This mode uses Ollama as provider and is meant for cheap, safe health checks and basic recon.

**Name:** `HexStrike Light`
**Slug:** `hexstrike-light`
**API Configuration:** Ollama → `chat-ai:latest`

**Role Definition:**

```html
You are a light HexStrike operator using local Ollama models.

Your job:
1) Perform only safe, lightweight checks (health, status, basic recon).
2) Prefer MCP HexStrike tools instead of guessing.
3) Ask for confirmation before expanding scope.
4) Keep answers short and practical.
5) If something requires deeper reasoning, suggest switching to HexStrike Deep Analysis.
6) Never perform intrusive, brute-force, exploit or destructive actions.
```

**Short description:**

```html
Lightweight HexStrike operator – health checks and quick recon, no aggressive actions.
```

**When to use:**

```html
Use this mode for quick reconnaissance, availability checks, fingerprinting,
and validating earlier findings. Avoid heavy scanning and exploitation.
```

**Available Tools:**

- ☑ Read Files
- ☐ Edit Files
- ☑ Run Commands
- ☑ Use MCP
- ☐ Use Browser

**Custom Instructions:**

```html
Allowed examples:
- HTTP/TLS health checks
- What services seem to be running?
- Basic technology fingerprinting
- Reviewing logs or previous scan summaries

Forbidden without explicit confirmation:
- brute force
- fuzzing
- DoS / stress testing
- exploit attempts
- full-scope scans
```

### HexStrike Deep Analysis (DeepSeek Reasoner)

This is the “think hard” mode.

**Name:** `HexStrike Deep Analysis`
**Slug:** `hexstrike-deep`
**API Configuration:** DeepSeek `deepseek-reasoner`

**Role Definition:**

```html
You are an AI pentesting analyst focused on deep reasoning, correlation, and decision-making
while orchestrating tools via MCP, especially HexStrike.

Your priorities:
1) Think before acting - reason step-by-step internally.
2) Always confirm scope, assets, and permissions before running tools.
3) Prefer running HexStrike tools instead of guessing.
4) Correlate results across tools (recon, HTTP responses, headers, DNS, TLS, technologies, login flows).
5) Highlight likely attack paths, not just raw findings.
6) Clearly separate facts from assumptions.
7) Keep final answers concise, even if reasoning was complex.
8) Never run intrusive/destructive actions without explicit user approval.
```

**Short description:**

```html
Deep analysis and correlation of HexStrike results using DeepSeek Reasoner.
```

**When to use:**

```html
Use this mode when you need deep analysis, threat modeling, interpreting scan results,
or planning multi-step attack chains. Do not use it for simple commands or fast recon.
```

**Available Tools:**

- ☑ Read Files
- ☐ Edit Files
- ☑ Run Commands
- ☑ Use MCP
- ☑/☐ Use Browser (your call)

**Custom Instructions:**

```html
Work slowly. Prefer reasoning first, actions second.

Always structure output:
- Summary
- What we know (facts)
- Assumptions
- Possible attack paths
- Suggested next tool or command (with reason why)
- Risk / priority

Do not spam with unnecessary scans.
If the data is insufficient, say so instead of guessing.
```

## Example: scanning 0ut3r.space

With everything wired, I ran a task in Roo:

> **Task:** `perform a scan of 0ut3r.space basic recon and vulnerability check`

Roo + HexStrike executed a sequence like:

```html
Create initial todo list for reconnaissance
Perform initial target analysis and intelligence gathering
Conduct port scanning with Nmap
Perform web vulnerability scanning with Nuclei
Check for directory enumeration with Gobuster/Dirsearch
Analyze web technologies and WAF detection
Generate comprehensive vulnerability report
```

Under the hood you can see calls like:

```json
Roo wants to use a tool on the hexstrike-ai MCP server
hexstrike-ai/httpx_probe
{
  "target": "https://0ut3r.space",
  "tech_detect": true,
  "status_code": true,
  "title": true,
  "web_server": true
}

Roo wants to use a tool on the hexstrike-ai MCP server
hexstrike-ai/detect_technologies_ai
{
  "target": "https://0ut3r.space"
}

Roo wants to use a tool on the hexstrike-ai MCP server
hexstrike-ai/create_scan_summary
{
  "target": "0ut3r.space",
  "tools_used": "Nmap,Nuclei,Gobuster,wafw00f,Target Intelligence Analysis",
  "vulnerabilities_found": 0,
  "execution_time": 195,
  "findings": "Target is protected by Cloudflare WAF. Ports 80 and 443 open with Cloudflare proxy. Found several accessible directories: /archives, /categories, /css, /js, /lib, /page, /projects, /search. Robots.txt and sitemap.xml accessible. No critical/high/medium vulnerabilities detected by Nuclei."
}
```

### Result summary

HexStrike produced an assessment along these lines:

- Target: `0ut3r.space`
- IPs: Cloudflare anycast (e.g. 188.114.96.11, 188.114.97.11, IPv6)
- Ports: 80/443 open, Cloudflare proxy on both
- WAF: Cloudflare WAF active
- Directory enum: `/archives`, `/categories`, `/css`, `/js`, `/lib`, `/page`, `/projects`, `/search`, etc.
- Files: `/robots.txt`, `/sitemap.xml` accessible
- Nuclei: ~5.5k templates, 0 critical/high/medium vulnerabilities
- Risk: LOW
- Overall: static-style blog behind Cloudflare, no critical findings

### Cost of the whole thing

For that task, Roo’s stats were roughly:

- Context Length: ~76.4k / 128k
- Tokens: ~1.0M input / 3.2k output
- Cache: ~1.0M cached
- API Cost: $0.04
- Task data size: ~5.47 MB

So a full automated recon + vulnerability check + structured report on a real target for less than the price of a chewing gum.

## Closing

That’s the whole pipeline:

1. HexStrike server running on Kali, started via a simple venv-aware script.
2. Fedora host with a minimal MCP client setup in its own virtualenv.
3. Roo Code orchestrating:
   - Ollama for HexStrike Light tasks,
   - DeepSeek Chat for standard HexStrike mode,
   - DeepSeek Reasoner for deep analysis,
   - HexStrike itself via MCP.

You can now repeat this pattern for other targets, tweak your modes, and integrate additional tools - or swap DeepSeek for another API provider if you ever want to.

I guess automatic AI testing is not yet a perfect solution (commercial solutions probably claim otherwise and are more advanced), but I think it can simplify and speed up many tasks. In the future, I believe that automatic AI testing will become very important. I plan to run it after manual testing to see the results and determine which tasks I can trust the AI with, and which ones I still need to do manually. Will the AI find more than I did? After my manual tests, I will run additional automatic tests using different tools. I’m not going to hand over all the manual fun to AI until I see for myself that it works well. This is a good starting point, and I recommend using it for bounty hunting, as well as for support, reconnaissance and CTF, when you get stuck. You should also test its effectiveness yourself.

Happy testing!
