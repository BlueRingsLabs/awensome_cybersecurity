---
id: ckb-d42b2e560590
title: Remote Desktop Penetration Testing Port 3389
category: offensive-security
format: guide
language: en
tags: [credential-access, exploit-development, metasploit, persistence, windows]
summary: This technical guide walks through enumerating, attacking, exploiting, and hardening the Remote Desktop Protocol (RDP) on Windows environments.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.5-flash-lite
  confidence: 0.95
classified_by: google:gemini-3.5-flash-lite@2026-10-08T00:57:49Z
---

 Page 2 of 27

Contents
Introduction ........................................................................................... 3
Nmap Port Scan ...................................................................................... 4
Login Bruteforce ..................................................................................... 5
Mitigation Against Bruteforce................................................................ 6
Post Exploitation using Metasploit ........................................................ 8
Persistence ............................................................................................. 9
Credential Dumping ............................................................................. 10
Session Hijacking .................................................................................. 11
Mitigation against Session Hijacking ................................................... 15
DoS Attack (MS12-020 Free DoS) ......................................................... 17
Exploitation: BlueKeep ......................................................................... 19
Changing the RDP Port ......................................................................... 21
Man-in-the-Middle Attack: SETH ......................................................... 22
Conclusion ............................................................................................ 27

 Page 3 of 27

Introduction
From Wikipedia Remote Desktop Protocol (RDP), also known as "Terminal Services Client," is a
proprietary protocol developed by Microsoft that allows a user to connect to another computer via a
network connection using a graphical interface.RDP servers are built into Windows operating systems;
by default, the server listens on TCP port 3389.

In a network environment, it is best practise to disable the services that are not being used, as they can
be the potential cause of a compromise. The Remote Desktop Service is no exception to this. If the service
is disabled on the system, it can be enabled using the following steps. Inside the control panel of the
system, there exists a system and security section. Inside this section, there is a system section. After
traversing inside this section, on the left-hand side menu, there exists a Remote Settings option, as
depicted in the image below. It can also be verified that the system that we are working on is Windows
10 Enterprise Edition.

By clicking on the Remote Setting option, we see that a small window opens. It consists of multiple tabs.
However, inside the Remote Tab, we see that there is a section labelled "Remote Desktop." This section
can be used to enable or disable the Remote Desktop Service. For the time being, we are enabling the
service as shown in the image below.

 Page 4 of 27

Nmap Port Scan
Since we have enabled the Remote Desktop service on our Windows machine, it is possible to verify the
service is running on the device by performing an Nmap Port Scan. By default, the port that the Remote
Desktop service runs on is port 3389. It can be seen that the Windows machine with the IP address
192.168.1.41 is running Remote Desktop Service. It is also able to extract the system name of the machine;
it is MSEDGEWIN10.

nmap -A -p3389 192.168.1.41

 Page 5 of 27

Login Bruteforce
In a process of performing a penetration test on the Remote Desktop service, after the Nmap scan, it is
time to do a Bruteforce Attack. There is a long list of tools that can be used to perform a Bruteforce attack,
but one of the most reliable tools that can get the job done is Hydra. Although referred to as a
"bruteforce," it is more akin to a dictionary attack. We need to make two dictionaries, one with a list of
probable usernames and another with a list of probable passwords. The dictionaries are named user.txt
and pass.txt. With all this preparation, all that is left is to provide the dictionaries and the IP address of
the target machine to the Hydra to perform a Bruteforce attack on the login of RDP. We see that a set of
credentials were recovered. It is possible to initiate an RDP session using this set of credentials.

hydra -L user.txt -P pass.txt 192.168.1.41 rdp

 Page 6 of 27

Mitigation Against Bruteforce
The Bruteforce attack that we just performed can be mitigated. It requires the creation of an account
policy that will prevent Hydra or any other tool from trying multiple credentials. It is essentially a lockout
policy. Toggling this policy requires opening the Local Security Policy window. This can be done by typing
in "secpol.msc". It will open a window similar to the one shown below. To get to the particular policy, we
need to account for policies under Security Settings. Inside the account policies, there is an account
lockout policy. It contains 3 policies, each working on an aspect of the account lockout. The first one
controls the duration of the lockout. This is the time that is required to be passed to log in again after the
lockout. Then we have the lockout threshold. This controls the number of invalid attempts. Please toggle
these as per your requirements. This should prevent the Bruteforce attack.

After trying the Bruteforce attack using Hydra, it can be observed that it is not possible to extract the
credentials as before. Although there is still some risk, that can be prevented by forcing the users to
change the passwords frequently and enforcing good password policies.

hydra -L user.txt -P pass.txt 192.168.1.41 rdp

 Page 7 of 27

As we enabled a lockout policy, we will not be able to log in to the machine even with the correct password
until the time that we toggled in the policy has passed. You will be greeted with a lockout message, as
shown in the image below.

 Page 8 of 27

Post Exploitation using Metasploit
Although it has been years since its introduction, the Metasploit Framework is still one of the most reliable
ways to perform post-exploitation. During penetration testing, if there is a machine that has RDP disabled,
it is possible to enable RDP on that device through a meterpreter. In the image below, we have the
meterpreter of the machine that has RDP disabled. We use the getgui command on meterpreter to create
a user by the name of ignite with a password of 123. After completion, we can log in on the machine as
an ignite user through RDP.

This was the meterpreter command getgui. It uses the post/windows/manage/enable_rdp module to add
a new user with RDP privileges. Let’s try to use the module directly. We background the meterpreter
sessions and then open the enable_rdp module. We provide the username and password for the user to
be created and the session identifier. It will create another user by the name of Pavan with a password as
123 on the machine which then can be used for accessing the machine through RDP.

run getgui -e -u ignite -p 123
use post/windows/mange/enable_rdp
set username pavan
set password 123
set session 1
exploit

 Page 9 of 27

Persistence
The session that can be accessed as the user that is created using the enable_rdp module will be a low
privilege session. This can be further elevated to gain administrative privileges with the combination of
using the sticky_keys exploit. After selecting the exploit, we need to provide a session identifier. In the
image, it can be observed that the exploit was created successfully. It replaces the Ease of Access Sticky
Keys operation with a Command Prompt so that when Sticky Keys are initiated on the machine, it opens
a Command Prompt with elevated access.

Since Sticky Keys can be initiated by pressing the Shift key 5 times, we connect to the target machine using
RDP and then proceed to do so. This will open an elevated command prompt window, as shown in the
image below.
use post/windows/manage/sticky_keys
set session 1
exploit

 Page 10 of 27

Credential Dumping
Mimikatz can be used to perform this kind of attack. As the attacker was able to gain access to the session
of the machine, they used Mimikatz and ran the mstsc function inside the ts module. Mstsc is a process
that runs when the Remote Desktop service is in use. It then intercepts the RDP protocol communication
to extract the stored credentials. It can be seen in the image below that Mimikatz can extract the
credentials for the user raj.

privilege::debug
ts::mstsc

 Page 11 of 27

Session Hijacking
Session Hijacking is a type of attack where an attacker can gain access to an active session that is not
directly accessible to the attacker. To demonstrate this kind of attacker, we need to create a scenario.
Here we have a Windows machine with the Remote Desktop service enabled and running with two active
users: raj and aarti. One of the most important factors in performing a Session Hijacking Attack is that the
other session that we are trying to hijack must be an active session. Here, the raj user and aarti user are
both active users with active sessions on the target machine.

We log in to the raj user using the credentials that we were able to extract using the Mimikatz.

 Page 12 of 27

Now we will need to run the Mimikatz again after logging in as raj user. We need to list all the active
sessions. We use the sessions command from the ts module. Here we can see that there is a Session 3 for
aarti user that is active.

privilege::debug
ts::sessions

 Page 13 of 27

We use the elevate command from the token module to impersonate a token for the NT
Authority\SYSTEM and provide the ability to connect to other sessions. Back to the session output, we
saw that the aarti user has session 3. We need to connect to that particular session using the remote
command of the ts module.

token::elevate
ts::remote /id:3

 Page 14 of 27

As we can see in the image, we were able to get the remote desktop session for the aarti user from the
raj user access. This is the process through which session hijacking is possible for the Remote Desktop
services.

 Page 15 of 27

Mitigation against Session Hijacking
To discuss mitigation, we first need to detect the possibility of an attack. Like all the services on Windows,
Remote Desktop also creates various logs that contain information about the users that are logged on or
the time when they logged on and off, along with the device name and, in some cases, the IP address of
the user connecting as well.

There are various types of logs regarding the remote desktop service. It includes the Authentication Logs,
Logon, Logoff, and Sessions Connection. While connecting to the client, the authentication can either be
successful or fail. In both these cases, we have different EventIDs to recognise. The authentication logs
are located inside the Security Section.

EventID 4624: Authentication process was successful
EventID 4625: Authentication process was failure

 Then we have the logon and logoff events. A logon will occur after successful authentication. Logoff will
track when the user is disconnected from the system. These particular logs will be located at the following:

Applications and Services Logs > Microsoft > Windows > TerminalServices-LocalSessionManager >
Operational.
Event ID 21: Remote Desktop Logon
Event ID 23: Remote Desktop Logoff

Finally, we have the Session Connection Logs. This category has the most events because there are various
reasons for disconnection and it should be clear to the user based on the particular EventID. These logs
are located at the following:
Applications and Services Logs > Microsoft > Windows > TerminalServices-LocalSessionManager >
Operational.
EventID 24: Remote Desktop Session is disconnected
EventID 25: Remote Desktop Session is reconnection

We can see that in the given image, the aarti user was reconnected. This is a log entry from the time we
performed the Session Hijacking demonstration. That means if an attacker attempts that kind of activity,
you might be looking for these kinds of logs.

 Page 16 of 27

For mitigation, we can set a particular time limit for disconnected sessions, idle Remote Desktop services
that might be clogging up the memory usage, and others. These policies can be found at:

Administrative Templates > Windows Components > Remote Desktop Services > Remote Desktop
Session Host > Session Time Limits.

 Page 17 of 27

When implemented, these policies will restrict the one necessity required by session hijacking, i.e., Active
User Session. Hence, mitigation of the possibility of session hijacking altogether.
DoS Attack (MS12-020 Free DoS)
A DoS attack, or denial-of-service in respect of the Remote Desktop services, is very similar to the typical
DoS attack. One of the things to notice before getting on with the attack is that DoS attacks through
remote desktops are generally not possible. In this demonstration, we will be using a Windows 7 machine.
Before getting to the exploit, Metasploit has an auxiliary that can be used to scan the machine for this
particular vulnerability. As it can be observed from the image below, the machine that we were targeting
is vulnerable to a DoS attack.

use auxiliary/scanner/rdp/ms12_020_check
set rhosts 192.168.1.21
exploit

 Page 18 of 27

Now that we have the confirmation for the vulnerability, we can use it to attack our target machine. This
attack is named as max channel attack. This attack works in the following method. Firstly, it detects the
target machine using the IP Address. Then it tries to connect to the machine through the RDP service.
When the target machine responds that it is ready to connect, the exploit sends large size packets to the
machine. The size of the packets is incremental until it becomes unresponsive. In our demonstration, we
can see that it starts with a 210 bytes packet.

It will continue to send packets until the target machine is unable to handle those packets. It can be
observed from the image below that the target machine crashed, resulting in a BSOD, or Blue Screen of
Death.
use auxiliary/dos/windows/rdp/ms12_020_maxchannelids
set rhosts 192.168.1.21
exploit

 Page 19 of 27

Exploitation: BlueKeep
BlueKeep was a security vulnerability that was discovered in the Remote Desktop Protocol
implementation that could allow the attacker to perform remote code execution. It was reported in mid-
2019. Windows Server 2008 and Windows 7 were the main targets of these vulnerabilities. To understand
the attack, we need to understand that RDP uses virtual channels, which are configured before
authentication. When a server associates the virtual channel "MS_T120" with a static channel other than
31, heap corruption occurs, allowing arbitrary code execution on the system.But since this attack is based
on heap corruption, there is a chance that if the configuration of the exploit is incorrect, it could lead to
memory crashes. BlueKeep's auxiliary scanner and exploit are contained in Metasploit. Let’s focus on the
scanner. It requires the IP address of the target machine. We are running this against a Windows 7
machine with Remote Desktop enabled. We see that it returns that the target is vulnerable.

use auxiliary/scanner/rdp/cve_2019_0708_bluekeep
set rhosts 192.168.1.16
exploit

 Page 20 of 27

Since we now know that the target is vulnerable, we can move on to exploiting the target.  After selecting
the exploit, we provide the remote IP address of the machine with the particular target. It can vary based
on the Operating System; for Windows 7 use the target as 5. We can see that it connects to the target and
first checks if it is vulnerable. Then it proceeds to inflict the heap corruption that we discussed earlier and
results in a meterpreter shell on the target machine.

use exploit/windows/rdp/cve_2019_0708_bluekeep_rce
set rhosts 192.168.1.16
set target 5
exploit
sysinfo

 Page 21 of 27

Changing the RDP Port
There are a lot of mitigations that can help a wide range of environments. It can include installing the
latest updates and security patches from Microsoft or, as the NSA suggests, disabling the Remote Desktop
Service until it is used and disabling it after use. The BlueKeep attacks can be mitigated to a large extent
by upgrading the operating system from Windows 7. There is a long list of other mitigation steps that can
be implemented, such as implementing an intrusion detection mechanism and other defence
mechanisms. One of the steps that can be taken with immediate effect is changing the port number on
which the Remote Desktop operates. This, although it seems like a big defence mechanism, might not
even be noticed if done correctly. The attacker might not even look for this angle. Anyone who thinks RDP
thinks 3389, but when changed, it is possible that the attacker won’t even be able to detect the presence
of RDP. To do this, we need to make changes to the registry. Open the registry editor and proceed to the
following path:

Here we have the port number as shown in the image. Change it to another value and save your changes.
Now the RDP will be running on the specified port.

Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal
Server\WinStations\RDP-Tcp

 Page 22 of 27

In our demonstration, we changed the port to 3314 from 3389. We can use the rdesktop command from
Linux to connect to the Windows machine as shown in the image given below.

Man-in-the-Middle Attack: SETH
As we are familiar with the typical Man-in-the-Middle attacks, the attacker most likely impersonates the
correct authentication mode and the user who is unaware of the switch unknowingly provides the correct
credentials. Some other methods and tools can be used to perform this kind of attack, but the SETH toolkit
is the one that seems elegant. We start by cloning it directly from its GitHub repository and then installing
some pre-requirements.

rdesktop 192.168.1.41:3314
git clone https://github.com/SySS-Research/Seth.git
cd Seth
pip install -r requirements.txt
apt install dsniff

 Page 23 of 27

After the installation, to mount the attack, we require the local IP address, the target IP address, and the
network interface that will be used. In this case, it is eth0. Here we see that the attack has been mounted
and is ready for the victim.

./seth.sh eth0 192.168.1.5 192.168.1.3 192.168.1.41

 Page 24 of 27

From the victim’s perspective, they open up the Remote Desktop Connection dialogue and try to connect
to the machine and user of their choice. It asks for the credentials to connect as any original security
authentication prompt.

 Page 25 of 27

Next, we have the Certificate Manager. Here we can see that there seems to be a conflict regarding the
server name and trusted certifying authority. This is usually quite similar to the window that asks you to
save the certificate. The victim won’t think twice before clicking "Yes" on the window.

 Page 26 of 27

As soon as the connection is established, we can go back to Kali Linux, where we mounted the attack. We
can see that it was able to capture the NTLM hash as well as the password that was entered by the victim.
This completes the Man-In-the-Middle Attack.

 Page 27 of 27

Conclusion
The Remote Desktop Service is one of the most used services. It was quite important when it was
introduced by Microsoft, but the pandemic and work from home culture have made it a necessity for
every enterprise. This article serves as a detailed guide to how to perform a penetration test on an RDP
setup. We hope it can give penetration testers the edge that they need over threat actors targeting their
RDP environment.

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
