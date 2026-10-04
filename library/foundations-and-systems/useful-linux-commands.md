---
id: ckb-d58576abb992
title: Useful Linux Commands
category: foundations-and-systems
format: article
language: en
tags: [bash, git, linux, log-analysis, privilege-escalation, python]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.99
---

# Useful Linux Commands

There is a lot of infographics about basic Linux commands. They are useful to start journey with Linux terminal. In this article I will show you basic commands with their extended usage and how I am using them. Using `ls -l` command with basic parameter is cool for directory listing, but it can do a lot more!

![Linux commands](linux-commands.png)

All pro hackers and regular visitors of this blog know, that this is another quick article, prepared in a rush, at the end of the month, just to have at least one entry on October :( I am trying guys, I know I suck! This website is also my personal knowledge base, so sooner or later I would publish all my handy Linux commands in one place anyway. Like I did for [Useful PowerShell Commands](https://reycdxyc24gf7jrnwutzdn3smmweizedy7uojsa7ols6sflwu25ijoyd.onion/useful-powershell-commands/). Never mind! I will try herder next month (I do not promise lol).

If you would like to learn more about any Linux commands and their parameters, then you should check [online man pages](http://man7.org/linux/man-pages/index.html).

I will update this from time to time, so worth to get back here in the future.

Lets start form simplest.

## System Info

`date` - show current date and time.

`cal` - show this month’s calendar.

`uptime` - show current uptime.

`w` - display who is online.

`whoami` - who you are logged in as.

`finger <user>` - display information about *user*.

`uname -a` - show kernel information.

`cat /proc/cpuinfo` - cpu information.

`cat /proc/meminfo` - memory information.

`man <command>` - show the manual for *command*.

`df` - show disk usage. `-h` more human friendly values.

`du` - show directory space usage.

`du -hsx * | sort -rh | head -10` - show directories, in human readable form, sort from biggest to lowest, summarize folder sizes and show top 10 positions.

`free` - show memory and swap usage.

`whereis <app>` - show possible locations of *app*. `-b` -binaries, `-m` -manual section, `-s` -source

`which <app>` - show which *app* will be run by default.

`lsb_release -a` - distribution information, `-r` -release number, `-c` -codename.

`cat /etc/os-release` - distribution information.

`hostnamectl` - OS version.

`uname -a` - Kernel architecture.

`cat /proc/version` - distribution information.

## File Commands

`ls -F` - show indicators after each entry, slash if for folder, asterisk is executable file, at sign is for alias.

`ls -lah` - translate file sizes to more human-friendly notation.

`ls -t` - sort by time.

`ls -m` - comma separated.

`ls -R` - list with recursion.

`pwd` - show current directory.

`mkdir` - create directory.

`rm` - delete file.

`rm -r` - delete directory.

`rm -f` - force remove.

`cp` - copy file.

`cp -r` - copy directory.

`mv` - move file.

`ln -s` - create a symbolic link.

`ln -s python_script.py /usr/bin/command` - creating user *command* that will execute *python script* and will be recognized globally by the system.

`touch <file>` - create *file*.

`cat > file` - create *file*, you can write something to save in that file and to save hit `Ctrl+D`.

`cat <file>` - display file content.

`cat -n <file>` - show line numbers.

`more` - display file content line by line.

`less` - display file and allows move between lines using arrows up and down.

`head` - display the first 10 lines of file.

`tail` - display last 10 lines of file.

`tails -f` - keep showing last 10 lines of file as it grows. Track changes.

`tail -n 15 -f access.log` - display and track changes for last 15 lines of log file.

`tail -f access.log | grep 127.0.0.1` - display and track changes for specific value (in this example IP 127.0.0.1) in access log file.

`watch tail -n 15 access.log` - display last 15 lines of log file and update output every 2 seconds.

`watch -n 10 tail -n 15 access.log` - display and track changes every 10 sec for last 15 lines.

`wc` - count lines, words, characters.

`wc -l <filename>` - count lines in file.

`tr` - manipulate text without needing to make multiple changes manually – think of the find and replace feature in a Word document. `tr [original_string] [string_to_replace] < input_file.txt > output_file.txt`

`sed` - is commonly used to search and replace specific string patterns from text. Unlike tr, sed can search and replace for more specific strings rather than simply converting all instances of a character in the text. `sed ‘s/pattern_to_find/pattern_to_replace/g’ input_file.txt`

`cut` - extract specified sections (columns) by cutting them based on delimiter.

`cut -d ' ' -f1,3,6 access.log` - delimiter is space, and we want to display columns from 1 to 3.

`cut -d ' ' -f3 access.log | sort | uniq -c` - list by 3rd column, remove, sort alphabetically, removes duplicates and counts of each.

`nl` - display line numbers, useful before head and tail command.

`|` - pipe, connect two or more commands, example: `grep KEYWORD access.log | head -n 5`

## File Permissions

`chmod <octal> <file>` - change the permission of *file* to *octal*, which can be found separately for users, group and world by adding:

- 4 - read (r)
- 2 - write (w)
- 1 - execute (x)

`chmod 777 file` - read, write, execute for all to *file*.

## Compression

`tar cf <file.tar> <files>` - create a tar named *file.tar* containing *files*.

`tar xf <file.tar>` - extract the files from *file.tar*.

`tar czf <file.tar.gz>` - create a tar with Gzip compression.

`tar xzf <file.tar.gz>` - extract a tar using Gzip.

`tar cjf <file.tar.bz2>` - create a tar with Bzip2 compression.

`tar xjf <file.tar.bz2>` - extract a tar using Bzip2.

`gzip <file>` - compresses *file* and renames it to *file.gz*.

`gzip -d <file.gz>` - decompresses *file.gz* back to file.

`7zr a -t7z <archive.7z> /folder/` - create 7z *archive* from folder. You can also point to file.

`7zr a -tzip <archive.7z> /folder/` - create zip *archive* from folder. You can also point to file.

`7zr e files.7z` - extract 7z *file*.

`unrar e file.rar </path>` - extract rar *file* to specific *path*.

`unrar x file.rar` - extract a rar file with their original directory structure.

`rar a file.rar /folder/` - create rar file from *folder*.

## Searching

`grep <pattern> <files>` - search for a *pattern* in *files*. `-A NUM`, `--after-context=NUM` - print NUM lines of trailing context after matching lines. `-B NUM`, `--before-context=NUM` - print NUM lines of leading context before matching lines.

`grep -r <pattern> <dir>` - search recursively for *pattern* in *dir*.

`<command> | grep <pattern>` - search for *pattern* in the output of *command*.

`locate <file>` - find all instances of *file*.

`find </path/> -iname pattern.extension` - search for files with specified *pattern* and *extension* in specific *path*. `-type f` - for files and `-type d` - for directories.

`find </path/> | grep 'word'` - search for *word* in filename in specific *path*.

`grep word /path/file` - search for *word* in *file*.

*Midnight Commander* have option to search for files and text.

Run `mc` and hit `Alt + Shfit + ?` to open search window.

## Process Management

`ps` - your active processes.

`top` - all running processes.

`htop` - console process manager, you need to install it. You will love it.

`kill <pid>` - kill process id pid.

`killall <name>` - kill all processes by *name*.

`bg` - list/resume stopped or background jobs.

`fg` - bring the most recent job to foreground.

## Network

`ping <host>` - ping *host* and output results.

`whois <domain>` - get whois information for *domain*.

`dig <domain>` - get DNS information for *domain*.

`dig -x <host>` - reverse lookup *host*.

`wget <file>` - download *file*.

`wget -c <file>` - continue a stopped download.

`sudo lsof -i -P -n | grep LISTEN` - check open ports.

`sudo netstat -tulpn | grep LISTEN` - check open ports.

`sudo ss -tulpn | grep LISTEN` - check open ports.

`sudo lsof -i:22` - check specific port such as 22.

`sudo nmap -sTU -O IP-address-Here` - check open ports.

## SSH

`ssh user@host -p 8022` - connect to host as user on port 8022.

`ssh-copy-id user@host` - add your key to host for user to enable a keyed or passwordless login.

## Installation

Install from source steps:

`./configure`

`make`

`make install`

Install from file:

`dpkg - i <pkg.deb>` - install a package (Debian).

`apt install <pkg.deb>` - install a package (Debian).

`rpm - Uvh <pkg.rpm>` - install a package (RPM).

## Shortcuts

`Ctrl+C` - halts the current command

`Ctrl+Z` - stops the current command, resume with `fg` in foreground or `bg` in the background.

`Ctrl+D` - log out of current session, similar to `exit`.

`Ctrl+W` - erases one word in the current line.

`Ctrl+U` - erases the whole line.

`Ctrl+R` - type to bring up a recent command.

`!!` - repeats the last command.

`&&` or `;` is used to chain commands together.

`/` by itself at the end of a line is a means of concatenating lines together

`|` - send the output of one command/program/process to another command/program/process for further processing.

`exit` - log out of current session.

## GitHub

I mostly use it to download some scripts and keep it up to date.

`git pull <http://some_repo/code.git /opt/code` - download/update local repository to the newest commit.

If you have a lot of local repos, like me, for example on your Kali machine and want to keep them all up to date you can use [gitup](https://github.com/earwig/git-repo-updater). This tool is created for updating multiple git repositories at once. You can simply install it in Debian `apt install gitup`. Then just run:

`gitup /opt/` - updates all GitHub repositories located under */opt* folder. You can do it folder by folder or recursively. You can also bookmark your repos `gitup --add ~/repos` if you add many of them `--add ~/repos/foo ~/repos/bar ~/repos/baz` you can just use `gitup` command to update all of your bookmarks and not point to each folder.

## Python

Running python scripts is simple.

`python script.py` - running Python script using default Python version.

`python2.7 script.py` - running Python script using specified version.

To check your version just type `python -V`.

Default Python in Kali Linux is set to 3, but some old, still good script are written in Python 2. Sometimes when I pull script from GitHub and create system alias for that script, to be recognized as system command, it is executed with error, because of default Python version. For example [golismero](https://github.com/golismero/golismero).

Create system command based on script: `ln -s ${PWD}/golismero.py /usr/bin/golismero`.

Now command `golismero` is recognized by system and I can run it whatever I am located.

Header of the Python file has defined shebang: `#!/usr/bin/env python` so it will be executed as Python 3. You can change that to `#!/usr/bin/env python2.7` and save, but you need to remember that every time you pull and updates. To avoid this, create shell script e.g.: `golismero.sh` and add there:

```shell
#!/bin/sh
python2.7 /opt/golismero/golismero.py
```

make it executable `chmod u+x golismero.sh` and create link `ln -s /opt/golismero.sh user/bin/golismero`.

You can also change Python version globally:

`sudo update-alternatives --config python`

but I do not recommend this.

## Image conversion and optimization

Mass image file conversion:

`mogrify -quality 80% *.jpg` - change quality of all *jpg* files to *80%*.

`mogrify -format jpg *.png` - convert all *png* files to *jpg* files.

`mogrify -format jpg -path ./new_folder *.png` - convert all *png* files to *jpg* files and save in *new_folder*.

`mogrify -format jpg -resize 50% -path ./new_folder *.png` - convert all *png* files to *jpg* files, resize them by *50%* and save in *new_folder*.

`mogrify -quality 85 -format jpg *.png && rm *.png` - convert all *png* files to *jpg* files located in the same folder, change *jpg* file quality to *85%* and delete source *png* files after conversion.

## Website database logs cleanup

`sudo ls -al /var/log/mysql/` - list all binary logs from MySQL or MariaDB. The output will show you list of logs. For example last one will be `mariadb-bin.002345`.

Log in to the databse `sudo mysql -u root -p` and purge all to the last one `PURGE BINARY LOGS TO 'mariadb-bin.002345';`

You can also use time instead of name `PURGE BINARY LOGS BEFORE '2021-10-01 22:00:00';`

It is worth to set up expiration `SET GLOBAL expire_logs_days = 5;` then in database conf file `my.cnf`

change value in line`expire-logs-days = 5`

## Logs and backups cleanup

`sudo find /var/log/* -name "*.gz" -exec rm -f {} \;` - this command finds all compressed logs and delete them. In section Search I described `find` command now you can see it in action in real case scenario.

`-name "FILE-TO-FIND"` - file pattern.
`-exec rm -rf {} \;` - delete all files matched by file pattern.

Other example is to find `bak` files and delete them with confirmation from user:

`find . -type f -name "*.bak" -exec rm -i {} \;`

Delete files older than 15 days in backup folder:

`find /home/user/backup/* -mtime +15 -exec rm {} \;`

## Auto mount hard drive

Mount drive on user login without providing password on mount.

`lsblk` - List available disk

`sudo mkdir /mnt/folder1`or `sudo mkdir /media/folder1` - Create new mount point

`sudo nano /etc/fstab` - edit fstab

Add line `/dev/sdb1  /mnt/folder1  ext4  defaults  0  2`

Reload daemon: `sudo systemctl daemon-reload` and test if mount works `sudo mount -a`

## Change hostname

Easy steps to change hostname

```bash
sudo nano /etc/hostname
NAME
sudo nano /etc/hosts
127.0.1.1    NAME
sudo hostname NAME
sudo systemctl restart systemd-logind.service
```

## Clean up system journals

```bash
sudo journalctl --vacuum-time=7d
sudo systemctl restart systemd-journald
```

## Cleanup logs

```bash
sudo du -sh /var/log/*
or
sudo find /var/log -type f -mtime +30 -delete
```

## Check directory size

```bash
sudo du -h --max-depth=1 | sort -rh | head -n 10
```

## Packages cleanup

```bash
sudo apt clean
sudo apt autoclean
sudo apt autoremove
sudo rm -rf /tmp/*
```

## Clean NPM cache

```bash
npm prune
npm cache clean --force
```

## Yarn project cleanup

```bash
yarn autoclean --init
yarn autoclean --force
yarn cache clean
du -sh /usr/local/share/.cache/yarn
```

## Firmware update

```bash
fwupdmgr get-devices
fwupdmgr refresh
fwupdmgr get-updates

sudo fwupdmgr update
```

## Log size check

```bash
sudo du -ah /var/log | sort -rh | head -n 10
sudo du -sh /var/log
```

## Journal size limit

```bash
sudo nano /etc/systemd/journald.conf

[Journal]
# Max log file in Megabytes MB
SystemMaxUse=500M
# Max size of one log file
SystemMaxFileSize=50M
# Max days to keep log files
MaxRetentionSec=30day

sudo systemctl restart systemd-journald #restart service
sudo logrotate -v /etc/logrotate.conf #check current settings
sudo logrotate -d /etc/logrotate.conf
```

## Plymouth theme change

```bash
sudo update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/new/newone.plymouth 100
sudo update-alternatives --config default.plymouth
sudo update-initramfs -u
```

## Disable guest session in LightDM

```bash
sudo nano /usr/share/lightdm/lightdm.conf.d/50-guest-wrapper.conf
[Seat:*]
allow-guest=false
```

## Memory type

```bash
dmidecode --type memory
```

## Reset touchpad

```bash
sudo rmmod psmouse
sudo modprobe psmouse
```

## Remove unused flatpaks

```bash
flatpak uninstall --unused
```

## Add bluetooth device from cli

```bash
bluetoothctl
scan on
scan off
pair <MAC_ADDRESS>
trust <MAC_ADDRESS>
```
