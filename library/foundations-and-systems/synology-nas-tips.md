---
id: ckb-e610a8cb2733
title: Synology NAS tips
category: foundations-and-systems
format: guide
language: en
tags: [bash, dns, homelab, linux]
summary: This guide provides practical configuration tips for Synology NAS devices, including package management, cron job scheduling, and automating dynamic DNS updates via Cloudflare.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.9
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:16:22Z
---

# Synology NAS tips

You may or may not remember my article [Mount Synology NAS in Linux](../../../../2019/07/23/mount-nas/index.html). Being the lucky owner of a Synology DS720+, I sometimes do some interesting things on it besides the standard stuff. And since this site is also my online notebook, I have collected all the things I have configured on my NAS in this article. This article will surely grow in the future. For now I will start with what I have.

![Synology Nas Setup](synologynassetup.webp)

## Mount Synology NAS in Linux

I covered this in a separate article -> [Mount Synology NAS in Linux](../../../../2019/07/23/mount-nas/index.html). Useful if you want to permanently mount Synology network shares in a Linux system.

## Additional packages

It wasn’t until recently that I discovered a repository of packages created by the Synology community. With this repository, you can easily extend the packages available in the Package Centre.

Installation is quite simple:

1. Log into your NAS as administrator and go to **Main Menu → Package Center → Settings** and set Trust Level to *Synology Inc. and trusted publishers*.
2. In the **Package Sources** tab, click **Add**, type *SynoCommunity* as **Name** and *<https://packages.synocommunity.com/>* as **Location** and then press **OK** to validate.
3. Go back to the **Package Center** and enjoy SynoCommunity’s packages in the **Community** tab.

More details on the official website: <https://synocommunity.com/>

## Cron on a Synology NAS

The standard [cron](https://en.wikipedia.org/wiki/Cron) command as in any Linux does not work. So `crontab -e` is not there.

To modify crontab and enable deamon, you must first become a root:

```bash
sudo -i
```

You obviously already have ssh access enabled and you are connected to ssh :) Tip: never expose SSH to the world, only allow connections from the local network.

Edit crontab:

```bash
nano /etc/crontab
```

add your stuff there and restart the cron deamon:

```bash
synoservice -restart crond
```

## Automatic updating of IP address via Cloudflare

This can be useful if you have your domain associated with the IP address of your NAS and the IP address changes dynamically.

My NAS is at home and the ISP changes the IP of my router quite often, especially after reboots and updates. Access to my NAS is restricted by a firewall and I access it from my domain using the web interface with 2FA. I also use the domain to connect to my VPN. I used to buy a permanent address, but why would I need the extra cost when I can automatically update my dynamic address for my domain.

First, sign up for a free [Cloudflare](https://www.cloudflare.com/) account. Add your domain (example.com) to Cloudflare. This process involves changing your domain’s DNS servers to Cloudflare’s DNS servers.

The API token needs to be created. Login to your Cloudflare account. Go to **My Profile** > **API Tokens**. Click on **Create Token** and select **Edit zone DNS**. Configure the token to access your domain (example.com), and generate the token. Make a note of the API token, as you will need it to configure the DNS update script.

Make sure that curl is installed when you ssh to the NAS: `curl -V`.

Create a script that automatically updates the DNS record in Cloudflare. Below is a sample bash script (you can keep the script in your home directory). I use [nano](https://www.nano-editor.org/), my favourite console text editor to edit files, it is not installed by default. You can install it from the Synology Community repository, the package that contains nano is called [SynoCli File Tool](https://synocommunity.com/package/synocli-file) (adding the Synology Community repository is described earlier in this article).

Create bash script `nano dns.sh`:

```bash
#!/bin/bash

# Cloudflare configuration
CF_API_TOKEN="YOUR_API_TOKEN"
CF_ZONE_ID="YOUR_ZONE_ID"
CF_RECORD_ID="YOUR_RECORD_ID"
CF_RECORD_NAME="nas.example.com"

# Get and save the current IP address
CURRENT_IP=$(curl -s http://ipv4.icanhazip.com)

# Get a saved IP address
RECORD_IP=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$CF_RECORD_ID" \
-H "Authorization: Bearer $CF_API_TOKEN" \
-H "Content-Type: application/json" | jq -r '.result.content')

# Check if the IP address is different
if [ "$CURRENT_IP" != "$RECORD_IP" ]; then
    echo "IP address has changed. Updating the DNS record..."
    curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$CF_RECORD_ID" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data "{\"type\":\"A\",\"name\":\"$CF_RECORD_NAME\",\"content\":\"$CURRENT_IP\",\"ttl\":120,\"proxied\":false}"
else
    echo "The IP address is up to date."
fi
```

Replace `YOUR_API_TOKEN` with your Cloudflare API token. Replace `YOUR_ZONE_ID` with the zone identifier for your domain (you can find this in your Cloudflare dashboard). Replace `YOUR_RECORD_ID` with the DNS record identifier for your subdomain (you can also find this in your Cloudflare dashboard). The script will check the current external IP address, compare it with the current address in Cloudflare’s DNS and update the record if it is different.

One more thing, I did not find the `CF_RECORD_ID` element directly specified like the other values anywhere in the Cloudflare dashboard. However, this can be checked in a simple way, just run it:

```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
-H "Authorization: Bearer $CF_API_TOKEN" \
-H "Content-Type: application/json"
```

This will return a string containing the ID.

The next step is to run the `dns.sh` script from time to time. To run the script automaticaly as a cron task, edit `nano /etc/crontab` and add something like this:

```bash
*/10    *       *       *       *       root    /var/services/homes/user/dns.sh > /dev/null 2>&1
```

It will execute script at every 10th minute. You can adapt this to your own needs.

## Firewall

These are just general tips to make your Synology NAS more secure.

My firewall blocks almost everything. I only allow access to the VPN from around the world, so once I connect to the VPN hosted on Synology, I can access other things on Synology, so when I connect to the VPN, it is like being on my home network. I only have port 80 and 443 on the US network so I can renew my LetsEncrypt certificate ([there is no list of IPs to whitelist on firewall](https://community.letsencrypt.org/t/multi-perspective-validation-geoblocking-faq/218158), there is a workaround but I haven’t tested it yet), and port 5001 just for the country I live in so that I can access the NAS via the web interface, and so that Synology Android apps like Drive, Note, Audio can connect via https to the NAS. I have disabled the admin account and any other account requires additional token authorisation. When I am out of the country I connect to the VPN or temporarily add the country as a permitted country to connect to. I also have a backup VPN which, if I connect from its address, also has an entry just in case, so an additional one IP address is therefore allowed on the firewall. I also allow everything when I am connected to the Synology VPN, so the entire subnet 10.8.0.0 and the entire home subnet 192.168.1.1. The last rule on the list is to deny everything from everywhere.

In short, this solution allows me to

- Use Android apps and web interface in my country
- Renew my LetsEncrypt certificate
- Allow me to connect to the VPN from anywhere in the world and feel like I am in my home network
- Do not block anything inside when I am connected via VPN
- Have a backup VPN that allows me to access the NAS as if I were using Synology Hosted VPN.
- A password and 2FA protected process.

## Video Station alternative

The latest [Synology update removes Video Station](https://www.reddit.com/r/synology/comments/1f2kunt/synology_video_station_no_longer_available_on_dsm/), which can be replaced with [Plex](https://www.synology.com/pl-pl/dsm/packages/PlexMediaServer) (or a slightly more complicated implementation, but still possible with [Jellyfin](https://jellyfin.org/docs/general/installation/synology/) or [Emby](https://emby.media/synology-server.html)). I chose Plex and it works fine, I just disabled all the Plex features to act as a my media server.
