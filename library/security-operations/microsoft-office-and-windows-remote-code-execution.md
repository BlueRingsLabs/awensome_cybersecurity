---
id: ckb-8740c017fd0e
title: Microsoft Office and Windows Remote Code Execution
category: security-operations
format: guide
language: en
tags: [firewall, log-analysis, networking, phishing, vulnerability-management, windows]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.38
---

CVE-2023-36884
Microsoft Office and Windows
HTML Remote Code Execution
investigate as Incident Responder
Table Of Content
Alert
Verify
Initial Access
IP Reputation
Containment
Lessons Learned
03
04
05
09
 17
 18
Author: Muhammet Donmez
Looking at the reason that triggers the Alert, it has been
found out that the system is trying to exploit the CVE-2023-
36884 vulnerability which is a critical level alarm with RCE
(Remote Code Execution).
A file named
“Overview_of_UWCs_UkraineInNATO_campaign.docx” is
shared under the downloads folder in the alert details. In
addition, the L1 analyst investigation noted that the file
“Overview_of_UWCs_UkraineInNATO_campaign.rar” was
sent to Anthony via e-mail.
First, this alert should be verified by checking the existing
logs, and then it should be determined whether the attack
was successful or not.
Alert
We start investigating the logs by searching the source IP
address (172.16.17.157) in the alert in the Log Management.
As a result of our searches, we have seen the OS, Proxy,
Firewall and AV/EDR logs.
We can check the AV/EDR logs to be able to confirm the
alarm. In the details of the relevant log, We see that the file
C:\Users\LetsDefend\Downloads\Overview_of_UWCs_Ukra
ineInNATO_campaign.doc file is paired with
“Exploit:O97M/CVE-2023-36884” and the malware was
quarantined.
We were able to verify that the alarm was True Positive
within our first examinations.
Verify
We should check our Email Security tool to confirm the email
mentioned in the L1 analyst note. Our search comes with at
result showing that the relevant user receives an e-mail with
the subject “Information about the "Ukraine in NATO"
Campaign” from the “no-war@freeukraine.io” sender.
We have also detected the
“Overview_of_UWCs_UkraineInNATO_campaign.rar” file
when we check the emails attachment.
Initial Access
Now, we need to review 2 critical points here. We first need to
confirm whether the file has been downloaded and if it was
run on the system. We can go through and investigate the OS
logs in detail for 172.16.17.157. As a result of our search, we
found out that the following file was created at 01:06 PM:
“C:\Users\LetsDefend\Downloads\~$erview_of_UWCs_Ukr
aineInNATO_campaign.doc”.
We also found out that the file was run over WinWord.exe
within the same minute:
“C:\Users\LetsDefend\Downloads\Overview_of_UWCs_Ukr
aineInNATO_campaign.doc”. This confirms that the
malware infected the system via an e-mail. We should
extend our search on the Email Security tool to make sure if it
is a phishing or spear phishing attack by searching the
sender email address and subject and see if there are any
other user who received the same or similar emails.
Our searches on both subject and sender addresses on our
Email Security tool showed that the malicious e-mail was
only sent to anthony[@]letsdefend.io which we can consider
as a “Phishing: Spearphishing Attachment (T1566.001)” for
initial access.
We can continue our investigations with other logs remaining
on the Log Management. Again, when a search for the
172.16.17.157 IP address, network traffic towards
“192.229.211.108” and “74.50.94.156” over port 80 stand
out.
We can continue our investigations with other logs remaining
on the Log Management. Again, when a search for the
172.16.17.157 IP address, network traffic towards
“192.229.211.108” and “74.50.94.156” over port 80 stand
out.
When we review If these three logs in detail, we see both
proxy and firewall logs towards 74[.]50[.]94.156 IP
address. Here in the detail of the proxy log, we see that a GET
request was sent to
"http[:]//74[.]50[.]94.156/MSHTML_C7/start.xml" and the
"WINWORD.EXE" process was the source of this request
which could be the reason why we see the traffic on the
firewall. No information is shared regarding the traffic
towards the 192,229,211.108 IP address in the raw data.
We have detected that the malicious file that was run on the
system came via an e-mail within our initial examinations.
When a conduct a search for "Anthony" on the Log
Management tool, we see the mail traffic in the exchange
logs that originates from no-war[@]freeukraine.io email
address with the source IP of 23.94.78.60.
We should also conduct the IP reputation check for
“23.94.78.60” that we detected on the exchange logs as
well as the “74.50.94.156” and “192.229.211.108” IP
addresses that are queried over port 80.
IP Reputation
Finally, the risk score of “23.94.78.60” IP address came out
clean at the end of our reputation control. Following the IP
reputation check, we should also conduct a hash check of the
Overview_of_UWCs_UkraineInNATO_campaign.doc file
shared in the alarm details.
Hash :
A61B2EAFCF39715031357DF6B01E85E0D1EA2E8EE1DFEC241
B114E18F7A1163F
The hash control we performed on multiple sources show that
all the sources reported this hash as malicious. VirusTotal
also associates it with the "CVE-2023-36884" vulnerability
in some sources.
When we search for the details of this vulnerability, we see
that the “74.50.94.156” IP address is shared in the IOC lists
in all sources.
The request that was made to
"hxxp://74.50.94.156/MSHTML_C7/start.xml" is an attempt
to download a file named "start.xml" to the system.
References: https://www.joesecurity.org/reports/report-
d227874863036b8e73a3894a19bd25a0.html
https://blogs.blackberry.com/en/2023/07/romcom-
targets-ukraine-nato-membership-talks-at-nato-summit
In the investigations made so far, we have found out that a
file associated with CVE-2023-36884 was downloaded to
the system and requests towards the “74.50.94.156” IP
address which is among the shared IOCs for the related
vulnerability. You can determine whether the relevant file
was run or not by reviewing the logs in the Event Viewer on
the system. You can connect to the system through the
Endpoint Security tool by pressing the "connect" button.
You should follow the path the below path to open the
Sysmon after connecting to the system:
Event Viewer->Application and Services Logs->Microsoft-
>Windows->Sysmon->Operational
When the related file is searched in the File create logs, we
see that the related file was extracted using 7zip at 01:06:49
PM.
Then, you can search for
“Overview_of_UWCs_UkraineInNATO_campaign.docx” file
in the Process Create logs. And, as a result, we see that the
file was opened via winword.exe in the relevant log records.
We see that there are a large number of Event ID: 3 (network
connections) in a short time after the related process runs.
Winword.exe is the process in these logs. Although most of
these connections (port 443) are considered to be harmless,
traffic over port 80 may worth checking.
Then, you can search for
“Overview_of_UWCs_UkraineInNATO_campaign.docx” file
in the Process Create logs. And, as a result, we see that the
file was opened via winword.exe in the relevant log records.
We see that there are a large number of Event ID: 3 (network
connections) in a short time after the related process runs.
Winword.exe is the process in these logs. Although most of
these connections (port 443) are considered to be harmless,
traffic over port 80 may worth checking.
Now, we need to check the Defender AV to see whether it
detected these activities or not. For this we can open Virus &
Threat Protection > Threat History and see the alarm that
was quarantined.
IP Reputation
So far, we have found out that Anthony downloaded a
malicious file that was sent through an email. We have
confirmed through the logs that he opened that malicious
file after downloading it to the system. We have also
detected network traffic towards malicious IP address
“74.50.94.156”. We see that the malicious file was reported
with reported with CVE-2023-36884 when we review its
reputation record which is why the system should be isolated
from the network.
Containment
Vulnerable products should not be used in
servers/clients,
We should increase the users' awareness of information
security with routine trainings and phishing tests,
AV/EDR products on the systems must be active at and
their signatures must be up to date at all times.
Lessons Learned
