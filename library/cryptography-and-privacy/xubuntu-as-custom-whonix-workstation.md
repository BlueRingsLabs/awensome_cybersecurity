---
id: ckb-53beb549ee44
title: Xubuntu as custom Whonix workstation
category: cryptography-and-privacy
format: article
language: en
tags: [anonymity, bash, hardening, networking, privilege-escalation, tls]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.89
---

# Xubuntu as custom Whonix workstation

If you are a [Whonix](https://www.whonix.org/) user this guide may be useful for you. Sometimes when I want to torify whole traffic from a virtual system I am using Whonix Gateway virtual machine. For people who haven’t use Whonix yet here is a short description with links:

> Whonix ™ consists of two VMs: the [Whonix-Gateway ™](https://www.whonix.org/wiki/Whonix-Gateway) and the [Whonix-Workstation ™](https://www.whonix.org/wiki/Whonix-Workstation). The former runs Tor processes and acts as a gateway, while the latter runs user applications on a completely isolated network.

![xubuntu workstation](xubuntu-workstation.jpg)

So sometimes in my virtual lab I want to use standard Linux distribution instead of the Whonix Workstation. There is a quite nice documentation about setting up a network in [other operating systems](https://www.whonix.org/wiki/Other_Operating_Systems). There is also section about [Ubuntu](https://www.whonix.org/wiki/Ubuntu_Tips), but since network configuration is now based on [netplan](https://netplan.io/), the wiki entry didn’t work for me. I set it up by myself, and decided to share the configuration steps. I did it on Xubuntu 22.04.

## Whonix network configuration for Xubuntu

First, run the following set of commands to disable the `NetworkManager`:

```bash
sudo systemctl stop NetworkManager
sudo systemctl disable NetworkManager
sudo systemctl mask NetworkManager
```

Next, start and enable the `systemd-networkd` service:

```bash
sudo systemctl unmask systemd-networkd.service
sudo systemctl enable systemd-networkd.service
sudo systemctl start systemd-networkd.service
```

edit conf file:

```bash
sudo nano /etc/netplan/01-network-manager-all.yaml
```

Your config should look like the one below:

```plaintext
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - 10.152.152.12/18
      routes:
        - to: default
          via: 10.152.152.10
      nameservers:
        addresses: [10.152.152.10]
```

where `enp0s3` is the name of your network adapter and apply new configuration:

```bash
sudo netplan apply
```

then shutdown the system.

In Virtual Box configuration for the virtual machine with Xubuntu choose network as `Internal Network` and name choose `Whonix`. (I guess you already have imported Whonix Gateway and know how to use it.)

Turn on the Gateway and your Xubuntu and that’s all. All the traffic from the Xubuntu machine is now passed through Whonix Gateway and “torified”.

Remember that Whonix Workstation has more security settings implemented, so you should harden your custom workstation for better security, privacy and anonymity. Check some cool [comparison](https://www.whonix.org/wiki/Other_Operating_Systems#Security_Comparison:_Whonix_%E2%84%A2-Download-Workstation_vs._Whonix-Custom-Workstation_%E2%84%A2) and read about [More Security](https://www.whonix.org/wiki/Other_Operating_Systems#More_security) or [Even More Security](https://www.whonix.org/wiki/Other_Operating_Systems#Even_more_security) to make your custom workstation even better.

## Firefox hardening

Basic steps would be to set some Firefox settings (hardening). Go to `about:config` and change some options. Of course all depends on your needs, but below you can find some suggestions.

Allow onion

```plaintext
network.dns.blockDotOnion false
```

Disable Firefox Screenshots extension

```plaintext
extensions.screenshots.disabled	true
```

Disable telemetry

```plaintext
browser.newtabpage.activity-stream.feeds.telemetry false
browser.ping-centre.telemetry false
browser.tabs.crashReporting.sendReport false
toolkit.telemetry.enabled false
toolkit.telemetry.unified false
```

Delete the URL for `toolkit.telemetry.server`, and leave it empty.

Disable Pocket

```plaintext
browser.newtabpage.activity-stream.feeds.discoverystreamfeed false
browser.newtabpage.activity-stream.feeds.section.topstories false
browser.newtabpage.activity-stream.section.highlights.includePocket false
browser.newtabpage.activity-stream.showSponsored false
extensions.pocket.enabled false
```

Disable prefetching

```plaintext
network.dns.disablePrefetch true
network.prefetch-next false
```

Disable JavaScript in PDF

```plaintext
pdfjs.enableScripting false
```

Disable Firefox account features

```plaintext
identity.fxaccounts.enabled false
```

Disable geolocation support

```plaintext
geo.enabled false
```

Disable notification support

```plaintext
dom.webnotifications.enabled false
```

Disable WebRTC

```plaintext
media.peerconnection.enabled false
media.navigator.enabled false
```

Disable WebGL

```plaintext
webgl.disabled true
```

Resist browser fingerprinting

```plaintext
privacy.resistFingerprinting true
```

Disable clipboard events

```plaintext
dom.event.clipboardevents.enabled false
```

Of course go to standard Firefox setting available from GUI and change some options too, like clear history and cookie every time when Firefox is closed etc.

If you would like to use Tor Browser on custom Whonix Workstation, don’t forget to set it up correctly to avoid [Tor Over Tor](https://www.whonix.org/wiki/DoNot#Allow_Tor_over_Tor_Scenarios) scenario.
