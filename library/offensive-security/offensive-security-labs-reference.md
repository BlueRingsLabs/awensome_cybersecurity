---
id: ckb-612d1919aaab
title: Offensive Security Labs Reference
category: offensive-security
format: reference
language: en
tags: [active-directory, api-security, ctf, red-team, web-security]
summary: This document is a curated reference collection of intentionally vulnerable applications, CTF platforms, and practice environments for penetration testing.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.5-flash-lite
  confidence: 1.0
classified_by: google:gemini-3.5-flash-lite@2026-10-08T00:02:10Z
---

OFFENSIVE
SECURITY
LABS &
PLATFORMS
C O M P L E T E  R E F E R E N C E
A curated collection of intentionally vulnerable applications, CTF platforms, and
practice environments for penetration testing and red team training. Web, API, Cloud,
Active Directory Kubernetes Mobile AI/LLM and more
Active Directory, Kubernetes, Mobile, AI/LLM, and more.
R E D  T E A M  L E A D E R S  |  C Y B E R S E C U R I T Y  T R A I N I N G  |  2 0 2 5  E D I T I O N
Web Application Security Labs (15)
Damn Vulnerable Web Application (DVWA)
The classic intentionally vulnerable PHP/MySQL web app. Covers SQL injection,
XSS, CSRF, file inclusion, command injection, brute force, and more. Multiple
difficulty levels.
https://github.com/digininja/DVWA
OWASP Juice Shop
Modern, feature-rich intentionally insecure web app written in Node.js. Covers
OWASP Top 10 and beyond with 100+ hacking challenges across 6 difficulty levels.
Gamified with a scoreboard.
https://github.com/juice-shop/juice-shop
OWASP WebGoat
A deliberately insecure Java web application maintained by OWASP for teaching web
application security. Guided lessons for each vulnerability class.
https://github.com/WebGoat/WebGoat
bWAPP (Buggy Web Application)
Free, open-source PHP web app with over 100 web vulnerabilities covering all
OWASP Top 10 risks and more. Available as standalone or via bee-box VM.
https://github.com/raesene/bWAPP
Damn Vulnerable Web Services (DVWS)
Insecure web application with vulnerable web service components (SOAP, REST) for
learning web service vulnerabilities.
https://github.com/snoopysecurity/dvws-node
OWASP Mutillidae II
Free, open-source, deliberately vulnerable web application providing a target for web
security enthusiasts. LAMP stack based with 40+ vulnerabilities.
https://github.com/webpwnized/mutillidae
HackTheBox OWASP Top 10 Labs
Online platform with browser-based labs targeting specific OWASP Top 10
vulnerability classes. Guided and unguided challenges.
https://www.hackthebox.com
PortSwigger Web Security Academy
Free online web security training with 200+ interactive labs. Covers SQL injection,
XSS, SSRF, access control, authentication, and advanced topics. Industry gold
standard for web pentesting training.
https://portswigger.net/web-security
Damn Vulnerable Python Web App (DVPWA)
Intentionally vulnerable Python/Django web application for practicing web security
testing against Python-based applications.
https://github.com/anxolerd/dvpwa
Damn Vulnerable NodeJS Application (DVNA)
Intentionally vulnerable Node.js/Express application demonstrating OWASP Top 10
vulnerabilities in the Node.js ecosystem.
https://github.com/appsecco/dvna
Damn Vulnerable WordPress Site (DVWPS)
A vulnerable WordPress installation with intentionally insecure plugins and
configurations for WordPress-specific security testing.
https://github.com/vianasw/dvwps
XXE Lab
Focused lab for practicing XML External Entity (XXE) injection attacks. Simple,
targeted setup for mastering XXE exploitation.
https://github.com/jbarone/xxelab
SQLi-labs
A comprehensive platform for learning SQL injection techniques. Multiple levels from
basic to advanced, covering different SQL injection types and bypasses.
https://github.com/Audi-1/sqli-labs
XSS Game by Google
Interactive game by Google for learning Cross-Site Scripting (XSS) exploitation
techniques with progressive difficulty.
https://xss-game.appspot.com
PentesterLab Exercises
Progressive web security exercises from basic to advanced. Some free, subscription
for full access. Excellent structured learning paths.
https://pentesterlab.com/exercises
API Security Labs (8)
Damn Vulnerable GraphQL Application (DVGA)
Intentionally vulnerable GraphQL implementation for learning GraphQL security.
Covers injection, DoS, authorization bypass, information disclosure, and code
execution. Beginner and Expert modes.
https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application
vAPI (Vulnerable API)
Deliberately vulnerable API built with Flask. Covers OWASP API Top 10
vulnerabilities including BOLA, broken authentication, excessive data exposure, and
injection.
https://github.com/roottusk/vapi
crAPI (Completely Ridiculous API)
OWASP flagship project — a vulnerable API application designed to demonstrate the
OWASP API Security Top 10 risks. Modern microservices architecture.
https://github.com/OWASP/crAPI
DVWS-Node (Damn Vulnerable Web Service - Node)
Vulnerable web services application with SOAP and REST APIs. Built with Node.js
for learning API and web service specific attacks.
https://github.com/snoopysecurity/dvws-node
Damn Vulnerable RESTaurant API
Deliberately vulnerable REST API for OWASP Top 10 API security testing. Built with
Node.js/Express/MongoDB.
https://github.com/theowni/Damn-Vulnerable-RESTaurant-API-Game
Vulnerable GraphQL API
A simple, intentionally vulnerable GraphQL API implementation for practicing
GraphQL-specific attacks.
https://github.com/ivision-research/vulnerable-graphql-api
gRPC-Goat
Vulnerable-by-design gRPC application for learning gRPC-specific security issues.
Hands-on playground for gRPC security testing.
https://github.com/nishant-sachdeva/gRPC-Goat
Generic University API (GUNA)
Deliberately insecure API application with multiple microservices for practicing API
enumeration, authentication bypasses, and IDOR vulnerabilities.
https://github.com/Manas-kashyap/GenUni-API-Security
Active Directory & Windows Labs (7)
GOAD (Game of Active Directory)
The most comprehensive free AD pentesting lab. Multiple configurations: full GOAD
(5 VMs, 2 forests, 3 domains), GOAD-Light (3 VMs), SCCM lab, and NHA challenge.
Covers Kerberoasting, delegation abuse, ACL attacks, trust exploitation, ADCS,
SCCM attacks, and more. Automated deployment with Vagrant + Ansible.
https://github.com/Orange-Cyberdefense/GOAD
Vulnerable-AD (VulnAD)
Intentionally vulnerable Active Directory environment with PowerShell-based
automated setup. Creates a domain with misconfigurations for practicing AD attacks.
https://github.com/safebuffer/vulnerable-AD
DVAD (Damn Vulnerable Active Directory)
Intentionally vulnerable Active Directory environment for practicing AD-specific attack
techniques.
https://github.com/WazeHell/vulnerable-AD
Detection Lab
Lab environment with pre-configured logging and detection capabilities. Includes
Windows AD domain with Splunk, osquery, and Zeek. Great for both attack and
detection practice.
https://github.com/clong/DetectionLab
PurpleCloud
Multi-cloud cybersecurity lab built with Terraform for Azure. Deploys an AD domain
lab environment with Sentinel logging for red/blue team exercises.
https://github.com/iknowjason/PurpleCloud
BadBlood
Fills an Active Directory domain with realistic structure and thousands of objects
(users, groups, computers, ACLs) for testing BloodHound and AD attack tools.
https://github.com/davidprowe/BadBlood
ADLab
Automated Active Directory lab deployment scripts using PowerShell and Vagrant.
Configures a realistic AD environment with common misconfigurations.
https://github.com/xbufu/ADLab
Cloud Security Labs (14)
AWSGoat — Damn Vulnerable AWS Infrastructure
INE's intentionally vulnerable AWS environment. Multiple modules covering SSRF to
RCE, privilege escalation, S3 misconfigurations, Lambda exploitation, and IAM
abuse. Deploys with Terraform.
https://github.com/ine-labs/AWSGoat
AzureGoat — Damn Vulnerable Azure Infrastructure
INE's intentionally vulnerable Azure environment. Covers identity attacks, storage
misconfigurations, key vault exploitation, and Azure-specific attack paths.
https://github.com/ine-labs/AzureGoat
GCPGoat — Damn Vulnerable GCP Infrastructure
INE's intentionally vulnerable GCP environment. Covers GCP-specific
misconfigurations, IAM exploitation, and cloud-native attack paths.
https://github.com/ine-labs/GCPGoat
CloudGoat
Rhino Security Labs' 'Vulnerable by Design' AWS deployment tool. Provides multiple
scenario-based exercises targeting IAM misconfigurations, privilege escalation, and
data exfiltration in AWS.
https://github.com/RhinoSecurityLabs/cloudgoat
Kubernetes Goat
Interactive Kubernetes security learning environment. 'Vulnerable by Design' cluster
with 20+ scenarios covering container escapes, RBAC misconfigurations, secrets
exposure, and more.
https://github.com/madhuakula/kubernetes-goat
WrongSecrets
OWASP project showing how NOT to handle secrets in Docker, Kubernetes, and
cloud (AWS/GCP/Azure). CTF-style challenges for secrets management security.
https://github.com/OWASP/wrongsecrets
Damn Vulnerable Cloud Application (DVCA)
Vulnerable cloud application for practicing cloud-specific attacks and
misconfigurations.
https://github.com/m6a-UdS/dvca
DVFaaS (Damn Vulnerable Functions as a Service)
Vulnerable serverless application for learning serverless-specific security issues.
Covers AWS Lambda, API Gateway, and DynamoDB misconfigurations.
https://github.com/we45/DVFaaS-Damn-Vulnerable-Functions-as-a-Service
Sadcloud
Terraform-based tool for spinning up intentionally insecure AWS infrastructure for
security testing. Quick deployment of misconfigured resources.
https://github.com/nccgroup/sadcloud
TerraGoat
Bridgecrew's 'Vulnerable by Design' Terraform repository. Demonstrates common IaC
security misconfigurations across AWS, Azure, and GCP.
https://github.com/bridgecrewio/terragoat
CdkGoat
Bridgecrew's 'Vulnerable by Design' AWS CDK repository for learning CDK-specific
security misconfigurations.
https://github.com/bridgecrewio/cdkgoat
CfnGoat
Bridgecrew's 'Vulnerable by Design' CloudFormation repository for learning
CloudFormation security issues.
https://github.com/bridgecrewio/cfngoat
Caponeme
Capital One breach simulation. Deploys a vulnerable AWS environment replicating
the conditions that led to the 2019 Capital One breach.
https://github.com/avishayil/caponern
Unguard
An insecure cloud-native microservices demo application for Kubernetes security
testing. Realistic multi-service architecture with intentional vulnerabilities.
https://github.com/dynatrace-oss/unguard
Container & Kubernetes Security Labs (4)
Kubernetes Goat
Comprehensive Kubernetes security learning environment with 20+ scenarios.
Covers RBAC abuse, container escapes, secrets, network policies, and supply chain
attacks.
https://github.com/madhuakula/kubernetes-goat
kube-hunter
Tool for hunting security weaknesses in Kubernetes clusters. Can be used against
intentionally vulnerable clusters for practice.
https://github.com/aquasecurity/kube-hunter
Bust-a-Kube
Intentionally vulnerable Kubernetes cluster for practicing K8s-specific attacks and
misconfigurations.
https://www.youracclaim.com/org/bustakube
Contained.af
A game to teach about Linux container escapes and security. Interactive browser-
based challenges.
https://contained.af
Network & Infrastructure Labs (8)
Metasploitable 2
Intentionally vulnerable Ubuntu VM from Rapid7. Pre-configured with numerous
vulnerable services for practicing Metasploit and general network pentesting.
https://sourceforge.net/projects/metasploitable/
Metasploitable 3
Updated intentionally vulnerable VM with both Windows and Linux versions. More
complex than v2 with additional attack scenarios.
https://github.com/rapid7/metasploitable3
VulnHub
Repository of downloadable vulnerable VMs for offline practice. Hundreds of
machines across various difficulty levels. Excellent for building pentest methodology.
https://www.vulnhub.com
Hack The Box
Online platform with 200+ machines (active and retired) for penetration testing
practice. Includes Starting Point for beginners, Pro Labs for advanced scenarios, and
seasonal challenges.
https://www.hackthebox.com
TryHackMe
Browser-based guided learning platform with 600+ rooms covering networking,
pentesting, web security, privilege escalation, and more. Structured learning paths.
Excellent for beginners.
https://tryhackme.com
DVRF (Damn Vulnerable Router Firmware)
Intentionally vulnerable firmware image for practicing IoT/embedded device
exploitation. Covers buffer overflows, command injection, and firmware analysis.
https://github.com/praetorian-inc/DVRF
Vulnserver
A vulnerable TCP server for Windows used to learn software exploitation, specifically
buffer overflow attacks and exploit development.
https://github.com/stephenbradshaw/vulnserver
Exploit Education (Phoenix, Protostar, Nebula)
Series of VMs designed for learning binary exploitation and privilege escalation.
Progressive difficulty from basic to advanced.
https://exploit.education
Mobile Security Labs (6)
DVIA (Damn Vulnerable iOS App)
Intentionally vulnerable iOS application covering runtime manipulation, jailbreak
detection bypass, transport layer security, and local data storage issues.
https://github.com/prateek147/DVIA-v2
InsecureBankv2
Vulnerable Android app for security testing. Covers common mobile vulnerabilities
including insecure data storage, weak crypto, and authentication issues.
https://github.com/dineshshetty/Android-InsecureBankv2
Damn Vulnerable Bank
Intentionally vulnerable Android banking application built with modern architecture for
mobile pentesting practice.
https://github.com/nicholasaleks/Damn-Vulnerable-Bank
OWASP MSTG (UnCrackable Apps)
OWASP Mobile Security Testing Guide challenge apps. Android and iOS apps with
reverse engineering and tampering challenges.
https://github.com/OWASP/owasp-mastg
InjuredAndroid
Vulnerable Android application with CTF-style challenges covering various Android
security vulnerabilities. Built in Kotlin.
https://github.com/B3nac/InjuredAndroid
AndroGoat
Intentionally vulnerable Android app built in Kotlin for practicing mobile security
testing.
https://github.com/satishpatnayak/AndroGoat
AI & LLM Security Labs (4)
Damn Vulnerable LLM Project
Intentionally vulnerable LLM application for practicing LLM-specific security testing:
prompt injection, data leakage, hallucination exploitation, and more.
https://github.com/harishsg993010/DamnVulnerableLLMProject
Damn Vulnerable LLM Agent
Vulnerable LLM agent application for testing agent-specific vulnerabilities: tool abuse,
prompt injection through tool outputs, and unauthorized actions.
https://github.com/WithSecureLabs/damn-vulnerable-llm-agent
Vulnerable Banking App with LLM
Banking application integrating LLM capabilities with intentional vulnerabilities at the
intersection of traditional web security and AI security.
https://github.com/Commando-X/vuln-bank
Gandalf (Lakera)
Online interactive challenge to practice prompt injection attacks against an LLM
guarding a secret password. Multiple levels of increasing difficulty.
https://gandalf.lakera.ai
CTF Platforms & Wargames (12)
Hack The Box
Premier online pentesting platform with machines, challenges, Pro Labs, and ranked
CTF competitions. Active community with write-ups and discussions.
https://www.hackthebox.com
TryHackMe
Guided learning platform with structured paths for beginners through advanced.
Browser-based VMs. Topics span the full security spectrum.
https://tryhackme.com
PicoCTF
Free beginner-friendly CTF by Carnegie Mellon University. Excellent entry point with
progressive difficulty. Runs annual competition and has practice challenges year-
round.
https://picoctf.org
OverTheWire (Bandit, Natas, Leviathan)
Classic wargames for learning Linux, web security, and binary exploitation. Bandit is
the quintessential starting point for command line and SSH skills.
https://overthewire.org/wargames
CTFtime
Global CTF event tracker and team rankings. Calendar of upcoming competitions,
past CTF write-ups, and team registration. The hub for competitive CTF.
https://ctftime.org
RingZer0 CTF
Online CTF platform with 400+ challenges covering cryptography, reverse
engineering, steganography, web, and forensics.
https://ringzer0ctf.com
Root Me
Free platform with 500+ hacking challenges and 80+ virtual environments across
web, network, cryptography, forensics, and programming.
https://www.root-me.org
CyberDefenders
Blue team focused CTF platform. Practice DFIR, log analysis, malware analysis, and
threat hunting with realistic challenge scenarios.
https://cyberdefenders.org
LetsDefend
SOC analyst training platform with realistic alerts, SIEM access, and investigation
workflows. Browser-based with guided and unguided challenges.
https://letsdefend.io
Pwnable.kr / Pwnable.tw
Binary exploitation wargames focusing on memory corruption, reverse engineering,
and exploit development. Progressive difficulty.
https://pwnable.kr
CryptoHack
Free platform for learning modern cryptography through challenges. Covers AES,
RSA, elliptic curves, hash functions, and more.
https://cryptohack.org
SANS Holiday Hack / KringleCon
Free annual CTF by SANS with diverse challenges spanning web, OSINT, crypto,
cloud, and more. Fun holiday-themed storyline.
https://www.holidayhackchallenge.com
RED TEAM LEADERS
C Y B E R S E C U R I T Y  T R A I N I N G
78 labs & platforms across 9 categories.
Your offensive security practice ground.
Build. Break. Learn. Repeat.
w w w . r e d t e a m l e a d e r s . c o m  |  ©  2 0 2 5  R e d  Te a m  L e a d e r s .
