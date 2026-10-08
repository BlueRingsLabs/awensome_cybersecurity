---
id: ckb-331015566dbd
title: GoAccess and real website stats
category: security-operations
format: article
language: en
tags: [bash, linux, log-analysis]
summary: This article demonstrates how to use GoAccess to analyze server logs for accurate website traffic statistics, highlighting the discrepancies between server-side logging and client-side analytics tools.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.9
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:15:22Z
---

# GoAccess and real website stats

Does [Google Analytics](https://analytics.google.com/) shows the same stats as logs from your server? Sure it doesn’t. A lot of people (including me) use various [Privacy tools](https://privacybadger.org/), [Ads](https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm) or [JavaScript](https://noscript.net/) blockers. As an admin of the website, I would like to know how many visitors I have. It is going to be even harder, when your website also have an onion address. Connection is anonymized and [TorBrowser](https://www.torproject.org/download/) is blocking by default all scripts. Additionally, the use of external analysis tools only feeds large corporations with data on user behavior in the network. I don’t say they are bad, but they are not showing you everything.

![weblogs](weblogs.jpg)

So it doesn’t matter if I am using Google Analytics or some open source alternative like [Matomo](https://matomo.org/) (previously Piwik), [Open Web Analytics](http://www.openwebanalytics.com/) or any other. I have to rely on my own logs. I have [read one article](https://informatykzakladowy.pl/google-analytics-a-prawdziwa-ogladalnosc-bloga/) recently, and one guy in the comments remind me about [GoAccess](https://goaccess.io/). I’ve played with it in the past and forgot it completely. Time to turn it back on and check for discrepancies.

I am on Debian, I decided to use official repository (in Debian repo GoAccess is outdated).

```bash
echo "deb https://deb.goaccess.io/ $(lsb_release -cs) main" | sudo tee -a /etc/apt/sources.list.d/goaccess.list
wget -O - https://deb.goaccess.io/gnugpg.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/goaccess.gpg add -
sudo apt-get update
sudo apt-get install goaccess
```

On [Github](https://github.com/allinurl/goaccess) page you can find other methods to install GoAccess on various systems. [Official documentation](https://goaccess.io/get-started) is also quit nice.

One simple command to check logs:

```bash
sudo goaccess /var/log/nginx/access.log /var/log/nginx/access.log.1 --log-format=COMBINED
```

Just provide path to your access.log defined in www server (Apache or Nginx etc.) To check logs in real-time add parameter `-c`

![GoAccess Console Stats](goaccess_console_stats.jpg)

To generate console output from all logs even these compressed, you can use:

```bash
zcat -f access.log* | goaccess --log-format=COMBINED
or
zcat access.log.*.gz | goaccess --log-format=COMBINED
```

To generate HTML report use:

```bash
sudo goaccess access.log -a > report.html
```

To see html report in real time on your website:

```bash
sudo goaccess access.log -o /usr/share/nginx/html/your_site/report.html --real-time-html
```

![GoAccess HTML Report](goaccess_html_stats.jpg)

## Results

This part probably is going to be boring for you, but I am excited to see and compare results. Time range is 16.03.2021 to 12.03.2021.

Of course, this whole comparison should include a lot more, like network scanners, bots etc, but I don’t really need it, and someone inspired by this article might go a step further. The analysis and comparisons of others show that the difference in their observations is always 40% to 60% between server logs and Google Analytics results. I also have an Onion address so in my case looks like 0ut3r.space is more popular in Tor rather than standard Internet. Same knowledge split in two domains, but the one served as hidden service is more interesting. I experimented with artificially generated traffic, or free points, or SEO coupons for positioning phrases in search engines like Google and Bing, for the domain in Clearnet. I have not done stroke of work when it comes to the onion domain :) It looks like everything that is uploaded to the deep web is twice as interesting, useful, forbidden and hacker-friendly than on the regular Internet. The domain [https://0ut3r.space](https://0ut3r.space/) is just another stupid and boring blog from some amateur. On the other side domain [http://reycdxyc24gf7jrnwutzdn3smmweizedy7uojsa7ols6sflwu25ijoyd.onion](../../../../index.html) is definitely a hacker, cracker, pyromaniac and [éminence grise](https://en.wikipedia.org/wiki/%C3%89minence_grise), who definitely use drugs and is taking a bath in a bathtub full of Bitcoins.

### Visitors and Hits

Just one word about naming. Visitors and Hits in GoAccess are called Users and Pageviews in Google Analytics.

![Analytics Users and Pageviews](analytics_users.jpg)

966 Users and 1994 Pageviews

VS

![GoAccess Visitors and Hits](goaccess_users.png)

12929 Visitors and 186691Hits. [Narf!](https://media1.giphy.com/media/12UWMsiE9gTuCI/giphy.gif)

This screen can explain a lot in case of visitors from Tor Onion address, but still numbers are quite bit different right? This is why I like to analyze logs directly from the server.

![GoAccess IPS](goaccess_ips.png)

### Operating system

![Analytics OS](analytics_os.jpg)

VS

![GoAccess OS](goaccess_os.png)

### Browsers

![Analytics Browsers](analytics_browsers.jpg)

VS

![GoAccess Browsers](goaccess_browsers.png)

### Summary

The differences are visible. Is it wrong? It depends on what you want to achieve. Google Analytics shows what it can, and since the scripts analyzing traffic are often blocked, it will not count everything. The server logs do not lie, but they show everything they can and they are not enriched with what Google knows as a giant. Without info for the analyst who wants to see what profits the website will bring him or what the estimated age of users has been calculated. If you are interested in real traffic and the number of users, check the logs. If you are interested in earnings, ads, users age, shoe size and which model of smartphone was used, rely on Google Analytics or its alternatives. Google gives a lot of what you cannot read from the server logs alone.

For example definitely can’t find from logs what search query users put into the Google Search (or any other available fancy stats), and how many of them visited my page after such a search.

![Analytics Search Query](analytics_search_query.jpg)

On the other side, stats from the “Not Found URLs” tells a lot. If link points to something that never exist it means that some vulnerability scanner is looking for something. Maybe it is a Google Bot? Maybe hacker looking for weak points in configuration, or sensitive data? Who knows ;)

![GoAccess 404](goaccess_404.jpg)

Good luck with numbers and let me know how it looks on your side. If you are not a website admin, just a visitor, I definitely need to know what is your shoe size. I miss this data in Google Analytics.

I also created stats using GoAccess for my other website. You can check it [here](https://bountyhunter.red/stats.html), and see it in action. It shows website stats generated everyday on midnight and display in form of html report. Here is cron setup for this:

```bash
0 0 * * * zcat -f /var/log/nginx/access.log* | goaccess - -o /var/www/mywebsite/stats.html --log-format=combined --anonymize-ip --exclude-ip=<MY_IP> >/dev/null 2>&1
```

or you can create script file

```bash
#!/bin/bash
/bin/zcat -f /var/log/nginx/access.log* | goaccess - -o /var/www/mywebsite/stats.html --log-format=combined --anonymize-ip --exclude-ip=<MY_IP> > /dev/null 2>&1
```

and execute file by cron

```bash
0 0 * * * sh /home/user/updatestats.sh
```
