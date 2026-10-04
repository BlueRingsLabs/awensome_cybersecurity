---
id: ckb-c00d3e6e4578
title: Add Onion domain to your website
category: application-security
format: article
language: en
tags: [anonymity, bash, privilege-escalation, threat-intelligence, tls, web-security]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.3
---

# Add Onion domain to your website

This entry will show you, how to configure [onion domain](https://en.wikipedia.org/wiki/.onion) for your website. This will allow access to your website through the [Tor](https://www.torproject.org/) protocol, using .onion domain. [Facebook](https://en.wikipedia.org/wiki/Facebookcorewwwi.onion) did something similar. I decided that my site will also be available on the Tor network. You can reach 0ut3r Space using it standard address which is [http://0ut3r.space](http://0ut3r.space/) and now also using
[http://reycdxyc24gf7jrnwutzdn3smmweizedy7uojsa7ols6sflwu25ijoyd.onion/](../../../../index.html)
To open onion address you need to use [Tor Browser](https://www.torproject.org/projects/torbrowser.html.en).

![Onion](onion.jpg)

## Installing Tor

Edit sources.list:

```bash
sudo nano /etc/apt/sources.list
```

and add Tor repository ([here](https://www.torproject.org/docs/debian.html.en) you can find list of actual Tor repositories)

```bash
deb https://deb.torproject.org/torproject.org stretch main
deb-src https://deb.torproject.org/torproject.org stretch main
```

Add repository keys:

```bash
gpg2 --recv A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89
gpg2 --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add -
```

Update package list and install Tor:

```bash
sudo apt update && sudo apt install tor
```

## Tor configuration

Edit Tor configuration file to look like this (don’t forget to open HiddenService port on your firewall, in below example it is set to 8123):

```bash
SocksPort 9050
RunAsDaemon 1
HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServiceVersion 3
HiddenServicePort 80 127.0.0.1:8123
```

You can also use old version 2 or version 2 and 3 in same time but it is [recommended](https://trac.torproject.org/projects/tor/wiki/doc/HiddenServiceNames) to use next-gen onions version 3.

Now restart Tor:

```bash
sudo service tor restart
```

In folder `/var/lib/tor/hidden_service/` you can find your onion domain private key.

Inside file called `hostname` you will find your onion domain address.

## Nginx Configuration

Next to your virtual host file create another one for onion configuration.

```bash
server {
        listen 127.0.0.1:8123;
		}

        root /var/www/yourwebsite;

        index index.html index.htm index.php;

        server_name youronionaddress.onion;

}
```

Modify your hidden service port and root folder for your website. Server name should be set to your onion domain. By default, this file should look the same as the configuration of your page except the above changes, so don’t forget about php configuration and other setting you are using on your server.

Save this file and create link to activate this configuration.

```bash
sudo ln -s /etc/nginx/sites-available/youronionconfiguration /etc/nginx/sites-enabled/youronionconfiguration
```

Test Nginx configuration

```bash
sudo nginx -t
```

and if everything is ok restart web server

```bash
sudo service nginx restart
```

Now your website is visible in both networks. As standard domain in Internet and as onion domain in Tor network. You can find more about configuring Onion service in [official documentation](https://www.torproject.org/docs/tor-onion-service.html.en).

## Onion Location

Since 8th of July, it is possible to inform your visitors, that your website have onion address. Please read more on the official Tor Project blog in post [#MoreOnionsPorfavor: Onionize your website and take back the internet](https://blog.torproject.org/more-onions-porfavor).

Whole process of adding Onion Location is described in [documentation](https://community.torproject.org/onion-services/advanced/onion-location/).

In short, you need to add header to your server configuration.

### Example for Nginx.

Edit website conf:

```bash
sudo nano /etc/nginx/conf.d/<your-website>.conf
```

and add line:

```bash
add_header Onion-Location http://<your-onion-address>.onion$request_uri;
```

### Example for Apache

```bash
Header set Onion-Location "http://your-onion-address.onion%{REQUEST_URI}s"
```

Thanks to that if someone visit your website using Tor Browser with standard domain, will be informed that you have onion domain too.

Here is example how it looks like for 0ut3r.space

![onion available](outerspace-onion-available.png)

Nice, right?
