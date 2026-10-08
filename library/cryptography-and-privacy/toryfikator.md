---
id: ckb-068a3fa975da
title: Toryfikator
category: cryptography-and-privacy
format: article
language: en
tags: [anonymity, linux, networking, python]
summary: The author introduces Toryfikator, a simple Python script designed to route all system traffic through Tor on Kali Linux.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.5-flash-lite
  confidence: 0.9
classified_by: google:gemini-3.5-flash-lite@2026-10-08T00:14:21Z
---

# Toryfikator

When testing hidden services on the Tor network, I often use [torsocks](https://support.torproject.org/glossary/torsocks/), but sometimes I need to [torify](https://linux.die.net/man/1/torify) all traffic; you can use [Whonix Gateway](https://www.whonix.org/wiki/Whonix-Gateway) for this, but you can also use simple [iptables](https://en.wikipedia.org/wiki/Iptables) rules (like I ever understood how to make them, lol). [Parrot OS](https://parrotsec.org/), for example, has an [anonsurf](https://parrotsec.org/docs/tools/anonsurf/) solution. Several similar solutions have been developed for Kali like [kali-anonsurf](https://github.com/Und3rf10w/kali-anonsurf), [kalitorify](https://github.com/brainfucksec/kalitorify) or [ToriFY](https://github.com/Debajyoti0-0/ToriFY) but some don’t work, some are not further developed, some are quite extensive, and I also wanted to learn something new, so I created the simplest solution I could think of, which was a simple Python script. Because why not create another solution [when others already exist](https://xkcd.com/927/).

![Dragon Eats Onion](dragoneatsonion.webp)

Btw, occasionally I do some coding, and since there’s already some weird stuff in my [GitHub repository](https://github.com/h0ek?tab=repositories), I decided to create a new category. Since my programming skills are limited to scripting, copy-pasting and modifying, rather than being a real programmer, this category will have a name that reflects my skills ([devving](../../../../categories/devving/index.html)). In future, you will find all the unusual pseudo-programmes I write in this category. I guess [x-resize](../../../../2024/12/26/auto-resize-x-screen-for-kali-on-kvm/index.html) should now also be in this category, but for the sake of the SEO I’ll leave it where it is.

But back to the topic. I created the [Toryfikator](https://github.com/h0ek/toryfikator) Python 3 utility for routing all system traffic through Tor on Kali Linux (this is not a tool for anonymity!). As usual, I launched my favorite development environment, ChatGPT… xD never mind.

Check out the official [Toryfikator GitHub repository](https://github.com/h0ek/toryfikator) for all the details. I would like to achieve something like [anonsurf](https://parrotsec.org/docs/tools/anonsurf/) by Parrot in the future with this project, where there would be a nice GUI and more options, but that is a distant dream for now.

The script and the article were written as a prelude to the next one, which will appear soon and cover hacking — *pah!* — unethically, to test the security of hidden services on the Tor network. Or rather, how and why it tests those services.

Thank you for your attention and have a nice day!
