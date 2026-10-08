---
id: ckb-55d371a9fc85
title: Starting with hexo.io
category: foundations-and-systems
format: guide
language: en
tags: [git, linux]
summary: This guide provides a technical walkthrough for installing and configuring the Hexo static site generator on Debian and Ubuntu systems.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.9
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:16:20Z
---

# Starting with hexo.io

I decided to run my personal web page using something light and fast. I did some research and I found [Hexo](https://hexo.io/)! This is my very first post. That was not so hard. Below you can find steps I did to create this page.

![Hexo](hexo.jpg)

## Quick Start

My installation is based on [Debian](https://www.debian.org/) server and test environment on [Xbuntu](https://xubuntu.org/) laptop.

### Dependencies

Everything you need before install Hexo is [Node.js](https://nodejs.org/) and [git](https://git-scm.com/).

#### Node.js

```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
nvm install stable
```

#### git

```bash
sudo apt-get install git-core
```

If you would like to install latest version of git here is solution.

##### Ubuntu

Add `ppa` repository and install

```bash
sudo add-apt-repository ppa:git-core/ppa 
sudo apt update
sudo apt install git
```

##### Debian

Add repository and create pinning config

```bash
sudo echo "deb http://ftp.us.debian.org/debian/ sid main contrib non-free" > /etc/apt/sources.list
sudo nano /etc/apt/preferences.d/pinning
```

Paste configuration (where n=your_codename)

```bash
Package: *
Pin: release n=jessie
Pin-Priority: 700

Package: linux-image-amd64
Pin: release *
Pin-Priority: -1
```

Install latest version

```bash
sudo apt-get -t sid install git
```

### Installation

```bash
npm install -g hexo-cli
```

Setup

```bash
hexo init <folder>
cd <folder>
npm install
```

And thats all.

*Basic configuration* and *Getting started* you can find in [Official Documentation](https://hexo.io/docs/)

### Server

To check your published files you can install `hexo-server` then run it

```bash
hexo server
```

your page will be visible at `http://localhost:4000`

### Themes

My page is using modified Cactus theme

```bash
git clone https://github.com/probberechts/hexo-theme-cactus.git themes/cactus
```

Here you can find other [Themes](https://hexo.io/themes/)

### Plugins

My page is also using few plugins

Feed generator

```bash
npm install hexo-generator-feed --save
```

Search

```bash
npm install hexo-generator-search --save
```

Sitemap generator

```bash
npm install hexo-generator-sitemap --save
```

Visit [plugin page](https://hexo.io/plugins/) for more interesting plugins.

To check installed plugins use command:

```bash
npm ls --depth 0
```

Install plugin:

```bash
sudo npm install <plugin-name> --save
```

Uninstall plugin:

```bash
sudo npm uninstall <plugin-name>
```

### Updates

Every administrator should use latest version of software. To check what version you have, get inside your Hexo instance and use command:

```bash
hexo --version
```

To update Hexo server, plugins and Npm go to your Hexo folder and run commands:

```bash
sudo npm i -g npm
```

for the `npm` update and

```bash
sudo npm update
```

for Hexo update.
