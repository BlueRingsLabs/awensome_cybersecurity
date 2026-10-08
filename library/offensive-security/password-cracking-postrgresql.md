---
id: ckb-f262db7706a3
title: Password Cracking Postrgresql
category: offensive-security
format: guide
language: en
tags: [databases, mitre-attack, nmap, password-security, red-team]
summary: A technical guide covering enumeration and brute-force techniques against PostgreSQL databases, including defensive strategies and MITRE ATT&CK mapping.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-26b-a4b-it
  confidence: 0.95
classified_by: google:gemma-4-26b-a4b-it@2026-10-08T00:48:01Z
---

Password Cracking: PostgreSQL

                                                                                                 1 | P a g e

Password Cracking: PostgreSQL

                                                                                                 2 | P a g e

Contents
IntroducƟon ............................................................................................................................................ 3
MITRE ATT&CK Techniques ............................................................................................................. 3
IntroducƟon to PostgreSQL (Port 5432) .................................................................................................. 3
EnumeraƟon............................................................................................................................................ 3
Nmap Scan .......................................................................................................................................... 3
Defensive Strategy: ......................................................................................................................... 3
Brute-Force Techniques .......................................................................................................................... 4
Tools Quick Reference ......................................................................................................................... 4
Hydra ................................................................................................................................................... 4
Step To Reproduce .......................................................................................................................... 4
DetecƟon Strategy: ......................................................................................................................... 4
Metasploit ........................................................................................................................................... 4
Step To Reproduce .......................................................................................................................... 5
Defensive Control: ........................................................................................................................... 5
Medusa ............................................................................................................................................... 5
Step To Reproduce .......................................................................................................................... 5
Defensive Strategy: ......................................................................................................................... 6
Ncrack ................................................................................................................................................. 6
Step To Reproduce .......................................................................................................................... 6
Defensive Strategy: ......................................................................................................................... 6
Patator ................................................................................................................................................. 6
Step To Reproduce .......................................................................................................................... 6
Defensive SuggesƟon: ..................................................................................................................... 7
NMAP NSE Script ................................................................................................................................. 7
Step To Reproduce .......................................................................................................................... 8
Defensive Strategy: ......................................................................................................................... 8
BruteSpray ........................................................................................................................................... 8
Defensive Strategy: ....................................................................................................................... 11
PostgreSQL Brute-Force – Oﬀense, Defense & MITRE Mapping ........................................................... 11
Defense-in-Depth Summary .................................................................................................................. 11

Password Cracking: PostgreSQL

                                                                                                 3 | P a g e

Introduction
This arƟcle covers how to idenƟfy and brute force PostgreSQL logins using common tools, from quick
single host tests to automated mulƟ host atacks during internal assessments.
MITRE ATT&CK Techniques
•
T1110.001 – Brute Force: Password Guessing
•
T1046 – Network Service Scanning
•
T1078 – Valid Accounts
Introduction to PostgreSQL (Port 5432)
PostgreSQL is a robust open-source database typically running on port 5432. It uses password-based
authenƟcaƟon and is vulnerable to brute force atacks if exposed to untrusted networks or
misconﬁgured.
Enumeration
Nmap Scan
Run an Nmap scan to discover open PostgreSQL services and detect version info:
nmap -p 5432 -sV 192.168.1.13
ExplanaƟon:
•
-p 5432: Scans for the default PostgreSQL Service on port 5432.
•
-sV: Enables version detecƟon to idenƟfy the speciﬁc PostgreSQL version running on the
target host.
Once Nmap conﬁrms that port 5432 is open and a PostgreSQL service is acƟve, this informaƟon can
be used to select appropriate brute force tools, script modules, or potenƟal version-based
vulnerabiliƟes.

Defensive Strategy:
Use IDS/IPS to ﬂag scans. Restrict PostgreSQL access to known IP ranges using ﬁrewalls.
Password Cracking: PostgreSQL

                                                                                                 4 | P a g e

Brute-Force Techniques
Tools Quick Reference

Hydra
Hydra is a powerful tool used for brute-force atacks. It's oŌen used to test PostgreSQL logins. It
works with username and password lists (user.txt and pass.txt) to quickly try logging in to exposed
services. This makes it helpful for ﬁnding weak or default passwords.
Step To Reproduce
Brute-force PostgreSQL with parallel login atempts using username and password lists by running
following command
hydra -L users.txt -P pass.txt 192.168.1.13 postgres
ExplanaƟon:
•
-L user.txt: Speciﬁes the path to the username list.
•
-P pass.txt: Speciﬁes the path to the password list.
•
192.168.1.13: Target IP address.
•
postgres: Protocol to atack.

Detection Strategy:
Enable log_connecƟons and log_failed_login_atempts in PostgreSQL. Apply IP based throtling via
fail2ban or ﬁrewalls. Monitor failed login bursts via SIEM.
Metasploit
Metasploit oﬀers a dedicated module for brute forcing PostgreSQL logins, ideal for red team use.
With support for user.txt and pass.txt, it enables structured, automated atempts that integrate well
into post exploitaƟon workﬂows.

Password Cracking: PostgreSQL

                                                                                                 5 | P a g e

Step To Reproduce
msf6 > use auxiliary/scanner/postgres/postgres_login
set rhosts 192.168.1.13
set user_file users.txt
set pass_file pass.txt
set verbose false
run
ExplanaƟon:
•
use auxiliary/scanner/postgres/postgres_login: Loads the PostgreSQL login scanner module
used for brute force authenƟcaƟon.
•
set rhosts 192.168.1.13: Speciﬁes the IP address of the target PostgreSQL server.
•
set user_ﬁle users.txt: Deﬁnes the ﬁle containing potenƟal usernames.
•
set pass_ﬁle pass.txt: Deﬁnes the ﬁle containing passwords to pair with the usernames.
•
set verbose false: Disables verbose output to reduce console noise during the brute force
process.
•
run: Executes the module and begins tesƟng all username password combinaƟons against
the PostgreSQL service.

Defensive Control:
Use pg_hba.conf to restrict access to known IP ranges. Enable PostgreSQL logging (log_connecƟons,
log_disconnecƟons) and integrate with SIEM tools for correlaƟon and alerƟng.
Medusa
Medusa is a fast tool made for trying many username and password combinaƟons. It's useful for
tesƟng PostgreSQL login. It can handle large lists (like user.txt and pass.txt) at the same Ɵme, which
makes it quick and eﬀecƟve for tesƟng inside networks. Its results are simple and can be used easily
in other tools or scripts.
Step To Reproduce
Below we have successfully grabbed credenƟals using the following command:
medusa -h 192.168.1.13 -U users.txt -P pass.txt -M postgres | grep SUCCESS
ExplanaƟon:
•
medusa: Invokes the Medusa brute force tool.
•
-h 192.168.1.13: Speciﬁes the IP address of the target machine.
•
-U: Points to a ﬁle containing a list of usernames to try.
Password Cracking: PostgreSQL

                                                                                                 6 | P a g e

•
-P: Points to a ﬁle containing a list of passwords.
•
-M postgres: Indicates that the PostgreSQL module should be used for this atack.
•
|grep SUCCESS: Filters the command output to display only successful login atempts,
making it easier to idenƟfy valid credenƟals.

Defensive Strategy:
Use SIEM to detect bursts of login atempts. Enable rate limiƟng via PostgreSQL middleware (e.g.,
pgBouncer). Enforce account lockout policies where possible.
Ncrack
Ncrack, developed by the creators of Nmap, is a high-speed tool for tesƟng PostgreSQL logins across
large environments. Its mulƟ-threaded design enables quick credenƟal checks, making it eﬀecƟve for
spoƫng reused or default passwords in enterprise deployments.
Step To Reproduce
Use Ncrack to perform high speed PostgreSQL login tesƟng on a target IP.
ncrack -U user.txt -P pass.txt 192.168.1.13 -p 5432
ExplanaƟon:
•
ncrack: Launches the Ncrack password cracking tool.
•
-U user.txt: Indicates the ﬁle containing a list of potenƟal usernames.
•
-P pass.txt: Indicates the ﬁle containing a list of potenƟal passwords.
•
-p 5432: Speciﬁes the PostgreSQL default port for authenƟcaƟon atempts.

Defensive Strategy:
Use PostgreSQL’s naƟve logging to detect rapid logins. Limit connecƟon rates per IP. Implement
ﬁrewall-based IP ﬁltering and alert on excessive connecƟon atempts.
Patator
Patator is a ﬂexible tool used for brute-force atacks. It can try to log in to PostgreSQL servers. It has
features like smart error handling, custom retry opƟons, and adjustable delays between atempts.
These features help avoid detecƟon and make it useful when you need to stay hidden.
Step To Reproduce
Launch adapƟve brute force atempts against PostgreSQL using Patator by running following
command
patator pgsql_login host=192.168.1.13 user=FILE0 0=users.txt password=FILE1 1=pass.txt
Password Cracking: PostgreSQL

                                                                                                 7 | P a g e

ExplanaƟon:
•
patator: Launches the Patator brute force tool.
•
pgsql_login: Speciﬁes the module for PostgreSQL login atempts.
•
host=192.168.1.13: Indicates the target machine’s IP address.
•
user=FILE0 0=user.txt: Assigns FILE0 as a placeholder for usernames, pulling values from
user.txt.
•
password=FILE1 1=pass.txt: Assigns FILE1 as a placeholder for passwords, pulling values
from pass.txt.

Note: You can add | grep ‘200 OK’ or -x ignore:code=530 for success ﬁltering or to skip known failed
responses based on Patator’s output codes.
Defensive Suggestion:
Monitor PostgreSQL for repeƟƟve failed login paterns. Use network level throtling. Detect Patator’s
retry logic via behavioral SIEM correlaƟon.
NMAP NSE Script
Nmap is a powerful tool for scanning and gathering informaƟon about systems. It supports scripts
through something called the Nmap ScripƟng Engine (NSE). One script, pgsql-brute, is used to try
many usernames and passwords to break into PostgreSQL servers using your own wordlists.
This script is parƟcularly eﬀecƟve during early discovery phases to check for weak credenƟals directly
in conjuncƟon with version and port scanning.
Password Cracking: PostgreSQL

                                                                                                 8 | P a g e

Step To Reproduce
Perform brute force login tesƟng on PostgreSQL directly from Nmap using NSE by running following
command
nmap -p5432 --script pgsql-brute.nse --script-args userdb=users.txt,passdb=pass.txt 192.168.1.13
ExplanaƟon:
•
–p5432: Scans the default port used by PostgreSQL.
•
–script pgsql-brute.nse: Speciﬁes the use of the PostgreSQL brute force NSE script.
•
–script-args userdb=user.txt,passdb=pass.txt: Provides the script with your custom username
and password lists.
This method is especially useful during early-stage reconnaissance to idenƟfy weak or default
PostgreSQL credenƟals on a target system.

Defensive Strategy:
Track login failures originaƟng from Nmap/NSE paterns. Alert on rapid session iniƟaƟons. Limit
PostgreSQL exposure to known IP ranges and apply TLS with authenƟcaƟon.
BruteSpray
BruteSpray helps automate login atempts (credenƟal spraying) on services found using Nmap scans.
It reads Nmap's GNMAP output to ﬁnd PostgreSQL servers and tries to log in using lists of usernames
and passwords (user.txt and pass.txt). It spreads out the atempts to avoid geƫng detected.
Steps To Reproduce:
Spray credenƟals across mulƟple PostgreSQL hosts parsed from an Nmap GNMAP ﬁle. Scan and save
output to a ﬁle to later use with BruteSpray by running following command
Nmap -p 5432 192.168.1.13 -oG pgsql_scan.txt
ExplanaƟon:
•
nmap: Network scanning tool used to discover hosts and services.
•
-p 5432: Scans only port 5432, the default port for PostgreSQL.
•
192.168.1.13: Target IP address to scan.
•
-oG pgsql_scan.txt: Saves the scan output in grepable format to the ﬁle pgsql_scan.txt.
Password Cracking: PostgreSQL

                                                                                                 9 | P a g e

brutespray -f pgsql_scan.txt -u users.txt -p pass.txt
ExplanaƟon:
•
brutespray: launches BruteSpray tool for automated credenƟal spraying
•
-f pgsql_scan.txt: Speciﬁes the Nmap output ﬁle to use.
•
-u user.txt: Path to the list of usernames.
•
-p pass.txt: Path to the list of passwords.
Password Cracking: PostgreSQL

                                                                                                 10 | P a g e

Password Cracking: PostgreSQL

                                                                                                 11 | P a g e

Defensive Strategy:
Analyze PostgreSQL logs across systems for distributed spray atempts. Use correlaƟon in SIEM tools.
Implement connecƟon throtling via proxy layers or PostgreSQL middleware.
PostgreSQL Brute-Force – Offense, Defense & MITRE Mapping

Defense-in-Depth Summary

JOIN OUR
TRAINING PROGRAMS
www.ignitetechnologies.in
BEGINNER
Network Pentest
Bug Bounty
Wireless Pentest
Network Security
Essentials
Ethical Hacking
ADVANCED
EXPERT
Burp Suite Pro
CTF
Windows
Linux
Pro
Infrastructure VAPT
APT’s - MITRE Attack Tactics
MSSQL Security Assessment
Active Directory Attack
Red Team Operation
Privilege Escalation
Web
Services-API
Android Pentest
Computer
Forensics
Advanced
Metasploit
CLICK HERE
