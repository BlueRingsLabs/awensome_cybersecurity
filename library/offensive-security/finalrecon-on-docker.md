---
id: ckb-a7c0b8d66cef
title: FinalRecon on Docker
category: offensive-security
format: guide
language: en
tags: [bash, containers, linux, web-security]
summary: This guide demonstrates how to deploy and manage the FinalRecon web reconnaissance tool using Docker containers on a Linux VPS.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.95
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:12:37Z
---

# FinalRecon on Docker

[FinalRecon](https://github.com/thewhiteh4t/FinalRecon) is actively developed script that can help you conduct basic web reconnaissance automatically. I like to automate some of my work and this script looks quite good to gather information about target. I know at least where to start and what could be interesting for me in the next steps.

![finalrecon](finalrecon.jpg)

> FinalRecon is an **automatic web reconnaissance** tool written in python. Goal of FinalRecon is to provide an **overview** of the target in a **short** amount of time while maintaining the **accuracy** of results. Instead of executing **several tools** one after another it can provide similar results keeping dependencies **small and simple**.

Some of basic tools I use, I run from my VPS. Mainly tools that need more time to complete all tasks. I can run them as separate sessions on the server and come back for the results in a few hours or days. Thus, not blocking my computer or laptop at home. Virtual machines (e.g. Kali) may shut down and wait for more manual or demanding tasks.

Of course, you can simply run the FinalRecon script on any Linux, by installing it from GitHub. I know from experience that scripts and programs used by hackers and written for hackers are written with the intention of using them in a suitable environment, e.g. a distribution like Kali Linux, where most packages and libraries already exist and are delivered or available from distribution repositories. So not always everything works right away without the extra time spent fixing it. As always in Linux ;) also I do not want to clutter my server too much, so that then I do not waste time cleaning it and restoring it to a usable state.

Some time ago I was playing with Docker for a while. I went back to Docker for FinalRecon. The script is available as a container. So there is no need to waste any time. Below I will present how I run FinalRecon as a Docker container on my VPS server.

## Docker and FinalRecon installation

Most information of [Docker](https://www.docker.com/), [installation](https://docs.docker.com/engine/install/) and [containers](https://www.docker.com/resources/what-container) you can find in official [Docs](https://docs.docker.com/). It is really very well organized and easy to understand.

> Docker is a platform for developers and sysadmins to **build, run, and share** applications with containers. The use of containers to deploy applications is called *containerization*. Containers are not new, but their use for easily deploying applications is.

![docker](docker.jpg)

Installation of Docker on my [Debian](https://www.debian.org/) VPS is pretty simple. Follow these steps on your VPS with Debian system.

Install all necessary dependencies:

```bash
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```

Download and add Docker repo key:

```bash
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
```

Add Docker repository:

```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
```

Update repositories:

```bash
sudo apt-get update
```

Finally install Docker:

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

That’s all. All containers you can download and use are listed in official [Docker Hub](https://hub.docker.com/).

Download [FinalRecon Docker container](https://hub.docker.com/r/thewhiteh4t/finalrecon):

```bash
sudo docker pull thewhiteh4t/finalrecon
```

Now, on this simple container I will show you how to use Docker and how to navigate in Docker.

## Docker usage

To run container with FinalRecon use command:

```bash
sudo docker run -it --entrypoint /bin/sh thewhiteh4t/finalrecon
```

`-i` keep STDIN open even if not attached
`-t` allocate a pseudo-tty
`--entrypoint=""` overwrite the default entrypoint set by the image

Additionally you may want to use:

`--name` provide own name for container ([read more about name parameter](https://docs.docker.com/engine/reference/run/#name---name))

`-d` detached mode, run container in the background, print new container id

So you are in container with FinalRecon, this is just bash with installed script. Type `ls` command to list files in folder you are. As you can see it is just another bash dedicated just for FinalRecon. Cool right?

To exit container type `exit`. You will get back to your VPS shell, and the container session will be terminated. Other useful commands below.

List Running Docker Containers

```bash
sudo docker ps
```

List Stopped Docker Containers

```bash
sudo docker ps -f "status=exited"
```

List All Docker Containers

```bash
sudo docker ps -a
```

Back to running docker container

```bash
sudo docker attach <container_ID>
or
sudo docker attach <container_name>
```

If you want to leave the container but keep it running in the background use keyboard shortcuts:`Ctrl+p` then `Ctrl+q`.

`Ctrl+p` turn interactive mode to daemon mode.

`Ctrl+q` exit container.

Now use `sudo docker ps` command to list your containers. The one with status `Up` is the one you left running in background.

If container is stopped you can start it using command:

```bash
sudo docker start <container_ID or container_name>
```

To stop, type:

```bash
sudo docker stop <container_ID or container_name>
```

To remove stopped container from the list:

```bash
sudo docker rm <container_ID or container_name>
```

Remove all stopped containers:

```bash
sudo docker rm $(sudo docker ps -a -q)
```

`-a` show all containers (default shows just running)
`-q` only display numeric IDs

To copy files between container and local host use:

```bash
docker cp CONTAINER:SRC_PATH DEST_PATH|-
docker cp SRC_PATH|- CONTAINER:DEST_PATH
```

With these few commands you are pretty good Docker user :)

## FinalRecon usage

If you’re in container type:

`finalrecon -h` to see how to use tool.

Output:

```bash
usage: finalrecon.py [-h] [--headers] [--sslinfo] [--whois] [--crawl] [--dns] [--sub] [--trace] [--dir] [--ps] [--full] [-t T] [-T T] [-w W]
                     [-r] [-s] [-sp SP] [-d D] [-e E] [-m M] [-p P] [-tt TT] [-o O]
                     url

FinalRecon - The Last Recon Tool You Will Need | v1.0.8

positional arguments:
  url         Target URL

optional arguments:
  -h, --help  show this help message and exit
  --headers   Header Information
  --sslinfo   SSL Certificate Information
  --whois     Whois Lookup
  --crawl     Crawl Target
  --dns       DNS Enumeration
  --sub       Sub-Domain Enumeration
  --trace     Traceroute
  --dir       Directory Search
  --ps        Fast Port Scan
  --full      Full Recon

Extra Options:
  -t T        Number of Threads [ Default : 30 ]
  -T T        Request Timeout [ Default : 30.0 ]
  -w W        Path to Wordlist [ Default : wordlists/dirb_common.txt ]
  -r          Allow Redirect [ Default : False ]
  -s          Toggle SSL Verification [ Default : True ]
  -sp SP      Specify SSL Port [ Default : 443 ]
  -d D        Custom DNS Servers [ Default : 1.1.1.1 ]
  -e E        File Extensions [ Example : txt, xml, php ]
  -m M        Traceroute Mode [ Default : UDP ] [ Available : TCP, ICMP ]
  -p P        Port for Traceroute [ Default : 80 / 33434 ]
  -tt TT      Traceroute Timeout [ Default : 1.0 ]
  -o O        Export Output [ Default : txt ] [ Available : xml, csv ]
  
Examples:
# Check headers

python3 finalrecon.py --headers <url>

# Check ssl Certificate

python3 finalrecon.py --sslinfo <url>

# Check whois Information

python3 finalrecon.py --whois <url>

# Crawl Target

python3 finalrecon.py --crawl <url>

# Directory Searching

python3 finalrecon.py --dir <url> -e txt,php -w /path/to/wordlist

# full scan

python3 finalrecon.py --full <url>
```

Everything is clear.

Run a test on your website using command:

```plaintext
python3 finalrecon.py --full https://example.com/
```

You can observe results during scanning and after it is done it will be saved in `/root/finalrecon/dumps/example.com.txt` location.

If you want to copy file with results from container to your local machine use command:

```bash
sudo docker cp <Container_Name>:/root/finalrecon/dumps/example.com.txt /home/<USER>/
```

In my case with automatically generated name for container it will be:

```bash
sudo docker cp pensive_panini:/root/finalrecon/dumps/example.com.txt /home/hoek/
```

Yeah, that’s pretty much all you need to know in this topic.

Happy reconnaissance! Good luck with your findings and please do not test your knowledge on my server, it will die if you all guys start scanning it. Let it work for others who have a thirst for knowledge.
