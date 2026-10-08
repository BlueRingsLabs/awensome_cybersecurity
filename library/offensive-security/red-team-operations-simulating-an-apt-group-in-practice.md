---
id: ckb-02b55d58b29e
title: Red Team Operations Simulating an APT Group in Practice
category: offensive-security
format: guide
language: en
tags: [evasion, mitre-attack, persistence, privilege-escalation, red-team, windows]
summary: This document provides an overview of red teaming operations by detailing common APT tactics, techniques, and procedures, including specific methods for AMSI bypass, persistence, and defense evasion via syscall manipulation.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.95
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:57:36Z
---

Translated from Portuguese to English - www.onlinedoctranslator.com
Red Team Operations –
Simulating an APT group in practice
What is APT
APT (Advanced Persistent Threat) is a group or threat actor that carries
out sophisticated, prolonged and targeted cyber attacks on a specific
entity, usually aiming to steal valuable information or cause damage.
These attacks are characterized by:
- Persistence
- Stealth
- Ability to adapt
- Evasion of detections
ANATOMY
source:SOC Investigations
source:Google Image Search
MITER ATT&CK AND TTPS
to thetacticsare the
tactical objectives that
a threat can use during
an operation.
to thetechniquesdescribe
the actions that threats
take to achieve their
goals.
youproceduresare the
technical steps required
to perform the action.
source:redteam.guide
Modus Operandi - APT29 AND APT 38
APT29 (also known as "Cozy Bear" or "The Dukes")
Origin:APT29 is widely associated with the Russian government, specifically the Foreign
Intelligence Service (SVR).
Operation:It is estimated that the group has been active since at least 2008.
APT38 (aka "Lazarus Group")
Origin:APT38 is widely associated with the North Korean government, specifically Bureau
121, the country's cyberwarfare unit.
Operation:It is estimated that the group has been active since at least 2009
UNC3313 Attack Chain
source:Security Affairs
APT29 Attack Chain
source:Miter Center for Threat Informed Defense
APT29 Attack Chain
source:Fortinet
APT38 Attack Chain
source:Radware
Examples:
Tactics, Techniques and Procedures
Initial Access – Spear-Phishing
- Top Domain Levels
(Ex: .xyz, .io, .to,
.xxx)
- - Cloudflare
Turnstile (Avoid
Bots)
- - Private Whois
- - IDN Homograph and
Punycode
source:ResearchGate
Execution – AMSI Bypass
When a user runs a script or opens
PowerShell, AMSI.dll is loaded into
the process' memory. Before the
script runs, the antivirus uses the
functionsAmsiScanBuffer()andAmsi
ScanString()to check the code for
signs of malware. If something
suspicious is found, the script is
blocked and the antivirus shows a
message that execution has been
prevented.
source:Pentest Laboratories
Execution – AMSI Bypass
The image shows a PowerShell
command where the user attempts to
bypass the Windows Malware
Scanning Interface (AMSI) to run a
blocked script. Initially, a script was
blocked from downloading by
antivirus software, so the user used
code to disable AMSI before trying to
execute the blocked command again.
source:MDSec
Persistence – Techniques
source:ScienceDirect
Persistence– Backdoor with Lib-nosa
lib-nosa is a minimalist C library designed to facilitate
socket connections via AFD driver IOCTL operations on Windows.
By bypassing the traditional winsock2.h -> (ws2_dll.dll)
header, lib-nosa interacts directly with the internal AFD
(Ancillary Function Driver for WinSock) socket APIs, offering
developers a lightweight, low-level alternative to software
programming. network.
source:ViperX by Alexa Souza
Privilege Escalation - Techniques
source:Certcube
Defense Evasion – Direct Syscall
In this method, the malware directly
implements the syscall stub in the
assembly code, which means it
transitions from user mode to kernel
mode without going through the
functions of native Windows
libraries such as ntdll.dll. Instead of
invoking the NtCreateFile API from
ntdll.dll, the malware directly
executes the assembly instructions
required to invoke the syscall. This
involves preparing the registers and
calling the syscall instruction.
source:RedOps
Defense Evasion – Indirect Syscall
In indirect syscall, the malware uses
ntdll.dll to execute the system call.
The malware invokes the
NtCreateFile function in ntdll.dll,
which in turn transitions it to the
kernel. This means that the
execution of the syscall command
occurs in the legitimate memory of
ntdll.dll. After executing the syscall
in the kernel, the return of the
execution flow also occurs in the
ntdll.dll memory
source:RedOps
Defense Evasion – Gate
Techniques
Hells Gate:Advanced evasion technique that executes syscalls directly,
without going through the code of ntdll.dll, where EDRs usually apply
hooks.
By avoiding the library, Hells Gate is able to make calls to the kernel
transparently, minimizing the risk of detection and increasing malware
stealth.
Defense Evasion – Gate
Techniques
Halo's Gate:A variant of Hells Gate, Halo's Gate uses an indirect syscall
technique, SSN resolution by comparing neighboring functions to determine
whether they are hooked.
By avoiding monitored functions, it calculates the correct syscall and
invokes it directly, bypassing protections from EDRs and other security
systems that monitor ntdll.dll.
Defense Evasion – Gate
Techniques
HookChain: Through a precise combination of IAT Hooking techniques, dynamic
SSN resolution and indirect system calls, HookChain redirects the execution
flow of Windows subsystems in a way that remains invisible to the watchful
eyes of EDRs that act only on Ntdll.dll , without requiring changes to the
source code of the applications and malware involved.
source:Helvio Junior aka M4v3r1ck
Defense Evasion – Gate
Techniques
Heavens Gate:Technique that allows code execution
64-bit process from a 32-bit process, known as a form of mixed architecture
circumvention.
Heavens Gate takes advantage of differences between execution modes to bypass
protections and allow malicious code to run in restricted environments.
When a 32-bit application running inside a 64-bit process needs to call a 64-bit system
function or interface, it must switch the processor to 64-bit mode. This is where the
Heaven's Gate technique comes into play.
The technique involves executing a special syscall instruction, code segment register
value: for x86: 0x23, x64: 0x33 that triggers a context switch from 32-bit mode to 64-
bit mode, effectively changing the contents of the CS register .
Defense Evasion – Gate
Techniques
Phantoms Gate: PhantomsGate is a sophisticated
shellcode injection technique that uses Hell's Gate to
dynamically find syscall numbers, modifies system calls
to fool EDRs, and uses thread hijacking to inject and
execute shellcode in a process.
Defense Evasion – Vulnerable Drivers
source:InfoSec Write Ups by EINiak
Defense Evasion – Process Injection
Mockingjay
The injection is performed without allocating space,
setting permissions, or even starting a thread. The
uniqueness of this technique is that it requires a
vulnerable DLL and code copying to the correct section.
source:Security Joes by Thiago Peixoto
Credential Access – Techniques
source:Elastic Global
Lateral Movement – ​Techniques
●Pass-the-Hash:Technique where the attacker uses the user's password hash to authenticate
to other systems, without needing to know the password itself.
# psexec.py -hashes <NTLM_HASH> <domain>/<username>@<target_ip>
●Remote Services:Access remote services such as RDP, SMB or SSH to move from one
compromised system to another.
# mstsc /v:<target_ip>
●Windows Admin Shares:Using Windows administrative shares (such as C$, ADMIN$) to transfer
files or remotely execute commands on other systems within the same domain.
# net use \\<target_ip>\C$ /user:<domain>\<username> <password>
Lateral Movement – ​Techniques
source:Wizlynx Group
ANDxfiltration – Techniques
●Compressed data (zip of zip)
●Encoded data (Base64)
●Encrypted data (Symmetric and Asymmetric)
●Data transfer size limits -> data fragments (separate files
into smaller bytes)
●Exfiltration by alternative protocol (SSH, DNS, SFTP, SMTP,
HTTPS)
●Exfiltration through C2 channel
●Exfiltration by physical means (Pendrives, External HDs,
etc.)
Exfiltration – Techniques
source:ResearchGate
REFERENCES
https://www.socinvestigation.com/anatomy-of-the-ransomware-cybercrime-economy/
https://prodigy13.com/kill-chain-pros-cons/
https://redteam.guide/
https://securityaffairs.com/128493/malware/unc3313-apt-two-backdoors.html
https://www.researchgate.net/figure/Data-Exfiltration-via-DNS-queries_fig1_359077112
https://www.fortinet.com/blog/threat-research/teamcity-intrusion-saga-apt29-suspected-exploiting-cve-
2023-42793
https://www.radware.com/cyberpedia/ddos-attacks/the-lazarus-group-apt38-north-korean-threat-actor/
https://www.researchgate.net/figure/Phases-of-a-common-Spear-Phishing-attack_fig1_361946872
https://pentestlaboratories.com/2021/05/17/amsi-bypass-methods/
https://www.mdsec.co.uk/2018/06/exploring-powershell-amsi-and-logging-evasion/
https://www.sciencedirect.com/science/article/pii/S0167404822002498
https://github.com/ViperXSecurity/lib-nosa
https://blog.certcube.com/windows-privilege-escalation-methods/
https://redops.at/en/blog/direct-syscalls-vs-indirect-syscalls
https://github.com/helviojunior/hookchain
https://infosecwriteups.com/byovd-attacks-the-hidden-threats-of-vulnerable-drivers-d1aebe9b552e
https://www.securityjoes.com/post/process-mockingjay-echoing-rwx-in-userland-to-achieve-code-execution
https://www.elastic.co/es/blog/elastic-global-threat-report-breakdown-credential-access
https://www.wizlynxgroup.com/us/cyber-security-usa/red-team-assessment-services
https://www.researchgate.net/figure/Data-Exfiltration-via-DNS-queries_fig1_359077112
