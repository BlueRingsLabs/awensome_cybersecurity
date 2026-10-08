---
id: ckb-204b2d29c14c
title: Gemini server for 0ut3r.space
category: foundations-and-systems
format: article
language: en
tags: [networking]
summary: The author describes setting up a Gemini protocol server using Agate to serve a text-based alternative to the traditional web.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-31b-it
  confidence: 0.9
classified_by: google:gemma-4-31b-it@2026-10-07T23:50:57Z
---

# Gemini server for 0ut3r.space

Another strange thing I decided to do with 0ut3r.space was to serve it via Gemini, I mean not the full copy, but a frontage only (full copy maybe if there will be someone who wants to read it in the Gemini world). As always, I wanted to learn something new while discovering something new. Also, only real hackers serve content over Gemini (lol), and I wanted to get new visitors by allowing users from another network to access my site’s resources, thus increasing its audience and reach. If you have any ideas where else I could post blog content, let me know in the comments below the post (lol*2). Yes I know there are no comments there xD, but I’m sure you’ll find the 0ut3r.space community somewhere, you’re smart because those are the only people who read this blog, oh gosh what a bullshit…

![Gemini Protocol](gemini.png)

So what the heck is Gemini? The best would be read [Wikipedia](https://en.wikipedia.org/wiki/Gemini_(protocol)) entry and [official website](https://geminiprotocol.net/), if you are looking for shorter description I here is the best quote:

> Gemini in 100 words
>
> Gemini is a new internet technology supporting an electronic library of interconnected text documents. That’s not a new idea, but it’s not old fashioned either. It’s timeless, and deserves tools which treat it as a first class concept, not a vestigial corner case. Gemini isn’t about innovation or disruption, it’s about providing some respite for those who feel the internet has been disrupted enough already. We’re not out to change the world or destroy other technologies. We are out to build a lightweight online space where documents are just documents, in the interests of every reader’s privacy, attention and bandwidth.

Nice, right? It’s like [Gopher](https://en.wikipedia.org/wiki/Gopher_(protocol)), but fresh and much more security-oriented. I knew about Gopher and had read about it in the past, but I didn’t know about Gemini, I didn’t even know it existed.

Gemini is not going to make us all suddenly abandon the regular internet. But it is an interesting alternative for boomers like me who like to read and not be distracted by a million images, ads, pop-ups and suggestions. Even with ad blockers and all that crap, the internet doesn’t look like it used to. So you can use Gemini and feel like it used to be. Will you find different content? I don’t think so. You will definitely find something interesting, more individual and made with passion. From geeks for geeks.

But as with everything Gemini is a curiosity, at least for now. Maybe that will change in the future, but for now it can be something you get excited about very quickly, only to abandon completely after a while. A great example of this is [article by makeworld user](https://www.makeworld.space/2023/08/bye_gemini.html). I recommend reading it.

## Gemini browser

To understand this better, download the browser and look at a few pages and everything will become clear. Let me give you some of the browser projects that are actively under development.

- [Lagrange](https://github.com/skyjake/lagrange) - A Beautiful Gemini Client
- [Kristall](https://kristall.random-projects.net/) - A high-quality visual cross-platform gemini browser
- [Amfora](https://github.com/makew0rld/amfora) - A fancy terminal browser for the Gemini protocol
- [Rosy Crow](https://rosy-crow.app/) - Gemini protocol client for Android

First two also supports gopher and [finger](https://en.wikipedia.org/wiki/Finger_(protocol)) protocols. Choose one and visit some Gemini pages.

You can also browse Gemini network using web proxy.

- <https://portal.mozz.us/>
- <https://www.warmedal.se/~wobbly/>
- <https://gemini.tildeverse.org/>

### Gemini links

And here is a list of some Gemini websites good as a starting point:

- <gemini://warmedal.se/~antenna/> - Geminispace aggregator
- <gemini://geminispace.info> - public search provider for Gemini
- <gemini://gemplex.space> - experimental Search Engine for Gemini written in Go
- <gemini://kennedy.gemi.dev> - public search provider for Gemini
- <gemini://houston.gmi.bacardi55.io> - A simple tool to check if a capsule is up or not
- <gemini://tlgs.one> - Another public search provider for Gemini.

Additional Gopher info and links

- <gopher://gopher.floodgap.com/>
- <gopher://gopher.floodgap.com/1/world>

Other resources:

- <https://github.com/kr1sp1n/awesome-gemini>

## Gemini server

If you want to set up your server and share content in the Gemini network, it is quite easy and requires few resources. Uses fewer resources than a normal web server. And the content is a `gmi` file whose content is [gemtext](https://geminiprotocol.net/docs/gemtext.gmi) very similar to the [markdown](https://en.wikipedia.org/wiki/Markdown). At the end of the day, the Gemini Network is all about pure text with no quirks, along with illustrations to accompany the text.

For my setup I choose the [Agate](https://github.com/mbrubeck/agate/) server, simple and lightweight. It also has it’s own [website served in Gemini](gemini://qwertqwefsday.eu/agate.gmi). For my setup I mixed up things from these tutorials:

- [Creating and serving gemini capsules](https://diyhosting.bhh.sh/gemini.html)
- [How to install and set-up a gemini server](https://www.youtube.com/watch?v=ldPlP4xVIag)
- [How to make a gemini capsule - the protocol, not the rocket. So you too can be cool!](https://www.youtube.com/watch?v=GtCTp0YwIlY)

If you want to build more complex Gemini websites you may be interested in other server solutions to the Agate:

- [JetForce](https://github.com/michael-lazar/jetforce)
- [Spacebeans](gemini://capsule.usebox.net/spacebeans/) (this one is served on Gemini, use proper browser)

And here are my instructions, I set it up on my VPS running Debian where my 0ut3r.space website is hosted.

### Preparation

Prepare user. It is a good idea to run this service as a separate user. In general, it is good practice to run different services as separate users. This is the same approach as with Nginx, which always runs as `www-data` or `nginx` user.

```bash
sudo adduser --system --no-create-home gemini
```

The `--system` flag creates a system user without a home directory, and `--no-create-home` ensures that no home directory is created for the user. Command creates a system user, which by default has `/bin/false` as its login shell. This effectively blocks interactive logon for the user.

Prepare folders:

```bash
mkdir -p /opt/gemini/{content,cert,bin}
```

`bin` for the server, `cert` for the certificate and `content` for the Gemini page content.

Add `gemini` user permissions to these folders:

```bash
sudo chown -R gemini:gemini /opt/gemini/
sudo chmod -R u+rwx /opt/gemini/
```

### Server

Download latest Agate [release](https://github.com/mbrubeck/agate/releases):

```bash
wget https://github.com/mbrubeck/agate/releases/download/v3.3.4/agate.x86_64-unknown-linux-gnu.gz
```

Unzip content:

```bash
gunzip agate.x86_64-unknown-linux-gnu.gz
```

Rename it and allow execute:

```bash
mv agate.x86_64-unknown-linux-gnu agate
chmod +x agate
```

Agate should be placed in`/opt/gemini/bin`.

### Content

Now create content for you capsule, here is my example:

```bash
nano /opt/gemini/content/index.gmi
```

with gemtext code inside:

```markdown
# 0ut3r.space

```
  ___        _   _____
 / _ \ _   _| |_|___ / _ __ ___ _ __   __ _  ___ ___
| | | | | | | __| |_ \| '__/ __| '_ \ / _` |/ __/ _ \
| |_| | |_| | |_ ___) | |_ \__ \ |_) | (_| | (_|  __/
 \___/ \__,_|\__|____/|_(_)|___/ .__/ \__,_|\___\___|
                               |_|
```

Welcome to 0ut3r Space Gemini Capsule!

This is just a signpost in the Gemini world to the real website. Maybe if some readers are interested I will move my posts here too. Just let me know.

## Full blog articles
=> https://0ut3r.space HTTPS main 0ut3r.space website
=> http://reycdxyc24gf7jrnwutzdn3smmweizedy7uojsa7ols6sflwu25ijoyd.onion Onion mirror in Tor

## Articles importd to Gemini Capsule
=> art/cve-2023-32784.gmi CVE-2023-32784 - Hacking Keepass
=> art/windows-defender.gmi Windows Defender is enough, if you harden it

## Socials
=> https://mastodon.social/@h03k Mastodon
```

My articles are located in `/opt/gemini/content/art/` and images for the articles are in `/opt/gemini/content/img`.

Since I use the [Hexo](https://hexo.io/) content generator my article source files with articles are in markdown format so I simply convert them using [md2gemini](https://pypi.org/project/md2gemini/) Python tool to converts markdown to gemtext compatible with Gemini.

```bash
.\md2gemini.exe -w -d c:\output\ C:\source\article.md
```

Unfortunately the output was not the best and I had to tweak it manually. Maybe I will write a script to convert a hexo markdown file to gemtext.

### Certificate

The Agate server will automatically create a cert during the first run in the folder you specify in the parameter:

```bash
/opt/gemini/bin/agate --content /opt/gemini/content/ --certs /opt/gemini/cert/ --hostname capsule.example.com --lang en-US --addr 0.0.0.0:1965
```

However, if you are using a different server, here is some information on how to create your own self-signed certificate. If you are using Agate, you can skip this step.

Gemini protocol prefers self-signed certificates over those issued by trusted Certificate Authorities (CAs) for several reasons:

1. **Minimization of Complexity**: Gemini emphasizes simplicity and minimalism in its design. Using self-signed certificates eliminates the need to trust external CAs and manage them, which aligns with this philosophy.
2. **No Third-Party Dependency**: With self-signed certificates, there’s no need to rely on external institutions (such as trusted CAs), which may be more in line with the decentralization and independence ideals important to the Gemini protocol.
3. **Control Over Keys**: Users have full control over the key and certificate generation process, which can enhance the sense of security and privacy.
4. **Informality**: Gemini doesn’t require formal certificates, which are standard for protocols like HTTPS. In Gemini’s case, self-signed certificates are sufficient to provide encryption and data integrity.
5. **Security**: Self-signed certificates can be as secure as those issued by CAs, as long as keys are properly managed and stored.

In summary, Gemini prefers self-signed certificates due to their simplicity, lack of reliance on external institutions, user control over keys, informality of the protocol, and the ability to provide security and privacy without the need for a third party.

For Gemini protocol, when choosing a certificate for self-signed Gemini sites, it’s generally better to opt for the ECDSA (Elliptic Curve Digital Signature Algorithm) algorithm over RSA (Rivest-Shamir-Adleman). Here’s why:

1. **Performance**: ECDSA algorithm is typically more efficient than RSA, meaning encryption and decryption operations can be processed faster, which is significant in the context of a Gemini server handling potentially large volumes of requests.
2. **Key Size**: ECDSA keys are much shorter than RSA keys for equivalent security levels. This means ECDSA certificates generate less network and memory overhead.
3. **Security**: Currently, ECDSA is considered to offer a similar level of security to RSA but with shorter key lengths.
4. **Support for Older Clients**: It’s worth noting that older Gemini clients may not support ECDSA, in which case RSA would be necessary. However, most modern clients do support ECDSA.

The ECDSA algorithm is typically a better choice for self-signed Gemini site certificates due to its performance, smaller key size, and overall good security. However, it’s important to ensure that the client being used supports ECDSA to avoid compatibility issues. It is more up to you which one you will choose.

Here is the command to create a certificate:

```bash
sudo openssl req -new -subj "/CN=capsule.example.com" -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -days 3650 -nodes -out /opt/gemini/cert/cert.pem -keyout /opt/gemini/cert/key.pem
```

If you decide to go with RSA algorithm use this one:

```bash
sudo openssl req -new -subj "/CN=capsule.example.com" -x509 -newkey rsa:2048 -days 3650 -nodes -out /opt/gemini/cert/cert.pem -keyout /opt/gemini/cert/key.pem
```

Don’t forget to change you `CN=` to match your domain.

### Nginx configuration

I also added Nginx configuration to redirect my subdomain to Gemini protocol, it’s just additional server block and Let’s Encrypt cert for subdomain:

```bash
server {
    listen 80;
    server_name capsule.example.com;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name capsule.example.com;

    # Redirect for Gemini protocol in standard web browser
    location / {
        return 301 gemini://capsule.example.com$request_uri;
    }

    # SSL Configuration for capsule subdomain
    ssl_certificate /etc/letsencrypt/live/capsule.example.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/capsule.0ut3r.space/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
```

I created this server for the subdomain capsule.0ut3r.space so in the DNS section for the subdomain this address points to my server IP, if you create a fresh server with a new domain do not forget to set up DNS in your domain provider dashboard. I had to choose subdomain for my capsule and not main as I use Cloudflare and it doesn’t support gopher/gemini protocols.

If you only have a Gemini server, or are using the same main address for both Gemini and web server, you can skip this step. I just wanted to show you how I handled it on my server.

### Firewall

Gemini capsules are served on port `1965` so do not forget to enable it on firewall:

```bash
sudo ufw allow 1965
```

### Service

Almost everything is ready. Lets setup Agate as service.

```bash
sudo nano /etc/systemd/system/agate.service
```

Here is the content:

```bash
[Unit]
Description=Agate
After=network.target

[Service]
User=gemini
Type=simple
ExecStart=/opt/gemini/bin/agate --content /opt/gemini/content --certs /opt/gemini/cert/ --hostname capsule.example.com --lang en-US --addr 0.0.0.0:1965

[Install]
WantedBy=default.target
```

Once again, make sure that the permissions for each newly created file are OK.

```bash
sudo chown -R gemini:gemini /opt/gemini/
sudo chmod -R u+rwx /opt/gemini/
```

Enable and start Agate server.

```bash
sudo systemctl enable agate
sudo systemctl daemon-reload
sudo systemctl start agate
```

That’s it! Now go and visit your server in Gemini browser e.g. Lagrange. My URL is <gemini://capsule.0ut3r.space>.

Now I feel like a real hacker…

Issues I found:

1. I tried to use it with Cloudflare, but unfortunately it does not work with the free subscription and [gemini/gopher protocols are not supported](https://community.cloudflare.com/t/does-cloudflare-support-the-gopher-and-gemini-protocols/263447). It is probably possible with paid option and [Cloudflare Spectrum](https://www.cloudflare.com/application-services/products/cloudflare-spectrum/), but I am not able to test it. If someone ever setup Cloudflare for Gemini server I am happy to get feedback.

Update: I do not host 0ut3r.space as a capsule anymore.
