---
id: ckb-74cb809d7934
title: Incident Response Cheat Sheet
category: incident-response-and-forensics
format: cheatsheet
language: en
tags: [cheatsheet, incident-response, linux, networking, powershell, windows]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.76
---

Page | 1

Follow us:
www.hackingarticles.in

Page | 2

Follow us:
www.hackingarticles.in
Table of Contents

Abstract
5 L

6
What is Incident Response?
7
User Accounts
7
/etc/passwd
7
passwd -S
8
grep
8
find /-nouser
8
/etc/shadow
9
/etc/group
10
/etc/sudoers
11
Log Entries
12
Lastlog
12
Auth.log
12
History
13
System Resources
14
Uptime
14
Free
14
/proc/memory
14
/proc/mounts
15
Processes
15
top
15
ps aux
16
PID
16
Services
17
Service
17
/etc/cronjob
18
/etc/resolv.conf
18
/etc/hosts
19
iptables
19
Files
20
Page | 3
Follow us:
www.hackingarticles.in
Large Files
20
mtime
20
Network Settings
21
ifconfig
21
Open files
21
netstat
22
arp
22
path
22 W
23
Users
24
Local users
24
Net user
25
net localgroup
25
Local user
26
Processes
26
Task Manager
26
tasklist
27
Powershell
28
Services
30
GUI
30
net Start
30
sc query
31
Task Scheduler
32
tasklist
32
GUI
32
Schtasks
33
Startup
33
GUI
33
Powershell
34
Registry
35
GUI
35
PowerShell
36
Active TCP and UDP Port
36
netstat
36

Page | 4

Follow us:
www.hackingarticles.in
Powershell
37
File Sharing
38
net view
38
SMBShare
38
Files
39
Forfiles
39
Firewall Settings
41
Sessions with other system
42
Open Sessions
43
Log Enteries
43
Event Viewer
43
Cmd
44
PowerShell
44
Conclusion
45
References
45
About Us
46

Page | 5

Follow us:
www.hackingarticles.in

Abstract

For some people who use their computer systems, their systems might seem normal to them,
but they might never realise that there could be something really fishy or even that fact that
their systems could have been compromised. Making use of Incident Response a large number
of attacks at the primary level could be detected. The investigation can be carried out to obtain
any digital evidence.

Detecting any intrusion in your system is a very important step towards Incident response.
Incident response is quite vast, but it is always better to start small. While performing incident
response, you should always focus on suspected systems and the areas where it seems there
could be a breach. Making use of Incident Response, you could detect a large number of attacks
at the primary level.
The purpose of incident response is nothing but Live Forensics. The investigation can be
carried out to obtain any digital evidence. This article mainly focuses on how incident response
can be performed in a Linux system. So, to get you started with this cheat sheet, switch on your
Linux machine and open the terminal to accomplish these commands.

Page | 6

Follow us:
www.hackingarticles.in

 L

Page | 7

Follow us:
www.hackingarticles.in
What is Incident Response?

Incident Response can be defined as a course of action that is taken whenever a computer or network
security incident occurs. As an Incident Responder, you should always be aware of what should be and
should not be present in your systems.
The security incidents that could be overcome by:

By examining the running processes

By having insights into the contents of physical memory.

By gathering details on the hostname, IP address, operating systems etc

Gathering information on system services.

By identifying all the known and unknown users logged onto the system.

By inspecting network connections, open ports and any network activity.

By determining the various files present
User Accounts

As an Incident Responder, it is very important to investigate the user account’s activity. It helps you
understand the logged-in users, the existing users, usual or unusual logins, failed login attempts,
permissions, access by sudo etc.
The various commands to check the user account activity:

/etc/passwd

To identify whether there is an account entry in your system that may seem suspicious. This command
usually fetches all the information about the user account. To do so, type

cat  /etc/passwd

Page | 8

Follow us:
www.hackingarticles.in

passwd -S

The ‘Setuid’ option in Linux is unique file permission. So, on a Linux system when a user wants to make
the change of password, they can run the ‘passwd’ command. As the root account is marked as setuid,
you can get temporary permission.

grep

Grep is used for searching plain- text for lines that match a regular expression. :0: is used to display
‘UID 0’ files in /etc/passwd file.

find /-nouser

To Identify and display whether an attacker created any temporary user to perform an attack, type

passwd -S raj
grep :0: /etc/passwd
find / -nouser -print

Page | 9

Follow us:
www.hackingarticles.in

/etc/shadow

The /etc/shadow contains the encrypted password, details about the passwords and is only
accessible by the root users.

cat /etc/shadow

Page | 10

Follow us:
www.hackingarticles.in
/etc/group

The group file displays the information of the groups used by the user. To view the details, type

cat /etc/group

Page | 11

Follow us:
www.hackingarticles.in
/etc/sudoers

If you want to view information about user and group privileges to be displayed, the/ etc/sudoers
file can be viewed

cat /etc/sudoers

Page | 12

Follow us:
www.hackingarticles.in
Log Entries

Lastlog

To view the reports of the most recent login of a particular user or all the users in the Linux system,
you can type,

Auth.log

To identify any curious SSH & telnet logins or authentication in the system, you can go to /var/log/
directory and then type

tail auth.log
lastlog

Page | 13

Follow us:
www.hackingarticles.in

History

To view the history of commands that the user has typed, you can type history with less or can even
mention up to the number of commands you typed last. To view history, you can type

history| less

Page | 14

Follow us:
www.hackingarticles.in
System Resources
System resources can tell you a lot about system logging information, uptime of the system, the
memory space and utilisation of the system etc.

Uptime

To know whether your Linux system has been running overtime or to see how long the server has
been running for, the current time in the system, how many users have currently logged on, and the load
averages of the system, then you can type:

Free

To view the memory utilisation by the system in Linux, the used physical and swap memory in the
system, as well as the buffers used by the kernel, you can type,

/proc/memory

As an incident responder to check the detail information of the ram, memory space available,
buffers and swap on the system, you can type

uptime
free
cat /proc/meminfo

Page | 15

Follow us:
www.hackingarticles.in

/proc/mounts

As an incident responder, it’s your responsibility to check if there is an unknown mount on your
system, to check the mount present on your system, you can type

Processes

As an incident responder, you should be always curious when you are looking through the output
generated by your system. Your curiosity should compel you to view the programs that are currently
running in the system, if they necessary to run and if they should be running, and usage of the CPU
usage by these processes etc.

top

To get a dynamic and a real-time visual of all the processes running in the Linux system, a summary
of the information of the system and the list of processes and their ID numbers or threads managed
by Linux Kernel, you can make use of

cat /proc/mounts
top

Page | 16

Follow us:
www.hackingarticles.in

ps aux

To see the process status of your Linux and the currently running processes system and the PID. To
identify abnormal processes that could indicate any malicious activity in the Linux system, you can
use

PID

To display more details on a particular process, you can use,

ps aux
lsof –p [pid]

Page | 17

Follow us:
www.hackingarticles.in
Services
The services in the Linux system can be classified into system and network services. System services
include the status of services, cron, etc and network services include file transfer, domain name
resolution, firewalls, etc. As an incident responder, you identify if there is an anomaly in the services.
Service

To find any abnormally running services, you can use

service –-status-all

Page | 18

Follow us:
www.hackingarticles.in
/etc/cronjob

The incident responder should look for any suspicious scheduled tasks and jobs. To find the
scheduled tasks, you can use,

/etc/resolv.conf

To resolve DNS configuration issues and to avail a list of keywords with values that provide the
various types of resolver information, you can use

cat /etc/crontab
more /etc/resolv.conf

Page | 19

Follow us:
www.hackingarticles.in

/etc/hosts

To check file that translates hostnames or domain names to IP addresses, which is useful for testing
changes to the website or the SSL setup, you can use

iptables

To check and manage the IPv4 packet filtering and NAT in Linux systems, you can use iptables and
can make use of a variety of commands like:

more /etc/hosts
iptables -L -n

Page | 20

Follow us:
www.hackingarticles.in
Files
As an incident responder, you should be aware of any abnormal-looking files in your system.

Large Files

To identify any overly large files in your system and their permissions with their destination, you can
use

mtime

As an incident responder, if you want to see an anomalous file that has been present in the system
for 2 days, you can use the command,

find /home/ -type f -size +512k -exec ls -lh {} \;
find / -mtime -2 -ls

Page | 21

Follow us:
www.hackingarticles.in
Network Settings
As an incident responder, you should have a keen eye on the Network activity and setting. It is
extremely vital to identify the overall picture of a system network and its health.

ifconfig

To obtain the network activity information, you can use various commands.

To see all the network interfaces, you can use

Open files

To list all the processes that are listening to ports with their PID, you can use

ifconfig
ifconfig -a
lsof -i

Page | 22

Follow us:
www.hackingarticles.in
netstat

To display all the listening ports in the network use

arp

To display the system ARP cache, you can type

path

The $PATH displays a list of directories that tells the shell which directories to search for executable
files, to check for directories that are in your path you can use.

netstat -nap
arp -a
echo $PATH

Page | 23

Follow us:
www.hackingarticles.in

 W

Page | 24

Follow us:
www.hackingarticles.in
Users
In Incident response it is very necessary to investigate the user activity. It is used to find if there is
any suspicious user account is present or any restricted permissions have been assigned to a user. By
checking the user account one can be able to get answers to questions like which user is currently
logged in and what kind of a user account one has.
The ways one can view the user accounts are:

Local users

To view the local user accounts in GUI, press ‘Windows+R’, then type ‘lusrmgr.msc’.

Now click on ‘okay’, and here you will be able to see the user accounts and their descriptions.

Page | 25

Follow us:
www.hackingarticles.in
net user

You can now open the command prompt and run it as an administrator. Then type the command ‘net
user’ and press enter. You can now see the user accounts for the system and the type of account it is.

net localgroup

‘Net localgroup groupname’ command is used to manage local user groups on a system. By using this
command, an administrator can add local or domain users to a group, delete users from a group,
create new groups and delete existing groups.
Open Command prompt and run as an administrator then type ‘net local group administrators’ and
press enter.

net user
net local group administrators

Page | 26

Follow us:
www.hackingarticles.in
Local user

To view the local user accounts in PowerShell, open PowerShell as an administrator, type ‘Get-
LocalUser’ and press enter. You will be able to see the local user accounts, with their names, if they
are enabled and their description.

Processes

To get the list of all the processes running on the system, you can use ‘tasklist’ command for this
purpose. By making use of this command, you can get a list of the processes the memory space
used, running time, image file name, services running in the process etc
To view the processes, you can use the following methods;

Task Manager

To view the running processes in a GUI, press ‘Windows+R’, then type ‘taskmgr.exe’.

Now click on ‘OK’ and you will be able to see all the running processes in your system and will be able
to check if there is any unnecessary process running.
Get-LocalUser

Page | 27

Follow us:
www.hackingarticles.in

tasklist

To view the processes in the command prompt, Open the command prompt as an administrator and
type ‘tasklist’ and press enter. Here you will be able to see all the running processes with their Process
ID (PID) and their session name and the amount of memory used.

tasklist

Page | 28

Follow us:
www.hackingarticles.in
Powershell

To view the process list in PowerShell, run PowerShell as an administrator and type ‘Get-Process’ and
press enter. It gets a list of all active processes running on the local computer.

Windows system has an extremely powerful tool with the Windows Management Instrumentation
Command (WMIC). Wmic is very useful when it comes to incident response. This tool is enough to
notice some abnormal signs in the system. This command can be used in the Command-prompt as
well as PowerShell when run as an administrator. The syntax is ‘wmic process list full’.

To get more details about the parent process IDs, Name of the process and the process ID, open
PowerShell as an administrator and type ‘wmic process get name,parentprocessid,processid’. This
would be the next step after you determine which process is performing a strange network activity.
You will see the following details.

get-process
wmic process get name,parentprocessid,processid
wmic process list full

Page | 29

Follow us:
www.hackingarticles.in

To get the path of the Wmic process, open PowerShell and type ‘wmic process where 'ProcessID=PID’
get Commandline’ and press enter.

wmic process where 'ProcessID=PID’ get Commandline

Page | 30

Follow us:
www.hackingarticles.in
Services
To identify if there is any abnormal service running in your system or some service is not functioning
properly, you can view your services.

GUI

To view all the services in GUI, press ‘Windows+R’ and type ‘services.msc’.

Now click on ‘Ok’ to see the list of processes.

net start

To start and view the list of services that are currently running in your system, open the command
prompt as an administrator, type ‘net start’ and press enter.

net start

Page | 31

Follow us:
www.hackingarticles.in

sc query

To view whether a service is running and to get its more details like its service name, display name,
etc.

sc query | more

Page | 32

Follow us:
www.hackingarticles.in
Task Scheduler

tasklist

If you want a list of running processes with their associated services in the command prompt, run
command prompt as an administrator, then type ‘tasklist /svc’ and press enter.

GUI

Task Scheduler is a component in the Windows which provides the ability to schedule the launch
of programs or any scripts at a pre-defined time or after specified time intervals. You can view
these scheduled tasks which are of high privileges and look suspicious.To view the task
Scheduler in GUI, then go the path and press enter.
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Administrative Tools

tasklist /svc

Page | 33

Follow us:
www.hackingarticles.in
Schtasks

To view the schedule tasks in the command prompt, run command prompt as an administrator,
type ‘schtasks’ and press enter.

Startup

The startup folder in Windows, automatically runs applications when you log on. So, an incident
handler, you should observe the applications that auto start.

GUI

To view the applications in Startup menu in GUI, open the task manager and click on the ‘Startup’
menu. By doing this, you can see which applications are enabled and disabled on startup. On
opening the following path, it will give you the same option
dir /s /b "C:\Users\raj\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
schtasks

Page | 34

Follow us:
www.hackingarticles.in

Powershell

To view, the startup applications in the PowerShell run the PowerShell as an administrator, type
‘wmic startup get caption,command’ and press enter.

To get a detailed list of the AutoStart applications in PowerShell , you can run it as an administrator
and type ‘Get-CimInstance Win32_StartupCommand | Select-Object Name, command, Location,
User | Format-List’ and press enter.
wmic startup get caption,command

Page | 35

Follow us:
www.hackingarticles.in

Registry
Sometimes if there is a presence of unsophisticated malware it can be found by taking a look at
the Windows Registry's run key.

GUI

To view the GUI of the registry key, you can open REGEDIT reach the run key manually.

Get-CimInstance Win32_StartupCommand | Select-Object
Name, command, Location, User | Format-List’

Page | 36

Follow us:
www.hackingarticles.in

PowerShell

You can also view the registry of the Local Machine of the Run key in the PowerShell, by running
it as an administrator and then type
‘reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run’ and press enter.

You can also view the registry of the Current User of the Run key in the PowerShell, by running it
as an administrator and then type
‘reg query HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run’ and
press enter.

Active TCP and UDP Port
As an Incident Responder you should carefully pay attention to the active TCP and UDP ports of
your system.

netstat

reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run

Page | 37

Follow us:
www.hackingarticles.in
The network statistics of a system can be using a tool. The criteria tested are incoming and
outgoing connections, routing tables, port listening, and usage statistics. Open the command
prompt, type ‘netstat –ano’ and press enter.

Powershell

Well, this can also be checked in the PowerShell with a differentcommand. Run PowerShell and
type ‘Get-NetTCPConnection -LocalAddress 192.168.0.110 | Sort-Object LocalPort’ and press
enter. You will get detailed information about the IP and the local ports.

netstat –ano
Get-NetTCPConnection -LocalAddress 192.168.0.110 | Sort-Object
LocalPort

Page | 38

Follow us:
www.hackingarticles.in
File Sharing
As an incident responder you should make sure that every file share is accountable and reasonable
and there in no unnecessary file sharing.

net view

In order to check up on the file sharing options in command prompt, type ‘net view \\<localhost>’
and press enter.

SMBShare

To see the file sharing in PowerShell, you can type ‘Get -SMBShare’ and press enter.

net view \\127.0.0.1
Get-SMBShare

Page | 39

Follow us:
www.hackingarticles.in
Files
To view the files which could be malicious or end with a particular extension, you can use ‘forfiles’
command. Forfiles is a command line utility software. It was shipped with Microsoft Windows
Vista. During that time, management of multiples files through the command line was difficult as
most of the commands at that time we made to work on single files

Forfiles

To view the .exe files with their path to locate them in the command prompt, type ‘forfiles /D -10
/S /M *.exe /C "cmd /c echo @path"’ and press enter.

To View files without its path and more details of the particular file extension and its modification
date, type ‘forfiles /D -10 /S /M *.exe /C "cmd /c echo @ext @fname @fdate"’and press enter.

forfiles /D -10 /S /M *.exe /C "cmd /c echo @path"
forfiles /D -10 /S /M *.exe /C "cmd /c echo @ext @fname @fdate"

Page | 40

Follow us:
www.hackingarticles.in
To check for files modified in the last 10 days type ‘forfiles /p c: /S /D -10’.

To check for file size below 6MB, you can use the file explorer’s search box and enter
"size:>6M”

forfiles /p c: /S /D -10

Page | 41

Follow us:
www.hackingarticles.in
Firewall Settings

The incident responder should pay attention to the firewall configurations and settings and should
maintain it regularly.
To view the firewall configurations in the command prompt, type ‘netsh firewall show config’ and
press enter to view the inbound and outbound traffic.

netsh firewall show config

Page | 42

Follow us:
www.hackingarticles.in
To view the firewall settings of the current profile in the command prompt, type ‘netsh advfirewall
show currentprofile’ and press enter.

Sessions with other system

To check the session details that are created with other systems, you can type ‘net use’ in
command prompt and press enter.

netsh advfirewall show currentprofile
net use

Page | 43

Follow us:
www.hackingarticles.in
Open Sessions
You can type ‘net session’ in the command prompt and press enter to see any open sessions of
your system. It gives you the details about the duration of the session.

Log Enteries
To view the log entries in GUI you can open the event viewer and see the logs.  Press ‘Windows+
R’ and type ‘eventvwr.msc’ and press ‘OK’.

Event Viewer

net session

Page | 44

Follow us:
www.hackingarticles.in
Cmd

To export certain logs of a particular event in command prompt type ‘wevtutil qe security’ and
press enter.

PowerShell

To get the event log list in the PowerShell, type ‘Get-EventLog -list’ and type the particular event
in the supply value and you will get event details of that particular event.

wevtutil qe security
Get-Eventlog -List

Page | 45

Follow us:
www.hackingarticles.in

Conclusion
Hence, one can make use of these commands as an incident responder and keep their systems
away from threat.
References

https://www.hackingarticles.in/incident-response-linux-cheatsheet/

https://www.hackingarticles.in/incident-response-windows-cheatsheet/

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
