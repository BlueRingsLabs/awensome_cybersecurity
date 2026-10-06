---
id: ckb-78ea9c3dd9b8
title: Device search engine
category: foundations-and-systems
format: article
language: en
tags: [bash, networking, nmap, osint, tls, web-security]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.49
---

# Device search engine

It’s possible to scan all Internet looking for devices and network components. But it’s not so easy. If you would like to get more information about that, check these materials [Fyodor - Nmap: Scanning The Internet](https://nmap.org/presentations/BHDC08/). Interesting, right?

Today it’s easier. Theres few web search engines which allows everyone to search for computers, printers, video recorders, NAS servers and any other device connected to the Internet. If these devices are not correctly setup you can even gain access to them. But you shouldn’t do that, more or less it is illegal.

![Search Engines](networkdevices.jpg)

How it works is simple. The website crawls the Internet for publicly accessible devices and display results.

The primary users of these systems are cybersecurity professionals, researchers and law enforcement agencies but also cybercriminals.

Here is the list of device search engines.

## Shodan

Shodan is the world’s first search engine for Internet-connected devices.

<https://www.shodan.io/>

Here you can find an interesting way to display data from Shodan <https://2000.shodan.io/>

Shodan have it’s own [command line interface](https://cli.shodan.io/). Also there is interesting tool using [Shodan Api](https://developer.shodan.io/) called [SearchDiggity](https://www.bishopfox.com/resources/tools/google-hacking-diggity/attack-tools/).

### Example of use:

Find Apache servers in New York:

```bash
apache city:"New York"
```

Find Nginx servers in Germany:

```bash
nginx country:"DE"
```

Find Cisco devices on a particular subnet:

```bash
cisco net:"216.219.143.0/24"
```

The basic search filters you can use:

- `city`: find devices in a particular city
- `country`: find devices in a particular country
- `geo`: you can pass it coordinates
- `hostname`: find values that match the hostname
- `net`: search based on an IP or /x CIDR
- `os`: search based on operating system
- `port`: find particular ports that are open
- `before/after`: find results within a timeframe

## CenSys

Censys is a platform that helps information security practitioners discover, monitor, and analyze devices that are accessible from the Internet.

<https://censys.io/>

### Example of use:

Search for hosts with the HTTP Server Header “Apache” in Germany

```bash
80.http.get.headers.server: Apache and location.country_code: DE
```

Telnet and FTP hosts in Germany:

```bash
location.country_code: DE and protocols: ("23/telnet" or "21/ftp")
```

## ZoomEye

ZoomEyeis a Cyberspace Search Engine recording information of devices, websites, services and components etc.

<https://www.zoomeye.org/>

### Example of use:

Search by application:

```bash
app: application name
ver: version number
```

Search by location:

```bash
country: country code (for example: UK, IT, ES, FR, CN, JP..)
city: name of city
```

Search by port:

```bash
port: port number
```

Search by OS:

```bash
os: name of the operating system (for example os:linux)
```

Search by service:

```bash
service: service name
```

Search by hostname:

```bash
hostname: hostname (for example hostname:google.com)
```

Search by IP Address:

```bash
ip: ip address (for example ip:8.8.8.8)
```

Search by CIDR:

```bash
cidr: cidr segment (for example cidr:8.8.8.8/24)
```

Search by site:

```bash
site: domain name (for example site:google.com)
```

Search by HTTP Headers:

```bash
headers: headers in HTTP request
```

Search by SEO keywords:

```bash
keywords: keywords defined inside <meta name="Keywords">
```

Search by description:

```bash
desc: description inside <meta name="description">
```

Search by title:

```bash
title: title inside <title>
```

## FoFa

The Chinese equivalent of Shodan.

<https://fofa.so/>

FoFa also has a [client version](https://fofa.so/about_client).

### Example of use:

```bash
title="abc"
header="abc"
body="abc"
domain="qq.com"
host=".gov.cn"
port="443"
ip="1.1.1.1"
protocol="https"
city="Beijing"
region="Zhejiang"
country="CN"
cert="google.com"
banner=users && protocol=ftp
type=service
os=windows
server=="Microsoft-IIS/7.5"
```

```bash
title="powered by" && title!=discuz
```

More complex:

```bash
title!="powered by" && body=discuz
( body="content=\"WordPress" || (header="X-Pingback" && header="/xmlrpc.php" && body="/wp-includes/") ) && host="gov.cn" 
```

## Ivre

IVRE is an open-source framework for network recon. It relies on open-source well-known tools (Nmap, Zmap, Masscan, Bro and p0f) to gather data (*network intelligence*), stores it in a database (MongoDB), and provides tools to analyze it.

<https://ivre.rocks/>

### Example of use:

This tool is not available to public. You need to install, configure and gather data on your own before use.
