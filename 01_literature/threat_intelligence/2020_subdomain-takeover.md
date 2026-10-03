[[ PAGE 1 ]]

# Subdomain takeover

A few years ago, taking over a subdomain was one of the easiest way to earn, several hundred dollars (sometimes thousands). It was a good salary for a beginner bounty hunter. Today, companies are more careful in this matter. Which does not mean that it is not worth trying. The rewards aren’t lower, but it is harder to spot this. You will need a lot of patience and time.

You do not need to be a super technical person and have some knowledge, to try your hand at this field. I will not go deep into the theoretical details, I will refer you to the pages where it has already been very well described and explained. Here we will focus on the search itself and the tools necessary to facilitate the search.

![subdomain takeover](subdomain-takeover.png)

*Image source: [Microsoft Docs](https://docs.microsoft.com/en-us/azure/security/fundamentals/subdomain-takeover)*

Remember if you get any hits on this and you will receive a reward, don’t forget to give me [10%](https://0ut3r.space/donations/) for showing you how to become a bounty hunter (just kidding you gotta give me all your winnings).

## Can I take over

First of all you need to know which services provider can be taken over. Here you can find up to date list of services with dangling DNS records.

<https://github.com/EdOverflow/can-i-take-over-xyz>

## Theory

If you want to know more than how to get money in easy way, check these links. These are good sources of knowledge about how it all works. Read and you will understand more. Don’t be like script kiddie.

[Subdomain Takeover: Basics](https://0xpatrik.com/subdomain-takeover-basics/)

[Subdomain Takeover: Going beyond CNAME](https://0xpatrik.com/subdomain-takeover-ns/)

[Subdomain Takeover: Proof Creation for Bug Bounties](https://0xpatrik.com/takeover-proofs/)

[Subdomain Takeover: Finding Candidates](https://0xpatrik.com/subdomain-takeover-candidates/)

[A guide to subdomain takeovers](https://www.hackerone.com/blog/Guide-Subdomain-Takeovers)

## Scope

Search for scope in bounty hunter programs like [Bugcrowd](https://www.bugcrowd.com/), [Hackerone](https://www.hackerone.com/), [Intigriti](https://www.intigriti.com/). There is many more of course. Find the one that best fits you.

## Enumeration

Once you have a scope. You need to prepare subdomain list. A few tools will help you with that.

I like [subfinder](https://github.com/projectdiscovery/subfinder) tool for enumeration and [knock](https://github.com/guelfoweb/knock) for wordlist. But here are all, still developed and very good tools. Test each and choose the best.

### Sublist3r

[Sublist3r](https://github.com/aboul3la/Sublist3r) is a python tool designed to enumerate subdomains of websites using OSINT. It helps penetration testers and bug hunters collect and gather subdomains for the domain they are targeting. Sublist3r enumerates subdomains using many search engines such as Google, Yahoo, Bing, Baidu and Ask. Sublist3r also enumerates subdomains using Netcraft, Virustotal, ThreatCrowd, DNSdumpster and ReverseDNS.

```bash
sublist3r -d example.com -t 50 -o subdomainlist.txt
```

### Subfinder

[subfinder](https://github.com/projectdiscovery/subfinder) is a subdomain discovery tool that discovers valid subdomains for websites by using passive online sources. It has a simple modular architecture and is optimized for speed. subfinder is built for doing one thing only - passive subdomain enumeration, and it does that very well.

After installation it is worth to add [API’s to your config file](https://github.com/projectdiscovery/subfinder#post-installation-instructions). This will increase your list building efficiency.

```bash
subfinder -d example.com -o subdomainlist.txt -t 50
```

This tool can check multiple domains from a file:

```bash
subfinder -dL domainlist.txt -o subdomainlist.txt -t 50
```

`-nW` - Remove Wildcard & Dead Subdomains from output

### knock

[Knockpy](https://github.com/guelfoweb/knock) is a python tool designed to enumerate subdomains on a target domain through a wordlist. It is designed to scan for DNS zone transfer and to try to bypass the wildcard DNS record automatically if it is enabled.

Subdomain scan with internal wordlist

```bash
knockpy example.com
```

Subdomain scan with external wordlist

```bash
knockpy example.com -w wordlist.txt
```

`-c` output to cvs

You can take interesting wordlist for subdomain enumeration from [dnscan repo](https://github.com/rbsec/dnscan) or [here](https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056).

### Set up script symlink

Sometimes, when you will install scripts/tools from GitHub, you need provide full path to run it. Easier solution is to add [symlink](https://en.wikipedia.org/wiki/Symbolic_link) to the script.

Example for Sublist3r installed from GitHub repository:

```bash
chmod +x sublist3r.py
cd /usr/local/bin/
sudo ln -s /opt/Sublist3r/sublist3r.py
mv sublist3r.py sublist3r
```

Now, no matter where you are in the system just write a command `sublister` to run the script.

You can do the same for other scripts/tools. That’s just small tip, you are pro and probably already knew it.

## Check if you can take over

Now it is time to check, if it is possible to takeover one of the subdomain from prepared list.

Never search manually. There is too much here to manually check one by one. It would be waste of time. Anyway below I showed for example how to do it manually using [dig](https://en.wikipedia.org/wiki/Dig_(command)).

### dig

You can use dig to manually check subdomain.

```bash
dig example.com
```

or list

```bash
dig -f subdomainlist.txt > dig.txt
```

Check then for status: NXDOMAIN and CNAME pointing to dangling DNS records.

### takeover

[Takeover](https://github.com/m4ll0k/takeover) - Subdomain Takeover Finder.

```bash
python3 takeover.py -l subdomainlist.txt -v -t 50 -o output.txt
python3 takeover.py -d example.com -v -t 50 -o output.txt
```

#### screen

Sometimes when you have a list with >10k entries it is worth to leave this on your VPS server as a session. Use screen for that.

```bash
screen -S your_session_name
```

New session will be opened, type there your command (eg. the one from **takeover** example) and then hit `ctrl+a+d` to keep your session in background.

You can now work on your VPS or run another session and not block your terminal, or just logoff. The process will still run in the background.

To check all your current session type `screen -ls`, to restore session type `screen -r your_session_name` or if you didn’t name your session, then session number provided on the session list. To kill session just enter to it, and type `exit`.

### sub404

[Sub 404](https://github.com/r3curs1v3-pr0xy/sub404) is a tool written in python which is used to check possibility of subdomain takeover vulnerability and it is fast as it is Asynchronous.

You can easily provide your subdomain list as a file:

```bash
python3 sub404.py -f subdomainlist.txt
```

or

```bash
python3 sub404.py -d example.com
```

this combines result from sublist3r and subfinder tool and checks for possibility of takeover.

This tool fetches CNAME of 404 response code URL and removes all URL which have target domain in CNAME. So chances of false positives are high.

### Recsech

[Recsech](https://github.com/radenvodka/Recsech) is a tool for doing Footprinting and Reconnaissance on the target web. Recsech collects information such as DNS Information, Sub Domains, HoneySpot Detected, Subdomain takeovers, Reconnaissance On Github and much more.

This tool is mentioned just as a bonus. One of its options is to check if a given domain has subdomains to take over, but it’s not a very efficient option.

```bash
Recsech.php example.com -o output.txt
```

## Takeover and PoC

So, if you are lucky one and you get hit, go and register your resource/service/bucket with the same name as the one you discovered. Redirect it to your www server with [PoC](https://en.wikipedia.org/wiki/Proof_of_concept) placeholder.

Here is example for **Traffic Manager**.

Create free subscription on [Azure](https://portal.azure.com/). Go to **Home**>**New**>**Traffic Manager profile**>**Create traffic manager profile**.

Create it with same name as the one from subdomain you want to take over. Once you put subdomain name, you will see if it is available to register.

> Name: subdomain  
> Routing method: Performance  
> Subscription: your_subscription  
> Resource group: Create new  
> Name: PoC  
> Resource group location: eg. East Europe

Now you need to point this domain to one of your servers. Just set IP address of your server as target. On the server, create virtual host with landing page.

In the links I provided in the **theory** part, you can find more useful information about how to set this up for Azure, GitHub, Heroku etc.

That’s all. Your PoC is ready to go. If you visit subdomain it will redirect you to your server.

Now prepare a good and detailed report and deliver it in bug bounty. [Check this report example](https://hackerone.com/reports/388622).

## How to protect your resources

Maintain order in your infrastructure ;)

[Check this guide from Microsoft](https://docs.microsoft.com/en-us/azure/security/fundamentals/subdomain-takeover), this link/document can be also used as solution for bug bounties reports.

Good luck. You will need it.

## Cheat sheet

I am really using it during my work.

One domain using Sublist3r

```bash
sublist3r -d example.com -t 50 -o subdomainlist.txt
```

One domain using Subfinder

```bash
subfinder -d example.com -t 50 -o subdomainlist.txt -timeout 5
```

List of domains using Subfinder

```bash
subfinder -dL domain-list.txt -t 50 -o subdomainlist.txt -timeout 5
```

Check if takeover is possible using takover

```bash
takeover -l subdomainlist.txt -v -t 10 -T 3 -o readyfortakeover.txt
```

Good solution for quick check all in one. Sub404 will merge results from Subliste3r and Subfinder, then it will look for domains available for takeover, parameter `-o` will give you merged results from Sublist3r and Subfinder.

```bash
python3 sub404.py -d example.com -o subdomains.txt
```

If you already have list of subdomains list you can also put it to sub404.

```bash
python3 sub404.py -f subdomainlist.txt
```
