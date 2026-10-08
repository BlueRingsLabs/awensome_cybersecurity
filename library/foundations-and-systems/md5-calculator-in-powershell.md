---
id: ckb-0f3ab1b3b4f8
title: MD5 calculator in powershell
category: foundations-and-systems
format: guide
language: en
tags: [cryptography, powershell]
summary: This guide provides a PowerShell script designed to calculate MD5 hash values for individual files or entire directories.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.9
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:15:30Z
---

# MD5 calculator in powershell

## Compute the hash value

`Get-FileHash` cmdlet allows easily to compute the [hash value](https://en.wikipedia.org/wiki/Hash_function) for a file since PowerShell version 4.0. The acceptable values for algorithm are: SHA1, SHA256, SHA384, SHA512, MD5. More about `Get-FileHash` you can read in [official documentation](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash?view=powershell-6).
Simplest way to calculate md5 hash value for a file is to use command:

```powershell
Get-FileHash path_to_file -Algorithm MD5 | Format-List
```

I decided to build simple MD5 calculator using [Powershell](https://en.wikipedia.org/wiki/PowerShell).

## MD5 calcuator

Powershell GUI

### Menu

First I created a menu

```powershell
function Show-Menu
{
     param (
           [string]$Title = 'MD5 Calculator'
     )
     cls
     Write-Host "===================== $Title ====================="

     Write-Host "1: Press '1' for single file, output in console"
     Write-Host "2: Press '2' for single file, output in text file"
     Write-Host "3: Press '3' for all files in folder, output in console"
     Write-Host "4: Press '4' for all files in folder, output in text file"
     Write-Host "Q: Press 'Q' to quit."
}
```

![md5 calculator](md5calc.jpg)

### Variables

I used few variables which need to be provided by user:

- `$FilePath` - for the file source
- `$FolderPath` - for folder source
- `$Output` - text file output location

### Options

I added four options like:

1. MD5 for single file, output in console `Get-FileHash $FilePath -Algorithm MD5 | Format-List`
2. MD5 for single file, output in text file `Get-FileHash $FilePath -Algorithm MD5 | Format-List > $Output\MD5.txt`
3. MD5 for all files in folder, output in console `Get-ChildItem $FolderPath | Get-FileHash -Algorithm MD5 | Format-List`
4. MD5 for all files in folder, output in text file `Get-ChildItem $FolderPath | Get-FileHash -Algorithm MD5 | Format-List > $Output\MD5.txt`

### Progress info

I also wanted to display some information about work in progress so I added three text variables

- `$Activity = "Calculating MD5 Hash Value"`
- `$Id       = 1`
- `$Task     = "Please wait"`

and part of code to display progress info during the hash value is calculated

```powershell
Write-Progress -Id $Id -Activity $Activity -Status $Task
```

![](md5calcoutput.jpg)

## Whole script

And the full code looks like below

```powershell
function Show-Menu
{
     param (
           [string]$Title = 'MD5 Calculator'
     )
     cls
     Write-Host "===================== $Title ====================="

     Write-Host "1: Press '1' for single file, output in console"
     Write-Host "2: Press '2' for single file, output in text file"
     Write-Host "3: Press '3' for all files in folder, output in console"
     Write-Host "4: Press '4' for all files in folder, output in text file"
     Write-Host "Q: Press 'Q' to quit."
}
do
{
     Show-Menu
     $input = Read-Host "Please make a selection"
     switch ($input)
     {
           '1' {
                cls
                'MD5 for single file, output in console'
                'Paste UNC path to file you want to calculate'
                $FilePath = Read-Host -Prompt 'Source file path'
                $Activity = "Calculating MD5 Hash Value"
                $Id       = 1
                $Task     = "Please wait"
                Write-Progress -Id $Id -Activity $Activity -Status $Task
                Get-FileHash $FilePath -Algorithm MD5 | Format-List
           } '2' {
                cls
                'MD5 for single file, output in text file'
                'Paste UNC path to file you want to calculate'
                $FilePath = Read-Host -Prompt 'Source file path'
                'Paste path for output report eg: C:\reports'
                $Output = Read-Host -Prompt 'Report location path'
                $Activity = "Calculating MD5 Hash Value"
                $Id       = 1
                $Task     = "Please wait"
                Write-Progress -Id $Id -Activity $Activity -Status $Task
                Get-FileHash $FilePath -Algorithm MD5 | Format-List > $Output\MD5.txt
                'Complete! Report saved to MD5.txt file'
           } '3' {
                cls
                'MD5 for all files in folder, output in console'
                'Paste UNC path to folder with files you want to calculate'
                $FolderPath = Read-Host -Prompt 'Source folder path'
                $Activity = "Calculating MD5 Hash Value"
                $Id       = 1
                $Task     = "Please wait"
                Write-Progress -Id $Id -Activity $Activity -Status $Task
                Get-ChildItem -Recurse $FolderPath | Get-FileHash -Algorithm MD5 | Format-List

           } '4' {
                cls
                'MD5 for all files in folder, output in text file'
                'Paste UNC path to folder with files you want to calculate'
                $FilePath = Read-Host -Prompt 'Source folder path'
                'Paste path for output report eg: C:\reports'
                $Output = Read-Host -Prompt 'Report location path'
                $Activity = "Calculating MD5 Hash Value"
                $Id       = 1
                $Task     = "Please wait"
                Write-Progress -Id $Id -Activity $Activity -Status $Task
                Get-ChildItem -Recurse $FolderPath | Get-FileHash -Algorithm MD5 |Format-List > $Output\MD5.txt
                'Complete! Report saved to MD5.txt file'
           } 'q' {
                return
           }
     }
     pause
}
until ($input -eq 'q')
```

### Usage

All you need is to copy everything and save as **MD5Calculator.ps1** then run with Powershell and follow instructions on the screen. By changing the `-Algorithm` parameter you can simply create a calculator for other algorithms.
