[[ PAGE 1 ]]

# Running own Tor Relay on a VPS

Yesterday I bought myself a new VPS. Why not? Also because the other three I have are already at full capacity.

I was a Tor relay operator twice in the past, for several years each time. I have now decided to gather all my notes together and review the project requirements once again. I have set up a new relay, hoping that the third time will be the charm. I hope this relay will last as long as I do. If you want to set up a Tor relay too and are wondering how to do it properly, you will find instructions with additional links below.

This guide walks you through a production-grade Tor Middle/Guard relay deployment on a VPS. It is NOT an Exit relay, so the legal/abuse risk is significantly lower, the attack surface is smaller, and you still contribute meaningful capacity to the Tor network.

**Primary reference:** [Relay Operations hub](https://community.torproject.org/relay/)

![Tor Relay](tor-relay.webp)

## Why run a Tor relay?

Running a Tor relay is one of the most direct ways to support online privacy and freedom of access.

- **Real support for the Tor network capacity**  
  Middle and Guard relays provide the backbone of the Tor network. More stable relays mean higher throughput, lower latency, and better anonymity for everyone.
- **Helping people bypass censorship**  
  Even non-exit relays play a critical role in enabling access to information for users in heavily censored networks. Without enough relays, bridges and anti-censorship systems like Snowflake cannot scale effectively.
- **Lower legal and operational risk (middle/guard ≠ exit)**  
  Since no traffic exits to the public internet, the risk of abuse complaints or legal issues is minimal compared to running an exit relay.
- **Low hardware and maintenance requirements**  
  A modest VPS with stable bandwidth is sufficient. Once set up correctly, a relay can run unattended for months.
- **Long-term contribution that compounds over time**  
  Relay reputation and trust increase with uptime and stability. A well-maintained relay becomes more useful to the network the longer it runs.
- **Supporting an open and decentralized internet**  
  Operating a relay is a practical way to support the idea that access to information should not depend on geography, politics, or local restrictions.
- **Contributing infrastructure, not just opinions**  
  Instead of only advocating for privacy, running a relay provides tangible infrastructure that people rely on every day.

## What we’re building here

**Middle/Guard relay**

- No “exit” traffic
- Safer for the operator
- Highly valuable to the network
- Works on a budget VPS

## Requirements (official + practical)

**Official Guard/Middle requirements include:**

- Able to handle at least 7000 concurrent connections
- At least 10 Mbit/s up/down (16 Mbit/s recommended)
- Donate 100 GB/month minimum (2 TB+ ideal)
- 512 MB RAM if <40 Mbps, 1 GB RAM if >40 Mbps
- IPv4 address (stable for at least 3 hours; static preferred)
- ~200 MB disk
- Uptime ideally 24/7

**My practical recommendation:**

- 2 GB RAM+ (especially with ipset/iptables DDoS rules + monitoring)
- 2 vCPU
- 2 TB+ monthly traffic (3 TB is a good baseline)

## Choosing the VPS

If you want the cheapest option that still feels “professional” (not barely surviving), choose something like:

- **2 vCPU**
- **2–3 GB RAM**
- **3 TB+ transfer**
- dedicated IPv4
- 1 Gbps port

Example: [RackNerd 2.5 GB KVM VPS](https://my.racknerd.com/aff.php?aff=9079&pid=924) (affiliate link)

## OS: Debian 13 (trixie)

Debian is a solid baseline for long-term relay ops. Remember to upgrade to the latest Debian release before the end-of-life date for each version. At the time of writing, Debian 13 (trixie) is supported by the Tor Project APT repository. If you are using an older or LTS-only environment, Debian 12 (bookworm) works equally well.

```bash
sudo apt update && apt upgrade -y
sudo timedatectl set-timezone UTC
```

## Time synchronization (NTP) - why it matters

Correct time is critical for Tor relays. If your clock drifts:

- relays can fail reachability checks or behave inconsistently
- consensus timing and TLS/cert validity can be impacted
- debugging becomes painful fast

Tor Project [recommends](https://community.torproject.org/relay/setup/post-install/) using NTP and setting timezone correctly.

Enable NTP:

```bash
sudo apt install -y systemd-timesyncd
sudo timedatectl set-ntp true
sudo timedatectl status
```

## Install Tor

Tor Project provides [official install instructions](https://community.torproject.org/relay/), including the modern Debian/Ubuntu source format.

### Prereqs + key

```bash
sudo apt install -y apt-transport-https gnupg lsb-release wget

wget -qO- https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc \
 | gpg --dearmor \
 | sudo tee /usr/share/keyrings/deb.torproject.org-keyring.gpg >/dev/null
```

### Create tor.source

This auto-matches your Debian suite (e.g., `trixie`):

```bash
CODENAME="$(lsb_release -cs)"

cat <<EOF | sudo tee /etc/apt/sources.list.d/tor.sources >/dev/null
Types: deb deb-src
URIs: https://deb.torproject.org/torproject.org/
Suites: ${CODENAME}
Components: main
Signed-By: /usr/share/keyrings/deb.torproject.org-keyring.gpg
EOF
```

### Install Tor

```bash
sudo apt update
sudo apt install -y tor deb.torproject.org-keyring
```

## Enable automatic security updates

```bash
sudo apt install -y unattended-upgrades apt-listchanges
```

Edit file `sudo nano /etc/apt/apt.conf.d/50unattended-upgrades`

```bash
Unattended-Upgrade::Origins-Pattern {
  "origin=Debian,codename=${distro_codename},label=Debian";
  "origin=Debian,codename=${distro_codename},label=Debian-Security";
  "origin=Debian,codename=${distro_codename}-security,label=Debian-Security";
  "origin=TorProject";
};

Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "04:00";

Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Remove-New-Unused-Dependencies "true";
```

Edit file `sudo nano /etc/apt/apt.conf.d/20auto-upgrades`

```bash
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

Test:

```bash
sudo unattended-upgrade --dry-run --debug
```

## Configure the Tor relay

Open config:

```bash
sudo nano /etc/tor/torrc
```

### Minimal production relay config (Middle/Guard)

```bash
Nickname NICKNAME_OF_YOUR_RELAY
ContactInfo NICKNAME <EMAIL@EXAMPLE.COM>

# Public IPv4 address of your VPS (replace with your own)
Address AAA.BBB.CCC.DDD

# Inbound port for Tor relay connections (IPv4-only).
# 443 is common and often reachable through restrictive networks.
ORPort 443 IPv4Only

# NOT an exit relay.
ExitRelay 0
ExitPolicy reject *:*

# Disable local SOCKS proxy (this server is a relay, not a client).
SocksPort 0

DataDirectory /var/lib/tor

## Bandwidth control (avoid provider limits)
BandwidthRate 12 MBytes
BandwidthBurst 16 MBytes

## Monthly accounting: hard cap total traffic
AccountingStart month 1 00:00
AccountingMax 2800 GBytes
```

`Address` is required here so that tools like `torutils` can correctly detect your ORPort (IP:port) and create firewall rules that still allow Tor traffic when the default INPUT policy is DROP.

This guide assumes an IPv4-only relay, which is perfectly fine and fully supported by the Tor network. If your VPS also has a public IPv6 address and you want your relay to be reachable over IPv6 as well, you can:

Add an IPv6 ORPort to your `torrc`, for example:

```plaintext
# Example – replace with your real IPv6 address
ORPort [2001:db8:1234:5678::1]:443
```

Restart Tor:

```bash
sudo systemctl restart tor@default
sudo journalctl -u tor@default -f
```

## Bandwidth & traffic limiting

Tor does not limit usage by default. You typically want controls to:

- avoid exceeding VPS monthly transfer limits
- reduce “noisy neighbor” problems
- keep relay stable and predictable

The values below are examples. Do not mix different bandwidth strategies - pick one set and keep it consistent.

### Monthly accounting (total cap)

```bash
AccountingStart month 1 00:00
AccountingMax 3370 GBytes
```

- `AccountingStart`: when counters reset (UTC recommended)
- `AccountingMax`: after reaching the cap, Tor stops relaying until the next period

### Global bandwidth caps

```bash
BandwidthRate 1.4 MBytes
BandwidthBurst 2 MBytes
```

- `BandwidthRate`: steady-state cap
- `BandwidthBurst`: short burst cap (helps absorb spikes without sustained overload)

### Relay-only caps (optional)

```bash
RelayBandwidthRate 1.3 MBytes
RelayBandwidthBurst 1.8 MBytes
```

These target *relay traffic specifically* (and can matter in mixed “client+relay” setups).  
 In a pure relay box (SocksPort 0), many operators keep it simple and use only `BandwidthRate/BandwidthBurst`.  
 Pick ONE approach and keep it consistent.

### Bandwidth calculation (why these numbers work)

```bash
BandwidthRate 12 MBytes
BandwidthBurst 16 MBytes
AccountingMax 2800 GBytes
```

- `12 MBytes/s` ≈ 96 Mbit/s sustained
- `16 MBytes/s` ≈ 128 Mbit/s short bursts

If the relay ran at the full `BandwidthRate` continuously:

```bash
12 MB/s × 60 × 60 × 24 × 30 ≈ 912 GB / month
```

In reality, Tor relays rarely operate at a perfect 24/7 maximum. Traffic fluctuates, and guard/middle relays typically consume ~1.2–2.2 TB/month at these limits.

By setting:

```bash
AccountingMax 2800 GBytes
```

we leave a safe buffer below a 3 TB provider limit, preventing overage fees, throttling, or suspension.

**Will this be a “fast” relay for the Tor network?**

Yes. A sustained ~100 Mbit/s relay with good uptime is considered solid and valuable by the Tor network. Stability and long-term availability matter more than peak throughput. This configuration avoids running the VPS “at the edge” while still providing meaningful capacity.

## Guard vs Middle relay

By default, the configuration above creates a Middle relay. A Guard relay is a relay that the Tor network selects as an *entry node* for clients.

Important points:

- You do not manually enable Guard mode.
- Guard status is assigned automatically by the Tor network over time.
- A relay typically needs:
  - good uptime
  - stable bandwidth
  - several days/weeks of continuous operation

Once trusted, the directory authorities may assign the Guard flag.

**Do I need to change my configuration to become a Guard relay?**

No additional configuration is required.

This setup is already compatible with becoming a Guard relay:

- public ORPort
- stable bandwidth limits
- no exit traffic
- long uptime

**Is being a Guard relay riskier for the operator?**

For Middle vs Guard, the difference in operator risk is minimal:

- Both are non-exit relays
- No traffic leaves Tor to the public internet
- Abuse complaints are extremely rare

From an operator perspective:

- Exit relays carry the highest risk
- Guard and Middle relays are considered low-risk and safe

### Operational considerations for Guard relays

Because guard relays are used as entry points:

- uptime consistency matters more than raw speed
- frequent restarts or IP changes reduce the chance of receiving the Guard flag
- protecting the relay from DDoS (e.g., `torutils`) is especially important

Once a relay becomes a Guard, it is even more valuable to the network, but it does not significantly change day-to-day operations for the operator.

## Firewall (iptables) - minimal and safe baseline

Firewall rules are managed dynamically and intentionally not persisted with iptables-persistent, as torutils manages rule state and ipsets independently.

Debian 13 no longer ships classic iptables as the default firewall backend. Instead, it uses nftables, and the `iptables` command may not even be installed. That’s normal - nftables is the modern Linux firewall layer and Tor works fine with it. However, tools like torutils and many community relay hardening guides still expect iptables-style commands. If you want to follow this guide as written, simply install the compatibility package:

```bash
sudo apt install -y iptables
```

### Flush old rules

```bash
sudo iptables -F
sudo ip6tables -F #optional – only if your VPS has IPv6
```

### Minimal inbound policy (IPv4)

```bash
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -j DROP
```

### Optional: IPv6 firewall (if your VPS has a public IPv6 address)

```bash
sudo ip6tables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo ip6tables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo ip6tables -A INPUT -j DROP
```

## DDoS protection at the network layer

Tor relays can be targeted by simple connection-flood DDoS attempts. `torutils` provides IPv4/IPv6 scripts that:

- track connection attempts per IP over short windows
- mark IPs as malicious when thresholds are exceeded
- block them for longer periods using **ipset**
- avoid breaking established connections
- try to avoid excessive overblocking [GitHub](https://github.com/toralf/torutils)

### torutils

```bash
sudo apt update
sudo apt install -y jq ipset iptables conntrack

sudo mkdir -p /opt/torutils
cd /opt/torutils

sudo wget -q https://raw.githubusercontent.com/toralf/torutils/main/ipv4-rules.sh -O ipv4-rules.sh
sudo chmod +x ./ipv4-rules.sh
```

Optional – if your VPS also has a public IPv6 address and you want DDoS protection for IPv6 as well:

```bash
cd /opt/torutils
sudo wget -q https://raw.githubusercontent.com/toralf/torutils/main/ipv6-rules.sh -O ipv6-rules.sh
sudo chmod +x ./ipv6-rules.sh
```

### Test rules

```bash
cd /opt/torutils
sudo ./ipv4-rules.sh test
# sudo ./ipv6-rules.sh test   # optional, only if you use IPv6
```

### Apply rules safely

Recommended by torutils: stop Tor, flush conntrack, start rules, then start Tor.

```bash
sudo systemctl stop tor
sudo conntrack -F

cd /opt/torutils
sudo ./ipv4-rules.sh start
# sudo ./ipv6-rules.sh start # optional, only if you use IPv6

sudo systemctl start tor
```

### Live watch

```bash
watch -t /opt/torutils/ipv4-rules.sh
# watch -t /opt/torutils/ipv6-rules.sh   # optional
```

### Disable iptables-persistent (important)

torutils recommends ensuring `iptables-persistent` is removed or disabled, otherwise it may overwrite rules on reboot.

```bash
sudo systemctl disable netfilter-persistent || true
sudo systemctl mask netfilter-persistent || true
```

### Cron jobs (start/save/update)

Add in crontab `sudo crontab -e`

```bash
# DDoS prevention: load rules at boot
@reboot /opt/torutils/ipv4-rules.sh start

# Save ipsets hourly so reboots keep recent data
@hourly /opt/torutils/ipv4-rules.sh save

# Update Tor authorities list daily
@daily  /opt/torutils/ipv4-rules.sh update
```

Optional for ipv6:

```bash
@reboot /opt/torutils/ipv6-rules.sh start
@hourly /opt/torutils/ipv6-rules.sh save
@daily  /opt/torutils/ipv6-rules.sh update
```

**What does “update Tor authorities list” mean?**

The torutils scripts use lists related to Tor directory authorities/network components to keep certain allow/block logic accurate over time. The `update` job refreshes that data periodically so your filtering stays aligned with current Tor authority info.

## Post-install checks (official Tor guidance)

After starting the relay, [Tor Community recommends](https://community.torproject.org/relay/setup/post-install/):

1. Verify your ORPort is reachable
2. Confirm the relay publishes descriptors
3. Understand relay lifecycle/ramp-up
4. Consider configuration management if you scale beyond 1 relay
5. Configure outage notifications (Tor Weather)

**What you want to see in logs**

```bash
sudo journalctl -u tor@default -f
```

Look for messages like:

- ORPort reachable / self-test OK
- Publishing server descriptor

Relay appears in Metrics. After a few hours it should show up on [TorMetrics](https://metrics.torproject.org/rs.html).

## Relay lifecycle

Many new operators expect instant saturation. In practice, the network needs time to measure and trust your relay. Tor Project describes phases like “unmeasured”, “remote measurement”, “ramp-up”, and “steady-state”. Check more here: [The lifecycle of a new relay](https://blog.torproject.org/lifecycle-of-a-new-relay/).

## Outage notifications

Tor Community explicitly recommends Tor Weather for relay/bridge outage notifications.

- Service: <https://weather.torproject.org/>

You can register and add your relay(s) to receive email alerts (or use your own monitoring stack).

Tor Weather can send email notifications when something unusual happens with your relay - for example if it goes offline or its bandwidth suddenly drops. After adding your relay Fingerprint, you can also enable bandwidth-based alerts.

### Threshold Bandwidth

Minimum average throughput (in KBps) below which Tor Weather considers your relay unhealthy and starts the timer.

> 1 MB/s = 1024 KBps  
>  10 MB/s ≈ 10240 KBps

During the first days a new relay:

- is “unmeasured”
- receives little traffic
- may sit almost idle

So, to avoid false positives, start with:

```bash
Threshold Bandwidth: 1500 KBps   (~1.5 MB/s)
Wait For:            8 hours
```

This way you only get alerts when the relay is really down, not just ramping up.

Once your relay shows up in Tor Metrics and keeps a more stable rate (about 2 to 3 weeks), pick a threshold around 30–40% below the normal average.

Examples:

| Typical average | Threshold Bandwidth |
| --- | --- |
| ~10 MB/s | 4000–5000 KBps |
| ~20 MB/s | 8000–10000 KBps |
| ~30 MB/s | 12000–15000 KBps |

For the waiting period:

```bash
Wait For: 6–12 hours
```

- **6 hours** → more sensitive, faster alerts
- **12 hours** → fewer alerts during normal fluctuations

Update your settings when:

- you raise limits in `torrc`
- the relay consistently carries more traffic
- Tor Metrics shows a new, stable baseline

If you intentionally power the relay down for maintenance, it’s usually easier to temporarily increase *Wait For* rather than deleting the subscription.

## Network health dashboards

- [OrNetStats](https://nusenu.github.io/OrNetStats/)
- [Metrics relay search](https://metrics.torproject.org/rs.html)

## Expectations for relay operators

Before running a relay long-term, read and follow: [Expectations for relay operators](https://community.torproject.org/policies/relays/expectations-for-relay-operators/) This covers responsible operation, community norms, and operational expectations.

## Hardening SSH with an SSH User CA

Optional, but recommended.

This section replaces “static authorized_keys” with short-lived, CA-signed SSH certificates:

- disable passwords
- no long-lived keys on the server
- centralized trust root (the CA public key)

### Create a User CA keypair (on the server)

```bash
sudo mkdir -p /etc/ssh/ca
cd /etc/ssh/ca
sudo ssh-keygen -t ed25519 -f ca_user -C "SSH User CA" -N ""
sudo chmod 600 /etc/ssh/ca/ca_user
```

You get:

- `/etc/ssh/ca/ca_user` (private CA key) - keep it secret, ideally offline backup
- `/etc/ssh/ca/ca_user.pub` (public CA key) - used by sshd to trust user certs

### Generate a user keypair (on your client machine)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C "user@example.com" -N ""
```

### Sign the user’s public key (on the server)

Copy the client public key to the server:

```bash
scp ~/.ssh/id_ed25519.pub root@YOUR_SERVER:/tmp/user.pub
```

Sign it:

```bash
sudo ssh-keygen -s /etc/ssh/ca/ca_user \
  -I user@example.com \
  -n alice,bob \
  -V +52w \
  -z 1 \
  /tmp/user.pub
```

Meaning:

- `-s`: CA private key used to sign
- `-I`: certificate identity label
- `-n`: allowed UNIX usernames (login is only permitted as these accounts)
- `-V +52w`: validity window (52 weeks)
- `-z`: serial number

This creates `/tmp/user-cert.pub`.

Copy it back to the client:

```bash
scp root@YOUR_SERVER:/tmp/user-cert.pub ~/.ssh/
```

### Configure sshd to trust only CA-signed certs

Edit:

```bash
sudo nano /etc/ssh/sshd_config
```

Add/ensure:

```bash
TrustedUserCAKeys /etc/ssh/ca/ca_user.pub

PubkeyAuthentication yes
AuthorizedKeysFile none

PasswordAuthentication no
ChallengeResponseAuthentication no
KbdInteractiveAuthentication no

PermitRootLogin no
AuthenticationMethods publickey
```

Optional: restrict users:

```bash
AllowUsers alice bob
```

Reload sshd:

```bash
sudo systemctl reload sshd
```

### Configure your SSH client

Edit `~/.ssh/config`:

```bash
Host myserver
  HostName your.server.ip.or.host
  User alice
  IdentityFile ~/.ssh/id_ed25519
  CertificateFile ~/.ssh/user-cert.pub
  IdentitiesOnly yes
```

Before disconnecting from the server, test the connection after making all changes.

```bash
ssh -vv myserver
```

If correct, the server accepts your CA-signed cert and won’t offer passwords. Now for login use:

```bash
ssh myserver
```

## Backup recommendations (important)

### Backup CA keys (server)

```bash
sudo mkdir -p ~/ssh-backup/ca
sudo cp /etc/ssh/ca/ca_user     ~/ssh-backup/ca/ca_user
sudo cp /etc/ssh/ca/ca_user.pub ~/ssh-backup/ca/ca_user.pub
```

Also store the CA private key offline. Without it you cannot sign new user certs or rotate cleanly.

### Backup client keys/cert

```bash
mkdir -p ~/ssh-backup/client
cp ~/.ssh/id_ed25519       ~/ssh-backup/client/
cp ~/.ssh/id_ed25519.pub   ~/ssh-backup/client/
cp ~/.ssh/user-cert.pub    ~/ssh-backup/client/
cp ~/.ssh/config           ~/ssh-backup/client/config.bak
```

### Backup Tor relay identity keys (MUST DO)

Losing relay keys = new fingerprint = reputation reset.

```bash
sudo tar czf /root/tor-keys-backup.tar.gz /var/lib/tor/keys
```

Store it somewhere safe (encrypted, offline copy recommended).

## Final checklist

- Debian updated, timezone UTC, NTP enabled
- Tor installed from official repo
- `SocksPort 0`, `ExitRelay 0`, `ORPort` open
- Bandwidth limits + accounting configured
- Firewall configured (IPv4, IPv6 if used)
- torutils IPv4 rules installed + cron (start/save/update)
- iptables-persistent disabled/masked
- Relay appears on Metrics
- Tor Weather notifications enabled
- SSH CA auth in place (optional but recommended)
- Tor keys backed up

## References

- [Relay Operations hub](https://community.torproject.org/relay/)
- [Relay requirements](https://community.torproject.org/relay/relays-requirements/)
- [Post-install guide](https://community.torproject.org/relay/setup/post-install/)
- [Expectations for operators](https://community.torproject.org/policies/relays/expectations-for-relay-operators/)
- [Tor Debian repo install](https://support.torproject.org/little-t-tor/getting-started/installing/)
- [Tor relay lifecycle](https://blog.torproject.org/lifecycle-of-a-new-relay/)
- [Tor Weather](https://weather.torproject.org/)
- [torutils](https://github.com/toralf/torutils)
- [OrNetStats](https://nusenu.github.io/OrNetStats/)

## A note on running a Tor Exit relay

This guide intentionally focuses on Middle/Guard relays. Running a Tor Exit relay is a very different responsibility and should not be treated as a simple extension of a normal relay setup.

### Exit relays require significantly more preparation

Operating an Exit relay means that traffic leaves the Tor network and enters the public Internet from your IP address. As a result, exit operators must be prepared for:

- abuse complaints (copyright, spam, scanning, etc.)
- misunderstandings from hosting providers or upstream ISPs
- occasional law enforcement inquiries
- higher operational and legal overhead

This does not mean exit relays are illegal - but they require serious preparation.

### What you should have before running an Exit relay

Before even considering an Exit relay, you should have:

- A provider that explicitly allows Tor Exit traffic. Many VPS providers forbid exits in their ToS. You need written confirmation or a provider known to support exits.
- Proper legal understanding in your jurisdiction. You should understand how intermediary liability works in your country and what protections (or risks) exist.
- Clear and responsive abuse handling

  - a working abuse mailbox
  - templated responses explaining Tor exits
  - links to Tor Project abuse documentation
  - willingness to answer complaints calmly and professionally
- More time and operational maturity. Exit relays are not “set and forget”. They require monitoring, communication, and sometimes rapid response.

### Why Exit relays still matter

Despite the challenges, Exit relays are essential:

- Without exits, Tor users cannot access the open Internet
- Exit capacity is often more scarce than middle/guard capacity
- Well-run exits dramatically improve Tor usability

For experienced operators with the right setup, running an Exit relay is one of the most impactful contributions to the network.

### Official Tor Project resources for Exit relay operators

If you are considering running an Exit relay, start here - do not skip the official documentation:

- [Exit relay specific guidance](https://community.torproject.org/relay/setup/exit/)
- [Expectations for relay operators](https://community.torproject.org/policies/relays/expectations-for-relay-operators/)
- [Handling abuse complaints](https://support.torproject.org/abuse/)
- [Tor Exit operator FAQ](https://support.torproject.org/relays/)

### Final recommendation

If you are new to operating Tor infrastructure, start with a Middle/Guard relay. Gain operational experience, understand Tor’s ecosystem, and build confidence. Exit relays are invaluable - but they are best run by operators who are fully prepared, informed, and willing to take on the additional responsibility.

## How to support Tor if you don’t have a VPS

Running a Tor relay or bridge is one of the best ways to support the network, but it’s not the only one. If you don’t have a VPS, can’t commit to 24/7 uptime, or simply prefer a low-effort contribution, here are great alternatives:

### Run a Snowflake proxy

Snowflake is an anti-censorship technology that helps people connect to Tor from networks where Tor is blocked. As a volunteer, you can run a Snowflake proxy by installing a browser extension or keeping a Snowflake web page open - no special infrastructure needed.

- [Official Snowflake guide](https://support.torproject.org/anti-censorship/running-snowflake/)
- [What Snowflake is](https://support.torproject.org/anti-censorship/what-is-snowflake/)
- [Snowflake Project page](https://snowflake.torproject.org/)

### Help with translations

Tor is used globally, and localization directly helps people who rely on Tor in many regions and languages.

- [Tor Community – Localization](https://community.torproject.org/localization/)
- [Join the Tor Community](https://community.torproject.org/) (other volunteer paths)

### Donate to the Tor Project

If you can’t contribute infrastructure or time, donations still make a real impact and help fund development, research, and operations.

- [Donate Tor Project](https://donate.torproject.org/)
- [Donate Tor Project using crypto](https://donate.torproject.org/cryptocurrency/)
- [Tor Project Donation FAQ](https://donate.torproject.org/faq/)

I hope that bringing all the information together in one place will help you to set up your own relay and support the Tor Project.

You can check my relay [here](https://metrics.torproject.org/rs.html#details/5135CD996C21C385268E2E223F4DB7A008D0C76E).

Enjoy!

PS: I am doing all this to claim Tor T-Shirt Award ;)
