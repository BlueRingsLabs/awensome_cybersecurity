---
id: ckb-41846fe8587a
title: JavaScript for Hackers 2
category: offensive-security
format: reference
language: en
tags: [exploit-development, javascript, owasp, red-team, web-security]
summary: This document provides a curated list of JavaScript tools, XSS payloads, and resources for penetration testing and offensive security operations.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.5-flash-lite
  confidence: 0.95
classified_by: google:gemini-3.5-flash-lite@2026-10-08T00:02:04Z
---

JavaScript for Hackers
2
Joas Antonio
Whoami
• Hacking is not crime advocate;
• OWASP Member;
• Red Team Expert;
JavaScript Tools
JaSt - JS AST-Based Analysis
• Syntactic detection of malicious (obfuscated) JavaScript files
• https://github.com/Aurore54F/JaSt
JS RANSOMWARE
https://gist.github.com/cb1kenobi/8b42d4cd69e65e1c8551
Drupal Create Admin User
https://github.com/hakluke/weaponised-XSS-
payloads/blob/master/drupal_create_admin_user.js
iFrame Template
https://github.com/hakluke/weaponised-XSS-
payloads/blob/master/iframe_template.js
Staged XSS
https://github.com/hakluke/weaponised-XSS-
payloads/blob/master/staged-xss.js
Wordpress RCE
https://github.com/hakluke/weaponised-XSS-
payloads/blob/master/wordpress_rce.js
Wordpress Create ADMIN
https://github.com/hakluke/weaponised-XSS-
payloads/blob/master/wordpress_create_admin_user.js
XSS Payloads
https://github.com/pgaijin66/XSS-
Payloads/blob/master/payload/payload.txt
JavaScript PenTesting - Task
https://github.com/cybersecurity-acmgmrit/Javascript-Pentesting
POWN
• Pown.js is a security testing and exploitation toolkit built on top of Node.js
and NPM. Unlike traditional security tools, notably Metasploits, Pown.js
considers frameworks to be an anti-pattern. Therefore, each feature in
Pown is in fact a standalone NPM module allowing greater degree of reuse
and flexibility. Creating new features is a matter of publishing new modules
to NPM. This module provides simple means to start the cli. As a result you
can easily build your own tools with pown or create new tools by
composition.
• https://github.com/pownjs/pown
BROSEC
• Brosec is a terminal based reference utility designed to help us
infosec bros and broettes with useful (yet sometimes complex)
payloads and commands that are often used during work as infosec
practitioners. An example of one of Brosec's most popular use cases is
the ability to generate on the fly reverse shells (python, perl,
powershell, etc) that get copied to the clipboard.
• https://github.com/gabemarshall/Brosec
NETCAT
• Netcat port in pure JS
• https://github.com/roccomuso/netcat
HoneyPot
• Low interaction honeypot application that displays real time attacks in
the web-interface. Made just for fun and it is not production ready.
• Written in Node.js the application listens on 128 most common TCP
ports and saves results to the MySQL Database for further analysis.
• https://github.com/Shmakov/Honeypot
Slowloris
https://gist.github.com/ktfth/f24ff4cf7f23d87f56d02485
c8f678f4
Node-mitm
https://github.com/moll/node-mitm
•
Mitm.js is a library for Node.js (and Io.js) to intercept and mock outgoing network TCP and HTTP connections.
Mitm.js intercepts and gives you a Net.Socket to communicate as if you were the remote server. For HTTP requests it
even gives you Http.IncomingMessage and Http.ServerResponse — just like you're used to when writing Node.js
servers. Except there's no actual server running, it's all just In-Process Interception™.
•
Intercepting connections and requests is extremely useful to test and ensure your code does what you expect. Assert
on request parameters and send back various responses to your code without ever having to hit the real network.
Fast as hell and a lot easier to develop with than external test servers.
•
Mitm.js works on all Node versions: ancient v0.10, v0.11 and v0.12 versions, previous and current LTS versions like v4
to v12 and the newest v13 and beyond. For all it has automated tests to ensure it will stay that way.
•
I've developed Mitm.js on a need-to basis for testing Monday Calendar's syncing, so if you find a use-case I haven't
come across, please fling me an email, a tweet or create an issue on GitHub.
Mouseclick-js
https://github.com/ankur8931/js-hacking/blob/master/mouse-
click.js
Multi-json
https://github.com/ankur8931/js-hacking/blob/master/multi-json.js
Multi-xml
https://github.com/ankur8931/js-hacking/blob/master/multi-xml.js
XMLHTTPREQ
https://github.com/ankur8931/js-
hacking/blob/master/xmlhttpreq.js
Data grabber for XSS
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md
Obtains the administrator cookie or sensitive access token, the
following payload will send it to a controlled page.
Data grabber for XSS
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md
Obtains the administrator cookie or sensitive access token, the
following payload will send it to a controlled page.
UI redressing
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md
Leverage the XSS to modify the HTML content of the page in
order to display a fake login form.
Javascript keylogger
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md
Another way to collect sensitive data is to set a javascript
keylogger.
Identify an XSS endpoint
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md
Another way to collect sensitive data is to set a javascript
keylogger.
XSS in HTML/Applications
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md
JavaScript PenTest Techniques
•
https://www.hackingloops.com/javascript-penetration-tester/
•
https://miloserdov.org/?p=4681
•
https://medium.com/swlh/secure-code-review-and-penetration-testing-of-node-js-and-javascript-apps-41485b1a9518
•
https://blog.appsecco.com/static-analysis-of-client-side-javascript-for-pen-testers-and-bug-bounty-hunters-f1cb1a5d5288
•
https://www.youtube.com/watch?v=HptfL5WRYF8&ab_channel=BitsPlease
•
https://pentestlab.blog/2018/01/08/command-and-control-javascript/
•
https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/02-
Testing_for_JavaScript_Execution
•
https://www.youtube.com/watch?v=N1R3qZhUvMg&ab_channel=DFIRScience
•
https://www.youtube.com/watch?v=ZOOkeUnQsjk&ab_channel=HoxFramework
•
https://medium.com/@secureica/hooking-victims-to-browser-exploitation-framework-beef-using-reflected-and-stored-xss-859266c5a00a
•
https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/02-
Testing_for_Stored_Cross_Site_Scripting
•
https://www.hacking-tutorial.com/hacking-tutorial/xss-attack-hacking-using-beef-xss-framework/#sthash.iGHfDiSw.dpbs
•
https://linuxhint.com/hacking_beef/
JavaScript PenTest Techniques
•
https://www.hackingloops.com/beef/
•
https://null-byte.wonderhowto.com/how-to/hack-web-browsers-with-beef-control-webcams-phish-for-credentials-more-0159961/
•
https://blog.nvisium.com/crossed-by-cross-site-scripting
•
https://www.secureideas.com/blog/2013/06/getting-started-with-beef-browser.html
•
https://www.softwaresecured.com/exploiting-less-js-to-achieve-rce/
•
https://snyk.io/vuln/SNYK-JS-TOTALJS-1077069
•
https://portswigger.net/daily-swig/remote-code-execution-vulnerability-exposed-in-popular-javascript-serialization-package
•
https://sca.analysiscenter.veracode.com/vulnerability-database/security/remote-code-execution-rce/javascript/sid-3575
•
https://rules.sonarsource.com/javascript/RSPEC-2755
•
https://sca.analysiscenter.veracode.com/vulnerability-database/security/xml-external-entity-xxe-injection/javascript/sid-5852
•
https://cloudmersive.medium.com/how-to-detect-xxe-attacks-from-text-input-in-javascript-d852d4646c10
•
https://codeql.github.com/codeql-query-help/javascript/js-xxe/
•
https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing
LABS
• https://tryhackme.com/
• https://www.hackthebox.eu/
• https://pentesterlab.com/
• https://www.defectdojo.org/
• https://sourceforge.net/projects/metasploitable/
• https://www.vulnhub.com/
• https://github.com/webpwnized/mutillidae
