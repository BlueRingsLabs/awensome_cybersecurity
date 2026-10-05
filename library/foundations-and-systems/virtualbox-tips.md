---
id: ckb-aab0161196cf
title: VirtualBox Tips
category: foundations-and-systems
format: article
language: en
tags: [bash, linux, powershell, tls, windows]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 1.0
---

# VirtualBox Tips

There is a lot of installation guides and configuration suggestion dedicated to the [VirtualBox](https://www.virtualbox.org/). There are also many problems solved that can be easily found in your favorite [search engine](https://duckduckgo.com/). So I will not make you bored and I not discuss a well-written installation and configuration which you will find in the [official documentation](https://www.virtualbox.org/manual/). I will summarize instead what should be done after installing VirtualBox so as to avoid basic errors. I will also mention a few solutions that every VirtualBox user is looking for, sooner or later.

![VirtualBox](virtualbox.jpg)

I wrote down the following steps to make it easier for myself to work with VirtualBox and not to wonder every time, why something does not work, just because I forgot about a few obvious settings.

## Three simple steps

Do this after every Virtual Box [installation on Linux host](https://www.virtualbox.org/manual/ch02.html#install-linux-host) to make sure everything works correctly.

1. Add user to `vboxusers` group on host machine and do the same on guest machine

```bash
usermod -aG vboxusers username
```

This change need log out and log in.

2. Install Extension Pack.
3. Install VirtualBox Guest Additions
    On guest machine install required packages

```bash
sudo apt install build-essential dkms linux-headers-$(uname -r)
```

then Insert Guest Additions CD and run as root `./VBoxLinuxAdditions.run`

With above 3 suggestion you should not have any problems with shared folder access, usb devices, copy & paste between host & guest, graphics adjustment.

## Reduce .vdi size

After some time, each [VDI](https://en.wikipedia.org/wiki/VirtualBox#VirtualBox_Disk_Image) disk created with dynamically allocated space has the maximum size even though the system does not really occupy the entire virtual surface. It is worth then to compact its size. This method works only for VDI files.

### Linux

#### On guest

Cleanup whole empty space by nullify free space:

```bash
dd if=/dev/zero of=/var/tmp/bigemptyfile bs=4096k ; rm /var/tmp/bigemptyfile
```

It can take some time.

#### On host

Use vboxmanage tool to compact disk

```bash
vboxmanage modifyhd /path/to/thedisk.vdi --compact
```

this command on VirtualBox version >=6.1.4 looks now:

```bash
VBoxManage modifymedium disk /path/to/thedisk.vdi --compact
```

### Windows

#### On guest

Run disk defragmentation.

Once done download [SDelete](https://docs.microsoft.com/pl-pl/sysinternals/downloads/sdelete) tool and run it from command line with parameter:

```bash
sdelete.exe c: -z
```

replace `c:` with the drive letter of the VDI

#### On host

```powershell
VBoxManage.exe modifyhd c:\path\to\thedisk.vdi --compact
```

this command on VirtualBox version >=6.1.4 looks now:

```powershell
VBoxManage modifymedium disk /path/to/thedisk.vdi --compact
```

## Disk conversion

If you would like to compact your disk but its in [VMDK](https://en.wikipedia.org/wiki/VMDK) format you can easily covert it to VDI.

```bash
VBoxManage clonehd "source.vmdk" "cloned.vdi" --format vdi
```

Just in case make a copy of drive before conversion.

## Resize disk

In case where your virtual disk is out of space you can resize it. This method also works for VDI files only.

```bash
VBoxManage modifyhd "disk.vdi" --resize 51200
```

Resize value should be set to the new size of whole disk, not the amount of new space you want to add.

Next, on guest host resize partition using your favorite partition manager, for example [Gparted](https://gparted.org/).

## Slow Windows guest

Since VirtualBox 6 if Hyper-V is enabled, then icon for green turtle will be shown in the notification area of VirtualBox, as shown below, and Virtual Machine will be slow.

![VirtualBox green turtle icon](greenturtle.png)

In my case I had to turn off one of the option in Microsoft Windows Defender called *Core isolation*.

Also turn off Hyper-V using command in PowerShell (don’t forget to run PowerShell as Admin).

```powershell
bcdedit /set hypervisorlaunchtype off
```

then reboot:

```powershell
shutdown -s -t 2
```
