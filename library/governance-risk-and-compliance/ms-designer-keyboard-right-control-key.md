---
id: ckb-18d4852b9ee0
title: MS Designer keyboard right control key
category: governance-risk-and-compliance
format: article
language: en
tags: [tls]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.17
---

# MS Designer keyboard right control key

Sometimes simple things require complex solutions. Today’s article is sponsored by Right Control key.

Funny situation… some time ago I bought another keyboard, this time [Microsoft Designer Compact Keyboard](https://www.microsoft.com/en-us/d/microsoft-designer-compact-keyboard/8zhrtr7zcswq?rtc=3&activetab=pivot:overviewtab). (I tested so many keyboards in my life and spent fortune on them… but this is probably a story for separate article). To be honest this keyboard is awesome. I really like it. Additionally, to have a full set I also bought [Microsoft Number Pad](https://www.microsoft.com/en-us/d/new-microsoft-number-pad/8v4nh9q07xc8?activetab=pivot:overviewtab) (my wife is using num pad a lot, so when she finishes her stuff, I can always put that separate numpad to the drawer). In short, everything works prefect. It is small, very comfortable keyboard and very well designed. So what is so funny? Besides the wife screaming “it’s probably the hundredth keyboard, why do you need another one” it does not have a right control key.

![MS Designer Compact Keyboard](ms-designer-keyboard.png)

In place of right control there is a “Expressive Key”. It is a key which by default run [“emoji” window](https://support.content.office.net/en-us/media/cb2595f2-f45a-80dd-85fb-54e862c2ee8c.png). Yeah you read it correctly, EMOJI! Just in case you would like to have a box of your favorite emojis to use in seconds (I’m sorry if I offended anyone who actually uses it, you sic bastard!). Fortunately using [Mouse and Keyboard Center](https://support.microsoft.com/en-us/topic/f5b10905-7887-eedb-2f1c-d0737a36a3b2) app you can remap that key to [Office Key](https://support.microsoft.com/en-us/topic/using-the-office-key-df8665d3-761b-4a16-84b8-2cfb830e6aff) (another useless fancy key, unless I have again offended an MS Office expert who turns on MS Office with this button every morning) or [Application Key](https://en.wikipedia.org/wiki/Menu_key) (you used that key once in your life, for few minutes, when your mouse was broken and you had a critical need, to click right key, to display a context menu and you are born before 2000). As you can guess so far, there is no option to select in official MS app to choose to remap that key to the Right Control. In 21 century this sounds funny. It is even more funny when you Google phrase like [ms designer keyboard right control](https://www.google.com/search?q=ms+designer+keyboard+right+control&oq=ms+designer+keyboard+right+control&aqs=chrome..69i57.5832j0j4&sourceid=chrome&ie=UTF-8) or [change emoji key to ctrl in Microsoft designer keyboard](https://www.google.com/search?q=change+emoji+key+to+ctrl+in+Microsoft+designer+keyboard&sxsrf=ALiCzsZjUs68uL_FZYZ2ivFIktq3HOoEiQ:1651673621027&ei=FYpyYpCqAYHWkwWq3afoCQ&ved=0ahUKEwjQiN3bg8b3AhUB66QKHaruCZ0Q4dUDCA4&uact=5&oq=change+emoji+key+to+ctrl+in+Microsoft+designer+keyboard&gs_lcp=Cgdnd3Mtd2l6EANKBAhBGABKBAhGGABQAFgAYN8CaABwAXgAgAGwAYgBsAGSAQMwLjGYAQCgAQKgAQHAAQE&sclient=gws-wiz).

But why do you need a Right Control key? (for god sake who uses the right control key - now I’m offending myself and I apologize if I inadvertently felt offended). For example if you work a lot with virtual machines like the one in Virtual Box, the Right Control key is the host key.

> To return ownership of keyboard and mouse to your host OS, Oracle VM VirtualBox reserves a special key on your keyboard: the Host key. By default, this is **the right Ctrl key on your keyboard**.

So I press this button for almost last ten years in combination Right Control + F, just to turn on and off the full screen view :) and now, my new keyboard which I thought would be the best in the world and I paid for it around fifty bucks does not have a key I am using for ten years. This key is crucial for my existence.

A wise man will say, change the key combination in Virtual Box to another and live with it. An old, stubborn man like me will say, no.

Since, I think I’ve explained everything, I can safely move on to the most important part of this article, which is changing the emoji key to the right control. I’ll probably make this a separate headline… so here it comes.

## Change emoji key to ctrl in Microsoft designer keyboard

Welcome to my fascinating $50 keyboard key swap tutorial.

First. Install [Mouse and Keyboard Center](https://support.microsoft.com/en-us/topic/f5b10905-7887-eedb-2f1c-d0737a36a3b2) app. Run it and remap default Expressive Key to Application Key. Just like it is shown in the screenshot below.

![Expressive Key Settings](ms-designer-keyboard-app-key.png)

Well done. Now download and install (or run as portable) [AutoHotkey](https://www.autohotkey.com/) app.

## AutoHotkey v1 (deprecated)

Create file on your desktop called as you wish, in my example it is `rctrl.ahk`.

Edit this file and put some magic into it:

```bash
AppsKey::SendInput, {RControl Down}
AppsKey Up::SendInput, {RControl Up}
```

## AutoHotkey v2

Same as above, but for current developed AutoHotkey v2. Create file `rctrl.ahk` with content:

```bash
#Requires AutoHotkey v2.0
AppsKey::RControl
```

Save it, run it. Test it. You’re welcome!

You can run it manually or add to the AutoStart. Script is just waiting for the moment when the AppsKey (Application Key - the one you mapped using Mouse and Keyboard Center) is pressed and simulate the right control key. First line is when button is pressed and second when released.

If you need to update any of your own AutoHotkey scripts, check this awesome [converter](https://github.com/mmikeww/AHK-v2-script-converter/tree/master). It will help you convert scripts from version 1 to 2.

TBH it would be awesome if this functionality would be added in the future to the official Mouse and Keyboard Center. Because now it looks a little funny. I tried to ask Bill Gates to do it, but he wrote back that he no longer deals with such things. So maybe pass it on and someone will eventually add such functionality.

Thanks for reading, stay safe and lots of smiles, I would put here some emoji, but I remapped my emoji key… damn it.
