---
id: ckb-e38517ebc005
title: Let’s Encrypt SSL Cert for Nginx
category: cryptography-and-privacy
format: article
language: en
tags: [bash, firewall, linux, privilege-escalation, tls, web-security]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.52
---

# Let’s Encrypt SSL Cert for Nginx

I decided to use the [Let’s Encrypt](https://letsencrypt.org/) offer and configure the free certificate for my website. From today you are browsing my website in a safe way.

[HTTPS](https://en.wikipedia.org/wiki/HTTPS) keeps stuff secret by encrypting it as it moves between your browser and the website’s server. This ensures that anyone listening in on the conversation can’t read anything. This could include your ISP, a hacker, snooping governments, or anyone else who manages to position themselves between you and the web server.

![http encryption](httpsncryption.jpg)

I encourage everyone to implement this solution on their websites. In addition, using https has a good effect on website positioning. Google is more likely to promote websites that encrypt traffic than those without encryption.

Below I will present the steps I have made to configure my web server ([Nginx](https://www.nginx.com/)) on Debian to use HTTPS.

[Here](https://certbot.eff.org/) are other solutions for other web servers and systems.

## SSL Cert for Nginx on Debian

### Pre-settings

Edit source list

```bash
sudo nano /etc/apt/source.list
```

Add backports (in my case it is Debian 9)

```bash
deb http://ftp.debian.org/debian stretch-backports main
```

Update packages list

```bash
sudo apt-get update
```

Install [Certbot](https://certbot.eff.org/) for Nginx

```bash
sudo apt-get install python-certbot-nginx -t stretch-backports
```

### Firewall rules

I am using [UFW](https://0ut3r.space/2018/09/03/ufw-simple-firewall/). These are commands to allow traffic on spcific ports.

```bash
sudo ufw allow 443/tcp
sudo ufw allow 80/tcp
```

For IP Tables:

```bash
iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
iptables-save > /etc/iptables/rules.v4
```

### Nginx

In Nginx configuration you need to check if `server_name` is set.

```bash
sudo nano /etc/nginx/sites-available/default
```

Add domain name to server block

```bash
server_name example.com www.example.com;
```

Check Nginx config

```bash
sudo nginx -t
```

If everything is ok, restart Nginx.

```bash
sudo service nginx restart
```

or

```bash
sudo systemctl restart nginx
```

### Get an SSL Certificate

If this is your first time running `certbot`, you will be prompted to enter an email address and agree to the terms of service.

```bash
sudo certbot --authenticator standalone --installer nginx -d example.com -d www.example.com --pre-hook "systemctl stop nginx" --post-hook "systemctl start nginx"
```

Provide your email and accept terms. Your cert will be generated.

If successful, you will be able to choose between enabling both http and https access or forcing all requests to redirect to https.

```bash
Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
-------------------------------------------------------------------------------
1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
-------------------------------------------------------------------------------
Select the appropriate number [1-2] then [enter] (press 'c' to cancel):
```

I suggest to choose option 2. Certbot will add automatically additional lines to your website config. Once complete you will get message:

```bash
-------------------------------------------------------------------------------
Congratulations! You have successfully enabled https://example.com and
https://www.example.com

You should test your configuration at:
https://www.ssllabs.com/ssltest/analyze.html?d=example.com
https://www.ssllabs.com/ssltest/analyze.html?d=www.example.com
-------------------------------------------------------------------------------

IMPORTANT NOTES:
- Congratulations! Your certificate and chain have been saved at:
/etc/letsencrypt/live/example.com/fullchain.pem
Your key file has been saved at:
/etc/letsencrypt/live/example.com/privkey.pem
Your cert will expire on 2018-09-12. To obtain a new or tweaked
version of this certificate in the future, simply run certbot again
with the "certonly" option. To non-interactively renew *all* of
your certificates, run "certbot renew"
- If you like Certbot, please consider supporting our work by:

Donating to ISRG / Let's Encrypt: https://letsencrypt.org/donate
Donating to EFF: https://eff.org/donate-le
```

### Auto Renewal

As Let’s Encrypt certs expire after 90 days, they need to be checked for renewal periodically. Certbot will automatically run twice a day and renew any certificate that is within thirty days of expiration.

To test that this renewal process is working correctly, you can run:

```bash
sudo certbot renew --dry-run
```

### Backup

Don’t forget to backup your keys. They are located here:

```bash
/etc/letsencrypt/archive/
```

## Alternative method

Everywhere where the above method doesn’t work you can try official, alternative method. It’s perfect for Debian 8 (Jessie).

Uninstall certbot (if installed):

```bash
sudo apt-get remove certbot
```

Download certbot-auto:

```bash
wget https://dl.eff.org/certbot-auto
```

Allow execute:

```bash
chmod a+x certbot-auto
```

`certbot-auto` accepts the same flags as `certbot`; it installs all of its own dependencies and updates the client code automatically.

Certbot has an Nginx plugin, which is supported on many platforms, and automates certificate installation.

```bash
sudo /path/to/certbot-auto --nginx
```

Running this command will get a certificate for you and have Certbot edit your Nginx configuration automatically to serve it. If you’re feeling more conservative and would like to make the changes to your Nginx configuration by hand, you can use the certonly subcommand:

```bash
sudo /path/to/certbot-auto --nginx certonly
```

Check if automating renewal works good:

```bash
sudo /path/to/certbot-auto renew --dry-run
```

Add cron task to autorenew cert:

```bash
0 0 * * 1 /path/to/certbot-auto renew --quiet --pre-hook "service nginx stop" --post-hook "service nginx start"
```

This will run renew at 00:00 on Monday every week with flag to silence all output except errors and another flag to restart Nginx service.

## Online generators

On [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/) and [CAA Record Helper by SSLMate](https://sslmate.com/caa/) website you can create configuration files automatically.
