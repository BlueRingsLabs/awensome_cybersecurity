---
id: ckb-f4fea8a593ba
title: Rclone backup
category: foundations-and-systems
format: article
language: en
tags: [bash, cloud, cryptography, homelab, password-security, tls]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.94
---

# Rclone backup

Backing up data is important. Anyone who has ever lost data would agree. There is also a golden rule: “There are two kinds of people in this world—those who back up their data and those who will.”

Be smart and start doing this before you lose your data. I currently use Fedora (since [Arch users can brag what they use](https://miro.medium.com/v2/resize:fit:720/format:webp/1*ZuHOJuHW1Rajpfr8yLmZOQ.jpeg), so why not me?). I back up my laptop (btw, with encrypted disk using LUKS) to my Synology NAS (which has RAID 1 - mirror, encrypted) via SMB, but also to the cloud using the **3-2-1** rule.

**3 copies** of data (the original + 2 backups). **2 different media** (e.g. a local disk + the cloud, or disk + tape). **1 off-site copy** (e.g. in the cloud or at another location).

So in my case:

- **Copy 1:** the original data on my laptop
- **Copy 2:** a backup on my NAS (SMB)
- **Copy 3:** a backup on Proton Drive

This gives me **3 copies** on **2 different media** (NAS disk + cloud) with **1 off-site copy** ([Proton Drive](https://proton.me/drive)).

I have already written about [server backup](../../../../2019/05/25/server-backup/index.html) and [backing up in general](../../../../2021/05/18/backup-your-data/index.html). This time, however, I will go into a little more technical detail.

I asked ChatGPT to create illustrations for this article about a hacker configuring rclone. As always, it turned out weird. I don’t know why hackers are always portrayed as villains. Even in the AI’s opinion. Oh well, never mind.

![Rclone Backup](rclonebackup.webp)

## Rclone backup

First, install rclone. I use the `dnf` package manager in Fedora. Debian users probably use the `apt` package manager, and Windows users can use the installer.

```bash
sudo dnf install rclone
```

You can read more about rclone on its [official website](https://rclone.org/). Below, I will show you my configurations for SMB and Proton Drive. Based on my setup, you can set any destination that supports rclone with confidence. There are many [options](https://rclone.org/overview/).

### SMB (on NAS)

For more information about the SMB configuration, please refer to the [documentation](https://rclone.org/smb/).

Start by launching the tool and creating the first remote location. Rclone has user-friendly wizards that will guide you through the entire process.

```bash
rclone config

No remotes found, make a new one?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n

Enter name for new remote.
name> nas

Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.
...
49 / SMB / CIFS
   \ (smb)
...
Storage> 49

Option host.
SMB server hostname to connect to.
E.g. "example.com".
Enter a value.
host> NAS_IP

Option user.
SMB username.
Enter a value of type string. Press Enter for the default (hoek).
user> USERNAME

Option port.
SMB port number.
Enter a signed integer. Press Enter for the default (445).
port> 445

Option pass.
SMB password.
Choose an alternative below. Press Enter for the default (n).
y) Yes, type in my own password
g) Generate random password
n) No, leave this optional password blank (default)
y/g/n> y
Enter the password:
password: PASSWORD
Confirm the password:
password: PASSWORD

Option domain.
Domain name for NTLM authentication.
Enter a value of type string. Press Enter for the default (WORKGROUP).
domain> WORKGROUP

Option spn.
Service principal name.
Rclone presents this name to the server. Some servers use this as further
authentication, and it often needs to be set for clusters. For example:
    cifs/remotehost:1020
Leave blank if not sure.
Enter a value. Press Enter to leave empty.
spn> 

Option use_kerberos.
Use Kerberos authentication.
If set, rclone will use Kerberos authentication instead of NTLM. This
requires a valid Kerberos configuration and credentials cache to be
available, either in the default locations or as specified by the
KRB5_CONFIG and KRB5CCNAME environment variables.
Enter a boolean value (true or false). Press Enter for the default (false).
use_kerberos> 

Edit advanced config?
y) Yes
n) No (default)
y/n> n

Configuration complete.
Options:
- type: smb
- host: NAS_IP
- pass: *** ENCRYPTED ***
Keep this "nas" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y

Current remotes:

Name                 Type
====                 ====
nas                  smb
```

I test whether it works:

```bash
rclone lsd nas:/path/to/the/folder
```

I am configuring encryption for files, their names, and directory names.

```bash
rclone config

Current remotes:

Name                 Type
====                 ====
nas                  smb

e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q> n

Enter name for new remote.
name> nas-crypt

Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.
...
15 / Encrypt/Decrypt a remote
...
Storage> 15

Option remote.
Remote to encrypt/decrypt.
Normally should contain a ':' and a path, e.g. "myremote:path/to/dir",
"myremote:bucket" or maybe "myremote:" (not recommended).
Enter a value.
remote> nas:path/to/the/folder

Option filename_encryption.
How to encrypt the filenames.
Choose a number from below, or type in your own value of type string.
Press Enter for the default (standard).
   / Encrypt the filenames.
 1 | See the docs for the details.
   \ (standard)
 2 / Very simple filename obfuscation.
   \ (obfuscate)
   / Don't encrypt the file names.
 3 | Adds a ".bin", or "suffix" extension only.
   \ (off)
filename_encryption> 1

Option directory_name_encryption.
Option to either encrypt directory names or leave them intact.
NB If filename_encryption is "off" then this option will do nothing.
Choose a number from below, or type in your own boolean value (true or false).
Press Enter for the default (true).
 1 / Encrypt directory names.
   \ (true)
 2 / Don't encrypt directory names, leave them intact.
   \ (false)
directory_name_encryption> 1

Option password.
Password or pass phrase for encryption.
Choose an alternative below.
y) Yes, type in my own password
g) Generate random password
y/g> y                                  
Enter the password:
password: PASSWORD
Confirm the password:
password: PASSWORD

Option password2.
Password or pass phrase for salt.
Optional but recommended.
Should be different to the previous password.
Choose an alternative below. Press Enter for the default (n).
y) Yes, type in my own password
g) Generate random password
n) No, leave this optional password blank (default)
y/g/n> y                                  
Enter the password:
password: PASSWORD
Confirm the password:
password: PASSWORD

Edit advanced config?
y) Yes
n) No (default)
y/n> n

Configuration complete.
Options:
- type: crypt
- remote: nas:path/to/the/folder
- password: *** ENCRYPTED ***
- password2: *** ENCRYPTED ***
Keep this "nas-crypt" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y

Current remotes:

Name                 Type
====                 ====
nas                  smb
nas-crypt            crypt
```

### Proton Drive

I am now creating a second remote location on Proton Drive, similar to the first, so that I have one copy at home and one in the cloud.

```bash
rclone config

Current remotes:

Name                 Type
====                 ====
nas                  smb
nas-crypt            crypt

e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q> n

Enter name for new remote.
name> proton

Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.
...
45 / Proton Drive
...
Storage> 45

Option username.
The username of your proton account
Enter a value.
username> PROTON_EMAIL

Option password.
The password of your proton account.
Choose an alternative below.
y) Yes, type in my own password
g) Generate random password
y/g> y
Enter the password:
password: PROTON_PASSWORD
Confirm the password:
password: PROTON_PASSWORD

Option 2fa.
The 2FA code
Leave empty here — automatic 2FA will be configured later.
Enter a value. Press Enter to leave empty.
2fa> 

Edit advanced config?
y) Yes
n) No (default)
y/n> n

Configuration complete.
Options:
- type: protondrive
- username: PROTON_EMAIL
- password: *** ENCRYPTED ***
Keep this "proton" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y

Current remotes:

Name                 Type
====                 ====
nas                  smb
nas-crypt            crypt
proton               protondrive
```

To enable fully automatic backups (cron / systemd), configure the TOTP secret instead of entering a one-time 6-digit code.

```bash
SECRET='YOUR_BASE32_TOTP_SECRET'
rclone config update proton otp_secret_key "$(rclone obscure "$SECRET")"
```

Verify:

```bash
rclone config redacted | sed -n '/^\[proton\]/,/^\[/p'
```

You should see:

```bash
otp_secret_key = *** ENCRYPTED ***
```

Now rclone will generate 2FA codes automatically.

After entering the TOTP secret in the terminal, remove it from your Bash history:

```bash
history | grep -i SECRET
history -d <LINE_NUMBER>
history -w
```

Checking the connection:

```bash
rclone lsd proton:
```

The TOTP secret can be obtained from your authenticator setup.
In most authenticator apps (e.g., Aegis, Google Authenticator, etc.), you can edit the Proton entry and display the Base32 secret key used to generate the QR code. This is the value that must be provided to rclone as `otp_secret_key`.

Treat this secret like a password - anyone who has it can generate valid 2FA codes.

I am configuring encryption for files, their names, and directory names:

```bash
rclone config

Current remotes:

Name                 Type
====                 ====
nas                  smb
nas-crypt            crypt
proton               protondrive

e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q> n

Enter name for new remote.
name> proton-crypt

Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.
...
15 / Encrypt/Decrypt a remote
   \ (crypt)
...
Storage> 15

Option remote.
Remote to encrypt/decrypt.
Normally should contain a ':' and a path, e.g. "myremote:path/to/dir",
"myremote:bucket" or maybe "myremote:" (not recommended).
Enter a value.
remote> proton:path/to/dir

Option filename_encryption.
How to encrypt the filenames.
Choose a number from below, or type in your own value of type string.
Press Enter for the default (standard).
   / Encrypt the filenames.
 1 | See the docs for the details.
   \ (standard)
 2 / Very simple filename obfuscation.
   \ (obfuscate)
   / Don't encrypt the file names.
 3 | Adds a ".bin", or "suffix" extension only.
   \ (off)
filename_encryption> 1

Option directory_name_encryption.
Option to either encrypt directory names or leave them intact.
NB If filename_encryption is "off" then this option will do nothing.
Choose a number from below, or type in your own boolean value (true or false).
Press Enter for the default (true).
 1 / Encrypt directory names.
   \ (true)
 2 / Don't encrypt directory names, leave them intact.
   \ (false)
directory_name_encryption> 1

Option password.
Password or pass phrase for encryption.
Choose an alternative below.
y) Yes, type in my own password
g) Generate random password
y/g> y
Enter the password:
password: PASSWORD
Confirm the password:
password: PASSWORD

Option password2.
Password or pass phrase for salt.
Optional but recommended.
Should be different to the previous password.
Choose an alternative below. Press Enter for the default (n).
y) Yes, type in my own password
g) Generate random password
n) No, leave this optional password blank (default)
y/g/n> y
Enter the password:
password: PASSWORD
Confirm the password:
password: PASSWORD

Edit advanced config?
y) Yes
n) No (default)
y/n> n

Configuration complete.
Options:
- type: crypt
- remote: proton:path/to/dir
- password: *** ENCRYPTED ***
- password2: *** ENCRYPTED ***
Keep this "proton-crypt" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote
y/e/d> y

Current remotes:

Name                 Type
====                 ====
nas                  smb
nas-crypt            crypt
proton               protondrive
proton-crypt         crypt
```

### Backup script

After configuring rclone, I create a script that backs up my local folders to a NAS and Proton Drive.

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC1="/home/user/Desktop"
SRC2="/home/user/Documents"

for DEST in nas-crypt proton-crypt; do
  if [[ "$DEST" == "nas-crypt" ]]; then
    # flags for SMB
    FLAGS=(
      --progress
      --create-empty-src-dirs
      --links
      --stats-one-line
      --contimeout 30s
      --timeout 5m
      --low-level-retries 3
      --retries 3
      --retries-sleep 10s
      --checkers 8
      --transfers 4
    )
  else
    # flags for Proton Drive
    FLAGS=(
      --progress
      --create-empty-src-dirs
      --links
      --stats-one-line
      --fast-list
      --tpslimit 60
      --tpslimit-burst 120
      --low-level-retries 10
      --timeout 1m
      --contimeout 30s
      --retries 5
      --retries-sleep 20s
      --checkers 5
      --transfers 3
      --protondrive-replace-existing-draft=true
    )
  fi

  echo ">>> Sync $SRC1 → $DEST:Desktop"
  rclone sync "$SRC1" "$DEST:Desktop" "${FLAGS[@]}"

  echo ">>> Sync $SRC2 → $DEST:Documents"
  rclone sync "$SRC2" "$DEST:Documents" "${FLAGS[@]}"
done
```

Below is a description of the flags used for rclone:

#### General

- `--progress` - Show a live progress bar during sync (same as `-P`).
- `--create-empty-src-dirs` - Recreate source directories on the destination even if they end up empty after filtering.
- `--links` - Preserve symbolic links as symlinks.

#### Flags for **SMB** (`nas-crypt`)

- `--stats-one-line` - Output a single summary line at the end instead of periodic multi-line stats.
- `--contimeout 30s` - Maximum time to establish a connection to the SMB server (30 seconds).
- `--timeout 5m `- Maximum time for I/O operations before giving up (5 minutes).
- `--low-level-retries 3` - Retry failed low-level operations (e.g. temporary network glitches) up to 3 times.
- `--retries 3` - Retry higher-level operations (e.g. sync tasks) up to 3 times.
- `--retries-sleep 10s` - Wait 10 seconds between each high-level retry.
- `--checkers 8` - Use up to 8 parallel “checker” threads to list and compare files.
- `--transfers 4` - Use up to 4 parallel file copy threads.

#### Flags for **Proton Drive** (`proton-crypt`)

- `--stats-one-line` - As above, one summary line at the end.
- `--fast-list` - Retrieve the entire directory tree in a single API call (minimizes number of requests).
- `--tpslimit 60` - Limit metadata operations to an average of 60 HTTP requests per second.
- `--tpslimit-burst 120` - Allow short bursts up to 120 requests in a row before throttling back to 60 req/s.
- `--low-level-retries 10` - Retry transient network or API errors up to 10 times.
- `--timeout 1m`- Maximum time for I/O operations before giving up (1 minute).
- `--contimeout 30s` - Maximum time to establish an HTTP connection (30 seconds).
- `--retries 5` - Retry higher-level sync tasks up to 5 times.
- `--retries-sleep 20s` - Wait 20 seconds between each high-level retry.
- `--checkers 5` - Use up to 5 parallel “checker” threads for metadata operations.
- `--transfers 3` - Use up to 3 parallel file upload threads.
- `--protondrive-replace-existing-draft=true` - On filename conflicts, overwrite any existing draft revision rather than failing.

In my example, I only back up two folders, but you can back up as many as you want.

```bash
SRC1="/home/user/Desktop"
SRC2="/home/user/Documents"
SRC3="..."
```

Add another rclone execution after adding a new location.

```bash
...
echo ">>> Sync $SRC3 → $DEST:Desktop"
rclone sync "$SRC3" "$DEST:Desktop" "${FLAGS[@]}"

echo ">>> Sync $SRC3 → $DEST:Documents"
rclone sync "$SRC3" "$DEST:Documents" "${FLAGS[@]}"
...
```

You can always add file or directory exclusions to the script.

```bash
--exclude ".config/**" \
--exclude ".cache/**" \
--exclude "Download/**" \
--exclude "Public/**"
--exclude "virtualmachine.ova" \
--exclude "test.txt"
```

If the list is long, create a file called `excludes.txt`.

```bash
.config/**
.cache/**
Download/**
Public/**
**/virtualmachine.ova
**/test.txt
```

and add `--exclude-from excludes.txt` to the script.

You can also exclude files that are larger than a certain size:

```bash
--max-size 200M \
```

If you run the script now, a backup will be performed and the files in the target locations will be encrypted.

### Periodic execution

Of course, you can run this script manually from time to time, especially after making major changes to the files on the disk. However, it is also worth running it periodically.

To do this, create a file called `backup.service` in your home directory.

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/backup.service
```

fill it in:

```bash
[Unit]
Description=Rclone backup every 5 days

[Service]
Type=oneshot
ExecStart=/home/user/backup.sh
```

Create a timer:

```bash
nano ~/.config/systemd/user/backup.timer
```

with contents:

```bash
[Unit]
Description=Timer: backup every 5 days at 18:00 (with catch-up)

[Timer]
# every 5 days: at 1,6,11,16,21,26
OnCalendar=*-*-1/5 18:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Solution description:

- `OnCalendar=*-*-1/5 18:00:00` - Defines the calendar schedule.
  - The `*-*-1/5` means “every 5 days of the month”, i.e. days 1, 6, 11, 16, 21, 26.
  - `18:00:00` is the time of day to fire the timer.
- `Persistent=true` - If the scheduled time was missed (e.g. the machine was off), systemd will run the job immediately after the next boot/login to “catch up” on missed events.
- `WantedBy=timers.target` - Hooks this timer into the normal timer startup sequence. When you enable the timer (`systemctl --user enable backup.timer`), it creates a symlink so that `timers.target` will start it automatically at login.

Turn it on and activate the timer:

```bash
systemctl --user daemon-reload
systemctl --user enable --now backup.timer
```

Use the command below to check the status:

```bash
systemctl --user list-timers backup.timer
```

If you want it to run exactly every five days and not every few days of the month, use this:

```bash
[Timer]
OnUnitActiveSec=5d
Persistent=true
```

Then, start it manually the first time.

```bash
systemctl --user start backup.timer
```

The next ones will be exactly five days apart from the end of the last one.

To check the logs for the last backup, run:

```bash
journalctl --user -u backup.service
```

The statistics will be the same as when you run the script manually. You can narrow them down to a specific time.

```bash
journalctl --user --since "2025-07-13 00:00" -u backup.service
```

## Rclone recovery

Below are the steps to restore a backup from configured locations.

On the new system, you can configure rclone according to the above instructions, providing passwords for encryption. Alternatively, you can back up the `~/.config/rclone/rclone.conf` file. When the time comes to reinstall the system, simply install rclone and move the `rclone.conf` file to its location. Then, verify that all remote locations are configured with the `rclone listremotes` command. In my case:

```bash
nas:
nas-crypt:
proton:
proton-crypt:
```

To restore the data from the NAS drive, run the following command:

```bash
rclone sync nas-crypt:Desktop ~/Desktop --links
rclone sync nas-crypt:Dokumenty ~/Documents --links
```

or from Proton Drive:

```bash
rclone sync proton-crypt:Desktop ~/Desktop --links
rclone sync proton-crypt:Documents ~/Documents --links
```

I also encrypt the rclone configuration file using my PGP key.

```bash
gpg --list-keys

gpg --encrypt \
    --recipient "John Doe <john.doe@example.com>" \
    --output rclone.conf.gpg \
    rclone.conf
```

A file secured in this way can be stored anywhere. Use the following command to decrypt it:

```bash
gpg --decrypt \
    --output rclone.conf \
    rclone.conf.gpg
```

If you don’t have a [PGP](https://en.wikipedia.org/wiki/Pretty_Good_Privacy) key, you can use password-based symmetric encryption.

```bash
gpg --symmetric \
    --cipher-algo AES256 \
    --output rclone.conf.gpg \
    rclone.conf
```

Then, you will need to enter and save the password, for example, in[KeePassXC](https://keepassxc.org/).

## Deja Dup

Before implementing this solution, I used [Deja Dup](https://apps.gnome.org/DejaDup/), which allows you to easily back up and encrypt files to a mapped path or cloud drive. It is one of the better backup programs and has a GUI, making it more user-friendly for beginners. Deja Dup uses [Restic](https://restic.net/) as its engine.

That’s about it. Although it requires a lot of clicking, you only have to do it once. If anything ever happens to your data, you know where it is and how to recover it. You also won’t have to worry about some cloud provider having access to your files.

Periodically check the destination location to ensure that files are being created. From time to time, test the restore process by restoring your backup to a temporary folder to ensure that the entire system is functioning properly. After all, what good is a backup that doesn’t work?

May your data be safe!
