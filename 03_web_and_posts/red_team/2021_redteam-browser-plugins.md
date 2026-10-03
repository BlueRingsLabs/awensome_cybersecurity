[[ PAGE 1 ]]

# Red Team browser plugins

[How do you do, fellow kids](https://i.kym-cdn.com/photos/images/original/000/683/526/4b2.gif)? We have a beautiful, snowy day of January 2021. I was pretty busy last days, but I couldn’t miss post in January! I found very interesting browser plugin I started using. In this occasion I decided to list some cool browser extensions for pentesters. Some of them I was using in the past and some I have still installed in my browser. Nothing will replace good configured Kali environment, but some of the extensions can help you, in simple and standard tasks. Ready? Sure you are!

![HakcerTools](hacktools.jpg)

If you use something else, please let me know in comments or by email. I am happy to extend the list and to test new extensions.

## Hack Tools

This extension is described as “The all-in-one Red Team browser extension for Web Pentesters”. I discovered it at the end of last year. It is pretty useful. At the moment I am using it more like a cheat sheet for XSS, SQLi and base64 decoder or hash generator, but still learning other features.

> HackTools, is a web extension facilitating your web application penetration tests, it includes cheat sheets as well as all the tools used during a test such as XSS payloads, Reverse shells and much more.
> 
> With the extension you no longer need to search for payloads in different websites or in your local storage space, most of the tools are accessible in one click. HackTools is accessible either in pop up mode or in a whole tab in the Devtools part of the browser with F12.

More information about plugin can be found on [Github](https://github.com/LasCC/Hack-Tools). Plugin is available for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/hacktools/) and [Chrome](https://chrome.google.com/webstore/detail/hack-tools/cmbndhnoonmghfofefkcccljbkdpamhi?hl=en).

## HTTP Header Live

My must have for quick research. Before I run Burp, I always work with Http Header Live. In simple words this extension displays the HTTP header. Edit it and send it.

Official [Github](https://github.com/Nitrama/HTTP-Header-Live) page. Plugin available for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/http-header-live/) and [Chrome](https://chrome.google.com/webstore/detail/http-header-live/jljeikaiehipjcfbpedmgikbbhmknpkk).

## Tamper Data for FF Quantum

Alternative to the one above. Monitor live requests, edit headers on live requests, cancel live requests, redirect live requests.

> Capture http requests in the browser.

[Github](https://github.com/Pamblam/Tamper-Data-for-FF-Quantum) page. [Firefox](https://addons.mozilla.org/en-US/firefox/addon/tamper-data-for-ff-quantum/) only.

## Tamper Chrome

Fortunately there is Tamper plugin developed for Chrome browser with all the expected functionality.

> Tamper Dev is an extension that allows you to edit HTTP/HTTPS requests and responses as they happen without the need of a proxy.

[GitHub](https://github.com/google/tamperchrome). Official [website](https://tamper.dev/). Chrome [plugin](https://chrome.google.com/webstore/detail/tamper-dev/mdemppnhjflbejfbnlddahjbpdbeejnn).

## Wappalyzer

Identify technologies on websites. You can quickly check technologies and sometimes even versions. Good for quick reconnaissance.

> Wappalyzer is more than a CMS detector or framework detector: it uncovers more than a thousand technologies in dozens of categories such as programming languages, analytics, marketing tools, payment processors, CRM, CDN and others.

Developer [website](https://www.wappalyzer.com/). Firefox [extension](https://addons.mozilla.org/en-US/firefox/addon/wappalyzer/). Chrome [extension](https://chrome.google.com/webstore/detail/wappalyzer/gppongmhjkpfnbhagpmjfkannfbllamg?hl=en).

## HackBar

It was very popular in the past, after Firefox switched to Quantum it was rewritten. Now available for Firefox and Chrome. Allows to load, split, execute url from address bar. Custom/add referrer url, User Agent, cookie. Additional tools: md5, sha1, sha256, rot13 encryption, url, base64 encoding, beautifier json data, sql, xss features. Would be cool if all features from this plugin shows in [Hack Tools](https://github.com/LasCC/Hack-Tools).

> A HackBar for new firefox (Firefox Quantum). This addon is written in webextension and alternatives to the XUL version of original Hackbar. Press F12 to use HackBar

Firefox [plugin](https://addons.mozilla.org/pl/firefox/addon/hackbartool/). Chrome [plugin](https://chrome.google.com/webstore/detail/hackbar/djmoeoifnlhjolebkehmpaocfnipknbh).

## FoxyProxy Basic

Must have to simply switch between various proxy.

> FoxyProxy Basic is a simple on/off proxy switcher. More advanced features and configuration options are offered by FoxyProxy Standard.

Works only on [Firefox](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-basic/).

## Proxy SwitchyOmega

Great alternative to FoxyProxy for Chrome.

> Manage and switch between multiple proxies quickly & easily. Changing proxy settings has never been so convenient. Think SwitchyOmega as a modern version of the “Proxy Settings” dialog, designed to be simpler, quicker and more powerful, specially optimized for Chrome. No more digging through the advanced section in Chrome settings.

Download it [here](https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif).

## Injector

Pretty old, but still works very well.

> A free, lightweight web app bug finder. Intercept and replay web requests using custom injection lists.

Official [website](https://www.injector-addon.com/). Firefox [only](https://addons.mozilla.org/en-US/firefox/addon/injector/).

## Penetration Testing Kit

Last but not least. This one mix all features from plugins listed above.

> Penetration Testing Kit features:
> 
> 1. Dashboard - With information about client/server technologies, like Wappalyzer our PenTestKit extension can give you the same information and even more. You can see request/response information and then execute them again in request builder.
> 2. Request Builder - Need to check what happens if you send a SQL injection or XSS attack? Just use this request builder, modify the parameters, execute the request and check it right in your Chrome browser.
> 3. Recorder - This part of the extension is really good for InsightAppSec or AppSpider Enterprise users. You can record a macro and modify it right here if you need any changes, then copy or download the recorded macro and upload into directly InsightAppSec or AppSpider Enterprise. You also can record a traffic and export it as a HAR file and use for traffic authentication in AppSec products.
> 4. OWASP Security Headers - We do check for security headers like X-XSS-Protection or X-Content-Type-Options.

Official [website](https://denispodgurskii.github.io/pentestkit/). [GitHub](https://github.com/DenisPodgurskii/pentestkit). Chrome [plugin](https://chrome.google.com/webstore/detail/penetration-testing-kit/ojkchikaholjmcnefhjlbohackpeeknd/related?hl=en-GB).
