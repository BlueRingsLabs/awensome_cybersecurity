---
id: ckb-231a0d73109a
title: Fuzz the world
category: offensive-security
format: article
language: en
tags: [burp-suite, fuzzing, sql-injection, vulnerability-management, web-security]
summary: This article provides an introductory overview of fuzzing techniques, explaining the concept of automated input testing to identify vulnerabilities in applications and network protocols.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.95
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:01:58Z
---

# Fuzz the world

At the beginning of my pentesting journey, I was not quite sure what fuzzing was. Even though I used it all the time.

Being an amateur guitarist myself, fuzz to me was just a guitar effect that sounded like overdrive, but broken, like the amp had broken down and something was whining. As I didn’t have many colleagues, and still don’t, no one was able to explain to me in simple terms what fuzzing was. Nowadays, this is not a problem because you can type a phrase into Google and get thousands of answers and interpretations. But when I was studying in the days just after the extinction of the dinosaurs… in fact, when you start hacking, you pay little attention to the theory behind the tools and fire away at anything you can get your hands on. Hence the name Script Kiddie. But we all use scripts and automation! Yes, only experienced professionals know what they are doing. A script kiddie fires everything, without knowledge, without consistency, without thinking :)

![Fuzzing](fuzzing.jpg)

But to come to the point, fuzzing is nothing more than enumeration. In fact, I would call it blind enumeration. Sending everything, possible or impossible, expected or not, to the system or application and analysing the results. That’s my definition, but let’s check the official one.

> In programming and software development, fuzzing or fuzz testing is an automated software testing technique that involves providing invalid, unexpected, or random data as inputs to a computer program. The program is then monitored for exceptions such as crashes, failing built-in code assertions, or potential memory leaks. Typically, fuzzers are used to test programs that take structured inputs. This structure is specified, e.g., in a file format or protocol and distinguishes valid from invalid input. An effective fuzzer generates semi-valid inputs that are “valid enough” in that they are not directly rejected by the parser, but do create unexpected behaviors deeper in the program and are “invalid enough” to expose corner cases that have not been properly dealt with.
>
> – Wikipedia

In penetration testing, it’s the same thing, automatically sending various types of random input to the program and recording unwanted events such as crashes, memory leaks or unauthorised access.

If you think you have never done any fuzzing then you are wrong, there are many types of fuzzing activities that you have probably already done using various tools e.g. when testing web application and checking how it reacts to string input in available fields looking for XSS, information disclosure in errors or SQLI, entered folder names in URLs looking for interesting locations with configuration, wrong permissions, looking for admin panel or backups (directory fuzzing), analysing network communication (protocol fuzzing) also known as network fuzzing, focuses on testing the robustness of network protocols. It involves sending malformed or unexpected data to network protocols to identify weaknesses and vulnerabilities in the communication channels. File format fuzzing is specific to applications that handle different file formats, such as document readers, image processors or media players. The aim is to identify weaknesses in the way these applications handle different file formats. API fuzzing involves testing the inputs and outputs of APIs for vulnerabilities. This can help identify security problems in the way APIs handle unexpected or malicious input. Brute force is also known as password fuzzing.

Let him be the first to cast a stone who has not used intruder in a Burp, any Dir Buster tool, Hydra or SQLMap.

There are several types of fuzzing:

**Random fuzzing** - this is the simplest form of fuzzing, where random data is generated and fed as input to the target application. It aims to find vulnerabilities by introducing unexpected and arbitrary input.

**Mutation-based fuzzing** - involves taking existing valid input and making random changes to create new test cases. This method is more targeted than random fuzzing and can sometimes be more effective at finding vulnerabilities.

**Generation-based fuzzing** - test cases are generated based on knowledge of the input format or protocol used by the target application. This approach involves creating inputs that are likely to trigger specific code paths or edge cases within the software.

**Smart fuzzing** - involves the use of more intelligent techniques, such as feedback-driven fuzzing or machine learning, to guide the fuzzing process. This can help to priorities and generate test cases that are more likely to uncover critical vulnerabilities.

Depending on the target, type of activity and method of fuzzing, you will use different lists as input. These can be password dictionaries built from words on the page using [CeWL](https://github.com/digininja/CeWL) or information about the person you have using [Cupp](https://github.com/Mebus/cupp) or [password lists from SecLists](https://github.com/danielmiessler/SecLists/tree/master/Passwords). For directory scanning you can use [Seclist related to web content](https://github.com/danielmiessler/SecLists/tree/master/Discovery/Web-Content) and hundreds dedicated for fuzzing [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Fuzzing). Another good, but no longer updated source of lists is [fuzzdb](https://github.com/fuzzdb-project/fuzzdb).

Here are some simple fuzzing steps you can follow:

- Identify the target system
- Identify inputs
- Generate fuzzed data
- Perform tests on fuzzed data
- Analyse system behaviour
- Problem logging

Now that you know what fuzzing is and how it works, it’s time to look at some tools by way of example. There are two categories of fuzzing tools, those used for fuzzing everything and others known as directory/file fuzzing tools. I haven’t listed outdated, no longer developed tools like dirb, DirBuster and others because the ones that are actively developed are much more useful and have the same and even better functionality than the old ones, exception is made only for wfuzz.

## fuff

A fast web fuzzer written in Go aka Fuzz Fast You Fool. The most powerful fuzzing tool.

### Usage examples

Directory discovery

```bash
ffuf -w /path/to/wordlist -u https://target/FUZZ
```

Virtual host discovery

```bash
ffuf -w /path/to/vhost/wordlist -u https://target -H "Host: FUZZ" -fs 4242
```

GET parameter fuzzing

```bash
ffuf -w /path/to/paramnames.txt -u https://target/script.php?FUZZ=test_value -fs 4242
```

This also assumes a response size of 4242 bytes for invalid GET parameter name.

For wrong parameter in return filtring out 401 response:

```bash
ffuf -w /path/to/values.txt -u https://target/script.php?valid_name=FUZZ -fc 401
```

POST data fuzzing

```bash
ffuf -w /path/to/postdata.txt -X POST -d "username=admin\&password=FUZZ" -u https://target/login.php -fc 401
```

Check more at: <https://github.com/ffuf/ffuf>

## wfuzz

Wfuzz has been created to facilitate the task in web applications assessments and it is based on a simple concept: it replaces any reference to the FUZZ keyword by the value of a given payload. Tools is not developed anymore but works good.

More details: <https://github.com/xmendez/wfuzz>

### Usage examples

Directory discovery

```bash
wfuzz -w wordlist/general/common.txt --hc 404 http://testphp.vulnweb.com/FUZZ
```

Fuzzing parameter

```bash
wfuzz -z range,0-10 --hl 97 http://testphp.vulnweb.com/listproducts.php?cat=FUZZ
```

POST data fuzzing

```bash
wfuzz -z file,wordlist/others/common_pass.txt -d "uname=FUZZ&pass=FUZZ"  --hc 302 http://testphp.vulnweb.com/userinfo.php
```

Cookies

```bash
wfuzz -z file,wordlist/general/common.txt -b cookie=value1 -b cookie2=value2 http://testphp.vulnweb.com/FUZZ
```

or

```bash
wfuzz -z file,wordlist/general/common.txt -b cookie=FUZZ http://testphp.vulnweb.com/
```

Headers:

```bash
wfuzz -z file,wordlist/general/common.txt -H "myheader: headervalue" -H "myheader2: headervalue2" http://testphp.vulnweb.com/FUZZ
```

or

```bash
wfuzz -z file,wordlist/general/common.txt -H "User-Agent: FUZZ" http://testphp.vulnweb.com/
```

More usage samples: <https://wfuzz.readthedocs.io/en/latest/user/basicusage.html>

### My example

And here is my example using [Crunch](https://github.com/jim3ma/crunch) and [CeWL](https://github.com/digininja/CeWL) in combination with wfuzz and a login form attack using parameter fuzzing that I did in the past.

Examples of creating password/user lists:

```bash
crunch 3 3 0123456789ABCDEF -o passwords.txt
or
cewl -d 2 -m 5 -w passwords.txt http://target.com --with-numbers
or
cewl -d 0 -m 5 -w usernames.txt http://target.com/team.php --lowercase
```

and bruteforce using parameter fuzzing:

```bash
wfuzz -c -z file,usernames.txt -z file,passwords.txt --hs "Please enter the correct credentials" -u http://target.com/login.php -d "username=FUZZ&password=FUZ2Z"
```

`-z file,usernames.txt` loads the usernames list.
`-z file,passwords.txt` uses the password list generated by CeWL.
`--hs "Please enter the correct credentials"` hides responses containing the string “Please enter the correct credentials”, which is the message displayed for wrong login attempts.
`-u` specifies the target URL.
`-d "username=FUZZ&password=FUZ2Z"` provides the POST data format where `FUZZ` will be replaced by usernames and `FUZ2Z` by passwords.

Of course you can do the same using [thc-hydra](https://github.com/vanhauser-thc/thc-hydra):

```bash
hydra -L passwords.txt -P 3digits.txt -f -v http://target.com/ http-post-form "/login.php:pin=^PASS^:Access denied" -s 8000
```

but I just wanted to show you that a brute force login form can also be achieved by fuzzing parameters.

## feroxbuster

A fast, simple, recursive content discovery tool written in Rust.

More details: <https://github.com/epi052/feroxbuster>

### Usage examples

File extension fuzzing

```bash
./feroxbuster -u http://127.1 -x pdf -x js,html -x php txt json,docx
```

The command above adds .pdf, .js, .html, .php, .txt, .json, and .docx to each url.

Documentation: <https://epi052.github.io/feroxbuster-docs/docs/>

## dirsearch

Simple web path scanner.

More details: <https://github.com/maurosoria/dirsearch>

### Usage examples

Simple search

```bash
python3 dirsearch.py -u https://target
```

```bash
python3 dirsearch.py -e php,html,js -u https://target
```

```bash
python3 dirsearch.py -e php,html,js -u https://target -w /path/to/wordlist
```

## gobuster

Directory/File, DNS and VHost busting tool written in Go

More details: <https://github.com/OJ/gobuster>

### Usage examples

DNS fuzzing

```bash
gobuster dns -d mysite.com -t 50 -w common-names.txt
```

Directory

```bash
gobuster dir -u https://mysite.com/path/to/folder -c 'session=123456' -t 50 -w common-files.txt -x .php,.html
```

Vhost

```bash
gobuster vhost -u https://mysite.com -w common-vhosts.txt
```

Parameters

```bash
gobuster fuzz -u https://example.com?FUZZ=test -w parameter-names.txt
```

AWS bucket

```bash
gobuster vhost -u https://mysite.com -w common-vhosts.txt
```

## Fuzzing lists

Finally, interesting lists for the above tools. Each tool has it own lists, but it is worth to check other too.

- [SecList](https://github.com/danielmiessler/SecLists)
- [fuzzdb](https://github.com/fuzzdb-project/fuzzdb)
- [Combined-Wordlists](https://github.com/0xspade/Combined-Wordlists)
- [Common Web Managers Fuzz Wordlists](https://github.com/kaimi-io/web-fuzz-wordlists)

Enjoy fuzzing!
