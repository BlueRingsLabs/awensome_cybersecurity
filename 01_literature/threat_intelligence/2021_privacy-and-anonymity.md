[[ PAGE 1 ]]

# OS, apps and services for privacy and anonymity

There are few systems that ensure privacy. Even fewer of those who ensures anonymity. Even when we configure our system well, we must remember about the right application selection, so that our entire secure configuration is not compromised by one unfortunate program. We must also remember about our own behavior on the Internet and what we put in it. If someone gives you a service on the web for free, it is always at the expense of your data.

Ubiquitous telemetry, reports, artificial intelligence, content analysis, learning about user behavior, footprints, metadata and a lot of other tools and options. All this to facilitate and speed up the user’s work. Provide greater comfort of use. At least that’s what it looks like on paper and in the regulations.

It has been known for a long time that spying on the user of a system or service is aimed not only at improving the use, but also monetizing these analyzes. If we know what and where the user does, then we know what user likes, what doesn’t like, and what content to serve. We can then manipulate what the user sees. Provide them with materials that is more susceptible to and display ads, that is more likely to be clicked. Let’s just say it’s not the worst way to use such knowledge about user.

Computer hardware and operating systems have their backdoors that allow the “relevant” services to look where they want and collect information that is of interest to them. That’s why everyone is so much against encryption and open source. I will not cite any specific examples here. Over the years, many secret documents have emerged (e.g. thanks to [Edward Snowden](https://en.wikipedia.org/wiki/Edward_Snowden) or [Julian Assange](https://en.wikipedia.org/wiki/Julian_Assange)) that everyone can read the facts. These backdoors are sometimes by agreement and sometimes unconscious. However, you have to take into account that they are. Sometimes it is ordinary data about us, which law enforcement authorities use, in accordance with the law. Here’s a warrant, show us everything you have about this man.

The most important thing is to be an aware user. Choose the right software and services depending on your needs. And when you need something, look around what is safe and who you can trust. Don’t post everything about yourself online.

Public information like descriptions of your trips, photos from holidays, son’s illness, grandmother’s birthday, broken heart, or a drunken party, interest only you and those who want to use this data against you.

[OSINT](https://en.wikipedia.org/wiki/Open-source_intelligence) is the power. If I am a thief, I checked your Facebook profile to see that you were on bike trip with friends. I will check your profile on Strava to see model of your cool expensive bike. I’ll see when and where you go. In addition, you praised on Facebook that you are going on vacation to Croatia. By analyzing your online behavior, a liked alarm company profile, and a forum query about a broken home alarm. I know that you are going on vacation, you have an expensive bike at home, and your alarm is not working. I gather people and empty your apartment. Profiling people is fun, I recommend it.

When I started my professional career for large corporations, I had a background check done. What do I do online, what my superiors say about me, is what I wrote on my CV is true. Is my education real. At the end drug tests. If, during this process, a screening company found my profile on a neo-nazi forum where I preach racist arguments (no I am not a racist), would I get a job? Probably not. Freedom of speech. But does anyone want a racist in a multicultural corporation? [I don’t think so.](https://gifer.com/en/4kgw)

What if you care about privacy, but the data leaked? The same thing when you post everything in public, only can prove to be more embarrassing or dangerous. Think twice before hit enter. If some data hasn’t leaked yet, it doesn’t mean that it won’t leak or that someone already has access to it.

## Anonymity and privacy

![Anonymity and Privacy](anonimityandprivacy.png)

**Privacy** - is the equivalent of speaking to a close friend in a room with the door shut. I don’t necessarily have something to hide, I just want to keep the conversation private.

**Anonymity** - is the equivalent of riding on a crowded bus. You have no privacy, but no one on the bus knows who you are.

There is many interesting articles about [security, privacy and anonymity](https://www.google.com/search?q=security+privacy+and+anonymity).

This is generally a topic for long, interesting discussions that are always fruitful. I will let you explore this topic among you.

The hardest part of this discussion is that there is always someone who says “I have nothing to hide” or “only bad people who have something to hide, uses Tor and care about privacy and anonymity”.

Edward Snowden remarked:

> Arguing that you don’t care about the right to privacy because you have nothing to hide is no different than saying you don’t care about free speech because you have nothing to say.

For those who don’t get it, there’s always an argument with [“The dic-pic program”](https://www.youtube.com/watch?v=NRWxk7o-QlI). Check the [full interview](https://www.youtube.com/watch?v=XEVlyP4_11M), it is my favorite interview with Mr. Edward.

## Software and services

Nowadays it is very easy to find information about software and services, who creates it, is it trustworthy or works correctly, how many bugs were found, how quickly these bugs were fixed, whether the code is open source and transparent. If there was any data leak. You don’t have to be an expert, just analyze what the experts have already done.

Here are interesting places to check for software, services and operating systems

- [PrivacyTools](https://www.privacytools.io/)
- [RestorePrivacy](https://restoreprivacy.com/)
- [PrismBreak](https://prism-break.org/)
- [Privacy Heroes](https://privacyheroes.io/)
- [ThinkPrivacy](https://www.thinkprivacy.ch/)
- [Privacy Tools List](https://privacytoolslist.com/)

Here are some interesting online tools to test your web browser configuration

- [Cover Your Tracks](https://coveryourtracks.eff.org/)
- [Ip check](http://ip-check.info/)
- [BrowserAudit](https://browseraudit.com/)
- [PrivacyNet](https://privacy.net/analyzer/)

Check also [Top Security Browser Plugins](../../../../2020/01/08/top-security-browser-plugins/index.html) to easily pass the various test from tools above.

## Operating System

Although the above sites also list operating systems and put Linux on a pedestal, I’d like you to take a close look at the three below.

### Qubes OS

[Qubes OS](https://www.qubes-os.org/intro/) is an operating system designed with security in mind.

> Qubes OS is a free and open-source, security-oriented operating system for single-user desktop computing. Qubes OS leverages Xen-based virtualization to allow for the creation and management of isolated compartments called qubes.

![Qubes OS](qubesos.png)

In a nutshell, you can run applications in isolated compartments and group these compartments e.g. as work, private, or dangerous. Thanks to this, your identities and actions do not mix with each other and a mistake or unfortunate event does not compromise all data or system.

### Tails

[Tails](https://tails.boum.org/) system can be run from a flash drive wherever we have doubts about the machine we use. Thanks to this solution, you can start your own system and be sure that you work in a safe environment. We also benefit from being connected via the Tor network.

> Tails is a portable operating system that protects against surveillance and censorship.

![Tails](tails.png)

I have one USB drive with Tails installed when I am traveling. Encrypted system on USB drive with my personal data.

### Whonix

[Whonix](https://www.whonix.org/) is a slightly different approach. These are two virtual machines, one as a gateway and the other as a workstation, both configured to ensure complete anonymity via the Tor network. Gateway machine allows you to route all traffic on any other virtual machine (after proper network configuration) over the Tor.

> Whonix is software designed to preserve privacy and anonymity by helping users run applications anonymously. Whonix can be installed on Windows, macOS and Linux. Whonix also comes pre-installed in Qubes (Qubes-Whonix).

![Whonix](whonix.png)

To be honest I am using it in case when I don’t want to be detected. Like during bounty hunting. Also when I want to be totally anonymous, so for example when I am selling drugs over the internet… nah, just kidding, I am selling drugs like in old days on the street.
