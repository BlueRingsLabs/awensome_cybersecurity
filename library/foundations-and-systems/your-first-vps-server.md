---
id: ckb-674c71e87b58
title: Your first VPS server
category: foundations-and-systems
format: article
language: en
tags: [bash, firewall, homelab, linux, privilege-escalation, tls]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.89
---

# Your first VPS server

The best practice to learn Linux server administration, is to setup and configure virtual Linux server on your local machine. Using [VirtualBox](https://www.virtualbox.org/) and any of [hundreds Linux distribution](https://distrowatch.com/). For the beginners [Debian](https://www.debian.org/)/[Ubuntu](https://ubuntu.com/) is recommended. [Redhat](https://www.redhat.com/) distributions and other [based on it](https://distrowatch.com/search.php?basedon=Fedora#simple), like [Centos](https://www.centos.org/) are more likely used in enterprise environments, but also have longer support. So decision is up to you, in what direction you would like to develop. But whatever you will choose, rules are the same and differences are small. Next step is to buy and setup your first [VPS](https://en.wikipedia.org/wiki/Virtual_private_server).

In this article I will describe how to configure default settings on cheap VPS server, to make it more secure and ready for happy usage.

![virtual private server](vps.jpg)

If you are looking some good and cheap VPS servers, to practice your skills, you can check from [LoweEndBox](https://lowendbox.com/). There are some interesting and tested by users, good price offers. In my experience, don’t take the cheapest one, and before you buy, read comments from other users, check server localization, terms of conditions and legal docs. It is good to have at least 1 CPU and 512 GB of RAM. Amount of bandwidth and disk size depends on what would you like to do with your VPS in the future. If this will be your private VPN, disk size doesn’t matter, but the bandwidth is what you want. If this VPS will be your backup server, then you need a lot of space. Remember that you will study on this server first, after that you will want to use the server for specific purposes. So do not choose the weakest offer and adapt it to what you would like to do with it later. Also consider to choose [KVM](https://en.wikipedia.org/wiki/Kernel-based_Virtual_Machine) based rather than [OpenVZ](https://en.wikipedia.org/wiki/OpenVZ). Even if you are not familiar with the topic of types of virtualization and this is your first VPS, choose KVM and you will be happy of that choice when you will be more experience.

All steps described below can be used in the same way on the local virtual machine. The only difference is that you will connect to the local machine and not the one located in the Internet.

When buying, you can choose the operating system, but you can also change it to what you want in the administration panel later. My suggestion is to choose always minimal image. Thanks to this, you have a clean small system that you can expand according to your needs. These images are usually with a “mini” suffix in the name.

For a long time you can also pay with Bitcoins from the purchase of a virtual server.

So, you have got your first VPS, with minimal system and your root password. Time to connect to it and mess up a little in configuration.

Remember, if you break something, try to fix it, undo your changes, look for code or error content on the web. As a last resort, you can always reinstall the system in the server management panel and start again. However, problem solving is the case when you will learn most. So analyze errors, read messages and fix issues with configuration.

## Connect

Use your terminal if you are on Linux or [Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)/[Kitty](http://www.9bis.net/kitty/#!pages/download.md) if you are Windows user.

To connect from terminal you should use command:

```bash
ssh root@VPS_IP_ADDRESS
```

In Putty/Kitty just provide your VPS IP address and hit connect. It is [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface) you will know what to do.

Provide your password, and you are in.

## Update system

Most important thing is to keep your server up to date. Now you will do it manually for the first time, later I will show you how to automate this process.

```bash
apt update && apt dist-upgrade
```

## Add user

It is no the best idea to work on [superuser](https://en.wikipedia.org/wiki/Superuser) account so you should create new user, and add it to the [sudo](https://en.wikipedia.org/wiki/Superuser) group.

### Install sudo

```bash
apt install sudo
```

### Create new user

```bash
adduser USER_NAME
```

Follow the steps on the screen. Next, add this user to sudo, so you will be able to execute commands like root user, with administration privilege’s.

```bash
usermod -g sudo USER_NAME
```

or instead of adding to the group, edit sudo config:

```bash
visudo
```

to edit configuration file, where you need to add on the list, under the `User privilege specification` another line next to the root.

```bash
USER_NAME ALL=(ALL:ALL) ALL
```

save changes and exit.

Don’t forget to re-login to make changes active.

## SSH configuration

Next option is to do not allow root login to your server. This is why you created a new user in previous step.

To do this you need edit ssh configuration file:

```bash
nano /etc/ssh/sshd_config
```

I am using [nano](https://www.nano-editor.org/) because it is my favorite text editor, but you can use whatever you like.
In this file you are looking for line `#PermitRootLogin no`. Remove `#` symbol at front of it and save the file.

It is also worth to change your default port from `22` to any other. A lot of bots/automated scanner and brute force scripts using this as a default.

Find line `Port 22` and change it to other value, for eg. `2299`. Save and exit.

To submit changes you need to restart your ssh service.

```bash
service sshd restart
```

## Login

Ok, now we are ready to login as a new user.

You can try login as a root to see that it is not allowed now, don’t forget to use new port you selected.

```bash
ssh root@VPS_IP_ADDRESS -p 2299
```

now login as your new user:

```plaintext
ssh USER_NAME@VPS_IP_ADDRESS -p 2299
```

you are in. Now all commands that need admin privilege’s should be executed with `sudo`, for example system update command now will look like this:

```bash
sudo apt update && sudo apt dist-upgrade
```

## Firewall

Now setup firewall, I already wrote an article how to do it: [UWF - Simple Firewall](../../../../2018/09/03/ufw-simple-firewall/index.html).

Before you enable your firewall make sure you allowed connection on your SSH port configured in previous step.

## Portsentry

Read and implement this [Portsentry - stelath scan detection](../../../../2018/03/28/portsentry-stealth-scan-detection/index.html) to protect your server from [port scans](https://en.wikipedia.org/wiki/Port_scanner). This step is optional as software is not develop anymore and other system hardening is better solution.

## Fail2Ban

Read and implement this [Fail2Ban - best Jail](../../../../2018/05/01/fail2ban-best-jail/index.html) to protect your sever from [brute force attacks](https://en.wikipedia.org/wiki/Brute_force).

## Automatic updates

It is good to patch server automatically, to have the latest and not vulnerable software. Read this article to set it up correctly: [Unattended-Upgrades](../../../../2019/06/22/unattended-upgrades/index.html).

## System upgrade

Keep an eye on your system version and when it’s close to end of life, just upgrade it. Using VPS provider panel or [system upgrade instruction](../../../../2023/04/25/server-upgrade/index.html).

## Recommended VPS for start

RackNerd - [1 GB KVM VPS](https://my.racknerd.com/aff.php?aff=9079&pid=923) - 10.60 USD per year
RackNerd - [2.5 GB KVM VPS](https://my.racknerd.com/aff.php?aff=9079&pid=924) - 18.66 USD per year
RackNerd - [4 GB KVM VPS](https://my.racknerd.com/aff.php?aff=9079&pid=925) - 29.89 USD per year
RackNerd - [6 GB KVM VPS](https://my.racknerd.com/aff.php?aff=9079&pid=926) - 44.98 USD per year
RackNerd - [8 GB KVM VPS](https://my.racknerd.com/aff.php?aff=9079&pid=927) - 62.49 USD per year

If any of the promotions end, let me know and I will update the links. More interesting VPS offer can be found [here](../../../../donations/index.html#VPS).

## The end

And that’s all, now you have your small and secure, cheap VPS server ready for new challenges :)
For example you can now setup your own:
[Web Server using Nginx, Maria DB and PHP](../../../../2018/11/05/debian-lemp-stack/index.html)
or
[Personal VPN server](../../16/vpn-on-vps/index.html)
