---
id: ckb-d8c7cb142e7e
title: Gettng Started in ICS OT Cyber Security
category: network-and-wireless-security
format: guide
language: en
tags: [ics-ot, networking, nmap, osint, python, windows]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.6
---

© 2024 UƟlSec, LLC.
1

Geƫng Started in
ICS/OT Cyber Security
Lab Manual

© 2024 UƟlSec, LLC.
2

Contents
Part 1: Course IntroducƟon ........................................................................................................................... 4
Exercise 1.1: Seƫng Up VMware WorkstaƟon for Personal Use .............................................................. 4
Exercise 1.2 Installing Python on Windows .............................................................................................. 5
Exercise 1.3 Installing PIP .......................................................................................................................... 5
Part 2: ICS/OT Cyber Security Overview ....................................................................................................... 7
Exercise 2.1: Top CriƟcal Controls for ICS/OT Cyber Security .................................................................... 7
Part 3: Main Types of Control Systems & Protocols ...................................................................................... 9
Exercise 3.1: Installing a Modbus Server & Client ..................................................................................... 9
Exercise 3.2: Installing Wireshark............................................................................................................ 11
Exercise 3.3: Capturing Network Traﬃc with Wireshark ......................................................................... 12
Exercise 3.4: Using Wireshark StaƟsƟcs .................................................................................................. 15
Exercise 3.5: InspecƟng TCP/IP Traﬃc in Wireshark ............................................................................... 16
Exercise 3.6: InspecƟng ICS/OT Protocols in Wireshark .......................................................................... 17
Part 4: Secure Network Architecture .......................................................................................................... 19
Exercise 4.1: The Expanded Purdue Model ............................................................................................. 19
Exercise 4.2: Reviewing IT/OT DMZ Access Control Lists (ACLs) ............................................................. 21
Part 5: Asset Registers and Control Systems Inventory ............................................................................... 22
Exercise 5.1: Building an Asset Register with System Conﬁgs ................................................................. 22
Exercise 5.2: Building an Asset Register with Packet Captures ............................................................... 26
Part 6: Threat & Vulnerability Management ............................................................................................... 27
Exercise 6.1: Building an IT Host Scanning Target ................................................................................... 27
Exercise 6.2: AcƟve Scanning .................................................................................................................. 27
Exercise 6.3: Scanning for IT VulnerabiliƟes ............................................................................................ 30
Part 7: OSINT for Control Systems ............................................................................................................... 32
Exercise 7.1: Google Searches ................................................................................................................. 32
Exercise 7.2: Using WHOIS for OSINT ...................................................................................................... 35
Exercise 7.3: Using DNS for OSINT .......................................................................................................... 36
Exercise 7.4: Using LinkedIn for OSINT .................................................................................................... 36
Exercise 7.5: Using Shodan for OSINT ..................................................................................................... 37
Part 8: Incident DetecƟon & Response ....................................................................................................... 40
Exercise 8.1: Backdoors & Breaches (ICS OT Core Deck) ......................................................................... 40
Part 9: Industry Standards & RegulaƟons ................................................................................................... 41

© 2024 UƟlSec, LLC.
3

Part 10: IntroducƟon to ICS/OT PenetraƟon TesƟng ................................................................................... 42
Appendix B:  List of Resources (Books) ....................................................................................................... 53

© 2024 UƟlSec, LLC.
4

Part 1: Course IntroducƟon
Industrial Control Systems (ICS) and OperaƟonal Technology (OT) run the world around us. Power plants,
oﬀshore oil rigs, trains and other transportaƟon systems, manufacturing plants – these are just a few
examples of the criƟcal infrastructure that society depends on. Each ICS/OT environment is unique and
has specialized security requirements.
ProtecƟng criƟcal infrastructure becomes more important each day as the frequency of cyber aƩacks
and the number of aƩackers conƟnues to grow. NaƟon state adversaries are no longer the only ones
targeƟng these specialized environments. Today’s aƩackers include ransomware groups, hackƟvists,
cyber mercenaries, and more.
ICS/OT cyber security can seem complicated and even daunƟng at ﬁrst, but it does not have to be. This
course will help parƟcipants understand the fundamentals of how these environments operate and how
to secure such specialized networks.

Exercise 1.1: Seƫng Up VMware WorkstaƟon for Personal Use
Throughout this course, many of the exercises use virtual machines.  While there are several virtual
machine applicaƟons available for use, VMware WorkstaƟon is my preference and is free as of early May
2024.  And I’ll always point students towards free resources!
NOTE:  You can use other virtualizaƟon soŌware such as Oracle VirtualBox to complete the labs in this
course, but any special instrucƟons in this lab manual are speciﬁcally for VMware WorkstaƟon.
1. First, you will need to register for a Broadcom free account if you do not already have one.  You
can register at hƩps://proﬁle.broadcom.com/web/registraƟon.

2. Next, access the Broadcom portal download page at
hƩps://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware+WorkstaƟon
+Pro.

3. In the Broadcom portal, navigate to the download for the latest version of "VMware WorkstaƟon
Pro for Personal Use (For Windows)."

4. Once downloaded, launch the VMware WorkstaƟon Pro installer executable.

5. On the "Welcome to the VMware WorkstaƟon Pro Setup Wizard" screen, click 'Next.'

6. On the 'End-User License Agreement" screen, review the general terms presented, check the box
for "I accept the terms in the License Agreement" if you agree and click 'Next.'

7. If you receive the "CompaƟble Setup" message, you will typically need to install Windows
Hypervisor Plaƞorm (WHP) which Windows can do for you automaƟcally.  Check the box for
"Install Windows Hypervisor Plaƞorm (WHP) automaƟcally" and click 'Next.'

8. On the "Custom Setup" screen, click "Next."

© 2024 UƟlSec, LLC.
5

9. On the "User Experience Seƫngs" screen, make your privacy and product
selecƟons.  AŌerwards, click 'Next.'

10. On the "Shortcuts" screen, click 'Next.'

11. On the "Ready to install VMware WorkstaƟon Pro" window, click 'Install.'

12. Once the installaƟon is complete, click the "Finish" buƩon on the "Completed the VMware
WorkstaƟon Pro Setup Wizard" window.

NOTE: You'll have the opƟon for conﬁguring the License later.
Reboot your system.

13. Reboot your system.

Exercise 1.2 Installing Python on Windows
In this exercise, you will install the current version of the Python language on your Windows system.
Python will be the main language used to write scripts in this course as it can run on both Windows and
Linux.
1. On your main Windows host, download the current version of Python at
hƩps://www.python.org/downloads/.  You should see a yellow buƩon near the top of the page
under the header “Download the latest version for Windows.”

2. Once downloaded, install Python.  For the purpose of this course, accept all defaults.

3. To verify that Python is installed correctly on your system, open a command prompt and type
the following:

python --v

4. The screen should display output something similar to the following:

C:\Users\micha>python --version
Python 3.12.2

Exercise 1.3 Installing PIP
While PIP comes installed with Python 3.4 or higher, it is important to ensure that it is installed on your
system. PIP allows addiƟonal modules of Python funcƟonality to be added easily to the system.  Many of
the scripts we will be creaƟng in this course will require such modules to be installed and PIP is the
easiest way to make that happen!

© 2024 UƟlSec, LLC.
6

1.  Run the following command to see if PIP is installed:

python -m ensurepip --default-pip

If you receive a message that starts with “Requirement already saƟsﬁed” then you do not need
to take any further acƟon.
2. If it appears that PIP is not installed on your system, download the current version of PIP using
the following link:  hƩps://bootstrap.pypa.io/pip/pip.pyz.

3. Once downloaded, launch the .pyz ﬁle which is a specially craŌed ZIP ﬁle for Python.  At  this
point, PIP should install on your system.

© 2024 UƟlSec, LLC.
7

Part 2: ICS/OT Cyber Security Overview
In Part 2, we dive into what exactly is cyber security for ICS/OT, including: - Diﬀerences Between IT and
ICS/OT - Common Ways AƩackers Enter ICS/OT Networks - A Simple OT Example - Types of Industrial
Control Environments - What is ICS/OT Cyber Security? - Annotated History of ICS/OT Cyber Security -
Hybrid Approach to ICS/OT Cyber Security - The Sliding Scale of Cyber Security
Exercise 2.1: Top CriƟcal Controls for ICS/OT Cyber Security
Text
Read the LinkedIn post on the top CriƟcal Controls for ICS/OT Cyber Security.  The post can be found at
hƩps://www.linkedin.com/posts/mikeholcomb_the-top-ten-icsot-cyber-security-controls-acƟvity-
7191814014316732416-HfZg.
Answer the following quesƟons based on the post.
1. Which of the listed CriƟcal Controls reduces the most risk?

2. Which of the listed CriƟcal Controls reduces risk the least?

3. Which of the listed CriƟcal Controls should be addressed ﬁrst?

4. Which of the listed CriƟcal Controls should be addressed last?

5. In which CriƟcal Control would the business determine its overall exposure in the event of a
signiﬁcant incident?  For example, if a company was calculaƟng how much money they would
lose per hour of downƟme, this type of acƟvity would fall under which control?

6. Which CriƟcal Control ensures that operators can restore operaƟons as quickly and as eﬃciently
as possible in the event of a signiﬁcant incident?

7. Which of the CriƟcal Controls listed involves deploying an IT/OT DMZ between the IT and OT
networks?

8. Which of the CriƟcal Controls listed involves establishing an asset register and ensuring that it is
populated and kept up to date over Ɵme?

9. Which of the CriƟcal Controls listed involves deploying network traﬃc sensors to provide the OT
security team with the ability to watch network acƟvity for anomalies which might indicate an
operaƟonal or security issue is occurring?

10. Which of the CriƟcal Controls is oŌen exploited when an aƩacker gains control over a vendor’s
assets from over the Internet?

© 2024 UƟlSec, LLC.
8

11. Which of the CriƟcal Controls should be implemented as early as possible in the design of an
ICS/OT environment?

12. Which of the CriƟcal Controls is less a technical control and more of a “people” one?

13. Which of the CriƟcal Controls includes performing a risk assessment of a known issue in the
ICS/OT network which could be exploited by an aƩacker?

© 2024 UƟlSec, LLC.
9

Part 3: Main Types of Control Systems & Protocols
In Part 3, we talk about diﬀerent types of control systems as well as diﬀerent control system protocols,
including but not limited to: - How a Power Plant is Built - Control System Engineering Terms - Control
Systems (e.g., PLCs, HMIs, SIS, DCS, data historians) - ICS Protocols (e.g., Modbus, S7, OPC, OPC UA) -
Capturing and Viewing ICS Protocols

Exercise 3.1: Installing a Modbus Server & Client
1. Download the Modbus Server (ModRSSim2) from hƩps://sourceforge.net/projects/modrssim2/.

2. The ﬁle downloaded is a stand-alone executable and does not need to be installed to run.  Run
the ModRSSim2.exe ﬁle.
You should see a screen like the following:

3. Now that the Modbus server is running, we need to install the client.

4. Download Modbus Poll from hƩps://www.modbustools.com/download.html.

NOTE: Modbus Poll is free to evaluate for 30 days.

© 2024 UƟlSec, LLC.
10

5. The Modbus Poll applicaƟon does need to be installed.  Launch the installer ﬁle you downloaded
– ModbusPollSetup64Bit.exe.

6. On the 'License Agreement" screen, review the general terms presented, check the box for "I
accept the terms of the License Agreement" if you agree and click 'Next.'

7. On the “Choose Install LocaƟon” screen, accept the default by clicking ‘Next.’

8. On the “Choose Components” screen, accept the defaults by clicking ‘Next.’

9. On the second “Choose Components” screen, accept the defaults by click ‘Install.’

10. Once the installaƟon is complete, run the Modbus Poll applicaƟon.

11. When receiving the “this is an unregistered copy” message/window, click on “Register later.”

12. To connect the Modbus Poll app to the Modbus server running on your Windows system, click
on the ‘ConnecƟon’ menu opƟon and then select ‘Connect.’

13. In the ‘ConnecƟon Setup’ screen, under ‘ConnecƟon, select ‘Modbus TCP/IP.’

14. Under ‘Remote Modbus Server,’ ensure the localhost IP address of 127.0.0.1 is speciﬁed and click
‘OK.’

NOTE: The default port for Modbus is TCP 502.

15. If connected correctly, the Modbus Poll client should be retrieving values (as seen below).  These
values should be conƟnually changing and reﬂect the values displayed in the ModRSSim2 server.

© 2024 UƟlSec, LLC.
11

16. The Modbus Poll client displays three columns.  What are they?

17. What is parƟcular about the second column?  Why is this?

18. Leave both ModRSSim2 and Modbus Poll running to complete the next exercise.
Exercise 3.2: Installing Wireshark

1. Download Wireshark from hƩps://www.wireshark.org/download.html.

2. Once downloaded, launch the Wireshark installaƟon ﬁle.

3. On the ‘Welcome to Wireshark x.x.x Setup’ screen, click ‘Next.’

4. On the ‘License Agreement’ screen, review the general terms presented and click Noted.'

5. On the ‘Your donaƟons keep these releases coming,’ screen, click ‘Next.’

6. On the ‘Choose Components’ screen, accept the defaults and choose ‘Next.’

© 2024 UƟlSec, LLC.
12

7. On the ‘AddiƟonal Tasks’ screen, accept the defaults and choose ‘Next.’

8. On the ‘Choose Install LocaƟon’ screen, accept the defaults and choose ‘Next.’

9. On the ‘Packet Capture’ screen, accept the defaults and choose ‘Next.’

10. On the ‘USB Capture screen, accept the defaults and choose ‘Install.’

11. Once the installaƟon completes, click ‘Next.’

12. On the ‘CompleƟng Wireshark x.x.x Setup’ screen, click ‘Finish.’

Exercise 3.3: Capturing Network Traﬃc with Wireshark

1. Launch Wireshark.

2. Once Wireshark launches, you’ll see the default ‘Capture’ screen which lists each of the network
interfaces in your system running Wireshark along with a line graph to note any acƟvity on each
interface.

© 2024 UƟlSec, LLC.
13

3. Select the network interface which has visibility into the Modbus server and Modbus Poll client
traﬃc.

Note: This could be ‘Adapter for loopback traﬃc capture’ or another interface such as your
default ‘Wi-Fi’ connecƟon.

4. As the packet capture conƟnues, if you selected the correct interface, you should not only see
network packets generated, but you should see Modbus/TCP packets as seen below.

5. If you see Modbus/TCP packets, you’ve selected the correct interface.  Let the network capture
run for at least one minute.  Stop the capture by clicking the red stop buƩon on the top menu.

If you do not see Modbus/TCP packets, it is more than likely you’ve selected an incorrect
interface.  Close Wireshark and repeat this exercise starƟng at Step #1.

6. Once the capture is stopped, display only the Modbus/TCP traﬃc by typing in modbus in the
ﬁlter bar near the top of the window and hit ‘Enter.’  The ﬁlter bar has what appears to be a blue
bookmark on the leŌ and buƩons with an X and right arrow buƩon on the right.

7. Select one of the packets by double clicking on it.  The packet should be opened in its own
window.
8. In the top half of the window, you should see lines represenƟng the diﬀerent OSI layers captured
– Frame, Ethernet II, Internet Protocol, Transmission Control Protocol, Modbus/TCP and
Modbus.

9. Expand the ‘Frame’ secƟon.

a. Which interface is listed?

b. What is the frame number?

c. What is the frame length?

10. Expand the ‘Ethernet II’ secƟon.

© 2024 UƟlSec, LLC.
14

a. What is the DesƟnaƟon address?

b. What is the Source address?

c. What type of addresses are the Source and DesƟnaƟon address?

d. What protocol is listed under Type?

11. Expand the ‘Internet Protocol’ secƟon.

a. What version of IP is captured?

b. What number is listed under Protocol?  What transmission protocol does this represent?

c. What is the DesƟnaƟon address?

d. What is the Source address?

e. What type of addresses are the Source and DesƟnaƟon address?

12. Expand the ‘Transmission Control Protocol’ secƟon.

a. What is the Source Port?

b. What is the DesƟnaƟon Port?

c. Which TCP ﬂags are set?

d. How large is the TCP payload?

e. What is the size of the TCP header and CRC (tail)?

NOTE: Subtract the total length of the packet from the TCP header length.

13. Expand the ‘Modbus/TCP’ secƟon.

a. Which TransacƟon IdenƟﬁer is listed?

b. What is the Protocol IdenƟﬁer for the packet?

c. What is the Unit IdenƟﬁer for the packet?

14. Expand the ‘Modbus’ secƟon.

© 2024 UƟlSec, LLC.
15

a. Which Modbus command is captured being issued by the Modbus client to the server?

b. How many registers are requested by the single command?

c. What is the value of one of the returned registers?

d. Is this a binary value?

Exercise 3.4: Using Wireshark StaƟsƟcs

1. Open capture1.pcapng from the course ﬁles in Wireshark.

2. Use the Protocol Hierarchy from under the StaƟsƟcs menu to answer the following quesƟons.

a. What percentage of captured packets are IPv4?

b. What percentage of captured packets are TCP?

c. What percentage of captured packets are UDP?

d. What percentage of captured packets are ICMP?

e. How many packets are DNS packets?

f.
How many packets are NTP packets?

g. How many packets are ICMPv6 packets?

h. How much traﬃc in total was captured?  In Bytes?  In Megabytes?

i.
How much HTTP traﬃc was captured? In Bytes?  In Megabytes?

3. Use the ConversaƟons opƟon from under the StaƟsƟcs menu to answer the following quesƟons.

a. How many TCP connecƟons are idenƟﬁed in the packet capture?

b. Which host is responsible for sending the most packets?

c. What is the total amount of traﬃc sent by this host?

d. What is the desƟnaƟon IP address for this traﬃc?

© 2024 UƟlSec, LLC.
16

e. What is the listed duraƟon for this traﬃc?

f.
What is an internal IP address captured in the ﬁle?

4. Use the Resolved Addresses opƟon from under the StaƟsƟcs menu to answer the following
quesƟons.

a. What does the IP address of 104.244.42.194 resolve to?

b. What does the IP address of 34.198.182.201 resolve to?

c. What does the MAC address of 01:00:1d:00:00:05 resolve to?

d. What IP address does www.kali.org resolve to?

Exercise 3.5: InspecƟng TCP/IP Traﬃc in Wireshark
1. SƟll using capture1.pcapng from the course ﬁles, use Wireshark to answer the following
quesƟons:

a. How many packets are in the capture ﬁle?

b. What is the source IP address of Packet #452?

c. What is the desƟnaƟon IP address of Packet #452?

d. Which IP address above is a private (internal use only) address?

e. Which IP address above is a public (Internet-based) address?

f.
Examining the packet further, what type of packet is this?  HINT: Think three-way
handshake.

g. What is the desƟnaƟon port for this packet?  What is this connecƟon more than likely
being used for?

h. AŌer the connecƟon is established, a ﬁle is accessed.  What is the name of this ﬁle?

i.
What type of acƟvity is occurring in Packet #858?

j.
What type of acƟvity is occurring in Packet #859?

k. What is the MAC address of the system at 192.168.32.1?

© 2024 UƟlSec, LLC.
17

2. Open capture2.pcapng from the course ﬁles in Wireshark.  Use Wireshark to answer the
following quesƟons.

a. What applicaƟon protocols make up 16.7% of the captured traﬃc?

b. What is the ﬁrst packet in the capture where this type of traﬃc starts?

c. Right click on the packet and choose ‘Follow’ -> ‘TCP Stream’.

d. What type of informaƟon is displayed?  What is “special” about it?

e. How is Wireshark able to read the traﬃc idenƟﬁed in this way?

f.
Find a second session made with the same protocol.  Examine it by following the TCP
stream.

g. What is the diﬀerence in this second session?

h. What credenƟals are used to log on to the FTP site?

Exercise 3.6: InspecƟng ICS/OT Protocols in Wireshark

1. Open ‘capture3.pcap’ from the course ﬁles in Wireshark.

Which ICS/OT protocol is captured in the ﬁle?

2. Based on the queries and responses captured, what is the IP address of the PLC?

3. What is the IP address of the Engineering WorkstaƟon communicaƟng with the PLC?

4. Which Modbus command is ﬁrst sent to the PLC?

5. What is the purpose of this command?

6. Which Modbus command is sent in packet #23 to the PLC?

7. What is the purpose of this command?

8. What is the value of the coil read in Packet #51?

9. How many coils are read in Packet #54?  What are their values?

10. How many registers are read in Packet #57?  What are their values?

© 2024 UƟlSec, LLC.
18

11. Which register is updated in Packet #476?  What is its value?

12. What is the value of Register 198?

13. What value is wriƩen in Packet #1692?  What is this in decimal?  Which register is updated with
his value?

14. What is the last value wriƩen to the PLC?

© 2024 UƟlSec, LLC.
19

Part 4: Secure Network Architecture
The most important control in reducing risk in ICS/OT networks is ensuring that that OT network (and the
IT network it is connected to) have traﬃc properly controlled.  For organizaƟons just starƟng their ICS/OT
cyber security journey, the expanded Purdue Model can be an excellent place to start having discussions
on how to protect the OT network.  This always starts with the implementaƟon of the IT/OT DMZ which
sits between the IT and OT networks.  And, where possible, should not allow the IT network to originate
connecƟons into the OT network.

Exercise 4.1: The Expanded Purdue Model
Examine the diagram of the expanded Purdue Model and answer the following quesƟons.

© 2024 UƟlSec, LLC.
20

1. Which level of the expanded Purdue Model is connected directly to the Internet?

2. Which level of the expanded Purdue Model did not exist in the original reference model?

3. What is this level most referred to as?

4. How should traﬃc ﬂow be conﬁgured for this level?

5. Which level does the OT AcƟve Director domain controller reside on?

6. Which level is referred to as the Process level?  Why?

7. At which level should the SIS be located?

8. Which network should the SIS be connected to?  IT?  OT?

9. Using the "one up, one down rule," which levels should Level 3 be able to communicate with?

10. At which two levels are Engineering WorkstaƟons typically used?

11. Where should the OT patching server be located for downloading patches from the IT network?

12. How should communicaƟon for the OT patching server be conﬁgured?

13. Where could data historians be located?

14. How should communicaƟon for the data historians be conﬁgured?

15. At which level of the expanded Purdue Model do actuators reside?

16. Which network should CCTV cameras be connected to? IT? OT?

17. Enforcement boundaries are implemented by using what type of appliances?

18. What is the best pracƟce to consider when implemenƟng these enforcement boundaries?

19. At which level should an HMI reside?

20. An HMI typically needs to be able to communicate with which other level?

© 2024 UƟlSec, LLC.
21

Exercise 4.2: Reviewing IT/OT DMZ Access Control Lists (ACLs)
OŌen, the IT/OT DMZ can have its associated ﬁrewall rules misconﬁgured, potenƟally allowing aƩackers
a route into the OT network from the back oﬃce.  As the OT cyber security administrator for your plant,
you’re conducƟng a review of the ﬁrewall Access Control Lists which are conﬁgured on the external
interface for the IT-to-DMZ ﬁrewall.
In your environment, it is not possible to prevent the IT network from originaƟng connecƟons into the
OT network currently.
The Cisco ﬁrewall ACL is as follows:
1
permit tcp any host 10.2.1.5 eq 21
2
permit tcp any host 10.2.1.10 eq 80
3
permit tcp any host 10.2.1.10 eq 443
4
permit tcp any host 10.2.1.20 eq 3389
5
permit tcp any host 10.2.4.18 eq 502
6
permit icmp host 10.1.1.8 host 10.2.1.45
7
permit udp any host 10.2.1.66 eq 161
8
permit tcp host 10.1.1.1 any
AŌer reviewing the ACL, answer the following quesƟons to idenƟfy potenƟal security concerns:
1. What are three potenƟal security issues with the host at 10.2.1.5 being exposed as such?

2. What are three potenƟal security issues with the host at 10.2.1.10 being exposed as such?

3. Which operaƟng system is the host at 10.2.1.20 running?

4. What type of asset could the asset at 10.2.1.20 be?

5. What type of asset is the host at 10.2.4.18 more than likely?

6. What is unique about this IP address?  What security consideraƟons could it imply?

7. Why would ICMP be allowed from a parƟcular internal IP address on the IT network?

8. What are three potenƟal security issues with the asset at 10.2.1.66 being exposed as such?

9. Why should be concerned with the ACL listed on Line 8?

10. While not shown by default, what would Line 9 read if it was the last line of the Cisco ACL
conﬁg?

© 2024 UƟlSec, LLC.
22

Part 5: Asset Registers and Control Systems Inventory
One security control which is criƟcal to ensuring the security of any ICS/OT network is the asset register.
And yet, the importance of the asset register can oŌen be overlooked by ICS/OT team members.

Exercise 5.1: Building an Asset Register with System Conﬁgs

1. Open the asset register ﬁle stored in the course Google Drive locaƟon.  If you do not have access
to MicrosoŌ Excel, you can open the .csv version in Notepad/WordPad.

2. Review the asset register.

3. What type of environment does this appear to be an asset register for?

4. Why is it important to keep an asset register secure?

5. What vendor is listed as the manufacturer of the OT asset used to remotely control a plant
process via a PLC?

6. Based on the listed MAC address, who is the associated vendor for this asset?

© 2024 UƟlSec, LLC.
23

As an ICS/OT security analyst for your plant, you review the ARP cache on an engineering workstaƟon in
the OT network (see output below).
Use the informaƟon provided to add four addiƟonal assets to the asset register.
C:\Users\admin>arp -a
Interface: 192.168.1.210 --- 0xa
  Internet Address      Physical Address      Type
  192.168.1.1           00-02-fc-b0-42-77     dynamic
  192.168.1.50          00-08-06-d9-32-df     dynamic
  192.168.1.78          ac-64-17-55-8d-3e     dynamic
  192.168.255.255       ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static

7. Which three hosts can be found as dynamic entries in the engineering workstaƟon’s ARP cache?

8. Hosts located at .1 and .254 are usually what type of assets?

9. Which vendor manufactured the asset at 192.168.1.1?

10. Which vendor manufactured the other two “dynamic” assets?

11. Which addiƟonal host is listed?

12. How can you ﬁnd the MAC address for this host?

13. Create a MAC address for this host and add it to your asset register.

Next, you review the conﬁguraƟon of one of your Cisco switches.

© 2024 UƟlSec, LLC.
24

! EWS Subnet Switch

! Define VLANs
vlan 10
 name HOSTS_VLAN

! Interface Configuration
interface Vlan10
 ip address 192.168.1.1 255.255.255.0
 no shutdown

! Configure Access Ports
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast

interface FastEthernet0/2
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast

interface FastEthernet0/3
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast

! Assign IP Addresses to Hosts
ip dhcp pool HOST1
 network 192.168.1.0 255.255.255.0

© 2024 UƟlSec, LLC.
25

 default-router 192.168.1.1
 host 192.168.1.230 255.255.255.0
 client-identifier 0100.1500.3c4d.5e6f

ip dhcp pool HOST2
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 host 192.168.1.231 255.255.255.0
 client-identifier 01d4.bed9.3d4e.5f6g

ip dhcp pool HOST3
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 host 192.168.1.232 255.255.255.0
 client-identifier 0100.4238.3e4f.5g6h

! Enable IP Routing
ip routing

! Configure Default Gateway
ip default-gateway 192.168.1.1

14. What are the IP addresses for the three new hosts discovered in the Cisco switch conﬁguraƟon?

15. What is “unique” about these three IP addresses?

16. Add these assets to the register.  Include all relevant informaƟon.

© 2024 UƟlSec, LLC.
26

Exercise 5.2: Building an Asset Register with Packet Captures
Using your previous Wireshark skills, examine capture4.pcap and answer the following quesƟons.
1. What two IP addresses are discovered in the packet capture ﬁle?

2. What are the MAC addresses for these IP addresses?

3. Which vendor is associated with these MAC addresses?

4. Which port is being communicated with on the asset with the lower IP address?

5. What type of asset is this more than likely?

6. What is unique about the subnet associated with these IP addresses?

7. Which ICS/OT protocol is captured in the ﬁle?  HINT: It isn’t COTP.

8. Add these to your asset register with all relevant informaƟon.
One of the network administrators pings you to tell you they have the packet capture you requested
from a “special” VLAN that was set up along with the OT network.
Examine capture5,pcap and answer the following quesƟons.
9. Which two ICS/OT protocols are captured in the ﬁle?

10. What type of systems do these ICS/OT protocols typically support?

11. Are these assets typically located on the ICS/OT network or the IT network?

12. What other non-ICS/OT protocols are included in the ﬁle?

13. What is an RFC 1918 address?

14. Why is it important to note network communicaƟon with a non-RFC 1918 address?

15. Which enƟty is this non-RFC 1918 address associated with?

16. Who would you contact at this enƟty to discuss a potenƟal cyber security aƩack?

17. By reviewing the who-Has packets, name three locaƟons at the enƟty.

18. For more informaƟon on digging deeper into the BACnet protocol, review the following guide at

hƩps://guides.smartbuildingsacademy.com/deﬁniƟve-guide-bacnet

© 2024 UƟlSec, LLC.
27

Part 6: Threat & Vulnerability Management

Exercise 6.1: Building an IT Host Scanning Target

1. Download Metasploitable2 from
hƩps://sourceforge.net/projects/metasploitable/ﬁles/Metasploitable2/.

2. Unzip the downloaded ﬁle.  Once unzipped, double click the Metasploitable.vmx ﬁle to have
VMware WorkstaƟon automaƟcally create a Metasploitable2 VM.

3. Run the Metasploitable2 VM by selecƟng “Power on this virtual machine.”

4. If you receive the "This virtual machine might have been moved or copied" message, select "I
Copied It."

5. Once Metasploitable2 is up and running, login with a username and password of msfadmin.

6. Run the ifconfig command to determine which IP address was assigned to the host via DHCP.
This assumes you have an available DHCP server on your network.

Exercise 6.2: AcƟve Scanning
AcƟve scanning is conducted when tools are used to send packets to IP addresses and ports to
determine the presence of live hosts, open ports, running services and the version of those running
services. While a port scanner such as Nmap would be used to do so, addiƟonal tools such as Nessus
scan be used to scan speciﬁcally for vulnerabiliƟes.
6.2.A  Nmap Port Scan – Default Ports
1. To run a default Nmap scan against your target host, use the following command from a
terminal window (where x.x.x.x is the target’s IP address).
nmap x.x.x.x
2. Review the output of the scan to answer the following quesƟons.
a. How many closed ports are reported?
b. How many open ports are listed?
c. How many ports were tested?
d. Were both TCP and UDP ports tested? Or only one? If so, which?
e. How many total TCP and UDP ports exist on each system?
f. What are some of the ports that an aƩacker might be interested in?

© 2024 UƟlSec, LLC.
28

g. Which is the ﬁrst port listed that could be easily tested with a web browser?
h. What is the ﬁrst port that we might use telnet to connect to?
i. What is the MAC address of the remote host?
j. What is the vendor associated with the MAC address?

6.2.B Nmap Port Scan – All Ports
1. Use the following command to run an nmap scan of all 65,535 TCP ports on the target system.
nmap x.x.x.x -p-
a. How many closed ports are reported?
b. How many open ports are listed?
c. How many ports were tested?
d. Were both TCP and UDP ports tested? Or only one? If so, which?
e. Would any of the newly discovered ports be of interest to an aƩacker? If so, which?

6.2.C Nmap Subnet Scan
1. To run a default Nmap scan against your local subnet, use the following command from a
terminal window (where x.x.x.x/x is the address of your local subnet in CIDR notaƟon).
nmap 192.168.1.0/24
2. Review the output of the scan to answer the following quesƟons.
a. How many hosts were discovered on your local subnet?
b. How many closed ports are reported on each host?
c. How many open ports are listed on each host?
d. How many ports were tested on each host?
e. Did you discover any new ports that an aƩacker might be interested in?
f. What are the vendors associated with the MAC addresses of any newly discovered
hosts?
3. Re-run the same scan with the switch to only display open ports. What command would you
use?

© 2024 UƟlSec, LLC.
29

4. Compare the results of the “open port” scan to the default subnet scan. What is the diﬀerence
between the two?
6.2.D Nmap Service Scan
1. To run a Nmap Service scan against your target host on all ports, use the following command.
nmap x.x.x.x -p- -sV

2. Review the output of the Nmap service scan to answer the following quesƟons.
a. How many FTP related services are on the target host? Which versions?
b. What version of OpenSSH is open?
c. What version of DNS server is running on the target?
d. What version of Apache is running on TCP 80?
e. What version of Apache is running on 8180?
f. What version of MySQL is running on the host? What port is it on?
g. What version of PostgreSQL is running on the host? What port is it on?
h. What version of VNC is available?
i. What version of SAMBA is on the host?
j. What is the Windows workgroup associated with the host?

6.2.E Nmap NSE “Script” Scan – Single Target Host
1. To run a Nmap Script scan against your target host on all ports, use the following command.
nmap x.x.x.x -p- -sC
2. Review the output to answer the following quesƟons.
a. What type of access is available to remote users to the FTP service?
b. What is the addiƟonal informaƟon displayed for SSH?
c. What commands are supported by the default SMTP service?
d. Does the SMTP service oﬀer encrypted email exchange?
e. What version of SSL does SMTP support?
f. What is the Ɵtle page of the site running on TCP 80?

© 2024 UƟlSec, LLC.
30

g. Based on the rpcinfo service output, what service is running on TCP 2049?
h. What is the MySQL status?
i. What is the MySQL salt?
j. What form of VNC authenƟcaƟon is in use?
k. What is the Ɵtle of the webpage running on 8180?
l. What is the NetBIOS host name of the target host?
m. What is the system Ɵme reported on the target host?
n. Does the target host support SMB2?
Exercise 6.3: Scanning for IT VulnerabiliƟes

1.  Download and install Tenable Nessus Professional from
hƩps://www.tenable.com/lp/campaigns/22/try-nessus-mulƟprdct/free-trial.
2. Once installed, login and create a new vulnerability scan by clicking on ‘New Scan’.
3. On the ‘Scan Templates’ screen, click on ‘Advanced Scan’.
4. On the ‘Seƫngs’ tab, enter a name for your scan in the ‘Name’ ﬁeld such as “Home Scan”.
5. In the ‘Targets’ text box, enter the subnet range for your speciﬁc home network. For example,
you might choose to use CIDR notaƟon such as 192.168.1.0/24.
6. Click on the ‘Discovery’ selecƟon and review the opƟons.
7. Click on the ‘Port Scanning’ selecƟon and review the opƟons.
8. Click on the ‘Plugins’ tab and review the opƟons.
9. Save your seƫngs and run a vulnerability scan on your home network by click ‘Launch’.
10. Review the results to answer all remaining quesƟons below.
11. Reviewing the default set of ‘Scan Templates’ provided, what is the name of the malware
that is
associated with MS17-010 vulnerability?
12. How would someone address the MS17-010 vulnerability on a vulnerable Windows host?
13. Name one other scan template you think would be of interest to a security administrator?
Why did you choose this one?
14. On the ‘Discovery’ selecƟon page, what does the ‘ARP’ opƟon do?

© 2024 UƟlSec, LLC.
31

15. If you wanted to ensure you scanned all available TCP ports rather than just the default set of
ports,
what would you enter in the ‘Port scan range’ ﬁeld?
16. On the ‘CredenƟals’ tab, what three opƟons exist for supplying credenƟals?
17. Of the three opƟons for supplying ‘CredenƟals’, which is the one that would most likely be
used by
Nessus to login to a Linux-based host?
18. How many plugin checks exist to check for vulnerabiliƟes in various DNS services?
19. How many plugin checks exist to check for vulnerabiliƟes in Industrial Control Systems?
20. How many total plugin checks exist to search for the presence of vulnerabiliƟes on Windows
hosts?
21. Once you’ve completed the vulnerability scan of your home network including your
Metasploitable2 host, provide a screenshot of the screen which shows all of your hosts and
overview of the number of vulnerabiliƟes discovered.
22. Except for the Metasploitable2 host, what is the most vulnerable host on your home
network?
23. What type of system is the most vulnerable host on your home network?
24. What is one step you can take to strengthen the security of the most vulnerable host?
25. For the Metasploitable2 host, how many vulnerabiliƟes were discovered by Nessus?
26. What port is SSLv3 running on? What service is this port normally used for?
27. What is the password to the VNC service?
28. A backdoor was detected that was associated with what service? What port is this service
running on?
29. When accessing the Bind Shell backdoor, what user name and password are required to
remotely gain ‘root’ access to the host?

© 2024 UƟlSec, LLC.
32

Part 7: OSINT for Control Systems

Exercise 7.1: Google Searches
While there are several ways to ﬁnd Internet exposed PLCs, our friends at the NSA gave us a few
methods for doing so in their ELITEWOLF project.  While the project provided several Snort intrusion
detecƟon signatures for ICS/OT defenders to idenƟfy potenƟally malicious acƟvity on their networks, the
signatures also provided us with some Google searches to ﬁnd PLCs.
1.  Access the ELITEWOLF project site at hƩps://github.com/nsacyber/ELITEWOLF.

2. Select the ‘ELITEWOLF_SNORT_AllenBradley_RockwellAutomaƟon.txt’ ﬁle.

3. Looking at the last part of each Snort rule, the URL porƟon speciﬁed in the content: secƟon can
be used in Google to ﬁnd Allen Bradley/Rockwell AutomaƟon PLCs exposed to the Internet.

4. Go to Google and run a search for the ﬁrst URL porƟon listed in the ELITEWOLF ﬁle as seen
below.

© 2024 UƟlSec, LLC.
33

5. While some results will refer to PLC documentaƟon and the ELITEWOLF Github page itself, most
results will refer to actual PLCs exposed to the Internet.   For example, my search results start
with the two exposed PLCs at 173.181.149.217 and 185.9.25.82 as seen below.

As expected, based on the ELITEWOLF ﬁle we pulled the search string from, these appear to

be AllenBradley/Rockwell AutomaƟon PLCs.

6. Click on one of the links for the exposed PLCs.  You should see a web page that displays various
staƟsƟcs related to the PLC’s TCP funcƟonality such as seen below.

7. While each of the URLs can provide interesƟng pieces of informaƟon, I’m always fascinated
when I can see the netstat output of a remote system.  Run a Google search using the parƟal
URL of ‘/rokform/advancedDiags?pageReq=tcpconn’.

© 2024 UƟlSec, LLC.
34

8. Access the URL.  You should see the exposed PLCs netstat informaƟon, showing all IP addresses
(external AND internal) that are communicaƟng with the PLC.

9. In the previous example, there are several items of note:


The internal IP address of the PLC is 192.168.1.100.

The public IP address is the same as the IP in the URL.

The PLC is communicaƟng with mulƟple internal AND external IP addresses over HTTP
(TCP port 80) and EthernetIP (TCP port 44818).

10. If you look up the GeoIP informaƟon for the public IP addresses found on the tcpconn page you
had visited., you can ﬁnd a lot of interesƟng items of note.

In the sample above, we can note that:


The PLC is being remotely accessed from Shenyang in China, Sao Paulo in Brazil, Brussels
in Germany and (of course) Simpsonville, South Carolina, United States.

Internal hosts communicaƟng with the PLC include
192.1168.1.100,192.168.1.122,192.168.1.125, 192.168.1.127,192.168.1.130 and
192.168.1.131.

© 2024 UƟlSec, LLC.
35

So it appears we are not the only external visitors to the PLC’s web interface.  Not only that, but
we have also enumerated more than a few internal hosts on the PLCs ICS/OT network.

Exercise 7.2: Using WHOIS for OSINT
1. Use the dnslyƟcs.com site to perform the following research and answer the associated
quesƟon.

2. In the search ﬁeld, supply the IP address of 98.99.252.118 and click the magnifying glass icon to
run your search.

3. On the next screen, select ‘IP Report 98.99.252.118.’

4. Based on the provided descripƟon, which company is the IP address associated with?

NOTE: I’m siƫng in one of their stores right now as I write this lab. 놴
놲
놵
놶
놷
놳

5. What complete IP range is associated with this IP address?

6. What is the Autonomous System (AS) Number associated with this IP address?

7. Does this IP address appear on any of the 28 DNS blacklists tracked by DNSlyƟcs?

8. When was the associated domain name for this IP address registered?

9. When was the associated registraƟon informaƟon last updated?

10. Which physical address is associated with the owner for this IP address?

11. What is unique about this physical address?

12. Which Starbucks employee is associated with the domain registraƟon?

13. Which contact informaƟon of theirs is listed?

NOTE: Keep this informaƟon handy as we’ll be using it in the next exercise.

14. Which email address would you send an email to about a suspected cyber-aƩack coming from
that IP address?

© 2024 UƟlSec, LLC.
36

Exercise 7.3: Using DNS for OSINT
1. Use the dnsdumpster.com site to perform the following research and answer the associated
quesƟon.

2. In the search ﬁeld, supply the domain name of panerabread.com and run a search.

3. Which DNS servers are associated with this domain?

4. What are the IP addresses of the mail servers for panerabread.com?

5. Based on the associated TXT records, what would be one item of interest to aƩackers related to
the domain?

6. How many host (‘A’) records are returned by DNSdumpster?

7. Based on the host record names, which of these hosts might be of interest to an aƩacker?

8. The last column represents the Autonomous System (AS) Number and associated name for each
IP range.  What are some of the diﬀerent enƟƟes listed?

9. What could the informaƟon in QuesƟon #8 above be used to deduce about each system?

10. Based on that informaƟon, which host might be of interest to an aƩacker wanƟng a foothold on
the company’s internal corporate network?

Exercise 7.4: Using LinkedIn for OSINT
1. Use LinkedIn to perform the following research and answer the associated quesƟon.

2. Using the employee’s name found in Exercise 7.2, run a LinkedIn search for this person.

NOTE: To help, use only their ﬁrst name, last name and company name for your search.

3. How long has this person been with the company?

4. What is this person’s current job Ɵtle?

5. When were they promoted into this posiƟon?

6. What was this person’s original job Ɵtle when they started with the company?

7. Which web conferencing and instant messaging plaƞorm does this company use?

© 2024 UƟlSec, LLC.
37

8. Which IPAM soluƟon did this company use 13 years ago (and maybe today)?

9. What was this person’s ﬁrst job according to LinkedIn?

10. Which company did this person work for?

11. When was this person’s last post on LinkedIn?

12. Would this person be considered an acƟve parƟcipant on LinkedIn?

13. What sensiƟve informaƟon could be exposed by someone’s LinkedIn ‘Projects’ secƟon?

14. What LinkedIn groups is this person a member of?

Exercise 7.5: Using Shodan for OSINT
NOTE: Depending on when you are performing this lab, the results might not matched based on the
answers as the systems in quesƟon might have changed.
1. Use Shodan (shodan.io) to perform the following research and answer the associated quesƟon.

NOTE: Shodan free accounts are limited to two pages of results and do not have access to some
features.

2. Once logged in, click ‘Explore’ in the upper leŌ corner of the main page.

3. Next, click ‘Industrial Control Systems.’  You’ll be presented with a list of commonly seen ICS/OT
protocols on the Internet.

4. Click ‘EXPLORE MODBUS.’

5. What search string does Shodan use to look for hosts running Modbus?

6. What is the default TCP port number associated with Modbus?

7. Why is this not necessarily accurate in ﬁnding hosts running Modbus exposed to the Internet?

8. Run a Shodan search on the IP address 109.95.176.245 which has the default Modbus port
exposed.

Rather than Modbus, what service is running on this host?  What is it used for?

9. Run a Shodan search for ‘port:502 modbus.’  You should now receive a number of more relevant
hits such as the one seen below.

© 2024 UƟlSec, LLC.
38

10. Click on the IP address for the host running Modbus you idenƟﬁed.

11. What other ports are running on the host?

For example, the host seen above not only has the Modbus service running, but also appears to
have a web server listening on TCP port 80.

12. Based on the informaƟon presented in the example above, what type of ICS/OT asset is this?

13. What is the assets model type?

14. Find a picture of this type of ICS/OT asset.

© 2024 UƟlSec, LLC.
39

15. What are some of the security risks associated with exposing an ICS/OT protocol like Modbus to
the Internet?

16. What are some of the security risks associated with exposing a web service on this device to the
Internet?

17. Another way to ﬁnd ICS/OT assets on the Internet is to run a search for common ICS/OT vendor
names.

Run a new Shodan search for “Schneider Electric”.

Most of the devices returned should be Schneider Electric PLCs that are exposed to the Internet.

18. How many assets which adverƟse “Schneider Electric” as part of their service banner do you see
exposed to the Internet?

19. One other way covered during the course was to run Shodan searches for the actual names for
ICS/OT assets.

Run a new Shodan search for “Programmable Logic Controller”.

20. Now how many hosts do you see through Shodan?

21. What other brands of PLCs do you see exposed to the Internet besides the earlier Schneider
Electric ones?

© 2024 UƟlSec, LLC.
40

Part 8: Incident DetecƟon & Response

Exercise 8.1: Backdoors & Breaches (ICS OT Core Deck)
1. Access the Backdoors & Breaches site to play online at hƩps://play.backdoorsandbreaches.com/.

2. Click on the link for “ICS OT Core Deck.”  This will load a new B&B game to play.

To learn how to play B&B, watch this YouTube video with one of its creators, Jason Blanchard,
explaining the game play - hƩps://www.youtube.com/watch?v=pMY2HXUrKsg.

3. You can either play the online version as explained in the YouTube video or simply take a look at
the select cards.

4. Having been developed primarily by Dragos, these cards reﬂect real world scenarios that you
would see when responding to diﬀerent ICS/OT cyber security incidents.

5. Be sure to cycle through as many of the card types to get a good feel for how various ICS/OT
incidents occur.
a. IniƟal Compromise
b. Pivot and Escalate
c. C2 and Exﬁl
d. Persistence
Don’t forget the various procedures which you could emulate in your environment and then
injects which can be good for a laugh here or there!

© 2024 UƟlSec, LLC.
41

Part 9: Industry Standards & RegulaƟons

There are no labs for this part currently.

© 2024 UƟlSec, LLC.
42

Part 10: IntroducƟon to ICS/OT PenetraƟon TesƟng

There are no labs for this part currently.

© 2024 UƟlSec, LLC.
43

Appendix A:  Answer Key
Part 1: Course IntroducƟon
There are no quesƟons and answers for this part.

Part 2: ICS/OT Cybersecurity Overview
Exercise 2.1: Top CriƟcal Controls for ICS/OT Cyber Security
1.  Secure Network Architecture
2.  IT/OT Partnership
3.  Secure Network Architecture
4.  IT/OT Partnership
5.  ConducƟng Risk Assessments
6.  Backup & Recovery
7.  Secure Network Architecture
8.  Asset Inventory (Hardware, SoŌware & Firmware)
9.  Network Security Monitoring
10.  Secure Remote Access
11.  Secure Network Architecture
12.  Employee EducaƟon & Awareness (as well as IT/OT Partnership)
13.  ConƟnuous Vulnerability Management

Part 3: Control Systems & Protocols
Exercise 3.1: Installing a Modbus Server & Client
16.  Row IdenƟﬁer, Name and Value
17.  The second column is blank.  The Modbus server does not provide this informaƟon.

Exercise 3.2:  Installing Wireshark
There are no quesƟons and answers for this exercise.

© 2024 UƟlSec, LLC.
44

Exercise 3.3:  Capturing Network Traﬃc with Wireshark
9a. Answers will vary.  The network interface card should be listed with the term 'interface.'
9b. Answers will vary.
9c. Answers will vary.
10a.  Answers will vary.  You're looking for a MAC address such as a1-b2-c3-d4-e4-f6.
10b.  Answers will vary.  You're looking for a MAC address such as a1-b2-c3-d4-e4-f6.
10c.  MAC addresses
10d.  IPv4 (0x0800)
11a.  IPv4
11b.  6
11c.  127.0.0.1 (or your speciﬁc IP address)
11d.  127.0.0.1 (or your speciﬁc IP address)
11e.  Local addresses
12a.  Answers will vary.  This should be seen as a high order random port.
12b.  TCP 502
12c.  Answers will vary.
12d.  Answers will vary.
12e.  Answers will vary.
13a.  Answers will vary.
13b.  Answers will vary.
13c.  Answers will vary.
14a.  Read Holding Registers
14b.  10
14c.  Answers will vary.
14d.  No

Exercise 3.4:  Using Wireshark StaƟsƟcs
2a.  98.2%
2b.  86.5%

© 2024 UƟlSec, LLC.
45

2c.  8.7%
2d.  2.9%
2e.  518
2f.  10
2g.  8
2h.  8,238,801 Bytes / 7.8 MB
2i.  1,664,406 Bytes / 1.6 MB
3a.  30
3b.  192.168.33.95
3c.  920 bytes
3d.  38.229.71.1
3e.  18481.4411
3f.  Any address which begins with 192.168.33.
4a.  api.twiƩer.com
4b.  www.nethunter.com
4c.  Cabletron-PVST-BPDU
4d.  192.124.249.10

Exercise 3.5:  InspecƟng TCP/IP Traﬃc in Wireshark
1a.  6,085
1b.  192.168.33.95
1c.  209.190.218.107
1d.  192.168.33.95
1e.  209.190.218.107
1f.  SYN packet
1g.  TCP port 80; more than likely the packet is being used to establish a connecƟon with a web server.
1h.  success.txt
1i.  DNS lookup/name resoluƟon for an IPv4 address
1j.  DNS lookup/name resoluƟon for an IPv6 address

© 2024 UƟlSec, LLC.
46

1k.  a0:36:9f:92:ca:70
2a.  File Transfer Protocol (FTP)
2b.  Packet #38
2d.  The cleartext communicaƟon over FTP.
2e.  FTP traﬃc is unencrypted by default.
2g.  In the ﬁrst session, the user is unable to login with the credenƟals provided.  In the second session,
the user is able to login.
2h.  Username: joseph / Password: StarWars@123

Exercise 3.6:  InspecƟng ICS/OT Protocols in Wireshark
1.  Modbus (Modbus/TCP)
2.  10.0.0.3
3.  10.0.0.57
4.  Force Listen Only Mode
5.
6.  Clear Counters and DiagnosƟc Register
7.
8.  1
9.  2 (0 & 0)
10. 2 (9 & 24)
11. 101 (0000)
12.  0
13.  003c  / 60 / 502
14.  0000

Part 4: Secure Network Architecture
Exercise 4.1:  The Expanded Purdue Model
1.  Level 5
2.  Level 3.5

© 2024 UƟlSec, LLC.
47

3.  IT/OT DMZ
4.  Only traﬃc from the IT/OT DMZ to IT should be allowed.  IT should not be allowed to make
connecƟons into the IT/OT DMZ.
5.  Level 3
6.  Level 0.  This is where the Process takes place where the physical systems in the real world operate.
7.  Level 2
8.  None.  It should be airgapped.
9.  Levels 2 and 3.5
10.  Levels 2 and 3
11.  Level 3.5
12.  An OT patching server on the OT network at Level 3 should pull patches from the patching server in
the IT/OT DMZ (Level 3.5) which pulls the patches from the IT network.
13.  Typically on levels 2, 3 and 3.5 (as well as potenƟally in the IT network).
14.  Traﬃc is only sent up through the Purdue Model layers towards IT, never down.
15.  Level 0
16.  CCTV cameras should not be on either the IT or OT network.  If you had to choose, CCTV cameras
should reside on the IT network.
17.  Firewalls
18.  Consider using two physical ﬁrewalls from two diﬀerent vendors.
19.  Level 2
20.  Level 1 (where the PLCs it controls reside)

Exercise 4.2:  Reviewing IT/OT DMZ Access Control Lists (ACLs)
1.  TCP port 21 is normally associated with FTP which can have several security issues including that FTP
is an unencrypted protocol, the FTP service could have soŌware vulnerabiliƟes and FTP credenƟals could
be easily guessed.
2.  TCP port 80 and 443 are normally associated with website access which can have several security
issues including HTTP traﬃc over TCP port 80 is unencrypted, the associated web services could have
soŌware vulnerabiliƟes and the web applicaƟon could have its own vulnerabiliƟes.
3.  Windows
4.  A Windows workstaƟon or server (e.g., data historian, domain controller)

© 2024 UƟlSec, LLC.
48

5.  PLC
6.  The IP address for the PLC is on another subnet from the other hosts.
7.  The single source IP address could be used for monitoring upƟme of speciﬁc hosts.
8.  UDP port 161 is normally associated with SNMP which can have several security issues including that
older versions of SNMP are unencrypted, most SNMP services are implemented with the default
community string (a.k.a. password) and provide relevant informaƟon about the host that could be used
by aƩackers.
9.  The ACL allows the host at 10.1.1.1 to access ALL hosts on ALL ports.
10.  deny ip any any

Part 5: Asset Registers and Control Systems Inventory
Exercise 5.1:  Building an Asset Register with System Conﬁgs
3.  A power plant
4.  The asset register could aid aƩackers into compromising the environment.
5.  Schneider Electric
6.  Siemens AG
7.  192.168.1.1, 192.168.1.50 and 192.168.1.78
8.  Routers (or switches acƟng as routers)
9.  Cisco Systems, Inc.
10.  Siemens AG
11.  192.168.1.210
12.  ipconﬁg /all
13.  No answer required.
14.  192.168.1.230, 192.168.1.231, 192.168.1.232
15.  These are dynamic IP addresses assigned to speciﬁc hosts by the switch via DHCP.  These hosts are
idenƟﬁed by their MAC addresses.
Exercise 5.2:  Building an Asset Register with Packet Captures
1.  192.168.25.131, 192.168.25.177
2.  192.168.25.131 = 00:1c:06:0f:bd:e5, 192.168.25.177 = 00:50:56:2b:5c:65
3.  192.168.25.131 = Siemens, 192.168.25.177 = VMware

© 2024 UƟlSec, LLC.
49

4.  TCP port 102
5.  PLC
6.  It is diﬀerent than the other subnets found in the asset registry.
7.  Siemens' S7
8.  No answer required.
9.  BACnet-APDU and BVLC
10.  Building AutomaƟon Controls
11.  Typically located on the IT network.
12.  HTTP
13.  An RFC 1918 address is one that is reserved for private internal use and is not directly routable on
the Internet.
14.  CommunicaƟon with a non-RFC 1918 address, otherwise referred to as a public or Internet address,
would typically indicate the ICS/OT network has acƟve communicaƟon with a host on the Internet.
15.  Florida InternaƟonal University
16.  David Rotella
17.  Valid locaƟons would include FIU-SOUTH-NAE35, FIU-SOUT-NAE36 and FIU-SOUTH-NAE27.

Part 6: Threat & Vulnerability Management
Exercise 6.1: Building an IT Host Scanning Target
No answers required for this exercise.
Exercise 6.2: AcƟve Scanning
6.2.A Nmap Port Scan - Default Ports
1.  No answer required.
2a.  977 closed ports
2b.  23
2c.  1,000
2d.  Only TCP ports
2e.  65,535 TCP ports and 65,535 UDP ports

© 2024 UƟlSec, LLC.
50

2f.  Any port could be of interest to an aƩacker, parƟcularly those associated with known
services that are typically vulnerable such as FTP and Telnet.
2g.  TCP port 80
2h.  TCP port 21
2i.  Answer will vary.
2j.  Answer will vary.  Should be the vendor of your virtualizaƟon plaƞorm.

6.2.B Nmap Port Scan - All Ports
1a.  65,505 closed ports
1b.  30 open ports
1c.  65,5345
1d.  Only TCP ports
1e.  Any perhaps though we'll have more context aŌer we perform service/script scans.

6.2.C Nmap Subnet Scan
1.  No answer required.
2a. Answer will vary.
2b. Answer will vary.
2c. Answer will vary.
2d. Answer will vary.
2e. Answer will vary.
2f. Answer will vary.
3.  Answer will vary.
4.  Answer will vary.

6.2.D Nmap Service Scan
1.  No answer required.

© 2024 UƟlSec, LLC.
51

2a.  2
2b.  OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
2c.  ISC BIND 9.4.2
2d.  Apache hƩpd 2.2.8 ((Ubuntu) DAV/2)
2e.  Apache Tomcat/Coyote JSP engine 1.1
2f.  MySQL 5.0.51a-3ubuntu5 on TCP 3306
2g.  PostgreSQL DB 8.3.0 - 8.3.7 on TCP 5432
2h.  VNC (protocol 3.3)
2i.  Samba smbd 3.X - 4.X
2j.  Workgroup

6.2.E Nmap NSE "Script" Scan - Single Target Host
1.  No answer required.
2a.  Anonymous access
2b.  Public SSH keys
2c.  PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME,
DSN
2d.  Yes
2e.  SSLv2
2f.  Metasploitable2 - Linux
2g.  NFS
2h.  Autocommit
2i.  /WF8(\wcknf4pYNZY1(p
2j.  VNC AuthenƟcaƟon (2)
2k.  Apache Tomcat/5.5
2l.  metasploitable
2m.  Answer will vary.

© 2024 UƟlSec, LLC.
52

2n.  No

© 2024 UƟlSec, LLC.
53

Appendix B:  List of Resources (Books)

1. "Sandworm: A New Era of Cyberwar and the Hunt for the Kremlin's Most Dangerous Hackers"
by Andy Greenberg

An incredible introducƟon to the world of ICS/OT cyber security and why it is needed in protecƟng the
world around us! It becomes even more important in helping explain the geopoliƟcal consideraƟons of
cyber security.

2. "Hacking Exposed Industrial Control Systems: ICS and SCADA Security Secrets & SoluƟons" by Clint
Bodungen, Stephen Hilt, Aaron Shbeeb, Bryan Singer and Kyle Wilhoit

Who doesn't love to learn about how to break into ICS/OT networks?

3. "PracƟcal Industrial Cyber Security: ICS, Industry 4.0 & IIoT" by Charles J. Brooks and Philip A. Craig,
Jr.

WriƩen as a study guide for the GICSP exam, the book provides an excellent overview of industrial cyber
security with some great pracƟcal examples.

4. "Countdown to Zero Day: Stuxnet and the Launch of the World's First Digital Weapons" by Kim ZeƩer

For many of us, Stuxnet is where it all begins. Similar to Sandworm, this is a great book that's an easy
read to get lost in.

5. "Industrial AutomaƟon and Control Systems Security Principles" by Dr. Ronald Krutz

The "oﬃcial" ICS/OT cyber security guide sponsored by ISA and provided during the ISA/IEC 62443
cerƟﬁcaƟon courses.

6. "Industrial Cybersecurity"* by Pascal Ackerman

While there are diﬀerent "ediƟons" of the book, each is really a completely diﬀerent book.

Each is a monster in their own right but deﬁnitely references you want to have on hand if you're on-site
and have no Internet access for research!

7. "Engineering-Grade OT Security: A Manager's Guide" by Andrew Ginter

Be sure to check out his other two books as well! I'm just starƟng this new release!

8. ImplemenƟng IEC 62443 - A PragmaƟc Approach to Cybersecurity by Michael D. Medoﬀ and Patrick
C. O'Brien

Understanding how to implement ISA/IEC 62443 can be daunƟng at ﬁrst, but it doesn't have to be.

© 2024 UƟlSec, LLC.
54

9. Industrial Cybersecurity: Case Studies and Best PracƟces by Steve Mustard

Real world examples and case studies can oŌen be the best way to learn!

10. "Industrial Network Security: Securing CriƟcal Infrastructure Networks for Smart Grid, SCADA, and
Other Industrial Control Systems" by Eric D. Knapp.
