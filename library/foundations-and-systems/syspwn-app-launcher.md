---
id: ckb-2d1a2945c9a6
title: SysPwn - App Launcher
category: foundations-and-systems
format: article
language: en
tags: [homelab, python, red-team]
summary: The author describes the development of a simple Python-based application launcher designed to manage and execute portable security tools from a USB drive.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.9
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:16:24Z
---

# SysPwn - App Launcher

Everyone knows that I am not a programmer, but yesterday was a holiday in my country and I was doing some tidying up of my notes and todo lists, and one entry was quite old and I thought, ok, it is probably time to complete this task. Holy moly, but how does that relate to programming? Let’s start at the beginning.

![coding](coding.webp)

When I was a young and handsome IT specialist supporting end users in a company, like any such specialist I had a pen drive full of applications to fix computer problems. And of course the immortal [Hirens Boot CD](https://www.hirensbootcd.org/). To make things easier for myself, after a few years I also created a menu of links to portable applications that I could launch from the USB to speed things up. There’s even a trace of this on alternativeto.net, the tool was called [Hoek’s Tools](https://alternativeto.net/software/hoek-s-tools/about/). Funny, because it was just a menu for third party applications. But it was used by various people in my company, colleagues and even 8 other people around the world ;) The tool died when I stopped solving users’ problems and started creating them. I mean, I started working closer to cybersecurity. And today, as a red teamer and ethical hacker, I do more breaking than fixing. Fixing is what others do after I break.

I had to replace my normal memory stick with one with a write-block option because I was increasingly using tools that were detected as malicious. I then bought a [Kanguru FlashBlu30™ Lightning-Fast USB3.0 with Physical Write Protect Switch 8GB](https://www.kanguru.com/products/kanguru-flashblu30-usb3-flash-drive). Cheap and good. Every time I plug a USB stick into a computer with AV, it doesn’t spoil my toolkit by automatically deleting it. No need to copy the tools every time.

But what about programming? Not so fast. I was tidying up my notes and one of the tasks from the distant past was to create an application in any programming language. USB app launcher.

Well, I started with [AutoHotkey](https://www.autohotkey.com/), which has little to do with programming, but I couldn’t manage it, it is possible to build a GUI and automate things there, but for an app launcher it was probably too much. Anyone who reads my blog knows that I’ve been trying to learn Python for years, and I find it difficult. Or to tell the truth, I am damn lazy. Fortunately, when I don’t know what to do, my friend ChatGPT comes to the rescue. We chatted together yesterday and managed to write a simple application runner in Python.

The intention was simple. I have an `apps` folder on a USB stick where I drop various applications into folders with different categories. My launcher scans this folder and subfolders on startup and creates a list of apps and categories. Each `exe` file is treated as an app name and added to the menu. This allows everyone to build their own set of tools. There is also a search box at the top to make it easier to search the long list. I manually added an entry to run a PowerShell console that runs in the `apps` folder on the USB stick. Also, in the `cfg` file, you can exclude `exe` files that you do not want to be included in the list. For example, the [System Informer](https://systeminformer.sourceforge.io/) application (formerly known as [Process Hacker](https://processhacker.sourceforge.io/)) has an auxiliary `exe` file in its folder in addition to the main application, which would also appear in the list without exclusion. Or you may simply want to hide an application for some other reason. I decided not to put the icon in the taskbar because if I pull out the memory stick in an emergency and forget to close the application, it leaves a visible trace in the form of a taskbar icon.

Pros:

- I completed a 10-year-old task on my list.
- I have a dream and simple application launcher from my USB.
- I learned new things in Python.

Cons:

- My wife was unhappy that I spent half the day in front of the computer.
- I still don’t know how to code in Python xD

If you want to see the result of the work I encourage you to check out the code on [GitHub](https://github.com/h0ek/SysPwn). I called it SysPwn. Because I use it for just such purposes ;)

Remember to document your work so that it is easier to return to and develop in the future, and it is also worth sharing your solutions with others who may find them useful.

Example screenshot: (more in the code repository).

![SysPwn](syspwn_main_window_menu.webp)

Have a great day!
