---
id: ckb-c7ef9f7eb533
title: Debian LEMP stack
category: foundations-and-systems
format: article
language: en
tags: [bash, cryptography, linux, privilege-escalation, threat-intelligence, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.83
---

# Debian LEMP stack

There is a lot of guides how to configure [Nginx](https://nginx.org/), [MariaDB](https://mariadb.org/) and [PHP](http://www.php.net/) on [Linux](https://en.wikipedia.org/wiki/Linux). A lot of them is outdated. Probably someday this one get out of date too… no wait! This one will be different, always fresh!

No matter what version of [Debian](https://www.debian.org/) you use, your Nginx, MariaDB and PHP (8.1) will be always up to date.

![Lemp Stack](lemp.jpg)

I will not argue my decision about such and no other configuration, I just like Nginx and MariaDB. Rather, I will focus on showing the configuration that will allow us to use the latest versions of each program. Most applications from the official repositories of a given distribution are not in the latest version. Of course, this is due to the desire to maintain stability. Personally, I use the solution described in this article and never complained about errors or instability. However, before you implement such a solution, or try to update an existing infrastructure, first make sure that everything goes smooth in the test environment. The fact that it works for me does not mean that it will also work for you :)

Install necessary packages:

```bash
sudo apt install curl gnupg2 ca-certificates lsb-release debian-archive-keyring
```

Repositories. It’a all about repositories. Before you set up new repository for your server, you need to know what version of Debian you are using. The `codename`. To check `codename` use command below:

```bash
sudo lsb_release -sc
```

To see more info about your system you can use:

```bash
sudo lsb_release -a
```

Example result of command:

```bash
Distributor ID:	Debian
Description:	Debian GNU/Linux 12 (bookworm)
Release:	12
Codename:	bookworm
```

As you now know the `codename` of your server you can use the `codename` name in the configuration below.

## Nginx

Download signing key. For any config files changes use your favorite editor. Mine is [nano](https://www.nano-editor.org/). You can find latest [official Nginx repos here](http://nginx.org/en/linux_packages.html#Debian).

```bash
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
```

add it:

```bash
gpg --dry-run --quiet --no-keyring --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg
```

add official stable Nginx repository:

```bash
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
http://nginx.org/packages/debian `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
```

If you would like to use mainline Nginx packages, run the following command instead:

```bash
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
http://nginx.org/packages/mainline/debian `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
```

Now you can update package list and install latest version of Nginx:

```bash
sudo apt update && sudo apt install nginx
```

Congrats, you have latest version of Nginx!

Clean Nginx from official repo is not tweaked as Debian prepared version called `nginx-full`. You will need to spend some time to configure it.

## PHP

Similar steps like above.

Add repository:

```bash
sudo sh -c 'echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list'
```

Download and add repository key:

```bash
sudo wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
```

Update package list and install PHP 8.2-fpm:

```bash
sudo apt update && sudo apt install php8.2-fpm
```

and then PHP itself:

```bash
sudo apt install php8.2
```

It is also worth to setup repository pining to make sure you are installing from official source and not default Debian repo:

```bash
echo -e "Package: php*\nPin: origin packages.sury.org\nPin-Priority: 900\n" \
    | sudo tee /etc/apt/preferences.d/99php
```

This will make `packages.sury.org` priority.

To chek you php version run:

```bash
sudo php -v
```

You may also be interested in additional PHP modules, like for WordPress:

```bash
sudo apt install php-bcmath php-curl php-gd php-imagick php-intl php-json php-mcrypt php-mysql php-ssh2 php-xml php-zip php-apcu php-mbstring php-soap php-igbinary php-memcached
```

Congrats, you have latest version of PHP 8.2!

## MariaDB

Before you install latest MariaDB you need to check for repository on [MariaDB repository page](https://downloads.mariadb.org/mariadb/repositories/).

Go to page, choose your Linux Distribution, Release/Codename and then mirror.

Install required package:

```bash
sudo apt install apt-transport-https curl
```

Add repository key:

```bash
sudo mkdir -p /etc/apt/keyrings
sudo curl -o /etc/apt/keyrings/mariadb-keyring.pgp 'https://mariadb.org/mariadb_release_signing_key.pgp'
```

Add repository to your source.list

```bash
sudo nano /etc/apt/sources.list.d/mariadb.sources
```

File should contain:

```bash
# MariaDB 10.11 repository list - created 2023-07-30 13:57 UTC
# https://mariadb.org/download/
X-Repolib-Name: MariaDB
Types: deb
# deb.mariadb.org is a dynamic mirror if your preferred mirror goes offline. See https://mariadb.org/mirrorbits/ for details.
# URIs: https://deb.mariadb.org/10.11/debian
URIs: https://ftp.bme.hu/pub/mirrors/mariadb/repo/10.11/debian
Suites: sid
Components: main
Signed-By: /etc/apt/keyrings/mariadb-keyring.pgp
```

Update package list and install MariaDB:

```bash
sudo apt update && sudo apt install mariadb-server mariadb-client mariadb-backup
```

After all configure it using wizard:

```bash
sudo mariadb-secure-installation
```

Congrats, you have latest version of MariaDB!

## Extra steps

Additional steps worth to make. Additional information.

### SSL

You may be interested to add free [Let’s Encrypt](https://letsencrypt.org/) certificate, to make communication with your web server secure. Check my guide how to do that: [Let’s Encrypt SSL Cert for Nginx](https://0ut3r.space/2018/09/05/lets-encrypt-ssl-cert-for-nginx/)

### Nginx configuration

Nginx configuration adjust:

```bash
sudo nano /etc/nginx/nginx.conf
```

Edit/add line:

```bash
keepalive_timeout 2;
```

Sometimes after installation or restarting Nginx you can get error like this:

```bash
Starting nginx: nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
```

Fix it using this command:

```bash
sudo fuser -k 80/tcp
```

### PHP FPM

If [php-fpm](https://php-fpm.org/) (alternative for [PHP FastCGI](https://en.wikipedia.org/wiki/FastCGI)) is your favorite process manager for PHP, edit your website configuration:

```bash
sudo nano /etc/nginx/conf.d/default.conf
```

and change line with `php section` :

```bash
location ~ \.php$ {
    try_files $uri =404;
    include /etc/nginx/fastcgi_params;
    fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_split_path_info ^(.+\.php)(/.+)$;
}
```

edit `php.ini`

```bash
sudo nano /etc/php/8.2/fpm/php.ini
```

change option `cgi.fix_pathinfo`

```bash
cgi.fix_pathinfo=0
```

Choose proper web server user for PHP. This is additional settings because we are using official Nginx repo and not the one prepared by Debian. So user is not www-data anymore, but nginx.

```bash
sudo nano /etc/php/8.2/fpm/pool.d/www.conf
```

and find parameters listed below and set them as listed:

```bash
user = nginx
group = nginx
listen = /run/php/php8.2-fpm.sock
listen.owner = nginx
listen.group = nginx
```

Reload php-fpm service:

```bash
sudo systemctl reload php8.2-fpm
```

### PHP Info

If you would like to check your PHP configuration, create `info.php` file in your www location:

```bash
sudo nano /var/www/html/info.php
```

put this code to this file:

```php
<?php
phpinfo();
?>
```

and navigate to that file in your browser:

`http://example.com/info.php`

Don’t forget to delete this file if not needed anymore.

### Database creation

Login to your database server:

```bash
sudo mysql
```

Create database:

```plaintext
CREATE DATABASE database_name;
```

Create user and password:

```plaintext
CREATE USER 'user_name'@'%' IDENTIFIED BY 'password';
```

Authorize the user to have complete control over the database:

```plaintext
GRANT ALL PRIVILEGES ON database_name.* TO 'user_name'@'%';
```

Forces immediate application of changes in privileges.

```plaintext
FLUSH PRIVILEGES;
```
