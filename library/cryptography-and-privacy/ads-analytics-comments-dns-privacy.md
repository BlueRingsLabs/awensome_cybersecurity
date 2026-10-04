---
id: ckb-11b84ebf6d1c
title: Ads, analytics, comments, dns, privacy ...
category: cryptography-and-privacy
format: article
language: en
tags: [anonymity, databases, dns, git, privacy, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.48
---

# Ads, analytics, comments, dns, privacy ...

In the past I tested [GoAccess as solution to monitor page views, visitors activity and technology](../../../../2021/04/12/goaccess/index.html). I also compared it to the Google Analytics. When I wrote article about [Anonymous Tor Phone](../../../05/02/anonymous-tor-phone/index.html) I received one comment like:

> How fucking ironic is this post? This dude has no fucking idea what he is talking about. Everything that you posted about your setup is literally the opposite of what a person with real opsec would do. I am not going to debunk the whole post because that would take ages and considering how stupid the author is, I dont even think he would get the point. Also, talking about anonymity and having google ads on your blog justifies my whole point. This person is moronic and a hypocrite. I fucking hate people like this.
>
> ~Dan

That was one of the reason I disabled anonymous comments. Probably freedom of speech should not look like this. Other reason was that Disqus forced too much ads above comment section. I wanted to replace it with some [Utternace](https://github.com/utterance/utterances) commenting system, but it was not worth time spent on configuration in compare to amount of comments I received since the beginning of this website. Anyway. Not sure how much article about anonymous phone is related to the website where Google Ads are displayed, it was probably some very big mental shortcut, but even from comments like this I always try to find something good I can improve.

As every blogger would like to get some money for what they are doing (remember, for me it is a hobby and place where I can skill up my English and writing skills) I also started looking for ads platform, and tbh Google on this field is not bad and pay good for displaying ads. Thanks to the one ad, located at the bottom of each article, the server where 0ut3r.space is hosted, is paid. For me that’s cool. I did some research about ads platforms, but didn’t find anything good for such a small website like mine. If you have any good tested solution as alternative to Google, for small websites, I am more than happy to test it. But would it change anything related to privacy? I do not think so, as every ads company track users to display ads better. When I get rich I disable ads on 0ut3r.space. In the past I displayed it in a few more places, but after other visitor comment, that there is too much ads, I changed it to minimum, and put it in place where its not breaking content. Funny is that other people even didn’t notice that ads are here as they were using adblocker :) Also I think its cool when ads are related to website, it content and are targeted for reader based on his activity. I know that there is a very fine line between targeted advertising, and exploiting people, and pushing trash to them at an inflated price. But Google is doing a good job of selecting ads on my site so far.

Anyway, I thought ok, but I am also using Google Analytics for website stats, that’s probably big privacy issue for my visitors. Probably even bigger than Google Ads (why Dan was not concerned about that?) I feed big evil corporation with my readers data and thanks to that, ads can be displayed better, and Google knows more about 0ut3r Space visitors operating system, country, city, age, shoe size, ex girlfriends name, etc.

I decided to do a research about Google Analytics alternative and I found a lot self hosted solutions. It took me some time to choose one that fits my needs, but it was worth it. Now I have all my visitors data and I can do with it whatever I want for example sell it, publish it and do all stuff like Google is doing. Okay too much sarcasm. But keep in the back of your mind that big corporations are already so tightened and monitored that your data is much safer there than on my hard drive in the basement.

I choose [Umami](https://umami.is/). From today Google Analytics are disabled and stats for this website are hosted on same server where website is located and only I have access to it. People in foil hats can say, yes, you and Umami owners. Yeah who knows, I would also add Jesus, as Jesus sees everything.

![Umami Analytics](umami.png)

We should individually decide who we trust, who we entrust our data to and who we don’t. And if someone trusts Google and someone else trusts Facebook, we should respect that. I use solutions from Google, but avoid Meta and Twitter. Someone else uses Microsoft, but avoids Google and has Twitter. Nowadays it’s really hard to give up all the goodies, or to say with a clear conscience, my data is safe. Well, unless you turn off your computer and throw away your phone and delete everything you put to the internet from the very first day. But even then you will be in some institution or government office database. But that’s probably good idea for other article about nobody cares.

Lets get back to the topic. I think Google Analytics tool is awesome, complex and have everything that big companies, SEO team, or marketing guys needs. For me sometimes it was too much, and half of stats I do not understand and even do not have need to understand or even not use. But this is one of the big evil corp that use these stats for themselves.

Umami, is easy to setup, clean, simple, but also powerful with all stats I need. I just want to see how many users visited my site, some page views and referrers. Rest like system, browser, location etc. is just fancy addon. Also live stats are cool, to see how many visitors are online. Also hosting analytics tool in a subdomain of main domain probably makes it more trusted by browsers and not blocked by default by some extensions. That’s something I am considering to test in near future.

## Basic compare Google and Umami

Here is a bunch of screenshots to compare results for 7 days of stats from Google Analytics and Umami. I wanted to review it before I trust Umami and disable Google Analytics.

Users and page views

![views visitors google](views-visitors-google.png)

![views visitors umami](views-visitors-umami.png)

Pages and referrers

![pages referrers google](pages-referrers-google.png)

![pages referrers umami](pages-referrers-umami.png)

Browser, OS, device

![browser os device google](browser-os-device-google.png)

![browser os device umami](browser-os-device-umami.png)

Countries

![Countries Google](countries-google.png)

![countries umami](countries-umami.png)

That’s are just quick summary, to make general overview. Pretty much the same. Even for URLs and details if I go deeper in Google Analytics dashboards.

If you have a time I recommend you to setup your own self hosted analytics system, and add your websites there. A lot of fun and it looks cool.

## Self hosted analytics platform

Here is the list of self hosted analytics platforms I discovered during my research. Some of theme are very advanced and can do the same or even more than Google Analytics. Maybe you will find something useful for you.

- <https://umami.is/>
- <https://matomo.org/>
- <https://www.goatcounter.com/>
- <https://www.openwebanalytics.com/>
- <https://github.com/milesmcc/shynet>
- <https://piwik.pro/>
- <https://plausible.io/>
- <https://github.com/offen/offen>
- <https://github.com/allinurl/goaccess>
- <https://github.com/electerious/Ackee>
- <https://github.com/Countly/countly-server>
- <https://github.com/PostHog/posthog>

## Ads and trackers blockers

I am not sure why Dan (they guy from the comment from the beginning of this article) seen ads on my website, as if he cares about his privacy and anonymity he should definitely use tools like ads blocker, java script blocker and other privacy browser extensions. Then no matter what is implemented on any website, user is more secure. Or even choose connecting to my site using [onion domain](https://0ut3r.space/2019/01/21/onion-address/), I configured in case that someone would like to visit my site more anonymously using Tor Browser.

Funny story is that before I proper configured Google Ads on my website I allowed Google to place ads where they think it’s best and as much as they think it should be. I forgot about that test and didn’t see results as I forgot to disable ads blocker for my own website xD. Next day my wife told me that my website started looking trashy, I realized then - oh my gosh, I forgot to change settings. Ads were everywhere, like in the Internet Explorer in the beginning of 21’st century.

![](iepopups.jpg)

But after some manual tweaks it looks good now.

If you do not like ads or tracking systems and want to block theme use ads block web browser extension. I am using [uBlock](https://ublock.org/en) with some additional custom lists, and I can fully recommend it. At the end of 2022 I even created a list of [Top security web browser plugins](../../../../2020/01/08/top-security-browser-plugins/index.html) it is also located on [Alternativeto.net](https://alternativeto.net/list/381/top-security-web-browser-plugins/). Don’t use them all at once, choose one or two and configure it properly.

And I recommend read Terms Of Service, Privacy Policy and some Disclaimers on each website and service you are using, before interact deeper or create account, as if you do not agree about something you can stop use it. Here is [ToS](../../../../tos/index.html) for 0ut3r.space I guess you even didn’t know about it. There is info about cookies, tracking codes and other stuff that nobody cares, but should on every website.

## DNS

If you want to block trackers, malicious content and ads on a bit higher level you can always use some DNS solution. You can setup your own DNS using [Pi-Hole](https://pi-hole.net/) and pass through it all your devices connected to the network.

You can also choose some already working free solutions like <https://adguard-dns.io/> or <https://nextdns.io/>.

For my mobile devices I am using AdGuard and here is example of 7 days stats from my 3 mobile devices (my phone, my wife’s phone and kitchen tablet).

![dns-stats](dns-stats.png)

52% of requests were blocked. More than half of my mobile devices traffic is a junk :) Free plan is too small for adding my laptop and TV, so maybe I will buy paid plan or setup Pi-Hole in near future. Meanwhile browser plug-ins have to suffice.

It has to be article about moving from Google Analytics to Umami, but it ended with some ads blocking, comments, privacy related and DNS stuff. Well, that happens every time I got a plan and a thousand thoughts around.

## Umami installation

Oh yeah btw, in case you would also check Umami, here are some useful links for Umami installation.

- <https://umami.is/docs/getting-started> - installation instruction. You can use Yarn or Npm or both in same time. I discovered Yarn during this deployment and found it faster than npm.
- Pm2 usage - <https://pm2.keymetrics.io/docs/usage/process-management/>

Some useful commands for Mysql:

Check users:

```plaintext
SELECT user,authentication_string,plugin,host FROM mysql.user;
```

Create user

```plaintext
CREATE USER 'USERNAME'@'localhost' IDENTIFIED BY 'password';
```

Create database

```plaintext
CREATE DATABASE `DTABASENAME`;
```

Grant privilages

```plaintext
GRANT ALL privileges ON `DATABASENAME`.* TO 'USERNAME'@localhost IDENTIFIED BY 'YOURPASSWORD';
```

Apply changes

```plaintext
FLUSH PRIVILEGES;
```

And here are steps I did for installing:

```bash
sudo npm install -g yarn
git clone https://github.com/umami-software/umami.git
cd umami
sudo yarn install
sudo nano .env
```

And in that configuration file I added database details:

```bash
DATABASE_URL={connection url}
DATABASE_URL=mysql://USERNAME:YOURPASSWORD@localhost:3306/DATABASENAME
```

That’s all folks. Happy stats analyzing.
