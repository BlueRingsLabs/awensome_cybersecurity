---
id: ckb-2e3c159cf87d
title: Cool selfhosted solutions
category: foundations-and-systems
format: article
language: en
tags: [containers, git, homelab, mobile, tls, vpn]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.99
---

# Cool selfhosted solutions

Currently, my NAS is set up as a Synology DS720+ with two 4TB drives in RAID 1 configuration, plus two 1GB M.2 drives for caching and 6GB of RAM. It is accessible via a Cloudflare tunnel. In the near future, I will set up own NAS using [Unraid](https://unraid.net/) + custom hardware, and I will describe the process step by step. Today, however, I will tell you about some cool open-source solutions using Docker containers that I have set up on my Synology NAS as an alternative to the Synology ecosystem.

![cool-selfhosted-solutions](cool-selfhosted-solutions.webp)

## Cloudflared

Official [client](https://hub.docker.com/r/cloudflare/cloudflared) for [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/), a daemon that exposes private services through the Cloudflare edge. Without it, no NAS has any reason to exist on the Internet <- personal opinion xD. While you can expose your NAS to the world, configure a firewall and limit access by location or IP, there is a better solution. While it is good to allow access only through a VPN, I believe that the best solution is a Cloudflare tunnel. No one knows or sees anything (from the INternet, no open ports, no other services), we have additional protection against attacks and we can set up Zero Trust to limit access by location. I highly recommend it to every NAS owner. And all of this is available on the free tier. Cloudflare sees traffic and metadata, so if that bothers you, add your own certificate.

## Jellyfin

It’s one of the best media management systems around. I use it for movies, TV shows, travel videos and music. You can also use it for books and photos. [Jellyfin](https://jellyfin.org/) is simple, efficient, and actively developed. If you are looking for an alternative, there is also [Plex](https://app.plex.tv/). I have used both personally, and Jellyfin seems lighter and more independent to me.

For me, this solution replaces both Synology DS Video and Synology DS Audio.

Additionally, I have the [finamp](https://github.com/jmshrv/finamp) app installed on my phone to listen to my music collection from Jellyfin. If you want to listen to music and watch videos from your server, there is also an official mobile app called [Jellyfin](https://play.google.com/store/apps/details/Jellyfin?id=org.jellyfin.mobile). If you search, you will find a lot of other apps that work with the Jellyfin server. For listening on your desktop, there is, for example, [Jellyamp](https://github.com/jellyfin-labs/jellyamp).

However, if any of you want to separate the video from the audio and create something dedicated to music, I recommend [Navidrome](https://www.navidrome.org/) plus [supersonic](https://github.com/dweymouth/supersonic) on your desktop and [Symfonium](https://symfonium.app/) on your phone (both also work with Jellyfin).

## Immich

For photos, only [Immich](https://immich.app/). Organising and storing photos has never been easier! Hmm, I sound like a salesperson! Immich has replaced Google Images and Synology DS Photos for me. I have the Immich app on my phone, which syncs my camera folder. This gives me a backup of my phone photos and my own independent library that only my family has access to.

## Paperless-ngx

I keep the most important documents in paper form in binders in a fireproof safe. I have a digital copy of all of them on encrypted NAS drives. Paper documents that are no longer valid, or that do not require a paper copy, and that are several years old, are shredded and only kept electronically. I recommend buying a shredder with at least a basic DIN 4 [certificate](https://en.wikipedia.org/wiki/Paper_shredder).

When you keep everything as documents in folders for years, it becomes difficult to find anything. That’s why [Paperless-ngx](https://docs.paperless-ngx.com/) is the ideal solution for document management. Not only can you easily upload documents to the database, but you can also scan documents using [your phone](https://play.google.com/store/apps/details?id=de.astubenbord.paperless_mobile) and extract text from them using OCR. Proper tagging of documents and extracted text allows you to find documents related to specific keywords or tags in seconds, and also automate tagging and actions based on extracted text. It is a good idea to keep an encrypted copy of these documents in one more place. I send it as an encrypted package to Proton Drive. Then, in the event of a fire/flood/war/tornado or simply damage to both drives, I still have a copy somewhere. This allows me to comply with the [3-2-1 backup rule](https://en.wikipedia.org/wiki/Backup).

This solution replaces the classic SMB folder for me. It can be an alternative to Google Drive and Google Scanner, as well as OCR from the MS Office suite.

## syncthing

I used to think that finding a self-hosted alternative to Google Drive would be complicated. Thanks to the [syncthing](https://syncthing.net/) project, it’s actually very simple. Here’s a quote from the website that sums it up best.

> Syncthing is a **continuous file synchronization** program. It synchronizes files between two or more computers in real time, safely protected from prying eyes. Your data is your data alone and you deserve to choose where it is stored, whether it is shared with some third party, and how it’s transmitted over the internet.

It is configured on a NAS, as well as on a Linux laptop, a Windows laptop, two phones and a tablet. This allows me to synchronise important files, such as the Keepass key database, unilaterally from the NAS to the phones, and to back up important files from all devices to the NAS. If I lose my laptop or phone, all my documents are on the NAS.

I use it as an alternative to Google Drive and Synology Drive.

Remember to encrypt all your device’s drives, whether it’s a phone or laptop.

## transmission

Docker with [transmission](https://transmissionbt.com/) is the perfect solution for downloading ISO images of well-known Linux distributions :) What more can I say, it’s just a web-based torrent client. Plus a few scripts for cleaning up junk after the download is complete and disabling seeding after the download.

## joplin

I mainly keep my technical notes and todo’s in [Obsidian](https://obsidian.md/) (you can synchronize your notes folder using syncthing, for example; I just back it up this way on NAS), but there are general or shared notes that are not related to IT and security, which I host using a container from [Joplin](https://joplinapp.org/). I also use apps on my phone and laptop. This gives me easy access to my own and shared notes. Joplin clients are lightweight, and editing notes is straightforward.

This solution replaces Synology DS Notes for me. (By the way, creating notes in it is tedious and formatting content is a headache). Markdown above all else!

## grocy

My wife loves [Grocy](https://grocy.info/). The slogan on the homepage sums it up perfectly: ‘ERP beyond your fridge.’ It lists the contents of your pantry, fridge and kitchen cupboards. It also automatically generates shopping lists based on low product levels and regular lists that you create yourself. It also includes a repository of household appliance manuals, a recipe collection integrated with product levels, a task list and reminders to replace device batteries. It’s a really powerful tool. Although you have to spend a lot of time initially entering your data, once you’re done, you simply have an app on your phone showing your current product levels and your shopping list.

You need to get into the habit of marking what you’ve used up, what you’ve bought and what you’ve opened. With your phone to hand and a tablet in the kitchen, it’s easy, just one click! You still need to take an inventory from time to time, but Grocy also has a feature that reminds you when products are about to expire. You won’t waste food by forgetting about items hidden at the back of the cupboard, covered by others. You can also help yourself by adding product barcodes: when you take a carton of milk, for example, you can scan the code to check the pantry stock or mark it as used.

## Ocular and Actual Budget

I keep track of my finances using a spreadsheet. You know, Excel will accept anything. Everyone hates Excel, but everyone uses it. [Ocular](https://github.com/simonwep/ocular) and [Actual Budget](https://actualbudget.org/) are two cool finance apps. Personally, I haven’t migrated to either of them yet. Ocular looks more like my Excel spreadsheet — the only feature missing for me to switch to this solution is a savings option — and Actual Budget is a powerhouse that probably offers more than I need. My simple Excel spreadsheet only contains basic expenses and savings. I don’t keep a complete income and expense ledger and I don’t scan every receipt. If necessary, I use the tools provided by my bank, such as the history or balance sheet functions. I want to keep an eye on my biggest expenses, such as bills, subscriptions, fuel and holidays, as well as tracking my savings and monitoring how they compare to my main expenses. If you know of any solution that will allow me to convert my spreadsheet into a self-hosted app, please let me know. If I can’t find anything better, I’ll migrate to Ocular. I looked at lots of other solutions, but these two were the best.

## kavita

I store my comics and books on a NAS via SMB, then load them into [Calibre](https://calibre-ebook.com/) on my laptop before reading them on a PocketBook reader. However, I have found the perfect solution for managing my library on the NAS. [Kavita](https://www.kavitareader.com/) is a fast and user-friendly way to browse and view your library online. Once you have configured your reader, you can download books directly from the server.

## unraid

Finally, I would like to mention [Unraid](https://unraid.net/). It’s simply an operating system for your own NAS. When I build my own NAS in the near future, I will choose this one. After spending many hours scrolling through the internet, I am certain that it is the simplest and most advanced solution for managing your NAS. I will add a few more virtual machines, migrate my current containers and their configuration along with the data, and add a VPN on [Wireguard](https://www.wireguard.com/) (I currently use [Tailscale](https://tailscale.com/)). I think I will then have everything I could dream of. According to my preliminary calculations, I need around $3,000 to finalise it, but I’m sure I’ll achieve it someday.

## Sum up

Thanks to my own NAS and cool open-source projects, I am less dependent on large companies and their potential misuse of my data or metadata. Even if you have a NAS from a specific manufacturer with its own software, it’s worth not limiting yourself to its ecosystem, as migration may become more difficult over time. Setting up your own servers and experimenting with creating your own cloud gives you more control over your data. I only use external companies for additional encrypted backup.

I also encourage you to support the creators of the projects you use, either financially or technically. In most cases, these are hobby projects. When I receive a donation for something I’ve created, I’m happier than when I see a big paycheque from my employer, even if it’s only pennies. Small donations motivate me and lift my spirits. I make donations, and if I can, I sometimes help fix a bug or translate a project. I often hear criticism such as, “Why pay for it when it’s free?” This tells me that the person has never created or shared anything.

When choosing a solution, check how often the project is updated and whether it is actively developed and maintained. Larger projects are more likely to survive or be taken over by the community if development ceases.

The downside to most of the projects mentioned in this article is that, even in 2025, they still do not have multi-factor authentication ([MFA](https://en.wikipedia.org/wiki/Multi-factor_authentication)) implemented. While the problem is somewhat solved by a VPN or a Cloudflare tunnel, an additional layer of protection would be welcome. Unfortunately, it is not always possible to implement zero trust from Cloudflare because mobile and desktop applications do not support it. However, if you only use the web interface, it is worth enabling it for more critical applications. Continue to use long passwords.

If you are the only technical person in the family and implement such a solution for all household members, remember to document the entire process and provide simple instructions for use and troubleshooting. If you are unavailable for some reason, it is important that your family members can quickly restore the NAS in the event of a failure. For example, provide instructions on what to do in the event of a power outage or if the NAS does not start up after a failure, or if the USB drive on which the Unraid is located fails (create a backup of the Unraid on another USB stick and include instructions on how to replace the USB). If they can’t do it themselves, they can always hire an IT company to fix the problem and help maintain the NAS based on their usage description and your documentation. It is easier to find a local IT company to fix issues with the NAS based on your documentation in the event of your death than it is to find a good necromancer to bring you back from the dead.

There are many other interesting projects, such as [NextCloud](https://nextcloud.com/), but I have only described the ones I use. Personally, I will also set up a mini mail server as an SMTP server for all of the above services, so they can ‘talk’ to me by sending various types of notifications. I will write about this soon.

I wish you all the best in configuring your own services!
