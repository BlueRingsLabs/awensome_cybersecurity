---
id: ckb-b8db591bfd6b
title: Windows software on Linux
category: foundations-and-systems
format: article
language: en
tags: [bash, linux, privilege-escalation, threat-intelligence, tls, windows]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 1.0
---

# Windows software on Linux

## Introduction

Sometimes it happens that we have to run Windows application on Linux. Sometimes we just want to play a game that has no support for Linux. To make this possible, we do not need to install a second system or configure a virtual machine. No! You don’t need to buy Windows to run few apps. The only thing you need is Wine.

> [Wine](https://www.winehq.org/ "Wine") (recursive backronym for Wine Is Not an Emulator) is a free and open-source compatibility layer that aims to allow computer programs (application software and computer games) developed for Microsoft Windows to run on Unix-like operating systems.

![wine](wine.jpg)

### Installation

There are three versions of Wine.

Stable branch

```bash
sudo apt-get install --install-recommends winehq-stable
```

Development branch

```bash
sudo apt-get install --install-recommends winehq-devel
```

Staging branch

```bash
sudo apt-get install --install-recommends winehq-staging
```

In most cases you probably would like to use latest version so it’s Development branch.

For latest version in Ubuntu add repositories

```bash
wget https://dl.winehq.org/wine-builds/Release.key
sudo apt-key add Release.key
sudo apt-add-repository 'https://dl.winehq.org/wine-builds/ubuntu/'
```

### Winetricks

In order to facilitate the configuration of Wine, the Winetricks script will also be useful, thanks to which we can easily change the Wine configuration and download/install various redistributable runtime libraries, packages and fonts.

```bash
sudo apt-get install winetricks
```

## Configuration

To configure wine we need to run command `winecfg` or `winetricks`.
These commands will create a default prefix located in your home user folder `/home/user/.wine`. Check this location and then you will see similar folder structure to the one from Windows system. This is the place where all Windows software will be installed and stored.
![winecfg](winecfg.jpg)

![winetricks](wineprefix.jpg)

### Prefixes

They’re not virtual machines, but they do behave somewhat similarly.
The default WINE prefix is `~/.wine`, but different and multiple prefixes can be used. Of course you can install all apps into one prefix but some apps require more system-wide edits like registry entries and .dlls to run, the potential for conflicts between these applications rises. It’s not all that common for programs running in Wine to break each other, but it does happen. This is especially true if you’re dealing with some 32bit applications on a 64bit WINE install.

To create new prefix run command

```bash
WINEPREFIX=/home/user/.newprefix1 winecfg
```

or for 32-bit architecture

```bash
WINEPREFIX=/home/user/.newprefix2 WINEARCH="win32" winecfg
```

`winecfg` at the end you can change with `winetricks`, it depends how would you like to configure newly created prefix.

When creating a new Wine prefix, you will be asked if you want to download `wine-mono` and `wine-gecko` components. For best compatibility, it is recommended to click Yes here.

To configure already created prefix run command

```bash
WINEPREFIX=/home/user/.newprefix1 winetricks
```

or

```bash
WINEPREFIX=/home/user/.newprefix1 winecfg
```

to configure default prefix just type `winecfg` or `winetricks`

## Running

To show how install Windows software in Linux I will let you know how to install Notepad++ for example. Download latest version and use command.

```bash
wine ~/Downloads/npp.7.5.6.Installer.exe
```

or for the specific prefixe

```bash
WINEPREFIX=/home/user/.office WINEARCH="win32" wine ~/Downloads/npp.7.5.6.Installer.exe
```

Complete all the necessary steps in the installer, as in the standard installation on the Windows system, and thats all. Shortcut to application will be waiting in your start menu/desktop. To be honest once you have installed Wine and created default prefix you can just double click on downloaded installer and it will work in the same way as on Windows.

Some of programs may need additional dlls or packages which you can easily add using Winetricks.

![wintericks packages](winetrickspackages.jpg)

Alos you can modify registry

![wintericks registry](wineregistry.jpg)

If you would like to unsintall application just run Winetricks and choose Uninstall Software option which will allow you to uninstall any application from the installe software list.

![winecfg uninstall](winecfguninstall.jpg)

## Office 2010

Best example for more complex application is Office 2010 installation. Yes! You can have fully working Microsoft Office 2010 on Linux. First install winbind.

```bash
sudo apt-get install winbind
```

Then create 32bit prefix

```bash
WINEPREFIX=/home/user/.office WINEARCH="win32" winetricks
```

Confirm `wine-mono` and `wine-gecko` installation.

Install additional packages `dotnet20`, `msxml6`, fonts `corefonts` and libraries `riched20` and `gdiplus`. You can do it using Winetricks.

In `wincfg` go to library tab and override `riched20` and `gdiplus` to “Native”

Run installer. Once complete you will have fully working Windows 2010 under Linux.

## Alternatives

There are also extensive graphical interfaces available on the market based on the Wine engine, which allows you to configure and install everything using windows.

### PlayOnLinux (PlayOnMac)

[https://www.playonlinux.com](https://www.playonlinux.com/)

### Crossover

<https://www.codeweavers.com/>

### Bottles

<https://usebottles.com/>
