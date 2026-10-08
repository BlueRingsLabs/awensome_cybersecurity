---
id: ckb-4c225ffb53f6
title: Backup your data
category: general-technology
format: article
language: en
tags: [homelab]
summary: This article discusses personal data backup strategies, network-attached storage devices, and general data protection practices.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.5-flash-lite
  confidence: 0.85
classified_by: google:gemini-3.5-flash-lite@2026-10-08T00:14:28Z
---

# Backup your data

Few months ago I bought [Synology DiskStation DS720+](https://www.synology.com/en-global/products/DS720+). I was using Synology DS218j for about 5 years and wanted to buy something more efficient. This article is a small review and a reminder for you to backup your data. If you think about NAS, you care about your data, and you want to run virtual machines from NAS, read it. Unfortunately this article is not sponsored, no one pays me to say how cool Synology product is (which is a pity, although I recently got my first [coffee-donation](https://ko-fi.com/Q5Q320GFC), thank you Anton!). It also does not matter which company you choose. It always depends on your needs.

![types of people](backups.jpg)

I love the message from the image above. It can be also replaced with “there are two kinds of people: those who backup, and those who have never lost all their data”. I am the lucky guy that never lost data, but I always did a backup. Which I never had to use, but I checked from time to time to see if it worked.

When I started with a 600 Mb hard drive and the disc prices were out of space (a long time ago right after the dinosaur era), the backup ended up on a CD, and it was the most important documents few photos and other files that felt important to me. Then there were DVDs, so I could backup my music and much more photos. Then came the flash drive era, but for a time CD/DVDs were still more profitable, and USB sticks which liked often to broke. Once the disk prices started to become acceptable, I always had one disk in my drawer and updated my backup from time to time. Such solutions have never fully protected all my data, and time between backups made current files insecure. I was automating my solution by connecting the disk and configuring programs like [rsync](https://rsync.samba.org/) or [Rclone](https://rclone.org/) or [similar](https://alternativeto.net/software/rsync/). It was also necessary, to remove files, that are no longer important to me from the backup, to free up some space. Still, it was manual work which I had to perform repetitively. Then came the time of the cloud and software for synchronizing all devices, even those mobile. At that time, I was not a convinced of uploading my data to someone else’s servers. Today, I consider solutions such as [Dropbox](https://www.dropbox.com/) or [Google Drive](https://www.google.com/intl/en/drive/download/) to be safe, and reasonable for people who have no alternative, or are not technical. It’s better to create a strong password, enable two factor authentication and do an encrypted cloud backup, than not to do it at all. Just before I choose [NAS solution](https://en.wikipedia.org/wiki/Network-attached_storage), I set up my own server with [OwnCloud](https://owncloud.com/) software. Personal cloud, all devices synchronized on the fly and I finally had access to my data wherever I was in the world (of course, with a lot of security implementation). Solution also expensive, because you need another PC at home which is turned on 24h/7. Also keeping a server and backup at home is not the best solution, because if your house is flooded or burned down, or a thief steals everything, it doesn’t make sense. But let’s just say I’m not a big company going to lose millions and don’t need multiple locations for backup. Of course, the most important files, critical without which I would not be able to manage my digital (and sometimes real life), are thrown as an encrypted container on one of the private clouds that synchronizes with my NAS. You will now ask, what these secret files are? Nothing special, files such as a KeePass container with passwords, keys to various cryptocurrency wallets, important documents, electronic souvenirs, etc.

Well, we probably have the whole story already. Time to write about NAS.

Small box connected to the network, with installed hard drive (or 2 in my case) inside. Can work as a server for multimedia (photo, video, music, notes), backup, virtual machines, docker container, www, surveillance station, VPN, mail, proxy, office, Radius server and many more.

When many years ago I decided to choose a NAS, I did some research among the available solutions. I was mainly interested in the price and well-developed interface. The final choice was between [Synology](https://www.synology.com/) and [Qnap](https://www.qnap.com/). Difficult decision, most likely, regardless of the choice, the functionality would be the same at a similar price. A matter of taste. In order not to choose randomly, I decided to look for how many attacks and vulnerabilities appeared on the devices of both companies. Uncle [Google](https://www.google.com/), [Exploit-DB](https://www.exploit-db.com/) and [CEV-Mitre](https://cve.mitre.org/index.html) helped me review discovered vulnerabilities. At that time, there were more critical for Qnap. I also had a good feedback from my friend, from UK (thanks Yati!) who was using same Synology product I wanted to buy (Synology DS218j).

If we are in the topic of vulnerabilities did you hear about [QNAP ransomware attack](https://www.helpnetsecurity.com/2021/04/26/qnap-nas-ransomware/) and [AgeLocker Ransomware](https://www.qnap.com/en/security-advisory/qsa-21-15)? Here is also official info from [QNAP](https://www.qnap.com/en/security-news/2021/response-to-qlocker-ransomware-attacks-take-actions-to-secure-qnap-nas). If this is new to you, and you are the user of QNAP, make sure you read this and update your device.

Back to the topic. This year I bought new one DS720+. Why? Because I was interested in possibility of running [virtual machines](https://www.synology.com/pl-pl/dsm/feature/virtual_machine_manager) and [Docker containers](https://www.synology.com/en-global/dsm/feature/docker). Also I wanted something faster. DS218j was good for backup, for music and movies it was quite slow.

Here you can find [specification](https://www.synology.com/en-global/products/DS720+#specs).

So now maybe a few screenshots of configuration.

My storage pool is build from two WD RED PRO 4TB 7200 256MB CMR disks and connected together in RAID with [Btrfs](https://en.wikipedia.org/wiki/Btrfs) (just because it is required by virtualization) file system.

![Storage Pool](storage-pool.png)

Additionally I set up a SSD cache using ADATA XPG SX8200 PRO 1 TB M.2 2280 PCI-E x4 Gen3 NVMe also as a RAID1.

![SSD Cache](ssd-cache.png)

At the end 2 HDD and 2 SSDdrives used in this small box.

![Hard drives](hard-drives-in-my-NAS.png)

I use NAS for:

- Backup - All devices like laptops and smartphones synchronize most important folders and files to NAS.
- Network Drive - All other data is located on NAS and mapped as network share to laptops.
- Private Cloud - I am using [Synology Drive](https://www.synology.com/en-global/dsm/feature/drive). Same as [Google Drive](https://www.google.pl/intl/en/drive/), this app can be installed on PC or mobile phone, same options, same functions.
- Notepad - [Note Station](https://www.synology.com/en-global/dsm/feature/note_station). Synchronized notes, tasks and to do list on all devices. It is not perfect but works.
- Multimedia Server - [Audio Station](https://www.synology.com/en-global/dsm/feature/audio_station) for music, I have access to my music library on the PC and smartphone, something like personal Spotify. It also have [Video Station](https://www.synology.com/en-global/dsm/feature/video_station) app, I just watch videos from mapped drive, but with this app you can build your personal Netflix alternative :)
- [Docker containers](https://www.synology.com/en-global/dsm/feature/docker) - I run various Docker containers. This way you can easily extend possibilities of your NAS.
- [Virtual Machine Manager](https://www.synology.com/en-global/dsm/feature/virtual_machine_manager) - I run various virtual machines like Parrot OS or Kali Linux. You can browse your system through the web browser :)
- Download Server - Using extension called [Download Station](https://www.synology.com/en-global/dsm/packages/DownloadStation) my NAS can download torrents and other files for me. Like good old download mangers.
- VPN server - Nothing to add, I can connect to the server and use it like I would be at home.
- [Surveillance Station](https://www.synology.com/en-global/surveillance) - I have few IP cameras at home and when I am out, they are monitoring my home. Motion and sound detection record directly to disk. Thanks to this, I also have an overview of my apartment.
- Books library - I am using [Calibre](https://calibre-ebook.com/) as my eBook management tool. Library is located on NAS.

Yeah that’s probably all. Of course there is much more options to use like [e-mail server](https://www.synology.com/en-global/dsm/packages/MailServer), [www server](https://www.synology.com/en-global/dsm/packages/WebStation), [calendar](https://www.synology.com/en-global/dsm/packages/Calendar), [office](https://www.synology.com/en-global/dsm/packages/Spreadsheet) and [many more](https://www.synology.com/en-global/dsm/packages).

A little bit about security. Everything is set up to updates automatically (system, firmware and apps). Web interface is accessible from the Internet and only necessary ports are open. 2FA is enabled. Strong password policy and periodic password change is enabled. Firewall allows connection only from my location. Whole world is blocked. I allow connection from specific country only for time of my travel/business trip. Only connected to the VPN I have access to network shares. Admin account and some default accounts disabled/removed. I disabled aps and services I do not use. Antivirus software is installed on NAS. Disabled auto router configuration. I follow [Synology Security Advisory](https://www.synology.com/en-global/security/advisory) as [RSS](https://www.synology.com/api/rssfeed/security/en-global).

Yeah, that’s probably everything. I hope you enjoy.

So remember, do backups! On USB drive, CD/DVD, NAS, portable hard drive, [ownCloud](https://owncloud.com/) self hosted server, Google Drive, Dropbox, One Drive or any other alternative. Keep data in encrypted container on these places using for example [VeraCrypt](https://www.veracrypt.fr/code/VeraCrypt/) and passwords in offline password managers like [Keepass](https://keepass.info/). Always use two factor authentication everywhere it is possible. And check if your automated backup solutions works, whether the copies are creating correctly and whether you are able to recreate them. And do not keep backup of important data in one place, make backup of your backup in other location, because if your data center will look like this:

![OVH in fire](ovh.jpg)

and official communication from vendor is like:

![OVH info](ovh-suggestion.jpg)

you don’t want to ask similar questions:

![Disaster Recovery Plan](disaster-recoveryplan.jpg)

;)
