---
id: ckb-335da84b7ace
title: OpenSSH hardening
category: security-operations
format: guide
language: en
tags: [bash, hardening, linux, nist]
summary: This guide provides practical instructions for hardening OpenSSH server configurations based on CIS benchmark recommendations to improve remote access security.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.95
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:14:01Z
---

# OpenSSH hardening

If you manage or administer a server, you need secure access to it. In Windows it’s RDP ([Remote Desktop Protocol](https://en.wikipedia.org/wiki/Remote_Desktop_Protocol)), usually configured with VPN or a jump host ([jump server, jump box](https://en.wikipedia.org/wiki/Jump_server)). On Linux it is the [OpenSSH](https://www.openssh.com/) server. As I only manage Linux machines privately, I decided to share best practices and hardening options based on the [CIS benchmarks](https://www.cisecurity.org/cis-benchmarks). If you use SSH to connect to your server, you should follow the steps below to make your server and connection more secure. Of course a lot depends on your configuration and what you use your server for, but it’s always worth checking that everything is configured as well as possible. I described each configuration change to make you easier to decide if you want to implement specific configuration change.

![OpenSSH](openssh.jpg)

Why CIS benchmarks? Because they are very good and built by experts. Much more clever than me. I just took everything in one place. To make a simple guide with all the options in one place, you know that this site is in a way my private notebook, when I do something or configure it, I document my actions so that in the future when I have to do something from scratch, I have my own proven manual that I can improve with new solutions if necessary, and I do not have to start from scratch. It is better to do proper research and documentation once, and improve it later, than to have to Google everything from scratch every time. I encourage you to keep your own structured documentation and update it from time to time. Fortunately, for such basic services as the SSH server, there are not many changes. Only new features appear from time to time, but the basic principles remain the same.

Btw, you do not need necessarily share your notes in public, as I do, unless you also want to share your knowledge. Sharing knowledge has the advantage that someone can help you find the flaw in your own reasoning and make you more perfect and your knowledge base more complete. Well, unless someone decides to write a quick comment like “you are dumb, you don’t know anything, because fuck you, that’s why”.

So there are a few CIS benchmarks that have sections related to SSH server configuration. At the time of writing, there are *Distribution Independent Linux v2.0.0 - 07-16-2019*, *Debian Linux 11 Benchmark v1.0.0 - 09-22-2022*, *Ubuntu Linux 22.04 LTS Benchmark v1.0.0 - 08-30-2022* and many more related to specific distributions, but in the end they are all the same when it comes to the OpenSSH section and configuration. I focused on the three listed above because they are very close to my environment and I wanted to make sure I was not missing anything based on version or release date. For other Linux distributions, the configuration is the same.

I believe you already have installed, up and running OpenSSH. I will focus here more on configuration and hardening than installing it. But yeah, it is very easy just type `sudo apt install openssh-server` You can check if the SSH server is running and if it is added to the system startup (so that it automatically starts on boot) with the following command `sudo systemctl status ssh`. To start OpenSSH server type `sudo systemctl start ssh`. To add it to the startup type `sudo systemctl enable ssh`. When it is up and running it is configured and ready to use on default port 22.

SSH is a secure, encrypted replacement for common login services such as telnet, ftp, rlogin, rsh, and rcp. It is strongly recommended that sites abandon older clear-text login protocols and use SSH to prevent session hijacking and sniffing of sensitive data off the network.

Let’s finally start with the configuration for hardening SSH server.

## SSH Server Configuration

Once all configuration changes have been made to `/etc/ssh/sshd_config`, the sshd configuration must be reloaded.

```bash
sudo systemctl reload sshd
```

All checks and remediations below are based and copied from CIS Benchmarks for SSH server hardening with my additional comments where needed.

### Ensure permissions on /etc/ssh/sshd_config are configured

The `/etc/ssh/sshd_config` file contains configuration specifications for sshd. The command below sets the owner and group of the file to root. This file needs to be protected from unauthorized changes by non-privileged users.

**Audit**

Run the following command and verify *Uid* and *Gid* are both *0/root* and *Access* does not grant permissions to *group* or *other*:

```bash
sudo stat /etc/ssh/sshd_config
```

Proper output:

```bash
Access: (0600/-rw-------)  Uid: (    0/    root)   Gid: (    0/    root)
```

**Remediation**

Run the following commands to set ownership and permissions on `/etc/ssh/sshd_config`:

```bash
sudo chown root:root /etc/ssh/sshd_config
sudo chmod og-rwx /etc/ssh/sshd_config
```

### Ensure permissions on SSH private host key files are configured

SSH connections can be secured using both passwords and SSH private keys, but SSH keys are generally considered more secure than passwords for several reasons:

1. **Stronger Authentication**: SSH keys use asymmetric encryption, making them more secure than passwords. When you use an SSH key, you have a pair of keys: a public key and a private key. The public key can be freely shared, while the private key must be kept secret. This setup provides stronger authentication because it is much more difficult for an attacker to guess or crack your private key.
2. **No Password Guessing**: With password-based authentication, attackers can use various techniques to guess or crack your password. With SSH keys, there are no passwords to guess, making it resistant to brute-force and dictionary attacks.
3. **Automation**: SSH keys can be used in automated scripts and processes without requiring manual password entry, which is often necessary for tasks like remote server administration and file transfers.
4. **Convenience**: While this may not be a security advantage per se, SSH keys are more convenient for users as they eliminate the need to remember and enter passwords every time you connect to a remote server.
5. **Key Revocation**: If a private key is compromised, you can revoke that specific key’s access without affecting other keys or the user account’s password.

However, SSH keys are only more secure if they are properly managed. Here are some best practices for using SSH keys securely:

- **Use Strong Passphrases**: Protect your private key with a strong passphrase. This adds an extra layer of security in case the private key is ever stolen.
- **Keep Keys Secure**: Protect your private key and do not share it with anyone. Store it in a secure location.
- **Key Rotation**: Periodically rotate SSH keys to enhance security. If a key is compromised, changing the key pair ensures that the attacker no longer has access.

In summary, SSH keys are generally considered more secure than password-based authentication for SSH connections, but they require careful management to maintain their security. Using strong passphrases and implementing other security measures can further enhance the security of SSH key-based authentication.

So if you use password you can skip this check, if you use keys please continue.

An SSH private key is one of two files used in SSH public key authentication. In this authentication method, The possession of the private key is proof of identity. Only a private key that corresponds to a public key will be able to authenticate successfully. The private keys need to be stored and handled carefully, and no copies of the private key should be distributed. If an unauthorized user obtains the private SSH host key file, the host could be impersonated.

**Audit**

Run the following command and verify *Uid* is *0/root* and and *Gid* is *0/root*. Ensure group and other do not have permissions.

```bash
sudo find /etc/ssh -xdev -type f -name 'ssh_host_*_key' -exec stat {} \;
```

Proper output:

```bash
File: ‘/etc/ssh/ssh_host_rsa_key’
  Size: 1679            Blocks: 8          IO Block: 4096   regular file
Device: ca01h/51713d    Inode: 8628138     Links: 1
Access: (0600/-rw-------)  Uid: (    0/    root)   Gid: (  0/root)
Access: 2018-10-22 18:24:56.861750616 +0000
Modify: 2018-10-22 18:24:56.861750616 +0000
Change: 2018-10-22 18:24:56.873750616 +0000
 Birth: - 
  File: ‘/etc/ssh/ssh_host_ecdsa_key’ 
  Size: 227             Blocks: 8          IO Block: 4096   regular file
Device: ca01h/51713d    Inode: 8631760     Links: 1
Access: (0600/-rw-------)  Uid: (    0/    root)   Gid: (  0/root)
Access: 2018-10-22 18:24:56.897750616 +0000
Modify: 2018-10-22 18:24:56.897750616 +0000
Change: 2018-10-22 18:24:56.905750616 +0000
 Birth: -
  File: ‘/etc/ssh/ssh_host_ed25519_key’
  Size: 387             Blocks: 8          IO Block: 4096   regular file
Device: ca01h/51713d    Inode: 8631762     Links: 1
Access: (0600/-rw-------)  Uid: (    0/    root)   Gid: ( 0/root)
Access: 2018-10-22 18:24:56.945750616 +0000
Modify: 2018-10-22 18:24:56.945750616 +0000
Change: 2018-10-22 18:24:56.957750616 +0000
 Birth: -
```

**Remediation**

Run the following commands to set ownership and permissions on the private SSH host key files:

```bash
sudo find /etc/ssh -xdev -type f -name 'ssh_host_*_key' -exec chown root:root {}  \;
sudo find /etc/ssh -xdev -type f -name 'ssh_host_*_key' -exec chmod 0600 {} \;
```

### Ensure permissions on SSH public host key files are configured

Same as above, check only when key authentication is enabled.

An SSH public key is one of two files used in SSH public key authentication. In this authentication method, a public key is a key that can be used for verifying digital signatures generated using a corresponding private key. Only a public key that corresponds to a private key will be able to authenticate successfully. If a public host key file is modified by an unauthorized user, the SSH service may be compromised.

**Audit**

Run the following command and verify *Access* does not grant write or execute permissions to group or other for all returned files.

```bash
sudo find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub' -exec stat {} \;
```

Proper output:

```bash
  File: ‘/etc/ssh/ssh_host_rsa_key.pub’
  Size: 382             Blocks: 8          IO Block: 4096   regular file
Device: ca01h/51713d    Inode: 8631758     Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2018-10-22 18:24:56.861750616 +0000
Modify: 2018-10-22 18:24:56.861750616 +0000
Change: 2018-10-22 18:24:56.881750616 +0000
 Birth: -
  File: ‘/etc/ssh/ssh_host_ecdsa_key.pub’
  Size: 162             Blocks: 8          IO Block: 4096   regular file
Device: ca01h/51713d    Inode: 8631761     Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2018-10-22 18:24:56.897750616 +0000
Modify: 2018-10-22 18:24:56.897750616 +0000
Change: 2018-10-22 18:24:56.917750616 +0000
 Birth: -
  File: ‘/etc/ssh/ssh_host_ed25519_key.pub’
  Size: 82              Blocks: 8          IO Block: 4096   regular file
Device: ca01h/51713d    Inode: 8631763     Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2018-10-22 18:24:56.945750616 +0000
Modify: 2018-10-22 18:24:56.945750616 +0000
Change: 2018-10-22 18:24:56.961750616 +0000
 Birth: -
```

**Remediation**

Run the following commands to set permissions and ownership on the SSH host public key files.

```bash
sudo find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub' -exec chmod 0644 {} \;
sudo find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub' -exec chown root:root {} \;
```

### Ensure SSH Protocol is set to 2

Older versions of SSH support two different and incompatible protocols: SSH1 and SSH2. SSH1 was the original protocol and was subject to security issues. SSH2 is more advanced and secure. SSH v1 suffers from insecurities that do not affect SSH v2.

**Audit**

Run the following command and verify that output matches:

```bash
sudo grep ^Protocol /etc/ssh/sshd_config
```

Proper output:

```bash
Protocol 2
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
Protocol 2
```

This command not longer exists in newer versions of SSH. This check is still being included for systems that may be running an older version of SSH. As of OpenSSH version 7.4 this parameter will not cause an issue when included.

For example, as of this writing, the current version of OpenSSH is 9.5, which was released on 4 October 2023.

### Ensure SSH LogLevel is appropriate

*INFO* level is the basic level that only records login activity of SSH users. In many such as Incident Response, it is important to determine when a particular user on a system. The logout record can eliminate those users who disconnected, narrow the field.
*VERBOSE* level specifies that login and logout activity as well as the key fingerprint SSH key used for login will be logged. This information is important for SSH key management, especially in legacy environments. SSH provides several logging levels with varying amounts of verbosity. **DEBUG** not recommended other than strictly for debugging SSH communications since so much data that it is difficult to identify important security information.

**Audit**

Run the following command and verify that output matches:

```bash
sudo sshd -T | grep loglevel
```

Proper output:

```bash
LogLevel VERBOSE
OR
loglevel INFO
```

**Remediation**

Edit `the /etc/ssh/sshd_config` file to set the parameter as follows:

```bash
LogLevel VERBOSE
OR
loglevel INFO
```

Default Value: `LogLevel INFO`

### Ensure SSH X11 forwarding is disabled

The *X11Forwarding* parameter provides the ability to tunnel X11 traffic through the connection to enable remote graphic connections. Disable X11 forwarding unless there is an operational requirement to use X11 applications directly. There is a small risk that the remote X11 servers of users who are logged in via SSH with X11 forwarding could be compromised by other users on the X11 server. Note that even if X11 forwarding is disabled, users can always install their own forwarders.

**Audit**

Run the following command and verify that output matches:

```bash
sudo sshd -T | grep x11forwarding
```

Proper output:

```bash
X11Forwarding no
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
X11Forwarding no
```

### Ensure SSH MaxAuthTries is set to 4 or less

The *MaxAuthTries* parameter specifies the maximum number of authentication attempts permitted per connection. When the login failure count reaches half the number, error messages will be written to the syslog file detailing the login failure. Setting the *MaxAuthTries* parameter to a low number will minimize the risk of successful brute force attacks to the SSH server. While the recommended setting is 4, set the number based on site policy.

**Audit**

Run the following command and verify that output *MaxAuthTries* is 4 or less:

```bash
sudo sshd -T | grep maxauthtries
```

Proper output:

```bash
MaxAuthTries 4
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
MaxAuthTries 4
```

Default Value: `MaxAuthTries 6`

### Ensure SSH IgnoreRhosts is enabled

The *IgnoreRhosts* parameter specifies that *.rhosts* and *.shosts* files will not be used in *RhostsRSAAuthentication* or *HostbasedAuthentication*. Setting this parameter forces users to enter a password when authenticating with ssh.

**Audit**

Run the following command and verify that output matches:

```bash
sudo sshd -T | grep ignorerhosts
```

Proper output:

```bash
IgnoreRhosts yes
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
IgnoreRhosts yes
```

Default Value: `IgnoreRhosts yes`

### Ensure SSH HostbasedAuthentication is disabled

The *HostbasedAuthentication* parameter specifies if authentication is allowed through trusted hosts via the user of *.rhosts*, or */etc/hosts.equiv*, along with successful public key client host authentication. This option only applies to SSH Protocol Version 2. Even though the *.rhosts* files are ineffective if support is disabled in */etc/pam.conf*, disabling the ability to use *.rhosts* files in SSH provides an additional layer of protection.

**Audit**

Run the following command and verify that output matches:

```bash
sudo sshd -T | grep hostbasedauthentication
```

Proper output:

```bash
HostbasedAuthentication no
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
HostbasedAuthentication no
```

Default Value: `HostbasedAuthentication no`

### Ensure SSH root login is disabled

The *PermitRootLogin* parameter specifies if the root user can log in using ssh. The default is no. Disallowing root logins over SSH requires system admins to authenticate using their own individual account, then escalating to root via *sudo* or *su*. This in turn limits opportunity for non-repudiation and provides a clear audit trail in the event of a security incident.

**Audit**

Run the following command and verify that output matches:

```bash
sudo sshd -T | grep permitrootlogin
```

Proper output:

```bash
PermitRootLogin no
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
PermitRootLogin no
```

Default Value: `PermitRootLogin without-password`

### Ensure SSH PermitEmptyPasswords is disabled

The *PermitEmptyPasswords* parameter specifies if the SSH server allows login to accounts with empty password strings. Disallowing remote shell access to accounts that have an empty password reduces the probability of unauthorized access to the system.

**Audit**

Run the following command and verify that output matches:

```bash
sudo sshd -T | grep permitemptypasswords
```

Proper output:

```bash
PermitEmptyPasswords no
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
PermitEmptyPasswords no
```

Default Value: `PermitEmptyPasswords no`

### Ensure SSH PermitUserEnvironment is disabled

The *PermitUserEnvironment* option allows users to present environment options to the ssh daemon. Permitting users the ability to set environment variables through the SSH daemon could potentially allow users to bypass security controls (e.g. setting an execution path that has ssh executing trojan’d programs).

**Audit**

Run the following command and verify that output matches:

```bash
sudo sshd -T | grep permituserenvironment
```

Proper output:

```bash
PermitUserEnvironment no
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
PermitUserEnvironment no
```

Default Value: `PermitUserEnvironment no`

### Ensure only strong Ciphers are used

This variable limits the ciphers that SSH can use during communication. Weak ciphers that are used for authentication to the cryptographic module cannot be relied upon to provide confidentiality or integrity, and system data may be compromised
*The DES*, *Triple DES*, and *Blowfish* ciphers, as used in SSH, have a birthday bound of approximately four billion blocks, which makes it easier for remote attackers to obtain cleartext data via a birthday attack against a long-duration encrypted session, aka a
“*Sweet32*“ attack The *RC4* algorithm, as used in the TLS protocol and SSL protocol, does not properly combine state data with key data during the initialization phase, which makes it easier for remote attackers to conduct plaintext-recovery attacks against the initial bytes of a stream by sniffing network traffic that occasionally relies on keys affected by the Invariance Weakness, and then using a brute-force approach involving LSB values, aka the “*Bar Mitzvah*“ issue. The passwords used during an SSH session encrypted with RC4 can be recovered by an attacker who is able to capture and replay the session. Error handling in the SSH protocol; Client and Server, when using a block cipher algorithm in *Cipher Block Chaining* (CBC) mode, makes it easier for remote attackers to recover certain plaintext data from an arbitrary block of ciphertext in an SSH session via unknown vectors. The *mm_newkeys_from_blob function* in *monitor_wrap.c*, when an AES-GCM cipher is used, does not properly initialize memory for a MAC context data structure, which allows remote authenticated users to bypass intended *ForceCommand* and login-shell restrictions via packet data that provides a crafted callback address.

**Audit**

Run the following command and verify that output does not contain any of the listed weak ciphers:

```bash
sudo sshd -T | grep ciphers
```

Weak Ciphers:

```bash
3des-cbc
aes128-cbc
aes192-cbc
aes256-cbc
arcfour
arcfour128
arcfour256
blowfish-cbc
cast128-cbc
rijndael-cbc@lysator.liu.se
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file add/modify the *Ciphers* line to contain a comma separated list of the site approved ciphers.

**Example**

```bash
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
```

Default Value: `Ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com,aes128-cbc,aes192-cbc,aes256-cbc,blowfish-cbc,cast128-cbc,3des-cbc`

### Ensure only strong MAC algorithms are used

This variable limits the types of *MAC* algorithms that SSH can use during communication. *MD5* and *96-bit MAC* algorithms are considered weak and have been shown to increase exploitability in SSH downgrade attacks. Weak algorithms continue to have a great deal of attention as a weak spot that can be exploited with expanded computing power. An attacker that breaks the algorithm could take advantage of a MiTM position to decrypt the SSH tunnel and capture credentials and information.

**Audit**

Run the following command and verify that output does not contain any of the listed weak MAC algorithms:

```bash
sudo sshd -T | grep -i "MACs"
```

Weak MAC algorithms:

```bash
hmac-md5
hmac-md5-96
hmac-ripemd160
hmac-sha1
hmac-sha1-96
umac-64@openssh.com
umac-128@openssh.com
hmac-md5-etm@openssh.com
hmac-md5-96-etm@openssh.com 
hmac-ripemd160-etm@openssh.com 
hmac-sha1-etm@openssh.com
hmac-sha1-96-etm@openssh.com
umac-64-etm@openssh.com
umac-128-etm@openssh.com
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file and add/modify the MACs line to contain a comma separated list of the site approved MACs:

**Example**

```bash
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256
```

Default Value: `MACs umac-64-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com,umac-64@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1,hmac-sha1-etm@openssh.com`

### Ensure only strong Key Exchange algorithms are used

Key exchange is any method in cryptography by which cryptographic keys are exchanged between two parties, allowing use of a cryptographic algorithm. If the sender and receiver wish to exchange encrypted messages, each must be equipped to encrypt messages to be sent and decrypt messages received. Key exchange methods that are considered weak should be removed. A key exchange method may be weak because too few bits are used, or the hashing algorithm is considered too weak. Using weak algorithms could expose connections to man-in-the-middle attacks.

**Audit**

Run the following command and verify that output does not contain any of the listed weak Key Exchange algorithms:

```bash
sudo sshd -T | grep kexalgorithms
```

Weak Key Exchange Algorithms:

```bash
diffie-hellman-group1-sha1
diffie-hellman-group14-sha1
diffie-hellman-group-exchange-sha1
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file add/modify the *KexAlgorithms* line to contain a comma separated list of the site approved key exchange algorithms.

**Example**

```bash
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group14-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256
```

Default Value: `KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1`

### Ensure SSH Idle Timeout Interval is configured

The two options *ClientAliveInterval* and *ClientAliveCountMax* control the timeout of ssh sessions. When the *ClientAliveInterval* variable is set, ssh sessions that have no activity for the specified length of time are terminated. When the *ClientAliveCountMax*
variable is set, sshd will send client alive messages at every *ClientAliveInterval* interval. When the number of consecutive client alive messages are sent with no response from the client, the ssh session is terminated. For example, if the *ClientAliveInterval* is set to 15 seconds and the *ClientAliveCountMax* is set to 3, the client ssh session will be terminated after 45 seconds of idle time. Having no timeout value associated with a connection could allow an unauthorized user access to another user’s ssh session (e.g. user walks away from their computer and doesn’t lock the screen). Setting a timeout value at least reduces the risk of this happening. While the recommended setting is 300 seconds (5 minutes), set this timeout value based on site policy. The recommended setting for *ClientAliveCountMax* is 0. In this case, the client session will be terminated after 5 minutes of idle time and no keepalive messages will be sent.

**Audit**

Run the following commands and verify *ClientAliveInterval* is between 1 and 300 and *ClientAliveCountMax* is 3 or less:

```bash
sudo sshd -T | grep clientaliveinterval
sudo sshd -T | grep clientalivecountmax
```

Proper output:

```bash
ClientAliveInterval 300
ClientAliveCountMax 0
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameters according to site policy:

```bash
ClientAliveInterval 300
ClientAliveCountMax 0
```

Default Value: `ClientAliveInterval 300` and `ClientAliveCountMax 0`

### Ensure SSH LoginGraceTime is set to one minute or less

The *LoginGraceTime* parameter specifies the time allowed for successful authentication to the SSH server. The longer the *Grace* period is the more open unauthenticated connections can exist. Like other session controls in this session the *Grace* Period should be limited to appropriate organizational limits to ensure the service is available for needed access. Setting the *LoginGraceTime* parameter to a low number will minimize the risk of successful brute force attacks to the SSH server. It will also limit the number of concurrent unauthenticated connections. While the recommended setting is 60 seconds (1 Minute), set
the number based on site policy.

**Audit**

Run the following command and verify that output *LoginGraceTime* is between 1 and 60:

```bash
sudo sshd -T | grep logingracetime
```

Proper output:

```bash
LoginGraceTime 60
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
LoginGraceTime 60
```

Default Value: `LoginGraceTime 120`

### Ensure SSH access is limited

There are several options available to limit which users and group can access the system via SSH. It is recommended that at least one of the following options be leveraged:

- *AllowUsers*

  The *AllowUsers* variable gives the system administrator the option of allowing specific users to ssh into the system. The list consists of space separated user names. Numeric user IDs are not recognized with this variable. If a system administrator wants to restrict user access further by only allowing the allowed users to log in from a particular host, the entry can be specified in the form of *user@host*.
- *AllowGroups*

  The *AllowGroups* variable gives the system administrator the option of allowing specific groups of users to ssh into the system. The list consists of space separated group names. Numeric group IDs are not recognized with this variable.
- *DenyUsers*

  The *DenyUsers* variable gives the system administrator the option of denying specific users to ssh into the system. The list consists of space separated user names. Numeric user IDs are not recognized with this variable. If a system administrator wants to restrict user access further by specifically denying a user’s access from a particular host, the entry can be specified in the form of *user@host*.
- *DenyGroups*

  The *DenyGroups* variable gives the system administrator the option of denying specific groups of users to ssh into the system. The list consists of space separated group names. Numeric group IDs are not recognized with this variable.

Restricting which users can remotely access the system via SSH will help ensure that only authorized users access the system.

**Audit**

Run the following commands and verify that output matches for at least one:

```bash
sudo sshd -T | grep allowusers
sudo sshd -T | grep allowgroups
sudo sshd -T | grep denyusers
sudo sshd -T | grep denygroups
```

Proper output:

```bash
AllowUsers <userlist>
AllowGroups <grouplist>
DenyUsers <userlist>
DenyGroups <grouplist>
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set one or more of the parameter as follows:

```bash
AllowUsers <userlist>
AllowGroups <grouplist>
DenyUsers <userlist>
DenyGroups <grouplist
```

### Ensure SSH warning banner is configured

The Banner parameter specifies a file whose contents must be sent to the remote user before authentication is permitted. By default, no banner is displayed. Banners are used to warn connecting users of the particular site’s policy regarding connection. Presenting a warning message prior to the normal user login may assist the prosecution of trespassers on the computer system.

**Audit**

Run the following command and verify that output matches:

```bash
sudo sshd -T | grep banner
```

Proper output:

```bash
Banner /etc/issue.net
```

**Remediation**
Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
Banner /etc/issue.net
```

Setting up an SSH server banner using the `/etc/issue.net` file can be both a good idea and a bad idea, depending on the context and how it is used. Let’s explore the advantages and disadvantages and provide examples of its content.

**Advantages:**

1. **Customization**: The banner allows you to customize the message that users see when they connect to your SSH server. This can be helpful for conveying important information or providing a welcome message.
2. **Legal Notices**: You can use the banner to display legal disclaimers or terms of use that users must acknowledge before accessing your system. This can be helpful in certain legal and compliance contexts.
3. **Security Warning**: You can use the banner to display a security warning to make users aware of the monitoring and logging activities on the server. This can serve as a deterrent to unauthorized access.

**Disadvantages:**

1. **Security Risk**: The content of the banner is visible to anyone connecting to the SSH server. If you include sensitive information or reveal details about your system, it can potentially be used by attackers to gather information about your server.
2. **Aesthetic Impact**: In some cases, the banner may appear unprofessional or clutter the login process, especially if it’s overly long or not well-designed.
3. **False Sense of Security**: Relying solely on a banner for security warnings is not sufficient. Users may disregard or overlook the message, and it should not replace robust security measures.

**Examples of `/etc/issue.net` content:**

1. **Welcome Message**:

   ```plaintext
   Welcome to MyServer
   ```
2. **Legal Disclaimer**:

   ```plaintext
   ** WARNING: Unauthorized access prohibited! **
   By accessing this system, you agree to abide by our terms of use.
   All activities are logged.
   ```
3. **Security Warning**:

   ```plaintext
   ** WARNING: This system is monitored **
   Your IP address and actions are being logged. Unauthorized access will be prosecuted.
   ```
4. **Holiday Greetings**:

   ```plaintext
   Happy Holidays! Enjoy your stay on our server.
   ```
5. **Plain and Minimalistic**:

   ```plaintext
   ---------------------------
   This is a secure server.
   ---------------------------
   ```

When deciding whether to use an SSH banner and what its content should be, consider your specific use case, the audience connecting to your server, and your organization’s policies. If used, ensure that the content is clear, concise, and relevant to the purpose, and avoid disclosing sensitive information. It should be part of a comprehensive security strategy, not the sole defense mechanism.

### Ensure SSH PAM is enabled

*UsePAM* Enables the Pluggable Authentication Module interface. If set to “*yes*” this will enable PAM authentication using *ChallengeResponseAuthentication* and *PasswordAuthentication* in addition to PAM account and session module processing for all authentication types. When *usePAM* is set to yes, PAM runs through account and session types properly. This is important if you want to restrict access to services based off of IP, time or other factors of the account. Additionally, you can make sure users inherit certain environment variables on login or disallow access to the server.

**Audit**

Run the following command and verify that output matches:

```bash
sudo sshd -T | grep -i usepam
```

Proper output:

```bash
UsePAM yes
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
UsePAM yes
```

Impact:
If *UsePAM* is enabled, you will not be able to run sshd as a non-root user.

Default Value: `usePAM yes`

### Ensure SSH AllowTcpForwarding is disabled

SSH port forwarding is a mechanism in SSH for tunneling application ports from the client to the server, or servers to clients. It can be used for adding encryption to legacy applications, going through firewalls, and some system administrators and IT professionals use it for opening backdoors into the internal network from their home machines Leaving port forwarding enabled can expose the organization to security risks and back-doors. SSH connections are protected with strong encryption. This makes their contents invisible to most deployed network monitoring and traffic filtering solutions. This invisibility carries considerable risk potential if it is used for malicious purposes such as data exfiltration. Cybercriminals or malware could exploit SSH to hide their unauthorized communications, or to exfiltrate stolen data from the target network.

**Audit**

Run the following command and verify that output matches:

```bash
sudo sshd -T | grep -i allowtcpforwarding
```

Proper output:

```bash
AllowTcpForwarding no
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
AllowTcpForwarding no
```

Impact:

SSH tunnels are widely used in many corporate environments that employ mainframe systems as their application backends. In those environments the applications themselves may have very limited native support for security. By utilizing tunneling, compliance with SOX, HIPAA, PCI-DSS, and other standards can be achieved without having to modify the applications.

Default Value: `AllowTcpForwarding yes`

### Ensure SSH MaxStartups is configured

The *MaxStartups* parameter specifies the maximum number of concurrent unauthenticated connections to the SSH daemon. To protect a system from denial of service due to a large number of pending authentication connection attempts, use the rate limiting function of *MaxStartups* to protect availability of sshd logins and prevent overwhelming the daemon.

**Audit**

Run the following command and verify that output *MaxStartups* is 10:30:60 or matches site policy:

```bash
sudo sshd -T | grep -i maxstartups
```

Proper output:

```bash
MaxStartups 10:30:60
```

**Remediation**
Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
MaxStartups 10:30:60
```

The format is: `MaxStartups` `max:rate:burst`

1. `max`: This parameter specifies the maximum number of unauthenticated connections allowed. In example, `max` is set to 10, meaning the SSH server will allow a maximum of 10 unauthenticated connections.
2. `rate`: This parameter defines the rate at which new connections are allowed. In example, `rate` is set to 30, meaning the server allows new connections at a rate of 30 connections per second.
3. `burst`: The `burst` parameter defines how many additional connections are permitted beyond the `rate` within a short burst. In example, `burst` is set to 60, indicating that 60 additional connections are allowed within the burst before the server starts refusing new connections.

The purpose of these parameters is to prevent excessive connection attempts and protect the SSH server from potential abuse or denial-of-service (DoS) attacks. By setting limits on the number of connections and their rate, you can ensure that the SSH server remains responsive and available for legitimate users while discouraging malicious or excessive connection attempts.

In example (*MaxStartups 10:30:60*), it means that the SSH server will allow up to 10 unauthenticated connections. It will permit new connections at a rate of 30 per second, and during a burst, it will allow an additional 60 connections. If the number of unauthenticated connections exceeds these limits, the server will start refusing new connections until the rate drops below the specified limits.

### Ensure SSH MaxSessions is set to 4 or less

The *MaxSessions* parameter specifies the maximum number of open sessions permitted from a given connection. To protect a system from denial of service due to a large number of concurrent sessions, use the rate limiting function of *MaxSessions* to protect availability of sshd logins and prevent overwhelming the daemon.

**Audit**

Run the following command and verify that output *MaxSessions* is 4 or less, or matches site policy:

```bash
sudo sshd -T | grep -i maxsessions
```

Proper output:

```bash
MaxSessions 4
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
MaxSessions 4
```

### Keep OpenSSH up to date

This is my advice not from CIS Benchmark. Just keep your SSH server up to date with the latest version and update it regularly and preferably automatically. The same applies to all packages on the server.

```bash
sudo apt update && sudo apt upgrade
```

### Changing the default SSH port

This is also my advice.

Changing the default SSH port can be a security measure, but it’s not a guaranteed protection and should be part of a broader security strategy. When an attacker scans a network, they often scan a range of common ports, including the default SSH port (22). By changing the port, you make it less likely for automated scanners to identify your SSH server. However, it won’t stop a determined attacker who is specifically targeting your server.

Here are some considerations regarding changing the SSH port:

**Advantages:**

1. **Reduced Automated Scanning**: Automated network scans (like Nmap) that target the default SSH port are less likely to detect your server. This can reduce the number of random login attempts and automated attacks.
2. **Obscurity**: It adds a layer of obscurity, which can make your server less visible to casual attackers.

**Disadvantages:**

1. **Inconvenience**: Changing the port means that you and your legitimate users will need to specify the custom port when connecting. This can be inconvenient and may lead to user errors.
2. **Security Through Obscurity**: Changing the port is not a substitute for proper security practices. It should be used in addition to other security measures, not as the sole defense.
3. **Log Analysis**: Attackers who discover the non-standard port might still try to access it. Your server’s logs will show these login attempts, and you must still maintain vigilant monitoring.
4. **Port Scans**: Determined attackers may perform more comprehensive port scans, checking a wide range of ports, so they might still find your SSH server.

If you decide to change the SSH port, it’s essential to choose a port that is not reserved for other services and is not commonly used for other purposes. However, avoid using ports below 1024 unless necessary, as they often require elevated privileges to bind to.

As for the range of Nmap scans, Nmap can scan a wide range of ports, depending on the scan type and options specified. The default scan in Nmap, known as a “*quick scan*“ or “*default scan*“, generally scans the most common 1,000 ports. This includes well-known ports for services like HTTP (80), HTTPS (443), FTP (21), and SSH (22), among others.

To make your SSH server less conspicuous to default network scans, you can choose a non-standard port between 1024 and 65535. For example, ports like 2222, 8022, or 22222 are often used for this purpose. However, remember that while changing the port can add a layer of security, it should be used alongside strong password policies, public key authentication, and other security measures to ensure the overall security of your SSH server.

**Audit**

```bash
sudo sshd -T | grep -i port
```

Example of output:

```bash
port 22
```

**Remediation**

Edit the `/etc/ssh/sshd_config` file to set the parameter as follows:

```bash
port 8022
```

Impact:

You need remember to open that custom port on firewall. If you use other tools monitoring SSH connection please configure them to use this port.

### Setup a jail for SSH connection

I already created article in the past about [Fail2Ban](https://0ut3r.space/2018/05/01/fail2ban-best-jail/) software. You can check it and use to protect your SSH server.

Fail2Ban is an intrusion prevention framework written in Python that protects Linux systems and servers from brute-force attacks. You can setup Fail2Ban to provide brute-force protection for SSH on your server.

Edit your Fail2Ban jail config `/etc/fail2ban/jail.local`. Here is example with comments.

```bash
[sshd] # Name of the jail. This section is for the SSH daemon.
enabled = true # This jail is enabled and will be active.
port = ssh # The port or service name to monitor. In this case, it's monitoring SSH on the default port (22).
filter = sshd # The filter to use. The "sshd" filter is used to analyze log entries specific to the SSH daemon.
logpath = /var/log/auth.log # The log file to monitor for SSH authentication attempts. This is the standard location for SSH logs.
maxretry = 3 # The number of authentication failures allowed before banning the IP address.
findtime = 300 # A time window (in seconds) during which Fail2ban counts authentication failures. If failures occur within this window, it may result in a ban.
bantime = 3600 # The duration (in seconds) for which an IP address is banned if it exceeds the "maxretry" limit.
ignoreip = 127.0.0.1 # IP addresses listed here are whitelisted and won't be banned, even if they trigger "maxretry" failures. In this case, it's allowing connections from the localhost (127.0.0.1) to remain unrestricted.
```

In case you have different SSH port, change it here too `port = 8022`, add your IP address, to make sure that by mistake you are not block yourself.

## Example of SSHD config

Finally, an example of how to configure the SSH server, including all options, to log in with a password, with additional comments:

```bash
Port 8022 # SSH server will listen on port 8022
LogLevel INFO # Set the log level to INFO
PermitRootLogin no # Disable root login
MaxAuthTries 4 # Allow a maximum of 4 authentication attempts
MaxSessions 4 # Limit the maximum number of concurrent sessions to 4
MaxStartups 10:30:60 # Allow up to 10 unauthenticated connections at 30 connections/second with a burst of 60
IgnoreRhosts yes # Ignore .rhosts and .shosts files for added security
HostbasedAuthentication no # Disable host-based authentication
PermitEmptyPasswords no # Do not allow empty passwords
PermitUserEnvironment no # Do not allow users to set environment options
ChallengeResponseAuthentication no # Disable Challenge-Response Authentication
UsePAM yes # Use Pluggable Authentication Module (PAM) for authentication
X11Forwarding no # Disable X11 forwarding
PrintMotd no # Do not print the message of the day (MOTD)
Banner /etc/issue.net # Display the banner message from /etc/issue.net
AcceptEnv LANG LC_* # Accept environment variables LANG and LC_*
ClientAliveInterval 300 # Send a keep-alive message every 300 seconds
ClientAliveCountMax 0 # Disconnect idle sessions with no limit
LoginGraceTime 60 # Allow 60 seconds for login grace time
AllowUsers johndoe # Allow the user "johndoe" to log in
AllowTcpForwarding no # Disable TCP forwarding
Subsystem sftp /usr/lib/openssh/sftp-server  # Specify the SFTP subsystem and its location
Ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com # Specify the list of allowed encryption ciphers
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256 # Specify the list of allowed message authentication codes
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group14-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256 # Specify the list of key exchange algorithms
```

For key-based authentication for SSH you need just add to the config:

```bash
PasswordAuthentication no # Disable password authentication
PubkeyAuthentication yes # Enable public key authentication
```

Of course after you configure properly key-based authentication.

## Setting up key-based authentication for SSH

1. **Generate SSH Key Pair (Client-side):**

   If you haven’t already, you need to generate an SSH key pair on your client computer (the computer you’ll be connecting from). You can do this with the following command:

   ```bash
   ssh-keygen -t rsa -b 4096
   ```

   This command generates an RSA key pair with 4096 bits. It will prompt you for a location to save the key pair and an optional passphrase for added security. The key pair consists of a public key (usually named `id_rsa.pub`) and a private key (`id_rsa`). The private key should be kept secure and never shared.
2. **Copy the Public Key to the Server:**

   You’ll need to copy the public key (`id_rsa.pub` or the name you specified during key generation) to your SSH server. You can use the `ssh-copy-id` command or manually append the key to the `~/.ssh/authorized_keys` file on the server.

   Using `ssh-copy-id` (recommended):

   ```bash
   ssh-copy-id user@hostname
   ```

   Replace `user` with your server’s username, and `hostname` with your server’s IP address or domain name.

   Manually (not recommended unless `ssh-copy-id` is not available):

   ```bash
   cat ~/.ssh/id_rsa.pub | ssh user@hostname 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
   ```
3. **SSH Server Configuration:**

   Edit the SSH server configuration file (in `/etc/ssh/sshd_config`) on your server:

   ```bash
   sudo nano /etc/ssh/sshd_config
   ```

   Make sure the following options are set in the SSH server configuration:

   ```bash
   PasswordAuthentication no # Disable password authentication
   PubkeyAuthentication yes # Enable public key authentication
   ChallengeResponseAuthentication no # Disable challenge-response authentication
   ```

   Save the changes and exit the text editor.
4. **Restart the SSH Service:**

   After making changes to the SSH configuration, restart the SSH service to apply the new settings:

   ```bash
   sudo service ssh restart
   ```

   The specific command may vary depending on your Linux distribution.
5. **Test SSH Key Authentication:**

   Try to SSH into your server from the client machine. You should now be prompted for the passphrase of your private key, and not for a password. If you didn’t set a passphrase when generating the key, you’ll be logged in directly.

   ```bash
   ssh user@hostname
   ```

   Replace `user` with your server’s username, and `hostname` with your server’s IP address or domain name.

   By following these steps, you have set up key-based authentication for SSH and disabled password authentication.

That’s probably all on the subject of hardening SSH servers. If I have missed anything, or if you have any other good ideas, or if you would like to see a similar hardening tutorial for another service, just let me know. But for everything I recommend CIS benchmarks, they are the best and most complex.
