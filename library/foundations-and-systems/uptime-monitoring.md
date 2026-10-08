---
id: ckb-e23cb886e3d6
title: Uptime monitoring
category: foundations-and-systems
format: article
language: en
tags: [homelab, linux]
summary: The author discusses the importance of service monitoring and provides a guide on setting up Uptime Kuma for self-hosting service status checks.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-31b-it
  confidence: 0.9
classified_by: google:gemma-4-31b-it@2026-10-08T00:20:40Z
---

# Uptime monitoring

I will start the new year with a simple entry. Specifically, monitoring my own services. As time goes by and you have more and more websites or servers that like to stop working from time to time for various reasons, it is worth monitoring their status. Especially when they are sites or services that provide a cash flow. However, whatever the nature of the site or server, it is worth making a habit of monitoring the status. And that is what today’s article will be about.

![uptime](uptime.webp)

So far, I have been using [Uptime Robot](https://uptimerobot.com/). A free solution with the possibility of extending functionality in the paid version, but the free one allows 50 monitors with 5-minute checks. For an amateur like me, this is completely sufficient. Even for basic monitoring of a small business it is also sufficient. But… as you probably already know, if you are my regular reader, that I like to host my own services. To keep my data and visitor data to myself and not share it with big corporations. And, of course, for learning something new and the joy of independence. This, of course, has its downsides but about that later.

But first, briefly what service monitoring is? It is simply another script that queries services in various ways, e.g. via ping, DNS, tcp port, http queries etc. at a specified interval, checking that the service is responding. If it responds, it is known, everything is ok. If it does not respond, it means the service is not working and sends a status alert, e.g. via email or push message to a Telegram or Discord contact. This allows the service administrator to react quickly and efficiently, resolve the problem and bring the service back to life.

In addition, a service status page can be set up for users to visit. In the event of an outage, they can visit the status page and check whether the service is online or whether it is perhaps a problem on the user’s side. Status pages also allow you to add information about failures and corrective actions, increasing the flow of information between the administrator and users.

The downside of hosting your own monitoring service is that you have to have a separate server just for this service. It makes no sense to put monitoring on the same server that you want to monitor, because if it goes down, so does the monitor. This is obvious to many, but not to all ;)

Another downside, but it’s like any service of your own, you have to deal with it. Maintaining a service means configuration, updates, repairs, changes etc. In the case of the service monitor, this is not too much work. A little bit of time to set up the server, a little bit of time to configure the service itself and then updates and looking in from time to time.

Just what if the monitoring server goes down? You have to set up a monitoring server for the monitoring server, lol.

It is therefore best to set up a small simple server that only supports the monitoring system. I personally have a small VPS for such a solution and have not had any problems with it yet for a year. I have implemented automatic system updates and from time to time when a new version of the monitor comes out, I manually update it. In addition, I have a status page open in my browser bookmarks and look there once a day.

Thanks to the monitor, I solve service problems within a few hours, well, unless it’s night and I’m asleep, I fix it straight away in the morning. If my monitoring server goes down, at worst I will see it during the day, but its absence does not affect the operation of other services, only trace their monitoring.

Now to the point, I use [Uptime Kuma](https://uptime.kuma.pet/) as a solution. Here you can check status page [for UptimeKuma](https://status.kuma.pet/) itself, and here is the [GitHub repository](https://github.com/louislam/uptime-kuma). If you choose it as your solution too, please refer to the [documentataion](https://github.com/louislam/uptime-kuma/wiki).

You can check my services status page [here](https://uptime.0ut3r.space/status/hoek). And if you are a loyal fan of mine, use the status page to monitor your favourite services that I run. Currently I am monitoring this blog [0ut3r.space](https://0ut3r.space/) and it’s [onion URL](../../../../index.html) + [Swap Cab](https://swap.cab/) website about crypto swaps and crypto debit cards + [Bounty Hunter](https://bountyhunter.red/), my private bounty landing page + [5BTC](https://5btc.lol/), fancy, social crypto currency experiment and also its [onion URL](http://sjpglmishoubmbxzop3t7cwmck6vphskdkmxvwcpxfpjpz4e7yhb5pid.onion/) + [Captured Today](https://captured.today/) which is my amateur photo gallery + home router, so when I am on holidays I know if something wrong is going on with my home network + [Stats](https://stats.0ut3r.space/) page, so my self hosted analytics service based on [Umami](https://github.com/umami-software/umami). I encourage you to read the article in which [I switch from Google Analytics to Umami](https://reycdxyc24gf7jrnwutzdn3smmweizedy7uojsa7ols6sflwu25ijoyd.onion/2025/01/15/uptime-monitoring/2023/06/15/analytics/). I took the opportunity to advertise all my current services. I hope you don’t mind. You can always find a list of all current ones on the [projects subpage](https://reycdxyc24gf7jrnwutzdn3smmweizedy7uojsa7ols6sflwu25ijoyd.onion/2025/01/15/uptime-monitoring/projects/).

Setting up the Uptime Kuma service itself, is not complicated. This can be done with the help of Docker or manually. I am not a fan of containers, so I do it manually. Here are the steps I followed on my previously configured and secured server running Debian.

To run the Non-Docker option you will also need to have all the prerequisites installed, here is the list with links to the installation procedures.

- [Node.js](https://nodejs.org/en/download/) + Npm
- [Git](https://git-scm.com/downloads)
- [PM2](https://pm2.keymetrics.io/docs/usage/quick-start/)

When all requirements are met, we continue as described in the official instructions:

```bash
git clone https://github.com/louislam/uptime-kuma.git
cd uptime-kuma
npm run setup

Run in the background using PM2
# Install PM2 if you don't have it:
npm install pm2 -g && pm2 install pm2-logrotate

# Start Server
pm2 start server/server.js --name uptime-kuma
```

Other useful commands for managing the background service:

```bash
# If you want to see the current console output
pm2 monit

# If you want to add it to startup
pm2 save && pm2 startup

# If you want to list running applications
pm2 list
```

Official steps can be found in [Non-Docker instruction](https://github.com/louislam/uptime-kuma?tab=readme-ov-file).

To upgrade when a new version is released, simply follow these steps:

```bash
cd <uptime-kuma-directory>

# Update from git
git fetch --all
git checkout 1.23.16 --force

# Install dependencies and prebuilt
npm install --production
npm run download-dist

# Restart
pm2 restart uptime-kuma
```

For more details on updates [How To Update](https://github.com/louislam/uptime-kuma/wiki/%F0%9F%86%99-How-to-Update).

It is also a good idea to configure nginx to act as a reverse proxy for our monitor, allowing access to the world. It is not advisable (if only for security reasons) to open ports and forward traffic from the world directly to the application.

My Nginx configuration with Certbot looks like this:

```bash
server {
  server_name uptime.0ut3r.space;
  location / {
    proxy_pass http://127.0.0.1:3001;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   Host $host;
    proxy_http_version 1.1;
    proxy_set_header   Upgrade $http_upgrade;
    proxy_set_header   Connection "upgrade";
}
        # X-XSS-Protection
        add_header x-xss-protection "1; mode=block";
        # X-Content-Type-Options
        add_header X-Content-Type-Options "nosniff";
        # X-Frame-Options
        add_header x-frame-options "SAMEORIGIN";
        # Referrer-Policy header
        add_header Referrer-Policy "no-referrer-when-downgrade";

        #Bad Bot Blocker
        include /etc/nginx/bots.d/blockbots.conf;
        include /etc/nginx/bots.d/ddos.conf;

        # Logs
        error_log  /var/log/nginx/uptime.error.log;
        access_log /var/log/nginx/uptime.access.log;

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/uptime.0ut3r.space/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/uptime.0ut3r.space/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
server {
    if ($host = uptime.0ut3r.space) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

  server_name uptime.0ut3r.space;
    listen 80;
    return 404; # managed by Certbot
}
```

You can take it with you, but don’t forget to modify it to suit your needs and setup.

You may probably noticed that it also monitors services configured as [hidden services](https://support.torproject.org/pl/glossary/hidden-services/) with the [onion domain](https://support.torproject.org/onionservices/). This is also the reason why I chose Uptime Kuma and the self-hosted solution, so that I could configure my own proxy server with Tor to query the onion domains and monitor their status.

For this we need [Tor](https://support.torproject.org/apt/) and [Tinyproxy](https://github.com/tinyproxy/tinyproxy). Install both using the linked instructions. Tor has a socks proxy server open on port 9050 by default after installation.

For example, configure Tinyproxy on port 8888 and use it with Tor.

```bash
sudo nano /etc/tinyproxy/tinyproxy.conf
```

Find and change these values:

```bash
Port 8888
upstream socks5 127.0.0.1:9050
MaxClients 1
Allow 127.0.0.1
BasicAuth <SET_PROXY_USERNAME> <SET_PROXY_PASSWORD>
```

Restart Tinyproxy:

```bash
sudo systemctl restart tinyproxy
```

Allow port 8888 on the firewall, I am running Debian so I will use UFW:

```bash
sudo ufw allow 8888/tcp
```

Now you can go to the `Uptime Kuma Dashboard -> Settings -> Proxy` and enter all the details. Protocol is HTTP, server localhost on port 8888. Enable the server authorization option and fill in the user and password you set up in Tinyproxy config.

When you add a new monitor in Uptime Kuma, you can select a proxy option for it. Select the one you just configured and from now on this monitor will use proxy configured with Tor and will be able to resolve onion domains.

Remember to adjust the response time for such a monitor and the number of attempts before an alarm is triggered accordingly, onion services take a little longer to respond than standard sites on the regular Internet. Based on your own experience and the number of false alarms you will be able to adjust these values. I have set my parameters so that, for normal pages, the check is performed every 3 minutes (180 sec), if the service does not respond, it is checked twice more every minute (60 sec) and if it does not respond after this many attempts, an alarm is generated. The request time limit is 48 sec. For onion domains I have a check every 20 minutes (1200 sec) and if twice every 5 minutes (300 sec) the service does not respond after the first being offline, an alarm is generated. The request time limit is 96 seconds. It could probably be done better, but for me it works as it should and I have no false alarms.

When you configure alerts without repeats and every short interval, for example, for my router at home, I have seen interruptions when it resets during an update or regularly at 2 am, or when the provider makes changes to the firmware. As I don’t need this kind of knowledge, implementing repetition in checking the service in a quick interval when it reports a problem the first time excludes short reboots or simply temporary problems with the network, proxy etc. from monitoring. I don’t have an SLA of three nines so I can afford to do this.

That would be it for this first entry in the new year. All the best and as few interruptions to your servers as possible!
