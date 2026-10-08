---
id: ckb-da2c225840a2
title: Unattended upgrades
category: security-operations
format: guide
language: en
tags: [bash, hardening, linux]
summary: A technical guide on configuring automatic security updates using the unattended-upgrades package on Debian-based Linux systems.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-31b-it
  confidence: 0.95
classified_by: google:gemma-4-31b-it@2026-10-08T00:19:24Z
---

# Unattended upgrades

Have the latest security patches and updates, whether you’re sleep or not is very good idea. You can automate this process to make sure your server is secure. You should always update your systems and applications everywhere on every device to avoid unpleasant situations.

![upgrade](upgrade.jpg)

## Manual updates

That’s easy:

```bash
sudo apt update && sudo apt upgrade
```

or

```bash
sudo apt update && sudo apt dist-upgrade
```

Differences between `upgrade` and `dist-upgrade`

> upgrade
>  upgrade is used to install the newest versions of all packages
>  currently installed on the system from the sources enumerated in
>  /etc/apt/sources.list. Packages currently installed with new
>  versions available are retrieved and upgraded; under no
>  circumstances are currently installed packages removed, or packages
>  not already installed retrieved and installed. New versions of
>  currently installed packages that cannot be upgraded without
>  changing the install status of another package will be left at
>  their current version. An update must be performed first so that
>  apt-get knows that new versions of packages are available.

and

> dist-upgrade
>  dist-upgrade in addition to performing the function of upgrade,
>  also intelligently handles changing dependencies with new versions
>  of packages; apt-get has a “smart” conflict resolution system, and
>  it will attempt to upgrade the most important packages at the
>  expense of less important ones if necessary. So, dist-upgrade
>  command may remove some packages. The /etc/apt/sources.list file
>  contains a list of locations from which to retrieve desired package
>  files. See also apt_preferences(5) for a mechanism for overriding
>  the general settings for individual packages.

## Automatic updates

Install the `unattended-upgrades` package, along with a package to identify the changes:

```bash
sudo apt -y install unattended-upgrades apt-listchanges
```

Edit the `20unattended-upgrades` configuration file:

```bash
sudo nano /etc/apt/apt.conf.d/20auto-upgrades
```

or create it using command:

```bash
sudo dpkg-reconfigure -plow unattended-upgrades
```

and your configuration file should look like this:

```bash
// Enable unattended upgrades.
APT::Periodic::Enable "1";
APT::Periodic::Unattended-Upgrade "1";
// Do "apt-get upgrade" every n-days (0=disable).
APT::Periodic::Update-Package-Lists "1";
// Do "apt-get upgrade --download-only" every n-days (0=disable).
APT::Periodic::Download-Upgradeable-Packages "1";
// Do "apt-get autoclean" every n-days (0=disable).
APT::Periodic::AutocleanInterval "7";
```

Edit the `50unattended-upgrades` configuration:

```bash
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
```

and check these lines to make them configured like in my example:

```bash
Unattended-Upgrade::Origins-Pattern {
        // Codename based matching:
        // This will follow the migration of a release through different
        // archives (e.g. from testing to stable and later oldstable).
        // Software will be the latest available for the named release,
        // but the Debian release itself will not be automatically upgraded.
        "origin=Debian,codename=${distro_codename}-updates";
        "origin=Debian,codename=${distro_codename}-proposed-updates";
        "origin=Debian,codename=${distro_codename},label=Debian";
        "origin=Debian,codename=${distro_codename},label=Debian-Security";
        "origin=Debian,codename=${distro_codename}-security,label=Debian-Security";

Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-WithUsers "true";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
Unattended-Upgrade::Remove-New-Unused-Dependencies "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::InstallOnShutdown "false";
Unattended-Upgrade::Mail "root";
Unattended-Upgrade::MailOnlyOnError "true";

// Force to keep local config file
Dpkg::Options {
   "--force-confdef";
   "--force-confold";
};
```

Optional lines to add for 3rd party repositories (in my case Tor, GoAccess, PHP, Node, MariaDB and Nginx):

```bash
"origin=Tor Project,codename=${distro_codename},label=Tor Project";
"origin=GoAccess,codename=${distro_codename},label=GoAccess";
"origin=deb.sury.org";
"origin=Nodesource,codename=${distro_codename},label=Nodesource";
"origin=MariaDB,codename=${distro_codename},label=MariaDB";
"origin=Nginx";
```

This file is very well described in comments, so it’s easy to enable and disable options you would like to choose, above is my example. I also added at the end part related to keep local config file during upgrade, to not mess with my configuration.

Open `/etc/apt/listchanges.conf` to configure APT to save the changes to a database:

```bash
[apt]
frontend=pager
which=news
email_address=root
email_format=text
confirm=false
headers=false
reverse=false
save_seen=/var/lib/apt/listchanges.db
```

`unattended-ugprades` is running automatically and is called via `cronjob`.

If you want to debug it, you can easily run it with parameter:

```bash
sudo unattended-upgrade --dry-run --debug
```

All logs can be found here: `/var/log/unattended-upgrades/unattended-upgrades.log`

Now you can sleep peacefully ;)
