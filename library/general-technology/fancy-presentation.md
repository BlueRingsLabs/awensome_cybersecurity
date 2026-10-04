---
id: ckb-bda84b88cab0
title: Fancy presentation
category: general-technology
format: article
language: en
tags: [git, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.99
---

# Fancy presentation

Normal people prepare presentations in PowerPoint (or Libre’s Impress or Google’s Slides), but it’s boring. I mean, presentations are generally boring and should only be a background for a speaker, and making them in a software like a PowerPoint makes them even worse (too many options to distract the creator and not focus on the content). Great presenters are remembered for their speeches, not their slides. Slides should be simple, clean and sometimes funny. They should just give an outline of what will be discussed, but not give too much away. That’s just my personal opinion, of course. When I see slides full of tables, content, text, charts, I feel sick. If I wanted to see that much data, I would open a documentation, a book or Excel. When I see a slide like that, I know it will be boring. Especially when the presenter just starts reading the content of the slide. It is even worse as I will not learn anything and this could be a podcast or audiobook :) I can read, I do not need people to read slides for me, if they read slides they could just send them to me and say read it. People who work in a big corporation know that most of the meetings with the slides could be just an email, but managers love to see overloaded slides, bars, graphs, charts, diagrams, preferably so much on a slide that it is virtually unreadable.

![worst slide](worst-slide.png)

Working for large companies, I have had to create presentations using corporate templates that are already so overloaded that there is little room for content. Fortunately, I do presentations for people in-house, so I don’t give a damn about those corporate templates.

As I travel around different conferences, I learn from the presenters, I watch them speak, I ask them what they create in and how they create. Last year I was at [The Hack Summit](https://thehacksummit.com/) conference and one session was called [Watch me run malwate from NPM](https://naugtur.pl/pres3/lava/malware.html#/) by naugtur. Click on the link to see what the presentation looks like. It is very simple, clean and very well done. It is a web browser version with cool navigation. The session itself was interesting, the speaker has great knowledge and the way he spoke was encouraging to listen to, slightly chaotic but engaging. I thought ok, I want to have slides like that.

If you check the source of the presentation, you can see:

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reset.css">
```

so yeah it is [reveal.js](https://revealjs.com/). I thought it was nice that it was a ready-made solution and not custom code from the presenter. So I started looking for other solutions like this. I found another cool option like [impress.js](https://impress.js.org/#/bored). I was thinking ok I will go back to reveal.js and start configuring but at the same time I found [Marp](https://marp.app/). Holy moly, that is what I have been looking for all my life. Just kidding. Marp allows me to create presentation content in Markdown (which I love and use whenever possible) and additionally format it using HTML and make it beautiful thanks to CSS. I had to spend some time learning Marp, reading the documentation, creating my own template and after a few hours everything was ready. Now, every time I need to make a presentation, I just open the template and focus on the slide content, then click generate and that’s it. Everything is formatted correctly and ready to go. It is possible to export code to html, pptx, pdf, png and jpg. Exporting to html allows you to run in presenter mode, so on one screen you can see a preview of the slides, presenter comments and a preview of the next slide, and on the second screen you can have the presentation slides in full screen.

To use Marp, you can install Marp CLI or, which is a better solution, install it as an extension for VS Code. I chose the second option and my workbench looks like this

![marp slide vs code](presentation_code.png)

On the left the source code of the template and on the right the preview. The only thing to do after installation is to change one option in the extension settings: `Markdown>Marp: Enable HTML` will enable all HTML elements in Markdown. And here is one slide from my presentation as an example:

![marp slide](slide.png)

I made my own theme based on the [Rosé Pine Moon by rainbowflesh](https://rainbowflesh.github.io/html/rose-pine-moon.html) (check this link as this is also live demo of Marp). Here is the source [github repository](https://github.com/rainbowflesh/Rose-Pine-For-Marp) with all the details and files. But you can also find a lot of different themes made by the community:

- [Dracula](https://github.com/dracula/marp)
- [Academic](https://github.com/kaisugi/marp-theme-academic)
- [Awesome](https://github.com/favourhong/Awesome-Marp)
- [MyMarp](https://github.com/rnd195/my-marp-themes)
- [MarpStyle](https://github.com/cunhapaulo/marpstyle)
- [NordicBeamer](https://github.com/n-ari/marp-theme-nordic-beamer)
- [BaseType](https://github.com/rstacruz/marp-basetype)

and many more. Beautifull, clean and simple. Much better than:

![horrible summary](horrible-summary-slide.png)

Someone might say, but why? Why make life harder and learn extra stuff to make a simple presentation? I don’t know, for fun, for education, to automate work, because you hate MS? I am a weirdo, personally I like to learn new things and automate my work and make simple and beautiful things with code.

I hope I infected you with the idea to make interesting presentations.

When creating presentations and speaking as a presenter, there are several important points to keep in mind for effective communication:

1. **Clarity of Message**: Ensure that your message is clear, concise, and easy to understand. Avoid technical jargon or overly complex language that may confuse your audience. Even if this is very complex topic or very technical one. Make it simple.
2. **Engagement**: Keep your audience engaged by using storytelling, humor, or interactive elements to maintain their interest throughout your presentation.
3. **Visual Appeal**: Use visually appealing slides with clear, easy-to-read fonts and high-quality graphics. Avoid cluttered slides with too much text or distracting animations. Keep it simple, but not too simple ;) Black text on a white background sounds simple, but it is also terrible. Focus on the content, add the most important things you will talk about and some things that support or complete your speech.
4. **Structure**: Organize your presentation into logical sections with a clear introduction, body, and conclusion. Use signposting to guide your audience through the flow of your presentation.
5. **Practice**: Practice your presentation multiple times to ensure smooth delivery and confidence on stage. Time yourself to ensure that you stay within the allocated time slot.
6. **Audience Interaction**: Encourage audience participation through questions, polls, or discussions to create a more interactive experience.
7. **Confidence and Body Language**: Maintain confident body language, such as making eye contact, using gestures, and speaking clearly and audibly. Confidence in your delivery will help engage your audience.
8. **Adaptability**: Be prepared to adapt your presentation based on audience feedback or unexpected circumstances. Stay flexible and open to adjusting your content as needed.
9. **Technical Preparation**: Test all technical aspects, such as audiovisual equipment and slides, before your presentation to avoid any last-minute issues.
10. **Feedback and Improvement**: Seek feedback from peers or mentors to continually improve your presentation skills. Reflect on your performance and identify areas for growth.
11. **Live examples**: If you have a live example that might not work for some reason (like presenting a complicated proof of concept), record your steps as a video and play it back to explain what you are doing. In a live session something can always go wrong, you get stressed and focus on fixing mistakes, wasting time instead of showing what you want. Even if you have done something 100 times before the presentation, everything that can go wrong will go wrong, this is Murphy’s Law.
12. **Video over the stream**: Do not embed video into the presentation, it is better to run it separately during the session rather than adding heavy content to the slides. If you have a live session that is online and not on stage, make sure that any multimedia files you are going to play will play smoothly. In most cases I’ve seen, turning on the video in a live stream/webinar interrupts it and people on the other side can’t see or hear anything.

When I practise my presentation, this is my first audience:

![hoek's audience](hoeksaudience.jpg)

they are patient and appear to be interested but do not give feedback.

Then I create an online meeting using [Jitsi](https://jitsi.org/) and invite friends and I do it again to get feedback. Finally, am ready to present to the target audience. Or at least I think so, because when it comes to presentations, I just get stressed, but I know I’ve rehearsed it so I do my thing. Maybe one day I will have a chance to say and present something interesting at one conference.
