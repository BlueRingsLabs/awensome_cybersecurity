---
id: ckb-d765a1a92757
title: Ransomware Investigation OSINT and Hunting Overview Pt1
category: threat-intelligence-and-osint
format: guide
language: en
tags: [blockchain, malware, osint, ransomware, threat-hunting, tls]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.62
---

RANSOMWARE
INVESTIGATION
(OSINT AND
HUNTING) –
OVERVIEW PT1
Joas Antonio
https://www.linkedin.com/in/
joas-antonio-dos-santos
What is Ransomware?
• Ransomware is malware that employs encryption to hold a
victim’s information at ransom. A user or organization’s
critical data is encrypted so that they cannot access files,
databases, or applications. A ransom is then demanded to
provide access. Ransomware is often designed to spread
across a network and target database and file servers, and
can thus quickly paralyze an entire organization. It is a
growing threat, generating billions of dollars in payments
to cybercriminals and inflicting significant damage and
expenses for businesses and governmental organizations.
Types of Ransomware
Types of Ransomware
1. Crypto ransomware
• The goal of crypto ransomware is to hack and encrypt the sensitive files located on
the victim’s computer, such as documents, pictures, or videos. While cybercriminals
withhold access to these files, they don’t go as far as interfering with basic
computer functions like other types of ransomware. Hackers want to create a sense
of panic within the user by allowing them to see their files without the ability to
open their information.
2. Locker ransomware
• Locker ransomware is unique in that it solely aims to lock victims out of their
computers. Hackers do this by disabling all basic computer functions with an
exception for minor mouse and keyboard capabilities. Leaving the mouse and
keyboard somewhat operable lets the user fulfill the demands of the cybercriminal
to gain access back into their device.
• A common trend with locker ransomware is that it generally doesn’t target specific
files. So, the likelihood of data destruction is lower compared to other types of
ransomware attacks. However, there are no guarantees when dealing with
cybercriminal masterminds.
Types of Ransomware
3. Scareware
• Scareware is a malicious software created to make false claims about viruses infecting a
user's computer or device. A payment is typically requested from the owner to solve the
falsified issues. While some types of scareware can lock a user out of their device, others will
only go as far as flooding the screen with countless pop-ups to overwhelm the user.
4. Ransomware as a Service (RaaS)
• Ransomware as a Service (RaaS) is a dark web business model created to help ransomware
hackers streamline their attacks. Developers created this software to automatically carry out
all aspects of a ransomware attack for the cyberthief, from sending out the ransomware to
collecting payments and restoring user access.
5. Doxware or leakware
• Doxware, also known as leakware, threatens the distribution of sensitive data online,
targeting people and businesses alike. Since hackers know people, and especially
businesses, will do almost anything to prevent confidential and personal data from falling
into the wrong hands, they often demand compensation to prevent its release.
Ransomware Report
Ransomware in 2022
https://www.blackfog.com/the-state-of-ransomware-in-2022/
https://therecord.media/ransomware-tracker-the-latest-
figures/
https://www.trendmicro.com/vinfo/us/security/news/ransom
ware-by-the-numbers/lockbit-conti-and-blackcat-lead-pack-
amid-rise-in-active-raas-and-extortion-groups-ransomware-
in-q1-2022
Commons Ransomware
• Cerber
• Bad Rabbit
• CryptoWall
• Crysis
• LockerGoga
• LeChiffre
• Petya
• NotPetya
• KeRanger
• Jigsaw
• GoldenEye
• CTB-Locker
• Maze
• Locky
• WannaCry
• ZCryptor
• TorrentLocker
• TeslaCrypt
• Spider
• Ryuk
INVESTIGATION
RANSOMWARE
APT Groups
• Groups are sets of related intrusion activity that are tracked
by a common name in the security community. Analysts
track clusters of activities using various analytic
methodologies and terms such as threat groups, activity
groups, threat actors, intrusion sets, and campaigns. Some
groups have multiple names associated with similar
activities due to various organizations tracking similar
activities by different names. Organizations' group
definitions may partially overlap with groups designated by
other organizations and may disagree on specific activity.
APT Groups – List and Report
• https://attack.mitre.org/groups/
• https://www.mandiant.com/resources/insights/apt-groups
• https://cybersophia.net/cyber-threat-intel/advanced-
persistent-threat-apt-groups/
• https://adversary.crowdstrike.com/en-US/?L=32
• https://www.crowdstrike.com/resources/reports/global-
threat-report/
RANSOMWARE INCIDENT RESPONSE
Ransomware Process
Ransomware Attack and Recovery
OSINT – What is?
• By gathering publicly available sources of information about a particular
target an attacker – or friendly penetration tester – can profile a potential
victim to better understand its characteristics and to narrow down the
search area for possible vulnerabilities. Without actively engaging the
target, the attacker can use the intelligence produced to build a threat model
and develop a plan of attack. Targeted cyber attacks, like military attacks,
begin with reconnaissance, and the first stage of digital reconnaissance is
passively acquiring intelligence without alerting the target.
• Gathering OSINT on yourself or your business is also a great way to
understand what information you are gifting potential attackers. Once you
are aware of what kind of intel can be gathered about you from public
sources, you can use this to help you or your security team develop better
defensive strategies. What vulnerabilities does your public information
expose? What can an attacker learn that they might leverage in a social
engineering or phishing attack?
OSINT Framework – What is?
• Gathering information from a vast range of sources is a time
consuming job, but there are many tools to make intelligence
gathering simpler. While you may have heard of tools like
Shodan and port scanners like Nmap and Zenmap, the full range
of tools is vast. Fortunately, security researchers themselves
have begun to document the tools available.
• A great place to start is the OSINT Framework put together by
Justin Nordine. The framework provides links to a large
collection of resources for a huge variety of tasks from
harvesting email addresses to searching social media or the
dark web.
Malware Database
• https://github.com/Endermanch/MalwareDatabase
• https://github.com/Pyran1/MalwareDatabase
• https://github.com/acastillorobles77/MalwareDatabase
• https://github.com/sophos/SOREL-20M
• https://virusshare.com/
• https://labs.inquest.net/
• https://bazaar.abuse.ch/
• https://www.hybrid-analysis.com/
• https://urlhaus.abuse.ch/
• https://beta.virusbay.io/
• https://www.virustotal.com/
Malware Samples
• https://github.com/jstrosch/malware-samples
• https://github.com/fabrimagic72/malware-samples
• https://github.com/ytisf/theZoo
• https://github.com/mstfknn/malware-sample-library
Create Lab
• Install Windows 7 and 10
• Install Linux or preference Kali Linux
• https://www.sentinelone.com/labs/building-a-custom-
malware-analysis-lab-environment/
• https://www.youtube.com/watch?v=GE_aSVq8ZnQ
• https://www.youtube.com/watch?v=fLJifLf_fRE
• https://www.youtube.com/watch?v=bBvOiADXjEQ
OSINT – Maltegoce Transforms
•
Intezer Analyze Transforms for
Maltego;
•
Abuse.ch URLhaus;
•
AbuseIPDB;
•
ATII Hades Darkweb;
•
Virus Total Premium;
•
Cybersixgill;
•
Att&ck MISP;
•
Threat Crowd;
•
Shodan;
•
Crowdstrike Intel;
•
Recorded Future;
•
Hyas insight;
•
Flashpoint;
•
Hybrid Analysis;
•
Threat Miner;
•
Blockchain.info
•
Cipher Trace;
•
Tatum Blockchain;
OSINT – Maltegoce Cryptocurrency 1
Blockchain.com (formerly Blockchain.info
) is a provider of cryptocurrency
blockchain explorer services. It’s a
platform that offers ways to buy, hold,
and use cryptocurrency. It creates a
financial system for the internet that
empowers anyone in the world to control
their money. Over 50+ million customers
have signed up to use the
Blockchain.com platform. It’s a fast and
easy way to buy bitcoin, trade crypto,
send, receive, secure, and borrow digital
currencies.
OSINT – Maltegoce Cryptocurrency 2
https://sociallinks.io/we
binars/analysing-
cryptocurrencies-and-
investigating-
blockchains
https://www.youtube.c
om/watch?v=A7XhEvA
gYz4
https://alphasec.io/how
-to-visualize-ethereum-
transactions-using-
maltego/
Model for the
Money laudering
of Ransomware
•
Anonymity: Bitcoin provides anonymity when payments are
received and when they are cashed out. That's because
bitcoin accounts and money transfers are difficult to trace
and depend largely on the cybercriminal being sloppy with
operations security.
•
Global Currency: Hackers typically prey on out-of-country
targets and need a fast, untraceable method to transfer
funds across nations without worrying about account
freezes. Bitcoin is used as a global currency because you
don't need to worry about the exchange rates between your
home country's currency and US dollars.
•
Ease of Payments: In the past, hackers used to rely on gift
cards for payment. This was troublesome on many levels —
for instance, gift cards can't be used globally, and criminals
needed to come up with a mailing addresses that can't be
traced. Bitcoin and the higher profile of cryptocurrency have
contributed to the rise in ransomware, as well as hackers'
ability to use extortion to elicit payments. One example
occurred after the Ashley Madison website breach, when
hackers threatened some users with a bitcoin ransom or
have their identities revealed as adulterers. Another tactic
involved using malicious emails to threaten a distributed
denial-of-service attack on an organization's network unless
a bitcoin payment was made.
Analyzing Wallet Addresses using
Blockchain Explorers
• In cryptocurrency investigations, blockchain ledgers play a significant role. To render it simpler to comprehend and make sense of the information, investigators use Wallet
explorers to conduct analysis on wallet addresses and transactions.
• Transaction analysis is crucial in cryptocurrency investigations since it not merely permits investigators to follow the money, but also determine the source and what sort of
tools the suspect employed
• One of the more known Explorers is Blockchain.com. It allows us to look up the wallet address and see all of its past transactions. It also shows how much currency it currently
holds. Blockchain transactions are simple to track in the case of public ledgers like Bitcoin or Ethereum.
• WalletExplorer
• BitcoinWho’sWho
• BitcoinAbuse
• IntelX
Wallet explorers usually update in real-time with the details of each transaction, comprising of:
• Hash: The transaction ID which serves as a way to look up a particular transaction on the blockchain. (Not to be confused with Cryptographic Hashes)
• From/To: The sender’s address and the recipient’s address.
• Time Stamp: Each block includes the precise time for when the transaction entered the blockchain. Thus, the time the block was mined.
• Actual Cost/Fee: The price of the transaction.
• Transaction Receipt Status: Confirmation of the transaction’s status.
• Value: How much cryptocurrency was sent and the equivalent USD value.
IoCs Ransomware
• Indicators of compromise (IoCs) are clues and evidence of a data breach in the form of digital breadcrumbs.
These indicators can tell us whether a cyberattack has occurred, who was behind them and what tools may
have been used. This information is generally obtained from software, including anti-malware and antivirus
systems.
• Some of the most common IoCs to watch for are:
1.
Unusual traffic patterns between internal systems
2.
Unusual usage patterns for privileged accounts
3.
Administrative access to your network from unsuspected geographical locations
4.
A spike in database read volumes
5.
A high rate of authentication attempts and failures
6.
Unusual configuration changes
7.
C2 Servers Ips
8.
Ethereum or Bitcoin Wallets
9.
Hashes File
https://www.packetlabs.net/posts/indicators-of-compromise-ioc/
Example IoCS Ransomwar: https://github.com/sophoslabs/IoCs/blob/master/Ransomware-Ryuk.csv
Wallet trace transactions
Visual tools are beneficial when investigating addresses and transactions. Using Coinpath®
technology, anyone can build visual tools to understand the money flow. We have built one on our
Bitquery explorer. You can visualize all the incoming and outgoing transactions from the hacker’s
address here.
Today, bitcoin blockchain confirms ~10 million transactions every month. All these transactions are
visible on the bitcoin blockchain. However, the blockchain only store addresses, public keys, and not
real-world identities. Therefore, Virtual asset service providers (VASP) are the primary way to link
real-world identities with bitcoin transactions. For example, VASPs such as Exchanges, wallets,
custodians provide cryptocurrency services to retail users and businesses. Most of these services
implement KYC (Know-your-customer) solutions. Therefore, linking real-world identity with bitcoin
addresses and transactions.
SIEM Splunk Investigation
https://www.splunk.com/en_us/blog/industries/detecti
ng-ransomware-attacks-with-splunk.html
Capturing Windows Memory Using
Winpmem
• Winpmem is a part of the Pmem Suite, a suite of memory acquisition tools for
Windows, Linux, and Mac OS. You can download the latest release of winpmem
from here: https://github.com/Velocidex/c-aff4/releases.
• Run Winpmem
• First, after I staged my malicious activity, I downloaded winpmem 3.3 RC3 onto the
victim Windows machine. From there, I opened a command-line terminal and
executed the program:
• C:\ winpmem_v3.3.rc3.exe --output memdump.raw --format raw --volume_
• The --output mem.raw option was used to name the output as memdump.raw. The
--format raw and --volume_format raw options were used to output the memory in
raw format (as opposed to something like aff4). After several minutes, the memory
dump finished. I then transferred the raw memory file, memdump.raw, to my Kali
machine.
• https://blog.cyberhacktics.com/memory-forensics-on-windows-10-with-volatility/
• https://github.com/Velocidex/c-aff4/releases
Volatility Ransomware
• Identifying Malicious Processes (python3 vol.py -f <filename> pslist)
• Below are the keys headers from ‘pslist’ that you will need to understand
when you begin using the tool:
• PID - Process ID number
• PPID - Parent process ID number
• ImageFileName - Name of the running process
• Offset - Hexadecimal value representing the location in memory the process is
running
• CreateTime - Time process started
• ExitTime - Time process ended
https://book.hacktricks.xyz/generic-methodologies-and-resources/basic-forensic-
methodology/memory-dump-analysis/volatility-examples#installation
https://github.com/volatilityfoundation/volatility/wiki/
Volatility
Ransomware 2
• Using ‘pstree’ is a great way to spot
these malicious processes
masquerading as legitimate Windows
processes. (python3 vol.py -f
<filename> pstree)
Volatility
Ransomware 3
• To view the network connections
associated with the RAM dump that is
being analyzed use the following
command: (python3 vol.py -f
<filename> netscan)
•
Offset - Location in memory
•
Proto - Network protocol used by process
•
LocalAddr - Source address of network
connection
•
LocalPort - Source port of network
connection
•
ForeignAddr - Destination address of
network connection
•
ForeignPort - Destination address of network
connection
•
State - State of network connection i.e.
established, closed or listening
•
PID - Process ID of associated process
•
Owner - Account associated with process
•
Created - Time network connection has
initiated
https://exchange.xforce.ibmcloud.com/
http://sitereview.symantec.com/#/
Volatility
Ransomware 4
• Using the commands covered in this
article should put you in a good
position to start identifying potential
malware running in memory on a
device. Using ‘netscan’ I was able to
identify a process named
‘smsfwder.exe’ that was making some
malicious network connections to
known C2 infrastructure. As part of my
investigation using Volatility, I can
extract this process for further analysis
using a feature called ‘procdump’.
• python3 vol.py -f <filename> -o <Directory
to dump process> dumpfiles –pid <PID>
Volatility
Ransomware 5
• To dump a process's executable, use
the procdump command. Optionally,
pass the --unsafe or -u flags to bypass
certain sanity checks used when
parsing the PE header. Some malware
will intentionally forge size fields in the
PE header so that memory dumping
tools fail.
• python3 vol.py -f memory.dmp --
profile=Win7SP1x64 procdump --dump-
dir=OUTDIR/
• Upload executable in virus total for
analyze
Essential Critical
Infrastructure
Workers
• It's perfect moment to remind about
MITRE ATTACK for ICS, it describes
every step of attack on SCADA/ICS
devices.
• https://collaborate.mitre.org/attackics
/index.php/Initial_Access
• https://www.offensiveosint.io/offensi
ve-osint-s01e03-intelligence-
gathering-on-critical-infrastructure-
in-southeast-asia/
Geolocation
IP
• A Geolocation OSINT Tool. Offers
geolocation information gathering
through social networking
platforms.
• https://www.geocreepy.com/
• MaxMind is one of the leading
providers of IP intelligence and
online fraud detection tools.
MaxMind provides IP intelligence
through their GeoIP brand. Over
5,000 companies use GeoIP data to
locate their internet visitors and
show them relevant content and
ads, enforce digital rights, and
efficiently route internet traffic.
Businesses can obtain additional
insights into their customers'
connection speeds, ISPs, and more
using GeoIP data.
• https://www.maltego.com/transform
-hub/maxmind/
• https://github.com/libresec/geo-ip-
maltego
Dark Web Investigation
•
Ahmia – one of the oldest and most reliable .onion search engines, accessible both from the darknet and the clearnet.
•
Onion Search Engine – for searching onion sites. It comes with browser extensions for Chrome and Firefox. Various
supported search options include images, videos, maps and pastes.
•
Tor Taxi – a launchpad website with links to multiple different onion domains. It has a handy colour-coded system for
displaying websites that are currently down.
•
Darkweb Wiki – a somewhat chaotic and not frequently updated list of onion sites – still, a valuable resource.
•
Hunchly – provides daily darkweb reports of what onion domains are up / down, in the form of a spreadsheet.
•
IACA Darkweb Tools – free resources provided by the International Anti Crime Academy.
•
Reddit communities – many subreddits dedicated to various aspects of the darkweb can be found, some of which are
hit and miss. However, there are 3 that are consistently good and up to date:
•
https://www.reddit.com/r/darknet/
•
https://www.reddit.com/r/TOR/
•
https://www.reddit.com/r/onions/
•
Discord – an up-and-coming alternative to Reddit for budding online communities and niche topics, Discord already
dominates in some aspects. While I have not yet found a publicly available channel worthy of a recommendation, you
can darknet-keyword search the available Discord servers.
Dark Web Investigation 2
• Ahmia – as mentioned above, but specifically for Tor:
• http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion
• Haystak – the self appointed “darknet’s largest search engine”, with thousands of
indexed .onion domains – including some historical ones.
• http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/
• Kilos – darknet market search engine allowing to search for vendors, listings,
reviews, forums and forum posts. Useful for conducting broad keyword-based
searches across multiple darkweb entities.
• http://mlyusr6htlxsyc7t2f4z53wdxh3win7q3qpxcrbam6jf3dmua7tnzuyd.onion/se
arch
• TOR66 – on top of the standard search, this enables the “fresh onions” and
“random onions” matches; tread with caution, these can bring you to some truly
random sites.
• http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion/
Dark Web Investigation 3
• First and foremost, awesome list of tools by Apurv Singh Gautam is
available here (but just a caveat, I have not used or tested all of
those – yet).
• Onioff – a Python tool for searching .onion URLs.
• Onion Ingestor – for scraping and collecting darkweb intelligence –
works with Kibana dashboards.
• Onion Search – tool for scraping .onion URLs from darkweb search
engines.
• The Devils Eye – for extracting .onion site links and descriptions
without connecting to Tor.
• TorBot – onion crawler, with many additional features still in active
development.
Dark Web Investigation 4
• AuCyble
• DarkDotFail
• darktracer_int
• darkowlcyber
• ido_cohen2
• josephfcox
• RansomAlert
• Torproject
Emails Analyzer
• Whenever an email is sent, information is transmitted with that
email and the route the email takes across a network is
recorded. This information is known as the  ‘Extended Header’.
• The extended header can be of great use to the researcher and
when used correctly, provides an insight into the sender, their
software and hardware and potential recipients.
• The extended header information potentially includes the
senders IP address, email client, return address and the route
the email has taken to reach its destination. This is useful in
identifying and investigating ‘spoof’ or ‘phishing’ emails.
Emails Analyzer - Tools
• Google Hacking;
site:organisation.com intext:@organisation.com
site:bbc.co.uk intext:@bbc.co.uk
intext:”boris.johnson.mp@parliament.uk” filetype:pdf
• Sherlock;
Emails Analyzer – Tools 2
• Pastebin;
• Have I been pwned?
• Emailrep.io;
• Hunter.io;
• Whitepages;
• Twitter;
• Mxtoolbox;
• Spiderfoot;
• ProtOsint;
• https://github.com/bitsofinfo/comms-analyzer-toolbox
Threat Intelligence Platform
• MISP;
• OpenCTI;
• IBM X-Force Exchange;
• ManageEngine;
• Anomali ThreatStream;
• LogRhytm TLM;
• Mandiant Threat Suite;
• Recorded Future;
• Virus Total Intelligence;
• Shodan;
Shodan Malware Hunter
• https://malware-hunter.shodan.io/
• Malware Hunter is a specialized Shodan crawler that
explores the Internet looking for command & control (C2s)
servers for botnets. It does this by pretending to be an
infected client that's reporting back to a C2. Since we don't
know where the C2s are located the crawler effectively
reports back to every IP on the Internet as if the target IP is
a C2. If the crawler gets a positive response from the IP
then we know that it's a C2.
Shodan
OSINT
• Shodan is a search engine that lets the
user find specific types of computers
(webcams, routers, servers, etc.)
connected to the internet using a
variety of filters. Some have also
described it as a search engine of
service banners, which are metadata
that the server sends back to the client.
This can be information about the
server software, what options the
service supports, a welcome message
or anything else that the client can find
out before interacting with the server.
Shodan
OSINT 2
• To select a specific country type:
country: <Country Symbol>
• To select specific ports type: port:
<Ports_HERE>
• To search for a specifit operating
system(OS) type: os: <OS_HERE>
https://www.blueteamsacademy.com/s
hodan/
Using Maltego to Identify and Investigate
on C2 Malware in Your Network
• Maltego has a number of data integrations especially helpful for
cybersecurity professionals and threat hunters seeking to identify hidden
threats in the organization’s network and trace the origin of said threats. In
this tutorial, we will demonstrate how you can use Transforms from
ATT&CK - MISP, VirusTotal Public API, and ZETAlytics Massive Passive to
acquire threat intel, find hashes related to certain domains and IPs, and
uncover threat actor network.
• Step 1: Identify Whether Hashes are False Alerts
• Step 2: Find Out Relevant IP Addresses using MISP Transforms
• Step 3: Investigate on Suspicious IP Addresses using ZETAlytics Transforms
• Step 4: Identify How the Malware Entered the Company Network
• Step 5: Deep-Dive into Malicious Domains to Find the Source of Malware
Entry
https://www.maltego.com/blog/identify-c2-malware-and-phishing-threats-
with-maltego/
Ransomware Playbook
https://github.com/counteractive/incident-response-plan-
template/blob/master/playbooks/playbook-ransomware.md
References
• https://www.trellix.com/en-us/security-awareness/ransomware/what-
is-ransomware.html
• https://us.norton.com/internetsecurity-malware-types-of-
ransomware.html
• https://h11dfs.com/9-step-ransomware-incident-response-plan/
• https://dxc.com/us/en/insights/perspectives/paper/ransomware-
survival-guide---recover-from-an-attack-
• https://www.sentinelone.com/cybersecurity-101/open-source-
intelligence-osint/
• https://www.researchgate.net/figure/Model-for-the-money-laundering-
of-ransomware-and-cryptoware-profits-via-bitcoins_fig2_343009039
• https://bitquery.io/blog/trace-bitcoin-transaction-and-address
• https://www.secjuice.com/osint-daily-dose-of-malware/
