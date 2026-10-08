---
id: ckb-0904da697ac8
title: Downloading big files from Tor
category: threat-intelligence-and-osint
format: guide
language: en
tags: [bash, dark-web, linux, osint, threat-intelligence]
summary: This guide provides a technical walkthrough for automating the download of large files from Tor hidden services using curl, screen, and Tor proxying.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.9
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:13:53Z
---

# Downloading big files from Tor

Some time ago I had to download some large files from the website, of one of the ransomware groups, in order to analyze the published (stolen) data. The leak was huge, hundreds of gigabytes, split in many large files and all published on the website hosted in Tor network.

![downloading](downloading.jpg)

The Tor network for anonymous communication and information exchange is ideal, but, for example, downloading files, [torrents](https://blog.torproject.org/bittorrent-over-tor-isnt-good-idea/) and other heavy materials is inefficient due to the speed of the network itself. Its not designed to exchange huge files, and that what Tor project developers is saying since the beginning.

With the development of the Tor project, the speed and capabilities have increased and, for example, watching YouTube videos or downloading smaller files is possible and relatively fast compared to the early days many years ago.

Also not all files you are downloading using Tor Browser have a chance to resume download in case of lost connection or new circuit or identity change.

If you visit <http://ransomwr3tsydeii4q43vazm7wofla5ujdajquitomtd47cxjtfgwyyd.onion/> you can see list of active ransomware group sites. Before ransomware start encryption of files, they are all exfiltrated to the ransomware operator server, all data in attacked company is encrypted and negotiation for encryption key starts. Each of group publish leaked data, if ransom is not paid.

Sometimes companies don’t know what exactly was leaked, and sometimes they don’t pay the ransom and download their unencrypted data after the leak :) but every time, you need to analyze what was leaked and limit further dangers of publishing company data.

So I had a task to download leak, analyze it, assess the risk and suggest what other attacks and threats may arise from the disclosed data. Overall, it’s a boring analytical task, but I was able to automate the process of downloading large files from the Tor network.

Ahh, before I describe technical details, one more challenge is managers…

I like the surprise on the faces of managers who ask how long it will take to download 300 giga of leaked data from Tor, and I say, with luck about 20 weeks. Then the conversation starts: “no way”, “that it has to be ASAP”, “best answer is to have it for yesterday”, “tomorrow at the latest”, “in the worst case by the end of the week during business hours” etc. So you need to start explain non technical guys how Tor network works :| Sometimes there are even ideas that if our computer is too slow or our network is weak, they can pay for the best connection and the fastest computer just to have the data for tomorrow (maybe you should have paid the ransom you would have data very fast back on drives, or invested in security before this sad situation occurred). Nobody understand that 300 GB of data with average speed of 0,2 MBit/s will take exactly 200000 minutes, so 138,9 days or 19,84 weeks or 4,563 months. The way of presenting stats depends on how stressed out the manager is and his sense of humor. Never mind.

## Introduction

Ok, to sum up steps from technical part, because it’s friday and I made it a little chaotic.

Solution, checks every one hour if curl is downloading files over Tor from the list of provided files, and all stuff is done in the background session. If download is dead, it will start it again, files on the list are rotated and resume on errors. Thanks to that you can forgot about it and wait till all files will be saved on local disk. You can remove logging errors and statuses option from the scripts, I did it because I was testing also other solutions for notifications. In general it’s not perfect, but it works. You can from time to time login to the virtual machine and check if everything works, like check network traffic or active sessions `sudo screen -ls` and if you want see how curl works bring back session `sudo screen -r <ID>`. To leave session press `Ctrl-A and d` to detach the screen. That’s all, maybe it will be useful for someone.

I assume that you have knowledge of Linux and it basic commands.

## Technical part

[Curl](https://curl.se/), [screen](https://linux.die.net/man/1/screen) and [Tor](https://www.torproject.org/) is all you need. Install virtual machine with Debian (no GUI needed, just minimal version of Debian, or whatever distribution you like, but in my example it’s Debian, configure it with your user and sudo stuff etc).

Install curl, screen and tor:

```bash
sudo apt install curl tor screen psmisc
```

Create a folder where files will be downloaded, put there text file with all links you want to download, one file per line.

Tor configuration is minimal (`sudo nano /etc/tor/torrc`)

```bash
RunAsDaemon 1
```

Restart it:

```bash
sudo service tor restart
```

In your home user directory create file `curl.sh` and put there:

```bash
#!/bin/bash
cd /home/user/test/download/
xargs -n 1 curl -x socks5h://127.0.0.1:9050 -L -O -k --retry 9999999 --retry-max-time 0 -C - < urls.txt
```

change `/home/user/test/download/` to location of your download folder and change `urls.txt` to the file you created that contains URLs to files. This file if executed will start download files listed in text file, one by one and retry on failure.

In details, `xargs` build and execute command lines from standard input, in our case it take each line from txt file and pass it to curl. `-x` parameter is for proxy and we are using socks5 for Tor. So far we have curl over Tor with list of files to download `-L`. Then `-O` is for remote name, so each downloaded file will be saved on disk with the same name as file on server. `-k` for insecure connection, by default, every SSL connection curl makes is verified to be secure, we don’t need that for Tor connection. `--retry` will retry number of times before giving up. `--retry-max-time` limit the total time allowed for retries and finally `-C -` tell curl to automatically find out where/how to resume the transfer. It then uses the given output/input files to figure that out.

Then create another file called `checker.sh` and put there:

```bash
#!/bin/bash
#Check if xargs is running
if pgrep -x "xargs" > /dev/null
then
    #Running
    echo "Running - no action - "$(date) >> /var/log/download.log
else
    #Not running
    echo "Not found - starting again - "$(date) >> /var/log/download.log
    #Kill all screen sessions
    killall screen >> /var/log/download.log
    #Run new session with curl
    screen -dm sh /home/user/curl.sh >> /var/log/download.log
fi
```

This script will check if process with `xarg` in name is running. If running, it will add log entry `Running - no action - <date of check>"` to the log file `var/log/download.log` If not running then entry about failure will be added to the same log file, then dead screen session in the background will be killed, this will be also added as note to the log file and new session will be created where our curl script for download files is executed.

Be careful as the log file can grow and eat up all your disk space, if you don’t need the logging option push everything to dev null `\> /dev/null`

Last thing is to add `checker.sh` script to the crontab.

```bash
sudo crontab -e
```

then add:

```bash
0 * * * * /home/user/checker.sh
```

to execute script every hour.

When all done execute command:

```bash
sudo sh checker.sh
```

It will check if the curl screen is running and create a fresh, first one, then `cron` will run it for you again every hour and create a new one if the curl download is interrupt.

Enjoy downloading big files from Tor.

## List preparation

Some time ago, I had to download not only large files, but a huge list of small and medium files from ransomware leak. It is always about creating a proper file with URLs. Each URL must be on a separate line, no spaces or other weird characters.

You can also use `sed` to add quotes at the beginning and end to make sure that each line is a single URL.

```sh
sed 's/.*/"&"/' input.txt > output.txt
```

This tool is great for manipulating and preparing link list.

In addition, ransomware groups started sharing leaked files as a list of files rather than large archives, as they realised that each large leak is almost impossible to download over Tor or takes too much time, so leaked files are locked and leaking them is not harmful to victims. So they make files available as loose files and directories, where each can be accessed from the browser. In most cases, these are some kind of freely available libraries for listing files on a website like a [jsTree](https://www.jstree.com/) or similar. Then you just have to list the files or get their names and build a list of URLs.

Each site may be different, the important thing is to find a starting point and build a list of files from there.

In my case, I was able to download a file with a directory listing.

```plaintext
.:

d 4.0K .
d 4.0K ..
d 4.0K Folder1
d 4.0K Folder2
d 4.0K Folder3
d 4.0K Folder4

Folder 1:

d 4.0K .
d 4.0K ..
d 20K Subfolder2

Folder1/Subfolder2:

d 20K .
d 4.0K ..
- 301K file1.docx
- 310K file2.jpg
- 12K file3.pdf
- 221K file5.txt
- 103K file6.xlsx
```

So all I had to do was clean it up and, using a Pythion script I invented using ChatGPT, format it to give me a full list of URLS to pass to curl.

```python
import re


def process_file(input_filename, output_filename, base_url):
    with (
        open(input_filename, "r", encoding="utf-8", errors="ignore") as input_file,
        open(output_filename, "w", encoding="utf-8") as output_file,
    ):
        current_path = ""
        for line in input_file:
            line = line.strip()

            # Check if a line ends with a colon
            if line.endswith(":"):
                current_path = line[:-1].replace(" ", "/")

            # Check if a line starts with a dash and a space and then contains a number followed by a dot and the letter K or M
            elif re.match(r"^- \d+(\.\d+)?[KM] ", line):
                parts = line.split(" ")
                filename = parts[-1]
                result_line = f"{base_url}/{current_path}/{filename}"
                output_file.write(result_line + "\n")


# Example of use:
base_url = "http://URL/files"  # Change the URL to your own
process_file("SOURCE_FILE", "urls.txt", base_url)
```

I was able to format the source list by searching only for file and directory names (regex magic in Python) and then add my URL to each file, so I had URL with onion domain, folder and filename. Which I used again in curl.

I will eventually learn Python, but I also wanted to show that you can use AI if you lack the know-how or if you want to automate something. Instead of manually modifying a file with different regexes.
