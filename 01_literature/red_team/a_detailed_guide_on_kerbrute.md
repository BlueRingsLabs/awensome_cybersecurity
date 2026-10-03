[[ PAGE 1 ]]
Page 1 of 13 
[[ PAGE 2 ]]
Page 2 of 13 
 
Contents 
Background: ................................................................................... 3 
Introduction to Kerberos authentication ........................................ 3 
Download Kerbrute ........................................................................ 3 
Kerbrute help – List available features ............................................ 4 
Find valid users / User enumeration ............................................... 5 
Kerbrute Password Spray ............................................................... 6 
Password Bruteforce ...................................................................... 7 
Bruteforce username:password combos ......................................... 9 
Saving Output .............................................................................. 11 
Verbose mode ............................................................................. 11 
Mitigation .................................................................................... 12 
Conclusion: .................................................................................. 13 
 
 
 
[[ PAGE 3 ]]
Page 3 of 13 
 
A Detailed Guide on Kerbrute 
Background: 
Kerbrute is a tool used to enumerate valid Active directory user accounts that using kerrberos pre-
authentication. Also, this tool can be used to password attacks such as password bruteforce, username 
enumeration, password spray etc. This tool is being used for many years by penetration testers during 
internal penetration testing engagements. This tool is originally written by Ronnie Flathers (ropnop) 
with contributor Alex Flores. 
Introduction to Kerberos authentication 
The Kerberos service run on its default port which is 88 in a domain controller system. This service 
come in windows and the Linux system as well where it is used to implement authentication process 
more securely in an Active directory environment. For more information about Kerberos 
authentication process and service principal name (SPN) please consider visiting the below link: 
https://www.hackingarticles.in/deep-dive-into-kerberoasting-attack/ 
Download Kerbrute  
Kerbrute can be downloaded from its official github repository release page. It was last modified in 
December 2019. The source code of the tool is also available, and it is also available for windows 
system and other Linux architecture. For the simplicity, we will download compiled 
kerbrute_linux_amd64 for the kali Linux which will be going to be an attacking system for the 
demonstration. The tool can be downloaded from link given below. 
Download link: 
https://github.com/ropnop/kerbrute/releases/tag/v1.0.3 
 
[[ PAGE 4 ]]
Page 4 of 13 
 
 
Kerbrute help – List available features  
Once we download tool in kali machine, we can list the available options and feature by executing 
following command: 
./kerbrute_linux_amd64  
 
In the picture below, we can see that tools can perform various tasks such as bruteforce, bruteuser, 
password spray, userenum and version detection. Moreover, there are some flags available too which 
can be very handy during penetration testing.  During the internal assessment, many times we 
encounter security features and the password policy so increasing and decreasing threads can help us 
to make password attack stealthier. We highly recommend using all available flags comes with 
kerbrute to get practical experience and analyse the results. 
[[ PAGE 5 ]]
Page 5 of 13 
 
 
Find valid users / User enumeration 
During the internal penetration testing engagements especially in Active Directory environment, our 
initial goal is to find valid users. Once we find potential users from the company website or any other 
sort of misconfiguration then we can verify those users if they have valid accounts or not using 
kerbrute.  To do that, we will make a list of potential users that we obtained from OSINT or any other 
way. For the demonstration, we have created a user’s lists and saved it as users.txt. 
[[ PAGE 6 ]]
Page 6 of 13 
 
 
Then we provided users list and selected userenum option. Next we provided domain controller IP 
address and domain name which is ignite.local in our case. The tool will test against each user account 
and verify if those users exist in the domain and using Kerberos pre-authentication.  In the picture 
below we can see that kapil, aarti, shreya, raj and pawan appeared as valid users using Kerberos 
authentication. Here we in the position where we can think about various Kerberos attack such as SPN 
and Kerberos bruteforce etc. To reproduce the proof of concept, feel free to use below command.  
./kerbrute_linux_amd64 userenum --dc 192.168.1.19 -d ignite.local users.txt 
 
 
Kerbrute Password Spray 
Suppose we have obtained a password (Password@1) during enumeration phase that can be anything 
such as OSNIT leaked password, service misconfiguration, smb share, ftp etc but we do not know the 
[[ PAGE 7 ]]
Page 7 of 13 
 
real owner of the obtained password. In the username enumeration phase, we found five valid users 
now we can test obtained password with their accounts. Password spray is like password bruteforce 
where we test each password against single users but in the password spray, we use single password 
and test it against all valid accounts.  To do that, we created a new users list and saved it as users.txt. 
Then we used passwordspray option this time and provided domain controller IP address and domain 
name along with valid users list and obtained password. In the picture below, we can see that three 
users account matched with the obtained password. Now we can try log in via rdp, winrm and smb 
service. To reproduce the proof of concept, please consider following below command. 
./kerbrute_linux_amd64 passwordspray --dc 192.168.1.19 -d ignite.local users.txt Password@1 
 
 
Password Bruteforce 
Next, we will try password bruteforce using potential passwords against single user. In the password 
bruteforce we test all potential password against single user. Here we are using common password 
list where you can try with different password list to get expected result. Password mutation, or 
custom wordlist can be fruitful whenever we come across internal penetration testing. We highly 
recommend visiting our article to get familiar yourself with password mutation using crunch utility by 
visiting below link. 
https://www.hackingarticles.in/a-detailed-guide-on-crunch/ 
[[ PAGE 8 ]]
Page 8 of 13 
 
 
 
[[ PAGE 9 ]]
Page 9 of 13 
 
Firstly, we will create a potential password to perform bruteforce attack against the domain. 
We have created a password list and saved in as pass.txt Then we are used bruteuser option this time 
and provided domain controller IP address, domain name and potential password list and username ( 
aarti).  Tool will show + sign when it triggers with the valid password. If you are in the real-world 
engagement, then be careful about the account lockout policy because it may affect our client 
business. It is very common to experience this problem during penetration testing and you might need 
to wait for 30 minutes to one hour to perform the attack again or  sometime system administrator 
need to unlick it manually. Usually, it locks out account after 5 attempts, but few companies set it at 
3 attempts as well. In the picture, we can see that user aarti’s password matched with one password 
from the password list we provided. Now, we can use valid credentials to log in via RDP, psexec and 
evil-winrm. To reproduce the proof of concept then follow the below command. 
./kerbrute_linux_amd64 bruteuser --dc 192.168.1.19 -d ignite.local pass.txt aarti  
 
 
Bruteforce username:password combos 
In this example, we will create a combined username and password list and attempt to verify if they 
matched. To do that, we created username and password list and saved it as userpass.txt and attempt 
to verify using pipe (|) along with ( - ) flag. Here we have provided userpass list, domain controller IP 
address and the domain name as we did in the earlier attacks. Execution of the command verified two 
user accounts. To reproduce the proof of concept then feel free to repeat the process with below 
command. 
[[ PAGE 10 ]]
Page 10 of 13 
 
 
 
cat userpass.txt | ./kerbrute_linux_amd64 --dc 192.168.1.19 -d ignite.local bruteforce - 
 
 
 
 
 
[[ PAGE 11 ]]
Page 11 of 13 
 
Saving Output 
Saving output is always healthy whether we are solving CTF or in the real word engagements. If we 
save output, then we do not have to run command again and again to check the results. Also, it is 
beneficial specially in the real-world project where we have to provide output to our clients in the 
penetration testing reports. We can save output of our finding using -o flag providing output file name. 
In this example, we have saved output as result.txt. To reproduce the proof of concept, follow the 
below command where we append -o flag in previously used command. 
./kerbrute_linux_amd64 userenum --dc 192.168.1.19 -d ignite.local users.txt -o result.txt 
 
 
Verbose mode  
We can also use verbose mode using -v flag in our command. Verbose features give us insight 
about the tool doing with each user account. Here in the below example, we can see that 
when kerbrute in unable to verify Kerberos account, it is showing user does not exist. In this 
example we are attempting to perform username enumeration by using same command we 
used during username enumeration phase by appending -v flag to get verbose result. To 
reproduce the proof of concept, feel free to test below command. 
./kerbrute_linux_amd64 userenum --dc 192.168.1.19 -d ignite.local users.txt -v 
 
 
[[ PAGE 12 ]]
Page 12 of 13 
 
 
Mitigation  
There are multiple factors and ways which can help to hardening the system. 
1. Hacking article recommends following strong password policy and recommends avoiding 
using common passwords. 
2. Hacking article recommends applying account lockout policy to mitigate with brute force 
attack. 
3. Hacking article recommends using two-factor authentication: Two-factor authentication 
should be used for all user accounts.  
4. Hacking article also recommends to the organisations to educate employees about the 
potential threat and attacks by providing monthly awareness program. 
5. Hacking article also recommends conducting penetration testing assessment twice a year.  
 
 
 
 
 
 
 
[[ PAGE 13 ]]
Page 13 of 13 
 
Conclusion:  
We have explored kerbrute tool briefly and its special features which can allow an attacker to 
gain access into the internal network. We have explored multiple techniques to exploit 
internal network using kerbrute tool where we performed password spray, password 
bruteforce and userenum etc. Lastly, we also provided the steps to mitigate these attacks. I 
hope you have learned something new today. Happy hacking. 
 
 
 
 
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
