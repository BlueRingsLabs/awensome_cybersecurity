---
id: ckb-632658dc497f
title: Comprehensive Guide on Honeypots
category: security-operations
format: guide
language: en
tags: [android, detection-engineering, linux, malware, soc, windows]
summary: This document provides a comprehensive overview of honeypots, detailing their types, purposes, and installation procedures across Windows, Android, and Linux environments.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.5-flash-lite
  confidence: 0.95
classified_by: google:gemini-3.5-flash-lite@2026-10-08T00:39:28Z
---

 Page 2 of 27

Contents
Introduction .......................................................................................3
What are honeypots? .........................................................................3
Working of honeypots ........................................................................3
Types of Honeypots ...........................................................................4
Windows System ............................................................................................. 7
Android Honeypot ........................................................................... 14
Linux Honeypot ................................................................................ 24

 Page 3 of 27

Introduction
Honeypots are generally hardware or software that are deployed by the security departments of any
organization to examine the threats that are possessed by the attackers. Honeypots usually act as baits
for an organization to gather information on the attacker and alongside protect the real target system.

What are honeypots?
Honeypots are a type of Internet security resource that is used to entice cybercriminals to deceive them
when they try to intrude into the network for any illegal use. These honeypots are generally set up to
understand the activities of the attacker in the network so that the organisation can come up with
stronger prevention methods against these intrusions. The honeypots do not carry any valuable data as
they are faked proxies that help in logging the network traffic.
Working of honeypots
As an IT administrator, you would want to set up a honeypot system that might look like a genuine system
to the outside world. The kind of data that honeypots generally capture:

Keystrokes entered and typed by the attacker.

The IP address of the attacker

The usernames and different privileges used by the attackers

The type of data that the attacker had accessed, deleted or that was altered.

 Page 4 of 27

Types of Honeypots

Low-Interaction Honeypots:
They match a very limited number of services and applications that are present on the network or on
the system. This type of honeypot can be used to keep track of UDP, TCP, and ICMP ports and services.
Here we make use of fake databases, data, files, etc. as bait to trap attackers to understand the attacks
that would happen in real-time. Examples of a few low-interaction tools are Honeytrap, Specter,
KFsensor, etc.

Medium-Interaction Honeypots:
They are based on imitating real-time operating systems and have all the applications and services of a
target network. They tend to capture more information as their purpose is to stall the attacker so that the
organisation gets more time to respond appropriately to the threat. Examples of a few medium-
interaction tools are Cowrie, HoneyPy, etc.

High-Interaction Honeypots:
They are genuine vulnerable software that is run on a real operating system with various applications that
a production system would generally have. The information gathered using these honeypots is more
resourceful, but they are difficult to maintain. An example of a high-interaction tool is the honeynet.

Pure Honeypots:

 Page 5 of 27

These honeypots usually imitate the actual production environment of an organization, which makes an
attacker assume it to be a genuine one and invest more time exploiting it. Once the attacker tries to find
the vulnerabilities, the organisation will be alerted, and hence any kind of attack can be prevented earlier.

Production Honeypots:
These honeypots are usually installed in the organization’s actual production network. They also help in
finding any internal vulnerabilities or attacks as they are present in the network internally.

Research Honeypots:
They are high-interaction honeypots, but they are set up with a focus of research in the areas of various
governmental or military organisations to gain more knowledge about the behaviour of the attackers.

 Page 6 of 27

Malware Honeypots:
They are the kind of honeypots that are used to trap malware in a network. Their purpose is to attract the
attacker or any malicious software and allow them to perform certain attacks that can be used to
understand the pattern of the attack.

Email Honeypots:
These honeypots are hoax email addresses that are used to attract attackers across the internet. The
emails that are received by any malicious actor can be monitored and examined and can be used to help
the fall for phishing email scams.

Database Honeypots:
These honeypots pose as actual databases that are vulnerable in name and usually attract attacks like SQL
injections. They are meant to lure the attackers into thinking that they might contain sensitive information
like credit card details, which will let the organisation understand the pattern of the attacks they have
performed.

Spider Honeypots:
These honeypots are installed with the purpose of trapping the various web crawlers and spiders that
tend to steal important information from the web applications.

Spam Honeypots:
These honeypots consist of hoax email servers to attract spammers to exploit vulnerable email elements
and give details about the activities performed by them.

 Page 7 of 27

Honeynets:
these are nothing but a network of honeypots which are installed in a virtual and isolated environment
along with various servers to record the activities of the attackers and understand the potential threats.

Honeypots can be deployed in various environments. Today we will see the installation and working of
honeypots in the Windows, Android, and Linux environments.

Windows System

Today we will be looking at the famous honeypot software called HoneyBOT. which can be downloaded
here. Start Kali Linux as the attacker machine and your Windows system as the host machine.

Let us first do an nmap scan on the host machine when the honeypot is not installed.

Now on your Windows system, install the HoneyBOT software and configure it. Click on "yes" to proceed.
nmap -sV 192.168.1.17

 Page 8 of 27

Check all the parameters that you want in your honeypot and click on Apply to proceed.

To get email reports on your honeypot, add the recipient's email address and click on "Apply."

 Page 9 of 27

If you want to save the honeypot logs in CSV format, you can use this setting.

On the attacker's machine, performs a nmap scan, and there you will see so many fake services that are
open due to the presence of the honeypot in the system.

 Page 10 of 27

 Page 11 of 27

Let us try connecting via FTP from the attacker machine to the host machine.

As you see, a log has been generated of the attacker’s IP and the port that he was connected to.

 Page 12 of 27

Here you can see a detailed report on the connection that was created by the attacker.

Similarly, an SSH connection was initiated on port 22 from another operating system.

 Page 13 of 27

Now you can see that a log for the same has been generated for the connection created on port
22.

 Page 14 of 27

Android Honeypot
The honeypots can also be installed on Android phones using the Google Play store. Here we have
downloaded the Hostage honeypot.

 Page 15 of 27

 Page 16 of 27

On switching on the application, it looks safe.

 Page 17 of 27

 Page 18 of 27

Now let us check the IP address of your android device and let’s proceed.

 Page 19 of 27

 Page 20 of 27

Let’s turn on the attacker's system and let’s conduct an nmap scan on the IP address of the android device.

An alert will be generated on the android device when the nmap scan is connected.

 Page 21 of 27

 Page 22 of 27

A log will be created and we will see the IP of the attacker system and the ports that were attacked.

 Page 23 of 27

 Page 24 of 27

Linux Honeypot
We can install a honeypot on a Linux machine as well. Here we have demonstrated using Pentox, which
can be easily installed on Ubuntu.

Once it is installed, let us start using the pentbox. Select the network tools and honeypot from the menu
to install the honeypot. Go along with the manual configuration to install it according to your preferences
for a honeypot.

wget http://downloads.sourceforge.net/project/pentbox18realised/pentbox-1.8.tar.gz
tar -zxvf pentbox-1.8.tar.gz
./pentbox.rb

 Page 25 of 27

 Page 26 of 27

Now you can open the fake port according to your preference and insert a fake message. You can also
provide the option to save the log and save the name of the log. You can see that the honeypot is activated
on the required port, and similarly, you can manually activate honeypots for other ports.

Turn on the attacker's machine, and scan the host machine using nmap. The results of the open ports
and services are displayed below.

Here, the attacker machine is trying to connect with the host machine using telnet.

 Page 27 of 27

For every attempt of intrusion that is made, it gets alerted and a log is created where the attacker's IP and
port are recorded.

telnet 192.168.1.108
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
