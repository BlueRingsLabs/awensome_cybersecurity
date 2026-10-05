---
id: ckb-28e18648660c
title: Windows security and privacy
category: cryptography-and-privacy
format: article
language: en
tags: [git, hardening, linux, privacy, tls, windows]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.43
---

# Windows security and privacy

I guess for this article I will be again hanged, burned at the stake and executed by firing squad at the same time, but fortunately comments are disabled, so all ugly words and curses will not affect me directly. Also, please, do not think this is a step-by-step guide to make your system secure. It is just a general overview of what to do, and where to start, to make Windows 11 more secure. Windows and privacy sounds like an oxymoron. Unfortunately, with each new release of this system it is getting more and more chatty, and not just with Microsoft anymore, but with servers from different companies.

![windows11](windows11.jpg)

Here is a [great video](https://www.youtube.com/embed/IT4vDfA_4NI) I found:

but it all started with [this message on Mastodon](https://grafana.social/@dee/110493068746671277/):

Please read the whole thread, as many great ideas were shared by much more clever people than me.

Over the years, I switched between Windows and Linux, because of hardware I was using and places where I was hired. So I understand the issue very well. I am not a fanatic of one or another system, I am of the opinion that each was built for something different, like different needs, environment and people. I have always sat on Linux because I find it safer than Windows, but more complicated and less user-friendly for non-technical people. On Windows most things work out of the box (and on Linux these days, pretty much the same) but you do not have a place for non-standard configuration and system modification. On Linux, you can modify pretty much everything, but it always takes some time and if you do not know how to do something, you need to spend hours with Google. That doesn’t change the fact that when I upgraded from the old Dell Vostro to the Dell XPS 2in1 Ultrabook, I had to switch to Windows whether I wanted to or not, because with the look of the laptop came limitations such as lack of support for a fingerprint reader or built-in camera. I liked Windows 98, XP and 10 and 11 is not perfect, but it’s an excellent system as far as Windows goes. From the Linux side, I love Ubuntu, Debian, Fedora, I’ve tried Arch (in various versions for dummies like EndeavourOS and other distributions no longer in development) but I’m too stupid for Arch. Last month, I configured a few corporate servers on Alma Linux. However, every time I installed a system, Linux or Windows, I had to do a little hardening. Just to feel safe and to feel that my privacy is mine. This is why Dee question on Mastodon is very familiar to me, and probably to each human on earth who cares about security and privacy.

## Have a plan

No matter if you are a Linux or Windows user, you are a user of any asset, with the system, and connection to the Internet. You store on that system data which is important for you. Make it secure, like you secure your house, car and life.

There is no golden rule and one guide for everyone to make Windows (or any) system secure. This is why, each user should perform the [own security plan](https://ssd.eff.org/module/your-security-plan). Based on that, make hardening of the system. Different people have different needs, do different things, and store different data.

- What do I want to protect?
- Who do I want to protect it from?
- How bad are the consequences if I fail?
- How likely is it that I will need to protect it?
- How much trouble am I willing to go through to try to prevent potential consequences?

Additionally check the [Seven Steps To Digital Security](https://ssd.eff.org/module/seven-steps-digital-security).

- Knowledge is Power anchor link
- The Weakest Link
- Simpler is Safer and Easier
- More Expensive Doesn’t Mean More Secure
- It’s Okay To Trust Someone (But Always Know Who You’re Trusting)
- There is No One Perfect Security Plan
- What’s Secure Today May Not Be Secure Tomorrow

These suggestions are general, but you should start with a plan. Also, you need to take off your tin foil hat over the head, because it won’t work. I had to take off mine, because I had to find a compromise between functionality, safety and convenience. This is why I always estimate the risks and additionally place a small amount of trust in the service providers I use. For example, I have my own encrypted NAS not plugged directly into the network where I keep my super secret data. But I also have Google Drive, and sometimes I also use One Drive, and I keep less sensitive data there. This is because I believe Microsoft/Google engineers do a good job and my data is safe there. If you are a non-technical person, and have no knowledge about how to configure your own secure storage, you should trust Microsoft and Google in that case. If you just say Google and MS are pure evil and keep your data just on hard drive without any encryption or backup, you are doing it wrong, as your data is more secure on “their” storage. On the other hand, of course, you can assume that everyone is bad and not trust anyone, but then your life will consist of constantly configuring something that someone else did a long time ago and probably much better than you. Even I, with my knowledge, I’m afraid to expose my NAS directly to the internet because I know I could make a mistake, or miss something. And I see how often bugs appear in the system of this NAS provider. My whole security setup is nothing when the bug is in a system that I did not write or audit. That’s why I connect to a VPN at home to access the NAS. It would be more convenient and quicker to go straight to the NAS, but that’s how I assessed the threats and configured it that way. If something can’t be protected, add another layer of security to it.

Now that we have the idea, the foil hat is on the desk next to us, and we want a secure Windows 11, what should we do?

## Ready solutions

The lazy solution is to install (and trust it) one of the apps dedicated to helping users secure the system. On Windows machines where I do not store too much sensitive data, or I do not hack the world, I use O&O, but there are a few of them (all apps work with Windows 10 and 11):

- [O&O ShutUp10++](https://www.oo-software.com/en/shutup10)
- [W10Privacy](https://www.w10privacy.de/english-home/)
- [BloatyNosy](https://www.builtbybel.com/apps/bloatynosy)
- [SophiaApp](https://github.com/Sophia-Community/SophiApp)
- [WPD](https://wpd.app/)
- [WindowsSpyBlocker](https://crazymax.dev/WindowsSpyBlocker/)
- [Hard_Configurator](https://github.com/AndyFul/Hard_Configurator)
- [Sadcoy](https://github.com/Jisll/Sadcoy)

Which one is the best? I have no idea. Does all cover the same options? No. Is using all of them at once is ok? No. The cool thing is that most of them have an option to save configuration, and for example, after each Windows update you can reload configuration from the file to make sure that when something was changed during the update, it is again configured in your way.

Yes, you have read it correctly, it is not the rule, but confirmed information, that each bigger Windows Update can change your system settings, or add software or functionality you never wanted to. So you can spend a week tweaking your system, and then someday in the future some of the changes will be overwritten by a system update. Sadly, there is no question like in the Linux during the update: *Do you want to replace or to keep your configurations files?*

Checking the software listed above is also good for people who are getting back to Windows from Linux after many years, to understand and see what changes have taken place, what the focus of these applications is, what options they offer, what is switched on and off these days. This will make it easier to plan what you want to modify yourself. Even if you don’t use these applications, a list of their options can be a good cheat sheet.

## Scripts

Another treasure trove of knowledge is GitHub and various types of scripts. Unfortunately, trust should be limited in this area, and we should not use random scripts from the Internet to secure our own system without a thorough analysis of what they do. Fortunately, the community around such solutions is large, the code is open, and anyone with the right knowledge can take a look at what works and how it works. If you don’t know anything about coding or system commands, definitely don’t use a niche solution, look for one that has a large community of trusted and active developers and users around it. Each of the script should have described source code, and it’s mostly based on PowerShell scripts. If you are not and expert/developer, you can easily go for each line, read the comment, and Google command/check PowerShell documentation, to verify if it will do what the author described in the comment.

Here are some scripts:

- [Privacy Sexy](https://privacy.sexy/)
- [Win Debloat Tools](https://github.com/LeDragoX/Win-Debloat-Tools)
- [Debloat Windows 11](https://github.com/kdpuvvadi/debloat-windows11)
- [Debloat Windows 11](https://github.com/cramaboule/Debloat_Windows11)
- [win11tweak](https://github.com/kyaulabs/win11tweak)
- [BoxStarter](https://gist.github.com/ElJefeDSecurIT/014fcfb87a7372d64934995b5f09683e)

The downside of such scripts is that they are built for specific people for specific reasons. Often launching them involves turning off everything the author had in mind, not necessarily what we would have wanted. As with apps, it’s worth checking out what these scripts do to build your list, or even your own script based on theirs. It always makes things a little easier. Instead of building something from scratch.

Also, as you can see, most of the scripts are dedicated for some special system builds, as with every build you can get new stuff, and script may not work with the older or newer one. As some of them might not be very well documented, you need to go line by line and verify what it is doing.

## Security Benchmarks

Last but not least, you can follow security benchmarks. This is the most difficult and time-consuming option, but the results are truly wonderful. Not only do you secure the system according to the standards implemented in companies and large corporations, but you do it according to the guidelines of security experts. In a company it’s easier because you build policies and push them out to computers, at home, you have to go through everything one by one, you can automate it, but you still have to, read and understand it first and, as usual, adapt it to your needs. The pros of this is an in-depth understanding of the various mechanisms of the operating system and all sorts of options and their impact on the system, security or privacy.

Go and check the list of [CIS Benchmarks here](https://downloads.cisecurity.org/#/). You can read about it on [MS site too](https://learn.microsoft.com/en-us/compliance/regulatory/offering-cis-benchmark).

Download the one named “*CIS Microsoft Windows 11 Stand-alone Benchmark v2.0.0*“

![CIS Microsoft Windows 11 Benchmark](winbenchmark.png)

Open it and find that you need to read **1257** pages to audit your system and make it secure :) Why does the responsibility for privacy and security lie with the user and not with the supplier? We are the ones who have to spend hours configuring the product to meet the privacy and security requirements, which can be destroyed by a single system update.

In general, you could have a full time job to analyze every update, and Windows connection to modify settings to have better privacy and keep your tool or script up to date with all features. And also, you need to trust other people’s scripts and tools that they are doing the same. Would be cool to see a tool or script based on CIS Benchmark. I found [this](https://learn.cisecurity.org/build-kits). But it’s a paid solution and probably more useful for business.

And again, you can spend hours days weeks to set up everything and with the next Windows update everything can be changed, I personally used scripts to remove unwanted components (uninstall from PowerShell examples) and O&O with saved configuration. Then I always after each update recover the saved config, to make sure nothing has changed.

I asked ChatGPT about my concerns:

**I am using CIS Benchmark for Windows 11 and I am curious if it is possible that changes implemented by me, based on CIS Benchmark can be overwritten by any updates from Windows Updates during the system update?**

*Yes, it is possible that changes you make to your system based on the CIS (Center for Internet Security) benchmark for Windows 11 can be overwritten by updates from Windows Updates during a system update. When you apply updates to your operating system, they often include patches, bug fixes, security updates, and sometimes even changes to the system settings or configurations.*

*If the updates from Windows Updates include changes that conflict with the settings you’ve applied based on the CIS benchmark, the updates may overwrite your changes, and your system could revert to the default settings or settings defined by the update. This is a common occurrence during system updates, as Microsoft aims to ensure the security and stability of their operating systems.*

*To minimize the risk of your changes being overwritten, you should keep track of the updates you install and their potential impact on your system settings. Additionally, it’s a good practice to review the changelogs of updates to see if any of them might conflict with the CIS benchmark configurations you’ve applied. After installing updates, you should recheck and reapply the CIS benchmark settings if necessary.*

*In situations where you want to maintain strict adherence to the CIS benchmark, you may need to delay or selectively install certain updates to avoid conflicts. However, keep in mind that security updates are critical for maintaining the security of your system, so balancing security updates with adherence to the benchmark is essential.*

*Remember that managing system configurations and updates requires careful consideration, and it’s crucial to weigh the benefits of updates against any potential impact on your system’s security and stability.*

BTW, should we trust ChatGPT? Do you trust AI? Where the heck is my tin foil hat!

Never mind.

One of the cool things is that CIS Benchmark has a great Summary Table you can use as a checklist. You can even build your own checklist based on your security and privacy needs.

![summary](summary.png)

An alternative to CIS Benchmark are [Security Technical Implementation Guides (STIGs)](https://public.cyber.mil/stigs/downloads/). Or instead of alternative I should rather say supplementary? You can use online STIG viewer to [check suggestions for Windows 11](https://www.stigviewer.com/stig/microsoft_windows_11/).

Again, go one by one of 253 findings and audit your system.

![windows-stigs](windows-stigs.png)

## Third party apps

After some time from the installation, you have a secured system, without any bloatware, disabled telemetry with all security suggestions enabled. Antivirus and firewall are protecting your system. Now it’s a time to use proper tools. Install them, configure and harden.

What did you think? A secure system is nothing if you use shitty apps installed in the OS. Additionally, it would be good if you read the Privacy Policy, Disclaimers, and Terms of Service of each app you are using to make sure that the app developers or company behind it cares about your privacy.

So, get back to CIS and STIG Benchmarks and follow instructions for your favorite’s Web Browser…

![CIS Benchmark for Web Browser](cis-browsers.png)

…and Google other good practice’s for communicators, music streaming apps, social media, mail clients, image editors etc.

Look for apps and alternatives in places like:

- [Prism Break](https://prism-break.org/en/)
- [Privacy Test](https://privacytests.org/)
- [Privacy Tools](https://www.privacytools.io/)

Don’t forget about your BIOS or any firmware configuration for other devices plugged to the network.

## Network devices

When you finish with the apps, take a look at hardening your network devices, printers, routers, access points, IoT (smart fridge, doorbell camera, surveillance system) and mobile phone. Everything connected to your network or installed on your smartphone can bypass the best protected operating system installed on your computer.

And it all started with installing Windows, remember? And it is, after all, one big food chain of devices plugged into the network, connected to you as a person. Also remember, it doesn’t matter whether it’s Windows (1257 pages in CIS Benchmark), or Linux (Debian family Linux 504 pages), or macOS (402 pages) or Fedora family Linux (736 pages). It’s all about the operating system itself.

## Audit

After all, when you are a happy user of a secure operating system, with apps and configurations to make your privacy better, and network with whole assets after proper hardening, do not forget to perform an audit of everything from time to time, and keep an eye of changelog before updating anything.

Follow news, add a few security sources to your RSS reader to know about data leaks, changes in privacy policies, abuses of privacy by large organizations.

## Updates

Keep updated everything. System, apps, firmware, mobile phone system. Read the change log before updating. If the app or system is not directly exposed to the internet, or the update is just related to features or bug fixes and not a security patch, postpone the update for a few days. Sometimes updating a new feature breaks some security. If something is outdated, not developed anymore or abandoned, check for an alternative, buy a new device, migrate to something similar.

## Some other advices

- Encrypt everything, phone, hard drive, USB drive.
- Use strong, random, non-repetitive passwords. Generate them and store in offline passwords managers.
- Remember only 2, different, long passphrase. One used for password manager and the other for the system login.
- Use MFA everywhere it is possible to enable, avoid SMS, use authenticator app or hardware key.
- Make your social media profiles private, visible only to you and your close friends/family/coworkers. (Or avoid social media at all. Nobody cares about your photo from expensive holidays in a warm country, or your newborn ugly child)
- Do not upload anything to the Internet that you would not like to be leaked someday.
- Think before clicking.
- Do not buy not certificated devices, like some non brand Chinese phones or routers, from AliExpress.
- During installation (system or any app), carefully review and customize privacy settings. Opt for the most privacy-centric options available.
- Enable Windows Hello or a strong PIN for secure authentication.
- Configure BitLocker or a suitable encryption solution to secure your data.
- Check and configure Windows Defender for real-time protection and periodic scans.
- Review and adjust Windows Firewall settings to control inbound and outbound network traffic.
- Carefully manage app permissions for access to your device’s features (camera, microphone, etc.).
- Set up Telemetry options to your comfort level, while considering the trade-off between data sharing and system improvement.
- Configure app permissions in the Privacy settings to control data access for individual apps.
- Leverage the Microsoft Store for apps, and be cautious when installing apps from third-party sources.
- Explore Windows Package Manager (winget) for streamlined app installation.
- Set up regular backups using Windows’ built-in tools or a third-party solution.
- Familiarize yourself with recovery options in case of system issues.

I guess many other security experts, hackers and privacy enthusiasts would add much more, but these are just the basics, and my opinions. Always verify information from the internet, for example, double check stuff I wrote here to make sure I didn’t try to lower your security by mistake or lack of knowledge in some field.

At the beginning, all that stuff I write above can look scary and painful. The same applies to learning new habits, there is no longer an automatically saved password in the browser, you need to open the password manager, and it will enter the password for you. Once you develop good habits, everything else will come easier and safer. Just like in the past, my father constantly shouted “don’t slouch”, thanks to which I have a good straight figure and at my age I look good compared to hunched peers. But that’s a topic for another article about hunched computer scientists. And you, in what position were you bent the entire time you read the article? Straighten the fuck-up! Now!

PS. Imagine now everything from the beginning, with [tin foil hat](https://en.wikipedia.org/wiki/Tin_foil_hat) on the head. Easier to stay disconnected.
