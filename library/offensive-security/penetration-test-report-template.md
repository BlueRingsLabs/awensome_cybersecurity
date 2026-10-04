---
id: ckb-064a2a5a33c5
title: Penetration test report template
category: offensive-security
format: article
language: en
tags: [bug-bounty, compliance, git, reporting, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.68
---

# Penetration test report template

No matter if you are experienced penetration tester, or beginner red teamer, if you have technical skills better than anyone on earth, or you’re just a script kiddie. All what maters is how you will present your findings. Especially if you are not only a bug hunter, but when you work in a corporation, and the results of your test needs to be addressed to the management.

![reports](reports.jpg)

Report of findings is probably most boring part of penetration test itself, but it does not need to be like that. Creating a documentation of your work and documenting findings is not only for the client, but can help you organize another test in the future. It is also good as a cheat sheet for similar findings, to get back and see how something was analyzed, to reinvent it again. Additionally if you will automate that process and use some templates, at the end building a report will be quick and easy. But you need start thinking about it from the very beginning of your journey as penetration tester, or bug bounty hunter.

Don’t forget who is the audience of report you will create. In corporation it will be some project manager (probably not too much technical person) who requested penetration test based of company needs + owners of the app/service (sometimes technical guys sometimes not) + developers who need to fix issues you will find (technical people, but sometimes offended that you point out errors in their wonderful work, not always, but happens) + the management (the worst).

So report should have sections for all of them. TBH requestor/project owner is always happy if just get pdf on time, easy one (pentest done, project complete with success). Service owners sometimes does not even know what are doing in the project, but were delegated, because some of fancy asset is assigned to them in the company. Developers are happy of technical part and in most cases understand it, but want to discuss, just to discuss and provide some excuses like: “we know about this but we couldn’t fix it as project was in freeze, here we have lack of people, and here it is not so easy because framework needs to be updated”. And sometimes just to point you that you made a mistake and PHP is not in version 4.4 but 5.6. (lol like it would change something). Finally the report will land on the management desk, and for them you need to prepare executive summary, short as hell as they do not have a time for that, and not too technical as they do not have a knowledge about shit they just reading.

It looks really bad what I write and mostly comes from the experience in internal tests for own company. External test, bought by some external company are better for auditor, because you don’t see all that shit behind on the customer side, but it is probably same mess what you see in our own environment, but they mask it to look professional. Bigger corporation bigger mess.

I always focus on the bad side. Hahah, but there is a lot of companies who knows, why they are doing pentest and how to cooperate, and have very well organized environment.

On the other side if you are a bounty hunter you may ask, why the heck I need to create a report. I found something, submit it and give me the fucking money. Yeah so, it does not work like this. Two examples.

First one. You can have shitest, lowest, dummiest finding on the world, but if you sell it very well in a beautiful report wrapped in a red bow, maybe you will get paid, hired or don’t get minus points in reputation on [HackerOne](https://docs.hackerone.com/hackers/reputation.html).

Second example. You can have the greatest finding on the world, worth creating CVE for that, worth millions of billions dollars, but your report is so shitty, and nobody understand it, and it is rejected. Your genius overshadowed others, but you couldn’t describe it, or you described it so technically that a non-technical person thought it was some bullshit to extract cash, and rejected it without passing to the technical team. In one company for a while I was in a team who was responsible (part of duties) for accepting or rejecting submissions from [Zerocopter](https://www.zerocopter.com/). I tried my best to verify it, and if I was not sure, verified it with some collogues with bigger experience, but some of the team members (lazy one) reject shitty reports with no details, just because they didn’t want to waste a time to go deeper. Almost everyone also reject bad described findings with a lot of begging like, “I know it is out of scope, but please pay me 5 USD I need it for living”. Lol. Who knows if the report would be good maybe it would be worth to pay someone that 5 USD just for the good professional attitude and time spent on preparing good quality report.

Oki doki. So for the management you need to show real business risk and for developers technical details, proof of concept and remediations steps. Additionally add some fancy, informative charts. But also keep report as simple as possible.

So to make it as simple as possible focus on: general information and statistics, description of the detected vulnerabilities, technical details of the vulnerability, recommendations for repair. Here is an example from my template.

![Penetration TestReport TOC](tableofcontent.png)

And to make it even more simple, I will share with you template I prepared and refined over the years.

<pentest_report_template.docx>

Download it, review, modify and use if needed. I learned a lot while building this template, I’ve been modifying it for many years now, and it will probably be even better in a few years.

My first reports were poor, non-technical people didn’t understand them. I tried to include too much of my thoughts. Sometimes I gave too much embellishment, focused on appearance and not on content. And it is, after all, documentation of the work done, risk assessments, evidence of errors and instructions on how to fix them. Nothing more. This is not an essay for a literary class. And no one cares how crappy you think the app is.

I have been in companies where, reports were an important document, influencing business decisions and the development of the company, where the smallest mistakes and risks were taken seriously. Where post-repair application retests actually took place and were a rewarding success for all employees involved in the repair program.

But I’ve also been in companies where just doing the test was a big success for a project that was shut down just after report delivery.

You only have one life, and a report is a report. Don’t waste more time and energy on it than you really should. Especially since a report can turn out to be a lifesaver for a company once, or a launching pad for someone to get a bonus or as a toilet paper source :)

This is why always add to the report something like this:

> The carried-out internal audit does not guarantee or constitute a security certificate of system safety which is the results of the scope and mode of conducted works.

So that later some manager doesn’t tell you, but after all, the pentest was done and thanks to that the company is safe.

Since we’re already on the topic of awareness and understanding why you need to do penetration testing, it is worth mentioning a document called rules of engagement.

I will quote my template to explain what RoE is:

> Rules of engagement (RoE) are meant to list the details of the penetration test. That’s the details behind what exactly will be tested when it will be tested, how it will be tested, and who the primary contacts will be throughout the engagement. This way, internal audit team conducting the penetration test and the organization being tested will know precisely what to expect from the test.
>
> This document should be pre-filled by the person ordering the test, in cooperation with the owner and the team responsible for the condition and development of the service or application being tested. The document will then be discussed at a meeting with the audit team.

If someone knows what they want to test and why, they will fill out this document in one meeting and discuss it with you at the kickoff meeting.

If someone request a pentest because someone told him, or because there is money for it, or that it will look cool in a meeting with the board of directors, then such a document is a pain in the ass, because you will mostly have to explain everything, and fill it by yourself with confirmation of requestor.

The pluses are that this document makes it clear what you will and will not do. And no one will be able to accuse you of doing a bad test or not paying for the part you mutually agreed on. I created such a template also and will share with you, it is not perfect, and still needs a lot of work, but always on the content side I try to make sure that everything is already described, so that there are as few questions and opportunities to answer in such a way that I have to inquire.

<pentest_roe_template.docx>

I hope you find these two documents useful and that you use them in your work.

I was inspired by the best companies, reviewed many templates, read public reports and tips on how to write such reports.

In addition, everywhere you see tags like ,  etc. in my templates you can use it for automation. For example penetration test frameworks like [Dradis](https://dradisframework.com/reporting.html), [Faraday IDE](https://faradaysec.com/penetration-testing-reporting/), [Pentest Collaboration Framework](https://gitlab.com/invuls/pentest-projects/pcf), [ReconMap](https://docs.reconmap.com/user-manual/reports/pentest-report-configuration.html), [Reporter](https://securityreporter.app/), [PeTeReport](https://github.com/1modm/petereport), [WriteHack](https://github.com/blacklanternsecurity/writehat) or [PlexTrac](https://plextrac.com/platform/reports/) and many many more on the market allows you to import project details and findings from your workspace and favorite tools with parsing engine, and put it to the report as output. So you just build a template with placeholders for data and fill it automatically after the project is complete. Then manual correction and report is done!

If what I have provided you does not meet your requirements try as I did, look at the [public reports of large companies](https://pentestreports.com/reports/) and take the best and what you need most for your template.

As an easy and quick solution you can also use online report generator: <https://create.pentestreports.com/home>

That’s all folks for today.

PS.: I know that reading long texts is not popular nowadays, but I decided that this is how this blog will look like. Longer articles, without catchy headlines. Even if it has to come at the expense of the number of visitors. I prefer valuable text (shitty ones happen to me too) to a quick post about nothing, or text at all rather than a step-by-step click-by-click YouTube video following a presenter, where mostly in the end it doesn’t work anyway. It is better to understand something than to repeat blindly. But I’m almost boomer, so there are no excuses.
