---
id: ckb-e946867f79a6
title: Credential Dumping SAM
category: offensive-security
format: article
language: en
tags: [credential-access, lateral-movement, metasploit, powershell, windows]
summary: This document explores credential dumping from the Windows Security Account Manager database using various post-exploitation tools and techniques.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.5-flash-lite
  confidence: 1.0
classified_by: google:gemini-3.5-flash-lite@2026-10-08T00:39:32Z
---

Credential Dumping: SAM

                                                                                                 1 | P a g e

Credential Dumping: SAM

                                                                                                 2 | P a g e

Contents
Introduction ............................................................................................................................................ 3
Introduction to SAM ................................................................................................................................ 3
How are Passwords stored in Windows? ................................................................................................ 3
LM authentication ............................................................................................................................... 3
NTLM authentication .......................................................................................................................... 3
Windows 7 .............................................................................................................................................. 4
PwDump7 ............................................................................................................................................ 4
SamDump2 .......................................................................................................................................... 5
Metasploit Framework ........................................................................................................................ 5
Invoke-Powerdump.ps1 .................................................................................................................. 5
Get-PassHashes.ps1 ........................................................................................................................ 5
PowerShell .......................................................................................................................................... 6
Windows 10 ............................................................................................................................................ 6
Mimikatz ............................................................................................................................................. 6
Impacket .............................................................................................................................................. 9
Metasploit Framework ............................................................................................................................ 9
HashDump ........................................................................................................................................... 9
Credential_collector .......................................................................................................................... 10
Load kiwi ........................................................................................................................................... 10
Koadic .................................................................................................................................................... 11
Powershell Empire: mimikatz/sam .................................................................................................... 12
LaZAgne ............................................................................................................................................. 13
CrackMapExec ................................................................................................................................... 14
Decrypting Hash: John The Ripper ........................................................................................................ 14

Credential Dumping: SAM

                                                                                                 3 | P a g e

Introduction
Credential Dumping via SAM is a crucial technique in post-exploitation, allowing attackers to extract
password hashes from the Security Account Manager (SAM) database on Windows systems. By
accessing this sensitive data, adversaries can escalate privileges, move laterally within the network,
or even gain full control over target machines. Understanding this attack vector is essential for both
red teamers and defenders to identify and mitigate credential theft risks effectively.
In this article, we will learn about SAM. We will learn about the passwords and how they are stored
in the SAM. We will also focus on the NTLM Authentication. At last, we will be using a bunch of
different tools to extract those credentials from SAM.
Introduction to SAM
SAM is short for the Security Account Manager which manages all the user accounts and their
passwords. It acts as a database. All the passwords are hashed and then stored SAM. It is the
responsibility of LSA (Local Security Authority) to verify user login by matching the passwords with
the database maintained in SAM. SAM starts running in the background as soon as the Windows
boots up. SAM is found in C:\Windows\System32\config and passwords that are hashed and saved
in SAM can found in the registry, just open the Registry Editor and navigate yourself to
HKEY_LOCAL_MACHINE\SAM.
How are Passwords stored in Windows?
To understand how passwords are saved in Windows, you first need to know about LM, NTLM v1 &
v2, and Kerberos.
LM authentication
IBM developed LAN Manager (LM) authentication for Microsoft's Windows Operating Systems, but
the security it provides is considered hackable today. It converts your password into a hash by
breaking it into two chunks of seven characters each. And then further encrypting each chunk. It is
not case sensitive either, which is a huge drawback. This method coverts the whole password string
into uppercase, so when the attacker is applying any attack like brute force or dictionary; they can
altogether avoid the possibility of lowercase. The key it is using to encrypt is 56-bit DES which now
can be easily cracked.
NTLM authentication
NTLM authentication secures systems because LM proved to be insecure at the time. Its foundation
is a challenge-response mechanism that uses three components: nonce (challenge), response, and
authentication.
When Windows stores a password, NTLM encrypts the password and stores its hash, discarding the
actual password. Additionally, it sends the username to the server, which then generates a 16-byte
random numeric string called a nonce and sends it back to the client. Now, the client encrypts the
nonce using the hash of the password and returns the result to the server. This step is known as the
response. These three components (nonce, username, and response) are then sent to the Domain
Controller. The Domain Controller retrieves the password hash from the Security Account Manager
(SAM) database. Furthermore, it checks the nonce and response, and if they match, the
authentication is successful.
Credential Dumping: SAM

                                                                                                 4 | P a g e

Moreover, the working of NTLM v1 and NTLM v2 is similar, although there are some key differences.
For instance, NTLM v1 uses MD4 for hashing, while NTLM v2 uses MD5. In addition, NTLM v1 has a
C/R Length of 56 bits + 56 bits + 16 bits, while NTLM v2 uses 128 bits. When it comes to the C/R
Algorithm, NTLM v1 uses DES (ECB mode), whereas NTLM v2 relies on HMAC_MD5. Finally, NTLM
v1 has a C/R Value Length of 64 bits + 64 bits + 64 bits, while NTLM v2 uses 128 bits.
Now as we have understood these hashing systems, let's focus on how to dump them. The methods
we will focus on are best suited for both internal and external pen-testing. Let’s begin!
NOTE:
Microsoft changed the algorithm on Windows 10 v1607 which replaced the RC4 cipher with AES. This
change made all the extraction tools that directly access SAM to dump hashes obsolete. Some of the
tools have been updated and handle the new encryption method properly. But others were not able
to keep up. This doesn't mean that they cannot be used anymore. This just means that if we face the
latest Windows 10, we rather use update tools. Hence we divided this article into 2 parts. Windows 7
and Windows 10.
Windows 7
PwDump7
This tool is developed by Tarasco and you can download it from here. This tool extracts the SAM file
from the system and dumps its credentials. To execute this tool just run the following command in
command prompt after downloading:
PwDump7.exe

And as a result, it will dump all the hashes stored in SAM file as shown in the image above.
Now, we will save the registry values of the SAM file and system file in a file in the system by using
the following commands:
reg save hklm\sam c:\sam
reg save hklm\system c:\system
Credential Dumping: SAM

                                                                                                 5 | P a g e

We saved the values with the above command to retrieve the data from the SAM file.
SamDump2
Once you have retrieved the data from SAM, you can use SamDump2 tool to dump its hashes with
the following command:
samdump2 system sam

Metasploit Framework
Invoke-Powerdump.ps1
Download Invoke-Powerdump Script
The method of Metasploit involves PowerShell. After getting the meterpreter session, access
windows PowerShell by using the command load PowerShell. And then use the following set of
commands to run the Invoke-PowerDump.ps1 script.
powershell_import /root/powershell/Invoke-PowerDump.ps1
powershell_execute Invoke-PowerDump

Once the above commands execute the script, you will have the dumped passwords just as in the
image above.
Get-PassHashes.ps1
Download Get-PassHashes Script
Credential Dumping: SAM

                                                                                                 6 | P a g e

Again, via meterpreter, access the windows PowerShell using the command load PowerShell. And
just like in the previous method, use the following commands to execute the scripts to retrieve the
passwords.
powershell_import /root/powershell/Get-PassHashes.ps1
powershell_execute Get-PassHashes

And VOILA! All the passwords have been retrieved.
PowerShell
Download Invoke-Powerdump Script
This method is an excellent one for local testing, AKA internal testing. To use this method, simply
type the following in the Powershell:
Import-Module <'path of the powerdump script'>-
Invoke-PowerDump

And it will dump all the credentials for you.
NOTE: These were the tools that will only work on Windows 7. Now let's take a look at the tools that
work on Windows 10. The tools that work on Windows 10 can also work on Windows 7 but not vice
versa. The tools mentioned above work only on Windows 7. Even if they run on Windows 10 and give
the hash, that hash will not be accurate and will not work and/or crack.
Windows 10
Mimikatz
There is a good enough method to dump the hashes of SAM file using mimikatz. The method is
pretty easy and best suited for internal penetration testing. In one of our previous article, we have
covered mimikatz,  read that article click here. So in this method, we will use token::elevate
Credential Dumping: SAM

                                                                                                 7 | P a g e

command. This command is responsible for allowing mimikatz to access the SAM file in order to
dump hashes. Now, to use this method use the following set of commands:
privilege::debug
token::elevate
lsadump::sam
Credential Dumping: SAM

                                                                                                 8 | P a g e

Credential Dumping: SAM

                                                                                                 9 | P a g e

Impacket
Impacket tool can also extract all the hashes for you from the SAM file with the following command:
./secretsdump.py -sam /root/Desktop/sam -system /root/Desktop/system LOCAL

Metasploit Framework
HashDump
When you have a meterpreter session of a target, just run hashdump command and it will dump all
the hashes from SAM file of the target system. The same is shown in the image below:

Another way to dump hashes through hashdump module is through a post exploit that Metasploit
offers. To use the said exploit, use the following set of commands:
use post/windows/gather/hashdump
set session 1
exploit

Credential Dumping: SAM

                                                                                                 10 | P a g e

Credential_collector
Another way to dump credentials by using Metasploit is via another in-built post exploit. To use this
exploit, simply background your session and run the following command:
use post/windows/gather/credential/credential_collector
set session 1
exploit

Load kiwi
The next method that Metasploit offers are by firing up the mimikatz module. To load mimikatz, use
the load kiwi command and then use the following command to dump the whole SAM file using
mimikatz.
lsa_dump_sam
Credential Dumping: SAM

                                                                                                 11 | P a g e

Hence, you have your passwords as you can see in the image above.
Koadic
Once you have the session by Koadic C2, use the hashdump_sam module to get passwords as shown
below:
use hashdump_sam
execute
Credential Dumping: SAM

                                                                                                 12 | P a g e

The SAM file dumps all the hashes, as shown in the above image.
Powershell Empire: mimikatz/sam
Once you have the session through the empire, interact with the session and use the mimikatz/sam
module to dump the credentials with help of following commands:
usemodule credentials/mimikatz/sam
execute
Credential Dumping: SAM

                                                                                                 13 | P a g e

This exploit will run mimikatz and will get you all the passwords you desire by dumping SAM file.
LaZAgne
LaZage is an amazing tool for dumping all kinds of passwords. We have dedicatedly covered LaZagne
in our previous article. To visit the said article, click here. Now, to dump SAM hashes with LaZagne,
just use the following command:
lazagne.exe all
Credential Dumping: SAM

                                                                                                 14 | P a g e

CrackMapExec
You can install CrackMapExec easily with a simple 'apt install,' and it runs swiftly. Using
CrackMapExec we can dump the hashes in the SAM very quicly and easily. It requires a bunch of
things.
Requirements:
Username: Administrator
Password: Ignite@987
IP Address: 192.168.1.105
Syntax: crackmapexec smb [IP Address] -u ‘[Username]’ -p ‘[Password]’ --sam
crackmapexec smb 192.168.1.105 -u 'Administrator' -p 'Ignite@987' –sam

Read More: Lateral Moment on Active Directory: CrackMapExec
Decrypting Hash: John The Ripper
John The Ripper is an amazing hash cracking tool. We have dedicated two articles on this tool. To
learn more about John The Ripper, click here – part 1, part 2. Once you have dumped all the hashes
from SAM file by using any of method given above, then you just need John The Ripper tool to crack
the hashes by using the following command:
john –format=NT hash –show
Credential Dumping: SAM

                                                                                                 15 | P a g e

And as you can see, it will reveal the password by cracking the given hash.
The article focuses on dumping credentials from the Windows SAM file. Additionally, it demonstrates
various methods for successfully dumping credentials using multiple platforms. To secure yourself,
first understand how an attacker can exploit a vulnerability and to what extent. Therefore, knowing
these methods and their potential impact is important.
FOLLOW US ON
FOR MORE DETAILS
CONTACT US
T W I T T E R
G I T H U B
L I N K E D I N
D I S C O R D
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
