[[ PAGE 1 ]]
CERTIFIED 
RED TEAM 
LEADER (RTO 
II) – Overview 
to Study
https://www.linkedin.com/in
/joas-antonio-dos-santos
[[ PAGE 2 ]]
C2 Infrastructure
• Command and Control Infrastructure, also known as C2 or C&C, is the 
set of tools and techniques that attackers use to maintain 
communication with compromised devices following initial 
exploitation. The specific mechanisms vary greatly between attacks, 
but C2 generally consists of one or more covert communication 
channels between devices in a victim organization and a platform that 
the attacker controls. These communication channels are used to 
issue instructions to the compromised devices, download additional 
malicious payloads, and pipe stolen data back to the adversary.
[[ PAGE 3 ]]
C2 Infrastructure - Basic C2 Setup
Let's start by discussing the design for a basic 
C2 setup. First, we'll want to have a server that 
will publish our tasks and receive the results of 
those tasks (also known as a "listening post"). 
Next, we want to have a program that will run 
on a target computer and make contact with
our server periodically to find out what tasks to 
perform, execute those tasks, then respond 
back with the results (also known as an 
"implant"). Lastly, we'll want to have a client 
where an operator can easily create, manage 
and submit tasks. Tasks could include things like 
returning information about the 
computer/network the implant is running on, 
executing OS commands, enumerating 
processes/threads, injecting into another 
process, establishing persistence or stealing 
credentials for lateral movement. The flow of 
this setup looks like the diagram below:
[[ PAGE 4 ]]
C2 Infrastructure - Basic C2 Setup
To make our basic setup more resilient, we can include another server 
that proxies communication from implants and forwards traffic along to 
the listening post, also known as a "redirector". With the inclusion of 
redirectors, you never need to expose the address of your listening post 
to the implant. Thereby denying this information to any defender who 
happens to capture/analyze your C2 communications. Another benefit is 
that you can have multiple redirector addresses in your implants and that 
way, if one of your redirectors gets taken down or blocked, your implant 
can simply fall back to using one of the others.To address the issue of 
segmentation, you can have multiple listening posts responsible for 
handling different aspects of your operation. For instance, one way to 
segment the design is to have a server that handles day-to-day C2 
communications and is for "hands on keyboard" type activities where you 
want instant feedback or "short haul" tasks. Then, you can have another 
server that would be for re-establishing access in the target network or 
"long haul" tasks. The idea being, you expect your noisier short haul 
channel to be taken down regularly and you can use your quieter long 
haul channel to regain access. Ideally, your long haul C2 channel will have 
different network/host indicators as well. The flow of this more resilient 
setup looks like the diagram below:
[[ PAGE 5 ]]
C2 Infrastructure – Redirectors Nginx
1.hide the true location of the C2 server;
2.mimic legitimate communication;
3.allow only malware control traffic to reach the real C2 server;
4.be reliable — given detection the part of C2 infrastructure, 
still, maintain C2 channel to the target.
Simple port forwarding by tools like socat or SSH can solve 
bullet #1 and partly #4. However, to address bullets #2 and #3 
we need to introduce more sophisticated redirectors — hosts, 
which act as reverse proxies to forward only specific traffic to 
the real C2 server, whilst serving counterfeit content for the 
arbitrary visitor.
[[ PAGE 6 ]]
C2 Infrastructure 
– Redirectors 
Apache2
•
Replace TEAMSERVER-IP with the WAN IP of your Cobalt Strike team server. After saving the file, 
Apache will send requests for an approved URI with the user-agent configured in the Malleable C2 
profile to our Cobalt Strike team server and redirect all other requests to http://example.com/. The 
question mark towards in line 7 ends the rewrite and redirects the user to exactly 
http://example.com/. If you want to retain the original request URI, delete the question mark.
•
Notice that the two expected HTTP URIs on line 4 are split by a pipe, enclosed in parentheses, 
and omit the leading forward slash. You can add other URIs the same way; this line is evaluated as a 
regular expression. Also note that the HTTP User Agent regex on line 3 requires all spaces, periods, 
and parentheses be escaped.
•
If you configure your Cobalt Strike listener to use a port other than port 80, you will need to 
configure Apache to listen on that port. By default on Debian, you can edit the port(s) Apache 
listens on in /etc/apache2/ports.conf and /etc/apache2/sites-enabled/000-default.conf.
[[ PAGE 7 ]]
C2 Infrastructure – Generate Certificate
1.
Use the keytool program to create a Java Keystore file. This program will ask “What is your first and last name?” 
Make sure you answer with the fully qualified domain name to your Beacon server. Also, make sure you take note of 
the keystore password. You will need it later.
2.
$ keytool -genkey -keyalg RSA -keysize 2048 -keystore domain.store
2.
Use keytool to generate a Certificate Signing Request (CSR). You will submit this file to your SSL certificate vendor. 
They will verify that you are who you are and issue a certificate. Some vendors are easier and cheaper to deal with 
than others.
3.
$ keytool -certreq -keyalg RSA -file domain.csr -keystore domain.store
3.
Import the Root and any Intermediate Certificates that your SSL vendor provides.
4.
$ keytool -import -trustcacerts -alias FILE -file FILE.crt -keystore domain.store
4.
Finally, you must install your Domain Certificate.
5.
$ keytool -import -trustcacerts -alias mykey -file domain.crt -keystore domain.store
•
And, that’s it. You now have a Java Keystore file that’s ready to use with Cobalt Strike’s Beacon.
You have the option to use a Valid SSL certificate with Beacon. 
Use a Malleable C2 profile to specify a Java Keystore file and a 
password for the keystore. This keystore must contain your 
certificate’s private key, the root certificate, any intermediate 
certificates, and the domain certificate provided by your SSL 
certificate vendor. Cobalt Strike expects to find the Java 
Keystore file in the same folder as your Malleable C2 profile.
[[ PAGE 8 ]]
C2 Infrastructure – SSH Tunnel
The image above shows the victim system has an SSH Tunnel 
configured to listen on port 5430 and forwards anything it 
receives to the Empire Server. The Empire Server has Empire 
running and listening on the same port on its own localhost 
(127.0.0.1:5430). To make the SSH traffic blend in a little more, 
we have the SSH server listening on port 443 instead of the 
standard port 22. Remember to edit your SSH config file to 
have it listen on this port and also edit your cloud provider 
firewall to let traffic on this port through.
You must create or copy a private key to your victim system 
before establishing the tunnel. The associated public key must 
be added to the authorized_keys file of your empire-server to 
allow the SSH connection. In this example, we have put the 
private key file on the victim machine at ~/.ssh/.do.key.
[[ PAGE 9 ]]
C2 Infrastructure – External C2
The External C2 Specification 
https://www.cobaltstrike.com/downloads/externalc2spec.pdf
https://github.com/Und3rf10w/external_c2_framework
https://github.com/rasta-mouse/ExternalC2.NET
https://github.com/outflanknl/external_c2
Example of External C2 over Discord.
https://www.youtube.com/watch?v=OB4Xk2bCaes
[[ PAGE 10 ]]
C2 Infrastructure
• https://www.varonis.com/blog/what-is-c2
• https://shogunlab.gitbook.io/building-c2-implants-in-cpp-a-primer/chapter-1-
designing-a-c2-infrastructure
• https://ditrizna.medium.com/design-and-setup-of-c2-traffic-redirectors-
ec3c11bd227d
• https://www.computerweekly.com/news/252512104/Cobalt-Strike-still-C2-
infrastructure-of-choice
• https://bluescreenofjeff.com/2016-06-28-cobalt-strike-http-c2-redirectors-with-
apache-mod_rewrite/
• https://github.com/BishopFox/sliver/wiki/HTTP(S)-C2
• https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/co
ntent/topics/malleable-c2_valid-ssl-certificates.htm
• https://www.blackhillsinfosec.com/sshazam-hide-your-c2-inside-of-ssh/
[[ PAGE 11 ]]
Windows APIs - Concept
• The Windows API, informally WinAPI, is Microsoft’s core set of 
application programming interfaces (APIs) available in the Microsoft 
Windowsoperating systems. The name Windows API collectively 
refers to several different platform implementations that are often 
referred to by their own names (for example, Win32 API); see the 
versions section. Almost all Windows programs interact with the 
Windows API. On the Windows NT line of operating systems, a small 
number (such as programs started early in the Windows startup 
process) use the Native API.
[[ PAGE 12 ]]
Windows APIs - SharpWMI
• SharpWMI is a C# implementation of various WMI functionality. This 
includes local/remote WMI queries, remote WMI process creation 
through win32_process, and remote execution of arbitrary VBS 
through WMI event subscriptions. Alternate credentials are also 
supported for remote methods.
https://github.com/GhostPack/SharpWMI
[[ PAGE 13 ]]
Windows APIs – COM Bypass
• https://www.exploit-db.com/exploits/44888
• https://gist.github.com/infosecn1nja/24a733c5b3f0e5a8b6f0ca2cf75
967e3
• https://www.linkedin.com/pulse/bypass-edr-av-detection-using-
windows-undocumented-harish/
• https://perspectiverisk.com/a-practical-guide-to-bypassing-userland-
api-hooking/
[[ PAGE 14 ]]
Windows APIs – MessageBox
• https://social.msdn.microsoft.com/Forums/vstudio/en-US/d70a77b7-
1508-4884-a5bc-106cf068b1be/how-can-i-show-messagebox-in-
visual-c?forum=vcgeneral
• https://www.clubedohardware.com.br/forums/topic/786981-
message-box/
• https://docwiki.embarcadero.com/CodeExamples/Sydney/en/Messag
eBox_(C%2B%2B)
[[ PAGE 15 ]]
Windows APIs – CreateProcess
• https://learn.microsoft.com/pt-
br/windows/win32/procthread/creating-processes
• https://www.youtube.com/watch?v=KKYU5baDjI4&ab_channel=ASys
temProgrammingChannel
[[ PAGE 16 ]]
Windows APIs – Platform Invoke
• P/Invoke is a technology that allows you to access structs, callbacks, and 
functions in unmanaged libraries from your managed code. Most of the 
P/Invoke API is contained in two namespaces: System and 
System.Runtime.InteropServices. Using these two namespaces give you the 
tools to describe how you want to communicate with the native 
component.
• https://learn.microsoft.com/en-us/dotnet/standard/native-
interop/pinvoke
• https://stackoverflow.com/questions/9369301/pinvoke-dll-in-c-sharp
• https://cursos.alura.com.br/forum/topico-implementacao-com-dll-por-
pinvoke-133383
[[ PAGE 17 ]]
Windows APIs – DInvoke
• https://ppn.snovvcrash.rocks/red-team/maldev/dinvoke
• https://github.com/TheWover/DInvoke
• https://pi0x73.github.io/DInvoke-As-A-Better-Evasion-Practice/
• https://www.tevora.com/threat-blog/dynamic-invocation-in-csharp/
• https://www.nuget.org/packages/DInvoke/
[[ PAGE 18 ]]
Windows APIs – VBA-
RunPE
• A simple yet effective implementation of 
the RunPE technique in VBA. This code 
can be used to run executables from the 
memory of Word or Excel. It is 
compatible with both 32 bits and 64 bits 
versions of Microsoft Office 2010 and 
above.
• https://github.com/itm4n/VBA-RunPE
[[ PAGE 19 ]]
Windows APIs to Evasion
• https://int0x33.medium.com/day-59-windows-api-for-pentesting-
part-1-178c6ba280cb
• https://thalpius.com/2020/11/02/microsoft-defender-antivirus-
attack-surface-reduction-rules-bypasses/
• https://learn.microsoft.com/en-us/microsoft-365/security/defender-
endpoint/attack-surface-reduction-rules-reference?view=o365-
worldwide
[[ PAGE 20 ]]
Process Injection
• https://gist.github.com/tothi/9cdd2be3b49cb42723726fd75df96471
• https://damienbod.com/2019/09/07/using-certificate-
authentication-with-ihttpclientfactory-and-httpclient/
• https://learn.microsoft.com/en-us/aspnet/core/fundamentals/http-
requests?view=aspnetcore-6.0
• https://www.thecodebuzz.com/bypass-ssl-certificate-net-core-
windows-linux-ios-net/
[[ PAGE 21 ]]
Process Injection - NtCreateSection + 
NtMapViewOfSection Code Injection (Sector 
Memory)
• https://www.ired.team/offensive-security/code-injection-process-
injection/ntcreatesection-+-ntmapviewofsection-code-injection
• https://cocomelonc.github.io/tutorial/2021/12/13/malware-
injection-12.html
• https://blog.omroot.io/process-code-injection-through-
undocumented-ntapis/
• https://idiotc4t.com/code-and-dll-process-injection/untitled
[[ PAGE 22 ]]
Process Injection using 
CreateRemoteThread API
• https://tbhaxor.com/createremotethread
-process-injection/
• https://github.com/tbhaxor/WinAPI-
RedBlue/tree/main/Process%20Injection
• https://www.ired.team/offensive-
security/code-injection-process-
injection/process-injection
• https://secarma.com/process-injection-
part-2-modern-process-injection/
• https://hstechdocs.helpsystems.com/ma
nuals/cobaltstrike/current/userguide/con
tent/topics/malleable-c2-
extend_process-injection.htm
[[ PAGE 23 ]]
Defence Evasion
https://hstechdocs.helpsystems.com/manuals/cobaltstrike/curr
ent/userguide/content/topics/post-exploitation_main.htm
[[ PAGE 24 ]]
Defence Evasion – Cobalt Strike Tradecraft
• https://hausec.com/2021/07/26/cobalt-strike-and-tradecraft/
• https://github.com/S1ckB0y1337/Cobalt-Strike-CheatSheet
• https://www.trustedsec.com/blog/red-teaming-with-cobalt-strike-not-so-
obvious-features/
• https://www.youtube.com/watch?v=7tvfb9poTKg&ab_channel=RaphaelM
udge
• https://www.trustedsec.com/wp-content/uploads/2019/01/013019-
Tradecraft-2.pdf
• https://www.youtube.com/watch?v=qsFOVOivxdI&ab_channel=RaphaelM
udge
• https://www.youtube.com/watch?v=IRpS7oZ3z0o&ab_channel=RaphaelM
udge
[[ PAGE 25 ]]
Defence Evasion – PPID Spoofing
• https://gist.github.com/rasta-
mouse/af009f49229c856dc26e3a243db185ec
• https://www.ired.team/offensive-security/defense-evasion/parent-
process-id-ppid-spoofing
• https://crypt0ace.github.io/posts/Staying-under-the-Radar/
• https://medium.com/@r3n_hat/parent-pid-spoofing-b0b17317168e
• https://offensivedefence.co.uk/posts/ppidspoof-blockdlls-dinvoke/
• https://pentestlab.blog/2020/02/24/parent-pid-spoofing/
• https://rioasmara.com/2022/04/16/less-detectable-with-ppid-spoofing/
• https://www.hackingarticles.in/parent-pid-spoofing-mitret1134/
[[ PAGE 26 ]]
Defence Evasion – CS Post Exploitation
•
https://hstechdocs.helpsystems.com/manuals/cobaltst
rike/current/userguide/content/topics/post-
exploitation_main.htm
•
https://www.deepinstinct.com/blog/cobalt-strike-post-
exploitation-attackers-toolkit
•
https://www.youtube.com/watch?v=Pb6yvcB2aYw&ab
_channel=RaphaelMudge
•
https://www.cobaltstrike.com/blog/post-exploitation-
only-not-really/
•
https://www.cobaltstrike.com/blog/my-favorite-
powershell-post-exploitation-tools/
•
https://www.logpoint.com/en/blog/how-to-detect-
stealthy-cobalt-strike-activity-in-your-enterprise/
•
https://github.com/CyberSecurityUP/Red-Team-
Management/tree/main/Adversary%20Emulation/Tool
s
•
https://github.com/CyberSecurityUP/AutoSudoBins
[[ PAGE 27 ]]
Defence Evasion – Stage 
and Decrypt Traffic 
• https://www.cobaltstrike.com/blog/user
-defined-reflective-loader-udrl-update-
in-cobalt-strike-4-5/
• https://www.mdsec.co.uk/2022/07/part
-2-how-i-met-your-beacon-cobalt-strike/
• https://github.com/RedXRanger/StageSt
rike
• https://labs.withsecure.com/publication
s/experimenting-bypassing-memory-
scanners-with-cobalt-strike-and-gargoyle
• https://blog.nviso.eu/2021/11/29/cobalt
-strike-decrypting-dns-traffic-part-5/
[[ PAGE 28 ]]
Windows Defender Application Control
•
To elaborate further, WDAC (Windows Defender Application Control) is a security feature introduced by Microsoft in Windows 10
that allows system administrators to restrict the execution of applications and drivers on a Windows machine. It is essentially a 
form of application whitelisting that specifies which applications and drivers are allowed to run on a system, based on a set of
policies defined by the administrator.
•
WDAC works by using code integrity policies that are enforced by the Windows kernel. These policies can be configured to allow 
only trusted and signed applications and drivers to run on a system, or to block specific applications and drivers based on their 
hash, file path, or other attributes.
•
One of the key differences between WDAC and AppLocker, another application whitelisting feature in Windows, is that WDAC is 
recognized by Microsoft as an official security boundary. This means that any bypass or vulnerability found in WDAC is considered 
a high-priority security issue and is usually fixed by Microsoft as soon as possible.
•
However, as with any security feature, WDAC is only as effective as the policies that are deployed on a particular system. If the 
policies are poorly configured or implemented, attackers can find weaknesses or loopholes to exploit and bypass WDAC 
protections. These weaknesses may include misconfigured policies, untrusted signing certificates, or vulnerable drivers that can be 
used to execute malicious code on a system.
•
Therefore, it is important for system administrators to carefully configure and manage WDAC policies to ensure maximum security 
and protection against potential threats. Additionally, regular security assessments and testing can help identify and address any 
weaknesses or vulnerabilities in the WDAC policies deployed on a particular system.
[[ PAGE 29 ]]
WDAC - LOLBINS
• https://www.securityhq.com/blog/security-101-lolbins-malware-
exploitation/
• https://github.com/LOLBAS-Project/LOLBAS
• https://www.anvilogic.com/learn/land-binaries
• https://n3dx0o.medium.com/abusing-living-off-the-land-binaries-
lolbins-for-data-exfiltration-7d6a0c13fa43
• https://threatpost.com/living-off-the-land-malicious-use-legitimate-
utilities/177762/
• https://informationsecurityasia.com/what-is-lolbas/
[[ PAGE 30 ]]
WDAC – Wildcard PrivEsc
• https://help.sumologic.com/docs/send-data/reference-information/use-
wildcards-paths/
• https://www.hackingarticles.in/exploiting-wildcard-for-privilege-
escalation/
• https://book.hacktricks.xyz/linux-hardening/privilege-escalation/wildcards-
spare-tricks
• https://www.linkedin.com/pulse/exploiting-wildcard-privilege-escalation-
aarti-singh/
• https://hackinglethani.com/advantage-of-wildcards/
• https://systemweakness.com/privilege-escalation-using-wildcard-injection-
tar-wildcard-injection-a57bc81df61c
[[ PAGE 31 ]]
WDAC – CodeSign
• https://pentestlab.blog/tag/code-signing/
• https://atos.net/en/solutions/cyber-security/data-protection-and-
governance/penetration-testing-services
• https://attack.mitre.org/techniques/T1553/002/
• https://www.youtube.com/watch?v=CR5YAwkGJQo&ab_channel=x33
fcon
• https://book.hacktricks.xyz/crypto-and-stego/certificates
• https://gbhackers.com/malware-stolen-code-signing-certificate/
[[ PAGE 32 ]]
WDAC – Vulnerable Applications 
• DLL hijacks: This vulnerability occurs when a trusted application tries to load a Dynamic Link 
Library (DLL) file that is not present in the system, but is placed by an attacker in a known search 
path. This can allow the attacker to execute arbitrary code in the context of the trusted 
application. However, as mentioned earlier, WDAC policies can be configured to prevent 
untrusted DLLs from loading, making it less likely for DLL hijacks to bypass WDAC.
• Buffer overflows: This vulnerability occurs when a buffer in a program is overflowed with more 
data than it can handle, allowing an attacker to execute arbitrary code or modify the program's 
behavior. If the vulnerable program is a trusted application, the attacker can potentially use this 
vulnerability to bypass WDAC protections.
• Code injection: This vulnerability occurs when an attacker is able to inject their own code into a 
running process, allowing them to execute arbitrary code in the context of the process. If the 
process is a trusted application, the attacker can potentially use this vulnerability to bypass WDAC 
protections.
• Deserialization: This vulnerability occurs when an attacker is able to manipulate the serialized 
data that is passed between different components of an application, allowing them to execute 
arbitrary code or modify the application's behavior. If the vulnerable component is a trusted 
application, the attacker can potentially use this vulnerability to bypass WDAC protections.
[[ PAGE 33 ]]
EDR Evasion – IAT Hooking
• https://www.ired.team/offensive-security/code-injection-process-
injection/import-adress-table-iat-hooking
• https://github.com/m0n0ph1/IAT-Hooking-Revisited
• https://unprotect.it/technique/iat-hooking/
• https://f3real.github.io/iat_hooking.html
• https://hakril.github.io/PythonForWindows/build/html/iat_hook.html
• https://pentest.blog/offensive-iat-hooking/
• https://guidedhacking.com/register/
• https://www.youtube.com/watch?v=jHrzmflNrgY&ab_channel=Tech69
[[ PAGE 34 ]]
EDR Evasion – Inline Hooking
• https://github.com/liuyx/inline-hook
• https://github.com/topics/inline-hook
• https://github.com/MalwareTech/BasicHook
• https://www.malwaretech.com/2015/01/inline-hooking-for-programmers-part-1.html
• https://www.youtube.com/watch?v=e4HZgx3A-wk&ab_channel=247CTF
• https://pentestlab.blog/tag/hooking/
• https://www.slideshare.net/htbridge/inline-hooking-in-windows
• https://blog.nettitude.com/uk/windows-inline-function-hooking
• https://www.ired.team/offensive-security/defense-evasion/detecting-hooked-syscall-
functions
• https://pentest.blog/art-of-anti-detection-4-self-defense/
• https://ppn.snovvcrash.rocks/red-team/maldev/api-hooking
[[ PAGE 35 ]]
EDR Evasion – Hooking Bypass Strategies
• Direct system calls: Instead of calling the API functions that are hooked, attackers can call the 
underlying system calls directly, which can bypass the hooks. For example, instead of calling the 
"CreateProcess" API function, an attacker can call the "NtCreateProcess" system call directly.
• Inline hooking: Attackers can use inline hooking to replace the hooked API function with their own 
code. This can allow them to intercept and modify the parameters passed to the API function, 
which can bypass the hooks.
• DLL hijacking: As mentioned earlier, DLL hijacking can allow an attacker to load their own 
malicious DLL instead of the legitimate one, which can bypass hooks that rely on the legitimate 
DLL.
• Process hollowing: Process hollowing is a technique where an attacker creates a new process, but 
then replaces the legitimate code in the process with their own malicious code. This can allow 
them to bypass hooks that rely on the legitimate process.
• Reflective DLL injection: Reflective DLL injection is a technique where an attacker loads a DLL into 
a process without relying on the Windows API functions that are hooked. Instead, the attacker 
uses their own code to map the DLL into the process's memory, which can bypass hooks that rely 
on the Windows API functions.
[[ PAGE 36 ]]
EDR Evasion – OffensiveCSharp
• This is a collection of C# tooling and POCs I've created for use on 
operations. Each project is designed to use no external libraries. Open 
each project's .SLN in Visual Studio and compile as "Release".
• https://github.com/matterpreter/OffensiveCSharp
• https://github.com/diljith369/OffensiveCSharp
[[ PAGE 37 ]]
EDR Evasion – Syscall
• https://cytomate.medium.com/on-disk-detection-bypass-avs-edr-s-using-syscalls-with-legacy-
instruction-series-of-instructions-8eabc6bd215f
• https://www.youtube.com/watch?v=w-p4JIZhJoA&ab_channel=ExploitBlizzard
• https://www.youtube.com/watch?v=rElV-T6DIQ8&ab_channel=WassimElMririe
• https://outflank.nl/blog/2019/06/19/red-team-tactics-combining-direct-system-calls-and-srdi-to-
bypass-av-edr/
• https://github.com/klezVirus/SysWhispers3
• https://conference.hitb.org/hitbsecconf2022sin/materials/D1T1%20-
%20EDR%20Evasion%20Primer%20for%20Red%20Teamers%20-
%20Karsten%20Nohl%20&%20Jorge%20Gimenez.pdf
• https://cymulate.com/blog/extracting-syscalls-from-a-suspended-process/
• https://ethicalchaos.dev/2020/06/14/lets-create-an-edr-and-bypass-it-part-2/
• https://captmeelo.com/redteam/maldev/2021/11/18/av-evasion-syswhisper.html
• https://deepsec.net/docs/Slides/2020/EPP:EDR-Unhooking_Their_Protections_Daniel_Feichter.pdf
[[ PAGE 38 ]]
EDR Evasion – Syscall and Artifact Kit
• https://www.youtube.com/watch?v=mZyMs2PP38w&ab_channel=Rap
haelMudge
• https://br-sn.github.io/Implementing-Syscalls-In-The-CobaltStrike-
Artifact-Kit/
• https://www.reddit.com/r/purpleteamsec/comments/kwbxv2/using_di
rect_syscalls_in_cobalt_strikes_artifact/?onetap_auto=true
• https://blog.xenoscr.net/2022/03/12/Implementing-Syscalls-in-Cobalt-
Strike-Part-1-Battling-Imports-and-Dependencies.html
• https://github.com/jthuraisamy/SysWhispers2
• https://toutiao.io/posts/9f35rvl/preview
[[ PAGE 39 ]]
EDR Evasion – Driver Signature
• https://learn.microsoft.com/en-us/windows-hardware/drivers/install/the-
testsigning-boot-configuration-option
• https://www.matteomalvica.com/blog/2020/07/15/silencing-the-edr/
• https://www.picussecurity.com/resource/blog/blackbyte-ransomware-
bypasses-edr-products-via-rtcore64.sys-abuse
• https://subscription.packtpub.com/book/security/9781789610789/8/ch08lvl
1sec52/bypassing-driver-signature-enforcement
• https://www.youtube.com/watch?v=HqzhQGSrLUM&ab_channel=SecurityW
eekly
• https://kalilinuxtutorials.com/edrsandblast/
• https://news.sophos.com/en-us/2022/10/04/blackbyte-ransomware-returns/
• https://evait.medium.com/disable-advanced-edr-solutions-by-abusing-
microsoft-signed-kernel-driver-eb8d0ed0faa3
[[ PAGE 40 ]]
Exam Review
• It's a very nice exam, I made a study group with some friends and we exchanged a lot of experiences and 
useful techniques. Mainly materials about C#, Rust and C++ development that were crucial for the exam and 
course
• A lot is not covered in the course, and this is great especially for you to try new methods, as there is no 
recipe for cake
• Follow all lab and exam instructions, it will help you a lot
• OpSec knowledge is absolutely crucial (https://github.com/trichlorne/simple-opsec)
• Evasion, Pivoting, Lateral movement is the strong point of the race, so I recommend that you invest in 
enumeration so you don't have problems in the next phases
• Do I need to do RTO I to do RTO II? It's super worth it, taking the RTO I will help you gain experience with C2 
and exploration techniques in AD environments. Even if you are someone who holds an OSEP or equivalent, 
it is a test that has its particular points that I guarantee will be a good complement of knowledge.
• Study a lot of cobalt strike, it's a tool that I particularly use in my daily life, not only for academic purposes, 
but even for adversary emulation and evasion games in EDR/AV
• Finally, keep calm during the test and breathe, you have enough time to do it and I guarantee it will be fun. I 
particularly follow some professionals who always post interesting content about Red Team, C2 and Evasion 
and I see that the test pulls a lot of modern points, nothing about legacy or exploitation of CVE from 2003
[[ PAGE 41 ]]
Exam Other Reviews
• Recommended Course: https://training.zeropointsecurity.co.uk/courses/rust-for-
n00bs https://training.zeropointsecurity.co.uk/courses/csharp-for-n00bs
• https://fluidattacks.com/blog/crtl-review/
• https://www.bencteux.fr/posts/rto2/
• https://0xash.io/Certified-Red-Team-Operator-Review/
• https://ferreirasc.github.io/crtl-review/
• https://blog.sunggwanchoi.com/red-team-ops-2-review/
• https://theasshat.net/reviews/crtl
• https://www.youtube.com/watch?v=U1wkhWOjKmM&ab_channel=JohnHammo
nd
• https://www.youtube.com/watch?v=eYCWhmk_bSc&ab_channel=JSONSEC
