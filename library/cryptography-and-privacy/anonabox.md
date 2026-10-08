---
id: ckb-9c0599918006
title: Anonabox
category: cryptography-and-privacy
format: article
language: en
tags: [anonymity, hardware, privacy, vpn]
summary: An overview and personal experience using the Anonabox, a portable Tor router designed for privacy and anonymity.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-26b-a4b-it
  confidence: 0.95
classified_by: google:gemma-4-26b-a4b-it@2026-10-08T00:32:31Z
---

# Anonabox

*Update: After some time I can see that not much is happening when it comes to updating or developing firmware and software for this device. The packages are deprecated and their manual update is quite complicated and does not necessarily work as it should. Using the device below may put you at risk of compromising security. If you are here, because you are looking for cool solution to have a Tor router, please read my article about [Tor router on Raspberry Pi](https://0ut3r.space/2020/05/16/tor-router/). Treat the article below as a fun fact.*

Few months ago I bought [Anonabox](https://www.anonabox.com/index.html) device. I ordered the [Fawkes](https://www.anonabox.com/buy-anonabox-fawkes.html) model, but due to the lack of product in stock I received the [Pro](https://www.anonabox.com/buy-anonabox-pro.html) model at the same price. It was a pleasant surprise and a nice gesture from the manufacturer. Contact with the seller was nice and at a high level. The package also came to me quickly.

![Anonabox](anonabox.jpg)

Anonabox is a mini portable Tor router. If you are looking for a ready-made solution that will connect you to the Tor network, then you should be interested in this device. Of course, you can buy a router that allows you to upload, e.g. [DD-WRT](https://dd-wrt.com/), [OpenWRT](https://openwrt.org/) or [pfSense](https://www.pfsense.org/) and configure them yourself. It is not easy and when you make a mistake you will not be secured up the way you would like. By buying an Anonabox router you will trust that the company’s experts did it right.

> Anonabox is an innovative hardware company focused on providing internet security, privacy and freedom for all users. Utilizing the Tor Network and additional VPN services, our affordable devices help to conceal web browsing, emails, file sharing, and other digital entrails that typically follow web activity. Founded in 2014 after a successful crowdfunding campaign, Anonabox is now offering multiple devices aimed at a wide variety of users who wish to protect all aspects of their online activity.

Small size, possibility of using Tor network and additionally VPN connections enable safe surfing on the network. Configuration of the device is simple and possible to do using a graphical interface (web interface).

![anonabox](anonabox_package.jpg)

I use device as a second router in my house, as a gateway to the Tor network. If you’ve ever used the [Whonix](https://www.whonix.org/) system and the Whonix-Gateway virtual machine, Anonabox is such a physical equivalent of this system.

In this configuration, Anonabox connects to the WiFi router in my home to gain access to the Internet, after which it torify this traffic and makes it available to other devices. Thanks to this, I have two networks available. Normal and the one whose traffic is directed through the Tor network.

![anonabox](anonabox_open.jpg)

I always use a VPN connection when traveling. Since I have an Anonabox router, I also uses it to safely use the network, e.g. in a hotel. At the airport or during a visit to a restaurant, connecting a laptop to a VPN is much faster than building a small secure infrastructure. However, when I am in a hotel on vacation or business trip and for a few days my phone, or the other two laptops non-stop connect to the hotel network, this solution is handy. I just configure the VPN connection on the Anonabox router to link it to the hotel wifi and all my devices connects to the Anonabox. This way I know that all my traffic is always secured on every device.

![anonabox](anonabox_stickers.jpg)

Anonabox also has the ability to connect to the network via an internet cable, it can also work in [bridge](https://bridges.torproject.org/) or tor node and exit node modes. It enables connection with popular VPN providers as well as to my own VPN server (although I haven’t succeeded yet). It also allows you to host your own website with onion domain ([hidden service](https://2019.www.torproject.org/docs/onion-services.html.en)).

If you are interested, [click here](https://www.anonabox.com/compare-routers.html) to see the comparison of available devices.
