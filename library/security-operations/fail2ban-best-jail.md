---
id: ckb-07605f494192
title: Fail2Ban - best jail
category: security-operations
format: article
language: en
tags: [bash, linux, log-analysis, privilege-escalation, tls, web-security]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.35
---

# Fail2Ban - best jail

[Fail2Ban](https://www.fail2ban.org/wiki/index.php/Main_Page) is another great tool which help you to protect your servers against too many login attempts on your services.

> Fail2ban scans log files (e.g. `/var/log/apache/error_log`) and bans IPs that show the malicious signs – too many password failures, seeking for exploits, etc. Generally Fail2Ban is then used to update firewall rules to reject the IP addresses for a specified amount of time, although any arbitrary other action (e.g. sending an email) could also be configured. Out of the box Fail2Ban comes with filters for various services (apache, nginx, courier, ssh, etc).

![Fail2Ban](fail2ban.jpg)

## Instalation

Debian, Ubuntu:

```bash
sudo apt install fail2ban
```

## Configuration

Fail2ban reads `.conf` configuration files first, then `.local` files override any settings. All changes to the configuration are generally done in `.local` files.

### Global configuraton file

```bash
sudo cp /etc/fail2ban/fail2ban.conf /etc/fail2ban/fail2ban.local
```

Optional parameters to change:

- `loglevel` - the level of detail that Fail2ban’s logs provide can be set to 1 (error), 2 (warn), 3 (info), or 4 (debug).
- `logtarget` - logs actions into a specific file. The default value of `/var/log/fail2ban.log`

  puts all logging into the defined file. Alternately, you can change the value to:

  - `STDOUT`: output any data
  - `STDERR`: output any errors
  - `SYSLOG`: message-based logging
  - `FILE`: output to a file
- `socket` - the location of the socket file.
- `pidfile` - the location of the PID file.

### Jail configuration

```bash
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

Main parameters to change:

- `ignoreip = 127.0.0.1` - ignoreIP section allows you to white list certain IP addressess from blocking. Here, you can specify list of IP addresses with space separated and make sure you include your address.
- `bantime = 600` - the number of seconds that a host would be banned from the server. The default is set for 600 (600 seconds = 10 minutes).
- `findtime = 600` - the amount of time that a host has to log in. The default is set to 10 minutes, it means that if a host attempts, and fails, to log in more than the maxretry number of times, they will be banned.
- `maxretry = 3` - The number of failed login attempts before a host is blocked for the length of the ban time.
- To receive email when fail2ban is triggered, adjust the email settings:
  - `destemail` - the email address where you would like to receive the emails.
  - `sendername ` - the name under which the email shows up.
  - `sender` - the email address from which Fail2ban will send emails.

Beyond the basic settings address above, `jail.local` also contains various jail configurations for a number of common services, including SSH. By default, only SSH is enabled.

```bash
[ssh]

enabled  = true
port     = ssh
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3
```

- `enabled` - turn rule on/off.
- `port ` - port Fail2ban should be referencing in regards to the service. If using the default port, then the service name can be placed here. If using a non-traditional port, this should be the port number. For example, if you moved your SSH port to 2345, you would replace `ssh` with `2345`.
- `filter  ` - the name of the file located in `/etc/fail2ban/filter.d` that contains the failregex information used to parse log files appropriately. The `.conf` suffix need not be included.
- `logpath` - logs location.
- `maxretry` - this option will override the global `maxretry` for the defined service. `findtime` and `bantime` can also be added.
- `action` - this can be added as an additional setting, if the default action is not suitable for the jail. Additional actions can be found in the `action.d` folder.

## Failregexs

You may want to further customize these filters or create your own to suit your needs. Fail2ban uses *regular expressions* (*regex*) to parse log files, looking for instances of attempted break-ins and password failures. Fail2ban uses Python’s regex extensions.

Navigate to your website’s `access.log` (e.g. for Nginx at `/var/log/nginx/access.log`)

Find a failed login attempt (this example is created on Wordpress site):

```bash
123.123.123.123 - - [02/Dec/2017:11:40:23 -0400] "POST /wp-login.php HTTP/1.1" 200 1906 "http://example.com/wp-login.php" "Mozilla/4.0 (Windows; Intel; rv:40.0) Gecko/20100101 Firefox/40.0"
```

You will only need to track up to the `200`

So this line

```bash
123.45.67.89 - - [01/Oct/2015:12:46:34 -0400] "POST /wp-login.php HTTP/1.1" 200
```

in regex will looks like

```bash
<HOST> - - \[(\d{2})/\w{3}/\d{4}:\1:\1:\1 -\d{4}\] "POST /wp-login.php HTTP/1.1" 200
```

Go to `filter.d` directory:

```bash
cd /etc/fail2ban/filter.d
```

Create a file called `wordpress.conf`, and add your failregex:

```bash
# Fail2Ban filter for WordPress

[Definition]

failregex = <HOST> - - \[(\d{2})/\w{3}/\d{4}:\1:\1:\1 -\d{4}\] "POST /wp-login.php HTTP/1.1" 200
ignoreregex =
```

Restart service:

```plaintext
sudo service fail2ban restart
```

There is also interesting [plugin](https://blog.matrixpost.net/secure-wordpress-with-fail2ban/) for WordPress to use fail2ban with this CMS.

## Manage

Show current configuration:

```bash
sudo fail2ban-client –d7
```

Show current bans:

```bash
sudo iptables -L -n -v
```

## Latest version

Version in some Linux distribution repositories is a little old compare to the latest version.

You can find latest version on official [Github page](https://github.com/fail2ban/fail2ban). Download stable version from [release page](https://github.com/fail2ban/fail2ban/releases).

Remove your old version

```bash
sudo apt purge fail2ban
```

Extract and install new

```bash
tar xvfj fail2ban-0.10.4.tar.bz2
cd fail2ban-0.10.4
sudo python setup.py install
```

This will install Fail2Ban into the python library directory. The executable scripts are placed into `/usr/bin`, and configuration in `/etc/fail2ban`.

Fail2Ban should be correctly installed now. Just type:

```bash
fail2ban-client -h
```

to see if everything is alright. You should always use `fail2ban-client` and never call `fail2ban-server` directly. You can verify that you have the correct version installed with

```bash
fail2ban-client version
```

Please note that the system init/service script is not automatically installed. To enable Fail2Ban as an automatic service, simply copy the script for your distro from the files directory to `/etc/init.d`. Example (on a Debian-based system):

```bash
cp files/debian-initd /etc/init.d/fail2ban
update-rc.d fail2ban defaults
service fail2ban start
```

Configuration file in new version is a little different but if you understand how to configure Fail2Ban from first part of this article you will get it.
