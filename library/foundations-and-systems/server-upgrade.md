---
id: ckb-ce34774049b6
title: Server Upgrade
category: foundations-and-systems
format: article
language: en
tags: [bash, linux, log-analysis, privilege-escalation, threat-intelligence, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.93
---

# Server Upgrade

It’s hard to admit, but [0ut3r.space](https://0ut3r.space/) was running on Debian 9 (shame on me, on the 30 June 2022, Debian 9 “Stretch” went End of Life). A few days ago, I upgraded it to Debian 11. I thought it may be useful for someone to provide steps I did. Here it is, short article about upgrading 0ut3r.space from Debian 9 to Debian 11.

![Debian Upgrade](debian.jpg)

I guess, I do not need to remind people how important is to keep software and system up to date. All in all, I make money by entering where I shouldn’t, by using bugs in the old unpatched software.

If your server is running under Debian, you can use interesting tool - [debsecan](https://gitlab.com/fweimer/debsecan).

> The Debian Security Analyzer uses data from <https://security-tracker.debian.org/tracker/> to report vulnerable Debian packages installed on the current system.

As you can imagine results running this tool on Debian 9, and then after upgrade on 11, It is way much better now. Try it yourself. A lot of fun ;)

When you are updating system it is worth to follow path, going version by version. If you are on Debian 9, do not upgrade directly to 11. First go to 10, then 11.

But the main rule here is to do the backup before the upgrade :)

If you are using custom repositories, just disable them for the time of the upgrade, and setup correctly for the latest release after the whole system will be up and running again.

## Backup

I made backup of my system config files (where I made some changes), nginx configuration with virtual hosts, cron entry, custom scripts I am using for backups, certbot, tor, etc.

Always schedule a time for bringing back server if something goes wrong. Upgrade itself, depends on network speed and hardware you have, can take from 10 to 30 minutes, but if something goes wrong, you may need an hour to install clean server, configure it from scratch and then bring back services from backups.

## Version check

Next step is to check installed version and kernel, you can use commands below, and after each upgrade double check changes.

```bash
sudo cat /etc/os-release
sudo uname -a
sudo lsb_release -a
```

If you have limited disk size, clear the APT caches, this is optional, but can save you some space.

```bash
sudo apt clean all
```

## Custom repositories

I disabled my custom repositories, locates in `/etc/apt/sources.list.d/ ` and in `/etc/apt/sources.list`. To be honest I’m using only official Nginx repo, GoAccess, MariaDB and NodeJS. After upgrade you need to check what are new repos for each source and update it. Then enable it again and install updates.

## From Debian 9 to 10

Edit the file `/etc/apt/sources.list` using a text editor and replace each instance of `stretch` with `buster`.

Then go one bye one:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo reboot
```

During the process you may be asked to replace, or keep config files (default is to keep) and to restart services during the installation, which is also a good idea. If you would like to automate that, run above commands with option:

```bash
-o Dpkg::Options::="--force-confold" --force-yes -y
```

e.g.

```bash
sudo apt upgrade -o Dpkg::Options::="--force-confold" --force-yes -y
```

after reboot check installed version using command from **Version Check** step.

Cleanup system from unused packages:

```bash
sudo apt --purge autoremove
```

## From Debian 10 to 11

Edit the file `/etc/apt/sources.list` using a text editor and replace each instance of `buster` with `bullseye`.

Your source file should look like:

```bash
deb http://deb.debian.org/debian/ bullseye main
deb http://security.debian.org/debian-security bullseye-security main contrib
deb http://deb.debian.org/debian/ bullseye-updates main contrib
```

again same steps:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo reboot
```

after reboot check installed version using command from **Version Check** step.

Cleanup system from unused packages:

```bash
sudo apt --purge autoremove
```

## From Debian 11 to 12

Edit the file `/etc/apt/sources.list` using a text editor and replace each instance of `bullseye` with `bookworm`.

Your source file should look like:

```bash
deb http://deb.debian.org/debian/ bookworm main
deb http://security.debian.org/debian-security bookworm-security main contrib
deb http://deb.debian.org/debian/ bookworm-updates main contrib
```

again same steps:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo reboot
```

after reboot check installed version using command from **Version Check** step.

Cleanup system from unused packages:

```bash
sudo apt --purge autoremove
```

## Cleanup

Even after cleaning, some packages may still be there, check it:

```bash
# Debian 9
sudo dpkg -l | grep deb9
# Debian 10
sudo dpkg -l | grep deb10
# Debian 11
sudo dpkg -l | grep deb11
```

Remove them:

```bash
sudo apt purge <PACKAGE-NAME> -y
```

And that’s all. You have now lattes version of Debian. When new version will be available do same steps but change distribution codename to the new one. Also when you are using VPS, double check if you VPS provider already enabled new distribution from the server side. If you can see latest version of image for server reinstallation it means whole infrastructure is prepared for upgrade.

## Custom stuff

As I also have some other configurations I will put theme here too.

### Certbot

On Debian 9 my solution for cert was script from Certbot, but now it is just a package from snapd.

```bash
sudo apt remove certbot
sudo apt install snapd
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

To add entry to Nginx configuratuion and update cert:

```bash
sudo certbot --nginx
```

My configuration already have Certbot entries so I updated certs only

```bash
certbot --nginx certonly
```

To check if automatic renewal works run:

```bash
sudo certbot renew --dry-run
```

### NodeJS

NodeJS is easy to update:

```bash
sudo curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash - &&\
```

### GoAccess

```bash
wget -O - https://deb.goaccess.io/gnugpg.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/goaccess.gpg >/dev/null

echo "deb [signed-by=/usr/share/keyrings/goaccess.gpg arch=$(dpkg --print-architecture)] https://deb.goaccess.io/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/goaccess.list
```

### Ultimate Bad Bot Blocker

Additional interesting option is to install [Nginx Ultimate Bad Bot Blocker](https://github.com/mitchellkrogza/nginx-ultimate-bad-bot-blocker), please check the installation steps on the official GitHub repository. I am using it on my website for long time, and really recommend it.

## Thanks

From today I will keep system version up to date every time when official support will be close to the end. I promise. So around 2025 I will update server to Debian 13 :)

All security patches are always handled automatically by [Unattended Upgrades](https://0ut3r.space/2019/06/22/unattended-upgrades/).

PS: I added also custom clean and simple [error pages](https://github.com/denysvitali/nginx-error-pages). Check it here. [404](https://0ut3r.space/404).
