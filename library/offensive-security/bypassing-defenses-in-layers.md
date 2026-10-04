---
id: ckb-00292bdcfc7e
title: Bypassing Defenses in Layers
category: offensive-security
format: guide
language: en
tags: [physical-security, red-team, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.46
---

Bypassing
Layered Defenses
PT.1
joas antonio
Translated from Portuguese to English - www.onlinedoctranslator.com
Author
+Information Security Analyst (Red team) on move;
+Writer and Speaker Hacker Culture;
+Synack Red team member;
+OWASP Project Leader;
+hacking is note the Crime advocate;
PenTest Academy
•
A study by two researchers from the
University of Piraeus, Greece, published
with 48 pages in the scientific journal
Journal of cybersecurity and Privacy as of
December 31, indicates that the
overwhelming majority of protection and
response solutions for endpointsfailed to
efficiently detect and prevent the four
attack vectors used in the trial. Signed by
researchers Georgekarantzas and
Constantines Patsakis, the study
concludes that “the attack of sideload DLL
is the most successful [attack] as most of
the EDRs cannot detect it, much less
block it”
•
https://www.cisoadvisor.com.br/estudo-
mostra-fragility-das-atuais-solucoes-de-
edr/
Let’s Hack!
Sideloading DLL Hijacking
+THE side loadinginvolves hijacking the DLL which a program
loads. But instead of just planting the DLL inside a program's
search order and then waiting for the victim application to run,
adversaries can do the same.side-load directly from your
payloads by planting and then invoking a legitimate application
that runs your(s) payload (s).
Sideloading DLL Hijacking
https://github.com/Flangvik/DLLSideloader
Sideloading DLL
Hijacking
Sideloading DLL
Hijacking
Indirect code execution
+Adversaries can abuse utilities that allow the execution of
commands to circumvent security restrictions that limit the use
of command line interpreters. Various Windows utilities can be
used to run commands, possibly without invokingcmd. For
example,Forfiles, The program compatibility assistant
(pcalua.exe), Windows components subsystem for Linux (WSL)
as well as other utilities can invoke the execution of programs
and commands from a Command and scripting interpreter.
Indirect code execution
Trevorfuscation
+ https://github.com/CyberSecurityUP/Trevor
fuscation
books
PHYSICAL SECURITY DESIGN
bypass physical
Security
+
An attacker uses techniques and methods to circumvent the
physical security measures of a building or facility. Physical
locks can range from traditional lock and key mechanisms, cable
locks used to secure laptops or servers, locks on server cabinets
or other devices. Techniques such as knock blocking, forced
blocking by airguns, or lock picking can be employed to bypass
these locks and gain access to facilities or devices that protect,
albeit confidential, evidence of tampering and integrity of the
lock after an attack are considerations that can determine the
method used. Physical locks are limited by the complexity of the
locking mechanism.
bypass WAF Techniques
+Tools to Check and Bypass WAFs:
+w3af — Web Application Attack and Audit Framework
+wafw00f — Identify and fingerprint Web Application Firewall
+BypassWAF – Bypass firewalls by abusing DNS history. This tool will
search for old DNS A records and check if the server replies for that
domain.
+CloudFail – is a tactical reconnaissance tool that tries to find the
original IP address behind the Cloudflare WAF.
bypass WAF Techniques
+ 1. Case toggling Technique: Combine uppercase and lowercase
characters to create efficient payloads.
+ 2. URL encoding Technique: encode payloadsnormal with
%encoding/url encoding. You can use theburp. It has an
encoder/decoder tool.
+ 3. Unicode Technique: ASCII characters in Unicode encoding provide
us with great variants to bypass WAF. Code all or part of the payload
to get results.
<marquee onstart=prompt()>
obfuscated:
<marquee onstart=\u0070r\u006fpt()>
books 2
CONCLUSION
DOUBTS?
https://www.linkedin.com/in/joas-antonio-dos-santos
Links
+https://dmcxblue.gitbook.io/red-team-notes-2-0/red-team-
techniques/defense-evasion/untitled-5/dll-side-loading
+https://dmcxblue.gitbook.io/red-team-notes-2-0/red-team-
techniques/defense-evasion/t1202-indirect-command-execution
+https://capec.mitre.org/data/definitions/390.html
+https://www.sciencedirect.com/science/article/abs/pii/S18745482
14000420
+https://pentestit.medium.com/bypassing-waf-4cfa1aad16bf
+https://hacken.io/researches-and-investigations/how-to-bypass-
waf-hackenproof-cheat-sheet/
