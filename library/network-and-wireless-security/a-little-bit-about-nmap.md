---
id: ckb-da567539554f
title: A little bit about Nmap
category: network-and-wireless-security
format: article
language: en
tags: [dns, firewall, networking, nmap, privilege-escalation, tls]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.72
---

# A little bit about Nmap

[Nmap](https://nmap.org/) is powerful tool. Mostly used for network discovery and security auditing. If you want to know more about what assets are in your network and what services they are running, Nmap is best choice. I will also describe few other similar tools like [arp-scan](https://linux.die.net/man/1/arp-scan) or [masscan](https://github.com/robertdavidgraham/masscan).

![Nmap](nmapmain.jpg)

At first glance, the tool may seem easy to use. And so it is in the simplest cases. Unfortunately, the lack of knowledge of how Nmap works and inadequate selection of the appropriate parameters can cause quite a lot of traffic on the network, unnecessary attention to your actions and a waste of time, waiting for the result that can be obtained much faster.

This is why there is so many memes about Nmap.

![Nmap Meme](nmapmeme.jpg)

I hope that after reading this article you will understand what is funny in command like this (it is really funny):

```bash
nmap -v 10.0.0.0/8
```

Nmap during the scan and choosing different parameters go through steps like:

- Enumerate targets
- Discovery live hosts
- Reverse-DNS lookup
- Scan ports
- Detect versions
- Detect OS
- Traceroute
- Scripts
- Write output

In any reconnaissance you would do the same one by one, using various tools or system commands. Nmap allows you automate this process and display results all in one.

Everything starts from question what is your target. Is it just one IP or subnet? I don’t need to remind you that network basics are required to use Nmap. Make sure that before you start reading this article and using Nmap you are familiar with [ISO/OSI model](https://en.wikipedia.org/wiki/OSI_model), [TCP/IP protocols](https://en.wikipedia.org/wiki/Internet_protocol_suite), [TCP Header and TCP flags](https://en.wikipedia.org/wiki/Transmission_Control_Protocol).

## Enumerate targets

Nmap targets can be defined as a list, a range, or a subnet. In list you can add IPs, domains and subdomains. Range refers to IP and looks like 10.10.10.1-20, this will scan range from 10.10.10.1 to 10.10.10.20. Subnet is for example 10.10.10.1/30. To check how many hosts and usable host will be scanned you can always use a [Network Calculator](https://www.calculator.net/ip-subnet-calculator.html?cclass=any&csubnet=30&cip=10.10.10.1&ctype=ipv4&printit=0&x=72&y=10). Last option is to add list of targets as a parameter `nmap -iL list_of_hosts.txt`.

If you want to check list without scanning use `nmap -sL list_of_hosts.txt`. To avoid reverse-DNS resolution during standard scan add parameter `-n`.

## Discovery live hosts

Hosts can be discovered using **ARP**, **ICMP**, **TCP/UDP** and **Reverse-DNS lookup**.

**ARP** sending request to broadcast address of network segment and ask computer with specific IP to provide it’s **MAC address**. **ICMP** is just ping (**ICMP Echo**). **TCP and UDP** are packets sent for common ports to check target response. By default Nmap also do **Reverse-DNS lookup**, if you want to skip Reverse-DNS use `-n` and if you want to force it even for offline hosts use `-R`.

It is important to understand that Nmap uses different way to discover hosts and it depends on user privileges. Here are examples:

If you run Nmap as `root` on **local network** it will use **ARP request**. ARP scanning is possible only for local network. Use `-PR` parameter. You can also use `arp-scan` tool typing command `arp-scan -l` to scan local network. So just to discover hosts without port scanning you can use: `nmap -PR -sn 10.10.10.1/24` or `arp-scan -l`

If you run Nmap as `root` **outside local network** it will send **ICMP echo requests**, **TCP ACK** to port 80, **TCP SYN** to port 443, and **ICMP timestamp request**. Command: `sudo nmap -PE -sn 10.10.10.1/24`. ICMP echo request can be blocked by firewall so you can run ICMP Timestamp `-PP` or ICMP Address Mask `-PM`.

If you run Nmap as `normal` user **outside local network** then it starts **TCP 3-way handshake** by sending **SYN packets** to ports 80 and 443. To run **TCP SYN ping** use `-PS` parameter with port number. Similar for **TCP ACK Ping** use `-PA` with por and **UDP Ping** `-PU`

After discovery Nmap scans only live host. To check only for live hosts without port scan use parameter `-sn`.

[Masscan](https://github.com/robertdavidgraham/masscan) is similar tool, it can quickly scan network but it is aggressive and make a lot of noise. Example of use: `masscan 10.10.10.1/24 -p443`.

## Port Scan

When you are scanning ports, they can have different states. Let’s take a look at [Nmap documentation](https://nmap.org/book/man-port-scanning-basics.html). I copied part about states below.

**The six port states recognized by Nmap**

**open**

*An application is actively accepting TCP connections, UDP datagrams or SCTP associations on this port. Finding these is often the primary goal of port scanning. Security-minded people know that each open port is an avenue for attack. Attackers and pen-testers want to exploit the open ports, while administrators try to close or protect them with firewalls without thwarting legitimate users. Open ports are also interesting for non-security scans because they show services available for use on the network.*

**closed**

*A closed port is accessible (it receives and responds to Nmap probe packets), but there is no application listening on it. They can be helpful in showing that a host is up on an IP address (host discovery, or ping scanning), and as part of OS detection. Because closed ports are reachable, it may be worth scanning later in case some open up. Administrators may want to consider blocking such ports with a firewall. Then they would appear in the filtered state, discussed next.*

**filtered**

*Nmap cannot determine whether the port is open because packet filtering prevents its probes from reaching the port. The filtering could be from a dedicated firewall device, router rules, or host-based firewall software. These ports frustrate attackers because they provide so little information. Sometimes they respond with ICMP error messages such as type 3 code 13 (destination unreachable: communication administratively prohibited), but filters that simply drop probes without responding are far more common. This forces Nmap to retry several times just in case the probe was dropped due to network congestion rather than filtering. This slows down the scan dramatically.*

**unfiltered**

*The unfiltered state means that a port is accessible, but Nmap is unable to determine whether it is open or closed. Only the ACK scan, which is used to map firewall rulesets, classifies ports into this state. Scanning unfiltered ports with other scan types such as Window scan, SYN scan, or FIN scan, may help resolve whether the port is open.*

**open|filtered**

*Nmap places ports in this state when it is unable to determine whether a port is open or filtered. This occurs for scan types in which open ports give no response. The lack of response could also mean that a packet filter dropped the probe or any response it elicited. So Nmap does not know for sure whether the port is open or being filtered. The UDP, IP protocol, FIN, NULL, and Xmas scans classify ports this way.*

**closed|filtered**

*This state is used when Nmap is unable to determine whether a port is closed or filtered. It is only used for the IP ID idle scan.*

Standard **TCP connect** scan is possible with `-sT`. Just type `nmap -sT IP_address`. This scan is popular for unprivileged users. The default Nmap scan is **TCP SYN** and you need to be root to use it. It does not finish 3 -way handshake like previous so it is bigger chance your scan will be not detected. Parameter for this one is `-sS`. For UDP scan use `-sU`.

To see differences you can run [Wireshark](https://www.wireshark.org/) and capture the traffic during both scans and compare results. You can also download some samples from [Wireshark Wiki](https://wiki.wireshark.org/SampleCaptures).

> [NMap Captures.zip](https://wiki.wireshark.org/uploads/__moin_import__/attachments/SampleCaptures/NMap-Captures.zip) (libpcap) Some captures of various NMap port scan techniques.

Now, most important thing is performance. Good scan should be targeted to live host (gathered during dicovery stage) with proper scan timing parameter and specified range of ports. Scanning all ports (65535) on many hosts can take ages and it is not useful at all.

By default Nmap scans 1000 ports. You can list ports using `-p22,80,443` or set port range `-p1-1023`. Parameter `-F` will force to scan only 100 most common ports. Option to scan all ports is `-p-` and `--top-ports 10` will check the ten most common ports. You can change value from 10 to 90 etc.

Scan timing can be set using `-T` with value from 0 to 5 where `-T0` is slowest and `-T5` is the fastest. Values are templates:

- paranoid (0)
- sneaky (1)
- polite (2)
- normal (3)
- aggressive (4)
- insane (5)

If you don’t want to be discovered you should use 0 or 1. Scan 0 check one port every 5 minutes. By default Nmap use `-T3`. Fastest is `-T5`, but it can loss some packets.

My suggestion is to use `-T4` when you are learning, testing something or doing CTFs. When you need to be like a ninja and more stealth use `-T1`.

Other solution is to use `--min-rate <number>` and `--max-rate <number>` to limit number of packets sent by Nmap.

Because of different response and port state you might want to give it a try and use one of additional port scan type like, TCP Null Scan, TCP Fin Scan, TCP Xmas Scan, TCP Maimon Scan, TCP ACK Scan, TCP Windows Scan, Custom TCP Scan, Spoofed Source IP, Spoofed MAC Address, Decoy Scan, Idle (Zombie) Scan or Fragmented IP data scan. That’s a lot :) I will not explain all of them, as they are very well described in [documentation](https://nmap.org/book/scan-methods.html#scan-methods-intro). These are just different methods of sending TCP packets which are not a part of ongoing connection with different sets of flags. I added some of them in cheat sheet section at the end of this article.

## Version, OS decetion and traceroute

Nmap if powerful tool and after port discovery, it can detect running services and versions. This is mostly what you are looking for during CTF or penetration test. Just add parameter `-sV` which will also force Nmap to proceed with the TCP 3-way handshake and establish the connection. You can also add `--version-intensity` with value from 0 to 9 or `all`. Information are mostly gathered by banner grabbing.

To enable OS detection add `-O`, it is based on open ports and running services.

Nmap offers two versions of the OS detection scan, ‘Guess’ and ‘Limit’.

The `--osscan-guess` provides a faster, more aggressive scan, which is useful when Nmap retrieves close to 100% OS detection. However, aggressive scanning may result in missing some ports.

```bash
sudo nmap -O --osscan-guess Target_IP
```

The `--osscan-limit` is an option used to limit what targets to scan. This option is useful when you have a large range of IPs to scan.

To get information about route between you and target use `--traceroute`

## Nmap Scripting Engine (NSE)

Default installation of Nmap contains a lot of ready to use scripts. You can check them in Nmap folder: `/usr/share/nmap/scripts`. Scripts are grouped by [categories](https://nmap.org/book/nse-usage.html#nse-categories). To run default scripts use `--script=default` or just `-sC`. Default category contains scripts from categories like: auth, broadcast, brute, default, discovery, dos, exploit, external, fuzzer, intrusive, malware, safe, version, and vuln. You can chose scripts `--script "SCRIPT-NAME"` if you want to run more for one category just run pattern like `--script "ftp*"`. You can write your own script or download other built by someone else, for example one popular at the moment is [NSE log4shell detection](https://github.com/Diverto/nse-log4shell).

## Output

Always document your work and save output of your scans. You can use 3 formats in Nmap.

### Normal

Use `-oN FILENAME` to save console output to the file.

### Grepable

Use `-oG FILENAME` to save in format that can be filtered by `grep` command.

### XML

Use `-oX FILENAME` to save output as XML file. Good to use as input to other programs.

Additionally if you will use `-oA FILENAME` output will be saved in all 3 formats.

## Nmap cheatsheet

Small summary of all Nmap command used in this article. Table with scan types.

| Scan type | Command |
| --- | --- |
| Discovery - ARP Scan | `sudo nmap -PR -sn Target_IP/24` |
| Discovery - ICMP Echo Scan | `sudo nmap -PE -sn Target_IP/24` |
| Discovery - ICMP Timestamp Scan | `sudo nmap -PP -sn Target_IP/24` |
| Discovery - ICMP Address Mask Scan | `sudo nmap -PM -sn Target_IP/24` |
| Discovery -TCP SYN Ping Scan | `sudo nmap -PS22,80,443 -sn Target_IP/30` |
| Discovery - TCP ACK Ping Scan | `sudo nmap -PA22,80,443 -sn Target_IP/30` |
| Discovery - UDP Ping Scan | `sudo nmap -PU53,161,162 -sn Target_IP/30` |
| Port Scan - TCP Connect Scan | `nmap -sT Target_IP` |
| Port Scan - TCP SYN Scan | `sudo nmap -sS Target_IP` |
| Port Scan - UDP Scan | `sudo nmap -sU Target_IP` |
| Port Scan - TCP Null Scan | `sudo nmap -sN Target_IP` |
| Port Scan - TCP FIN Scan | `sudo nmap -sF Target_IP` |
| Port Scan - TCP Xmas Scan | `sudo nmap -sX Target_IP` |
| Port Scan - TCP Maimon Scan | `sudo nmap -sM Target_IP` |
| Port Scan - TCP ACK Scan | `sudo nmap -sA Target_IP` |
| Port Scan - TCP Window Scan | `sudo nmap -sW Target_IP` |
| Port Scan - Custom TCP Scan | `sudo nmap --scanflags URGACKPSHRSTSYNFIN Target_IP` |
| Port Scan - Spoofed Source IP | `sudo nmap -S SPOOFED_IP Target_IP` |
| Port Scan - Spoofed MAC Address | `sudo nmap -sT --spoof-mac SPOOFED_MAC Target_IP` |
| Port Scan - Decoy Scan | `sudo nmap -D DECOY_IP,Target_IP` |
| Port Scan - Idle (Zombie) Scan | `sudo nmap -sI ZOMBIE_IP Target_IP` |
| Port Scan - Fragment IP data into 8 bytes | `-f` |
| Port Scan - Fragment IP data into 16 bytes | `-ff` |
| Port Scan - Service Detection | `sudo nmap -sV --version-light Target_IP` |
| Port Scan - OS Detection | `sudo nmap -sS -O Target_IP` |
| Port Scan - OS Detection Guess | `sudo nmap -O --osscan-guess Target_IP` |
| Port Scan - Traceroute | `sudo nmap -sS --traceroute Target_IP` |
| Port Scan - Default scripts | `sudo nmap -sS -sC Target_IP` |
| Port Scan - FTP Brute force scripts | `sudo nmap -sS -n --script "ftp-brute" Target_IP` |

Summary of all useful parameters, table with parameters.

| Option | Meaning |
| --- | --- |
| `-sn` | host discovery only |
| `-n` | no DNS lookup |
| `-R` | DNS lookup for all hosts |
| `-p-` | scan all ports |
| `-p1-1023` | port range, from 1 to 1023 |
| `-F` | top 100 most common ports |
| `-r` | scan ports in consecutive order |
| `-T<0-5>` | scan timing, T0 - slowest, T5 fastest |
| `--max-rate 20` | rate <= 20 packets/sec |
| `--min-rate 10` | rate >= 15 packets/sec |
| `-v` | verbose mode |
| `-vv` | very verbose mode |
| `-d` | debugging |
| `-dd` | detailed debugging |
| `--reason` | add more info from Nmap about decision it takes |
| `-sV` | version of service detected on open port |
| `-sV --version-light` | amount of version probes (2) |
| `-sV --version-all` | all available probes (9) |
| `-O` | detect OS |
| `--traceroute` | run traceroute to target |
| `--script=SCRIPTS` | Nmap scripts to run |
| `-sC` or `--script=default` | run default scripts |
| `-A` | equivalent to `-sV -O -sC --traceroute` |
| `-oN` | save output in normal format |
| `-oG` | save output in grepable format |
| `-oX` | save output in XML format |
| `-oA` | save output in normal, XML and Grepable formats |

Examples of use:

`sudo nmap -O -sV --version-intensity 5 --traceroute -oA /tmp/scan_output 192.168.1.1`

Build your own queries depends on what you want to achieve. Now scroll up to meme image at the beginning of this article, and read again query listed under it, funny right?

Here are mine used in last days:

| Type | Command |
| --- | --- |
| Bypassing Windows IPsec filter | `sudo nmap -sS -v -v -Pn -g 88 Target_IP` |
| TCP FIN Scan Avoid Firewall | `sudo nmap -sF -p1-100 -T4 Target_IP` |
| Specific port, open only, all hosts up | `sudo nmap -iL input_list -oG output_file -Pn --open -v` |
| MSRCP scan | `sudo nmap -sS -iL list.txt -p135,139,445,593 -v - oA output -T3 -g 88` |
| Standard quick scan | `sudo nmap -sV -O Target_IP -T4` |

Check also [Nmap Cookbook The fat-free guide to network scanning by Nicholas Marsh](Nmap-CookBook.pdf).
