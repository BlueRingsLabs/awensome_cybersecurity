---
id: ckb-1bf54f941bc3
title: Easy GPG
category: cryptography-and-privacy
format: article
language: en
tags: [bash, cryptography, linux, password-security, privacy, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.97
---

# Easy GPG

[GNU Privacy Guard](https://en.wikipedia.org/wiki/GNU_Privacy_Guard) ([GnuPG](https://gnupg.org/) or GPG) is a complete and free implementation of the OpenPGP (also known as PGP)

> GnuPG allows you to encrypt and sign your data and communications; it features a versatile key management system, along with access modules for all kinds of public key directories. GnuPG, also known as GPG, is a command line tool with features for easy integration with other applications. A wealth of frontend applications and libraries are available. GnuPG also provides support for S/MIME and Secure Shell (ssh).

Thanks to the knowledge of GPG, you have the option of sending encrypted messages via any e-mail or service that allows communication in such a way that nobody but the recipient can read the message on the way. Cool right?

Sometimes users are afraid of complicated commands. If someone has concerns about the use of several commands, then can use the graphical frontends available for almost every operating system.

Each user must have two keys, public and private to be able to encrypt and decrypt messages.

The easiest way to understand the process is to look at the picture below

![GPG Process](gpgprocess.jpg)

*image source: [Open PGP](https://www.goanywhere.com/managed-file-transfer/encryption/open-pgp)*

So you have to create your private and public key and then learn how to share your public key, decrypt and encrypt messages. Additionally, it is also worth knowing how to sign the messages and check the signatures of others. At the beginning it seems complicated, as soon as you get it you’ll see how simple it is.

## GPG Commands

Examples for Linux. Don’t forget to [download](https://www.gnupg.org/download/index.html) version for your operating system. Commands are the same for any OS. This is just a quick guide with basics. Full documentation can be found [here](https://www.dewinter.com/gnupg_howto/english/GPGMiniHowto.html).

### Generate a GPG key pair

Just run a command:

```bash
gpg --full-generate-key
```

and follow instructions on the screen.

Specify the kind of key you want, or press Enter to accept the default RSA and RSA.
Enter the desired key size. Recommend the maximum key size of 4096.
Enter the length of time the key should be valid. Continue without any date then key doesn’t expire.
Verify that your selections are correct.
Enter your user ID information.
Type a secure passphrase. You will use this password to encrypt and decrypt messages.

Sometimes during generating, import or export you can have some errors so best solutions is to restart gpg agent

```bash
gpgconf --kill gpg-agent
```

### List secret keys

List GPG keys for which you have both a public and private key.

```bash
gpg --list-secret-keys --keyid-format
```

Example of output:

```bash
------------------------------------
sec   4096R/3BB5C34231531BA2 2019-01-01 [expires: 2020-01-01]
uid                         user user@example.com
ssb   4096R/42A457DF4AB29E7A 2019-01-01
```

From the list of GPG keys, copy the GPG key UID you’d like to use. In this example, the GPG key UID is `3BB5C34231531BA2`.

### Export public key

The public key is the key that you share with others so that they can encrypt the message for you. You can view and copy or export it in several ways. Try each option and compare the results to understand how each option works.

Print the GPG key UID, in ASCII armor format.

```bash
gpg --armor --export 3BB5C34231531BA2
```

Copy your GPG key, beginning with `-----BEGIN PGP PUBLIC KEY BLOCK-----` and ending with `-----END PGP PUBLIC KEY BLOCK-----` and share with others.

You can also export your public key to file (binary file).

```bash
gpg --export 3BB5C34231531BA2 > /tmp/my-public-key
```

or to a file as text

```bash
gpg --armour --export 3BB5C34231531BA2 > /tmp/my-public-key-text
```

You can also use email address or user name instead of UID.

```bash
gpg --export user@example.com > /tmp/my-public-key
```

```bash
gpg --export user > /tmp/my-public-key
```

### Export secret key

It is worth taking a copy of the private key and storing it, eg on an encrypted disk. Export is useful for transferring the key to another device. Never share your private key with anyone.

Export to binary file:

```bash
gpg --export-secret-key --armour > /tmp/my-private-key
```

Export to text file:

```bash
gpg --export-secret-key > /tmp/my-private-key-text
```

### Import keys

Easy like this:

```bash
gpg --import my-private-key
```

```bash
gpg --import any-public-key
```

If the key already existed, the import will fail saying ‘Key already known’. You will have to delete both the private and public key first.

### Delete keys

To delete the public key

```bash
gpg --delete-keys user@example.com
```

To delete the private key

```bash
gpg --delete-secret-keys user@example.com
```

### Sending to key server

Example of sending key to public key directory.

```bash
gpg --keyserver "hkp://keyserver.ubuntu.com" --send-key 3BB5C34231531BA2
```

Retrieving the key from the server

```bash
gpg --keyserver "hkp://keyserver.ubuntu.com" --recv-keys 3BB5C34231531BA2
```

### Fingerprints

If you want to see “Fingerprints” to ensure that somebody is really the person they claim (like in a telephone call). This command will result in a list of relatively small numbers.

```bash
gpg --fingerprint
```

After import key verify it by displaying fingerprint and contact with owner to compare fingerprint.

### Revoke a key

For several reasons you may want to revoke an existing key. For instance: the secret key has been stolen.

Create revoke certificate:

```bash
gpg --gen-revoke user@example.com
```

It will look like this:

```bash
-----BEGIN PGP PUBLIC KEY BLOCK-----
 Version: GnuPG v1.2.6 (GNU/Linux)
 Comment: A revocation certificate should follow
 
 iEkEIBECAAkFAkGgoKsCHQAACgkQZYUAdmML6D/RDQCgrRNm4cjauVRvtz3QWVdm
 0ZgDsP4An1tpIXoiO5P7G385m/KR/mGkm5sr
 =piFr
 -----END PGP PUBLIC KEY BLOCK-----
```

If you import it like a normal key then it revoke the one for which it was generated.

```bash
gpg --import /tmp/revoke_cert
```

### Key signing

Signing a key means expressing that you have checked that the user really belongs to that key. You should only sign a key as being authentic when you are ABSOLUTELY SURE that the key is really authentic!!!

```bash
gpg --edit-key user@example.com
```

we will enter the interactive mode, then write

```bash
sign
```

Based on the available signatures and “ownertrusts” GnuPG determines the validity of keys. Ownertrust is a value that the owner of a key uses to determine the level of trust for a certain key. The values are:

```bash
1 = Don't know
2 = I do NOT trust
3 = I trust marginally
4 = I trust fully
```

You can check results:

```bash
check
```

save changes and quit:

```bash
quit
```

We set the trust for the key on its own and it is personal information. This means that it is not exported with the key. It is even stored in a separate file.

### Key trust

Trusting a key means that you will accept signatures from it.

Determining key trust:

```bash
gpg --edit-key user@example.com
```

in interactive mode write:

```bash
trust
```

Values:

```bash
1 = I don't know or won't say
2 = I do NOT trust
3 = I trust marginally
4 = I trust fully
5 = I trust ultimately
```

save changes and quit:

```bash
quit
```

## Encrypt

Encryption of a text file (binary)

```bash
gpg -r recipent --encrypt /tmp/message.txt --output /tmp/message.gpg
```

Where `recipent` is the name of someone’s public key. Check your public key list `gpg --list-keys`. To see the signatures as well type `gpg --list-sigs`. This file is ready to send to your recipient.

To make it possible to copy the content, for example, to send it by e-mail

```bash
gpg -r recipent --encrypt /tmp/message.txt --armour --output /tmp/message.gpg
```

now you can open the file or display its contents in the console

```bash
cat /tmp/message.gpg
```

Copy your encrypted message, beginning with `-----BEGIN PGP MESSAGE-----` and ending with `-----END PGP MESSAGE-----` and send by email or communicator.

You can also just paste text into the console and get encrypted output to copy.

```bash
echo "This is a secret message" | gpg --encrypt --armor -r recipient@example.com
```

## Decrypt

Decrypting the message:

```bash
gpg --decrypt /tmp/message.gpg
```

You will be asked for the password for your private key and you will see the decrypted message when you enter it.

Descyrpt just pasted text:

```bash
echo "Decrypted Message Text" | gpg --decrypt
```

### Sign and verify

Signing a message:

```bash
gpg --sign /tmp/message.txt --armour --output /tmp/message.sig
```

veryfing the signature:

```bash
gpg --verify /tmp/message.sig
```

and veryfing and decrypting with help

```bash
gpg --decrypt /tmp/message.sig
```

to sign in a text form for people without gpg

```bash
gpg --clearsign /tmp/message.txt --output /tmp/message.sig
```

signing without modification of the text file with the signature in a separate file

```bash
gpg --detach-sig /tmp/message.txt --output /tmp/message.sig
```

then you verify with two files

```bash
gpg --verify /tmp/message.sig /tmp/message.txt
```

### Encryption without a key

You can use symmetric encryption to encrypt a file without having a key with a one-time password.

```bash
gpg --symmetric /tmp/message.txt --armour --output /tmp/message-sym.gpg 
```

Then provide the password with a separate secure channel other than the message itself.

## Frontends and other software

There are several graphical interfaces for the GPG. Here are some examples.

- Windows - [Gpg4win](https://gpg4win.org/index.html)
- MacOS - [GPG Suite](https://gpgtools.org/)
- Android - [OpenKeychain](https://www.openkeychain.org/)
- Linux - [Seahorse](https://wiki.gnome.org/Apps/Seahorse) as key manager and [Geany](https://www.geany.org/) editor with [GeanyPG](https://plugins.geany.org/geanypg.html) plugin.

Full list of frontends and software support GPG can be found [here](https://www.gnupg.org/software/frontends.html).

## Active key servers

There is a lot of dead links to key servers, where you can share you public key. The issues with PGP keyservers were more broadly related to the fact that they allowed anyone to upload PGP keys to the server without necessarily verifying the identity of the key owner. This led to various concerns, such as the potential for spam, misuse, and the inclusion of fake or malicious keys.

In 2019, a research paper titled “[Key Reinstallation Attacks: Forcing Nonce Reuse in WPA2](https://papers.mathyvanhoef.com/ccs2017.pdf)“ also highlighted vulnerabilities in the OpenPGP and S/MIME email encryption protocols. As a result, some keyservers took actions to mitigate potential risks. For instance, some keyservers disabled certain features or deprecated specific keyserver pools.

Additionally, there were incidents where individuals’ personal information, including email addresses, were exposed on keyservers, raising privacy issues. As a response to these concerns, some keyserver operators decided to shut down or limit their services.

Here are the servers that remain operational and active:

hkp://pgp.mit.edu
hkp://keyserver.ubuntu.com
hkp://keyring.debian.org
