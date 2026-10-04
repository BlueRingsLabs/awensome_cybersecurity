---
id: ckb-38174e420ce2
title: Red Team Tradecraft Complete Guide
category: offensive-security
format: guide
language: en
tags: [active-directory, azure, c2, cloud, evasion, red-team]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.74
---

RED TEAM
TRADECRAFT
C O M P L E T E  G U I D E
Master the art of covert offensive operations. Advanced techniques for
operational security, evasion, persistence, and stealth in modern adversary
simulation.
R E D  T E A M  L E A D E R S    |    C Y B E R S E C U R I T Y  T R A I N I N G    |    2 0 2 5  E D I T I O N
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
1/22
Table of Contents
01 What is Tradecraft?
3
Defining Red Team Tradecraft / The Tradecraft Pillars
3
02 Operational Security (OPSEC)
4
Identity Separation / Infrastructure OPSEC / Communication Security
4
03 Infrastructure Tradecraft
6
C2 Architecture / Redirectors / Domain Fronting / DNS over HTTPS
6
04 Phishing & Social Engineering Tradecraft
8
Pretext Development / Email Infrastructure / Payload Delivery
8
05 Payload & Evasion Tradecraft
10
EDR Evasion / Shellcode Loading / Memory Tradecraft / ETW & AMSI
10
06 Living Off the Land (LOL)
12
LOLBins / LOLDrivers / LOLBAS / Trusted Tool Abuse
12
07 Credential Tradecraft
13
Credential Harvesting / Token Manipulation / Kerberos Attacks
13
08 Lateral Movement Tradecraft
15
Covert Channels / Protocol Abuse / Pivoting Techniques
15
09 Active Directory Tradecraft
16
ACL Abuse / Delegation Attacks / Forest Trust Exploitation
16
10 Cloud Tradecraft
17
AWS / Azure / GCP Attack Patterns
17
11 Anti-Forensics & Cleanup
18
12 Tradecraft Maturity & Continuous Development
19
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
2/22
01
What is Tradecraft?
Defining Red Team Tradecraft
Tradecraft is the collection of techniques, procedures, and disciplines that enable a red team
operator to conduct offensive operations while remaining undetected. It is the difference
between simply exploiting a vulnerability and doing so in a way that mirrors a real-world
advanced persistent threat (APT) — silently, methodically, and with purpose.
While tools and exploits change constantly, tradecraft is a timeless discipline rooted in
operational planning, attention to detail, and a deep understanding of how defenders detect
and respond to threats. A skilled operator with strong tradecraft and basic tools will consistently
outperform a novice with the most advanced toolkit available.
"Tradecraft is not about the tools you use — it is about how you use them. It is the discipline of remaining
invisible while achieving your objectives in a hostile environment."
— Offensive Security Principle
The Tradecraft Pillars
Effective red team tradecraft rests on five interconnected pillars. Weakness in any single pillar
can compromise an entire operation.
1. Operational Security
Protecting the operation itself. Identity separation,
infrastructure isolation, communication security, and
evidence management.
2. Stealth & Evasion
Avoiding detection by EDR, SIEM, SOC analysts, and
automated defense systems. Blending in with legitimate
activity.
3. Persistence & Resilience
Maintaining access despite credential rotations, patch
cycles, and active threat hunting. Multiple redundant
footholds.
4. Situational Awareness
Understanding the environment, active defenses, logged
telemetry, and detection thresholds before taking action.
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
3/22
THE FIFTH PILLAR: ADAPTABILITY
The most critical tradecraft skill is the ability to adapt in real-time. When a technique is
detected, an operator must immediately pivot to an alternative approach without losing
composure or operational momentum. Pre-planned contingencies and deep knowledge
of multiple attack paths make this possible.
Tradecraft vs. Tool Proficiency
Many aspiring red teamers conflate tool proficiency with tradecraft. Knowing how to run Cobalt
Strike or Mimikatz is tool proficiency. Knowing when to use them, how to modify their
signatures, which logging they trigger, and what alternatives exist when they are blocked —
that is tradecraft. The most dangerous operators are those who can achieve objectives using
nothing but native operating system utilities and built-in administrative tools.
02
Operational Security (OPSEC)
The Foundation of Every Operation
Operational security is the discipline of protecting your operation from compromise. In red
teaming, a single OPSEC failure can burn the entire engagement — alerting defenders,
invalidating findings, and potentially exposing sensitive infrastructure to real adversaries.
OPSEC must be ingrained in every action, from the first domain purchase to the final report
delivery.
Identity Separation
Every red team engagement requires complete separation between the operator's real identity
and their operational persona. This separation must be maintained across all layers — digital,
physical, and social.
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
4/22
Identity Separation Checklist
Infrastructure OPSEC
Red team infrastructure is a high-value target — for the blue team during the engagement and
for real threat actors at all times. Every component must be deployed with security in mind.
Domain Hygiene
Purchase domains months in advance. Age them with
benign content. Use privacy registration. Categorize
domains through web proxies before operational use.
Never reuse domains across engagements.
Server Hardening
Minimal services running. SSH key-only authentication.
Firewall rules limiting access to known operator IPs.
Disable unnecessary logging to third parties. Encrypt all
disks.
Traffic Separation
Different servers for C2, phishing, payload hosting, and
data staging. Compromise of one component should not
expose others. Use different hosting providers for each
layer.
Ephemeral Infrastructure
Automate
infrastructure
deployment
with
Terraform/Ansible. Tear down and rebuild between
engagements. No persistent data between operations.
Infrastructure as Code for reproducibility.
Communication Security
All team communications related to an engagement must be encrypted end-to-end. Use
dedicated, encrypted channels separate from personal messaging. Avoid discussing specific
technical details (IP addresses, credentials, targets) over unencrypted channels. Establish
code words for sensitive topics when voice communication is necessary. Store all engagement
artifacts in encrypted containers with access limited to authorized team members.
Dedicated Hardware: Use separate laptops for offensive operations — never your personal device
▸
Separate Accounts: Distinct email addresses, cloud accounts, and payment methods for each
engagement
▸
VPN Layering: Commercial VPN as a base layer, then operational VPN or proxy. Never connect to
offensive infrastructure from your home IP
▸
Browser Isolation: Dedicated browser profiles with no cookies, history, or autofill from personal use
▸
Phone Separation: Burner phones or VoIP numbers for any engagement-related communication
▸
Social Media: Never research targets from accounts linked to your real identity
▸
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
5/22
⚠ Common OPSEC Failures
03
Infrastructure Tradecraft
C2 Architecture Design
A mature C2 architecture is layered, resilient, and designed to survive the loss of any single
component. The key principle is separation of concern: no single server should handle multiple
operational functions.
Redirectors & Traffic Shaping
Redirectors are the disposable front-end layer that protects the actual team server. They
forward legitimate C2 traffic to the team server while filtering or redirecting security
Connecting to C2 infrastructure from a home IP or office network
▸
Reusing domains, payloads, or infrastructure from previous engagements
▸
Discussing engagement details in unencrypted Slack, Teams, or email
▸
Using personal accounts to register operational infrastructure
▸
Forgetting to rotate SSH keys and API tokens between engagements
▸
Leaving operational logs on shared infrastructure after engagement
▸
Tier 1 — Long-Haul C2
Low-and-slow beaconing (12–24 hour intervals). Used for persistent access that survives short-term operations. DNS-based or
HTTPS with legitimate-looking traffic patterns. Never used for interactive operations.
Tier 2 — Standard C2
Regular beaconing (1–60 minute intervals). Primary operational channel for tasking and data collection. HTTPS with domain
fronting or CDN-based communication. Rotated periodically throughout the engagement.
Tier 3 — Interactive C2
Near real-time communication for active operations (port scanning, pivoting, interactive sessions). Short-lived sessions,
brought up only when needed and torn down immediately after. Most likely to be detected.
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
6/22
researchers, scanners, and blue team investigators to benign content.
REDIRECTOR TYPE
TECHNOLOGY
USE CASE
COMPLEXITY
HTTP/S Reverse Proxy
Nginx, Apache, Caddy
Standard web C2 traffic
Low
CDN-Based
CloudFront, Azure CDN
Domain fronting, high trust
Medium
DNS Redirector
socat, iptables
DNS-based C2 channels
Low
Serverless Functions
Lambda, Azure Functions
Ephemeral, hard to attribute
Medium
Legitimate Services
Slack API, Teams, GitHub
Blends with normal business traffic
High
Domain Fronting & CDN Abuse
Domain fronting allows C2 traffic to appear as though it is communicating with a legitimate,
high-reputation domain while the actual traffic is routed to the attacker's server. The technique
leverages the difference between the SNI (Server Name Indication) in the TLS handshake and
the Host header in the HTTP request. While many cloud providers have restricted this
technique, variations remain viable using CDN routing configurations, cloud function endpoints,
and trusted third-party services.
DNS over HTTPS (DoH) for C2
DNS over HTTPS provides an encrypted channel that is extremely difficult to inspect. By
embedding C2 communications within DoH queries to legitimate resolvers (Cloudflare,
Google), traffic becomes nearly indistinguishable from normal encrypted DNS resolution. This
technique requires custom tooling to encode and decode C2 data within DNS query and
response payloads, but offers exceptional stealth against network monitoring.
MALLEABLE C2 PROFILES
For tools like Cobalt Strike, malleable C2 profiles are essential tradecraft. These profiles
customize every aspect of beacon communication — HTTP headers, URIs, body
encoding, certificates, and timing — to mimic legitimate application traffic (e.g., Microsoft
Teams, Slack, or Office 365 API calls). A well-crafted malleable profile can survive deep
packet inspection and network behavioral analysis.
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
7/22
04
Phishing & Social Engineering Tradecraft
Pretext Development
The pretext is the story that makes the target take action. A convincing pretext is built on
thorough OSINT and mirrors scenarios the target encounters in their daily work. The best
pretexts create a sense of urgency without raising suspicion.
Authority-Based
Impersonating IT support, HR, legal, or executive
leadership. Leverages organizational hierarchy and
compliance instincts. Requires accurate knowledge of
internal processes and naming conventions.
Urgency-Based
Password expiration, security incident, invoice past-due,
delivery notification. Creates time pressure that overrides
critical thinking. Must feel natural and timely.
Curiosity-Based
Shared
document,
meeting
notes,
salary
review,
organizational changes. Appeals to human curiosity about
information that seems personally relevant.
Relationship-Based
Impersonating known contacts, vendors, or partners.
Requires extensive OSINT to identify relationships and
communication patterns. Highest success rate but most
preparation.
Email Infrastructure Tradecraft
A phishing email is only as good as its ability to reach the inbox. Modern email security stacks
(Microsoft Defender, Proofpoint, Mimecast) inspect sender reputation, authentication records,
link reputation, and content patterns. Proper email infrastructure setup is essential.
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
8/22
Email Delivery Checklist
Payload Delivery Tradecraft
Getting a payload past email gateways requires understanding what triggers detection:
executable attachments, known macro patterns, suspicious URLs, and content analysis.
Modern tradecraft employs HTML smuggling (embedding encoded payloads in HTML
attachments that reassemble client-side), password-protected archives (bypass automated
sandbox analysis), QR code phishing (redirect to mobile-based credential harvesting), and
legitimate file-sharing platforms (OneDrive, SharePoint, Google Drive links that bypass URL
reputation checks).
⚠ Vishing Tradecraft
Voice phishing is underestimated but highly effective. Preparation includes: researching the target's communication
style, understanding internal terminology, spoofing caller ID to display legitimate internal numbers, and rehearsing the
scenario. Record calls (with legal authorization) for debrief and reporting. Always have a natural exit strategy if the
target becomes suspicious.
05
Payload & Evasion Tradecraft
SPF Record: Configure Sender Policy Framework to authorize your sending IP
▸
DKIM Signing: Enable DomainKeys Identified Mail for cryptographic authentication
▸
DMARC Policy: Set up DMARC to pass alignment checks (p=none initially, then quarantine)
▸
Domain Age: Age domains for minimum 30 days with benign web content and light email traffic
▸
IP Warm-up: Gradually increase email volume from new IPs to build sender reputation
▸
Categorization: Submit domains to web proxy categorization services (Business, Technology) before
use
▸
SSL Certificate: Valid TLS certificate on the sending mail server and any linked pages
▸
Reverse DNS: Configure PTR records matching the sending domain
▸
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
9/22
Understanding the Detection Landscape
Modern endpoint detection and response (EDR) solutions combine multiple detection engines:
signature matching, behavioral analysis, memory scanning, machine learning classifiers, and
cloud-based detonation. Effective evasion requires understanding — and defeating — each
layer independently. A payload that evades signatures but triggers behavioral detection
provides zero operational value.
Shellcode Loading Techniques
The shellcode loader is the most critical component of any implant. Its job is to execute
arbitrary code in memory while evading static and runtime detection. Modern loaders must
handle API resolution, memory allocation, execution, and cleanup.
TECHNIQUE
EVASION LEVEL
COMPLEXITY
DETECTION VECTOR
Direct Syscalls
High
High
Syscall instruction detection
Indirect Syscalls
Very High
Very High
Stack analysis, call origin
Module Stomping
High
Medium
Memory section inconsistency
Process Hollowing
Medium
Medium
Process image mismatch
Thread Pool Injection
High
High
Thread start address analysis
Callback-Based Execution
High
Medium
Callback origin analysis
Fiber-Based Execution
Very High
High
Fiber enumeration (rare)
Memory Tradecraft
Once code is executing in memory, it remains vulnerable to memory scanning by EDR.
Advanced tradecraft employs several techniques to protect in-memory payloads from
detection.
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
10/22
Memory Protection Techniques
ETW & AMSI Evasion
Event Tracing for Windows (ETW) feeds telemetry directly to EDR solutions. AMSI
(Antimalware Scan Interface) inspects scripts and .NET assemblies at runtime. Both must be
addressed for effective operations. Techniques include patching ETW provider registration
functions, unhooking AMSI scan buffers, and using hardware breakpoint-based bypasses that
avoid modifying code sections (which themselves generate telemetry). The key tradecraft
principle: understand what each sensor reports and disable only what is necessary for your
specific operation.
PAYLOAD TESTING PROTOCOL
Never test payloads against online scanners (VirusTotal, AntiScan.me) — samples are
shared with security vendors. Maintain an internal testing lab with the same EDR
products deployed at the target. Test against multiple detection layers independently:
static analysis, dynamic analysis, memory scanning, and behavioral detection.
Document what triggers detection and iterate.
Sleep Obfuscation: Encrypt the payload in memory during beacon sleep intervals (Ekko, Foliage,
Nighthawk-style). The payload is only decrypted momentarily when active
▸
Stack Spoofing: Modify the call stack during sleep to hide the beacon's true return address. Makes
stack-walking detection ineffective
▸
Heap Encryption: Encrypt heap allocations containing sensitive data (configuration, task results)
when not in active use
▸
RX-to-RW Toggling: Switch memory page permissions between execute and read-write based on
current need, avoiding persistent RWX allocations
▸
Module Overloading: Load the payload over a legitimate DLL's memory space to appear as a normal
module in memory scans
▸
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
11/22
06
Living Off the Land (LOL)
The Philosophy of LOL
Living Off the Land is the tradecraft principle of using tools, binaries, and features already
present in the target environment to achieve offensive objectives. Because these tools are
legitimate, signed by Microsoft or other trusted vendors, and routinely used by administrators,
their execution generates minimal suspicion in security monitoring.
LOLBins — Living Off the Land Binaries
LOLBins are legitimate system binaries that can be repurposed for offensive operations. They
are signed, trusted, and present on every Windows installation.
BINARY
OFFENSIVE USE
MITRE TECHNIQUE
certutil.exe
File download, Base64 encode/decode
T1105, T1140
mshta.exe
Execute HTA payloads, proxy execution
T1218.005
rundll32.exe
Execute DLL exports, proxy execution
T1218.011
regsvr32.exe
Execute COM scriptlets remotely
T1218.010
wmic.exe
Remote execution, recon, process creation
T1047
msiexec.exe
Execute MSI payloads from remote URLs
T1218.007
bitsadmin.exe
File download with BITS jobs
T1197
cmstp.exe
UAC bypass, proxy execution
T1218.003
LOLDrivers — Bring Your Own Vulnerable Driver
Kernel-level access can be achieved by loading legitimate but vulnerable signed drivers. These
drivers contain exploitable vulnerabilities that allow an attacker to read/write kernel memory,
disable EDR kernel callbacks, and achieve ring-0 execution. This technique bypasses driver
signature enforcement because the drivers carry valid, trusted signatures. Maintain an internal
database of vulnerable drivers mapped to specific EDR products for targeted operations.
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
12/22
PowerShell Tradecraft
PowerShell remains a powerful operational tool despite increased monitoring. Tradecraft
includes using PowerShell in Constrained Language Mode bypasses, running through the
.NET System.Management.Automation API directly (avoiding powershell.exe entirely), using
unmanaged PowerShell runspaces from C# or BOFs, and leveraging PowerShell classes
without invoking Invoke-Expression or other commonly monitored cmdlets. The key is to
achieve PowerShell functionality without triggering ScriptBlock Logging, Module Logging, or
AMSI inspection.
07
Credential Tradecraft
Credential Harvesting Hierarchy
Credentials are the keys to the kingdom in any enterprise environment. Tradecraft dictates that
operators prioritize stealthy credential harvesting techniques over noisy approaches, always
considering what telemetry each method generates.
1. Passive Harvesting (Lowest Risk)
Capturing credentials from network traffic: LLMNR/NBT-NS poisoning, MITM6, ARP spoofing. No direct interaction with target
hosts. Detectable only through network monitoring.
2. Targeted Phishing (Low Risk)
Credential harvesting through targeted phishing pages mimicking SSO portals, VPN logins, or internal applications. Evilginx2
for MFA bypass via real-time proxy.
3. Kerberos Attacks (Medium Risk)
Kerberoasting (requesting TGS tickets for service accounts), AS-REP roasting (targeting accounts without pre-authentication).
Offline cracking generates no further telemetry.
4. LSASS Access (Higher Risk)
Dumping credentials from LSASS process memory. Highly monitored by EDR. Requires process handle, memory read
capabilities. Use alternatives: MiniDumpWriteDump via custom tools, direct memory reads, or LSASS cloning techniques.
5. NTDS.dit Extraction (Highest Impact)
Extracting the entire Active Directory database. Requires domain controller access. Techniques: DCSync (replication protocol),
Volume Shadow Copy, ntdsutil. Provides all domain password hashes.
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
13/22
Token Manipulation
Rather than cracking or stealing passwords, token manipulation allows operators to
impersonate other users by stealing or duplicating their authentication tokens. This is often
stealthier than traditional credential theft.
Token Impersonation
Duplicate tokens from processes running as target users.
Requires SeImpersonatePrivilege (common for service
accounts). Allows actions as the impersonated user
without knowing their password.
Token Theft via Handle Duplication
Open handles to processes running as target users and
duplicate their token. Less monitored than direct LSASS
access. Works across security contexts.
Kerberos Advanced Tradecraft
Beyond basic Kerberoasting, advanced Kerberos tradecraft includes: Silver Tickets (forged
TGS for specific services, avoiding KDC interaction), Golden Tickets (forged TGT granting
domain-wide access for up to 10 years), Diamond Tickets (modifying legitimate TGTs to
include arbitrary group memberships — harder to detect than Golden Tickets), and targeted
delegation
abuse
(exploiting
constrained/unconstrained/resource-based
constrained
delegation to impersonate privileged users against specific services).
⚠ Credential OPSEC
Never crack credentials on the target's infrastructure. Exfiltrate hashes to your own systems for offline cracking. Use
rule-based attacks informed by the target's password policy. Avoid spraying more than 1–2 passwords per account per
hour to stay below lockout thresholds. Track which credentials have been tried to avoid duplicate attempts.
08
Lateral Movement Tradecraft
Choosing the Right Technique
Lateral movement is the highest-risk phase of any engagement. Each technique generates
distinct telemetry, and the choice must be informed by what security tools are deployed and
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
14/22
what logging is enabled. The operator's tradecraft determines whether movement is invisible or
triggers an immediate incident response.
TECHNIQUE
TELEMETRY GENERATED
EDR VISIBILITY
BEST USED WHEN
WMI
Event 4648, process creation
Medium
Sysmon not deployed, WMI logging limited
WinRM
Event 4648, 91, PowerShell logs
Medium-High
PS Remoting is common in environment
DCOM (MMC20)
DCOM connection events
Low
Uncommon in monitoring rules
SSH
Auth logs, session events
Low
Linux/hybrid environments
RDP (SharpRDP)
Logon event 4624 type 10
Medium
RDP is normal admin activity
SMB + Service
7045, 4697, named pipe
High
Only when other methods unavailable
Covert Channels & Pivoting
When standard lateral movement protocols are monitored, operators must establish covert
channels that tunnel through allowed traffic. This includes SSH tunneling through compromised
Linux hosts, SOCKS proxying over C2 channels (Cobalt Strike's socks command), DNS
tunneling for crossing network segments, and named pipe pivoting within Windows
environments. The choice of pivoting technique depends on what protocols are allowed
between network segments and what monitoring exists at the boundaries.
LATERAL MOVEMENT OPSEC RULES
Always enumerate the target host remotely before connecting — identify EDR product, logged-on
users, running services
▸
Move during business hours when administrative activity is expected and generates less scrutiny
▸
Use the same protocols that administrators in the environment routinely use
▸
Avoid touching domain controllers directly when possible — use DCSync or replication-based
techniques instead
▸
Clean up any artifacts (services, scheduled tasks, files) immediately after lateral movement completes
▸
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
15/22
09
Active Directory Tradecraft
ACL-Based Attacks
Active Directory Access Control Lists (ACLs) are a goldmine for red team operators.
Misconfigured permissions on AD objects allow privilege escalation without exploiting any
vulnerability — just abusing legitimate but overly permissive configurations.
Key ACL Attack Paths
Delegation Attacks
Kerberos delegation is one of the most powerful and misunderstood attack surfaces in Active
Directory. Three delegation types create distinct attack opportunities: Unconstrained
Delegation (the compromised server can impersonate ANY user to ANY service — print the
TGT from memory), Constrained Delegation (the server can impersonate users to specified
services — exploit with S4U2Self and S4U2Proxy), and Resource-Based Constrained
Delegation (configurable by the target resource — can be weaponized by any user with write
access to the target's msDS-AllowedToActOnBehalfOfOtherIdentity attribute).
Forest Trust Exploitation
GenericAll: Full control over the target object — reset passwords, modify group membership, write to
any attribute
▸
GenericWrite: Write to non-protected attributes — set SPN for Kerberoasting, modify msDS-
AllowedToActOnBehalfOfOtherIdentity for RBCD
▸
WriteDACL: Modify the object's ACL itself — grant yourself GenericAll, then proceed with any attack
▸
WriteOwner: Take ownership of the object, then modify its DACL to grant full control
▸
ForceChangePassword: Reset the target user's password without knowing the current one
▸
AddMember: Add accounts to security groups, including privileged groups like Domain Admins
▸
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
16/22
When multiple Active Directory forests trust each other, the attack surface expands
dramatically. SID History injection allows forging cross-forest ticket requests with privileged
SIDs. The ExtraSids field in a referral ticket allows claiming membership in groups across the
trust boundary. While SID filtering mitigates some attacks, many organizations disable or
improperly configure these protections, enabling full cross-forest compromise from a single
domain admin position.
10
Cloud Tradecraft
Cloud Attack Surface Overview
Cloud environments present a fundamentally different attack surface than traditional on-
premises infrastructure. Identity is the new perimeter, and misconfiguration is the primary
vulnerability class. Red team tradecraft in cloud environments focuses on IAM exploitation,
service abuse, and lateral movement through cloud-native mechanisms.
AWS Tradecraft
IAM role chaining and assumption. EC2 instance
metadata abuse (IMDSv1 SSRF). Lambda function
environment variable extraction. S3 bucket policy
exploitation. CloudTrail evasion through event selectors.
Cross-account role assumption chains.
Azure Tradecraft
Entra ID (Azure AD) token theft and replay. Managed
Identity abuse. Azure Resource Manager API exploitation.
Key Vault access policy abuse. PRT (Primary Refresh
Token) theft for persistent cloud access. Conditional
Access policy bypass.
Cloud-Specific OPSEC
Cloud environments generate extensive logging that cannot be disabled by the operator
(CloudTrail, Azure Activity Log, GCP Audit Log). Tradecraft must focus on blending in: use API
calls that are common in the environment, operate during business hours, avoid bulk data
downloads that trigger DLP alerts, and understand which actions generate management
events versus data events. Some read-only operations in certain services may not be logged
by default — identify and leverage these blind spots.
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
17/22
HYBRID ENVIRONMENT TRADECRAFT
Most enterprises operate hybrid environments where on-premises AD synchronizes with
cloud identity (Azure AD Connect, AWS SSO). This creates bidirectional attack paths:
compromise on-premises AD to pivot to cloud via synchronized credentials, or
compromise cloud identity to move laterally to on-premises through SAML token forging
(Golden SAML), cloud-to-on-prem VPN access, or Azure AD joined device abuse.
Understanding these interconnections is essential for modern tradecraft.
11
Anti-Forensics & Cleanup
Minimizing Forensic Evidence
Professional tradecraft means leaving the smallest possible forensic footprint. While complete
invisibility is impossible, careful operators can significantly reduce the artifacts available to
incident responders and forensic analysts.
Artifact Minimization Techniques
Timestomping: Modify file creation/modification timestamps to match surrounding legitimate files
▸
Prefetch Awareness: Understand that Windows Prefetch records every binary executed — consider
using LOLBins that are already in Prefetch from legitimate use
▸
Event Log Awareness: Know which logs your actions generate. Avoid clearing entire logs (obvious
and itself logged). Instead, understand what gets logged and avoid the triggers
▸
USN Journal: NTFS tracks file changes in the USN Journal. File deletion alone is insufficient —
artifacts persist in the journal and MFT
▸
Memory-Only Operations: Whenever possible, execute code only in memory without writing to disk.
Use reflective loading, in-memory .NET assembly execution, and fileless techniques
▸
Secure Deletion: When disk artifacts are unavoidable, overwrite files before deletion rather than
simple delete (which leaves data recoverable)
▸
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
18/22
Engagement Cleanup Protocol
At the conclusion of every engagement, the red team must systematically remove all artifacts,
tools, and persistence mechanisms. This is not optional — leaving backdoors in a production
environment is a serious professional and ethical violation.
⚠ Critical Reminder
Maintain a meticulous operational log throughout the engagement documenting every action, tool, credential, and
artifact. This log is essential for cleanup, deconfliction, reporting, and proving that all implants have been removed. A
missing artifact in production is a real security risk, not just a professional embarrassment.
12
Tradecraft Maturity & Continuous Development
The Tradecraft Development Cycle
Tradecraft is never finished — it is a continuous cycle of learning, testing, operating, and
refining. As defenders improve their detection capabilities, operators must evolve their
techniques. The best red teams invest systematically in tradecraft research and development.
Remove all persistence mechanisms (registry keys, scheduled tasks, WMI subscriptions, services)
▸
Delete all uploaded tools, scripts, and payloads from target systems
▸
Remove any created user accounts or modified group memberships
▸
Tear down all external infrastructure (C2 servers, redirectors, phishing infrastructure)
▸
Destroy any exfiltrated data per the Rules of Engagement data handling agreement
▸
Provide the blue team with a complete list of IOCs for verification and hunting
▸
Verify cleanup by running the same discovery commands used during the engagement
▸
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
19/22
Study
Monitor threat intelligence reports, APT analysis, EDR
vendor blogs, and academic research. Understand what
defenders are detecting and how detection logic works.
Develop
Build custom tools, write new loaders, create novel
evasion techniques. Test against current EDR in an
isolated lab. Document what works and what gets caught.
Operate
Apply refined tradecraft in real engagements. Note what
succeeds, what triggers alerts, and what could be
improved. Collect operational intelligence on defensive
postures.
Share
Internal knowledge transfer: document techniques in
playbooks, conduct training sessions, and build team
capability. Elevate the entire team's tradecraft, not just
individuals.
Tradecraft Resources
Continuous learning is essential. Key resources include: offensive security conferences (DEF
CON, Black Hat, Wild West Hackin' Fest, SO-CON), threat intelligence reports from Mandiant,
CrowdStrike, and Microsoft, open-source research projects (Outflank, MDSec, SpecterOps
publications), internal lab testing against current EDR products, and cross-team knowledge
sharing sessions with your organization's detection engineering team.
FINAL TRADECRAFT PRINCIPLES
Know thy enemy: Understand defender tools, processes, and detection logic as deeply as your own
offensive capabilities
▸
Minimal footprint: Do only what is necessary. Every action generates telemetry — make each one
count
▸
Patience over speed: The best operators are patient. Wait for the right moment rather than rushing
and getting caught
▸
Always have a backup: Multiple C2 channels, multiple persistence mechanisms, multiple credential
sources. Redundancy is survival
▸
Document everything: If it wasn't documented, it didn't happen. Detailed logs enable cleanup,
reporting, and learning
▸
Stay humble: Every operator gets caught eventually. Learn from detection, improve, and come back
sharper
▸
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
20/22
"The mark of a true tradecraft master is not that they are never detected — it is that when they are
detected, they have already achieved their objectives and have three backup plans ready."
— Red Team Leaders Philosophy
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
21/22
RED TEAM LEADERS
C Y B E R S E C U R I T Y  T R A I N I N G
Mastering the art of offensive operations through disciplined tradecraft.
Silent. Persistent. Relentless.
w w w. r e d t e a m l e a d e r s . c o m    |    ©  2 0 2 5  R e d  Te a m  L e a d e r s .  A l l  r i g h t s  r e s e r v e d .
20/03/2026, 11:19
Red Team Tradecraft - Complete Guide
file:///Users/joas/Downloads/Red_Team_Tradecraft_Guide.html
22/22
