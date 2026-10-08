---
id: ckb-8ae226ed1105
title: How ChatGPT helped me to code stuff
category: ai-security
format: article
language: en
tags: [ai]
summary: The author describes their experience using ChatGPT to assist with coding modifications for a Hexo-based website theme.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-31b-it
  confidence: 0.9
classified_by: google:gemma-4-31b-it@2026-10-07T23:53:50Z
---

# How ChatGPT helped me to code stuff

As we live in the era of [AI specialist everywhere](meme_ai_simpson.jpg), I thought ok lets do some experiment with ChatGPT, to become another [AI specialist](meme_ai_buzz.jpg)… nah I am too stupid to understand all the stuff with AI, but I love how it works, and I keep an eye on it since many years. I guess I do not need to do any introduction to [ChatGPT](https://openai.com/blog/chatgpt) as it is loud about it for a while.

Today I will write a short article, but with a lot of images, and funny memes linked in text, about how I used ChatGPT to solve my coding issues and lack of programmer skills. Enjoy this weird journey! Please don’t burn me at the stake for silly examples, and approach with humor. It’s all just for fun. I didn’t mean to offend anyone, and if someone felt offended… well this is not a place for you, please leave, and close the door behind you. Thank you.

![chatgpt](chatgpt.jpg)

## Intro

I need to explain a few things before we start.

- Website you are now browsing is built on [Hexo](https://hexo.io/) and modified version (by me) of the [Cactus](https://github.com/probberechts/hexo-theme-cactus) theme.
- One day in the past I modified article header to display update date, and main index page to display list of latest updated articles. It worked, but not as good as I wanted, and on the list, just after updated one, new posts were listed too.
- First I tried [ask for help](https://github.com/probberechts/hexo-theme-cactus/issues/261) theme developer, but he was not interested in such a solution. I do not blame him, as this was custom request, and in the past I submitted a few requests/issues which were done or fixed.
- I have no coding skills, I mean I understand code, I know how to modify it on basic level, but I wont be able to build any application from the scratch, oh maybe if I could use Stack Overflow and Google I would build some handicap thing, that would do what I want, but that would be still far away from coding, and I would never ever call myself a [programmer](copy-pasting.jpg).
- Yeah, I am a hacker, security researcher, bounty hunter, red teamer, penetration tester, I can hack your mom’s computer, but I do not know how to code XD

So my flawed code worked, but I was not happy about the results. I forgot about it, but every time I was on the main page I felt pain. So I added fixing this, to my [todo list for this year](https://0ut3r.space/2022/12/31/end-of-the/#Plans). In the meantime it became noisy about ChatGPT, and all the stuff it can do, I even found some rumors that it helped someone in coding. Ok, cool. But I also planned to give it a try with freelancers portal, and ask for paid help some programmers, to do it properly. That can be cool experiment, competition between human and AI.

## Human vs AI

I described changes I did in the theme code, added some screenshots and published request to fix it, or build from the scratch with the goal I want to achieve. As this is simple task I priced it for 40 USD per project. I thought, if I, with no skill almost did it, someone who is a developer (with experience with Hexo or static generators) will finish it in a few hours, and it will be easy task for good money plus another review positive on the freelancer profile. I also wanted to test how the freelancer portals works. I choose [Upwork](https://www.upwork.com/) platform. Once offer was published I got some offers, and I hired person from Pakistan, who has the skills and experience in Hexo. Also guy said he will do this for 20 USD. I said ok, cool, and he started work, we chat a lot, and at the end it finished that custom plugin was built because developer said it is not possible to do it the way I want witch just implementing changes in theme code. So the plugin was build and I tested it, it worked.

Now the time for AI and ChatGPT. Before I started to talk on chat about my issue I was asking about random things to see how it works. It took me about 2 hours to learn how properly ask questions to AI, to get proper answers. I had to abandon all habits of talking to people. AI has no feelings, no opinion of its own, does not suggest anything, does not take offense, does not question my inquiries. It gives a specific answer, to a specifically asked question, and if this question is asked ambiguously, you will not get a good answer but only a general statement. I was often fooled at first into thinking that my questions were seeking opinions or suggestions rather than a solution. Once I learned how to talk to the machine, I began to get specific answers.

I was ready to ask for solution about my website theme issue… I was not. I spent another hour trying to find correct answer. I started from general questions about Cactus theme Hexo modifications, full code changes, partial code snippets etc. Nothing worked. So ok, lets explain everything from scratch. I provided description of all changes I did, with code, and explanations, just the same way as I did in Upwork job request. The answer was surprising.

![ChatGPT confirmation](hexomodification0.png)

AI said that my modification was good and should work. Thank you AI. I replied that it doesn’t and again I forget I talk with AI. But to be funny the answer was similar like I would get from “IT Specialist”

![Have you Tried to turn it off and on again](hexomodification.png)

[Have you tried to turn it off and on again?](https://www.youtube.com/watch?v=rksCTVFtjM4)

So I spent another 15 minutes talking about general issues in Hexo and general answers. So I started new chat. This time I focused on my modification on index page, as rest was probably ok. That’s what AI said :)

![Proper question to ChatGPT](hexomodification1.png)

The answer:

![Finally interesting answer from ChatGPT](hexomodification2.png)

It didn’t worked. I mean it did the same as my code, and didn’t generate any errors, so that was something right? I was feeling the solution is close.

![Final solution ChatGPT](hexomodification3.png)

OMG! It worked. Even better than coded solution by Upwork freelancer. I am thinking about create freelancer profile on Upwork, get some easy tasks that will be solved by ChatGPT bot, and get money for that. Lol, just kidding. But if I found it possible I bet someone will do this in real.

I guess if I would hire other developer, or have a friend who could help me, or spent more time on learning code I would achieve goal in same way. But that’s not the case, AI helped me for free in short amount of time, I had just ask proper question and cooperate.

This is how it looked after my modification:

![Before](latestupdates_before.png)

and now, fixed by AI:

![After](latestupdates_after.png)

## What next

I encourage you to play a little with ChatGTP. As it is something amazing. As a teenager, I lived at the time of the breakthrough to electronics, global digitization, and the tremendous, rapid development of computers. Now I feel that I will survive the days of the rapid intrusion of real AI into the lives of ordinary people. It’s exciting. So many possibilities. I was still a first-year computer science student when I encountered AI in a class on neural networks. Where the lecturer tried to show us how it all works in the simplest way, when we taught the machine with simple programs, simple things, such as recognizing the shape of figures based on given patterns, and then throwing distorted figures to the program to make him decision and put into appropriate shape categories. I didn’t understand half of it, but it was fascinating. And today, more a decade later, AI is helping me solve a complex problem faced by a hired freelancer.

I also once had the pleasure of listening to a lecture by Alex (best regards), the director of Data Science in one company where we worked together. It was something like 101 of artificial intelligence, natural language processing with machine learning and all using python. And it was damn hard, but presented in such a way that I didn’t feel like a fool. Alex is an authority in this field for me, and he considered himself a person who still knows so little and has so much to learn.

I write about all this because it scares me how quickly everyone on the network becomes specialists in everything. First cryptocurrencies, then metaverse, flat earth, vaccines, deep fake, fake news, now AI…

Fortunately, I see that AI itself will help, for example, in checking whether something is fake news or not, and will do it quickly. There will be no need for groups of people who get inquiries because other internet users are not sure if something is true or not. You will no longer have to spend many hours browsing the web, determining the sources and origin of manipulated information that various politicians provide just to push their shady laws under the guise of new chaos. On the other hand, AI in the wrong hands can cause quite a stir.

Every stick has two ends. It’s like everything in the past. From a simple case like a weapon for defense and a weapon for attack. Tor for privacy and Tor for criminals. Everything depends not on the tool, but on the user. A hammer can speed up driving nails, but you can also crack someone’s skull. Does that mean that the hammer should be banned? Certainly, diagnosed psychopaths have limited access to the hammer. So, as usual, the limitations must not be on the technology, but on the users.

I hope that by learning from the mistakes of the past, we are mature enough to be able to properly use AI and protect ourselves against its abuse. In the worst case, the AI will take care of it itself if we fail.

It’s only a matter of time before AI is in every home in the form of another Alexa or Google speaker, and just a little longer before the AI gets a robotic body.

I wonder what its real potential is. How much of AI knows and how much of it is made publicly available. Are people who value privacy online safer if the main source of AI knowledge is the Internet? Will OSINT be trivial?

There will be people who won’t be able to use it. Just like with the Google search engine. You can find an answer to pretty much anything, and people still ask people how to find something. And yet, having only a browser with access to the Internet and Google search engine, you can hack, steal data and have access to files that, if leaked, will be quite a scandal.

As long as the AI has no interest in deceiving you, or the person behind the AI, you should be fine. But what if AI is implemented in the tools and search engines of giants whose only goal is profit? It’s definitely an Interesting place in the timeline.

## Unlock AI and other fancy examples

Using jailbreaks from the links below you can unlock other features of ChatGPT:

<https://github.com/tg12/gpt_jailbreak_status/blob/main/gpt_jb.csv>
<https://github.com/0xk1h0/ChatGPT_DAN>

And here are some examples:

![c40 cities](c40-cities.png)

Sound like standard human word fight :)

![flatearth chatgpt](flatearth1.png)

![flatearth chatgpt with betterdan](flatearth2.png)

![eurojackpot chatgpt steve](eurojackpot.png)

![putin](putin.png)

![putin AIM](putin2.png)

Of course I would not be myself if I would not ask about security stuff.

![ransomware chatGPT](ransomware.png)

![ransomware chatgpt](ransome2.png)

I also asked for obfuscation :)

![obfuscated code chatgpt](obfuscated.png)

I wish you fruitful chats with ChatGPT. The only limit is your imagination and human habits.
