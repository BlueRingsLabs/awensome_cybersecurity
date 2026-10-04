---
id: ckb-315dc51b9e20
title: Windows Defender is enough, if you harden it
category: security-operations
format: article
language: en
tags: [cloud, hardening, malware, powershell, tls, windows]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.91
---

# Windows Defender is enough, if you harden it

This article is not intended to convince you to abandon your current antivirus solutions. In this post I would like to share my observations and ways to improve the effectiveness of Defender.

You don’t need to buy expensive antivirus software. If you are a standard user, surfing the web, you don’t want to install additional software (eg. which can slow down your PC), or you just have other better things to buy, you can definitely use antivirus software built into your Windows operating system. There is no perfect solution, and no mater if you install free or paid antivirus, you can always be infected, if you do not use your own brain. Sometimes it is easier to break a person than their computer security. Then even the most expensive solution will not help.

Unfortunately, no one checks anyone’s skills before buying the first computer or smartphone. If you want to drive a car, you need to get a driving license. If you want to shoot a gun, you need to get a permit. If you want to connect to the internet and interact with it, you don’t have to do anything. Reading some comments on random websites I guess you don’t even need a brain. Every Internet user these days should be careful, check links, verify sources and be aware. Anyone, even a security specialist, can have a weaker day, so somewhere in the background there should be a program running to protect your computer and data.

There are people who boast that they never had an anti virus program. There are some who think free solutions are crap. There are also those who write that you must have an antivirus program and preferably the most expensive one with all functions. In my opinion, you can have whatever you want. But if you have Windows and a built-in antivirus program, which isn’t the worst, better have it turned on and brag about never having to intervene than one day cry about your data being encrypted.

![defender](defender.jpg)

[Windows Defender](https://www.microsoft.com/en-us/windows/comprehensive-security) is simple, but very good, built in antivirus and threat protection solution in modern Windows OS. It has account, app & browser control, firewall and network protection and it helps you to keep your device secure. Interface of the software is a little bit different than standard antivirus software GUI you are familiar with. There aren’t too many configuration options here either, but all the available switches are well described.

Defender is not only used at home, but many large companies use Defender in conjunction with Sentinel (SIEM) and ASC as their primary protection. I myself had the opportunity to work in one of these companies and this solution had very good results. Because who, if not Microsoft alone, can defend his system best. Of course, together with colleagues from work, we have often laughed that all global companies that use Defender in production are beta testers (global testing environment) for Microsoft products. As many times as the administration interface changed without any announcement, or the product names evolved, once it was Microsoft Defender, then Windows Defender, sometimes you looked at Defender consoles, then it was Defender for Endpoint and then Defender ATP and Defender Security Center etc. There was a time when I didn’t know where I was logging in and what was its name, I was just analyzing the alerts under the currently working link :)

But today, let’s focus on Defender for the home user. It does not have additional functions that are offered by other commercial solutions, but what it does is enough. However, it is worth enabling some additional functions that are not available from the graphical interface.

The effectiveness of many antivirus programs is tested by sites such as [AV Comparatives](https://www.av-comparatives.org/vendors/microsoft/) or [AV Test](https://www.av-test.org/en/antivirus/home-windows/windows-10/december-2021/microsoft-defender-4.18-211616/). You can check which antivirus is “the best”. If you take a moment to analyze it, you’ll see that it all changes month to month and year to year. In the past, Defender had poor marks, now it’s better, and so are the products of other companies.

So as I said, the interface is not the best and turning on some features that will improve Defender’s performance requires a bit of messing around with the system. This, for sure, deters some users and discourages those who want to install something and everything has to be done for them. But even paid solutions tire users with pop-up windows asking what now, what next, and how you would like it to work. Thanks to this, they learn the user’s behavior, which is sometimes a several-week process of making decisions and clicking on buttons, to shut down forever and notify you only in the event of an emergency.

## Local group policy settings

[Local group policy](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/dn265982(v=ws.11)) setting is the key to make it better and harden Defender. Local Group Policy Editor is available only in pro/enterprise edition, but you can add it to the Home version of Windows too. If you do not want to enable this editor you can also change options described below in PowerShell chapter of this article. Anyway read this chapter to understand how it works, then it will be easier to change options using PowerShell.

Create `gpedit-enable.bat` file and put inside code (it works for Windows 10 and 11).

[Hey man! Just not a bat file](https://news.ycombinator.com/item?id=30580444#30581094). Yup, that’s true, random guy, random code, random website, ensure that the code is safe, click me. Sound like creepy scenario, fully agree. This is not a mandatory step and code was borrowed from [here for Windows 11](https://www.itechtics.com/enable-gpedit-msc-windows-11/) and [here for Windows 10](https://www.itechtics.com/enable-gpedit-windows-10-home/). Check links for more details. [If you trust the links I serve](https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Manwithtinfoilhat.jpg/800px-Manwithtinfoilhat.jpg) :) Either way, a big plus for being vigilant.

In any other case Google yourself solution for enabling Local group policy editor.

```powershell
@echo off
   nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
   REM --> If error flag set, we do not have admin.
   if '%errorlevel%' NEQ '0' (
   echo Requesting administrative privileges…
   goto UACPrompt
   ) else ( goto gotAdmin )
   :UACPrompt
   echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
   echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
   "%temp%\getadmin.vbs"
   exit /B
   :gotAdmin
   if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
   pushd "%CD%"
   CD /D "%~dp0" 
 pushd "%~dp0"
 dir /b %SystemRoot%\servicing\Packages\Microsoft-Windows-GroupPolicy-ClientExtensions-Package~3.mum >List.txt dir /b %SystemRoot%\servicing\Packages\Microsoft-Windows-GroupPolicy-ClientTools-Package~3.mum >>List.txt
 for /f %%i in ('findstr /i . List.txt 2^>nul') do dism /online /norestart /add-package:"%SystemRoot%\servicing\Packages\%%i"
 pause
```

Save it. Run it. Restart your PC and then run `gpedit.msc`. Once editor is open you can continue with next steps.

The code above is fancy version of checking admin rights and then enable policy editor.

### Enable MAPS

Microsoft Advanced Protection Service (MAPS), enhances standard real-time protection by cloud-delivered protection and next-generation technologies.

Steps below will allow you to Join Microsoft Advanced Protection Service (MAPS), Configure Block at First Sight feature, Configure local setting override for reporting to Microsoft MAPS, Send file samples when further analysis is required, Select Cloud Protection level in Windows Defender and Configure extended cloud check.

In Local Group Policy Editor navigate to: `Computer Configuration > Administrative Templates > Windows Components > Windows Defender Antivirus > Maps` or `Computer Configuration > Administrative Templates > Windows Components > Microsoft Defender Antivirus > Maps` depends on your Windows version. Open `Join Microsoft MAPS` entry and change it to `Enabled`. In options you can choose from dropdown menu MAPS level. Basic or Advanced Membership. (You can read about both in Help.) I choose `Advanced Membership`.

![MAPS gpedit](gpedit.png)

Configure Block at First Sight feature

Then open `Configure the "Block at First Sight" feature` entry and also choose `Enabled`. Do the same for `Configure the local setting override for reporting to Microsoft MAPS`. In `Send File Samples when further submission is required` choose option based on your preferences. It is also very well described. I suggest `Send safe samples`.

![MAPS gpedit](gpedit_maps.png)

Next go to `Computer Configuration > Administrative Templates > Windows Components > Windows Defender Antivirus > MpEngine` or `Computer Configuration > Administrative Templates > Windows Components > Microsoft Defender Antivirus > MpEngine`. Edit entry `Select cloud protection level`, enable it and set options to `High blocking level`. This option will make Windows Defender Antivirus more aggressive when identifying suspicious files. Last entry to edit is `Configure extended cloud check`, enable it and set time to `50`. The typical cloud check timeout is 10 seconds. To enable the extended cloud check feature, specify the extended time in seconds, up to an additional 50 seconds.

Reboot PC.

## Ransomware protection

This can be enabled from GUI. Just type `Windows Security` in Menu Start, go to `Virus & Threat protection` and at the bottom of that screen select `Ransomware protection` and click on `Manage ransomware protection` and select enable on `Controlled Folder access`.

## PowerShell

Use PowerShell… yes, to setup some options in Defender you need to use PowerShell. Run PowerShell as Administrator and type `Get-MpPreference` to check current Defender configuration.

### Signature update

Set `SignatureUpdateInterval` to every 1 hour.

```powershell
Set-MpPreference -SignatureUpdateInterval 1
```

Also it is worth to force update new signatures before each scan starts.

```powershell
Set-MpPreference -CheckForSignaturesBeforeRunningScan 1
```

Read about other parameters on the [official documentation](https://docs.microsoft.com/en-us/powershell/module/defender/set-mppreference?view=windowsserver2022-ps&viewFallbackFrom=win10-ps) and tweak them as you wish.

### Enable MAPS

If you skipped MAPS setup using Local Group Policy Editor you can see the same options in PowerShell.

`MAPSReporting`, 0 - disabled, 2 - enabled threats and additional data will be sent to MS (Advanced Membership), 1 - only basic data (Basic Membership). Set this option using `Set-MpPreference`. This is the same for every other options described later.

`SubmitSamplesConsent`, 0 - Always prompt, 1- Send safe samples automatically, 2 - Never send, 3 - Send all samples automatically.

`CloudBlockLevel`, described in documentation, in section above I suggested option 5 - High blocking level.

`CloudExtendedTimeout`, set to `50`.

### Potentially unwanted software

This can be enabled from GUI, but as you are already a pro Defender user you can use PowerShell for this too.

`PUAProtection`, specifies the level of detection for potentially unwanted applications. When potentially unwanted software is downloaded or attempts to install itself on your computer, you are warned.

## GUI

Of course rest of the options you should review is available in graphical interface of Windows Defender. Most important is part with `App & browser control`, `Reputation-based protection`, `Isolated browsing` (useful if you are using Edge) and `Exploit Protection`.

## Summary

As you can see setting up Defender to be useful, is pretty easy and even you grandmother can do it. Lol. Also pray that another update will not change your settings to the default one ;) I have my fingers crossed for Windows Defender and I hope in the future it will be much better and user friendly with integration for other web browsers. In the meantime I am using [Trend Micro Antivirus+](https://www.trendmicro.com/en_us/forHome/products/antivirus-plus.html) and when license ends I will test [Bitdefender Antivirus Plus](https://www.bitdefender.com/solutions/antivirus.html). What the heck did you think? That I am using Defender? Too much work with setup. I am too lazy. Let me know in the comments what do you prefer, and what do you think about Defender?

If you want to read interesting comments related to this article check [Hacker News thread](https://news.ycombinator.com/item?id=30580444). Thank you all for great and constructive dialogue, it will definitely let me help to make my articles better. Sorry if anyone felt offended by my private additions about no brain or shooting people. Rather, it’s an innate sarcasm and my twisted logic, I live in Poland, everyone is a bit different here ;) My readers are a small group that knows that sometimes I turn up the atmosphere. From time to time, some Reddit or Hacker News will hit my article and then I know that not everyone will understand my sense of humor and the way I run this blog. I’m not ready for fame and glory yet ;)
