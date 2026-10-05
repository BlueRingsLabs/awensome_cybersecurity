---
id: ckb-fe217c037742
title: AV and EDR Bypass Techniques for New Hackers Update 2022
category: offensive-security
format: guide
language: en
tags: [evasion, git, malware, mitre-attack, tls, windows]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.55
---

AV/EDR Bypass Techniques
for new Hackers
Joas Antonio (C0d3Cr4zy)
Whoami
• Asperger
• Red Team Leader, PenTester, Instructor
• Cyber Security Mentor
• Hacking is Not a Crime Advocate
What is EDR
and AV?
Concepts
What is EDR?
• Endpoint detection and response (EDR), also known as endpoint
threat detection and response (ETDR), is a cyber technology that
continually monitors and responds to mitigate cyber threats;
• Endpoint detection and response technology is used to protect
endpoints, which are computer hardware devices, from threat.
Creators of the EDR technology based platforms deploy tools to
gather data from endpoint devices, and then analyze the data to
reveal potential cyber threats and issues. It is a protection against
hacking attempts and theft of user data. The software is installed on
the end-user device and it is continually monitored. The data is stored
in a centralized database. In an incident when a threat is found, the
end-user is immediately prompted with preventive list of actions;
What is AV?
• Definition: Software that is created specifically to help detect,
prevent and remove malware (malicious software);
• Antivirus is a kind of software used to prevent, scan, detect and
delete viruses from a computer. Once installed, most antivirus
software runs automatically in the background to provide real-time
protection against virus attacks;
• Comprehensive virus protection programs help protect your files and
hardware from malware such as worms, Trojan horses and spyware,
and may also offer additional protection such as customizable
firewalls and website blocking;
AV X EDR
• Traditional antivirus programs are more simplistic and limited in
scope compared to the modern EDR systems. Antivirus can be perceived as
a part of the EDR system.
• Antivirus is generally a single program which serves basic purposes like
scanning, detecting and removing viruses and different types of malware.
• EDR security system, on the other hand, serves a much larger role. EDR not
only includes antivirus, but it also contains many security tools like
firewall, whitelisting tools, monitoring tools, etc. to provide comprehensive
protection against digital threats. It usually runs on the client-server model
and protects the various endpoints of an enterprise’s digital network and
keeps the endpoints secure.
Bypass AV/EDR
Concepts and Techniques
Bypass AV/EDR
• Bypassing an Antivirus or EDR is not a simple task, it requires some knowledge to
do so.
• 1. Know how the solutions work;
• 2. Know the operating system that the solution is installed on;
• 3. How the operating system and solution behave together;
• 4. Know the simplest Bypass techniques, involving simple attack vectors, even
more robust techniques with more advanced vectors;
• 5. Knowledge of programming is essential, be it high level as (Python, Go, Ruby
and C #), C and C ++ languages and the lowest level as assembly.
• 6. Windows API and Sysinternals Concept
•
Bypass AV/EDR - Mitre Att&ck
• Mitre Att&ck helps too much for you to get deeper into techniques to
bypass defense mechanisms, I recommend accessing the site and
exploring: https://attack.mitre.org/tactics/TA0005/
•
Bypass AV - Techniques (Obfuscation)
• Two common ways hackers mitigate antivirus detection are obfuscation and encryption.
• Obfuscation simply distorts the malware while keeping its form. A simple example would be
randomizing the case of the characters in a PowerShell script. The function is the same,
PowerShell doesn’t care about the case of the characters, but it may fool simple signature-
based scanning. In fact, Blackhills wrote about one well known example of obfuscation that
involves changing all references in the notorious memory tampering tool Mimikatz to
Mimidogz, along with changing a few other common strings. This simple obfuscation is
surprisingly effective, and LMG has used it on engagements to successfully bypass antivirus.
• As a proof of concept, the obfuscated “InvokeMimidogz” powershell script, with a few commo
n strings changed, was taken and obfuscated using the wonderfully powerful opensource tool,
InvokeObfuscation, written by Daniel Bohannon in 2016. This tool and the obfuscated powers
hell script have been around for several years and yet our team at LMG
Security regularly and successfully executes Invoke Mimikatz on hosts running antivirus solutio
ns like Kaspersky and Windows Defender.
•
Bypass AV/EDR - Techniques (C2 and Obfuscation)
• One of the methods I usually use is Trevor C2 + Pyfuscation, obfuscating the agent in
powershell using Pyfuscation I was successful in bypassing even EDR and AV like
Kaspersky Endpoint Security for Windows
•
• Now we are going to use pyfuscation to observe variables, strings and parameters
•
•
Bypass AV/EDR - Techniques
• Unhooking: unhooking is a technique working by replacing the ntdll.dll in memory with a fresh
copy from the filesystem
• Repatching: Repatching works by applying a counter patch to the patch previously applied by the
EDR
• Overload Mapping: Similar to the above. The payload stored in memory will be also backed by a
legitimate file on disk
• Syscall: This technique will map into memory only a specified function extracted from a target
DLL
Bypass AV/EDR - Techniques (Encryption)
• The second method is encryption. Encryption effectively eliminates the ability for
antivirus to detect malware through signature alone. Malware authors commonly use
‘crypters’ in order to encrypt their malicious payloads. Crypters encrypt a file and attach a
‘Stub’, a program which will decrypt the contents and then execute them.
• There are two types of crypters: ‘scantime’ and ‘runtime’.
• Scantime crypters are the most naïve and simply decrypt the payload, drop it onto the
disk and execute it.
• Runtime crypters use various process injection techniques to decrypt the malicious
payload and execute it in memory, never touching the disk.
•
Bypass AV/EDR - Win32 API
• Some malicious applications use internal
operating system APIs, being useful for creating
bypass techniques
• VirtualAlloc
• VirtualProtect
• WriteProcessMemory
• CreateRemoteThread
• There is also a hierarchy to the native APIs.
User applications will generally call “high-level”
APIs in kernel32 and user32 etc, and those APIs
will call “low-level” APIs in ntdll.
•
Bypass AV/EDR - API Unhooking
• To understand the unhooking technique, you must have a base understanding of what
“hooking” is. APIs (application programming interfaces) are the interface by which code is
used to make things happen on a computer system. Windows has a set of APIs (such as
syscall) that can be called to execute instructions that require direct system or kernel-
level access. As stated in the previous attack method, most EDR solutions use the
gateway ntdll.dll by “hooking” into it to watch for suspicious calls to memory.
• Unhooking refers to a method that attackers can use to load a fresh, unhooked version of
ntdll.dll AFTER Windows has already loaded the EDR-hooked version at process launch. At
this point the EDR is flying blind to any code that is running and it is unable to monitor
the return address for any API calls made, rendering it useless. A thorough hacker will go
so far as to “re-hook” the EDR at the end of his operation to cover their tracks. You can
read more about how unhooking works in this “red team” article about bypassing EDR to
dump credentials.
Bypass AV/EDR - Techniques (Full DLL Unhooking with C++)
• It's possible to completely unhook any given DLL loaded in memory, by reading the .text
section of ntdll.dll from disk and putting it on top of the .text section of the ntdll.dll that
is mapped in memory. This may help in evading some EDR solutions that rely on userland
API hooking.
• Below is a simplified graph, illustrating the core concept of the technique, where a
hooked .text section of ntdll.dll is replaced with a clean copy of .text section of ntdll.dll
from disk:
•
•
•
Bypass AV/EDR - Bypass LSA
• The Local Security Authority (LSA)
validates users credentials and
enforces security policies. The Local
Authority Subsystem Service (LSASS)
implements most of the LSA
functionality. Due to it’s importance
in maintaining the security of a
system, LSASS is often attacked to
gain access to credentials. In this
article, we’re going to be looking at
LSA protection mechanisms, and
how to bypass them.
• https://www.bordergate.co.uk/bypa
ssing-lsa-protections/
Bypass AV/EDR - Bypass LSA #2
•
To bypass LSA Protection you have a few options:
•
Remove the RunAsPPL registry key and reboot (probably
the worst method since you’ll lose any credentials in
memory)
•
Disable PPL flags on the LSASS process by patching the
EPROCESS kernel structure
•
Read the LSASS process memory contents directly instead
of using the open process functions
•
The latter 2 methods require the ability to read and write
kernel memory. The easiest method to achieve this will be
through loading a driver, although you can create your own
I’ve decided to leverage the RTCore64.sys driver from the
product MSI Afterburner. I chose this driver because it’s
signed and allows reading and writing arbitrary memory.
•
https://github.com/RedCursorSecurityConsulting/PPLKiller
Bypass AV/EDR - Indirect
Syscall
• With the increasing use of direct syscall as an evasion
technique against EDR API hooking, some detection
strategies such as "Mark of the Syscall" signature and
execution of syscall instruction originating from outside
of NTDLL were developed to identify abnormal syscall
usage in both static and dynamic perspective.
• Indirect syscall technique aims to replace the original
syscall instruction with a jump instruction pointing to a
memory address of NTDLL where it stores the syscall
instruction.For instance, the offset 0x12 of each NTDLL
API (i.e., NtAllocateVirtualMemory) will generally be
the syscall instruction as shown below:
Bypass AV/EDR - Indirect
Syscall #2
• To obtain the syscall address of each NTDLL API, we
could walk through the loaded NTDLL in the current
process to obtain the address of each NTDLL exported
functions and calculate the offset 0x12 and 0x0f
respectively to obtain address pointing to the
syscall/sysenter (syscall equivalent in 32-bit OS)
instruction.The original SharpWhispers had already did
the hard part to locate the export table directory and
the relative virtual address of each NTDLL API function.
My part will be trying to re-implement the similar
function as SysWhispers3 did in CSharp to obtain the
address of syscall instruction for each NTDLL APIs.
Bypass AV/EDR - Indirect
Syscall #3
•
Techniques:
•
Legacy Instruction (int 2Eh)
•
Series of Instructions
•
Random Instruction (nop)
•
Legacy Instruction
•
Wrote a C++ code which is doing process
injection using direct syscalls. And using
msfvenom generated shellcode with AES
encryption and injecting it into explorer.exe
using syscalls. I always use random names of
functions and variables to avoid static
detection.
Bypass AV/EDR - Techniques (Patching the patch)
• here were blog posts by @SpecialHoang and MDsec in the beginning of 2019 explaining
how to bypass AV/EDR software by patching the patch:
• https://medium.com/@fsx30/bypass-edrs-memory-protection-introduction-to-hooking-
2efb21acffd6
• https://www.mdsec.co.uk/2019/03/silencing-cylance-a-case-study-in-modern-edrs/
• If your implant or tool loads some functions from kernel32.dll or NTDLL.dll, a copy
of the library file is loaded into memory. The AV/EDR vendors typically patch some of the
functions from the in memory copy and place a JMP assembler instruction at the
beginning of the code to redirect the Windows API function to some inspecting code
from the AV/EDR software itself. So before calling the real Windows API function code, an
analysis is done. If this analysis results in no suspicious/malicious behaviour and returns a
clean result, the original Windows API function is called afterwards. If something
malicious is found, the Windows API call is blocked or the process will be killed
Bypass AV/EDR - Invoking Unmanaged Code
• In the example below, we use DInvoke_rs to dynamically call
RtlAdjustPrivilege in order to enable SeDebugPrivilege for the current
process token. This kind of execution will bypass any API hooks present
in Win32. Also, it won't create any entry on the final PE Import Address
Table, making it harder to detect the PE behaviour without executing it.
• Platform invoke is a service that enables managed code to call
unmanaged functions implemented in dynamic link libraries (DLLs),
such as those in the Windows API. It locates and invokes an exported
function and marshals its arguments (integers, strings, arrays,
structures, and so on) across the interoperation boundary as needed.
• This section introduces tasks associated with consuming unmanaged
DLL functions and provides more information about platform invoke. In
addition to the following tasks, there are general considerations and a
link providing additional information and examples.
Bypass AV/EDR - FUD Advanced Loader
• FUD advanced Loader implementing dynamic indirect
syscall with syscall number and syscall instruction
Unhooking with Halosgate technic. Shellcode in UUIDs
format to avoid static analysis, syscall instructions and
syscall number don't exist in the binary opcode which
makes it avoid static analysis and they get resolved at run
time. also it gets the API addresses from the PEB by offsets
and the comparison is done by hashing.
Bypass AV/EDR - Vectored
Syscall
•
It’s common to unhook any AV/EDRs hook in order to bypass them.
However to unhook the AV/EDRs hook we need to call a famous
Win32 API VirtualProtect which eventually ended up calling
NtVirtualProtectMemory inside ntdll.dll and that might also be
hooked by most of the AV/EDRs. Then there comes a technique
called  Direct Syscall to rescue us from this situation in which the
syscall doesn’t go through the ntdll module so the hooks placed in
the ntdll module are untouched during the syscall. However, syscalls
not originating from ntdll or other known modules are considered
suspicious. Direct syscalls can be detected using a technique called
hooking nirvana in which instrumentation callback is used.
•
Every-time the kernel returns to user mode, the RIP register is
checked to see if the address pointed by RIP is in a known module
address range, otherwise the syscall is crafted manually.
•
Due to the fact that RIP instruction is checked to detect manual
syscall, it can be bypassed by jumping indirectly to the ntdll address
space where the syscall instruction is located. However, we’re not
going to do that, instead we’ll leverage the VEH (Vectored Exception
Handler) to modify the context, especially RIP register to take us to
the syscall address.
Bypass AV/EDR - Techniques (Patching the patch)
•
• Both blog posts focus on bypassing the EDR-software CylancePROTECT and build a PoC
code for this specific software. By patching the additional JMP instruction from the
manipulated NTDLL.dll in memory, the analysis code of Cylance will never be executed
at all.
• One disadvantage for this technique is, that you may have to change the patch for every
different AV/EDR vendor. It is not very likely, that they all place an
additional JMP instruction in front of the same functions at the same point. They will
most likely hook different functions and maybe use another location for their patch.
•
Bypass AV/EDR - Techniques (AV Bypass with Metasploit
Templates and Custom Binaries)
• We can re-compile the payloads we use to insert our own shellcode, even modifying a
simple template. See an example I took from ired.team
• When generating metasploit payloads, our specified shellcode gets injected into the
template binaries. The payload we generated earlier got injected into the template for
which the source code is provided below
• If we make a couple of small changes to the code for memory allocation sizes:
•
•
•
• Re-compile and generate the payload using the newly compiled template with MSFVENOM
AV/EDR - Conclusion
• There are countless techniques for you to bypass AV / EDR, if I were to talk about
all of them, I would probably stay all day and not be able to explain even half,
because there are infinite possibilities;
• Attackers use these techniques + attack vectors to compromise their targets,
currently the most common is Phishing attacks to gain first access;
• I will leave some materials and courses for you who want to go deeper at the end
of this presentation;
•
AV/EDR - Studying
https://s3cur3th1ssh1t.github.io/
https://www.ired.team/offensive-security/defense-evasion/
https://attack.mitre.org/tactics/TA0005/
https://www.offensive-security.com/pen300-osep/
https://www.youtube.com/watch?v=mJZCNqcO10A&t=2s&ab_channel=RedTeamVillage (Fi
lipe Pires)
https://github.com/Techryptic/AV_Bypass
https://blog.f-secure.com/av-bypass-techniques-through-an-edr-lens/
https://www.youtube.com/watch?v=MO11gJ-WJqY&ab_channel=BlackHat (AVPASS: Leaking
and Bypassing Antivirus Detection Model Automatically)
https://www.youtube.com/watch?v=2HNuzUuVyv0&ab_channel=BlackHat (Red Team
Techniques for Evading, Bypassing & Disabling MS)
https://itm4n.github.io/bypassing-lsa-protection-userland/
https://www.netero1010-securitylab.com/evasion/indirect-syscall-in-csharp
AV/EDR - Studying
https://systemweakness.com/on-disk-detection-bypass-avs-edr-s-using-
syscalls-with-legacy-instruction-series-of-instructions-5c1f31d1af7d
https://learn.microsoft.com/en-us/dotnet/framework/interop/consuming-
unmanaged-dll-functions
https://research.nccgroup.com/2021/01/23/rift-analysing-a-lazarus-
shellcode-execution-method/
https://blog.sunggwanchoi.com/eng-uuid-shellcode-execution/
https://www.cyberwarfare.live/blog/vectored-syscall-poc
https://www.linkedin.com/in/saad-ahla/
AV/EDR - Tools
https://github.com/Ch0pin/AVIator
https://github.com/CBHue/PyFuscation
https://github.com/yeyintminthuhtut/Awesome-Red-Teaming#-defense-evasion
https://github.com/Veil-Framework/Veil-Evasion
https://www.shellterproject.com/
https://github.com/leechristensen/UnmanagedPowerShell
https://github.com/S3cur3Th1sSh1t/Amsi-Bypass-Powershell
https://github.com/danielbohannon/Invoke-Obfuscation
https://www.offensive-security.com/metasploit-unleashed/msfvenom/
https://www.ollydbg.de/
https://github.com/infosecn1nja/Red-Teaming-Toolkit (Repo Tools Red Team)
https://github.com/NVISOsecurity/brown-bags/tree/main/DInvoke%20to%20defeat%20EDRs
https://perspectiverisk.com/a-practical-guide-to-bypassing-userland-api-hooking/
https://github.com/D1rkMtr/FilelessRemotePE
AV/EDR - Tools
https://github.com/pwn1sher/uuid-loader
https://github.com/D1rkMtr/IORI_Loader
https://github.com/RedTeamOperations/VEH-PoC/
Thank you so much for the
opportunity
My LinkedIn
https://www.linkedin.com/in/joas-antonio-dos-santos
