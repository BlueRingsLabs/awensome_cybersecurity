[[ PAGE 1 ]]
Password Cracking: SMB 
 
                                                                                                 1 | P a g e  
 
 
 
 
[[ PAGE 2 ]]
Password Cracking: SMB 
 
                                                                                                 2 | P a g e  
 
Contents 
IntroducƟon ............................................................................................................................................ 3 
MITRE ATT&CK Techniques: ............................................................................................................ 3 
IntroducƟon to MSSQL (Port 1433) ......................................................................................................... 3 
EnumeraƟon............................................................................................................................................ 3 
Nmap Scan .......................................................................................................................................... 3 
Defensive Strategy: ......................................................................................................................... 4 
Brute-Force Techniques .......................................................................................................................... 4 
Tools Quick Reference ......................................................................................................................... 4 
Hydra ................................................................................................................................................... 4 
Step To Reproduce .......................................................................................................................... 4 
DetecƟon Strategy: ......................................................................................................................... 5 
Metasploit ........................................................................................................................................... 5 
Step To Reproduce .......................................................................................................................... 5 
Defensive Control: ........................................................................................................................... 6 
Medusa ............................................................................................................................................... 6 
Step To Reproduce .......................................................................................................................... 6 
Defensive Strategy: ......................................................................................................................... 6 
Netexec (aka nxc) ................................................................................................................................ 6 
Step To Reproduce .......................................................................................................................... 7 
Defensive Statergy: ......................................................................................................................... 7 
Ncrack ................................................................................................................................................. 7 
Step To Reproduce .......................................................................................................................... 7 
Defensive Strategy: ......................................................................................................................... 8 
Patator ................................................................................................................................................. 8 
Defensive SuggesƟon: ..................................................................................................................... 8 
Nmap NSE Script ................................................................................................................................. 8 
Step To Reproduce .......................................................................................................................... 9 
Defensive Strategy: ......................................................................................................................... 9 
MSSQL Brute-Force – Oﬀense, Defence & MITRE Mapping ................................................................. 10 
Defense-in-Depth Summary .................................................................................................................. 10 
 
 
 
[[ PAGE 3 ]]
Password Cracking: SMB 
 
                                                                                                 3 | P a g e  
 
 
Introduction 
MSSQL brute-force atacks are a frequent iniƟal access tacƟc during internal assessments and red 
team ops. MicrosoŌ SQL Server—commonly exposed on TCP port 1433—oŌen holds sensiƟve data 
and privileges, making it a high value target. When SQL authenƟcaƟon is enabled, atackers may 
exploit weak credenƟals using tools like Hydra, Metasploit, or Nmap NSE. 
This guide explores advanced techniques for exploiƟng MSSQL authenƟcaƟon mechanisms across 
diverse network environments. 
MITRE ATT&CK Techniques: 
• 
T1110.001 – Brute Force: Password Guessing 
• 
T1046 – Network Service Scanning 
• 
T1078 – Valid Accounts 
Introduction to MSSQL (Port 1433) 
MicrosoŌ SQL Server (MSSQL) is a relaƟonal database plaƞorm commonly deployed in enterprise 
networks to manage and store structured data. It communicates over TCP port 1433 and supports 
both SQL and Windows authenƟcaƟon mechanisms. While Windows authenƟcaƟon oﬀers beter 
security via AcƟve Directory integraƟon, SQL authenƟcaƟon remains widely used—oŌen with weak 
or default credenƟals. 
MSSQL instances, especially in internal or hybrid environments, can become high value targets due 
to their access to sensiƟve data and administraƟve privileges. Improperly secured deployments may 
allow atackers to exploit exposed services through brute force atacks, making MSSQL a criƟcal 
component in penetraƟon tesƟng and red teaming assessments. 
Enumeration 
Nmap Scan 
Firstly, to begin the enumeraƟon process, we perform an Nmap scan against the target IP address to 
idenƟfy an open MSSQL service and gather informaƟon about the server version. This helps conﬁrm 
the presence of a SQL Server instance and assess potenƟal vulnerabiliƟes based on version or 
conﬁguraƟon. 
nmap -p 1433 -sV 192.168.1.80 
ExplanaƟon: 
• 
-p 1433: Scans for the default MicrosoŌ SQL Server on port 1433. 
• 
-sV: Enables version detecƟon to idenƟfy the speciﬁc MSSQL version running on the target 
host. 
Once Nmap conﬁrms that port 1433 is open and an MSSQL service is acƟve, this informaƟon can be 
used to plan targeted authenƟcaƟon atacks or service speciﬁc exploitaƟon in the next phase. 
[[ PAGE 4 ]]
Password Cracking: SMB 
 
                                                                                                 4 | P a g e  
 
 
Defensive Strategy: 
Use IDS/IPS (e.g., Zeek, Suricata) to detect scan behavior. Limit SQL access to known IPs using 
ﬁrewall/NSG policies. 
Brute-Force Techniques 
Tools Quick Reference 
 
Hydra 
Hydra is parƟcularly eﬀecƟve in environments where SQL authenƟcaƟon is enabled and weak or 
default credenƟals are in use. The success of such atacks largely depends on the quality of the 
wordlists used, such as user.txt for usernames and pass.txt for passwords. The success of such atacks 
largely depends on the quality of the wordlists used, such as user.txt for usernames and pass.txt for 
passwords. 
Step To Reproduce 
To perform a brute force atack against an MSSQL service, use the following command: 
hydra -L user.txt -P pass.txt 192.168.1.80 mssql 
ExplanaƟon: 
• 
-L user.txt: Speciﬁes the path to the username list. 
• 
-P pass.txt: Speciﬁes the path to the password list. 
• 
192.168.1.80: Target IP address. 
• 
mssql: Protocol to atack. 
Hydra will systemaƟcally test each username-password pair against the MSSQL service on the 
speciﬁed host. If valid credenƟals are found, Hydra will clearly report the success. 
[[ PAGE 5 ]]
Password Cracking: SMB 
 
                                                                                                 5 | P a g e  
 
 
Detection Strategy: 
Enable SQL Server Audit or Extended Events. Detect failed logins (Event ID 18456) and alert via SIEM. 
Apply IP-based throtling using Fail2Ban or ﬁrewall rules. 
Metasploit 
Metasploit includes auxiliary module that enables automated brute force atempts with detailed 
logging, modular opƟons, and integraƟon into post exploitaƟon workﬂows. It's parƟcularly eﬀecƟve 
during red team simulaƟons where SQL Server access is needed for pivoƟng, lateral movement, or 
persistence. The framework’s output is structured, which makes it useful for integraƟon with 
reporƟng tools or pipelines. 
This module simply queries the MSSQL instance for a speciﬁc user/pass (default is sa with blank). 
Step To Reproduce 
msf6 > use auxiliary/scanner/mssql/mssql_login 
set rhosts 192.168.1.80 
set user_file user.txt 
set pass_file pass.txt 
set verbose false 
run 
ExplanaƟon: 
• 
use auxiliary/scanner/mssql/mssql_login: Loads the MSSQL login scanner module used for 
brute force authenƟcaƟon. 
• 
set rhosts 192.168.1.80: Speciﬁes the IP address of the target MSSQL server. 
• 
set user_ﬁle user.txt: Deﬁnes the ﬁle containing potenƟal usernames. 
• 
set pass_ﬁle pass.txt: Deﬁnes the ﬁle containing passwords to pair with the usernames. 
• 
set verbose false: Disables verbose output to reduce console noise during the brute force 
process. 
• 
run: Executes the module and begins tesƟng all username password combinaƟons against 
the MSSQL service. 
[[ PAGE 6 ]]
Password Cracking: SMB 
 
                                                                                                 6 | P a g e  
 
 
Defensive Control: 
Monitor audit logs for repeated failures. And addiƟonally block sources using host ﬁrewall or NSG. 
Detect scan to login sequences. 
Medusa 
Medusa is designed to support large scale login atempts by tesƟng mulƟple username password 
combinaƟons simultaneously across mulƟple hosts or services. It is parƟcularly eﬀecƟve in internal 
environments where SQL authenƟcaƟon is enabled. 
In this case, we can eﬃciently atempt login combinaƟons against MSSQL targets using prepared 
dicƟonaries such as user.txt and pass.txt. 
Step To Reproduce 
Below we have successfully grabbed credenƟals using following command: 
medusa -h 192.168.1.80 -U user.txt -P pass.txt -M mssql | grep "ACCOUNT FOUND" 
ExplanaƟon: 
• 
medusa: Invokes the Medusa brute force tool. 
• 
-h 192.169.1.80: Speciﬁes the IP address of the target machine. 
• 
-U: Points to a ﬁle containing a list of usernames to try. 
• 
-P: Points to a ﬁle containing a list of passwords. 
• 
-M mssql: Indicates that the MSSQL module should be used for this atack. 
• 
| grep “ACCOUNT FOUND”: Filters the command output to display only successful login 
atempts, making it easier to idenƟfy valid credenƟals. 
 
Defensive Strategy: 
Detect bulk login failures with SIEM correlaƟon. Enable lockout policies and rate limits per IP. 
Netexec (aka nxc) 
Among its many capabiliƟes, NetExec can, for example, perform brute force atacks on MicrosoŌ SQL 
Server by using speciﬁed username and password lists. It is parƟcularly useful for mass validaƟon of 
[[ PAGE 7 ]]
Password Cracking: SMB 
 
                                                                                                 7 | P a g e  
 
credenƟal pairs obtained during earlier recon or OSINT phases, especially in internal environments 
where SQL authenƟcaƟon is enabled and network segmentaƟon is limited. 
Step To Reproduce 
To iniƟate a brute force atack against an MSSQL service using NetExec, run the following command: 
nxc mssql 192.168.1.80 -u user.txt -p pass.txt --local-auth | grep [+] 
ExplanaƟon: 
• 
nxc: Invokes the NetExec burte force tool 
• 
mssql: Speciﬁes the protocol to target for MSSQL. 
• 
192.168.1.80: The IP address of the target host. 
• 
-u user.txt: Path to the ﬁle containing a list of usernames. 
• 
-p pass.txt: Path to the ﬁle containing a list of passwords. 
• 
| grep [+]: Filters the command output to display only successful login atempts, making it 
easier to idenƟfy valid credenƟals. 
 
Defensive Statergy: 
Monitor failed and successful logins. Limit SQL access by IP. Enforce Windows AuthenƟcaƟon where 
possible. 
Ncrack 
Ncrack supports modular conﬁguraƟon and mulƟthreaded execuƟon, allowing for eﬃcient brute 
force atempts while maintaining connecƟon stability and performance. 
In MSSQL-focused operaƟons, Ncrack is ideal for quickly tesƟng username and password pairs 
against exposed database services, parƟcularly in misconﬁgured or externally accessible SQL 
environments. 
Step To Reproduce 
ncrack -U user.txt -P pass.txt 192.168.1.80 -p 1433 
ExplanaƟon: 
• 
ncrack: Launches the Ncrack password-cracking tool. 
• 
-U user.txt: Indicates the ﬁle containing a list of potenƟal usernames. 
• 
-P pass.txt: Indicates the ﬁle containing a list of potenƟal passwords. 
• 
-p 1433: Speciﬁes the MSSQL default port for authenƟcaƟon atempts. 
[[ PAGE 8 ]]
Password Cracking: SMB 
 
                                                                                                 8 | P a g e  
 
 
Defensive Strategy: 
Rate-limit MSSQL connecƟons per IP. AddiƟonally, use NIDS to alert on rapid authenƟcaƟon 
atempts. Finally, restrict internet-facing SQL endpoints to minimize exposure. 
Patator 
Patator allows ﬁne-grained control over brute force behavior—such as custom delays, retry logic, 
and error handling—making it especially useful in stealthy or evasion-focused engagements. 
It can be used to perform MSSQL brute force atacks by iteraƟng through supplied username and 
password lists which in this case will be user.txt and pass.txt. 
patator mssql_login host=192.168.1.80 user=FILE0 0=user.txt password=FILE1 1=pass.txt 
ExplanaƟon: 
• 
patator: Launches the Patator brute force tool. 
• 
mssql_login: Speciﬁes the module for MicrosoŌ SQL Server login atempts. 
• 
host=192.168.1.80: Indicates the target machine’s IP address. 
• 
user=FILE0 0=user.txt: Assigns FILE0 as a placeholder for usernames, pulling values from 
user.txt. 
• 
password=FILE1 1=pass.txt: Assigns FILE1 as a placeholder for passwords, pulling values 
from pass.txt. 
 
 
Note: You can add | grep ‘200 OK’ or -x ignore:code=530 for success ﬁltering or to skip known failed 
responses based on Patator’s output codes. 
Defensive Suggestion: 
Detect retry paterns via audit logs. Apply per-IP throtling. AddiƟonally, Use IPS to block based on 
behavioural heurisƟcs. 
Nmap NSE Script 
The ms-sql-brute.nse script allows testers to perform credenƟal based login atempts against 
MicrosoŌ SQL Server using customized username and password lists. 
[[ PAGE 9 ]]
Password Cracking: SMB 
 
                                                                                                 9 | P a g e  
 
Step To Reproduce 
Firstly, to perform a brute force atack against an MSSQL service using Nmap, run the following 
command: 
nmap -p1433 --script ms-sql-brute.nse --script-args userdb=user.txt,passdb=pass.txt 192.168.1.80 
ExplanaƟon: 
• 
–p1433: Scans the default port used by MSSQL. 
• 
–script ms-sql-brute.nse: Speciﬁes the use of the MSSQL brute force NSE script. 
• 
–script-args userdb=user.txt,passdb=pass.txt: Provides the script with your custom username 
and password lists. 
This method is especially useful during early stage reconnaissance to idenƟfy weak or default MSSQL 
credenƟals on a target system. 
 
Defensive Strategy: 
Detect sequenƟal login failures Ɵed to Nmap scans. Block oﬀending IPs and alert via SIEM. 
[[ PAGE 10 ]]
Password Cracking: SMB 
 
                                                                                                 10 | P a g e  
 
MSSQL Brute-Force – Offense, Defense & MITRE Mapping 
 
Defense-in-Depth Summary 
 
To learn more about Password Cracking. Follow this Link. 
[[ PAGE 11 ]]
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
