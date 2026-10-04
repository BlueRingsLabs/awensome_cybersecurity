---
id: ckb-f737ba33feff
title: Whonix for KVM
category: foundations-and-systems
format: article
language: en
tags: [anonymity, bash, networking, privilege-escalation, threat-intelligence, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.56
---

# Whonix for KVM

As I moved my virtual machines and labs from VirtualBox to Virt-Manager, I shared some tips about my new configuration. Maybe they will be useful for someone else who is also migrating. If you are looking for Windows 11 tips, you can also check out the article [Windows 11 virtual machine on KVM](../../../../2024/10/26/windows11-kvm/index.html).

The Whonix documentation is quite extensive and very good, but it might be overwhelming for a simple task like downloading, configuring, and installing Whonix on KVM. It’s great to read all the documentation before doing something to understand how it works, but since this blog is also my public notepad, I like to make quick, straightforward instructions for myself in case I need to repeat something or configure something again in the future. I don’t want to go through the whole documentation again from scratch. Don’t get me wrong; the Whonix documentation is awesome, and you should always read the official documentation and instructions from any vendor.

![Whonix KVM](whonix-kvm.webp)

All of this is based on [Whonix KVM Wiki](https://www.whonix.org/wiki/KVM) and other Wiki entries that I will mention later in the text. I also assume that you have Virt-Manager up and running. If not, you need a different tutorial.

## Configuration

Let’s make it quick. First, download the CLI and/or the GUI. I always download both, and then after importing, I use the CLI Gateway and the GUI Workstation. But you can do whatever you want.

<https://www.whonix.org/wiki/KVM#Download_Whonix>

Properly extracting downloaded content is important. If you do it incorrectly, you will see a “no bootable device” error after booting, which is most likely related to the downloaded content not being unpacked correctly. It is best to follow the official command.

```bash
unpack tar -xvf Whonix*.libvirt.xz
```

Enter extracted folder and import Whonix VM Templates, starting from the network

```bash
sudo virsh -c qemu:///system net-define Whonix_external*.xml
sudo virsh -c qemu:///system net-define Whonix_internal*.xml
```

Activate virtual network cards

```bash
sudo virsh -c qemu:///system net-autostart Whonix-External
sudo virsh -c qemu:///system net-start Whonix-External
sudo virsh -c qemu:///system net-autostart Whonix-Internal
sudo virsh -c qemu:///system net-start Whonix-Internal
```

and finally import Whonix Gateway and Workstation images

```bash
sudo virsh -c qemu:///system define Whonix-Gateway*.xml
sudo virsh -c qemu:///system define Whonix-Workstation*.xml
```

Now moving Whonix image files

```bash
sudo mv Whonix-Gateway*.qcow2 /var/lib/libvirt/images/Whonix-Gateway.qcow2
sudo mv Whonix-Workstation*.qcow2 /var/lib/libvirt/images/Whonix-Workstation.qcow2
```

Now, you can delete the leftovers from the Downloads folder and run your machines. It’s so easy!

As [Whonix is based on Kicksecure](https://www.whonix.org/wiki/Based_on_Kicksecure) now, it has some additional security features like [sysmaint](https://www.kicksecure.com/wiki/Sysmaint). After years of using old Whonix this might be a little bit difficult to get used to because the profile is separated into system maintenance and normal user. However, I tested this solution and it is quite good. You just need to adjust. Even though it can be [disabled](https://www.kicksecure.com/wiki/Unrestricted_admin_mode#Uninstalling_user-sysmaint-split_and_Enabling_Unrestricted_Admin_Mode), I do not recommend giving up this solution. For advanced users, I recommend a different solution that allows you to use sudo. In reality, you don’t need additional permissions for normal use. All you need to do is configure the system once, and then you can use it, adding or removing things as needed from time to time in maintenance mode. In practice, you can have several workstations: one for important tasks and another for development.

So if you decide to go with sudo, check this [wiki entry.](https://www.kicksecure.com/wiki/Sysmaint#enable_sudo_access_in_USER_session) Or follow steps below.

### Enable sudo access in USER session

Boot into `PERSISTENT Mode | SYSMAINT Session | maintenance tasks`.

Create file: `/etc/privleap/conf.d/privleap-debugging.conf`

```bash
sudo append-once /etc/privleap/conf.d/privleap-debugging.conf "\
[action:sudo]
Command=chmod o+x /usr/bin/sudo
#Command=/usr/libexec/helper-scripts/sudo-tools-enable
AuthorizedGroups=sudo
AuthorizedUsers=user
"
```

Boot back into `PERSISTENT Mode | USER Session | daily activities`.

And to enable `sudo` run

```bash
leaprun sudo
```

You need to run this every time before you want to use sudo. After running this command you can just use `sudo` once for example `sudo touch /etc/testfile` or like in case with ZuluCrypt GUI, your chain of commands should look like: `leaprun sudo` > `sudo zuluCrypt-gui`.

### Enable clipboard on Workstation

Go to your machine details and to the XML tab, make section below to have `  <clipboard copypaste='yes'/>`

```bash
<graphics type='spice'>
  <listen type='none'/>
  <clipboard copypaste='yes'/>
  <filetransfer enable='no'/>
  <gl enable='no'/>
</graphics>
```

## Multiple Workstations

If you need multiple workstations, simply clone **Whonix-Workstation** by highlighting `Whonix-Workstation` → `Open` → `Virtual Machine` → `Clone` and then change the IP address in each network settings.

```bash
sudoedit /etc/network/interfaces.d/30_non-qubes-whonix
```

Look for line `address 10.152.152.11`. Change the last octet. For example, change `10.152.152.11` to `10.152.152.12`. When using more than 1 additional Whonix-Workstation however `10.152.152.12` should be changed to `10.152.152.13` and so forth.

If you are using a machine other than **Whonix-Workstation**, simply set up the network manually using either the GUI or command line in another Linux, Windows, or Android system as follows:

```bash
## increment last octet of IP address on additional workstations
IP address 10.152.152.50
Subnet netmask 255.255.192.0
Default gateway 10.152.152.10
Preferred DNS server 10.152.152.10
```

More details in [Multiple Whonix-Workstations Wiki](https://www.whonix.org/wiki/Multiple_Whonix-Workstation).

## DHCP

One interesting alternative solution is to set up DHCP on **Whonix-Gateway**. Why assign an IP address each time, remember which machine has which address, and keep track of which address was last used, just edit `sudo nano /etc/network/interfaces.d/30_non-qubes-whonix`, comment:

```bash
auto eth0
iface eth0 inet static
       address 10.152.152.11
       netmask 255.255.192.0
       gateway 10.152.152.10
```

and uncomment:

```bash
auto eth0
iface eth0 inet dhcp
```

Save the file and edit Whonix-Internal network in Virt-Manager:

```bash
sudo virsh net-edit Whonix-Internal
```

by adding IP address section:

```bash
<ip address='10.152.152.0' netmask='255.255.192.0'>
    <dhcp>
      <range start='10.152.128.1' end='10.152.191.254'/>
    </dhcp>
</ip>
```

Restart internal network:

```bash
sudo virsh net-destroy Whonix-Internal
sudo virsh -c qemu:///system net-start Whonix-Internal
```

and on every Whonix- Workstation install DHCP client:

```bash
sudo apt install isc-dhcp-client
```

on custom Workstations in network settings choose DHCP. For more details check [Whonix Wiki about DHCP](https://www.whonix.org/wiki/KVM#DHCP).

## Multiple Gateways

In the case of multiple gateways, there is a little more work involved. Personally, I use two gateways, one Whonix-Gateway, which was originally set up during installation. I use it only for Whonix-Workstation. The second gateway, which I call Hack-Gate, is used as a gateway for testing and hacking Tor services. This ensures that the network traffic of my Kali Linux virtual machine is fully torified. Then I don’t have to manually set up Tor Socks Proxy in all tools and my Gateways are separated. There are instructions for setting up multiple gateways on [wiki](https://www.whonix.org/wiki/Multiple_Whonix-Gateway#How_to_use_Multiple_Whonix-Gateway), but I think they are not yet complete. Therefore, I encourage you to familiarise yourself with my steps.

First of all clone Whonix-Gateway. For the purposes of this guide, call it **Gate**. Next export Whonix virtual networks:

```bash
sudo virsh net-dumpxml Whonix-Internal > Gate-Internal.xml
sudo virsh net-dumpxml Whonix-External > Gate-External.xml
```

Edit both files, starting from `Gate-Internal.xml`

```bash
<network>
  <name>Gate-Internal</name>
  <bridge name='virbr4' stp='on' delay='0'/>
  <dns enable='no'/>
</network>
```

then `Gate-External.xml`

```bash
<network>
  <name>Gate-External</name>
  <forward mode='nat'>
    <nat>
      <port start='1024' end='65535'/>
    </nat>
  </forward>
  <bridge name='virbr3' stp='on' delay='0'/>
  <dns enable='no'/>
  <ip address='10.0.3.2' netmask='255.255.255.0'>
  </ip>
</network>
```

In the external one, I also changed the IP address to avoid a collision with the network configured in the original Whonix-External.

Import both networks:

```bash
virsh -c qemu:///system net-define Gate-Internal.xml
virsh -c qemu:///system net-autostart Gate-Internal
virsh -c qemu:///system net-start Gate-Internal
virsh -c qemu:///system net-define Gate-External.xml
virsh -c qemu:///system net-autostart Gate-External
virsh -c qemu:///system net-start Gate-External
```

Here are two useful commands you can use to check your virtual network configuration and see which bridges are already in use:

```bash
virsh -c qemu:///system net-list --all
ip link show type bridge
```

These can be used to delete virtual networks in case of some mistakes or cleanup:

```bash
virsh -c qemu:///system net-destroy <Network-Name>
virsh -c qemu:///system net-autostart --disable <Network-Name>
virsh -c qemu:///system net-undefine <Network-Name>
```

In the cloned **Gate** machine, change the network card settings from Whonix-Internal to Gate-Internal and from Whonix-External to Gate-External.

To edit the VM virtual NIC settings`Highlight VM` → `Open` → `Settings` → `NIC virtual hardware` → Set Network Source to the new one.

Now, you need to change the network settings inside the **Gate** machine. You can modify the `30_non-qubes-whonix` file, but to avoid interfering with the official Whonix files, which may be overwritten during updates, you can create a new `50_custom-whonix` file. This will partially overwrite the `30_non-qubes-whonix` file.

Boot the **Gate** machine and create a new file.

```bash
nano /etc/network/interfaces.d/50_custom-whonix
```

put inside

```bash
# Custom Whonix Gateway overrides (loaded after 30_non-qubes-whonix)
auto eth0
iface eth0 inet static
	pre-up ip addr flush dev eth0
    address 10.0.3.15
    netmask 255.255.255.0
    gateway 10.0.3.2
```

Restart network interface:

```bash
sudo ifdown eth0 && sudo ifup eth0
```

Everything should be working now. To test this, run the updates on **Gate** using the command `upgrade-nonroot`.

In your Workstation settings, select new network Gate-Internal.

## Hardening custom Workstation

Below is a minimum checklist that will bring your Debian workstation closer to the level of hardening and anonymization of a Whonix-Workstation, assuming it is only connected to the internal Whonix-Internal network behind the gateway.

### System Installation

1. Perform a Debian netinstall (minimal version) and select only the basic packages and a graphical environment (e.g., Xfce).
2. Make sure that the VM has only one network card set to Whonix-Internal.

### Network and DNS

Remove or disable the local DNS resolver.

```bash
sudo systemctl disable --now systemd-resolved
sudo apt purge --auto-remove systemd-resolved dnsmasq-base
sudo rm /etc/resolv.conf
echo "nameserver 10.152.152.10" | sudo tee /etc/resolv.conf
```

#### Disable IPv6

Create`/etc/sysctl.d/99-disable-ipv6.conf`:

```bash
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```

and load the settings:

```bash
sudo sysctl --system
```

#### Configure DHCP or static

Depending on your gateway configuration. In `/etc/network/interfaces.d/30_whonix` for DHCP:

```bash
auto eth0
iface eth0 inet dhcp
```

or for static:

```bash
auto eth0
iface eth0 inet static
    address 10.152.152.15
    netmask 255.255.192.0
    gateway 10.152.152.10
```

### Local firewall

Install `ufw` and only enable traffic to the gateway.

```bash
sudo apt install ufw
sudo ufw default deny outgoing
sudo ufw allow out to 10.152.152.10
sudo ufw enable
```

### Synchronization of time

Install `chrony` and disable the default `systemd-timesyncd`:

```bash
sudo apt install chrony
sudo systemctl stop systemd-timesyncd.service
sudo systemctl disable systemd-timesyncd.service
```

Open `/etc/chrony/chrony.conf` and add the Whonix-Gateway server at the top (or replace the existing server lines):

```bash
# Whonix Gateway as NTP source
server 10.152.152.10 iburst

# Other optional public servers (as backups)
# server 0.pl.pool.ntp.org iburst
# server 1.pl.pool.ntp.org iburst
```

Save the file and start/services:

```bash
sudo systemctl restart chrony
sudo systemctl enable chrony
```

Check the status and time sources:

```bash
chronyc sources
chronyc tracking
```

### System hardening

#### AppArmor

```bash
sudo apt install apparmor apparmor-utils
sudo systemctl enable --now apparmor
```

Check profiles using `sudo aa-status`

#### Remove unnecessary services

```bash
sudo systemctl disable --now \
  cups avahi-daemon \
  bluetooth.service \
  rpcbind nfs-common \
  smbd nmbd \
  systemd-resolved \
  systemd-timesyncd \
  apt-daily.service apt-daily.timer apt-daily-upgrade.timer \
  whoopsie \
  ModemManager.service \
  ssh.service #if you not use it
```

Always adjust it for your needs, these are just examples.

#### Tor Browser (avoid regular Firefox)

Install and run **Tor Browser**:

```bash
sudo apt install torbrowser-launcher
torbrowser-launcher
```

Configure Tor Browser settings to avoid [Tor over Tor](https://www.whonix.org/wiki/Tips_on_Remaining_Anonymous#Refrain_from_%22Tor_over_Tor%22_Scenarios) by editing:

```bash
sudo nano /etc/environment
```

and adding there:

```bash
## Deactivate tor-launcher,
## a Vidalia replacement as browser extension,
## to prevent running Tor over Tor.
## https://gitlab.torproject.org/legacy/trac/-/issues/6009
## https://gitweb.torproject.org/tor-launcher.git
TOR_SKIP_LAUNCH=1

## Environment variable to disable the "TorButton" →
## "Open Network Settings..." menu item. It is not useful and confusing to have
## on a workstation, because this is forbidden for security reasons. Tor must be
## configured on the gateway.
TOR_NO_DISPLAY_NETWORK_SETTINGS=1

## environment variable to skip TorButton control port verification
## https://gitlab.torproject.org/legacy/trac/-/issues/13079
TOR_SKIP_CONTROLPORTTEST=1
```

Save and reboot. Verify environment variables.

```bash
env
```

The output should show:

```plaintext
TOR_NO_DISPLAY_NETWORK_SETTINGS=1
TOR_SKIP_CONTROLPORTTEST=1
TOR_SKIP_LAUNCH=1
```

Configure network settings

Now the file `~/.tb/tor-browser/Browser/TorBrowser/Data/Browser/profile.default/user.js` must be created. This presupposes Tor Browser has been installed and that a folder *~/.tb/tor-browser* exists.

Open file `~/.tb/tor-browser/Browser/TorBrowser/Data/Browser/profile.default/user.js` in a text editor as a regular, non-root user.

If you are using a graphical environment, run. `mousepad ~/.tb/tor-browser/Browser/TorBrowser/Data/Browser/profile.default/user.js`

If you are using a terminal, run. `nano ~/.tb/tor-browser/Browser/TorBrowser/Data/Browser/profile.default/user.js`

Add.

```plaintext
user_pref("extensions.torbutton.use_privoxy", false);
user_pref("extensions.torbutton.settings_method", "custom");
user_pref("extensions.torbutton.socks_host", "10.152.152.10");
user_pref("extensions.torbutton.socks_port", 9100);
user_pref("network.proxy.socks", "10.152.152.10");
user_pref("network.proxy.socks_port", 9100);
user_pref("extensions.torbutton.custom.socks_host", "10.152.152.10");
user_pref("extensions.torbutton.custom.socks_port", 9100);
user_pref("extensions.torlauncher.control_host", "10.152.152.10");
user_pref("extensions.torlauncher.control_port", 9052);
```

Save. Tor is now disabled in Tor Browser.

Do not use the system Firefox browser for surfing – it is easy to leak your fingerprint with it. You can significantly hinder tracking and fingerprinting in *regular* Firefox, but you will never achieve the same level of resistance as in Tor Browser.

Alternatively use a ready-made, enhanced stack: Librefox or Arkenfox-user.js

- [Librefox](https://librewolf.net/) is Firefox with a patch pack and default privacy settings. You install it instead of the *stock* Firefox and get telemetry disabled, enhanced `resistFingerprinting`, and many other *out-of-box* fixes.
- [Arkenfox user.js](https://github.com/arkenfox/user.js) (fork GHacks) is a user.js file that you copy to your Firefox profile. After restarting, it overwrites the default prefs, enabling dozens of settings from `privacy.resistFingerprinting`, ui.zoom, referer restrictions, etc.

#### User account

Create a separate `admin` account with `sudo` privileges:

```bash
adduser admin
usermod -aG sudo admin
```

Use the main `user` account to work in Tor Browser, without excessive permissions. Block `root` password.

#### Do not use system Tor

Make sure you are not using system Tor to avoid [Tor over Tor](https://www.whonix.org/wiki/Tips_on_Remaining_Anonymous#Refrain_from_%22Tor_over_Tor%22_Scenarios).

```bash
# Stop Tor
sudo systemctl stop tor
# Prevent Tor service from restarting after reboot.
sudo systemctl mask tor
# Or uninstall it
sudo apt purge tor
```

### Other

Check also [System Hardening Checklist](https://www.whonix.org/wiki/System_Hardening_Checklist).

And that’s probably all, folks!
