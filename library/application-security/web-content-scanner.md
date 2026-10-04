---
id: ckb-974cedf07ba3
title: Web Content Scanner
category: application-security
format: article
language: en
tags: [bash, dns, tls, web-security]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.77
---

# Web Content Scanner

One of step in web application testing process is scanning and analyzing web server content (searching for web objects). Basically we need launch a dictionary based attack against a server and analyzing the response. It is worth to scan web server to see what kind of files and folders are located on it. It is important to look at some hidden files or files which may contain some configuration options. Any configuration error or file with read access that should not be on the server is a chance to use such information to perform further tests or gain unauthorized access to data or server.

![webcontentscanner](webcontentscanner.jpg)

During several tests that I had the opportunity to do, I found a folders with confidential information or configuration files containing database credentials. Cherry on the top was the folder in which I found a text file with logins and passwords for all services and servers along with phone numbers for specific people responsible for the service. With such capture, the next steps are a trifle.

The scanning itself is fully automatic and does not take too long, which is why it is worth running it during the reconnaissance phase and the first automated operations. This is not always profitable, but this step should not be missed. In the worst case, we lose a maximum of 30 minutes, at best we will have everything we need.

There is few tools you can use. Below are tools recommended by me with some usage examples.

## DIRB

[DIRB](http://dirb.sourceforge.net/) is most popular and comes with a set of preconfigured attack wordlist.

```bash
dirb -r http://webscantest.com/
```

By default it use `/usr/share/wordlists/dirb/common.txt` with 4592 words, if you want to define your wordlist command will look like:

```bash
dirb http://webscantest.com/ /usr/share/wordlists/dirb/common.txt
```

Inside `/usr/share/wordlists/` folder you can find other wordlist.

If you want to generate your own wordlist use `gendict`.

```bash
root@kali:~# gendict
Usage: gendict -type pattern
  type: -n numeric [0-9]
        -c character [a-z]
        -C uppercase character [A-Z]
        -h hexa [0-f]
        -a alfanumeric [0-9a-z]
        -s case sensitive alfanumeric [0-9a-zA-Z]
  pattern: Must be an ascii string in which every 'X' character wildcard
           will be replaced with the incremental value.

Example: gendict -n thisword_X
  thisword_0
  thisword_1
  [...]
  thisword_9
```

## Gobuster

[Gobuster](https://github.com/OJ/gobuster) is a tool used to brute-force: URIs (directories and files) in web sites, DNS subdomains (with wildcard support) and Virtual Host names on target web servers.

Dir example:

```bash
gobuster dir -e -u http://webscantest.com/ -c 'session=123456' -t 50 -w common-files.txt -x php,html,htm,txt
```

DNS example:

```bash
gobuster dns -d webscantest.com -w ~/wordlists/subdomains.txt
```

VHost example:

```bash
gobuster vhost -u http://webscantest.com/ -w common-vhosts.txt
```

## DirBuster

[DirBuster](https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project) is similar to DirB but has a graphical interface. A great solution for fans of the GUI.

![dirbuster](dirbuster.jpg)

## Konan

[Konan](https://github.com/m4ll0k/Konan) is an advanced open source tool designed to brute force directories and files names on web/application servers. It have more features in compare to all tools above.

Basic usage:

```bash
python konan.py -u http://webscantest.com/
```

Provide only status code for output:

```bash
python konan.py -u http://webscantest.com/ -o 200,301,302
```

## Protection

How to defend yourself against this type of scan? Keep only the necessary files on the web server and specify the appropriate read and write permissions for them. Do not keep logs, temporary or test files that contain configurations that could show behavioral of web page or security vulnerabilities.
