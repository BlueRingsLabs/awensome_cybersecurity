---
id: ckb-d8d2fbcb09c4
title: Useful PowerShell commands
category: foundations-and-systems
format: cheatsheet
language: en
tags: [powershell, windows]
summary: A collection of useful PowerShell commands for file management, network statistics, and execution policy bypasses.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-31b-it
  confidence: 0.95
classified_by: google:gemma-4-31b-it@2026-10-08T00:22:09Z
---

# Useful PowerShell commands

Hello. Today I would like to share with you guys some useful [PowerShell](https://en.wikipedia.org/wiki/PowerShell) commands. These are more complex. Why PowerShell? Because it’s easy and much faster than some GUI operations. I will keep this post up to date, so if I will use something new and cool I add it here.

![powershell](powershell.jpg)

If you want to know more about PowerShell check official [PowerShell website](https://docs.microsoft.com/en-us/powershell/), [PowerShell Github repo](https://github.com/PowerShell/PowerShell) and awesome [PowerShell Survival Guide](https://social.technet.microsoft.com/wiki/contents/articles/183.windows-powershell-survival-guide.aspx).

## Count folder size

Sometimes checking size of folder in Explorer can take ages, especially when there is a lot of small files. Don’t wait! Just use open PowerShell, provide location you want to check and use command:

```powershell
"{0:N2} MB" -f ((Get-ChildItem C:\path_to_folder\ -Recurse | Measure-Object -Property Length -Sum -ErrorAction Stop).Sum / 1MB)
```

To see results in GB:

```powershell
"{0:N2} GB" -f ((Get-ChildItem C:\path_to_folder\ -Recurse | Measure-Object -Property Length -Sum -ErrorAction Stop).Sum / 1GB)
```

## Mass extension change

If you want to change extension for many files in folder use this:

```powershell
Dir *.tiff | rename-item -newname { [io.path]::ChangeExtension($_.name, "tif") }
```

In this example all files with tiff extension will be changed to tif.

## Display specified number of lines

To get the first 10 lines:

```powershell
Get-Content ".\test.txt" | select -First 10
```

To get the last 10 lines:

```powershell
Get-Content ".\test.txt" | select -Last 10
```

## Run Active Directory as different user

Use `runas` command to run application or other command as different user

```bash
runas /user:username@domain "mmc.exe dsa.msc"
```

In this case Active Directory Users and Computers snap-in. Provide your user name and domain.

## Search in file content

Linux Grep alternative.

```powershell
Get-ChildItem C:\Users\tes\Documents\ -Filter * -Recurse | Select-String "some_text"
```

or

```powershell
Select-String -Path C:\Users\test\Documents\* -Pattern "some_word"
```

## Network statistics

Some useful commands to gather network statistics

```powershell
netsh interface ipv4 show ipstats
```

TCP stats:

```powershell
netsh interface ipv4 show tcpstats
```

NetAdapter module

```powershell
netsh interface ipv4 show tcpstats
```

## Execution policy

Of course how to bypass it, just for script by spawning a new PowerShell process:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\script.ps1
```

PowerShell offers the ability to run commands encoded as base64. To do this, you must encode the contents of the file and pass the resulting string to the `-EncodedCommand` switch of PowerShell.

```powershell
$commands = Get-Content script.ps1 -Raw
$bytes = [System.Text.Encoding]::Unicode.GetBytes($commands)
$encodedCommand = [Convert]::ToBase64String($bytes)
powershell.exe -EncodedCommand $encodedCommand
```

Check policy:

```powershell
Get-ExecutionPolicy
```

Set it:

```powershell
Set-ExecutionPolicy Bypass
```

## To be continued…
