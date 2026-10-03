[[ PAGE 1 ]]

# PortSentry - stealth scan detection

PortSentry is great attack detection tool. It detects of scans on a host. PortSentry monitors for both TCP as well as UDP scans. It is worth installing and configuring it to improve the server security. Unfortunately this tool is not developed anymore and other hardening options are better solution than using it. But in case you would like to test it, feel free.

![nmap scan](portsentry.jpg)

## Instalation

Debian/Ubuntu

```bash
apt-get install portsentry
```

Fedora/CentOS

```bash
rpm -i portsentry*
```

Arch

```bash
yaourt -S portsentry
```

## Configuration

```bash
sudo nano /etc/portsentry/portsentry.conf
```

Below you can find settings from my configuration. Adjust them to suit your needs or leave as it is to keep ports of your server safe and block any scans.

### Port configuration

Uncomment one of the following set of ports

- Un-comment these if you are really anal
- Use these if you just want to be aware
- Use these for just bare-bones

Personally I always choose the first set. By default second set is uncommented.

```bash
# Un-comment these if you are really anal:
TCP_PORTS="1,7,9,11,15,70,79,80,109,110,111,119,138,139,143,512,513,514,515,540,635,1080,1524,2000,2001,4000,4001,5742,6000,6001,6667,12345,12346,20034,30303,32771,32772,32773,32774,31337,40421,40425,49724,54320"
UDP_PORTS="1,7,9,66,67,68,69,111,137,138,161,162,474,513,517,518,635,640,641,666,700,2049,32770,32771,32772,32773,32774,31337,54321"
#
# Use these if you just want to be aware:
#TCP_PORTS="1,11,15,79,111,119,143,540,635,1080,1524,2000,5742,6667,12345,12346,20034,31337,32771,32772,32773,32774,40421,49724,54320"
#UDP_PORTS="1,7,9,69,161,162,513,635,640,641,700,32770,32771,32772,32773,32774,31337,54321"
#
# Use these for just bare-bones
#TCP_PORTS="1,11,15,110,111,143,540,635,1080,524,2000,12345,12346,20034,32771,32772,32773,32774,49724,54320"
#UDP_PORTS="1,7,9,69,161,162,513,640,700,32770,32771,32772,32773,32774,31337,54321"
```

### Advanced Stealth Scan Detection Options

Here you can add additional ports you want to monitor

```bash
ADVANCED_PORTS_TCP="1023"
ADVANCED_PORTS_UDP="1023"
```

Also you can exclude some ports here:

```bash
ADVANCED_EXCLUDE_TCP="113,139"
ADVANCED_EXCLUDE_UDP="520,138,137,67"
```

### Configuration Files

Location for ignored, history and blocked hosts.

```bash
# Hosts to ignore
IGNORE_FILE="/usr/pkg/etc/portsentry.ignore"
# Hosts that have been denied (running history)
HISTORY_FILE="/usr/pkg/etc/portsentry.history"
# Hosts that have been denied this session only (temporary until next restart)
BLOCKED_FILE="/usr/pkg/etc/portsentry.blocked"
```

### Ignore Options

```bash
# 0 = Do not block UDP/TCP scans.
# 1 = Block UDP/TCP scans.
# 2 = Run external command only (KILL_RUN_CMD)

BLOCK_UDP="1"
BLOCK_TCP="1"
```

### TCP Wrappers

```bash
KILL_HOSTS_DENY="ALL: $TARGET$"
KILL_HOSTS_DENY="ALL: $TARGET$ : DENY"
```

### Port Banner Section

Enter text in here you want displayed to a person tripping the PortSentry.

```bash
PORT_BANNER="** UNAUTHORIZED ACCESS PROHIBITED *** YOUR CONNECTION ATTEMPT HAS BEEN LOGGED. GO AWAY."
```
