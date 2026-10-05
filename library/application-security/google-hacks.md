---
id: ckb-083a949cfac4
title: Google Hacks
category: application-security
format: article
language: en
tags: [databases, git, macos, osint, tls, web-security]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.43
---

# Google Hacks

The term “[Google Hacking](https://en.wikipedia.org/wiki/Google_hacking)“ certainly does not mean hacking Google company. It means that you can do specially selected queries for the popular Google search engine, which allow you to find information useful for analyzing the security of other websites. With the help of these queries, you will find e.g. vulnerable pages, holes in the code, server and script version, data that should not be published, passwords, databases, etc.

[Google Hacks](https://en.wikipedia.org/wiki/Google_Hacks) is also called Google Dorks.

![Google Hacking](googlehacking.png)

All you need is web browser, access to [Google Web Search](https://www.google.com/) and Google Dorks. There is a nice and big list of popular and fresh Google Dorks called [Google Hacking Database](https://www.exploit-db.com/google-hacking-database).

## Examples

Below I share with you some of the interesting Google Dorks I used in the past (one Google Dork per line):

```plaintext
allintext: “Pixie Powered”
“script_filename” “HTTP Headers Information” “allow_url_fopen” ext:php
intitle:”Index of” “/ .WNCRY”
inurl:/help/readme.nsf intitle:”release notes” intitle:domino
“Apache Server Status for” “Server Version” -“How to” -Guide -Tuning
inurl:”/web.config” ext:config
inurl:logs/gravityforms
“not for public release” filetype:pdf
“pcANYWHERE EXPRESS Java Client”
wwwboard WebAdmin inurl:passwd.txt wwwboard|webadmin
filetype:pem “PRIVATE KEY”
inurl:/t/ (portal OR intranet OR login)
intitle:”index of” “places.sqlite” “key3.db” -mozilla.org
inurl:”?db_backup” | inurl:”dbbackup” -site:http://github.com  “sql.gz” | “sql.tgz” | “sql.tar” | “sql.7z”
inurl:.php? intext:CHARACTER_SETS,COLLATIONS intitle:”phpmyadmin”
intitle:”=[ 1n73ct10n privat shell ]=”
filetype:rdp password
filetype:sh inurl:cgi-bin
allinurl:index.php?db=information_schema
inurl:index.rb
ext:json OR inurl:format=json
inurl:”server-status” intitle:”Apache Status” intext:”Apache Server Status for”
inurl:”.s3.amazonaws.com/”
site:http://s3.amazonaws.com  intitle:index.of.bucket
site:http://blob.core.windows.net 
site:* inurl:/user/register
intext:”There isn’t a Github Pages site here”
intitle:”Site not found · GitHub Pages”
inurl:%26 inurl:%3D
inurl:& inurl:%3D
intitle:”Dashboard [Hudson]”
intitle:”Dashboard [Jenkins]” intext:”Manage Jenkins”
“or greater is required”+”You have no flash plugin installed”
site:target.com filetype:”xls | xlsx | doc | docx | ppt | pptx | pdf”
```

Copy and paste each of them to Google Search and check the result. Interesting right? So, how it works?

## Search Operators

As you can see there is a lot of operators you can use in search, to narrow your search results to the most interesting ones. Here is the list with some examples. Read it and create some search queries combining several of them.

**OR** - Search for X or Y. Examples: jobs **OR** gates / jobs **|** gates

**AND** - Search for X and Y. Example: jobs **AND** gates

**-** - Exclude a term or phrase. Example: jobs **-**apple

***** - Acts as a wildcard and will match any word or phrase. Example: steve ***** apple

**( )** - Group multiple terms or search operators to control how the search is executed. Example: **(**ipad OR iphone**)** apple

**$** - Search for prices. Example: ipad **$**329

**define:** - A dictionary built into Google, basically. This will display the meaning of a word in a card-like result in the SERPs. Example: **define:**entrepreneur

**cache:** - Returns the most recent cached version of a web page. Example: **cache:**apple.com

**filetype:** - Restrict results to those of a certain filetype. E.g., PDF, DOCX, TXT, PPT, etc. Example: apple **filetype:pdf** / apple **ext:**pdf

**site:** - Limit results to those from a specific website. Example: **site:**apple.com

**related:** - Find sites related to a given domain. Example: **related:**apple.com

**intitle:** - Find pages with a certain word (or words) in the title. Example: **intitle:**apple

**allintitle:** - Similar to “intitle,” but only results containing all of the specified words in the title tag will be returned. Example: **allintitle:**apple iphone

**inurl:** - Find pages with a certain word (or words) in the URL. Example: **inurl:**apple

**allinurl:** - Similar to “**inurl**,” but only results containing all of the specified words in the URL will be returned. Example: **allinurl:**apple iphone

**intext:** - Find pages containing a certain word (or words) somewhere in the content. Example: **intext:**apple

**allintext:** - Similar to “**intext**,” but only results containing all of the specified words somewhere on the page will be returned. Example: **allintext:**apple iphone

**AROUND(X)** - Proximity search. Find pages containing two words or phrases within **X** words of each other. For this example, the words “apple” and “iphone” must be present in the content and no further than four **words** apart. Example: apple **AROUND(4)** iphone

**weather:** - Find the weather for a specific location. This is displayed in a weather snippet, but it also returns results from other “weather” websites. Example: **weather:**san francisco

**stocks:** - See stock information (i.e., price, etc.) for a specific ticker. Example: **stocks:**aapl
**map:** - Force Google to show map results for a locational search. Example: **map:**silicon valley

**movie:** - Find information about a specific movie. Also finds movie showtimes if the movie is currently showing near you. Example: **movie:**steve jobs

**in** - Convert one unit to another. Works with currencies, weights, temperatures, etc. Example: $329 **in** GBP

**source:** - Find news results from a certain source in Google News. Example: apple **source:t**he_verge
**_** - Acts as a wildcard for Google Autocomplete. Example: apple CEO **_** jobs

## Automation

During various types of search, it is useful to automate this process. Here are some interesting programs/scripts that will help you to run search using Google Dorks.

I am using these on [Kali Linux](https://www.kali.org/), but they will work on most Linux distributions. [Especially on distros for hackers](https://0ut3r.space/2020/02/29/linux-distros-for-hackers/).

### Katana

Katana-ds (ds for dork_scanner) is a simple python tool that automates Google Hacking/Dorking and support Tor. It becomes a more powerful in combination with [GHDB](https://www.exploit-db.com/google-hacking-database).

This tool search for websites automatically.

```bash
python3 kds.py -h (for help)
Options :
-g :for google mode
-s :for scada mode
-t :for tor mode
-p :for proxy mode
```

[Scada](https://en.wikipedia.org/wiki/SCADA) mode gives interesting results and it is awesome function.

**GitHub**: <https://github.com/adnane-X-tebbaa/Katana>

### uDork

uDork is a script written in Bash Scripting that uses advanced Google search techniques to obtain sensitive information in files or directories, find IoT devices, detect versions of web applications, and so on. uDork does NOT make attacks against any server, it only uses predefined dorks and/or official lists from exploit-db.com [GHDB](https://www.exploit-db.com/google-hacking-database).

```bash
./uDork.sh <Domain/IP> [option] <string> / all

======================== OPCIONES ========================
 -e <extensión> / <all> : Search files by extension. Use all to find the list extension.
 -s <text> / <all> : Find text in website content.
 -u <string> / <all> : Locate text strings within the URL.
 -t <string> / <all> : Lists text string in site title.
 -g <dork_name> : Attack a site with a predefined list of dorks. Review list <-l>. 
 -l : Shows the list of predefined dorks (Exploit-DB).
 -f <custom_list> : Use your own personalized list of dorks.
 -p <number> : Number of pages to search in Google. (By default 1 pages).
 -o <name_file> : Export results to a file.

======================== EXAMPLES ========================
 ./uDork.sh host.com -e pdf -p 3 (Search for .pdf files on the indicated website)
 ./uDork.sh host.com -e all (Search files by all extensions)
 ./uDork.sh host.com -t "Twitter David" (Find errors by the indicated chain)
 ./uDork.sh host.com -u all (Find the most used chains)
 ./uDork.sh host.com -g admin (Lists administration panels)

 -h : Show this help.
```

This tool allows you to define specific domain/IP address.

**GitHub**: <https://github.com/m3n0sd0n4ld/uDork>

### XSS-LOADER

All in one tools for XSS payload generator, XSS Scanner and also XSS Dork Finder.

This tool creates payload for use in xss injection, select default payload tags from parameter or write your payload. It makes xss inj. with Xss Scanner parameter and it finds vulnerable sites url with **Xss Dork Finder** parameter.

```bash
hoek@bughunter:/opt/XSS-LOADER$ python3 payloader.py 
             ╭━╮╭━┳━━━┳━━━╮╱╱╭╮╱╱╭━━━┳━━━┳━━━┳━━━┳━━━╮                               
             ╰╮╰╯╭┫╭━╮┃╭━╮┃╱╱┃┃╱╱┃╭━╮┃╭━╮┣╮╭╮┃╭━━┫╭━╮┃                               
             ╱╰╮╭╯┃╰━━┫╰━━╮╱╱┃┃╱╱┃┃╱┃┃┃╱┃┃┃┃┃┃╰━━┫╰━╯┃                               
             ╱╭╯╰╮╰━━╮┣━━╮┣━━┫┃╱╭┫┃╱┃┃╰━╯┃┃┃┃┃╭━━┫╭╮╭╯                               
             ╭╯╭╮╰┫╰━╯┃╰━╯┣━━┫╰━╯┃╰━╯┃╭━╮┣╯╰╯┃╰━━┫┃┃╰╮                               
             ╰━╯╰━┻━━━┻━━━╯╱╱╰━━━┻━━━┻╯╱╰┻━━━┻━━━┻╯╰━╯                               
        |||||||||||||||||||||||||||||||||||||||||||||||||||||                        
        ||                 XSS-LOADER TOOL                 ||                        
        ||               INSTAGRAM==>TMRSWRR               ||                        
        ||             CODED BY HULYA  KARABAG             ||                        
        |||||||||||||||||||||||||||||||||||||||||||||||||||||                        
        ||              WELCOME TO XSS-LOADER              ||                        
        |||||||||||||||||||||||||||||||||||||||||||||||||||||                        
                                                                                     
-----------------------------------                                                  
 |||      XSS-LOADER TOOLS      |||                                                  
-----------------------------------                                                  
1)  BASIC PAYLOAD                                                                    
2)  DIV PAYLOAD                                                                      
3)  IMG PAYLOAD                                                                      
4)  BODY PAYLOAD                                                                     
5)  SVG PAYLOAD                                                                      
6)  ENTER YOUR PAYLOAD                                                               
7)  XSS SCANNER                                                                      
8)  XSS DORK FINDER                                                                  
9)  EXIT                                                                             

SELECT PAYLOAD TO TAG:8                                                              
e.g---->inurl:"search.php?q="                                                                                                                            
Please enter your dork:
```

Enter your dork and check results.

**GitHub**: <https://github.com/capture0x/XSS-LOADER>

## Epilog

The use of Google Dorks is completely legal and not prohibited. The question is what you will do with the results you get. Everything that Google indexes becomes public, but in the case of private data it is mostly developer or user error. Perform your searches/scans with the use of a proxy or VPN. Don’t act to harm others. Use the finds to earn money as a bounty hunter.

If you know any interesting programs or scripts that you use, I’ll be happy to hear what.

Happy hacking.
