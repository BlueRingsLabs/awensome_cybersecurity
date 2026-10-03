[[ PAGE 1 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 1 | P a g e  
 
 
 
 
[[ PAGE 2 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 2 | P a g e  
 
Contents 
IntroducƟon ............................................................................................................................................ 3 
cat ............................................................................................................................................................ 3 
cd and pwd .............................................................................................................................................. 4 
checksum ................................................................................................................................................ 4 
cp ............................................................................................................................................................. 4 
dir ............................................................................................................................................................ 5 
download ................................................................................................................................................ 5 
edit .......................................................................................................................................................... 5 
getlwd ..................................................................................................................................................... 7 
getwd ...................................................................................................................................................... 7 
lcd ............................................................................................................................................................ 8 
lls ............................................................................................................................................................. 8 
lpwd......................................................................................................................................................... 8 
ls .............................................................................................................................................................. 9 
mkdir ....................................................................................................................................................... 9 
mv............................................................................................................................................................ 9 
pwd ....................................................................................................................................................... 10 
rm .......................................................................................................................................................... 10 
rmdir ..................................................................................................................................................... 11 
search .................................................................................................................................................... 11 
show_mount ......................................................................................................................................... 11 
upload ................................................................................................................................................... 12 
 
 
 
 
 
 
 
 
 
 
[[ PAGE 3 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 3 | P a g e  
 
 
Introduction 
Hey Friends!  
Did you know that meterpreter is known as Hacker’s Swiss Army Knife!! 
Well! Now you do. 
Meterpreter, a highly developed payload that can be extended dynamically, is known to be Hacker’s 
Swiss Army Knife. It uses a reﬂecƟve DLL injecƟon technique to further compromise the target aŌer 
the atack. Meterpreter is known to inﬂuence the funcƟonality of the Metasploit framework. It can 
help in doing a lot many things. Some of these include covering tracks aŌer the atack, accessing the 
operaƟng system, and dumping hashes. 
This arƟcle discusses meterpreter’s Stdapi File System Commands. There are 21 commands 
including cat, cd, pwd, and checksum. Figure 1 summarises them: 
 
Let’s start discussing them. 
cat 
It is the very ﬁrst command in the group of Stdapi File System Commands. It reads the contents of a 
ﬁle to the screen. In other words, cat displays a ﬁle’s contents. cat command in meterpreter is same 
as cat command used in Unix/Linux systems.  
The syntax of cat in meterpreter is as follows: 
cat filename 
 
[[ PAGE 4 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 4 | P a g e  
 
 
cd and pwd 
Though cd and pwd commands are two separate commands, they are usually used together. cd 
stands for change directory and pwd stands for print working directory. You use pwd command to 
check the directory you are working in. You can change this directory using the cd command. By 
default, the current working directory is the one where the connecƟon was established. 
The syntaxes of pwd and cd commands in meterpreter are as follows: 
pwd 
cd <path of the folder to change to> 
 
 
checksum 
This command retrieves the checksum of a ﬁle. The syntax of the checksum command is as follows: 
checksum [md5/sha1] file1 file2 file 3... 
 
 
cp 
This command copies the content of the old ﬁle to the new ﬁle. The syntax of the cp command is as 
follows: 
cp <oldfile> < newfile> 
 
 
 
[[ PAGE 5 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 5 | P a g e  
 
dir 
This command lists ﬁles. It is an alias for the ls command. It provides crucial details related to any ﬁle 
or directories such as File Permissions, Size of File, Last modiﬁed date and ﬁle Name & Type. The 
syntax of the dir command is as follows: 
dir 
 
 
download 
This command downloads remote ﬁles and directories from a remote locaƟon to the local machine. 
The syntax of download command is as follows: 
download [options] src1 src 2 src3... destination 
 
 
edit 
This command edits a ﬁle. The syntax of edit command is as follows: 
edit <file name> 
 
 
When you press the Enter key, the screen displayed is as shown in the below image: 
[[ PAGE 6 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 6 | P a g e  
 
 
AŌer ediƟng the ﬁle, type: x to save the changes and exit, as shown in the below image 
[[ PAGE 7 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 7 | P a g e  
 
 
getlwd 
This command prints the working directory on the local machine that is, in our case it is Kali Linux. 
The syntax of the getlwd command is as follows: 
getlwd 
  
 
getwd 
This command prints the working directory. The syntax of the getwd command is as follows: 
getwd 
 
 
[[ PAGE 8 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 8 | P a g e  
 
lcd 
This command changes the working directory of the local machine that is, in our case it is Kali Linux. 
The syntax of lcd is as follows: 
lcd 
 
 
You can see that local working directory changes to /root/Desktop 
lls 
This command lists ﬁles on the local machine that is, in our case it is Kali Linux. The syntax of lls 
command is as follows: 
lls 
 
 
lpwd 
This command prints the working directory on the local machine that is, in our case it is Kali Linux. It 
is the same as the getlwd command. The syntax of the lpwd command is as follows: 
lpwd 
 
 
[[ PAGE 9 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 9 | P a g e  
 
ls 
This command lists ﬁles. The syntax of the ls command is as follows: 
ls 
 
 
mkdir 
This command makes directory. The syntax of the mkdir command is as follows: 
mkdir dir1 dir2 dir3... 
 
 
mv 
This command moves a ﬁle from source to desƟnaƟon and it can also be used to rename the ﬁle as 
shown.  The syntax of the mv command is as follows: 
mv oldfile newfile 
[[ PAGE 10 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 10 | P a g e  
 
 
You can see the moved contents using cat command. 
pwd 
This command prints the working directory. The syntax of the pwd command is as follows: 
pwd 
 
 
rm 
This command deletes the speciﬁed ﬁle. The syntax of the rm ﬁle is as follows: 
rm file1 [file2...] 
 
 
[[ PAGE 11 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 11 | P a g e  
 
You can see the list of ﬁles before and aŌer using rm command. 
rmdir 
This command removes the directory. The syntax of the rmdir command is as follows: 
rmdir dir1 dir 2 dir 3... 
 
 
search 
This command search for ﬁles. The syntax of the search command is as follows: 
search -f *.doc 
 
 
show_mount 
This command list all mount points/logical drives. The syntax of the show_mount command is as 
follows: 
show_mount 
[[ PAGE 12 ]]
Meterpreter File System Commands Cheatsheet 
 
                                                                                                 12 | P a g e  
 
 
upload 
This command uploads a ﬁle or directory. The syntax of the upload command is as follows: 
upload [options] src1 src2 src3... destination 
 
 
You can see the uploaded ﬁle, as shown in the below image: 
 
To understand the fundamentals of Meterpreter. Click on this link. 
 
[[ PAGE 13 ]]
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
