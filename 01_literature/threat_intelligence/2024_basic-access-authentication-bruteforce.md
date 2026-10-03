[[ PAGE 1 ]]

# Basic access authentication bruteforce

Sometimes people try a simple way to hide access to parts of the site using the [basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) method based on HTTP user agent. It’s not very sophisticated, or super effective, but you can often come across this solution. It will definitely block a regular user and if the login and password is not `admin` and `12345` it will definitely stop someone. I often come across using this solution as the first security, for example, the admin login interface has an `example.com/admin` address and this part of the site is additionally blocked by basic access authentication. Recently I got the admin credentials (don’t as me how) for logging into one system, but basic access authentication got in the way. I already thought I was an admin, yet such a simple solution stopped me for a while.

![basic authentication](basicauthentication.webp)

Yes, you hear right, for a while, because mostly this login and password is short and simple. Everyone sets something simple there and shows more effort only in the target system to have a complicated password and saved in KeePass. It is not a rule, but in my career basic auth stopped me only once, and it was not today :)

The only difficulty for a young student of the hacking arts to perform brute force attack for that login form is that the login and password are sent as encoded string using [Base64](https://en.wikipedia.org/wiki/Base64). For example `admin:superpassword` looks like the following `YWRtaW46c3VwZXJoYXPFgm8=`. You can test it and decode [here](https://www.base64decode.org/). Below I’ll show you two of the many ways to prepare a proper payload and execute an attack.

## Using Burp

I assume you already know the basics of [Burp](https://portswigger.net/burp/communitydownload). So intercept the request with the provided fake login and password field and send it to the intruder.

Look for a request with an `Authorization:` part.

```html
GET /admin HTTP/2
Host: example.com
Cache-Control: max-age=0
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Sec-Ch-Ua: "Not?A_Brand";v="99", "Chromium";v="130"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
```

In Burp decode Base64 string, select string and `Right Click->Convert Selection->Base64->Base64-decode`. You can also use [CyberChief](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)) to practice decoding and using the CyberChief tool.

Once decoded you can see that login and pass looks like `username:password`. Now we need to prepare input and encode it to be able to push it and bruteforce auth form.

Select encoded content `§username:password§`. Attack type is `Sniper attack`. Payload type is `Brute Forcer`. In payload processing, add prefix for user `admin:` and Base64-Encode. It is important to remove the `=` character for encoding, because `=` is used by Base64 for padding. The complete setup can be seen on the screenshot below.

![SniperAttack](sniperattack.webp)

If you also want to add a list of users and a list of passwords, select `Cluster bomb attack`, your first payload list then will be a simple list with users in the form of `usernam1:`, `username2:` etc., with payload processing only Base64 encoding and the second payload will also be a simple list but, with passwords, also encoded.

![Cluster bomb payload 1](clusterbomb1.webp)

![Cluster bomb payload 2](clusterbomb2.webp)

Thanks to these two examples, you can combine whatever you want. But there is an even simpler solution.

## Using ffuf

[Fuff](https://github.com/ffuf/ffuf) is a great fuzzer and there is one awesome script build for it, [ffuf_basicauth.sh](https://github.com/ffuf/ffuf-scripts/blob/master/ffuf_basicauth.sh).

This script will generate a `username:password` string based on your user name and password lists and then encode it using Base64. So finally you have a finished payload that you can use in a Burp in sniper attack or use it directly with fuff.

```shell
./ffuf_basicauth.sh usernames.txt passwords.txt |ffuf -w -:AUTH -u https://example.com/endpoint -H "Authorization: Basic AUTH" -fc 403
```

Sweet right? In general people who use basic auth for websites are trying to make it harder to access to some part of websites, but in general they use some simple combination of username and password. You can use already build lists like [CommonAdminBase64.txt](https://github.com/danielmiessler/SecLists/blob/master/Usernames/CommonAdminBase64.txt) or just [names](https://github.com/danielmiessler/SecLists/blob/master/Usernames/Names/names.txt) in comparison with [2023-200_most_used_passwords.txt](https://github.com/danielmiessler/SecLists/blob/master/Passwords/2023-200_most_used_passwords.txt) and everyone’s favorite RockYou from [SecList](https://github.com/danielmiessler/SecLists).

Today’s guide was simple and short, but sometimes I find simple tasks to do, and I think it is worth documenting them for others, so… thats all folks!

In the end, all the simple tasks together will allow you to do the magic and hack whatever you want.
