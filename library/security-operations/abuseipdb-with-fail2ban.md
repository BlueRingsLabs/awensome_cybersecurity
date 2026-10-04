---
id: ckb-7c3259ec9c95
title: AbuseIPDB with Fail2Ban
category: security-operations
format: article
language: en
tags: [bash, git, privilege-escalation, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.31
---

# AbuseIPDB with Fail2Ban

Do you remember my last entry about [Fail2Ban](https://0ut3r.space/2018/05/01/fail2ban-best-jail/)? Cool. This time we will connect [Fail2Ban](https://www.fail2ban.org/wiki/index.php/Main_Page) with [AbuseIPDB](https://www.abuseipdb.com/fail2ban.html) service. Why? To report and identify IP addresses that have been associated with malicious activity online.

Below you can see my contributor badge. This badge shows you how many IPs I reported. All of them was blocked by Fail2Ban and automatically sent to AbuseIPDB.
 [![](https://www.abuseipdb.com/contributor/24947.svg)](https://www.abuseipdb.com/user/24947 "AbuseIPDB is an IP address blacklist for webmasters and sysadmins to report IP addresses engaging in abusive behavior on their networks")

## AbuseIPDB

I found this website few years ago and I was using it to check IP reputation. Never had a time to configure it with my server. Today came the day to finally get involved.

> [AbuseIPDB](https://www.abuseipdb.com/) is a project dedicated to helping combat the spread of hackers, spammers, and abusive activity on the internet.
>
> Our mission is to help make Web safer by providing a central blacklist for webmasters, system administrators, and other interested parties to report and find IP addresses that have been associated with malicious activity online.

So you can report bad IP, check IP reputation in database and also using API, integrate it with your server. There are few [pricing plans](https://www.abuseipdb.com/pricing) but for my needs, a free account is enough.

## Integrating AbuseIPDB with Fail2Ban

Few things before you can start configuration:

- make sure you have installed and configured Fail2Ban. You can use [my tutorial](https://0ut3r.space/2018/05/01/fail2ban-best-jail/) or find any other [online](https://duckduckgo.com/?q=fail2ban+configuration&t=h_&ia=web)
- register account on [AbuseIPDB](https://www.abuseipdb.com/pricing) website
- [verify](https://www.abuseipdb.com/account#webmasters) your website, it’s just few simple steps (it will also increase your daily limits from 1000 to 3000 requests)
- generate APIv2 key

All steps are described very good once you are logged in. Just follow instructions on website.

Now you are ready to go.

Ability to report IPs directly to AbuseIPDB was added to the Fail2Ban repository in **v0.10.0**. Check your version using command: `fail2ban-client -V`. Update Fail2Ban if needed. You can find latest version on [Github](https://github.com/fail2ban/fail2ban).

## Activate AbuseIPDB Reporting Action

You can invoke the AbuseIPDB action from some or all of the jails configured in `jail.local`. The action must be called with two parameters - your **AbuseIPDB API key**, and the [abuse category (or categories)](https://www.abuseipdb.com/categories) you would like to report the IP for. If these parameters are missing or invalid, your reports will fail.

```bash
%(action_abuseipdb)s[abuseipdb_apikey="my-api-key", abuseipdb_category="18,22"]
```

This line of code must be added to each jail for which you want to activate AbuseIPDB reporting. Here’s an example of how you would configure the AbuseIPDB report action to run, in addition to your default ban actions, when the ssh brute force jail is triggered:

```bash
[sshd]

# To use more aggressive sshd modes set filter parameter "mode" in jail.local:
# normal (default), ddos, extra or aggressive (combines all).
# See "tests/files/logs/sshd" or "filter.d/sshd.conf" for usage example and details.
#mode   = normal
enabled = true
port    = 22
logpath = %(sshd_log)s
backend = %(sshd_backend)s

# Ban IP and report to AbuseIPDB for SSH Brute-Forcing
action = %(action_)s
         %(action_abuseipdb)s[abuseipdb_apikey="my-api-key", abuseipdb_category="18,22"]
```

However, the AbuseIPDB action can also be added to the list of Fail2Ban actions in the global [DEFAULT] as shown below, which will cause it to run on all jails without an action specified:

```bash
# Choose default action.  To change, just override value of 'action' with the
# interpolation to the chosen action shortcut (e.g.  action_mw, action_mwl, etc) in jail.local
# globally (section [DEFAULT]) or per specific section
action = %(action_)s
         %(action_abuseipdb)s[abuseipdb_apikey="my-api-key", abuseipdb_category="18"]
```

But it’s recommended to add the AbuseIPDB action individually to your jails so you can customize the AbuseIPDB report categories.

As we configure APIv2 (because APIv1 is deprecated) one line need to be changed in `abuseipdb.conf`

```bash
sudo nano /etc/fail2ban/action.d/abuseipdb.conf 
```

Find line starting from `actionban` and replace it with

```bash
actionban = curl --fail 'https://api.abuseipdb.com/api/v2/report' -H 'Accept: application/json' -H 'Key: <abuseipdb_apikey>' --data-urlencode "comment=<matches>" --data-urlencode 'ip=<ip>' --data 'categories=<abuseipdversionb_category>'
```

Now save configuration and restart Fail2Ban service.

```bash
sudo service fail2ban restart
```

or

```bash
sudo fail2ban-client reload
```

If you stuck somewhere, you can always take a look into official documentation:

<https://www.abuseipdb.com/fail2ban.html>

<https://docs.abuseipdb.com/#configuring-fail2ban>

<https://www.fail2ban.org/wiki/index.php/Main_Page>

<https://github.com/fail2ban/fail2ban/wiki>

Good luck!
