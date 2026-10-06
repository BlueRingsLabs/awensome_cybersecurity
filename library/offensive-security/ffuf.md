---
id: ckb-800ec5942674
title: Ffuf
category: offensive-security
format: guide
language: en
tags: [burp-suite, dns, fuzzing, linux, tls, web-security]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.62
---

Page | 1

www.hackingarticles.in

Page | 2

www.hackingarticles.in

Table of Contents

Abstract ................................................. 4
Setup .................................................... 5
Input Options ............................................ 7
1. Simple Attack ........................................ 7
2. Multiple Wordlists ................................... 8
3. Ignore Wordlist Comment and Silent ................... 8
4. Extensions .......................................... 10
5. Request | Request-Proto | Mode ...................... 11
Match Options ........................................... 13
1. Match HTTP Code ..................................... 13
2. Match Lines ......................................... 14
3. Match Words ......................................... 15
4. Match Size .......................................... 16
5. Match Regular Expression ............................ 17
Filter Options .......................................... 18
1. Filter Code ......................................... 18
2. Filter Lines ........................................ 19
3. Filter Size ......................................... 20
4. Filter Words ........................................ 21
5. Filter Regular Expression ........................... 22
General Options ......................................... 23
1. Custom Auto Calibration ............................. 23
2. Color ............................................... 24
3. Maxtime For Task .................................... 25
4. Maxtime For Job ..................................... 26
5. Delay ............................................... 27
6. Request Rate ........................................ 28
7. Error Functions ..................................... 29
8. Verbose Mode ........................................ 30
9. Threads ............................................. 31
Output Options .......................................... 32
1. Output Format in HTML ............................... 32
2. Output Format in CSV ................................ 34
Page | 3

www.hackingarticles.in
3. All Output Format: .................................. 36
HTTP Options ............................................ 37
1. Timeout: ............................................ 37
2. Host Header ......................................... 38
3. Recursion ........................................... 39
4. Attack with Cookie .................................. 40
5. Replay-Proxy ........................................ 41
Conclusion .............................................. 43
References .............................................. 43
About Us ................................................ 44
Page | 4

www.hackingarticles.in

Abstract
We will learn how we can use ffuf, which states for “Fuzz Faster U Fool”, which
is an interesting open-source web fuzzing tool. Since its release, many people
have gravitated towards ffuf, particularly in the bug bounty scenario. So, let’s
dive into this learning process.
It is a professional command-line method for web fuzzing on a web server and
the credit goes to the author  (@joohoi). Many people have gravitated towards
ffuf since its release, especially in the bug bounty scene. While the bulk of this
shift is possibly attributable to the herd mentality, a significant portion of the
group has made the switch due to FFUF’s tempo, versatility, and capacity to
easily merge with external tooling.

Page | 5

www.hackingarticles.in
Setup
It is a command-line program that runs in the Linux Terminal or the Windows Command
Prompt. Upgrading from the source is not any more difficult than compiling from the source,
with the exception of the inclusion of the -u flag.

Due to the fact we are using Kali Linux, we’ll find ffuf in the apt repositories, allowing us to
install by running the simple command.

After installing this tool, to get its working parameters and options all we need is just to use [-
h] parameter for the help option.

go get -u github.com/ffuf/ffuf
apt install ffuf
ffuf -h
Page | 6

www.hackingarticles.in

Page | 7

www.hackingarticles.in
Input Options
These are parameters that help us to provide the required data for web fuzzing over a URL with
the help of a world list.
1. Simple Attack
For the default attack, we need to use parameters [-u] for the target URL and [-w] to load a
wordlist as shown in the image.

After running the command, let’s focus on the results.
•
Firstly, we noticed that it is by default running on HTTP method GET.
•
The next things are response code status [200, 204, 301, 302, 307, 401, 403, 405}; it
also shows the progression of our attack. At the end of the progress, we got our results.

ffuf -u http://testphp.vulnweb.com/FUZZ/ -w
Page | 8

www.hackingarticles.in
2. Multiple Wordlists
Sometimes one wordlist isn’t sufficient to show us our desired results. In that case, we case put
multiple wordlists at once to get better results. Only ffuf has the ability to run as many wordlists
as per our need for attack.
Here I provided two dictionaries dict.txt as W1 & W2 as Dns.txt and fuff will read both
dictionaries simultaneously.

3. Ignore Wordlist Comment and Silent
Generally, the default wordlist might have some comments that can affect our result accuracy.
In this case, we can use [-ic] parameter that can help us to get rid of that comment. Sometimes
we need to be more focused on attack rather than tools banners for this kind of accuracy we
need [-s] parameter which has the power to remove the banner of the tool.

ffuf -u https://ignitetechnologies.in/W2/W1/
-w dict.txt:W1 -w dns dict.txt:W2
Page | 9

www.hackingarticles.in

we can clearly see some comments are listed in the result when we have run above the
command and after using [-s] & [-ic] parameters in the next command the comments and
banner are removed.

ffuf -u http://testphp.vulnweb.com/FUZZ/ -w
dict.txt
ffuf -u http://testphp.vulnweb.com/FUZZ/
-w dict.txt -ic -s
Page | 10

www.hackingarticles.in
4. Extensions
We can search for a specific extension file on a web server with the help of [-e] parameter, all
we need to just to specify the extension file along with [-e] parameter. To get these results we
just need to follow the command.

ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt -e .php
Page | 11

www.hackingarticles.in
5. Request | Request-Proto | Mode
Burp Suite is an advanced framework for conducting web application security monitoring. Its
different instruments act in agreement to help the testing process as a whole. A cluster bomb is
a feature that uses several payload sets. For each given location, there is a different payload
package. the attack goes through each payload package one by one, checking all potential
payload variations.
There is a various parameter of this tool, which help to use this our scenario. Like [-
request] parameter which can use our request in the attack, [-request-proto] parameter through
which we can define our parameter, [-mode] parameter help us to define the mode of attack.
First of all, we use random credentials on our targeted URL page and set proxy up to capture
its request in intercept mode on Burpsuite.

Now in the intercept tab of the Burpsuite, change our provided credential
with HFUZZ and WFUZZ. Put HFUZZ in front of uname and WFUZZ in front of the pass.
Then copy-paste this request in a text and name as per your desire. In our case, we named that
brute.txt.
Page | 12

www.hackingarticles.in

Now proceed towards the main attack, where [-request] parameter hold our request text file. [-
request-proto] help us derive the http prototype [-mode] help us to derive us cluster bomb
attack. The wordlists we use in these (users.txt and pass.txt) consist of SQL injections. Follow
this command start attacking using these parameters.

as we can see in our attack results, we have successfully found out SQL injections working on
that particular target.

ffuf -request brute.txt -request-proto http
-mode clusterbomb -w users.txt:HFUZZ -w
pass.txt:WFUZZ -mc 200
Page | 13

www.hackingarticles.in
Match Options
If we want ffuf to show only that data which is important in our web fuzzing data. Then it will
help us to showcase only matched according to the parameter. Example: HTTP code, Lines,
Words, Size and Regular Expressions.
1. Match HTTP Code
To get an understanding of this parameter we need to consider a simple attack where we can
see which HTTP codes are appearing in our results.

we can clearly see that it showing some 302 HTTP code along with 200 HTTP code.

If only need successful results like 200 HTTP code we just need to use [-mc] parameter along
with our specific HTTP code. To use this parameter just follow the command.

ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt
ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt -mc 200
Page | 14

www.hackingarticles.in

2. Match Lines
Like the match code which we discussed earlier, it gives us the result for a specific-lines in a
file with the help of [-ml] parameter. We can use this [-ml] parameter by specifying the lines
we need in a file.
ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt -ml 15
Page | 15

www.hackingarticles.in

3. Match Words
Similarly, as the above functionalities match function it can provide us with a result with a
specific word count. To get this result we need to use [-mw] parameter along specific words
count we want in our results.

ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt -mw 53
Page | 16

www.hackingarticles.in

4. Match Size
Similarly, as the above functionalities match function it can provide us with a result with the
size of the file. We can use [-ms] parameter along with the specific size count we want in our
result.

ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt -ms 2929
Page | 17

www.hackingarticles.in

5. Match Regular Expression
It is the last of all match functions available in this tool. We are going to fuzz for LFI by
matching the string with followed pattern “root:x” for the given dictionary.
We are using a URL that can achieve this functionality and by using [-mr] parameter we define
the matching string “root:x”.
This our special wordlist looks like.

Page | 18

www.hackingarticles.in
By using this wordlist, follow the below command to use [-mr] parameter in an attack
scenario.

Here we got HTTP to respond 200 for /etc/passwd for the given wordlist.

Filter Options
The Filter options are absolutely opposite to Match options. We can use these options to
remove the unwanted from our web fuzzing. Example: HTTP Code, Lines, Words, Size,
Regular Expressions.
1. Filter Code
The [-fc] parameter need the specific HTTP status code we want to remove from the result.

ffuf -u http://testphp.vulnweb.com/showimage.php?file=FUZZ
-w dict2.txt -mr "root:x"
ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt -fc 302
Page | 19

www.hackingarticles.in

2. Filter Lines
The [-fl] parameter has the ability to remove a specific length from our result or we can filter
it out from our attack.

ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt -fl 26
Page | 20

www.hackingarticles.in

3. Filter Size
The [-fs] parameter has the ability to filter out the specified size is described by us during the
command of the attack.

ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt -fs 2929
Page | 21

www.hackingarticles.in

4. Filter Words
The [-fw] parameter has the ability to filter out the words count from results that we want to
remove.

ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt -fw 83
Page | 22

www.hackingarticles.in

5. Filter Regular Expression
The parameter [-fr] we can remove a specific regular expression, here we try to exclude the log
file from the output result.

ffuf -u http://192.168.1.12/dvwa/FUZZ/
-w dict.txt -fr log
Page | 23

www.hackingarticles.in

General Options
These are the general parameters of this tool, which revolves around its general working on
web fuzzing.
1. Custom Auto Calibration
We know that the power of a computer or machine to automatically calibrate itself is known
as auto-calibration. Calibration is the process of providing a measuring instrument with the
information it requires to understand the context in which it will be used. When gathering data,
calibrating a computer ensures its accuracy.
We can customize this feature according to our need with the help of [-acc] parameter. Which
can’t be used without [-ac] parameter for its customization.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -acc -ac -fl 26 -ac -fs 2929 -ac
-fw 54
Page | 24

www.hackingarticles.in

2. Color
Sometimes separation of colour creates extra attention to all details having in results. This [-
c] parameter helps to create colour separation.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -c
Page | 25

www.hackingarticles.in

3. Maxtime For Task
If you want to fuzz for a limited amount of time then you can choose [-maxtime] parameter.
Follow the command to provide a timeslot.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -maxtime 5
Page | 26

www.hackingarticles.in

4. Maxtime For Job
With the help of [-maxtime-job] parameter, we can put a time limit for a particular job. By
using this command, we are trying to limit the time per job or request execution.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -maxtime-job 2
Page | 27

www.hackingarticles.in

5. Delay
If we create a particular delay in each request offered by the attack. Through this feature, a
request has a better opportunity to get better results. The [-p] parameter help us to achieve delay
in those requests.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -p 1
Page | 28

www.hackingarticles.in

6. Request Rate
We can create a separate request rate for each of our attack with the help of the [-
rate] parameter. Through this parameter, we create our request per second as per our attack
desired.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -rate 500
Page | 29

www.hackingarticles.in

7. Error Functions
There are three parameters that support the Error function. The first parameter is [-se], which
is a spurious error. It states that the following request is genuine or not. The second parameter
is [-sf], it will stop our attack when more than 95% of requests occurred as an error. The third
and final parameter is [-sa], which is a combination of both the error parameter.
In our scenario, we are using [-se] parameter where it will stop our attack when our request is
not real.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -rate 500
Page | 30

www.hackingarticles.in

8. Verbose Mode
As we all know, the verbose mode is a feature used in many computers operating systems and
programming languages that provide extra information on what the computer is doing and what
drivers and applications it is loading at initialization. In programming, it produces accurate
output for debugging purposes, making it easy to debug a program. There is a parameter
called [-v] parameter.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -v
Page | 31

www.hackingarticles.in

9. Threads
The [-t] parameter is used to speed up or slow down a process. By default, it is set on 40. if we
want to pace up the process, we need to increase its number, vice versa to slow down process.

Page | 32

www.hackingarticles.in

Output Options
We save the performance of our attacks for the purposes of record-keeping, improved
readability, and potential references. We use [-o] parameter to save our output, but we need to
specify its format with [-of] parameter together.
1. Output Format in HTML
We use [-of] parameter and this defining with an HTML format. By using the command, we
can create our report in html.
ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -v
Page | 33

www.hackingarticles.in

Now after completion of this attack, we need to check our output file is up to that mark or not.
As we can see that our file is successfully created.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -o file.html -of html
Page | 34

www.hackingarticles.in

2. Output Format in CSV
Similarly, we just need to csv format along with [-of] parameter. Where csv is a comma-
separated values, which file allows you to store data in a tabular format.

 ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -o file.csv -of csv
Page | 35

www.hackingarticles.in

Now after completion of this attack, we need to check our output file is up to that mark or not.
As we can see that our file is successfully created.
Page | 36

www.hackingarticles.in

3. All Output Format:
Similarly, if we want all output format at once just use [-of all] parameter. Like json, ejson,
html, md, csv, ecsv. Follow this command to generate all reports at once.

Now after completion of this attack, we need to check our output files is up to that mark or not.
As we can see that our all files are successfully created.
ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -o output/file -of all
Page | 37

www.hackingarticles.in

HTTP Options
The options move around HTTP options, sometimes it required the details to run web fuzzing
Like HTTP request, Cookie, HTTP header, etc.
1. Timeout:
Timeout act as a deadline for the event. The [-timeout] parameter help of established this
feature with ease, follow this command to run this parameter.
Page | 38

www.hackingarticles.in

2. Host Header
If we want to perform fuzzing on subdomain, we can use [-H] parameter along with a domain
name wordlist as given below in the command.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -timeout 5
ffuf -u https://google.com -w dns_dict.txt
-mc 200 -H "HOST: FUZZ.google.com"
Page | 39

www.hackingarticles.in

3. Recursion
Recursion is the mechanism of repeating objects in a self-similar manner, as we all know. If a
program requires you to access a function within another function, this is referred to as a
recursive call of the function. By using [-recursion] parameter, we can achieve this
functionality in our attacks.
ffuf -u https://google.com -w dns_dict.txt
-recursion
Page | 40

www.hackingarticles.in

4. Attack with Cookie
Sometimes web fuzzing does not show the result on authenticated site without authentication.
There is a [-b] parameter through which we can achieve your goal by providing a session
cookie.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -b
Page | 41

www.hackingarticles.in

5. Replay-Proxy
As you might be aware, there are speed restrictions when using the Intruder function in the free
version of the Burp suite (Community Edition). The Intruder attack has been severely slowed,
with each order slowing the attack even further.
In our case we are using Burp suite proxy to get results for evaluation in it. First, we have to
establish a localhost proxy on port 8080.

Now use [-replay-proxy] parameter, which helps us to derive our local host proxy which we
established in the previous step on port 8080 along with our attack.

ffuf -u http://192.168.1.12/dvwa/FUZZ/ -w
dict.txt -replay-proxy http://127.0.0.1:8080
-v -mc 200
Page | 42

www.hackingarticles.in

This attack will show our results on two platforms. The first platform on the kali terminal and
the second on the Burp suite HTTP history tab. Through these various techniques, we can better
understand our target and our attack results.

Page | 43

www.hackingarticles.in
Conclusion
The ffuf is often compared to tools like dirb or dirbuster, which, although accurate to certain
extents, isn’t a reasonable analogy. Although FFUF can be used to brute force files, its true
strength lies in its simplicity, and a better comparative tool for FFUF would be anything like
Burp Suite Intruder or Turbo Intruder.
References
•
https://www.hackingarticles.in/comprehensive-guide-on-ffuf/

JOIN OUR
TRAINING PROGRAMS
www.ignitetechnologies.in
BEGINNER
Network Pentest
Bug Bounty
Wireless Pentest
Network Security
Essentials
Ethical Hacking
ADVANCED
EXPERT
Burp Suite Pro
CTF
Windows
Linux
Pro
Infrastructure VAPT
APT’s - MITRE Attack Tactics
MSSQL Security Assessment
Active Directory Attack
Red Team Operation
Privilege Escalation
Web
Services-API
Android Pentest
Computer
Forensics
Advanced
Metasploit
CLICK HERE
