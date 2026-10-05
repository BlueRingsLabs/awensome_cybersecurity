---
id: ckb-2941cc0c02f4
title: Most Critical Failure in Corporate Environments
category: offensive-security
format: guide
language: en
tags: [evasion, git, malware, mitre-attack, ransomware, tls]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.47
---

most common failure in
corporate environments
joas antonio dos santos
[~]$
[~]$
wh
Red team leader and instructor at hackersec
Contributor and researcher at miter att&ck
owasp project leader
author and speaker
+90 international certifications
Numerous CVs reported
oami
25%
18%
15%
15%
14%
6%
botnet
infostealer
cryptominers
banking
mobile
ransomware
30%
23%
19%
19%
14%
8%
botnet
infostealer
cryptominers
banking
mobile
ransomware
43%
30%
25%
25%
13%
10%
botnet
infostealer
cryptominers
banking
mobile
ransomware
25%
18%
15%
15%
14%
6%
botnet
infostealer
cryptominers
banking
mobile
ransomware
30%
23%
19%
19%
14%
8%
botnet
infostealer
cryptominers
banking
mobile
ransomware
43%
30%
25%
25%
13%
10%
botnet
infostealer
cryptominers
banking
mobile
ransomware
31%
21%
19%
19%
14%
8%
botnet
infostealer
cryptominers
banking
mobile
ransomware
global
americas
emea
apac
source:checkpoint
31%
21%
19%
19%
14%
8%
botnet
infostealer
cryptominers
banking
mobile
ransomware
source:connectwise
top 10 top cybersecurity threats
vulnerabilities:
newly discovered critical vulnerabilities in microsoft exchange
and advances in phishing create new areas for msps to monitor.
data center attacks:
these malicious activities are aimed at compromising the
security of data centers, facilities that house computer
systems, and other critical infrastructure.
cloud-based attacks:
With so many companies using the cloud and cloud networks
becoming more complex, your infrastructure has become an easy
target for digital threat actors.
Commitment corporate email:
when a cybercriminal gains access to a corporate email, they
can use it to send phishing, steal confidential information or
use the account to launch attacks.
crime-as-a-service:
this describes the provision of cybercriminal tools, services
and expertise through an underground, illicit market.
supply chain attacks:
Hackers infiltrate supply chain technology to access source
code, builds, and other infrastructure components of benign
software applications.
ransomware:
this form of cyber attack has been around for decades, and
hackers continue to develop and evolve their methods.
iot device hacking:
with many employees accessing sensitive company platforms and
data from multiple dispersed endpoints, hackers have more
opportunities for infiltration.
internal threats:
once internal system users are compromised, they can become an
even greater threat to the system than external attackers.
State-sponsored cyber warfare:
cyberattacks by one nation-state against another for strategic
or military purposes, often carried out by well-funded
companies and highly skilled teams of hackers or cyber
soldiers.
apt115 ac3r0l4
ac3r0l4timeline
emerged in 2015
in Brazil
dominant player
in selling
ransomware and
0days
Presence on popular
surface hacking forums
such as raidforums,
breached, cracked, and
xss.
ransomwareknown as
t1r4d3nt3s
variants sold on
genesis marketing
detection of your
operations in 15+
countries with
multiple ransomware
operators
task force created by
fireeye + mandiant +
trendmicro resulted in
apt115
06/2015
02/2016
01/2018
04/2019
03/2020
09/2021
10/2022
modus operandi
social engineering kit
polymorphic ransomware +
sophisticated ttps
bitcoin, monero and
ethereum wallets
invasions + theft and
kidnapping of data in
fortune 1000 companies
shared command and control
server (cobalt strike)
Private virtual private
servers from countries
like (Iran, Venezuela,
Panama and Switzerland)
vpn (airvpn, alerdium and
mullvad) and tor (whonix
or tails)
buying company access to
forums
vulnerability exploit kit
(0days), e.g. 0daytoday
tactics, techniques and procedures (ttps)
“att&ck mitre is a framework that maps cyber adversary
tactics and techniques to help defend and understand
cybersecurity threats.”
ttps (tactics, techniques and procedures) are a set of
specific strategies and actions used by adversary
actors to carry out cyber attacks, being important for
understanding and defending against these threats.
mitre att&ck and ttps
to the tacticsare
the tactical
objectives that a
threat can use
during an
operation.
to the
techniquesdescribe
the actions that
threats take to
achieve their
goals.
You procedures are
the technical steps
required to perform
the action.
source:redteam.guide
mitre att&ck and ttps
apt115 ac3r0l4 simulation
[~]$
initialaccess.ps1 --help
initial access
refers to the point at which the opposing team gains initial
unauthorized access to a target system or network
social engineering (spear-phishing + malicious pdf)
0day exploit: cve-2022-22965 (rce spring framework), cve-2021-44228
(log4j) and cve-2022-30190 (follina)
credential dump (i have been pwned + dump leak)
creation of payloads to manage compromised targets through a c2
initialaccess
metasploit framework (msfvenom)
vulnerability exploitation and
shellcode generation
exploit pack
development of exploits and
0days
macro pack
generate malicious documents
with vba macro
bad pdf generator
generate malicious pdf:
https://github.com/cybersecurity
up/badpdf-generator
gophishing + evilginx
carry out phishing campaigns
cobalt strike
manage compromised machines on a
command and control server,
using beacons and payloads
[~]$
evasion.cpp --help
evasion
refers to when the opposing team uses techniques to evade detection of
a protection mechanism and persist in a compromised environment.
configure a vpn to cloak network traffic
process injection techniques
exploration of defense mechanisms
obfuscation and payload encryption
use of valid accounts
evasion
atompepacker
packaging and file encryption:
https://github.com/nul0x4c/atomp
epacker
blackout
disable – edr and avs using
loldrivers (gmer64.sys)
https://github.com/zeromemoryex/
blackout
mortar – evasion techniques
binary encryption for av/edr
bypass
chimera
automation of automatic third-
party dll execution attacks (dll
sideloading):
https://github.com/georgesotiria
dis/chimera
airvpn
vpn service based on openvpn and
wireguard for hacktivism:
https://airvpn.org/
powershell obfuscation bible
collection of evasion techniques
in powershell:
https://github.com/t3l3machus/po
wershell-obfuscation-bible
[~]$
privesc.py --help
privilege escalation
refers to the point at which the adversary seeks to gain higher
privileges on a compromised system.
exploiting local vulnerabilities in cve
using lolbas to exploit incorrect permissions of an application
hash dump and domain controller attacks
valid accounts collected
privesc
peas-ng
escalation script suite
https://github.com/carlospolop/p
eass-ng
sweetpotato
a collection of various native
privilege escalation techniques
https://github.com/ccob/sweetpot
ato
elevatekit
privilege escalation kit for
cobalt strike
mimikatz
extract sensitive information
such as clear text passwords and
password hashes
[~]$
persistence.bat --help
persistence
refers to the point at which the opposing team gains continued access
to a compromised system
creation and modification of processes
create accounts on the machine
create scheduled tasks
rootkits (ring 3)
persistence
sharpersist
toolkit for persistence
https://github.com/mandiant/shar
persist
schedulerunner
customize scheduled tasks for
persistence
https://github.com/netero1010/sc
hedulerunner
r77
r77 hides in files, processes
and registry keys
https://github.com/bytecode77/r7
7-rootkit
lolbas
use built-in windows components
for persistence (binaries,
scripts and libraries)
[~]$
exfiltration.c --help
exfiltration and impact
refers to the point at which the opposing team steals information from
the network and compromises the availability of the environment.
data exfiltration via alternative protocols
data exfiltration through c2
ransomware development
exfiltration
dns-exfil
dns server created to exfiltrate
data
https://github.com/karimpwnz/dns
-exfil
sharpexfiltrate
uses secure channels as drivers
to exfiltrate data
https://github.com/flangvik/shar
pexfiltrate
cobalt strike
create https/dns beacon to
exfiltrate data
malware bazzar
malware samples to analyze or
use as a basis for creation.
RaasNet
Script that
generatesransomwarefor opponent
simulation
programming languages
go, c#, c++, python and ruby
prevention methods
source:network access
security in depth
risk management is the
process of identifying,
assessing and mitigating
risks that may affect an
organization, project,
process or activity.
The primary objective of
risk management is to take
proactive measures to reduce
the likelihood of adverse
events occurring and to
minimize their impact if
they do occur.
maturity
in
until
recommendation
insufficient
0.00
3.00
deal with
regular
3.01
5.00
to develop
good
5.01
7.50
to improve
very good
7.51
9.00
improve
great
9.01
10.00
to maintain
Risk management
nist-based maturity process
the nist cybersecurity
framework (csf) is a set of
guidelines and best
practices developed by the
us national institute of
standards and technology
(nist) to help organizations
manage and improve their
cybersecurity posture.
csf offers a flexible, risk-
based model that allows
organizations to tailor
their cybersecurity
strategies to their specific
needs.
identify
protect
to detect
to respond
to recover
asset Management
access control
anomalies and
events
response
recovery
business
environment
awareness and
training
continuous
security
monitoring
planning
planning
governance
data security
detection
processes
communications
improvements
risk assessment
information
protection
processes and
procedures
analyzes
communications
risk assessment
strategy
maintenance
mitigations
supply chain risk
management
protection
technology
improvements
cybersecurity solutions
source:cis
“Facilitate cybersecurity operations and
ensure effective controls across your
environment.”
this summarizes cybersecurity solutions
and their importance, and cis categorizes
at least 18 essential solutions for your
security maturity
and thesansmaps the top 20 security
controls through existing solutions on
the market.
Future of the cybersecurity market
source:burrelles
The hackersec as a business strategy
[~]$
cat thanks.txt
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%########## ###########*##*###**#****************************************** ****+=********#################%#%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%### ###################**#*####***************###***** *********+********################%%%%%
%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%% %###############*************+=+******************* ***+**************************#################%%%
%%%%%%%%%%%%%%%#%%%%%%%%%%%%%%%%%%%%%%#%%%%#%%%%%%% ###########*************++++++=+*****+*+******************
*****+++*************************************#################%%%
%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%##%%%%%#%%%%%%%%%## ##########**********++++=====--======+++*****+**** ****++++********************************+**###*######*######%##
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%#%%%### ######********+****++=---:-===+*#*++=++=+++******* *****+*++*********************#*##############%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###%%%%%%###### ##**************+=-------=+*#%%%#*###########*****+ *********************************############%%%%%%%%
%%%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##%########### ####*###******+=-------+##%%%%@@@@%%%%%%%%%#%%*+++ +++++**********+*++*************#############%###%
%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%%%#%%%%######## ##########****=-==-==+#%%%%@@%@@@%%%%%%%%%%%%@@%*= =++***+*************+********###############%##%%#*#
#%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%################## ###*#*******=-----=+*%@@%%%%%%%%%%####**+++*#%@@%* ++++++++++++++*****++*************#*###############%%##
%%%%%%%%%%%%%%#%%#%%%%%%%%%#%%%%#######%########### ##********+=-===+++#%@@@@%%%##***++==--::::::+%@@% *+++++++++=**+**************##################%##%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%####################### #********+--===+*#%@@@@@%#*+=------::::.....:=#@@ %*+++++++++++++++*************#####################
%%%#%%%%%%%%%%%%%%%%%%%%%%%%%#%#################### ####*****+=+++***#%@@@@%%#*+====--------:::::::-#@ @#*++++++********++**********########################
%%%%%%%%%%%%%%%%%###%%############################# **************++***#%@@@%%#*+==-----------::::.....=# @@*++++++*++**++**********+***############*############
%%%%%%%%%%%%%%%%%%%#%%%####*################*###### ********##***###%@@@@%#*+==-------------:::::::::* %@%*+++********************************##########################
#%%%%%%%%%%####################################***** *******#%%***###%@@@@#*++===---------------==+++== #@@#+++++++++++*************###**########*#########
%%%%%%%%%%%#######################################** ******%%%%**###%@@@@%#*++====++*****++++++###%##*+= #%@%*++***++==+*********###**######################
######################################*#####*##**** *****#%@%%#***#%@@@@%#*+++*#####%%%%#*+==*#%%%#+++ #%@@*++++++++++********+**#####**###########*#########
#################*##################*************** *****%@@@%#***%@@@@@%#*+******####%%#*-:.-*#%#*=-= *%@@#*++++++++++**********##**##***************###
#########################*##########*************** *****%@@@%#**#%@@@@@%#****###%%*+###*=-:..-+##**=- -*%@%#*++++************########*#***********#####*##
#################################****************** ****#%%@@%#+*%@@@@@@%**++++++**###*+=--:....:---:: :-#@@#*++************************************************#####*
################################*#***************** *****%%@@@#+#%@@@@@%#*++===++***+=-----:::::::::.. .:*%@%***************************************************######
##########################************* *****#%%%@#*%%@@@@@%#*+==-------::------+*+=:::.. .:*@@@#*++*****************************************************
#################*#########************* *****#%%%@##%@@@@@@@%#*++==----------=*####*-::::: --*@@@%**************************+****************
**************#************************************************ ******#%%@%%%@@@@@@@%#*++++==----:::::------:::..: :-
*%@@%***+++++++++********************************+****************
#*****##**###*######******************* *******#%%%%%@@@@@@@%#*++++**+++======+**#####*+=- -=#@@@@***++**+++************************************************
************************************************** +++++++*#%%##%%@@@@@@#+==+++**++==+********+=---- -=#@@@@*+++++++=+++++++*****************************
************************************************** *****++++#%%%%%%%@@@@%*++++++++++++++++++***##*+=--- -*%@@@%**+++++************************************************
******************************+**********+*+++++++++++ ++++++++*###%%%%%@@@@%%#++++++++++++++++++++++==--:- +%@%%#*++++++++++++++++++++++++*****+*************
*####*######**#***#######******#######***++++++**# **********#####%%%@@@@@@%#**+++++++++===----:::::+ %%%**********##*****########*****#########*##*#########
####*******########*****########****++=----==-==++ +**********####*#%%@@@%%%%%%##***++==-----====--+% %#***++*************+***#######*****###*######*****##
#***##########*#***############****=---======+=++++ +********++**######%%@%%%%%@%%%####******#######%%% ###***+*#####*######****#########*##****############*
#########*****########*##****##*=--=++++++==+++++* ******++++++***####%%%%%%%%%%@@%%%%%%%%%%%%@@@@%%# #*#*****+*#############***##############***########
*##******############*****####+=======+++*+++++*** ******++++********###%%%%%%%#%%%%%%%%%%%@@@@@@@%%#* ******#***++**###########*****#############*****###
#**##############****#########++*****++++++***++++ *******+++***#*****##%%#####%%@%%%%%%%%@@@@@%%%%## ###########++*########**#####****###############*#*
############*****#######*###===++**#####*++****+** #******+++++*##*****#########%@@%%##%%@@@@@%###### #############++#######*+########****###############
#########***###############+======+**#####******** ###****++++***#******########%@@%%%%%%@@@@%######## ###############++##################***##############
####*****#################*==++======++**###*+**** ####***++++************###############%%@%%#####*## ###############**++####################****#########
#***##%%%%##%%%%%%%%%%###*+++++++++===++++++******* *######**********##**********#############%%%%######*## ####%##%##%%%#%%###+*##%%%%%%#%%%%#%%%%%%#**###%##
#####################*+*##+==++++***++===+*+++++* *#%######******##********#####*-+*#++#%%%######*** ***#################*++#####################***+##
###################***#####+=++++++********+++++**#** **#%##****###*###********######+*++#%%#########** **+*############*#####*+*###%###%################**
########%%%%%%#***##%%%%##+==+++++++++++++++++=++++ **###%%##******##*************#*+-*#########*###** +*++=+*##########%##%#*+*#%%%%%%%%%%%%######%%%#
############*+*#####%%##*====+++++++++++++*+++++++ +++*#%%%%***#####*************##*=-#########*####** *+***+++++****############*+*######################
#########*+*###########*++===+++++++++++++++++++++* ++++++++**###*****************#*-=*#######**#%##*# *+++**++++++++=+*###%%%%%%%#++###%%%%%%%%%%%%%%%%%
#%%###*+*##%%%%%%%%%%#***++===++++++++++++++++++++++ +++++++*************************************#*+=*######***####**
*************+++*********+*###########++###################
###*+*#############+*%#++======+++++++++++++++=== ======+********##**************==*#####****####**+ ***++*************++###########*==#################
*++###%%%%%%##%%%%#+*#%#+=++==++++++++++++++++++== =+*****###%%%#########************=-*#####****####**+ +++*****#%##*****++*#%%%%%%%%%%%%#=+##%%%%%%%#%%%%
*#####%%%%%%%%%%%%#*#%%#++++=+++++*****+++++++++++++ +**#%%%@@%%#########**********#-=*####****#####*** ****##%#**##=*#**++#%%%%%%%%%%%%####=+#%%%%%%%%%%%
######################%#*++====+++**+*++++++++++++* **++++++*####%############****#-+#####***#####**** *****##%%##**##****+*################*=+##########
#%%%%%%%%#%%%%%%%%##%%##++++==+++*******++++++++*** *****++======*#################*=*##%#*#######***** ****###%%%%%%#******+*%%%%%%%%%%%%%%%%%*=*%%%%%%%%
*###############*#*#%###*+++==++********++++*+++** *****+++++****###***##########++##%%#*########***** ****#%%%##%%######*++=*###################+=+######
###%%%%%%%%%%%%##%%###%%@#*++++++******************************** *****########%%%%%##*#########+*#%%###########**** ***#%%%%%%%###%%%#*++=*#%%%%%%%%%%%%%%%%%%%*=*#%%%
########%%%%%###%##**#%##*+++++++**************** ******###########**+==+####**++##%%#########****** ***#%%%%%%#%%%##*+++++#%%%%%%%%%%%%%%%%%%%%##==*#%
******###########%##*#%##%****++++***************** ********++++++++====++++**++++++*###############*#* ***#%%%%%%%%#*****+**#*######################*#**==*
#########%%%%####**######+*+*++++**************** ******************############**+++=++***########### ##*#%%%%%%#+**###**###**#%%%%%%%%%%%%%%###%%%%%#*=
#######%%%%%%######%%####++***************#******* ****#####%%%%%%%%%%%%%%#########********+++*####### ###%%@@%#**##%#***#%%#*+*%%%%%%%%%%%%%%##%%%%%%###
*****#**#####**###%%%#%%*+*##******************** ****##########%%%%%%%%%%################**+++#%###% %##%%@%#**#%%#**#%%%#*++*************
######*###%%%###%%%%%###%***####****************** #####################%%%%%%%%##############**####%%% %%%@@@%##%%%#*##%%%*++***#%%%%%%%%%################
##########%####%%%%%#**##***###%##**********#*****## ###########################%%%%%%###########*###%%% %%%@@@%%%%%#*####***###**##%%%%%%%#%################
###########+-*%%@%#######***###%%##**###########%%% %%%%%%%%%%%%%%%%#################%%###########%%## #%@@@@%%@%#******##%%#****#############*############
##********+:=*#%%%%%#######**##%%%%#**####%%%%%%%% %%%%%%%%%%%%%%%%%%%%%%%%######################%%%%%% ##**%@%%%#****###%%#*++*************
%######*-=*###%%%#%%%#%%%%**##**#%%%%#####%%%%%@@@ @@@@@%@@@%%@@@@@@@@@@@@%%%%%%%%%%%%#%##%###%%%%%%% ###--*%%%#***#####*****###*##%%%%%%%####%%%#######
%####*=-*###%%%%%%%%##%%#***##*=-+%%%%%%%%%%%%@@@@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%% %%%+::=###******++++*#####*##%%%%%%%%%%%%%%%%%%#%#
####+-=######%%%%###*####***#%##*#@%@@%%%%@@@%@@@@ @@@@@@@@@@@%%%%%@@@%%@@@@@@@@@@@@@@@@%%%%%%%%@@@@@@ @@%#=-:=****######****+******#######################
**+-=********#%%%#*########**##%%%@@%%###%%@@@@%%@@ @@@@@@@@@@@@@@@@@@@@@@%%%%@@@@@@@@@@@@@@@@@@@@@@@@ @%#*************#######**********#####*###**####*#*
*--*#######%%###########%%**-+#%@%#**##%%@@%%@@@@% ####%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@% %%%@%#####***++++***#####***##%%%%%##%%%%%%%##%%##
-*#%%#%######*###%%%%%%@%####%%@%####%%%%%%%%@@@@@ %#**+******######%%%@@@@@@@@@@@@@@@@@%%%%%%%@%%%%% ####%%%##########*##**#####**#%%%%%%%%%%%%%%%%%%%%
#############*###%%####%####%%@%#**##%%%%%##%@%%@@ @@%%##*************%@@@@@@@@@%@@@@%%%%%###%%%%%%%# ########****##################%%%%%%%%%%%%%%#%%%%%
#%########%#################%%%#*########%#%%@%%%@ @@@@@@@%%###*******%@@@@@@@@%%%%%%%#########%%%%%%% %%%%%%%%%%##******##########%%%%%%%%%%%%%%%%%%%#%%
**********######***########%%%#**#%######%##%@%%%@ @@@@@@@@@@@%%%#####%@@%%%%%%%%%%%%################ #%%%%%%%@%%%%%##################**####*#####*####*##
%%%%%%%%%%%%%###**####%%%@@%%#****##*##%%%#%%%%#%@ @@@@@@@@@@@@@@@@%%%@@@@@@@%@@%@%%%%%%%%%%%%%%###** **##%%%%%%%@%%%%%%%###########%%%%%%%%%%%%%%%%%%%%%
%#####%%%%%%###*###%%%%%@@%#%%#*****##%%%%##%%##%% @@@@@@@@@@@@@@@@@@%@@%@%%%%@%%%@%%%%%%%%%%%%%%%%## #******##%%%%%%%%%%%#########%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%#####%%%%%@@@%#%@%*****##%%%%%%%%%#%%% %%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%% %%%####***#####%%%%%%#######%%%%%%%%%#%%%%%%%%%#%%
%%%%%%%%%%%%###%%%%%@@@%##%%#***##%%%%%%%#%%%%%%% %%%%%%%%@@@%%%%%%@@@@@@@@@@@@@@@@%%%@@@%@@@@%@@@@% %@@%%%%%##################%%%%%%%%%%%%#%%%%%%%%%%%#
linkedin — joas antonio dos santos
