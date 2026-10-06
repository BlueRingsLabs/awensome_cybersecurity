---
id: ckb-5cde9238fba5
title: Building a Local AI Environment
category: network-and-wireless-security
format: guide
language: en
tags: [credential-access, linux, networking, password-security, windows, wireless]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.76
---

Wireless PenetraƟon TesƟng: Airgeddon

                                                                                                 1 | P a g e

Wireless Penetration Testing: Airgeddon

                                                                                                 2 | P a g e

Contents
IntroducƟon ............................................................................................................................................ 3
Install Airgeddon & Usage ....................................................................................................................... 3
Airgrddon Features: ............................................................................................................................ 3
Capturing Handshake & DeauthenƟcaƟon ............................................................................................. 6
Launch DeauthenƟcaƟon Atack ............................................................................................................. 9
Aircrack DicƟonary Atack for WPA Handshake .................................................................................... 11
Airacrack Brute Force Atack for WPA Handshake ................................................................................ 14
Hashcat Rule-Based Atack for WPA Handshake ................................................................................... 16
Evil Twin Atack ..................................................................................................................................... 18
Capturing WPA Handshake and Saving CredenƟals ...................................................................... 22
Seƫng Up the CapƟve Portal ........................................................................................................ 22
PMKID Atack ........................................................................................................................................ 27

Wireless Penetration Testing: Airgeddon

                                                                                                 3 | P a g e

Introduction
You'll discover how to use airgeddon for Wi-Fi hacking in this arƟcle. It enables the capture of the
WPA/WPA2 and PKMID handshakes in order to start a brute force assault on the Wi-Fi password key.
It also aids in the creaƟon of a ﬁcƟƟous AP for launching Evil Twin Atack by luring clients into the
capƟve portal.
Let start by idenƟfying the state for our wireless adaptor by execuƟng the ifconﬁg wlan0 command.
Wlan0 states that our wiﬁ connecƟon mode is enabled in our machine.

Install Airgeddon & Usage
Airgrddon Features:
•
Full support for 2.4Ghz and 5Ghz bands
•
Assisted WPA/WPA2 personal networks Handshake ﬁle and PMKID capturing
•
Interface mode switcher (Monitor-Managed)
•
Oﬄine password decrypƟng on WPA/WPA2 captured ﬁles for personal networks
(Handshakes and PMKIDs) using a dicƟonary, bruteforce and rule-based atacks with aircrack,
crunch and hashcat tools. Enterprise networks captured password decrypƟng based on john
the ripper, crunch, asleap and hashcat tools.
•
Evil Twin atacks (Rogue AP)
•
WPS features
Download and run the airgeddon script by running the following commands in Kali Linux.
Note: execute the script as root or superuser.
git clone https://github.com/v1s1t0r1sh3r3/airgeddon.git
cd airgeddon
 ./airgeddon.sh
Wireless Penetration Testing: Airgeddon

                                                                                                 4 | P a g e

It will ﬁrst check for all dependencies and necessary tools before launching this framework. It will
atempt to instal the essenƟal tools if they are missing, which may take some Ɵme. As indicated
in the picture once the installaƟon is complete, you will see the OK status for both required and
opƟonal tools.
Wireless Penetration Testing: Airgeddon

                                                                                                 5 | P a g e

Now choose the network interface; for a wireless connecƟon, this will be wlan0; hence, choose
opƟon 3 as seen in the image.

Next, we'll put the Wi-Fi card in monitor mode; the card is in managed mode by default, which
means it can't capture packets from various networks; however, Wi-Fi in monitor mode can capture
packets passing across the air.
Wireless Penetration Testing: Airgeddon

                                                                                                 6 | P a g e

Select opƟon 2 for Monitor mode.
Note:
Monitor mode is the mode for monitoring traﬃc, usually on a particular channel. A lot of wireless
hardware is capable of ENTERing monitor mode, but the ability to set the wireless hardware into
monitor mode depends on support within the wireless driver. As such, you can force many cards into
monitor mode in Linux, but in Windows, you will probably need to write your own wireless network
card driver.

Capturing Handshake & Deauthentication
The wlan0mon is in monitor mode, we try to can capture the handshake packets of the wireless
network for WPA and WPA2 protocol.
Choose opƟon 5 to obtain the tool for capturing Handshake/PMKID
Wireless Penetration Testing: Airgeddon

                                                                                                 7 | P a g e

Choose opƟon 6 to select capture the handshake.
When you select opƟon 6, a new window will appear, scanning for WPA and WPA2 networks and
atempƟng to capture the 4-way handshake in a.cap ﬁle. AŌer geƫng Target's AP (Access Point), you
can press CTRL^C.
Wireless Penetration Testing: Airgeddon

                                                                                                 8 | P a g e

It will display a list of all ESSIDs (Wi-Fi names) examined, as well as their BSSID (MAC Address) and
ENC encrypƟon protocol type. Then, as we did for ESSID "Raaj," you can pick your target by supplying
a Serial Number.
NOTE: The asterisks (*) indicate client access points; they are maybe the best "clients" for acquiring
handshakes. Any Access Point that implements the WEP ENC protocol will be ignored by Airgeddon.
Wireless Penetration Testing: Airgeddon

                                                                                                 9 | P a g e

Launch Deauthentication Attack
This atack sends disassociate packets to one or more clients which are currently associated with a
parƟcular access point. DisassociaƟng clients can be done for several reasons:
•
Recovering a hidden ESSID. This is an ESSID that is not being broadcast. Another term for this
is “cloaked”.
•
Capturing WPA/WPA2 handshakes by forcing clients to reauthenƟcate
Wireless Penetration Testing: Airgeddon

                                                                                                 10 | P a g e

•
Generate ARP requests (Windows clients someƟmes ﬂush their ARP cache when
disconnected)
Now it will prompt you to select an atack-type; choose opƟon 2 for Death replay atack, which will
uƟlise deauth atack to disconnect all clients before capturing the AP-client handshake. Then, for a
Ɵmeout, select a period in seconds.

You'll see that two windows appear. AŌer deauthenƟcaƟon, one will atempt to undertake a deauth
atack, while the other will atempt to record the 4 Way handshake between the client and the
access point.

Wait unƟl the WPA Handshake shows in the top right corner of the window, then press CTRL^C.
Wireless Penetration Testing: Airgeddon

                                                                                                 11 | P a g e

As you can see, the WPA handshake for AP "raaj". You can now store this .cap ﬁle to your systems.

Aircrack Dictionary Attack for WPA Handshake
The Wi-Fi password was kept in a handshake ﬁle, but because it was encrypted, we had to decrypt it
to get the password. Return to the main menu by selecƟng opƟon 0.

It will show you the atack opƟons; select opƟon 6 for the oﬄine WPA/WPA2 decrypt menu.
Wireless Penetration Testing: Airgeddon

                                                                                                 12 | P a g e

Choose opƟon 1 to select Personal.

Now we will use a dicƟonary to decrypt the handshake captured ﬁle. Select opƟon 1 as shown in the
image. By default, it will take the last captured ﬁle to be brute force, ENTER Y to select the path and
BSSID the last the captured ﬁle.  Then provide the path of your dicƟonary or rockyou.txt and press
ENTER key to start a dicƟonary atack against the WPA handshake.
Wireless Penetration Testing: Airgeddon

                                                                                                 13 | P a g e

The password or Wi-Fi key will then be shown, as illustrated in the ﬁgure below. If you want to save
the key, it will prompt you to do so.
Wireless Penetration Testing: Airgeddon

                                                                                                 14 | P a g e

Airacrack Brute Force Attack for WPA Handshake
Select opƟon 2 to conduct a brute force atack against the WPA handshake ﬁle, which will decode
the packets using crunch and aircrack. By default, it will brute force the last captured ﬁle. ENTER Y to
pick the directory, and BSSID the last captured ﬁle. Then ENTER the path to your dicƟonary or
rockyou.txt and click the ENTER key to begin a brute force atack on the WPA handshake.
Wireless Penetration Testing: Airgeddon

                                                                                                 15 | P a g e

Select the character set, in this instance opƟon 6 to select the Lowercase + Numeric chars that will
atempt to brute force the Wi-Fi key using an alphanumeric character set. To begin the atack, press
the ENTER key.

If the atempt is successful, the password or Wi-Fi key will be displayed, as illustrated in the ﬁgure
below.
Wireless Penetration Testing: Airgeddon

                                                                                                 16 | P a g e

Hashcat Rule-Based Attack for WPA Handshake
Because we are all familiar with the capability of hashcat, airgeddon provides the opportunity to
uƟlise hashcat to crack the Wi-Fi key. Choose opƟon 5 and enter the path to your WPA handshake
ﬁle, dicƟonary, or rule-based ﬁle.
Here we provide the path to the best64.rule ﬁle, which will be used to perform a hashcat rule bashed
atack.

Press ENTER to start the atack, and it will try to decrypt the WPA encrypted communicaƟon.
Wireless Penetration Testing: Airgeddon

                                                                                                 17 | P a g e

AŌer a successful trial, it will prompt you to save the output result. To save the enumerated key, use
the ENTER key.
Wireless Penetration Testing: Airgeddon

                                                                                                 18 | P a g e

You can access the saved ﬁle to read the decrypted Wi-Fi password.

Evil Twin Attack
An evil twin is a forgery of a Wi-Fi access point (Bogus AP) that masquerades as genuine but is
purposefully set up to listen in on wireless traﬃc. By creaƟng a fake website and enƟcing people to it,
this type of atack can be used to obtain credenƟals from the legiƟmate clients.
From the main menu, select opƟon 7 for Evil Twin atack.

Then select opƟon 9, which will scan for nearby Access Points.
Wireless Penetration Testing: Airgeddon

                                                                                                 19 | P a g e

ConƟnue by pressing the ENTER key, and a window for scanning WPA/WPA2 access points will
appear.

To terminate the scan, use CTRL^C, and it will display a list of all Access Points that it has scanned.
Choose the AP that piques your curiosity.
Wireless Penetration Testing: Airgeddon

                                                                                                 20 | P a g e

Select opƟon 2 for a Deauth atack to disconnect the client from a selected AP. AŌer that, it may ask
to enable DoS pursuit mode, which we reject.

Before launching the deauth and atempƟng to capture the handshake, it will ask a few quesƟons
such as:
Do you want to spoof your Mac address during this atack [y/N]: y
Do you already have a captured ﬁle [y/N]: N
Time value in second:20
Press ENTER key to accept the proposal.
Wireless Penetration Testing: Airgeddon

                                                                                                 21 | P a g e

The two windows will appear again. One will atempt a deauth atack, while the other will atempt to
capture the WPA handshake between the client and the access point aŌer deauthenƟcaƟon.

Wait unƟl the WPA Handshake shows in the top right corner of the window, then press CTRL^C.

Wireless Penetration Testing: Airgeddon

                                                                                                 22 | P a g e

Capturing WPA Handshake and Saving Credentials
As you can see, we now have the WPA handshake for AP "raaj." Accept the proposal by saving the
cap ﬁle to your systems and pressing the ENTER key. Then, if you're using a capƟve portal, you'll be
asked to specify a path for the ﬁle that will hold the Wi-Fi password.
If the password for the Wi-Fi network is achieved with the capƟve portal, you must decide where to
save it: /root/rajpwd.txt

Setting Up the Captive Portal
Create a capƟve portal to phish your client and select the language in which the web portal will be
displayed to the client.
For English, we chose opƟon 1. Six windows will open as soon as you submit the selected opƟon.

AP: create a fake AP “raaj” for client.
DHCP: Start a bogus DHCP service to provide malicious IP to the client.
DNS: IniƟate with the malicious DNS query
Deauth: DeauthenƟcate the client from the original AP “raaj”.
Webserver: Start a service to host the capƟve portal.
Control: Try to sniﬀ the Wi-Fi password once the client connects with a fake AP.
Wireless Penetration Testing: Airgeddon

                                                                                                 23 | P a g e

Note: Do not close the windows; they will dissipate aŌer the password has been captured.

All clients connecƟng to the original AP "raaj" will be disconnected, and when they atempt to
reconnect, they will discover two APs with the same name. When the client connects to the bogus
AP, it is lured to the capƟve portal.
Wireless Penetration Testing: Airgeddon

                                                                                                 24 | P a g e

Wireless Penetration Testing: Airgeddon

                                                                                                 25 | P a g e

The capƟve web portal will ask to submit the Wi-Fi password key to get internet access.
Wireless Penetration Testing: Airgeddon

                                                                                                 26 | P a g e

Wireless Penetration Testing: Airgeddon

                                                                                                 27 | P a g e

If the client gives the Wi-Fi key, the password will be captured in plaintext in the control window.

AddiƟonally, save the password in the ﬁle you gave during the proposal.

PMKID Attack
PMKID is the unique key idenƟﬁer used by the AP to keep track of the PMK being used for the client.
It is a derivaƟve of AP MAC, Client MAC, PMK, and PMK Name. Read more from here
Let us capture PMKID by running the airgeddon script, select opƟon 5 as shown below.
Wireless Penetration Testing: Airgeddon

                                                                                                 28 | P a g e

Then again press 5 and wait for the script to capture SSIDs around.

Now you'll see a list of targets. Our goal for number 6 is “Amit 2.4 G.” Then simply ENTER the Ɵmeout
in seconds that you want the script to wait for before capturing the PMKID. Let's suppose 25 seconds
is ample Ɵme.
Wireless Penetration Testing: Airgeddon

                                                                                                 29 | P a g e

Sure enough, we can see a PMKID being captured here!

Wireless Penetration Testing: Airgeddon

                                                                                                 30 | P a g e

Then simply store this PMKID as a cap ﬁle. First press Y then ENTER the path and done.

Now, with an integrated aircrack-ng we can crack the cap ﬁle within airgeddon script itself like this:
Just choose dicƟonary atack and yes and then the dicƟonary ﬁle.

Sure enough, we have the password we needed
Wireless Penetration Testing: Airgeddon

                                                                                                 31 | P a g e

Reference:
htps://www.oreilly.com/library/view/network-security-tools/0596007949/ch10s03s01.html
htps://www.aircrack-ng.org/doku.php?id=deauthenƟcaƟon
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
