[[ PAGE 1 ]]

# TLS certificate for onion site

If you have ever dreamed about [TLS certificate](https://en.wikipedia.org/wiki/Transport_Layer_Security) for your onion site, now you can buy one. It was already possible but very expensive. If I remember correctly only [DigiCert](https://www.digicert.com/) offer certificate for onion domain, and the price is about 350 USD. It was not expensive for [Facebook](https://www.facebookcorewwwi.onion/), so they implemented it in their onion domain (click the link and check how it looks).

![tls-for-onion](tls-for-onion.png)

Now it is much cheaper thanks to [Harica](https://www.harica.gr/) (a Root CA Operator founded by [Academic Network (GUnet)](https://www.gunet.gr/en/), a civil society nonprofit from Greece). Check this great post on [Tor Project](https://blog.torproject.org/tls-certificate-for-onion-site) to get more info. Anyway, now it cost 30 USD per year.

![tls-for-onion-harica](tls-for-onion-harica.png)

Everyone knows that communication in Tor is already encrypted. So why TLS for onion?

> Our [Community portal page about onion services give you a list of reasons why a service admin would need a TLS certificate as part of their implementation](https://community.torproject.org/onion-services/advanced/https/). Here are some of them:
> 
> - Websites with complex setups and that are serving HTTP and HTTPS content
> - To help the user verify that the .onion address is indeed the site you are hosting (this would be a manual check done by the user looking at the cert registration information)
> - Some services work with protocols, frameworks, and other infrastructure that has HTTPS connection as a requirement
> - In case your web server and your tor process are in different machines
> 
> Source: <https://blog.torproject.org/>

Why I haven’t bought it yet? I have better ideas to spent 30 USD at the moment :) Anyway, I think in the near future TLS for onion will be available for free, for example provided by [Let’s Encrypt](https://letsencrypt.org/). Harrica solution is probably first big step to simplify the whole process and free certificates in the near future.

If you are one of the people who would like to buy cert and set it up, follow [Kushal guide](https://kushaldas.in/posts/get-a-tls-certificate-for-your-onion-service.html).

Also make sure you are doing it for onion v3 because Tor will [no longer support v2](https://blog.torproject.org/v2-deprecation-timeline) and support will be removed from the code base.

PS: Don’t forget to [update your Tor Browser](https://blog.torproject.org/new-release-tor-browser-10014) to the latest one ;)

PS1: [Check out](../../../../2024/02/09/tls-cert-for-onion/index.html) how I implemented it on the website you are now browsing.
