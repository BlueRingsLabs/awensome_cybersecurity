[[ PAGE 1 ]]

# ScopeWise - Yet Another Recon Script

Every bounty hunter, security analyst, or hacker has their favorite set of tools and scripts for automation. There are tons of people who share their solutions by providing cool tools, but there are also tons of bounty hunters who have their own arsenal and automation for hunting that they don’t share so as not to compete with each other. Sometimes, when I’m manually tinkering with something, I see an opportunity for automation, and then I think to myself, some awesome hacker probably scripted it a long time ago and is plowing through the whole world, and within 5 minutes of a vulnerability appearing, he’s already there exploiting or reporting it. This is more often seen in bounty hunting, e.g., in subdomain takeover. This low-hanging fruit is probably no longer easy to find manually. I know this because I myself have scripts that are just waiting for a dead, vulnerable subdomain pointing to some resource in the cloud to appear. If I can figure it out, experts definitely have an even better grasp of it.

![scopewise](scopewise.webp)

[The last article](../../08/reconftw/index.html) was about an excellent tool that automates recon. Today, I will show you my script, a poor version of ReconFTW. It is simply for faster and mass scanning of pages in search of a starting point for further investigation. Perhaps, based on this simple script, you will also build a pipeline of tools that collect and transfer data and generate results for later analysis.

[ScopeWise](https://github.com/h0ek/ScopeWise) is a lightweight script for automating network reconnaissance. It orchestrates a set of popular external tools into a systematic, phased workflow, running them sequentially for each host and saving the results in a clear directory structure. The tool is not a framework or a complete platform, but a simple orchestrator for quickly scanning the surface and collecting basic data. I am using it for long time.

Main features:

- launches reconnaissance phases on domains/hosts,
- input normalization and live URL validation,
- endpoint crawling and validation via httpx/katana,
- vulnerability scanning (e.g., nuclei, nmap, nikto),
- directory and file fuzzing (ffuf, feroxbuster),
- subdomain enumeration and subdomain takeover check.

Technical characteristics:

- shell/Bash orchestrator using tools available in PATH,
- per-host results in a directory structure with logs and raw outputs,
- acts as a simple integration layer, does not install dependencies automatically - tools must be installed separately.

Goal: quick, repeatable recon as a starting point for manual analysis and further targeted testing.

An example action plan is as follows: you collect interesting links, put them in a file, run the script, leave your computer for a while depending on the number of URLs you added to the list, come back after a few hours, and spend the next hour analyzing the results, noting down the most interesting details. Then, depending on your findings, you run other tools. For example, if it turns out that the site is WordPress, you run wpscan, etc.

Analysing files from different tools is always difficult because there is no single solution that can analyse the results of different tools and tell you what is OK and what isn’t, and what to do next. Of course, you can always upload the folder containing the results to AI and request a report and analysis. As with task automation, it is possible to overlook something interesting or make a mistake, and AI can also make mistakes when analysing results. That’s why it’s worth reviewing the results manually. If you don’t find anything interesting, upload them to AI to double-check in case you missed something. The same goes for automation itself. If an error occurs, the results are incomplete or missing altogether, it’s worth running the tool yourself to verify the scan and results again. There is no such thing as a perfect tool, and analysing results always takes time. However, analysing the operation of tools and their results can be educational. You can learn a lot and gain an understanding of how things work and where the results come from.

I have an idea to add a parser in the future, that will compile the results into a single report for review. This is not an easy task, which is why [ReconFTW does not do it](https://github.com/six2dez/reconftw/issues/928). Even a small change to the tools or the appearance of something new can cause the report to fail, and each tool produces output in a different format and style. I’ll try generate single page report in my spare time, so hopefully something will come of it. For now, you can use tools like Faradya, or analyse the results manually.

Happy hunting!
