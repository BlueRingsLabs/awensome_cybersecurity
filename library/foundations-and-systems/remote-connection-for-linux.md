---
id: ckb-0709c6efe1e5
title: Remote connection for Linux
category: foundations-and-systems
format: guide
language: en
tags: [bash, homelab, linux, networking]
summary: A guide on setting up x11vnc to enable remote desktop connections for Linux systems within a local network.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-26b-a4b-it
  confidence: 0.9
classified_by: google:gemma-4-26b-a4b-it@2026-10-08T00:16:01Z
---

# Remote connection for Linux

Remote connection for Windows is pretty easy. Built in RDP server and client allows you to connect to remote Windows machine without any additional software. It is of course not too safe, to allow remote connection from the Internet, without any additional security layer, but this is not the topic for today. Today we are talking about local network and Linux. In the past I was using various software to connect to Linux session remotely. Mostly it was solution like [TightVNC](https://www.tightvnc.com/), [TigerVNC](https://tigervnc.org/), [UltraVNC](https://www.uvnc.com/), and other fancy variations of VNC servers and clients. These programs, in most cases, allow you to start a dedicated new session and not connect to the existing one. There are some other software like [TeamViewer](https://www.teamviewer.com/) (which I use as an app, to support my family, and solve their problems with system and computer) and very good alternative [NoMachine](https://www.nomachine.com/). Anyway, I was looking for simple VNC server which will allows me, to connect, to existing session on my virtual machines located on my [Synology NAS](../../../05/18/backup-your-data/index.html), inside my home network. [Synology Virtual Machine Manager](https://www.synology.com/dsm/feature/virtual_machine_manager) allows you to run virtual machines and access them using web browser. It is awesome (a little delayed, and making clipboard works fine can take some time), but more practical and efficient, it is easier to use VNC connection. So if you are looking for solution, to connect remotely, to your physical or virtual machine with Linux, check the rest of the article.

![Linux VNC remote connection](remoteconnection.jpg)

## X11VNC

[x11vnc](https://github.com/LibVNC/x11vnc) is a VNC server for real X displays. That’s my favorite and simplest solution. In the past it was developed by Karl Runge, but since version 0.9.14 it is developed by LibVNC and Github community.

Installation is quite easy:

```bash
sudo apt-get update
sudo apt-get install x11vnc
```

After installation you need to setup password:

```bash
x11vnc -storepasswd 

Enter VNC password: *********
Verify password: *********  
Write password to /home/user/.vnc/passwd?  [y]/n y
Password written to: /home/user/.vnc/passwd
```

Password is stored as encrypted.

Turn server ON and test connection using any of the VNC viewer (connect to the IP of your machine and port selected below -5900):

```bash
sudo x11vnc -auth guess -forever -loop -noxdamage -repeat -rfbauth /home/user/.vnc/passwd -rfbport 5900 -shared
```

`-auth guess` to have x11vnc use its `-findauth` mechanism to try to guess the XAUTHORITY filename and use it.

`-forever` keep listening for more connections rather than exiting as soon as the first client(s) disconnect.

`-loop` create an outer loop restarting the x11vnc process whenever it terminates.

`-noxdamage` do not use the X DAMAGE extension to detect framebuffer changes even if it is available.

`-repeat` turn off default option `-norepeat` disables X server key auto repeat when VNC clients are connected and VNC keyboard input is not idle for more than 5 minutes.

`-rfbauth  passwd-file` use authentication on RFB protocol (use `x11vnc -storepasswd pass file` to create a password file).

`-rfbport port` TCP port for RFB protocol.

`-shared` VNC display is shared, i.e. more than one viewer can connect at the same time (default off).

Once it is running I am using my favorite multi protocol remote connection manager for Windows, [mRemoteNG](https://mremoteng.org/) :)

![Linux VNC mRemoteNG](parrotvnc.jpg)

If everything works good, create new service to run the server on the system startup. Create a file:

```bash
sudo nano /etc/systemd/system/x11vnc.service
```

put inside:

```bash
[Unit]
Description=x11vnc remote desktop server
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/x11vnc -auth guess -forever -loop -noxdamage -repeat -rfbauth /home/user/.vnc/passwd -rfbport 5900 -shared -o /var/log/x11vnc.log

Restart=on-failure

[Install]
WantedBy=multi-user.target
```

I added parameter `-o` to keep an eye for logs from app.

Run service and check it status:

```bash
sudo systemctl daemon-reload
sudo systemctl start x11vnc
sudo systemctl status x11vnc
```

If service is running (active) then enable it on boot:

```bash
sudo systemctl enable x11vnc.service
```

Done. In combination with VPN or tunnel over SSH you can make it more secure and use even outside your home network.
