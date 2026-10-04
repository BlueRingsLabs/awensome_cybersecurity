---
id: ckb-2d76e16b1fb0
title: Forensic Investigation of Nmap Scan Using Wireshark
category: incident-response-and-forensics
format: guide
language: en
tags: [forensics, linux, networking, nmap]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.47
---

 Page 2 of 28

Contents
Introduction .......................................................................................3
Requirement ......................................................................................3
Nmap ARP Scanning ...........................................................................3
Step to Identify Nmap ARP Scan ...................................................................... 4
Nmap ICMP Scanning .........................................................................6
Step to Identify NMAP ICMP Scan .................................................................... 7
Identify TCP Flags ............................................................................................. 9
Default NMAP Scan (Stealth Scan) .................................................... 11
Step to Identify NMAP Default Scan (Stealth Scan) ........................................ 12
Analysis TCP Header Details ........................................................................... 13
Nmap TCP Scan ................................................................................ 16
Step to Identify NMAP TCP Scan .................................................................... 16
Nmap FIN Scan ................................................................................. 19
Step to Identify NMAP FIN Scan ..................................................................... 20
Analysis TCP Header Details ........................................................................... 21
Nmap NULL Scan .............................................................................. 21
Step to Identify NMAP Null Scan .................................................................... 22
Analysis TCP Header Details ........................................................................... 23
Nmap XMAS Scan............................................................................. 24
Step to Identify NMAP XMAS Scan ................................................................. 24
Nmap UDP Scan ............................................................................... 26
Step to Identify NMAP UDP Scan ................................................................... 27
Analysis UDP Header Details .......................................................................... 28

 Page 3 of 28

Introduction
Today we are discussing how to read hexadecimal bytes from an IP packet that helps a network admin
identify various types of NMAP scanning. But before moving ahead, please read our previous articles,
"Network packet forensic" and "NMAP scanning with Wireshark".
Requirement
Attacking Tool: Nmap
Analysis Tool: Wireshark

We are going to calculate the hexadecimal bytes of Wireshark using the given below table. As we know,
Wireshark captures network packets mainly of 4 layers, which are described below in the table as per
the OSI layer model and the TCP/IP layer model.

Nmap ARP Scanning
Let ’s start!!
Hopefully, the reader is familiar with basic NMAP scanning techniques; if not, read about it here. Now,
open the terminal and run the "HOST SCAN" command to identify a live host in the network.

Nmap performs host scans with the –sP/–sn flag and broadcasts ARP request packets to determine
which IP address is assigned to the specific host machine.You can see that "1 host up" message in the
image below.
Working of ARP Scan for Live Host
1. Send ARP request for MAC address
2. Receive MAC address through ARP Reply packet
nmap -sn 192.168.1.100

 Page 4 of 28

Step to Identify Nmap ARP Scan

Collect Ethernet Header details
In this case, we used Wireshark to capture network packets from the victim's network, and to analyse only
the ARP packet, we used the filter " ip.addr == VICTIM IP || arp," as shown in the image below. Here you
will find 2 arp packets. Basically, the 1st arp packet is broadcasting IP to ask for the MAC address of that
network, and the 2nd packet is unicast and contains the answer to the IP query.
Now let’s read the hex value of the Ethernet header for identifying source and destination Mac addresses.
Along with that, we can also enumerate the bytes used for an encapsulated packet, in order to identify
what Ether type is being used here.

Hence, from the Ethernet header, we can conclude that it is an ARP broadcast packet asking for a
destination Mac address. There shouldn’t be any uncertainty in concern with the source Mac address of
the person responsible for sending the packet, but if we talk about the destination Mac address, then we
get ff:ff:ff:ff:ff:ff:ff which means the exact destination is the machine that is not available here. Further
moving ahead, we found Ether type 0x0806 highlighted in yellow, which is used for the ARP protocol.

 Page 5 of 28

Collect ARP Header (Request/Reply)
In order to identify an ARP scan, you need to investigate some important parameters that could help a
network admin make a correct assumption in regard to an ARP scan.
Try to collect the following details as given below:

Opcode (Request/Reply)

Source Mac

Source IP

Destination MAC

Destination IP

With the help of the following table, you can read the hex value highlighted in the above and below images
for ARP Request and Reply packets, respectively.

 Page 6 of 28

Nmap ICMP Scanning
Now run the "HOST SCAN" command to identify a live host in a network by sending a Ping request with
the help of an ICMP packet.

Now above command will send ICMP request packet instead of ARP request for identifying the live host
in a network.
Working of NMAP ICMP Ping when a host is live:
1. Send ICMP echo request packet.
2. Receive ICMP echo reply.

Send TCP SYN packet on any TCP port (this port must be rarely blocked by network admin).
1. Receive TCP RST-ACK from target’s Network.
As a result, NMAP displays the "HOST UP" message shown in the image below.
nmap -sn 192.168.1.100 --disable-arp-ping

 Page 7 of 28

Step to Identify NMAP ICMP Scan

Collect IP header details for the protocol version.
For reading data from Ethernet heads, visit our previous article, "Network packet forensic".
NOTE: Ether type for IPv4 is 0x0800
With the help of the IP header of a packet, since we know ICMP is a Layer 3 protocol according to the
OSI model, we need to focus on the following details for ICMP forensics.
Try to collect the following details as given below:
1. Ip header length 20 Bytes (5bits*4=20 bytes)
2. Protocol (01 for ICMP)
3. Source IP
4. Destination IP
From the given below image, you can observe the hexadecimal information of the IP header field and,
using the given table, you can study these values to obtain their original value.

 Page 8 of 28

The IP header length is always given in form of the bit and here it is 5 bit which is also minimum IP header
length and to make it 20 bytes multiple 5 with 4 i.e. 5*4 bytes =20 bytes.
Identify ICMP Message type (Request /Reply)
As we discussed above, according to the Nmap ICMP scanning technique, the 1st packet should be an
ICMP echo request packet and the 2nd packet should be an ICMP echo reply packet.

With the help of the following table, you can read the hex values highlighted in the above and below
images for ICMP Request and Reply packets, respectively.

 Page 9 of 28

Identify TCP Flags
As discussed above, after the ICMP reply, the 3rd packet should be of the TCP-SYN packet and the
4th should be of the TCP-RST/ACK packet. As we have seen in our previous article, the hex value of all
TCP-Flags is different from each other, so if we are talking about the TCP-SYN flag, then its hex value
should be 0x02.
From the given below table, you can observe the sequence of TCP flag and how bits of these flags are set
for sending the packet to the destination port.
For example, if you found a TCP SYN packet, then the bit for the SYN flag is set to 1, for which the binary
value will be 000000010 and its hexadecimal value will be 0x02.
NS
CWR
ECE
URG
ACK
PSH
RST
SYN
FIN
0
0
0
0
0
0
0
1
0

 Page 10 of 28

Sometimes you will get a combination of two or more flags in the TCP header, so in that scenario, take
the help of the following table to read the hex value of such a packet to identify which TCP flag bits are
being set 1.
For example, if you found TCP SYN/ACK packets then indicates that SYN & ACK flags are set 1 for which
the binary value will be 000010010 and its hexadecimal will be 0x12

NS
CWR
ECE
URG
ACK
PSH
RST
SYN
FIN
0
0
0
0
1
0
0
1
0

Therefore, I designed the below table to let you know more about the Hex value when two or more than
two flags are set 1.

The image given above contains the hex value of TCP-SYN packets, and the image given below contains
the hex value of TCP-RST/ACK packets, from which we can calculate the source port and the destination
port of the packet, respectively, as shown in the image given below.

 Page 11 of 28

Conclusion!
So as stated above regarding the working of NMAP ICMP scan, we had obtained the hex value for every
packet in the same sequence. Obtaining the hex value for every packet in such sequence gives the
indication to the Penetration tester that Someone has Choose NMAP ICMP scan for Network
enumeration.

Default NMAP Scan (Stealth Scan)
Here we are going with the default scan method to enumerate the "open" state of any specific port.
Working of Default Scan for open port:

1. Send TCP-SYN packet
2. Receive TCP-SYN/ACK
3. Send TCP-RST packet
It is also known as half Open TCP Scan as it does not send ACK packet after receive SYN/ACK packet.
nmap -p80 192.168.1.100

 Page 12 of 28

Step to Identify NMAP Default Scan (Stealth Scan)
Gather IP Header Information for Protocol Version
For reading data from Ethernet heads, visit our previous article, "Network packet forensic".
NOTE: Ether type for IPv4 is 0x0800.
Try to collect the following details as given below:
1. Ip header length 20 Bytes (5bits*4=20 bytes)
2. Protocol (6 for TCP)
3. Source IP
4. Destination IP

From the given below image, you can observe the hexadecimal information of the IP header field and,
using the given table, you can study these values to obtain their original value.

 Page 13 of 28

Analysis TCP Header Details

From the above image, we had to obtain the source and destination IP and protocol used for
communication, i.e., TCP. Now we need to identify the source and destination port and TCP Flag used for
establishing the connection between two systems.
In the image, we have highlighted the source port in "light brown colour" and the destination port in
"yellow colour". You can use the given table to read the hex value of the given image.

So, we come to know that here TCP-SYN packet is used for sending connection request on Port 80.

 Page 14 of 28

Again, we read the next packet. Here we found that hex value 12 indicates that TCP-SYN/ACK has been
sent from port 80.

Use the help given above to read the hex value of the given image. Hex value 12 for the TCP flag is used
for SYN + ACK as explained above, and we get 0x12 by adding the hex values "0x02 of SYN" and "0x10 of
ACK".

 Page 15 of 28

In the image given below, we come to know that the TCP-RST packet is used for sending a reset connection
to Port 80.

Conclusion!
So, as declared above, regarding the working of NMAP default scan or NMAP stealth scan, we had to
obtain the hex value for every packet in the same sequence. Obtaining the hex value for every packet in
such a sequence gives an indication to the penetration tester that someone has chosen the NMAP default
scan for network enumeration.

 Page 16 of 28

Nmap TCP Scan
Here we are going with TCP scan to enumerate state of any specific port

Working of Default Scan for open port:
1. Send TCP-SYN packet
2. Receive TCP-SYN/ACK
1. Send TCP-ACK packet
2. Send TCP-RST/ACK packet

Step to Identify NMAP TCP Scan

Collect IP Header Details for Protocol Version
nmap -sT -p80 192.168.1.100

 Page 17 of 28

For reading data of Ethernet head visit to our previous article "Network packet forensic".
NOTE: Ether type for IPv4 is 0x0800.
Try to collect the following details as given below:
1. Ip header length 20 bytes (5bits*4=20 bytes)
2. Protocol (06 for TCP)
3. Source IP
4. Destination IP

It is quite similar to the NMAP stealth scan, and using a given table, you can study these values to obtain
their original value.


Analysis TCP Header Details
NMAP TCP Scan follows 3-way handshake of TCP connection for enumeration open port. Identifying
source and destination port along with Flag hex value (TCP-SYN) are similar as above.

 Page 18 of 28

So, we come to know that the TCP-SYN packet is used for sending connection requests on Port 80.

Again, we read the next packet. Here we found that hex value 12 indicates that TCP-SYN/ACK has been
sent via port 80.

 Page 19 of 28

The only difference between Stealth Scan and TCP Scan is that here an ACK flag is sent by the source
machine who initiated the TCP communication. Again, we read the next packet. Here we found that hex
value 0x10 indicates that TCP- ACK has been sent via port 80.

Conclusion!
So, as stated above regarding the working of the NMAP TCP scan, we had obtained the hex value for every
packet in the same sequence. Obtaining the hex value for every packet in such a sequence gives an
indication to the penetration tester that someone has chosen the NMAP default scan for network
enumeration.
NOTE:  For packet TCP-RST/ACK the hex value will be " 0x14" send by the attacker machine

Nmap FIN Scan
In this case, we'll use TCP-FIN to enumerate the "OPEN" state of a specific port in any Linux-based system,
so run the command below.

FIN's OperationScan for open ports: Send 2 packets of TCP-FIN to a specific port.
FIN is part of the TCP flag and NMAP uses the FIN flag to initiate TCP communication instead of following
three-way handshake communication.
nmap -sF -p22 192.168.1.104

 Page 20 of 28

Step to Identify NMAP FIN Scan
Collect IP Header Details for Protocol Version
For reading data from Ethernet heads, visit our previous article, "Network packet forensic".
NOTE: Ether type for IPv4 is 0x0800
Try to collect the following details as given below:
1. Ip header length 20 Bytes (5 bits*4=20 bytes)
2. Protocol (06 for TCP)
3. Source IP
4. Destination IP
You can study these values using the table below to determine their original value.

 Page 21 of 28

Analysis TCP Header Details
Now let's identify the source and destination ports along with the flag hex value (TCP-FIN) so they are
similar as above.

So, through the given below image and with the help of a table, we came to know that the TCP-FIN packet
is used for sending connection requests on Port 22.
Conclusion:
So, as declared above regarding the working of the NMAP FIN scan, we had obtained the hex value for
every packet in the same sequence.
Obtaining the hex value for every packet in such a sequence gives an indication to the penetration tester
that someone has chosen NMAP FIN scan for network enumeration.
NOTE: The presence of the first FIN packet (0x01) and the second RST packet (0x04) on the targeted
network indicates a "Closed Port."

Nmap NULL Scan
Here we are going with TCP Null scan to enumerate “OPEN” state of any specific port in any Linux based
system.

nmap -sN -p22 192.168.1.104

 Page 22 of 28

To use Null Scan for an open port, send two TCP-NONE packets to a specific port. Instead of using the
three-way handshake protocol, NMAP used the NONE flag (No flag) to initiate TCP communication, and
the bits of each flag were set to "0."

Step to Identify NMAP Null Scan

Collect IP Header Details for Protocol Version
For reading data from Ethernet heads, visit our previous article, "Network packet forensic".
NOTE: Ether type for IPv4 is 0x0800
Try to collect the following details as given below:
1. Ip header length 20 Bytes (5bits*4=20 bytes)
2. Protocol (06 for TCP)
3. Source IP
4. Destination IP
You can study these values using the provided table to determine their original value.

 Page 23 of 28

Analysis TCP Header Details
Now let’s identify the source and destination ports along with the flag hex value (TCP-NONE) that is similar
to above.

So, through the given below image and with the help of a table, we come to know that here the TCP-NONE
packet is used for sending connection requests on Port 22.
Conclusion:
So, as stated above regarding the working of the NMAP NONE scan, we had obtained the hex value for
every packet in the same sequence.
Obtaining the hex value for every packet in such a sequence gives an indication to the penetration tester
that someone has chosen NMAP NONE scan for network enumeration.

NOTE: If you find the first NONE packet (0x00) and the second RST packet (0x04) on the target network,
it indicates a "Closed Port."

 Page 24 of 28

Nmap XMAS Scan
In this case, we'll use the XMAS scan to list the "OPEN" state of any specific port in any Linux-based system.

Send 2 packets of TCP Flags containing FIN, PSH, and URG on the specific port to perform an XMAS Scan
for open ports.
Instead of following three-way handshake communications, NMAP used three TCP flags (FIN, PSH, and
URG) to initiate TCP communication, with a bit of each flag set to "1."

Step to Identify NMAP XMAS Scan

Collect IP Header Details for Protocol Version
nmap -sX -p22 192.168.1.104

 Page 25 of 28

For reading data from Ethernet heads, visit our previous article, "Network packet forensic".
NOTE: Ether type for IPv4 is 0x0800
Try to collect the following details as given below:
1. Ip header length 20 Bytes (5bits*4=20 bytes)
2. Protocol (06 for TCP)
3. Source IP
4. Destination IP
It is quite similar to NMAP above Scan and using the given table you can study these values to obtain their
original value.


Analysis TCP Header Details
Now let's identify the source and destination ports along with the flag hex value (TCP-XMAS) similar as
above.

 Page 26 of 28

So, through the given below image and with the help of the table, we come to know that here TCP flags
{FIN, PSH, URG packets are used for sending connection requests on Port 22.
Conclusion!
So, as stated above regarding the working of the NMAP XMAS scan, we had obtained the hex value for
every packet in the same sequence.
Obtaining the hex value for every packet in such a sequence gives the indication to the penetration tester
that someone has chosen NMAP XMAS scanned for network enumeration.
NOTE:

If you discovered the first FIN, PSH, or URG packet (0x29) and the second RST packet (0x04) on
the targeted network, indicate "Closed Port.

"NMAP FIN, NMAP NULL, and NMAP XMAS scans are only applicable on Linux-based systems.

Nmap UDP Scan
Here we are going with XMAS Scan to enumerate the state of any specific port in any Linux based system.

The operation of the XMAS Scan for open ports is as follows: Send 2 packets of UDP to a specific port.
It is quite different from the TCP communication process in that here no flag is used for establishing a
connection or initiating a connection request with the target’s network.
nmap -sU -p 68 192.168.1.104

 Page 27 of 28

Step to Identify NMAP UDP Scan

Collect IP Header Details for Protocol Version
For reading data from Ethernet heads, visit our previous article, "Network packet forensic".
NOTE: Ether type for IPv4 is 0x0800
Try to collect the following details as given below:
1. Ip header length 20 Bytes (5 bits*4=20 bytes)
2. Protocol (11 for UDP)
3. Source IP
4. Destination IP
It is very similar to the NMAP above scan in that the "IP header" and "Ethernet header" information will
be the same whether it is TCP communication or UDP communication, and you can study these values to
obtain their original value using the provided table.

Basically, 11 is the hex value used for the UDP protocol, which is quite useful in identifying NMAP UDP
scans from remanding scanning methods.

 Page 28 of 28

Analysis UDP Header Details
Now let's identify the source and destination ports, as done above in TCP Scanning.

Conclusion!
Obtaining the hex value for every packet in such a sequence gives the penetration tester an indication
that someone has chosen NMAP UDP scan for network enumeration.
NOTE: If the first UDP packet and the second UDP with an ICMP Message Port are both unreachable, it
indicates that the target network has a "Closed Port."

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
