---
id: ckb-9898ae1a0451
title: Cheap Crypto Deal
category: ai-security
format: article
language: en
tags: [ai, api-security, blockchain, python, red-team]
summary: An author describes using ChatGPT to automate the creation of a cryptocurrency exchange rate comparison tool using PHP and API orchestration.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-26b-a4b-it
  confidence: 0.8
classified_by: google:gemma-4-26b-a4b-it@2026-10-08T00:29:19Z
---

# Cheap Crypto Deal

Someone might think, “what has this man come up with again”. I sometimes purchase the pro version of ChatGPT and test its capabilities. As I’ve been doing the [SANS SEC565](https://www.sans.org/cyber-security-courses/red-team-operations-adversary-emulation/) course recently (highly recommended) and I slowly need to prepare for the exam, in the meantime I wanted to do something to help me relax and not think about RedTeaming. The strange thing is that I relax from studying by doing other mental work. As you can probably guess, I don’t feel relaxed. Well, back to the topic. I bought ChatGPT again for a month and tested the o3-mini-high version (very cool, I recommend it) and had the site orchestrated, which is a price comparison of cryptocurrency exchanges on sites where I have referral links. A simple affair, a page made in PHP, which is a form in which the user selects the value he wants to exchange, the source currency and the target currency. When the button is pressed, the backend queries the API of any implemented page that exchanges cryptocurrencies and returns the result in a table. The table is sorted according to the best offer. In addition, I have added icons, and the status of KYC risk and whether the refund is without KYC and a referral link.

You can test the result [here](https://cryptodeal.cheap/) as a normal domain and on the Tor network as a [hidden service](http://lp7lxv6tkk4zepitwmf2uo3pzypvmwgglrzhdofekjswjpday7qemgqd.onion/).

![cheapcryptodeal](cheapcryptodeal.webp)

It may not be a masterpiece, and there are a few bugs and options to work on, but it reasonably works. If you visit my blog, you know that I created the [crypto swap](https://github.com/h0ek/crypto-swap) and [crypto debit card](https://github.com/h0ek/crypto-cards) lists and then based on that I made the [swap.cab](https://swap.cab/) website. I wanted to have a comparison engine for this, which I built with myself in mind, but also to eventually implement it on Swap Cab (damn, I need to put this all together in one simple page).

However, I mainly wanted something that I could use to speed up checking where I could currently exchange crypto with the least loss. I happen to juggle cryptocurrencies or just use them for purchases and I like to lose as little as possible on this (I recently apologised to Ethereum because gas is no longer so expensive and it is faster than Bitcoin, so I am using it again, what a shame that [Monolith](https://monolith.xyz/) died).

Ahh it’s been a long time since there have been so many topic changes and new threads within a sentence. Sorry, that’s how it is when you have a million ideas a second, haven’t written anything for a long time and additionally want to tell everyone everything at once.

Okay, I’ll try to digress less. It all started when I was eight years old and my mother… just kidding!

I am not a programmer, I am a pentester and ethical hacker, and soon to be a certified red teamer. I can write simple scripts and automations, but I can’t write applications or websites. When I need to do something, I use off-the-shelf open source solutions and adapt them to my needs. I’m more of a Stack Overflow and Google kind of guy. But now I have ChatGPT! I can break down applications to find holes in them to get what I want, and I know that if I knew how to code, I would definitely break through more security. Well, but what do we have AI for? Not just to write malware for me, but to automate my little goals. Well, we already know that I needed a comparison of my favourite crypto exchanges. I will now show you my methodology for working with the GPT chat. You can do the same with the free 4o model and see the results.

First, I describe the general aims of the project and what I want to achieve:

> General project description and initial assumptions
>
> - My new project Checp Crypto Deal allows users to compare cryptocurrency exchange rates between different exchanges based on each exchange’s API.
> - It presents a list of the best deals with reflinks and information on KYC requirements.
> - Download Floating Rate Values
> - The form allows the user to select the cryptocurrencies they wish to exchange. The drop-down list loads BTC, ETH, DOGE, XLM, LTC, BCH, XMR and these cryptocurrencies are associated with each API. For the selected cryptocurrency pair, the website sends queries to each API. The results are sorted by the cheapest offer.
> - The list contains the name of the exchange (value from the configuration), the icon (value from the configuration), the float value (information from the API), the KYC information (value from the configuration), whether the refund is with KYC (value from the configuration) and the reflink (value from the configuration).Then I add a bit about backend and frontend:

> Backend:
>
> - Pure PHP (no JS)
> - Retrieves data from each exchange’s API
> - Checks exchange availability for a given cryptocurrency pair
>
> Frontend:
>
> - HTML dynamically generated by PHP
>
> How it works:
>
> - User fills in a form
> - Enters amount, selects source currency and destination currency
> - Results are displayed in a table on the page, sorted from cheapest to most expensive.

I add a bit about appearance, how everything should be displayed, colours, css styles, icons, files, folders, tables, etc.

> The look of the site should be simple, clear and adaptable to changing sizes, which means it should display well on mobile phones. The position on the page is in the middle.
>
> In the middle is the title in the form of logo.png, which is also a link to the main page, then a field for selecting the source and destination cryptocurrencies, and next to the source a field for entering the exchange value.
>
> The button below is to load the list of exchangers when clicked to show the results. As described above, the Exchanger icon (from config), Name (from config), Floating Rate (from API), KYC Risk (from config), KYC Refunnd (from config) ‘Go exchange’ button (from config). The link will open the reflink in a new window.
>
> After re-entering the values and selecting the currencies, the user can click ‘Show Results’ again and a new table of results will be generated. At the bottom of the table the time and date of generation should be indicated. It should also be noted that the values are for the time of generation and may change slightly after generation on the target page, but will not differ much from the generated results.
>
> At the very bottom of the page, in the footer, is the information Made by Hoek (which is a link to [https://0ut3r.space](https://0ut3r.space/) opening in a new window) with ChatGPT.

Then I add a few more details, e.g.

> - The site should be modular so that individual elements of its operation can be changed in dedicated files when it comes to repair or improvement or expansion.
> - Appearance in a dedicated css file.
> - The site will be hosted on a server with Nginx and PHP version 8.4.
> - The site code, page and comments in the code must be in English.
> - Take security into account when writing the code (for example, check that input fields can only be filled with rate values). Adopt other good secure coding practices for html and php.
> - I want to have my defined values for the listings in a file so that I can expand it in the future and additional information is taken from it in addition to what I retrieve from the API.
> - Icon (in icons folder), Name of exchanger, KYC risk (options green dot low.png, yellow dot medium medium.png and red high high.png and anonymous.png icon if the exchange is anonymous.), No KYC refund (Yes or No, it is about whether the refund is without KYC), Reflink.
> - Size of icons 15x15px
> - Below the list and generation time there should be a legend describing what is on the list, that e.g. icons high.pmg low.png etc. and next to it a description.
> - The different APIs should also have their own configuration, so I will add new files for each API. We will start with two providers, FixedFloat and SimpleSwap.
> - If a value is not available from the API or the API does not match, the fields in the table should show n/a and what is taken from my file can normally be displayed.
> - The same is true for the exchanges whose API I have not yet added.
> - And here is the API documentation for the first two: <https://api.simpleswap.io/>, <https://ff.io/api>
> - Based on the documentation, add the first two APIs. We’ll add the next ones later once we’ve checked the performance on the two that the whole site works.

I then feed the values into the config file in the format icon, name, KYC, refund, reflink.

> fixedfloat.png, FixedFloat, Low, No, [https://reflink](https://reflink/)

I provide the API keys. At the end I write:

> Do your magic and create such a project for me with all the files and code.

And that’s it, I wait for all the files to be generated, in the meantime I set up the [web server on a virtual machine](../../../../2023/09/24/test-web-server/index.html). I create the directory and file structure according to what chatGPT gave me and fire up the site. Here something is not working, here something is crashing, so I analyse the logs, make corrections and just chat more to get a hint. I concentrate on solving one problem at a time. Sometimes I fix something manually when I see what is wrong (I know a bit about it), after each change I paste the fixes or just the whole file into the chat and say this is the latest version from now on. If something doesn’t work very well and I’m stuck, I’ll ask for help debugging it and add the errors to the logs. If there is a problem with an API, I just add all the documentation manually and in most cases this solves the problem. Sometimes I manually query the API to see what the result is so I can suggest fixes.

In the end, I have a product that works. I test it for security (that’s what I know) and bugs. I buy another cheap, weird domain, set up an onion domain, set up another VPS and web server, and show the world by blogging about the next weird thing I do for unknown reasons.

In fact, I wanted to show you that if you have some complex projects and you type everything like I did above, it will neither work immediately nor after a long chat without basic knowledge in programming, debugging, analysis, administration.

I have the basics of web development, I know how API works, I have the basics of web server configuration, I have the basics of Linux administration, I have the basics of hosting and configuring hidden services, I know how to analyse server, php and web logs for errors, I know what those errors mean and how to fix them.

I could probably write such a site myself, with my basic skills it would probably take 2 months or even a little longer. With GPT chat I did it in 4 days (after work, for fun). The project is not perfect, there are some bugs. I have to work on the Altquick API because sometimes it shows nonsense depending on the crypto selection (I have to correctly map the values returned by the API with what is displayed in the table for the cryptocurrency data). Some APIs do not return a value if the user does not match with the value between the minimum and maximum that is supported for a given currency (for these exchangers I have to get the min and max value and provide in the table the min or max value depending on what the user enters in the form). Not all exchanges allow cryptocurrency pair data, instead of showing “n/a” I can add the information “pair not supported”. Some exchangers have a limit on API requests, the limits are quite large, but it can still be optimised so that at some point I do not lose the value in the table in case I will have a lot of visitors). And many other weird things I have on the list to fix.

What has all this given me? I learned a lot. It made it easier for me to find the best exchange. I had some loose material for an article on my blog (because I put the complicated ones aside for later). I took my mind off the course I was doing every day to prepare for the SEC565 exam.

And maybe I showed someone that AI can help and do a lot, but only if we know what we want to achieve, have basic knowledge and know what the answer should look like (at least approximately). AI is a better and faster Google and Stack Overflow.

I am looking forward to the future and new versions of ChatGPT. I will be able to do less and faster what I have to do manually now. Or learn to automate what I don’t understand today.

PS.: This is all for the money anyway, you need to go trade your crypto with my reflinks. NOW!

PS.1: I have already fixed some of the things I mentioned in the article when I set up the web server in production :D
