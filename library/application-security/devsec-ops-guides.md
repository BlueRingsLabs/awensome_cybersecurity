---
id: ckb-8a55edc89e59
title: Devsec Ops Guides
category: application-security
format: book
language: en
tags: [compliance, devsecops, networking, owasp, privilege-escalation, risk-management]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.41
---

WWW.DEVSECOPSGUIDES.COM
HADESS
DevSecOps Guides
Comprehensive resource for integrating security into the software development
lifecycle.
Get started now
View it on GitHub
Welcome to DevSecOpsGuides, a comprehensive resource for developers, security professionals,
and operations teams who want to learn about the world of DevSecOps. DevSecOps is the
practice of integrating security into the entire software development lifecycle, from code creation
Simple Guide for Development and
Operation
to deployment and beyond. This approach ensures that security is a top priority at every stage of
the development process, leading to more secure and reliable applications.
Our guides cover a wide range of topics related to DevSecOps, including:
Our guides are written by experts in the field of DevSecOps, and are designed to be accessible to
developers, security professionals, and operations teams at all levels of experience. Whether you
are just getting started with DevSecOps or are looking to deepen your knowledge and skills,
DevSecOpsGuides is the perfect resource for you.
When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. Read more
about becoming a contributor in our GitHub repo.
Brought to you by:
Secure coding practices: Learn how to write code that is resistant to common security threats
such as SQL injection, cross-site scripting, and buffer overflow.
1
Threat modeling: Learn how to identify potential security vulnerabilities in your applications
and prioritize them based on their impact and likelihood of occurrence.
2
Security testing: Learn about different types of security testing, such as penetration testing,
vulnerability scanning, and code review, and how to incorporate them into your DevSecOps
workflow.
3
Infrastructure security: Learn about securing the infrastructure that supports your
applications, including servers, networks, and databases.
4
Compliance and regulations: Learn about compliance requirements and regulations such as
GDPR, HIPAA, and PCI-DSS, and how to ensure that your applications meet these standards.
5
Incident response: Learn how to respond to security incidents quickly and effectively,
minimizing the impact on your organization and customers.
6
Contributing
THANK YOU TO THE CONTRIBUTORS OF DEVSECOPS GUIDES!
HADESS
HADESS performs offensive cybersecurity services through infrastructures and software that
include vulnerability analysis, scenario attack planning, and implementation of custom integrated
preventive projects. We organized our activities around the prevention of corporate, industrial,
and laboratory cyber threats.
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Plan & Develop / AppSec
Application security (AppSec) threats refer to the security risks and vulnerabilities that can be
present in the software applications used by organizations. These threats can arise from various
sources, such as software bugs, coding errors, design flaws, and inadequate security controls.
AppSec threats can lead to data breaches, information theft, financial losses, reputational
damage, and legal liabilities for organizations.
To address AppSec threats, various standards and frameworks have been developed. Here are
some of the most important ones:
AppSec
OWASP Top Ten: The Open Web Application Security Project (OWASP) Top Ten is a list of the
most critical security risks to web applications. It is widely used by organizations as a guideline
for identifying and addressing AppSec threats.
1
PCI DSS: The Payment Card Industry Data Security Standard (PCI DSS) is a set of security
standards designed to protect credit card data. It requires merchants and service providers to
implement various security controls to prevent unauthorized access to cardholder data.
2
ISO 27001: The International Organization for Standardization (ISO) 27001 is a standard for
information security management systems. It provides a framework for implementing controls
and processes to protect sensitive information, including software applications.
3
NIST Cybersecurity Framework: The National Institute of Standards and Technology (NIST)
Cybersecurity Framework is a set of guidelines for managing and reducing cybersecurity risks.
It provides a framework for organizations to identify, protect, detect, respond to, and recover
from security incidents.
4
BSIMM: The Building Security In Maturity Model (BSIMM) is a software security framework that
provides a measurement of an organization’s software security program maturity. It identifies
best practices and benchmarks for implementing a successful software security program.
5
CSA: The Cloud Security Alliance (CSA) provides guidance for secure cloud computing. Its
Cloud Controls Matrix provides a framework for organizations to assess the security of cloud
6
Cheatsheet with rules/policies for preventing OWASP Top 10 vulnerabilities
Type
Vulnerability
Rule/Policy
A1: Injection
SQL Injection
Use prepared statements and parameterized
queries. Sanitize input and validate parameters.
A1: Injection
NoSQL Injection
Use parameterized queries with built-in
protections. Sanitize input and validate
parameters.
A1: Injection
LDAP Injection
Use parameterized queries and escape special
characters.
A1: Injection
Command Injection
Use safe APIs or libraries that do not allow
arbitrary command execution. Sanitize input and
validate parameters.
A2: Broken
Authentication and
Session Management
Weak Passwords
Enforce strong password policies, including
complexity requirements and regular password
changes. Use multi-factor authentication.
A2: Broken
Authentication and
Session Management
Session Fixation
Regenerate session ID upon login and logout.
Use secure cookies with HttpOnly and Secure
flags.
A3: Cross-Site Scripting
(XSS)
Reflected XSS
Sanitize all user input, especially from untrusted
sources such as URLs, forms, and cookies. Use
output encoding to prevent XSS attacks.
A3: Cross-Site Scripting
(XSS)
Stored XSS
Filter user-generated content to prevent
malicious scripts from being stored. Use output
encoding to prevent XSS attacks.
A4: Broken Access
Control
Insecure Direct Object
Reference (IDOR)
Implement proper access controls and
authorization checks to prevent direct object
service providers.
CWE/SANS Top 25: A list of the top 25 most dangerous software errors, as identified by the
Common Weakness Enumeration (CWE) and the SANS Institute.
7
NIST Cybersecurity Framework: A framework developed by the National Institute of Standards
and Technology (NIST) to help organizations manage and reduce cybersecurity risk.
8
Type
Vulnerability
Rule/Policy
reference attacks.
A5: Security
Misconfiguration
Improper Error
Handling
Do not reveal sensitive information in error
messages or logs. Use custom error pages.
A6: Insecure
Cryptographic Storage
Weak Cryptography
Use strong, up-to-date encryption algorithms
and keys. Implement proper key management
and storage practices.
A7: Insufficient
Transport Layer
Protection
Unencrypted
Communications
Use HTTPS with secure protocols and strong
encryption. Disable insecure protocols such as
SSLv2 and SSLv3.
A8: Insecure
Deserialization
Insecure
Deserialization
Validate and verify the integrity of serialized
objects. Avoid accepting serialized objects from
untrusted sources.
A9: Using Components
with Known
Vulnerabilities
Outdated Software
Keep all software and libraries up-to-date with
the latest security patches. Monitor for
vulnerabilities and apply patches as soon as
possible.
A10: Insufficient
Logging and Monitoring
Lack of Monitoring
Implement robust logging and monitoring
practices to detect and respond to security
events. Use SIEM tools and alerting systems.
Damage potential: How much damage could be caused if the vulnerability is exploited?
Reproducibility: How easy is it to reproduce the vulnerability?
Exploitability: How easy is it to actually exploit the vulnerability?
Affected users: How many users or systems are affected by the vulnerability?
DREAD:
•
•
•
•
Discoverability: How easy is it for an attacker to discover the vulnerability?
By evaluating each of these factors, organizations can assign a score to a particular vulnerability
and use that score to determine which vulnerabilities pose the greatest risk and should be
addressed first.
Core security training
Requirements:
Establish security requirements
Create quality gates/bug bars
Perform security and privacy risk assessments
Establish design requirements
Perform attack surface analysis reduction
Use threat modeling
Use approved tools
Deprecate unsafe functions
Perform static analysis
Perform dynamic analysis
Perform fuzz testing
Conduct attack surface review
Create an incident response plan
Conduct final security review
Certify, release, and archive
•
SDL (Security Development Lifecycle)
Training:
•
•
•
•
•
Design:
•
•
•
Implementation:
•
•
•
Verification:
•
•
•
Release:
•
•
•
OWASP SAMM categorizes security practices into four key business
Strategy and metrics
Policy and compliance
Education and guidance
Threat assessment
Security requirements
Secure architecture
Design review
Implementation review
Security testing
Issue management
Environment Hardening
Operational enablement
Copyright © 2019-2023 HADESS.
Response:
Execute incident response plan
1
OWASP SAMM
Governance:
•
•
•
Construction:
•
•
•
Verification:
•
•
•
Operations:
•
•
•
DevSecOps Guides
Plan & Develop / Driver
DevSecOps is a methodology that seeks to integrate security into the software development
lifecycle, rather than treating it as a separate process that is bolted on at the end. The goal is to
build secure, reliable software that meets the needs of the business, while also protecting
sensitive data and critical infrastructure. There are several drivers and challenges associated with
implementing DevSecOps, which are outlined below.
Drivers:
Challenges:
Driver
Security concerns: With the increasing frequency and severity of cyberattacks, security has
become a top priority for organizations. DevSecOps provides a way to build security into the
software development process, rather than relying on ad hoc security measures.
1
Compliance requirements: Many organizations are subject to regulatory requirements such as
PCI-DSS, HIPAA, and GDPR. DevSecOps can help ensure compliance with these regulations
by integrating security into the development process and providing visibility into the security
posture of the application.
2
Agility and speed: DevSecOps can help organizations develop and deploy software more
quickly and with greater agility. By integrating security into the development process,
organizations can reduce the time and cost of remediation and avoid delays caused by
security issues.
3
Collaboration: DevSecOps encourages collaboration between developers, security teams, and
operations teams. By working together, these teams can build more secure and reliable
software.
4
Cultural barriers: DevSecOps requires a cultural shift in the organization, with developers,
security teams, and operations teams working together in a collaborative manner. This can be
challenging, particularly in organizations with a siloed culture.
1
Authentication, Session Management, Access Control, Malicious Input handling, Output
encoding/escaping, Cryptography, Error handling and logging , Data Protection, Communication
Security, Http Security configuration, Security configuration, Malicious, Internal Security, Business
logic, Files and resources, Mobile, Web services
Security compliance checklist
Security requirement checklist (OWASP ASVS)
Top 10 security design issues
Security issues in the previous release
Customer or marketing feedback on security issues
Secure coding
Selection of reliable and secure third-party components
Secure configuration
A third-party software evaluation checklist:
Recommended third-party software and usage by projects:
CVE status of third-party components:
Lack of skills: DevSecOps requires a range of skills, including development, security, and
operations. Finding individuals with these skills can be difficult, particularly in a competitive job
market.
2
Tooling and automation: DevSecOps relies heavily on tooling and automation to integrate
security into the development process. Implementing and maintaining these tools can be
challenging, particularly for smaller organizations with limited resources.
3
Complexity: DevSecOps can be complex, particularly for organizations with large, complex
applications. It can be difficult to integrate security into the development process without
causing delays or creating additional complexity.
4
Application Security Verification Standard(ASVS):
Design review
•
•
•
•
•
Implementation review
•
•
•
Third-party components
•
•
•
Code Review
Static Application Security Testing (SAST)->FindSecbugs, Fortify, Coverity, klocwork.
Dynamic Application Security Testing (DAST)->OWASP ZAP, BurpSuite
Interactive Application Security Testing (IAST)->CheckMarks Varacode
Run-time Application Security Protection(RASP)->OpenRASP
https://www.owasp.org/index.php/Category:OWASP _Code_Review_Project SEI CERT Coding
https://wiki.sei.cmu.edu/confluence/display/seccode/SEI+CERT+Coding+Standards
Software Assurance Marketplace (SWAMP): https://www.mir-swamp.org/
Secure configuration baseline
Constant monitoring mechanism
Copyright © 2019-2023 HADESS.
•
•
•
•
•
•
Environment Hardening
•
•
Constant monitoring mechanism
Common vulnerabilities and exposures (CVEs) OpenVAS, NMAP
1
Integrity monitoring OSSEC
2
Secure configuration compliance OpenSCAP
3
Sensitive information exposure No specific open source tool in this area. However, we may
define specific regular expression patterns
4
DevSecOps Guides
Plan & Develop / Methodology
DevSecOps methodology is an approach to software development that integrates security
practices into the software development process from the beginning. The goal of DevSecOps is to
make security an integral part of the software development process, rather than an afterthought.
Some common methodologies used in DevSecOps include:
Methodology
Agile: Agile methodology focuses on iterative development and continuous delivery, with an
emphasis on collaboration and communication between developers and other stakeholders. In
DevSecOps, Agile is often used to facilitate a continuous feedback loop between developers
and security teams, allowing security issues to be identified and addressed early in the
development process.
1
Waterfall: Waterfall methodology is a traditional software development approach that involves
a linear progression of steps, with each step building on the previous one. In DevSecOps,
Waterfall can be used to ensure that security requirements are defined and addressed early in
the development process, before moving on to later stages of development.
2
DevOps: DevOps methodology focuses on collaboration and automation between developers
and IT operations teams. In DevSecOps, DevOps can be used to automate security testing and
other security-related tasks, allowing security issues to be identified and addressed more
quickly and efficiently.
3
Shift-Left: Shift-Left methodology involves moving security testing and other security-related
tasks earlier in the development process, to catch and address security issues earlier. In
DevSecOps, Shift-Left can be used to ensure that security is integrated into the development
process from the very beginning.
4
Threat Modeling: Threat modeling is a methodology that involves identifying and analyzing
potential threats to a software application, and then designing security controls to mitigate
those threats. In DevSecOps, threat modeling can be used to identify and address potential
5
These are just a few examples of the methodologies that can be used in DevSecOps. The key is to
integrate security practices into the development process from the beginning, and to use a
continuous feedback loop to identify and address security issues as early as possible.
DoD Methodology in DevSecOps refers to the specific methodology and framework that the US
Department of Defense (DoD) follows to implement DevSecOps practices in its software
development lifecycle. The DoD has created its own set of guidelines and best practices for
DevSecOps that align with its specific security requirements and regulations.
The DoD Methodology for DevSecOps is based on the following principles:
security issues early in the development process, before they become more difficult and
expensive to address.
DoD
Continuous Integration/Continuous Delivery (CI/CD) pipeline: The CI/CD pipeline is an
automated process for building, testing, and deploying software changes. The DoD
Methodology emphasizes the importance of automating the pipeline to speed up the delivery
process and ensure that all changes are tested thoroughly before they are deployed.
1
Security testing: The DoD Methodology requires that security testing is integrated throughout
the entire software development lifecycle. This includes static code analysis, dynamic
2
Overall, the DoD Methodology for DevSecOps is designed to help the Department of Defense
build secure, reliable, and resilient software systems that meet its unique security requirements
and regulations.
Microsoft has its own approach to DevSecOps, which is known as the Microsoft Secure
Development Lifecycle (SDL). The SDL is a comprehensive methodology that integrates security
practices and tools throughout the entire software development process, from planning and
design to testing and release.
The key principles of the Microsoft SDL are:
application security testing (DAST), and penetration testing.
Infrastructure as Code (IaC): The DoD Methodology promotes the use of IaC to automate the
deployment and management of infrastructure. This approach ensures that infrastructure is
consistent and repeatable, which helps to reduce the risk of misconfigurations and security
vulnerabilities.
3
Risk management: The DoD Methodology requires that risk management is an integral part of
the DevSecOps process. This involves identifying potential risks and vulnerabilities, prioritizing
them based on their severity, and taking appropriate measures to mitigate them.
4
Collaboration: The DoD Methodology emphasizes the importance of collaboration between
development, security, and operations teams. This includes regular communication, joint
planning, and cross-functional training to ensure that all team members have a common
understanding of the DevSecOps process.
5
Microsoft
The Microsoft SDL includes specific practices and tools for each stage of the development
process, such as threat modeling, code analysis, security testing, and incident response.
Microsoft also provides guidance and training for developers, operations teams, and security
professionals on how to implement the SDL in their organizations.
1- Security training: Security awareness, Security certification program, Case study knowledge
base, Top common issue, Penetration learning environment OWASP top 10, CWE top 25, OWASP
VWAD
2- Security maturity assessment Microsoft SDL, OWASP SAMM self-assessment for maturity level
Microsoft SDL, OWASP SAMM
3- Secure design Threat modeling templates (risks/mitigation knowledge base), Security
requirements for release gate, Security design case study, Privacy protection OWASP ASVS, NIST,
Privacy risk assessment
4- Secure coding Coding guidelines (C++, Java, Python, PHP, Shell, Mobile), Secure coding
scanning tools, Common secure coding case study CWE, Secure coding, CERT OWASP
5- Security testing Secure compiling options such as Stack Canary, NX, Fortify Source, PIE, and
RELRO, Security testing plans, Security testing cases, Known CVE testing, Known secure coding
issues, API-level security testing tools, Automation testing tools, Fuzz testing, Mobile testing,
Exploitation and penetration, Security compliance Kali Linux tools, CIS
Security by design: Security is considered from the beginning of the development process,
and is integrated into the design of the application.
1
Continuous improvement: The SDL is an iterative process, with continuous improvement of
security practices and tools based on feedback and lessons learned.
2
Risk management: Risks are identified and evaluated at each stage of the development
process, and appropriate measures are taken to mitigate them.
3
Collaboration: Security is a shared responsibility, and collaboration between development,
operations, and security teams is essential.
4
Automation: Automated tools and processes are used to ensure consistency and efficiency in
security practices.
5
Security guidelines and processes
6- Secure deployment Configuration checklist, Hardening guide, Communication ports/protocols,
Code signing CIS Benchmarks, CVE
7- Incident and vulnerability handling Root cause analysis templates, Incident handling process
and organization NIST SP800-61
8- Security training Security awareness by email, Case study newsletter, Toolkit usage hands-on
training, Security certificate and exam NIST 800- 50, NIST 800- 16, SAFECode security
engineering training
Leverage third-party cloud service provider security mechanisms (for example, AWS provides
IAM, KMS, security groups, WAF, Inspector, CloudWatch, and Config)
Secure configuration replies on external tools such as AWS Config and Inspector
Service or operation monitoring may apply to AWS Config, Inspector, CloudWatch, WAF, and
AWS shield
Stage 2 – building a security testing team
Vulnerability assessment: NMAP, OpenVAS
Static security analysis: FindBugs for Java, Brakeman for Ruby on Rails, Infer for Java, C++,
Objective C and C
Web security: OWASP dependency check, OWASP ZAP, Archni-Scanner, Burp Suite, SQLMap,
w3af
Communication: Nmap, NCAT, Wireshark, SSLScan, sslyze
Infrastructure security: OpenSCAP, InSpec
VM Toolset: Pentest Box for Windows, Kali Linux, Mobile Security Testing Framework
Security monitoring: ELK, MISP—Open source Threat Intelligence Platform, OSSCE—Open source
HIDS Security, Facebook/osquery—performant endpoint visibility, AlienValut OSSIM—opensource
SIEM
Stage 3 – SDL activities
Security shifts to the left and involves every stakeholder
Architect and design review is required to do threat modeling
Stage 1 – basic security control
•
•
•
•
•
Developers get secure design and secure coding training
Operation and development teams are as a closed-loop collaboration
Adoption of industry best practices such as OWASP SAMM and Microsoft SDL for security
maturity assessment
Stage 4 – self-build security services
Take Salesforce as an example—the Salesforce Developer Center portal provides security training
modules, coding, implementation guidelines, tools such as assessment tools, code scanning,
testing or CAPTCHA modules, and also a developer forum. Whether you are building an
application on top of salesforce or not, the Salesforce Developer Center is still a good reference
not only for security knowledge but also for some open source tools you may consider applying.
Stage 5 – big data security analysis and automation
Key characteristics at this stage are:
Fully or mostly automated security testing through the whole development cycle
Applying big data analysis and machine learning to identify abnormal behavior or unknown
threats
wProactive security action is taken automatically for security events, for example, the
deployment of WAF rules or the deployment of a virtual patch
Typical open source technical components in big data analysis frameworks include the following:
Flume, Log Logstash, and Rsyslog for log collection
Kafka, Storm, or Spark for log analysis
Redis, MySQL, HBase, and HDFS for data storage
Kibana, ElasticSearch, and Graylog for data indexing, searching, and presentation
The key stages in big data security analysis are explained in the table:
Data collection:
Collects logs from various kinds of sources and systems such as firewalls, web services, Linux,
networking gateways, endpoints, and so on.
Data normalization:
Sanitizes or transforms data formats into JSON, especially, for critical information such as IP,
hostname, email, port, and MAC.
•
•
•
•
•
•
•
•
•
•
Data enrich/label:
In terms of IP address data, it will further be associated with GeoIP and WhoIS information.
Furthermore, it may also be labeled if it’s a known black IP address.
Correlation:
The correlation analyzes the relationship between some key characteristics such as IP, hostname,
DNS domain, file hash, email address, and threat knowledge bases.
Storage:
There are different kinds of data that will be stored —the raw data from the source, the data with
enriched information, the results of correlation, GeoIP mapping, and the threat knowledge base.
Alerts:
Trigger alerts if threats were identified or based on specified alerting rules.
Presentation/query:
Security dashboards for motoring and queries. ElasticSearch, RESTful API, or third-party SIEM.
1- Security office under a CTO
Role of a security team in an organization
No dedicated Chief Security Officer (CSO)
The security team may not be big—for example, under 10 members
The security engineering team serves all projects based on their needs
The key responsibility of the security engineering team is to provide security guidelines,
policies, checklists, templates, or training for all project teams
It’s possible the security engineering team members may be allocated to a different project to
be subject matter experts based on the project’s needs
Security engineering provides the guidelines, toolkits, and training, but it’s the project team
that takes on the main responsibility for daily security activity execution
2-Dedicated security team
•
•
•
•
•
•
Security management: The team defines the security guidelines, process, policies,
templates, checklist, and requirements. The role of the security management team is the same
as the one previously discussed in the Security office under a CTO section.
Security testing: The team is performing in-house security testing before application release.
Security engineering: The team provides a common security framework, architecture, SDK,
and API for a development team to use
Security monitoring: This is the security operation team, who monitor the security status for
all online services.
Security services: This is the team that develops security services such as WAF and intrusion
deference services.
3- Security technical committee (taskforce)
•
•
•
•
•
The secure design taskforce will have a weekly meeting with all security representatives—from all
project teams— and security experts from the security team to discuss the following topics (not
an exhaustive list):
Common secure design issues and mitigation (initiated by security team)
Secure design patterns for a project to follow (initiated by security team)
Secure design framework suggestions for projects (initiated by security team) Specific secure
design issues raised by one project and looking for advice on other projects (initiated by
project team)
Secure design review assessment for one project (initiated by project team)
Copyright © 2019-2023 HADESS.
•
•
•
•
DevSecOps Guides
Plan & Develop / Threats
Threats
TABLE OF CONTENTS
Threat Modeling
1
Implementation
a
Threat Matrix
b
Tools
c
Threats
2
Weak or stolen credentials
a
Insecure authentication protocols
b
Insufficient access controls
c
Improper privilege escalation
d
Data leakage or unauthorized access
e
Insecure data storage
f
Inadequate network segmentation
g
Man-in-the-Middle attacks
h
Resource exhaustion
i
Distributed DoS (DDoS) attacks
j
Misconfigured security settings
k
Insecure default configurations
l
Delayed patching of software
m
Lack of vulnerability scanning
n
Malicious or negligent insiders
o
Unauthorized data access or theft
p
Unauthorized physical access
q
Theft or destruction of hardware
r
Vulnerabilities in third-party components
s
Threat modeling is a process that helps identify and prioritize potential security threats to a
system or application. The goal of threat modeling is to identify security risks early in the
development process and proactively mitigate them, rather than waiting for vulnerabilities to be
discovered after deployment.
One popular method for conducting threat modeling is called STRIDE, which stands for Spoofing,
Tampering, Repudiation, Information disclosure, Denial of service, and Elevation of privilege.
These are the six types of security threats that can affect a system, and by considering each of
them in turn, a threat model can help identify potential vulnerabilities and attacks.
The STRIDE methodology is often used in combination with a diagram designer tool, such as
Microsoft’s Threat Modeling Tool or the open-source OWASP Threat Dragon. These tools allow
you to create a visual representation of the system or application you are analyzing, and to map
out potential threats and attack vectors.
Explains the six types of security threats in the STRIDE methodology:
Lack of oversight on third-party activities
t
Threat detection
3
Indicators of compromises
4
External source client IP
a
Client fingerprint (OS, browser, user agent, devices, and so on)
b
Web site reputation
c
Random Domain Name by Domain Generation Algorithms (DGAs)
d
Suspicious file downloads
e
DNS query
f
Threat Modeling
STRIDE Threat
Description
Spoofing
Impersonating a user, device, or system in order to gain unauthorized access or
perform malicious actions. Examples include phishing attacks or using a fake SSL
certificate to intercept data.
Tampering
Modifying data or code in transit or at rest, in order to introduce errors, gain
unauthorized access, or perform other malicious actions. Examples include
modifying the source code of an application or altering data in a database.
Repudiation
Denying or disavowing actions or events, in order to evade accountability or
responsibility. Examples include denying that an action was taken, or that data was
accessed.
Information
Disclosure
Revealing confidential or sensitive information to unauthorized parties, whether
intentionally or accidentally. Examples include disclosing passwords or user data, or
exposing private keys.
Denial of
Service
Disrupting or degrading the availability or functionality of a system or application,
through network attacks, resource exhaustion, or other means. Examples include
Distributed Denial of Service (DDoS) attacks or flooding a server with requests.
Elevation of
Privilege
Gaining additional access or privileges beyond those that were initially granted, in
order to perform unauthorized actions or escalate an attack. Examples include
exploiting a software vulnerability to gain administrative access or using a social
engineering technique to obtain sensitive information.
Step 1: Define the Scope
Identify the application or system within the DevSecOps pipeline that you want to perform threat
modeling for. For example, let’s consider a microservices-based application deployed using
containerization and managed by Kubernetes.
Step 2: Gather Information
Gather information about the application’s architecture, design, and deployment. This includes
understanding the components, their interactions, data flows, and external dependencies.
Step 3: Identify Threats and Assets
Identify the critical assets and sensitive data involved in the application. Consider both internal
and external threats that could compromise the security of these assets. For example:
Implementation
Unauthorized access to customer data stored in a database Injection attacks on APIs or
containers Misconfiguration of Kubernetes resources leading to unauthorized access or privilege
escalation
Step 4: Assess Vulnerabilities and Risks
Evaluate the architecture and design to identify potential vulnerabilities and risks associated with
the identified threats. Consider the security implications at each stage of the DevSecOps pipeline,
including development, testing, deployment, and operations. For example: Insecure container
images containing known vulnerabilities Lack of proper access controls on Kubernetes resources
Weak or outdated authentication mechanisms
Step 5: Prioritize and Mitigate Risks
Prioritize the risks based on their potential impact and likelihood of occurrence. Develop
mitigation strategies and recommendations to address each identified risk. Consider integrating
security controls and best practices into the DevSecOps pipeline. For example: Implementing
automated vulnerability scanning and patch management for container images Applying secure
configuration practices for Kubernetes resources Enforcing strong authentication and access
controls at all stages of the pipeline
Step 6: Continuously Monitor and Improve
Incorporate threat modeling as an iterative process within the DevSecOps lifecycle. Regularly
review and update the threat model as the application evolves or new risks emerge. Continuously
monitor the system for potential threats and vulnerabilities.
Real-case Example:
In a DevSecOps context, consider a scenario where a development team is building a cloud-native
application using microservices architecture and deploying it on a container platform. The threat
modeling process could involve identifying risks such as:
Insecure container images with vulnerabilities
Weak authentication and authorization mechanisms
Inadequate logging and monitoring for containerized applications
Misconfiguration of cloud resources and access controls
Insecure communication between microservices
Injection attacks on API endpoints
Based on the identified risks, mitigation strategies could include:
•
•
•
•
•
•
Implementing automated vulnerability scanning and image hardening for containers
Applying strong authentication and authorization mechanisms, such as OAuth or JWT tokens
Incorporating centralized logging and monitoring solutions for containerized applications
Establishing proper cloud resource management and access control policies
Encrypting communication channels between microservices
Implementing input validation and security controls to prevent injection attacks
This matrix provides a starting point for identifying potential threats and corresponding
mitigations based on different categories.
Threat Category
Threat Description
Potential Mitigation
Authentication
Weak or stolen
credentials
Implement strong password policies, multi-factor
authentication, and password hashing algorithms.
Authentication
Insecure authentication
protocols
Use secure authentication protocols (e.g., TLS) and
avoid transmitting credentials in plaintext.
Authorization
Insufficient access
controls
Implement RBAC (Role-Based Access Control) and
apply the principle of least privilege.
Authorization
Improper privilege
escalation
Limit privilege escalation capabilities and regularly
review user permissions.
Data Protection
Data leakage or
unauthorized access
Encrypt sensitive data at rest and in transit, and
implement proper access controls.
Data Protection
Insecure data storage
Follow secure coding practices for data storage,
including encryption and secure key management.
Network Security
Inadequate network
segmentation
Implement proper network segmentation using
firewalls or network policies.
Network Security
Man-in-the-Middle
attacks
Use encryption and certificate-based
authentication for secure communication.
Denial-of-Service
(DoS)
Resource exhaustion
Implement rate limiting, request validation, and
monitoring for abnormal behavior.
Denial-of-Service
(DoS)
Distributed DoS (DDoS)
attacks
Employ DDoS mitigation techniques, such as traffic
filtering and load balancing.
•
•
•
•
•
•
Threat Matrix
Threat Category
Threat Description
Potential Mitigation
System
Configuration
Misconfigured security
settings
Apply secure configuration guidelines for all system
components.
System
Configuration
Insecure default
configurations
Change default settings and remove or disable
unnecessary services.
Vulnerability
Management
Delayed patching of
software
Establish a vulnerability management program with
regular patching and updates.
Vulnerability
Management
Lack of vulnerability
scanning
Conduct regular vulnerability scans and prioritize
remediation.
Insider Threats
Malicious or negligent
insiders
Implement proper access controls, monitoring, and
employee training programs.
Insider Threats
Unauthorized data access
or theft
Monitor and log user activities and implement data
loss prevention mechanisms.
Physical Security
Unauthorized physical
access
Secure physical access to data centers, server
rooms, and hardware components.
Physical Security
Theft or destruction of
hardware
Implement physical security controls, such as locks,
surveillance systems, and backups.
Third-Party
Dependencies
Vulnerabilities in third-
party components
Perform due diligence on third-party components,
apply patches, and monitor security advisories.
Third-Party
Dependencies
Lack of oversight on
third-party activities
Establish strong vendor management practices,
including audits and security assessments.
Threat Category
Threat Description
Microsoft Threat
Modeling Tool
A free tool from Microsoft that helps in creating threat models for software
systems. It provides a structured approach to identify, analyze, and mitigate
potential threats.
OWASP Threat Dragon
An open-source threat modeling tool that enables the creation of threat models
using the STRIDE methodology. It provides an intuitive interface and supports
Tools
Threat Category
Threat Description
collaboration among team members.
PyTM
An open-source threat modeling tool specifically designed for web applications.
It allows the modeling of various aspects of an application’s architecture and
helps in identifying potential threats.
ThreatModeler
A commercial tool that offers a comprehensive platform for threat modeling. It
provides a visual modeling interface, automated threat analysis, and integration
with other security tools and frameworks.
IriusRisK
A commercial tool that combines threat modeling with risk management. It
supports multiple threat modeling methodologies, provides risk assessment
capabilities, and offers integration with other tools and platforms.
TMT (Threat
Modeling Tool)
An open-source command-line tool developed by OWASP for threat modeling. It
supports the STRIDE methodology and allows for the automation of threat
modeling processes.
Secure Code Warrior
While not a traditional threat modeling tool, it offers interactive training modules
and challenges that can help developers understand and identify potential
threats during the development process.
This code creates a threat model using PyTM and represents the “Weak or Stolen Credentials”
threat scenario. It includes actors such as “Attacker” and “Insider,” a server representing the
application server, and a datastore representing the user’s data.
The threat model defines the “Weak or Stolen Credentials” threat and includes attack paths such
as “Password Guessing/Brute Force Attack,” “Credential Theft,” and “Insider Threat.” It also
defines the impact of these threats, such as unauthorized access to user data and data breaches.
The code generates a threat model diagram in PNG format, named
“weak_or_stolen_credentials_threat_model.png.”
Threats
Weak or stolen credentials
from pytm import TM, Server, Datastore, Actor
This code creates a threat model using PyTM and represents the “Insecure Authentication
Protocols” threat scenario. It includes actors such as “Attacker” and “User,” a server representing
the application server, and a datastore representing the user’s data.
The threat model defines the “Insecure Authentication Protocols” threat and includes attack paths
such as “Eavesdropping” and “Man-in-the-Middle Attack.” It also defines the impact of these
threats, such as unauthorized access to user data and data breaches.
# Create a new threat model
tm = TM("Weak or Stolen Credentials Threat Model")
# Create actors
attacker = Actor("Attacker")
insider = Actor("Insider")
# Create server and datastore
server = Server("Application Server")
datastore = Datastore("User Datastore")
# Define weak or stolen credentials threat
tm.add_threat()
tm.threat.name("Weak or Stolen Credentials")
tm.threat.description("Threat of weak or stolen user credentials")
# Define attack paths
tm.attack_path(attacker, server, "Password Guessing/Brute Force Attack")
tm.attack_path(attacker, server, "Credential Theft")
tm.attack_path(insider, server, "Insider Threat")
# Define impact
tm.data_flow(server, datastore, "Unauthorized Access to User Data")
tm.data_flow(server, datastore, "Data Breach and Exposure of Sensitive Information")
# Generate the threat model diagram
tm.generate_diagram("weak_or_stolen_credentials_threat_model.png")
Insecure authentication protocols
The code generates a threat model diagram in PNG format, named
“insecure_authentication_protocols_threat_model.png.”
This code creates a threat model using PyTM and represents the “Insufficient Access Controls”
threat scenario. It includes actors such as “Attacker” and “User,” a server representing the
application server, and a datastore representing the sensitive data.
from pytm import TM, Server, Datastore, Actor
# Create a new threat model
tm = TM("Insecure Authentication Protocols Threat Model")
# Create actors
attacker = Actor("Attacker")
user = Actor("User")
# Create server and datastore
server = Server("Application Server")
datastore = Datastore("User Datastore")
# Define insecure authentication protocols threat
tm.add_threat()
tm.threat.name("Insecure Authentication Protocols")
tm.threat.description("Threat of using insecure authentication protocols")
# Define attack paths
tm.attack_path(attacker, server, "Eavesdropping")
tm.attack_path(attacker, server, "Man-in-the-Middle Attack")
# Define impact
tm.data_flow(server, datastore, "Unauthorized Access to User Data")
tm.data_flow(server, datastore, "Data Breach and Exposure of Sensitive Information")
# Generate the threat model diagram
tm.generate_diagram("insecure_authentication_protocols_threat_model.png")
Insufficient access controls
The threat model defines the “Insufficient Access Controls” threat and includes attack paths such
as “Unauthorized Access” by the attacker and “Privilege Escalation” by the user. It also defines
the impact of these threats, such as unauthorized access to sensitive data and data leakage.
The code generates a threat model diagram in PNG format, named
“insufficient_access_controls_threat_model.png.”
from pytm import TM, Actor, Server, Datastore
# Create a new threat model
tm = TM("Insufficient Access Controls Threat Model")
# Create actors
attacker = Actor("Attacker")
user = Actor("User")
# Create server and datastore
server = Server("Application Server")
datastore = Datastore("Sensitive Datastore")
# Define insufficient access controls threat
tm.add_threat()
tm.threat.name("Insufficient Access Controls")
tm.threat.description("Threat of insufficient access controls on sensitive data")
# Define attack paths
tm.attack_path(attacker, server, "Unauthorized Access")
tm.attack_path(user, server, "Privilege Escalation")
# Define impact
tm.data_flow(server, datastore, "Unauthorized Access to Sensitive Data")
tm.data_flow(server, datastore, "Data Leakage")
# Generate the threat model diagram
tm.generate_diagram("insufficient_access_controls_threat_model.png")
Improper privilege escalation
This code creates a threat model using PyTM and represents the “Improper Privilege Escalation”
threat scenario. It includes actors such as “Attacker” and “User” and a server representing the
application server.
The threat model defines the “Improper Privilege Escalation” threat and includes attack paths
such as “Exploiting Vulnerability” by the attacker and “Abusing User Privileges” by the user.
The code generates a threat model diagram in PNG format, named
“improper_privilege_escalation_threat_model.png.”
This code creates a threat model using PyTM and represents the “Data Leakage or Unauthorized
Access” threat scenario. It includes actors such as “Attacker” and “User” and a datastore
representing sensitive data.
from pytm import TM, Actor, Server
# Create a new threat model
tm = TM("Improper Privilege Escalation Threat Model")
# Create actors
attacker = Actor("Attacker")
user = Actor("User")
# Create server
server = Server("Application Server")
# Define improper privilege escalation threat
tm.add_threat()
tm.threat.name("Improper Privilege Escalation")
tm.threat.description("Threat of improper privilege escalation in the application")
# Define attack paths
tm.attack_path(attacker, server, "Exploiting Vulnerability")
tm.attack_path(user, server, "Abusing User Privileges")
# Generate the threat model diagram
tm.generate_diagram("improper_privilege_escalation_threat_model.png")
Data leakage or unauthorized access
The threat model defines the “Data Leakage or Unauthorized Access” threat and includes attack
paths such as “Exploiting Vulnerability” by the attacker and “Unauthorized Access” by the user.
The code generates a threat model diagram in PNG format, named
“data_leakage_unauthorized_access_threat_model.png.”
This code creates a threat model using PyTM and represents the “Insecure Data Storage” threat
scenario. It includes actors such as “Attacker” and “User” and a datastore representing sensitive
data.
The threat model defines the “Insecure Data Storage” threat and includes attack paths such as
“Exploiting Storage Vulnerability” by the attacker and “Unauthorized Access to Stored Data” by
the user.
from pytm import TM, Actor, Datastore
# Create a new threat model
tm = TM("Data Leakage or Unauthorized Access Threat Model")
# Create actors
attacker = Actor("Attacker")
user = Actor("User")
# Create datastore
datastore = Datastore("Sensitive Data")
# Define data leakage or unauthorized access threat
tm.add_threat()
tm.threat.name("Data Leakage or Unauthorized Access")
tm.threat.description("Threat of unauthorized access or leakage of sensitive data")
# Define attack paths
tm.attack_path(attacker, datastore, "Exploiting Vulnerability")
tm.attack_path(user, datastore, "Unauthorized Access")
# Generate the threat model diagram
tm.generate_diagram("data_leakage_unauthorized_access_threat_model.png")
Insecure data storage
The code generates a threat model diagram in PNG format, named
“insecure_data_storage_threat_model.png.”
This code creates a threat model using PyTM and represents the “Inadequate Network
Segmentation” threat scenario. It includes actors such as “Attacker,” “Internal User,” and “External
User,” and defines boundaries for the internal and external networks.
The threat model defines the “Inadequate Network Segmentation” threat and includes dataflows
representing the flow of sensitive data, unauthorized access, exfiltration of sensitive data, and
command and control.
The code generates a threat model diagram in PNG format, named
“inadequate_network_segmentation_threat_model.png.”
from pytm import TM, Actor, Datastore
# Create a new threat model
tm = TM("Insecure Data Storage Threat Model")
# Create actors
attacker = Actor("Attacker")
user = Actor("User")
# Create datastore
datastore = Datastore("Sensitive Data")
# Define insecure data storage threat
tm.add_threat()
tm.threat.name("Insecure Data Storage")
tm.threat.description("Threat of insecure storage of sensitive data")
# Define attack paths
tm.attack_path(attacker, datastore, "Exploiting Storage Vulnerability")
tm.attack_path(user, datastore, "Unauthorized Access to Stored Data")
# Generate the threat model diagram
tm.generate_diagram("insecure_data_storage_threat_model.png")
Inadequate network segmentation
This code creates a threat model using PyTM and represents the “Man-in-the-Middle (MitM)
Attacks” threat scenario. It includes actors such as “Attacker,” “Client,” and “Server,” and defines
from pytm import TM, Actor, Dataflow, Boundary
# Create a new threat model
tm = TM("Inadequate Network Segmentation Threat Model")
# Create actors
attacker = Actor("Attacker")
internalUser = Actor("Internal User")
externalUser = Actor("External User")
# Create boundaries
internalNetwork = Boundary("Internal Network")
externalNetwork = Boundary("External Network")
# Define dataflows
dataflow1 = Dataflow(internalUser, internalNetwork, "Sensitive Data Flow")
dataflow2 = Dataflow(externalUser, internalNetwork, "Unauthorized Access")
dataflow3 = Dataflow(internalNetwork, externalNetwork, "Exfiltration of Sensitive Data")
dataflow4 = Dataflow(internalNetwork, externalNetwork, "Command and Control")
# Define inadequate network segmentation threat
tm.add_threat()
tm.threat.name("Inadequate Network Segmentation")
tm.threat.description("Threat of inadequate segmentation between internal and external networks")
# Define attack paths
tm.attack_path(attacker, dataflow2, "Exploiting Insufficient Segmentation")
tm.attack_path(attacker, dataflow3, "Exfiltration of Sensitive Data")
tm.attack_path(attacker, dataflow4, "Command and Control")
# Generate the threat model diagram
tm.generate_diagram("inadequate_network_segmentation_threat_model.png")
Man-in-the-Middle attacks
boundaries for the client and server components.
The threat model defines the “Man-in-the-Middle Attacks” threat and includes a dataflow
representing the flow of sensitive data between the client and server.
The code generates a threat model diagram in PNG format, named
“man_in_the_middle_attacks_threat_model.png.”
from pytm import TM, Actor, Dataflow, Boundary
# Create a new threat model
tm = TM("Man-in-the-Middle Attacks Threat Model")
# Create actors
attacker = Actor("Attacker")
client = Actor("Client")
server = Actor("Server")
# Create boundaries
clientBoundary = Boundary("Client Boundary")
serverBoundary = Boundary("Server Boundary")
# Define dataflows
dataflow1 = Dataflow(client, server, "Sensitive Data Flow")
# Define Man-in-the-Middle attack threat
tm.add_threat()
tm.threat.name("Man-in-the-Middle (MitM) Attacks")
tm.threat.description("Threat of an attacker intercepting and tampering with communication betwee
# Define attack paths
tm.attack_path(attacker, dataflow1, "Intercepting and Tampering with Communication")
# Generate the threat model diagram
tm.generate_diagram("man_in_the_middle_attacks_threat_model.png")
Resource exhaustion
This code creates a threat model using PyTM and represents the “Resource Exhaustion” threat
scenario. It includes actors such as “Attacker” and “Service” and defines a dataflow between
them.
The threat model defines the “Resource Exhaustion” threat and includes an attack path
representing the attacker’s ability to consume excessive resources, leading to service availability
impact.
The code generates a threat model diagram in PNG format, named
“resource_exhaustion_threat_model.png.”
This code creates a threat model using PyTM and represents the “Distributed Denial of Service
(DDoS) Attacks” threat scenario. It includes actors such as “Attacker” and “Target” and defines a
from pytm import TM, Actor, Dataflow
# Create a new threat model
tm = TM("Resource Exhaustion Threat Model")
# Create actors
attacker = Actor("Attacker")
service = Actor("Service")
# Define dataflows
dataflow = Dataflow(attacker, service, "Data Flow")
# Define Resource Exhaustion threat
tm.add_threat()
tm.threat.name("Resource Exhaustion")
tm.threat.description("Threat of an attacker consuming excessive resources and impacting service
# Define attack paths
tm.attack_path(attacker, dataflow, "Excessive Resource Consumption")
# Generate the threat model diagram
tm.generate_diagram("resource_exhaustion_threat_model.png")
Distributed DoS (DDoS) attacks
dataflow between them.
The threat model defines the “DDoS Attacks” threat and includes an attack path representing the
attacker overwhelming the target system with a high volume of requests, causing denial of
service.
The code generates a threat model diagram in PNG format, named
“ddos_attacks_threat_model.png.”
This code creates a threat model using PyTM and represents the “Misconfigured Security
Settings” threat scenario. It includes actors such as “Administrator” and “Attacker” and defines a
dataflow between them.
from pytm import TM, Actor, Dataflow
# Create a new threat model
tm = TM("DDoS Attacks Threat Model")
# Create actors
attacker = Actor("Attacker")
target = Actor("Target")
# Define dataflows
dataflow = Dataflow(attacker, target, "Data Flow")
# Define DDoS Attacks threat
tm.add_threat()
tm.threat.name("DDoS Attacks")
tm.threat.description("Threat of an attacker overwhelming the target system with a high volume of
# Define attack paths
tm.attack_path(attacker, dataflow, "DDoS Attack")
# Generate the threat model diagram
tm.generate_diagram("ddos_attacks_threat_model.png")
Misconfigured security settings
The threat model defines the “Misconfigured Security Settings” threat and describes the threat
arising from misconfigured security settings, leading to vulnerabilities and potential unauthorized
access.
The code generates a threat model diagram in PNG format, named
“misconfigured_security_settings_threat_model.png.”
This code creates a threat model using PyTM and represents the “Insecure Default
Configurations” threat scenario. It includes actors such as “Administrator” and “Attacker” and
defines a dataflow between them.
The threat model defines the “Insecure Default Configurations” threat and describes the threat
arising from insecure default configurations, leading to vulnerabilities and potential unauthorized
from pytm import TM, Actor, Dataflow
# Create a new threat model
tm = TM("Misconfigured Security Settings Threat Model")
# Create actors
administrator = Actor("Administrator")
attacker = Actor("Attacker")
# Define dataflows
dataflow = Dataflow(administrator, attacker, "Data Flow")
# Define Misconfigured Security Settings threat
tm.add_threat()
tm.threat.name("Misconfigured Security Settings")
tm.threat.description("Threat arising from misconfigured security settings, leading to vulnerabil
# Define attack paths
tm.attack_path(administrator, dataflow, "Misconfiguration Attack")
# Generate the threat model diagram
tm.generate_diagram("misconfigured_security_settings_threat_model.png")
Insecure default configurations
access.
The code generates a threat model diagram in PNG format, named
“insecure_default_configurations_threat_model.png.”
This code creates a threat model using PyTM and represents the “Delayed Patching of Software”
threat scenario. It includes actors such as “Administrator” and “Attacker” and defines a dataflow
between them.
The threat model defines the “Delayed Patching of Software” threat and describes the threat
arising from delayed or inadequate software patching, leaving systems vulnerable to known
exploits.
from pytm import TM, Actor, Dataflow
# Create a new threat model
tm = TM("Insecure Default Configurations Threat Model")
# Create actors
administrator = Actor("Administrator")
attacker = Actor("Attacker")
# Define dataflows
dataflow = Dataflow(administrator, attacker, "Data Flow")
# Define Insecure Default Configurations threat
tm.add_threat()
tm.threat.name("Insecure Default Configurations")
tm.threat.description("Threat arising from insecure default configurations, leading to vulnerabil
# Define attack paths
tm.attack_path(administrator, dataflow, "Insecure Default Configurations Attack")
# Generate the threat model diagram
tm.generate_diagram("insecure_default_configurations_threat_model.png")
Delayed patching of software
The code generates a threat model diagram in PNG format, named
“delayed_patching_threat_model.png.”
This code creates a threat model using PyTM and represents the “Lack of Vulnerability Scanning”
threat scenario. It includes actors such as “Administrator” and “Attacker” and defines a dataflow
between them.
The threat model defines the “Lack of Vulnerability Scanning” threat and describes the threat
arising from the lack of regular vulnerability scanning, which can result in undetected
vulnerabilities and potential exploitation.
The code generates a threat model diagram in PNG format, named
“lack_of_vulnerability_scanning_threat_model.png.”
from pytm import TM, Actor, Dataflow
# Create a new threat model
tm = TM("Delayed Patching of Software Threat Model")
# Create actors
administrator = Actor("Administrator")
attacker = Actor("Attacker")
# Define dataflows
dataflow = Dataflow(administrator, attacker, "Data Flow")
# Define Delayed Patching of Software threat
tm.add_threat()
tm.threat.name("Delayed Patching of Software")
tm.threat.description("Threat arising from delayed or inadequate software patching, leaving syste
# Define attack paths
tm.attack_path(administrator, dataflow, "Delayed Patching of Software Attack")
# Generate the threat model diagram
tm.generate_diagram("delayed_patching_threat_model.png")
Lack of vulnerability scanning
This code creates a threat model using PyTM and represents the “Malicious or Negligent Insiders”
threat scenario. It includes actors such as “Insider” and “Attacker” and defines a dataflow
between them.
The threat model defines the “Malicious or Negligent Insiders” threat and describes the threat
arising from insiders with malicious intent or negligent behavior who may abuse their privileges,
steal sensitive data, or cause damage to the system.
The code generates a threat model diagram in PNG format, named
“malicious_or_negligent_insiders_threat_model.png.”
from pytm import TM, Actor, Dataflow
# Create a new threat model
tm = TM("Lack of Vulnerability Scanning Threat Model")
# Create actors
administrator = Actor("Administrator")
attacker = Actor("Attacker")
# Define dataflows
dataflow = Dataflow(administrator, attacker, "Data Flow")
# Define Lack of Vulnerability Scanning threat
tm.add_threat()
tm.threat.name("Lack of Vulnerability Scanning")
tm.threat.description("Threat arising from the lack of regular vulnerability scanning, which can
# Define attack paths
tm.attack_path(administrator, dataflow, "Lack of Vulnerability Scanning Attack")
# Generate the threat model diagram
tm.generate_diagram("lack_of_vulnerability_scanning_threat_model.png")
Malicious or negligent insiders
This code creates a threat model using PyTM and represents the “Unauthorized Data Access or
Theft” threat scenario. It includes actors such as “Attacker” and “User” and defines a dataflow
between the user and a sensitive datastore.
The threat model defines the “Unauthorized Data Access or Theft” threat and describes the threat
of unauthorized access or theft of sensitive data by attackers.
The code generates a threat model diagram in PNG format, named
“unauthorized_data_access_theft_threat_model.png.”
from pytm import TM, Actor, Dataflow
# Create a new threat model
tm = TM("Malicious or Negligent Insiders Threat Model")
# Create actors
insider = Actor("Insider")
attacker = Actor("Attacker")
# Define dataflows
dataflow = Dataflow(insider, attacker, "Data Flow")
# Define Malicious or Negligent Insiders threat
tm.add_threat()
tm.threat.name("Malicious or Negligent Insiders")
tm.threat.description("Threat arising from insiders with malicious intent or negligent behavior w
# Define attack paths
tm.attack_path(insider, dataflow, "Malicious or Negligent Insiders Attack")
# Generate the threat model diagram
tm.generate_diagram("malicious_or_negligent_insiders_threat_model.png")
Unauthorized data access or theft
from pytm import TM, Actor, Datastore, Boundary, Dataflow
This code creates a threat model using PyTM and represents the “Unauthorized Physical Access”
threat scenario. It includes actors such as “Attacker,” “Physical Attacker,” and “User” and defines a
dataflow between the user and a sensitive equipment datastore.
The threat model defines the “Unauthorized Physical Access” threat and describes the threat of
unauthorized physical access to sensitive equipment by attackers.
The code generates a threat model diagram in PNG format, named
“unauthorized_physical_access_threat_model.png.”
# Create a new threat model
tm = TM("Unauthorized Data Access or Theft Threat Model")
# Create actors
attacker = Actor("Attacker")
user = Actor("User")
# Create a boundary
boundary = Boundary("Internal Network")
# Create a datastore
datastore = Datastore("Sensitive Data")
# Define dataflows
dataflow = Dataflow(user, datastore, "Data Access")
# Define Unauthorized Data Access or Theft threat
tm.add_threat()
tm.threat.name("Unauthorized Data Access or Theft")
tm.threat.description("Threat of unauthorized access or theft of sensitive data by attackers")
# Define attack paths
tm.attack_path(attacker, dataflow, "Unauthorized Data Access or Theft Attack")
# Generate the threat model diagram
tm.generate_diagram("unauthorized_data_access_theft_threat_model.png")
Unauthorized physical access
This code creates a threat model using PyTM and represents the “Theft or Destruction of
Hardware” threat scenario. It includes actors such as “Attacker,” “Physical Attacker,” and “User”
and defines a dataflow between the user and a hardware datastore.
from pytm import TM, Actor, Datastore, Boundary, Dataflow
# Create a new threat model
tm = TM("Unauthorized Physical Access Threat Model")
# Create actors
attacker = Actor("Attacker")
physical_attacker = Actor("Physical Attacker")
user = Actor("User")
# Create a boundary
boundary = Boundary("Physical Location")
# Create a datastore
datastore = Datastore("Sensitive Equipment")
# Define dataflows
dataflow = Dataflow(user, datastore, "Data Access")
# Define Unauthorized Physical Access threat
tm.add_threat()
tm.threat.name("Unauthorized Physical Access")
tm.threat.description("Threat of unauthorized physical access to sensitive equipment by attackers
# Define attack paths
tm.attack_path(physical_attacker, dataflow, "Unauthorized Physical Access Attack")
# Generate the threat model diagram
tm.generate_diagram("unauthorized_physical_access_threat_model.png")
Theft or destruction of hardware
The threat model defines the “Theft or Destruction of Hardware” threat and describes the threat
of theft or destruction of hardware by attackers.
The code generates a threat model diagram in PNG format, named
“theft_destruction_hardware_threat_model.png.”
from pytm import TM, Actor, Datastore, Boundary, Dataflow
# Create a new threat model
tm = TM("Theft or Destruction of Hardware Threat Model")
# Create actors
attacker = Actor("Attacker")
physical_attacker = Actor("Physical Attacker")
user = Actor("User")
# Create a boundary
boundary = Boundary("Physical Location")
# Create a datastore
datastore = Datastore("Hardware")
# Define dataflows
dataflow = Dataflow(user, datastore, "Data Access")
# Define Theft or Destruction of Hardware threat
tm.add_threat()
tm.threat.name("Theft or Destruction of Hardware")
tm.threat.description("Threat of theft or destruction of hardware by attackers")
# Define attack paths
tm.attack_path(physical_attacker, dataflow, "Theft or Destruction of Hardware Attack")
# Generate the threat model diagram
tm.generate_diagram("theft_destruction_hardware_threat_model.png")
Vulnerabilities in third-party components
This code creates a threat model using PyTM and represents the “Vulnerabilities in Third-Party
Components” threat scenario. It includes actors such as “Attacker” and “User” and defines a
dataflow between the user and a sensitive data datastore.
The threat model defines the “Vulnerabilities in Third-Party Components” threat and describes
the threat of vulnerabilities in third-party components used in the system.
The code generates a threat model diagram in PNG format, named
“third_party_component_vulnerabilities_threat_model.png.”
from pytm import TM, Actor, Datastore, Dataflow, Boundary
# Create a new threat model
tm = TM("Vulnerabilities in Third-Party Components Threat Model")
# Create actors
attacker = Actor("Attacker")
user = Actor("User")
# Create a boundary
boundary = Boundary("System Boundary")
# Create a datastore
datastore = Datastore("Sensitive Data")
# Define dataflows
dataflow = Dataflow(user, datastore, "Data Access")
# Define Vulnerabilities in Third-Party Components threat
tm.add_threat()
tm.threat.name("Vulnerabilities in Third-Party Components")
tm.threat.description("Threat of vulnerabilities in third-party components used in the system")
# Define attack paths
tm.attack_path(attacker, dataflow, "Exploitation of Third-Party Component Vulnerabilities")
This code creates a threat model using PyTM and represents the “Lack of Oversight on Third-
Party Activities” threat scenario. It includes actors such as “Attacker,” “User,” and “Third-Party”
and defines dataflows between the user, third-party process, and a sensitive data datastore.
The threat model defines the “Lack of Oversight on Third-Party Activities” threat and describes
the threat of insufficient oversight on third-party activities in the system.
The code generates a threat model diagram in PNG format, named
“lack_of_oversight_third_party_activities_threat_model.png.”
# Generate the threat model diagram
tm.generate_diagram("third_party_component_vulnerabilities_threat_model.png")
Lack of oversight on third-party activities
from pytm import TM, Actor, Process, Datastore, Dataflow, Boundary
# Create a new threat model
tm = TM("Lack of Oversight on Third-Party Activities Threat Model")
# Create actors
attacker = Actor("Attacker")
user = Actor("User")
third_party = Actor("Third-Party")
# Create a boundary
boundary = Boundary("System Boundary")
# Create a process
process = Process("Third-Party Process")
# Create a datastore
datastore = Datastore("Sensitive Data")
# Define dataflows
dataflow1 = Dataflow(user, process, "Data Sharing")
dataflow2 = Dataflow(process, datastore, "Data Storage")
Abnormal network traffic
Potential threats
Port/host scan
The port or host scan behaviors mean one of the hosts may have
been infected by a malware program, and the malware program
# Define Lack of Oversight on Third-Party Activities threat
tm.add_threat()
tm.threat.name("Lack of Oversight on Third-Party Activities")
tm.threat.description("Threat of lack of oversight on third-party activities in the system")
# Define attack paths
tm.attack_path(attacker, dataflow1, "Unauthorized Data Sharing")
tm.attack_path(attacker, dataflow2, "Unauthorized Data Storage")
# Generate the threat model diagram
tm.generate_diagram("lack_of_oversight_third_party_activities_threat_model.png")
Threat detection
Abnormal network traffic
Potential threats
is looking for vulnerabilities, other services, or hosts on the
network.
A high number of outbound DNS
requests from the same host
This is a symptom of Command and Control (C&C) malware,
establishing communication between the infected host and the
C&C server using the DNS protocol.
A high number of outbound HTTP
requests from the same host
This is a symptom of C&C, establishing communication between
the infected host and the C&C server using the HTTP protocol.
Periodical outbound traffic with
samesized requests or during the same
period of time every day
This is a symptom of C&C malware, establishing communication
between the infected host and the C&C server.
Outbound traffic to an external web
or DNS listed as a known threat by
threat intelligence feeds
The user may be tricked through social engineering to connect
to an external known threat web or the C&C connection is
successfully established.
To visualize the network threat status, there are two recommended open source tools: Malcom
and Maltrail (Malicious Traffic detection system). Malcom can present a host communication
relationship diagram. It helps us to understand whether there are any internal hosts connected to
an external suspicious C&C server or known bad sites https://github.com/tomchop/malcom#what-
is-malcom
An analysis of hosts for suspicious behaviors also poses a significant challenge due to the
availability of logs. For example, dynamic runtime information may not be logged in files and the
original process used to drop a suspicious file may not be recorded. Therefore, it is always
recommended to install a host IDS/IPS such as OSSEC (Open Source HIDS SEcurity) or host
antivirus software as the first line of defense against malware. Once the host IDS/IPS or antivirus
software is in place, threat intelligence and big data analysis are supplementary, helping us to
understand the overall host’s security posture and any known Indicators of Compromises (IoCs) in
existing host environments.
Based on the level of severity, the following are key behaviors that may indicate a compromised
host:
Indicators of compromises
The source of IP address analysis can help to identify the following: A known bad IP or TOR exit
node Abnormal geolocation changes Concurrent connections from different geolocations The
MaxMind GeoIP2 database can be used to translate the IP address to a geolocation:
https://dev.maxmind.com/geoip/geoip2/geolite2/#Downloads
The client fingerprint can be used to identify whether there are any unusual client or non-browser
connections. The open source ClientJS is a pure JavaScript that can be used to collect client
fingerprint information. The JA3 provided by Salesforce uses SSL/TLS connection profiling to
identify malicious clients. ClientJS: https://clientjs.org/ JA3: https://github.com/salesforce/ja3
When there is an outbound connection to an external website, we may check the threat reputation
of that target website. This can be done by means of the web application firewall, or web gateway
security solutions https://www.virustotal.com/
The domain name of the C&C server can be generated by DGAs. The key characteristics of the
DGA domain are high entropy, high consonant count, and long length of a domain name. Based on
these indicators, we may analyze whether the domain name is generated by DGAs and could be a
potential C&C server. DGA Detector: https://github.com/exp0se/dga_detector/ In addition, in order
to reduce false positives, we may also use Alexa’s top one million sites as a website whitelist.
Refer to https://s3.amazonaws.com/alexa-static/top-1m.csv.zip.
Cuckoo sandbox suspicious file analysis: https://cuckoosandbox.org/
In the case of DNS query analysis, the following are the key indicators of compromises: DNS
query to unauthorized DNS servers. Unmatched DNS replies can be an indicator of DNS spoofing.
Clients connect to multiple DNS servers. A long DNS query, such as one in excess of 150
characters, which is an indicator of DNS tunneling. A domain name with high entropy. This is an
indicator of DNS tunneling or a C&C server.
Copyright © 2019-2023 HADESS.
External source client IP
Client fingerprint (OS, browser, user agent, devices, and so on)
Web site reputation
Random Domain Name by Domain Generation Algorithms (DGAs)
Suspicious file downloads
DNS query
DevSecOps Guides
Code / SAST
SAST, or Static Application Security Testing, is a technique used in application security to analyze
the source code of an application for security vulnerabilities. SAST tools work by scanning the
source code of an application without actually executing the code, searching for common coding
errors, security flaws, and potential vulnerabilities.
SAST is a type of white-box testing, meaning that it relies on the tester having access to the
source code of the application being tested. This allows SAST tools to perform a thorough
analysis of the codebase, identifying potential vulnerabilities that may not be apparent through
other testing techniques.
SAST Tool
Description
Languages
Supported
Checkmarx
A SAST tool that analyzes source code for security
vulnerabilities, providing real-time feedback to developers
on potential issues.
Java, .NET, PHP,
Python, Ruby, Swift,
C/C++, Objective-C,
Scala, Kotlin,
JavaScript
SonarQube
A tool that provides continuous code inspection,
identifying and reporting potential security vulnerabilities,
as well as code quality issues.
Over 25 programming
languages, including
Java, C/C++, Python,
JavaScript, PHP, Ruby
Fortify Static
Code Analyzer
A SAST tool that analyzes source code for security
vulnerabilities, providing detailed reports and
recommendations for improving security.
Java, .NET, C/C++,
Python, JavaScript
Veracode Static
Analysis
A SAST tool that analyzes code for security vulnerabilities
and compliance with industry standards, providing
detailed reports and actionable recommendations.
Over 25 programming
languages, including
Java, .NET, Python,
SAST
SAST Tool
Description
Languages
Supported
Ruby, PHP, JavaScript,
C/C++
Semgrep
Semgrep is designed to be fast and easy to use, and it
supports multiple programming languages, including
Python, Java, JavaScript, Go, and more. It uses a simple
pattern matching language to identify patterns of code
that are known to be vulnerable, and it can be configured
to scan specific parts of a codebase, such as a single file
or a directory.
Over 25 programming
languages, including
Java, .NET, Python,
Ruby, PHP, JavaScript,
C/C++
CodeQL
CodeQL is based on a database of semantic code
representations that allows it to perform complex analysis
on code that other static analysis tools may miss. It
supports a wide range of programming languages,
including C, C++, C#, Java, JavaScript, Python, and more.
CodeQL can be used to analyze both open source and
proprietary code, and it can be used by both developers
and security researchers.
Over 25 programming
languages, including
Java, .NET, Python,
Ruby, PHP, JavaScript,
C/C++
Semgrep is designed to be fast and easy to use, and it supports multiple programming languages,
including Python, Java, JavaScript, Go, and more. It uses a simple pattern matching language to
identify patterns of code that are known to be vulnerable, and it can be configured to scan
specific parts of a codebase, such as a single file or a directory.
Semgrep can be used as part of the software development process to identify vulnerabilities early
on, before they can be exploited by attackers. It can be integrated into a CI/CD pipeline to
automatically scan code changes as they are made, and it can be used to enforce security
policies and coding standards across an organization.
create a sample rule. Here are the steps:
Semgrep
Install and set up Semgrep: To use Semgrep, you need to install it on your system. You can
download Semgrep from the official website, or install it using a package manager like pip.
Once installed, you need to set up a project and configure the scan settings.
1
The rule ID: This is a unique identifier for the rule.
The rule name: This is a descriptive name for the rule.
The rule description: This describes what the rule does and why it is important.
The rule pattern: This is the pattern that Semgrep will use to search for the vulnerability.
The rule severity: This is the severity level of the vulnerability (e.g. high, medium, low).
The rule language: This is the programming language that the rule applies to (e.g. Python,
Java, JavaScript).
The rule tags: These are optional tags that can be used to categorize the rule.
Here is an example rule that checks for SQL injection vulnerabilities in Python code:
Create a new Semgrep rule: To create a new Semgrep rule, you need to write a YAML file that
defines the rule. The YAML file should contain the following information:
2
•
•
•
•
•
•
•
id: sql-injection-py
name: SQL Injection in Python Code
description: Checks for SQL injection vulnerabilities in Python code.
severity: high
language: python
tags:
  - security
  - sql-injection
patterns:
  - pattern: |
      db.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + pas
    message: |
      SQL injection vulnerability found in line {line}: {code}
Run Semgrep with the new rule: Once you have created the new rule, you can run Semgrep to
scan your code. To run Semgrep, you need to specify the path to the code you want to scan
and the path to the YAML file that contains the rule. Here is an example command:
1
semgrep --config path/to/rule.yaml path/to/code/
Review the scan results: After the scan is complete, Semgrep will display the results in the
terminal. The results will include information about the vulnerabilities that were found,
1
how to use Semgrep in a CI/CD pipeline on GitHub:
Here is an example semgrep.yml file that checks for SQL injection vulnerabilities in Python code:
Here is an example semgrep.yml workflow that runs Semgrep on every push to the master branch:
including the severity level, the location in the code where the vulnerability was found, and the
code that triggered the rule.
Set up Semgrep in your project: To use Semgrep in your CI/CD pipeline, you need to install it
and set it up in your project. You can do this by adding a semgrep.yml file to your project’s root
directory. The semgrep.yml file should contain the rules that you want to apply to your
codebase.
1
rules:
  - id: sql-injection-py
    pattern: db.execute("SELECT * FROM users WHERE username = $username AND password = $password"
Create a GitHub workflow: Once you have set up Semgrep in your project, you need to create a
GitHub workflow that runs Semgrep as part of your CI/CD pipeline. To create a workflow, you
need to create a .github/workflows directory in your project and add a YAML file that defines
the workflow.
1
name: Semgrep
on:
  push:
    branches:
      - master
jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2
    - name: Run Semgrep
      uses: returntocorp/semgrep-action@v1
      with:
CodeQL is based on a database of semantic code representations that allows it to perform
complex analysis on code that other static analysis tools may miss. It supports a wide range of
programming languages, including C, C++, C#, Java, JavaScript, Python, and more. CodeQL can
be used to analyze both open source and proprietary code, and it can be used by both developers
and security researchers.
To use CodeQL, developers write queries in a dedicated query language called QL. QL is a
declarative language that allows developers to express complex analyses in a concise and
understandable way. Queries can be written to check for a wide range of issues, such as buffer
overflows, SQL injection vulnerabilities, race conditions, and more.
CodeQL can be integrated into a variety of development tools, such as IDEs, code review tools,
and CI/CD pipelines. This allows developers to run CodeQL automatically as part of their
development process and catch issues early in the development cycle.
Here is an example of how to create a CodeQL rule and run it:
        args: -c semgrep.yml
Push changes to GitHub: Once you have created the workflow, you need to push the changes
to your GitHub repository. This will trigger the workflow to run Semgrep on your codebase.
1
Review the results: After the workflow has completed, you can review the results in the GitHub
Actions tab. The results will include information about the vulnerabilities that were found,
including the severity level, the location in the code where the vulnerability was found, and the
code that triggered the rule.
2
CodeQL
Identify the issue: Let’s say we want to create a CodeQL rule to detect SQL injection
vulnerabilities in a Java web application.
1
Write the query: To write the query, we can use the CodeQL libraries for Java and the CodeQL
built-in functions for detecting SQL injection vulnerabilities. Here is an example query:
2
import java
class SqlInjection extends JavaScript {
This query looks for calls to the executeQuery method with a string argument that can be tainted
with user input, and then checks if the argument is used in a way that could lead to a SQL
injection vulnerability. If a vulnerability is detected, the query returns the call and a message
indicating the potential vulnerability.
This command runs the query against a CodeQL database named MyAppDB and outputs the
results to a CSV file named results.csv.
Here is an example command to add the query to our CodeQL database:
  SqlInjection() {
    this = "sql injection"
  }
  from MethodCall call, DataFlow::PathNode arg, SQL::StringExpression sqlExpr
  where call.getMethod().getName() = "executeQuery" and
        arg = call.getArgument(1) and
        arg = sqlExpr.getAnOperand() and
        exists (SQL::TaintedFlow tainted |
          tainted = dataFlow::taintThrough(arg, tainted) and
          tainted.(SQL::Source) and
          tainted.(SQL::Sink)
        )
  select call, "Potential SQL injection vulnerability"
}
Test the query: To test the query, we can run it against a small sample of our codebase using
the CodeQL CLI tool. Here is an example command:
1
$ codeql query run --database=MyAppDB --format=csv --output=results.csv path/to/query.ql
Integrate the query: To integrate the query into our development process, we can add it to our
CodeQL database and run it automatically as part of our CI/CD pipeline. This can be done
using the CodeQL CLI tool and the CodeQL GitHub Action.
1
And here is an example GitHub Action workflow to run the query automatically on every push to
the master branch:
Copyright © 2019-2023 HADESS.
$ codeql database analyze MyAppDB --queries=path/to/query.ql
name: CodeQL
on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/
DevSecOps Guides
Code / SCA
SCA stands for Software Composition Analysis. It is a type of application security testing that
focuses on identifying and managing third-party components and dependencies used within an
application. SCA tools scan an application’s codebase and build artifacts to identify any third-
party libraries or components, and then assess those components for known security
vulnerabilities or other issues.
the SCA process typically involves the following steps:
By performing SCA, organizations can gain visibility into the third-party components and libraries
used within their applications, and can proactively manage any security vulnerabilities or issues
associated with those components. This can help to improve the overall security and resilience of
the application.
SCA tools work by scanning your codebase and identifying the open source components that are
used in your application. They then compare this list against known vulnerabilities in their
database and alert you if any vulnerabilities are found. This helps you to manage your open source
components and ensure that you are not using any vulnerable components in your application.
SCA
Discovery: The SCA tool scans the application’s codebase and build artifacts to identify any
third-party libraries or components used within the application.
1
Inventory: The SCA tool creates an inventory of all the third-party components and libraries
used within the application, including their versions, license types, and any known security
vulnerabilities or issues.
2
Assessment: The SCA tool assesses each component in the inventory for known security
vulnerabilities or other issues, using sources such as the National Vulnerability Database
(NVD) and Common Vulnerabilities and Exposures (CVE) databases.
3
Remediation: Based on the results of the assessment, the SCA tool may provide
recommendations for remediation, such as upgrading to a newer version of a component, or
switching to an alternative component that is more secure.
4
SCA Tool
Description
Languages Supported
Sonatype Nexus
Lifecycle
A software supply chain automation and
management tool
Java, .NET, Ruby, JavaScript,
Python, Go, PHP, Swift
Black Duck
An open source security and license
compliance management tool
Over 20 languages including Java,
.NET, Python, Ruby, JavaScript,
PHP
WhiteSource
A cloud-based open source security and
license compliance management tool
Over 30 languages including Java,
.NET, Python, Ruby, JavaScript,
PHP
Snyk
A developer-first security and dependency
management tool
Over 40 languages including
Java, .NET, Python, Ruby,
JavaScript, PHP, Go
FOSSA
A software development tool that automates
open source license compliance and
vulnerability management
Over 30 languages including Java,
.NET, Python, Ruby, JavaScript,
PHP
Here is an example of how to use SCA in a CI/CD pipeline:
Choose an SCA tool: There are several SCA tools available in the market, such as Snyk, Black
Duck, and WhiteSource. You need to choose an SCA tool that is compatible with your
application stack and provides the features that you need.
1
Integrate the tool into your CI/CD pipeline: Once you have chosen an SCA tool, you need to
integrate it into your CI/CD pipeline. This can be done by adding a step in your pipeline that
runs the SCA tool and reports the results.
2
Configure the tool: You need to configure the SCA tool to scan your application code and
identify the open source components that are used in your application. This can be done by
providing the tool with access to your source code repository and specifying the
dependencies of your application.
3
Analyze the results: Once the SCA tool has finished scanning your codebase, it will generate a
report of the open source components that are used in your application and any vulnerabilities
that are associated with those components. You need to analyze the report and take action on
any vulnerabilities that are identified.
4
Here is an example of a CI/CD pipeline that includes an SCA step:
In this example, the SCA tool is integrated into the pipeline using the Snyk GitHub Action. The tool
is configured to scan the package.json file and report any vulnerabilities with a severity threshold
Remediate the vulnerabilities: If any vulnerabilities are identified, you need to remediate them
by either upgrading the vulnerable components or removing them from your application.
5
name: MyApp CI/CD Pipeline
on:
  push:
    branches: [ master ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2
    - name: Build and test
      run: |
        npm install
        npm test
    - name: Run SCA
      uses: snyk/actions@v1
      with:
        file: package.json
        args: --severity-threshold=high
    - name: Deploy to production
      if: github.ref == 'refs/heads/master'
      run: deploy.sh
of “high”. If any vulnerabilities are identified, the pipeline will fail and the developer will be notified
to take action.
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Code / Secure Pipeline
A secure pipeline is a set of processes and tools used to build, test, and deploy software in a way
that prioritizes security at every stage of the development lifecycle. The goal of a secure pipeline
is to ensure that applications are thoroughly tested for security vulnerabilities and compliance
with security standards before they are released into production.
A secure pipeline typically involves the following stages:
Secure Pipeline
Source Code Management: Developers use source code management tools, such as Git or
SVN, to manage the code for the application.
1
Build: The application code is built into executable code using a build tool, such as Maven or
Gradle.
2
Static Analysis: A static analysis tool, such as a SAST tool, is used to scan the code for
security vulnerabilities.
3
Unit Testing: Developers write unit tests to ensure that the application functions as expected
and to catch any bugs or errors.
4
Dynamic Analysis: A dynamic analysis tool, such as a DAST tool, is used to test the application
in a running environment and identify any security vulnerabilities.
5
Artifact Repository: The application and all its dependencies are stored in an artifact
repository, such as JFrog or Nexus.
6
Staging Environment: The application is deployed to a staging environment for further testing
and validation.
7
Compliance Check: A compliance tool is used to check that the application meets any
regulatory or compliance requirements.
8
Approval: The application is reviewed and approved for deployment to production.
9
By implementing a secure pipeline, organizations can ensure that their applications are thoroughly
tested for security vulnerabilities and compliance with security standards, reducing the risk of
security breaches and ensuring that applications are more resilient to attacks.
Step 1: Set up version control
Use a version control system (VCS) such as Git to manage your application code.
Store your code in a private repository and limit access to authorized users.
Use strong authentication and authorization controls to secure access to your repository.
Step 2: Implement continuous integration
Use a continuous integration (CI) tool such as Jenkins or Travis CI to automate your build
process.
Ensure that your CI tool is running in a secure environment.
Use containerization to isolate your build environment and prevent dependencies from
conflicting with each other.
Step 3: Perform automated security testing
Use SAST, DAST, and SCA tools to perform automated security testing on your application
code.
Integrate these tools into your CI pipeline so that security testing is performed automatically
with each build.
Configure the tools to report any security issues and fail the build if critical vulnerabilities are
found.
Step 4: Implement continuous deployment
Use a continuous deployment (CD) tool such as Kubernetes or AWS CodeDeploy to automate
your deployment process.
Implement a release process that includes thorough testing and review to ensure that only
secure and stable code is deployed.
Step 5: Monitor and respond to security threats
Implement security monitoring tools to detect and respond to security threats in real-time.
Deployment: The application is deployed to production using a deployment tool, such as
Ansible or Kubernetes.
10
•
•
•
•
•
•
•
•
•
•
•
•
Use tools such as intrusion detection systems (IDS) and security information and event
management (SIEM) systems to monitor your infrastructure and applications.
Implement a security incident response plan to quickly respond to any security incidents that
are detected.
example of a secure CI/CD pipeline
•
•
# Define the pipeline stages
stages:
  - build
  - test
  - security-test
  - deploy
# Define the jobs for each stage
jobs:
  build:
    # Build the Docker image and tag it with the commit SHA
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Build Docker image
        run: |
          docker build -t myapp:$ .
          docker tag myapp:$ myapp:latest
  test:
    # Run unit and integration tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
  security-test:
    # Perform automated security testing using SAST, DAST, and SCA tools
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Perform SAST
        uses: shiftleftio/action-sast@v3.3.1
        with:
          scan-targets: .
          shiftleft-org-id: $
          shiftleft-api-key: $
      - name: Perform DAST
        uses: aquasecurity/trivy-action@v0.5.0
        with:
          image-ref: myapp:$
      - name: Perform SCA
        uses: snyk/actions@v1
        with:
          file: package.json
          args: --severity-threshold=high
  deploy:
    # Deploy the application to the production environment
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/master'
    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@master
        with:
          host: production-server.example.com
          username: $
          password: $
          script: |
            docker pull myapp:latest
            docker stop myapp || true
            docker rm myapp || true
            docker run -d --name myapp -p 80:80 myapp:latest
In this example, the YAML file defines a CI/CD pipeline with four stages: build, test, security-test,
and deploy. Each stage has a job that performs a specific set of tasks. The build  job builds a
Docker image for the application, the test  job runs unit and integration tests, the security-test
job performs automated security testing using SAST, DAST, and SCA tools, and the deploy  job
deploys the application to the production environment.
Each job is defined with a runs-on  parameter that specifies the operating system that the job
should run on. The steps for each job are defined with name  and run  parameters that specify the
name of the step and the command to run. The uses  parameter is used to specify external actions
or packages that should be used in the step.
The if  parameter is used to conditionally run a job based on a specific condition, such as the
branch or tag that triggered the pipeline. Secrets are stored in the GitHub repository’s secrets
store and accessed using the $  syntax.
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Build & Test / Artifacts
Artifacts are typically created during the build and deployment process, and are stored in a
repository or other storage location so that they can be easily retrieved and deployed as needed.
There are a number of methods that can be used to save artifacts in a DevSecOps environment,
including:
1- Create a secure development environment:
Set up a development environment that is separate from production.
Use version control to track changes to the source code.
Use secrets management tools to store sensitive information like API keys and passwords.
2- Implement security testing into the development process:
Artifacts
Build Artifacts: Build artifacts are created during the build process and include compiled code,
libraries, and other files that are needed to deploy and run the application. These artifacts can
be saved in a repository or other storage location for later use.
1
Container Images: Container images are a type of artifact that contain everything needed to
run the application, including the code, runtime, and dependencies. These images can be
saved in a container registry or other storage location and can be easily deployed to any
environment that supports containers.
2
Infrastructure as Code (IaC) Artifacts: IaC artifacts are created as part of the configuration
management process and include scripts, templates, and other files that are used to define
and manage the infrastructure of the application. These artifacts can be stored in a repository
or other storage location and can be used to deploy the infrastructure to any environment.
3
Test Artifacts: Test artifacts include test scripts, test results, and other files that are created as
part of the testing process. These artifacts can be stored in a repository or other storage
location for later reference and analysis.
4
Checklist for developing an artifact in DevSecOps
•
•
•
Use static analysis security testing (SAST) tools to analyze the source code for vulnerabilities.
Use dynamic application security testing (DAST) tools to test the application in a real-world
environment.
Use interactive application security testing (IAST) tools to detect vulnerabilities in real-time
during testing.
3- Automate the build process:
Use build automation tools like Maven or Gradle to compile the source code and build the artifact.
Include security testing tools in the build process.
4- Automate deployment:
Use configuration management tools like Ansible or Chef to automate deployment of the
artifact.
Use infrastructure-as-code tools like Terraform or CloudFormation to automate the creation
and management of infrastructure.
5- Implement continuous integration/continuous delivery (CI/CD) practices:
Use a CI/CD pipeline to automate the entire development process.
Use tools like Jenkins or CircleCI to manage the pipeline and run tests automatically.
Copyright © 2019-2023 HADESS.
•
•
•
•
•
•
•
DevSecOps Guides
Build & Test / Configuration Management
Configuration management is the process of managing and maintaining the configuration of an
application or system in a consistent and reliable manner. In a DevSecOps environment,
configuration management is an important component of ensuring that applications are secure
and reliable. Here are some common tools and practices used in configuration management in
DevSecOps:
To achieve this, you can use a configuration management tool like Ansible or Puppet to manage
the configuration of the system. Here’s a high-level overview of how this might work:
Configuration Management
Infrastructure as Code (IaC): IaC is a practice that involves writing code to define and manage
the infrastructure and configuration of an application or system. This approach provides a
more automated and repeatable way of managing configurations, and helps to ensure that the
infrastructure is consistent across different environments.
1
Configuration Management Tools: There are a number of configuration management tools that
can be used to manage configurations in a DevSecOps environment. Some popular examples
include Ansible, Chef, Puppet, and SaltStack.
2
Version Control: Version control systems like Git can be used to manage changes to
configurations over time, making it easier to track changes and roll back to previous
configurations if necessary.
3
Continuous Integration and Deployment (CI/CD): CI/CD pipelines can be used to automate the
deployment and configuration of applications in a DevSecOps environment. This can help to
ensure that configurations are consistent and up-to-date across different environments.
4
Security Configuration Management: Security configuration management involves ensuring
that the configurations of applications and systems are secure and meet industry standards
and best practices. This can include configuring firewalls, encryption, access controls, and
other security measures.
5
Playbooks are the heart of Ansible, and define the configuration steps for your infrastructure.
Define the configuration: You define the configuration of the system in a configuration file or
script. This includes things like the software packages to be installed, the network settings, the
user accounts, and any other system settings.
1
Version control: You use version control tools like Git to track changes to the configuration file,
and to maintain a history of changes.
2
Continuous integration and deployment: You use a CI/CD pipeline to build and test the
application, and to deploy the containers to the different environments. The configuration
management tool is integrated into the pipeline, so that any changes to the configuration are
automatically applied to the containers as they are deployed.
3
Automation: The configuration management tool automates the process of configuring the
system, so that the same configuration is applied consistently across all environments. This
reduces the risk of configuration errors and makes it easier to maintain the system.
4
Monitoring and reporting: The configuration management tool provides monitoring and
reporting capabilities, so that you can track the status of the system and identify any issues or
errors.
5
Ansible
ANSIBLE PLAYBOOKS
# playbook.yml
- hosts: web_servers
  tasks:
    - name: Install Apache
      apt:
        name: apache2
        state: latest
    - name: Start Apache
      service:
        name: apache2
        state: started
ANSIBLE VARIABLES
Vault allows you to encrypt sensitive data, like passwords and API keys.
Copyright © 2019-2023 HADESS.
# playbook.yml
- hosts: web_servers
  vars:
    http_port: 80
  tasks:
    - name: Install Apache
      apt:
        name: apache2
        state: latest
    - name: Configure Apache
      template:
        src: apache.conf.j2
        dest: /etc/apache2/apache.conf
Ansible Ad-Hoc Commands
$ ansible web_servers -m ping
$ ansible web_servers -a "apt update && apt upgrade -y"
Ansible Vault
$ ansible-vault create secrets.yml
# secrets.yml
api_key: ABCDEFGHIJKLMNOPQRSTUVWXYZ
DevSecOps Guides
Build & Test / DAST
DAST stands for Dynamic Application Security Testing. It is a type of application security testing
that involves testing an application in a running state to identify security vulnerabilities that may
be present.
DAST tools work by interacting with an application in much the same way as a user would, by
sending HTTP requests to the application and analyzing the responses that are received. This
allows DAST tools to identify vulnerabilities that may be present in the application’s logic,
configuration, or architecture.
Here are some key features of DAST:
1- Realistic testing: DAST provides a more realistic testing environment than SAST because it
tests the application in a running state, simulating how an attacker would interact with it.
2- Automation: DAST tools can be automated to provide continuous testing, allowing for faster
feedback on vulnerabilities.
3- Scalability: DAST tools can be scaled to test large and complex applications, making them
suitable for enterprise-level testing.
4- Coverage: DAST tools can provide coverage for a wide range of security vulnerabilities,
including those that may be difficult to detect through other forms of testing.
5- Ease of use: DAST tools are typically easy to use and require minimal setup, making them
accessible to developers and security teams.
DAST Tool
Description
OWASP ZAP
an open-source web application security scanner
Burp Suite
a web application security testing toolkit
DAST
Assuming we have a web application that we want to test for security vulnerabilities using DAST,
we can use OWASP ZAP, an open-source web application security scanner, in our pipeline.
1- First, we need to install OWASP ZAP and configure it with our web application. This can be
done by running the following commands in the pipeline:
2- Next, we need to run the security scan using OWASP ZAP. This can be done by running the
following command in the pipeline:
This will start the OWASP ZAP spider to crawl the web application and then run an active scan to
identify security vulnerabilities.
3- Finally, we need to generate a report of the security scan results. This can be done by running
the following command in the pipeline:
- name: Install OWASP ZAP
  run: |
    wget https://github.com/zaproxy/zaproxy/releases/download/v2.10.0/ZAP_2.10.0_Core.zip
    unzip ZAP_2.10.0_Core.zip -d zap
- name: Start OWASP ZAP
  run: |
    zap/zap.sh -daemon -host 127.0.0.1 -port 8080 -config api.disablekey=true
- name: Configure OWASP ZAP
  run: |
    zap/zap-cli.py -p 8080 open-url https://example.com
- name: Run OWASP ZAP scan
  run: |
    zap/zap-cli.py -p 8080 spider https://example.com
    zap/zap-cli.py -p 8080 active-scan https://example.com
- name: Generate OWASP ZAP report
  run: |
This will generate an HTML report of the security scan results that can be reviewed and acted
upon.
Copyright © 2019-2023 HADESS.
    zap/zap-cli.py -p 8080 report -o zap-report.html -f html
DevSecOps Guides
Build & Test / IAST
IAST stands for Interactive Application Security Testing. It is a type of application security testing
that combines the benefits of SAST (Static Application Security Testing) and DAST (Dynamic
Application Security Testing) tools.
IAST tools are designed to be integrated into the application being tested, and work by
instrumenting the application’s code to provide real-time feedback on any security vulnerabilities
that are identified during runtime. This allows IAST tools to detect vulnerabilities that may not be
visible through other forms of testing, such as those that are introduced by the application’s
configuration or environment.
Here are some key features of IAST:
IAST
Real-time feedback: IAST tools provide real-time feedback on security vulnerabilities as they
are identified during runtime, allowing developers to fix them as they are found.
1
Accuracy: IAST tools have a high degree of accuracy because they are able to detect
vulnerabilities in the context of the application’s runtime environment.
2
Low false positive rate: IAST tools have a low false positive rate because they are able to
distinguish between actual vulnerabilities and benign code.
3
Integration: IAST tools can be integrated into the development process, allowing developers to
incorporate security testing into their workflows.
4
Automation: IAST tools can be automated, allowing for continuous testing and faster feedback
on vulnerabilities.
5
Coverage: IAST tools can provide coverage for a wide range of security vulnerabilities,
including those that may be difficult to detect through other forms of testing.
6
IAST Tool
Description
Contrast
Security
an IAST tool that automatically identifies and tracks vulnerabilities in real-time during
the software development process. It can be integrated into a CI/CD pipeline to
provide continuous monitoring and protection.
Hdiv Security
an IAST solution that detects and prevents attacks by monitoring the runtime
behavior of applications. It provides detailed insights into vulnerabilities and
generates reports for developers and security teams.
RIPS
Technologies
a security testing tool that combines IAST with SAST (Static Application Security
Testing) to provide comprehensive security analysis of web applications. It supports
multiple programming languages and frameworks.
Acunetix
a web application security tool that offers IAST capabilities for detecting
vulnerabilities in real-time. It provides detailed reports and integrates with CI/CD
pipelines to automate the security testing process.
AppSecEngineer
an open-source IAST tool for detecting and preventing security vulnerabilities in web
applications. It integrates with popular web frameworks such as Spring, Django, and
Ruby on Rails, and provides detailed reports of vulnerabilities and attack attempts.
an example of a CI/CD pipeline with IAST using Contrast Security:
stages:
  - build
  - test
  - iast
  - deploy
build:
  stage: build
  script:
    - mvn clean package
test:
  stage: test
  script:
    - mvn test
In this pipeline, the IAST stage is added after the test stage. The script in the IAST stage starts the
Contrast Security agent using the Java command with the -javaagent  option, and then starts the
application using the jar  command. The agent will monitor the application for security
vulnerabilities and provide real-time feedback.
Note that this is just an example pipeline and it can be customized according to your needs. Also,
make sure to configure the IAST tool properly and follow best practices for secure development
and deployment.
Copyright © 2019-2023 HADESS.
iast:
  stage: iast
  image: contrastsecurity/contrast-agent
  script:
    - java -javaagent:/opt/contrast/contrast.jar -jar target/myapp.jar
  allow_failure: true
deploy:
  stage: deploy
  script:
    - mvn deploy
  only:
    - master
DevSecOps Guides
Build & Test / Smoke Test
Smoke tests are typically conducted on a small subset of the application’s functionality, and are
designed to be quick and easy to execute. They may include basic checks such as verifying that
the application can be launched, that key features are functional, and that data is being processed
correctly. If the smoke test passes, the application can be considered ready for further testing.
Example commands for performing smoke tests in DevSecOps:
Use tools like cURL or HTTPie to make HTTP requests to the application’s endpoints and verify
that they return the expected responses.
For example, you might run a command like curl http://localhost:8080/api/health  to check the
health of the application.
Use SQL queries to verify that the application is correctly reading from and writing to the
database.
For example, you might run a command like mysql -u user -p password -e "SELECT * FROM users
WHERE id=1"  to verify that a user with ID 1 exists in the database.
Use testing frameworks like Selenium or Puppeteer to automate browser-based tests and
verify that the application’s UI is working correctly.
For example, you might create a script using Puppeteer that logs in to the application and
verifies that the user profile page is displayed correctly.
Smoke Test
HTTP requests:
•
•
Database queries:
•
•
Scripted tests:
•
•
Unit tests:
Use unit testing frameworks like JUnit or NUnit to test individual functions and methods in the
application.
For example, you might run a command like mvn test  to run all of the unit tests in a Java
application.
Copyright © 2019-2023 HADESS.
•
•
DevSecOps Guides
Production / Cloud Scanning
Cloud scanning in production DevSecOps refers to the process of continuously scanning the
production environment of an application deployed on cloud infrastructure for potential security
vulnerabilities and threats. This is done to ensure that the application remains secure and
compliant with security policies and standards even after it has been deployed to the cloud.
Cloud scanning tools can perform a variety of security scans on the production environment,
including vulnerability scanning, penetration testing, and compliance auditing. These tools can
help to identify security issues in real-time and provide alerts and notifications to the security
team.
Some of the benefits of cloud scanning in production DevSecOps include:
A tool that analyzes the behavior and configuration of AWS resources for potential security issues.
Cloud Scanning
Real-time security monitoring: Cloud scanning enables security teams to monitor the
production environment in real-time, providing early detection and response to potential
security threats.
1
Automated security checks: Cloud scanning tools can be integrated into the DevOps pipeline
to perform automated security checks on the production environment, enabling teams to
catch security issues early in the development cycle.
2
Improved compliance: Cloud scanning tools can help to ensure that the application remains
compliant with industry standards and regulations by continuously monitoring the production
environment for compliance violations.
3
Reduced risk: Cloud scanning can help to reduce the risk of security breaches and other
security incidents by detecting and addressing potential vulnerabilities in the production
environment.
4
AWS Inspector
A tool that provides threat protection across all of your services and deploys quickly with no
infrastructure to manage.
A tool that scans your App Engine app for common web vulnerabilities.
A tool that provides visibility, security, and compliance across your entire cloud infrastructure.
Copyright © 2019-2023 HADESS.
aws inspector start-assessment-run --assessment-template-arn arn:aws:inspector:us-west-2:12345678
Azure Security Center
az security assessment create --location westus --name "Example Assessment" --resource-group "MyR
Google Cloud Security Scanner
gcloud beta app deploy --no-promote --version staging<br>gcloud beta app gen-config --custom<br>g
CloudPassage Halo
curl -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -X POST https://api.cl
DevSecOps Guides
Production / Infrastructure Scanning
Infrastructure scanning in production DevSecOps refers to the process of continuously scanning
the underlying infrastructure of an application deployed on cloud infrastructure for potential
security vulnerabilities and threats. This is done to ensure that the infrastructure remains secure
and compliant with security policies and standards even after it has been deployed to the cloud.
A tool that scans your network for vulnerabilities and provides detailed reports.
An open-source vulnerability scanner that provides detailed reports and supports a wide range of
platforms.
A cloud-based security and compliance tool that provides continuous monitoring and detailed
reporting.
A Linux distro for intrusion detection, network security monitoring, and log management.
Infrastructure Scanning
Nessus
nessuscli scan new --policy "Basic Network Scan" --target "192.168.1.1"
OpenVAS
omp -u admin -w password -G "Full and fast" -T 192.168.1.1
Qualys
curl -H "X-Requested-With: Curl" -u "username:password" "https://qualysapi.qualys.com/api/2.0/fo/
Security Onion
A tool for auditing security on Unix-based systems that performs a system scan and provides
detailed reports.
A fast and customizable vulnerability scanner that supports a wide range of platforms and
technologies.
A collection of templates for Nuclei that cover a wide range of vulnerabilities and
misconfigurations.
A combination of Nuclei and Burp Suite that allows you to quickly scan and identify vulnerabilities
in web applications.
A combination of Nuclei and Masscan that allows you to quickly scan large IP ranges and identify
vulnerabilities.
sudo so-import-pcap -r 2022-01-01 -c example.pcap
Lynis
sudo lynis audit system
Nuclei
nuclei -u http://example.com -t cves/CVE-2021-1234.yaml
Nuclei Templates
nuclei -u http://example.com -t cves/ -max-time 5m
Nuclei with Burp Suite
nuclei -t web-vulns -target http://example.com -proxy http://localhost:8080
Nuclei with Masscan
masscan -p1-65535 192.168.1.1-254 -oL ips.txt && cat ips.txt
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Production / Secret Management
Secret management refers to the process of securely storing, managing, and accessing sensitive
information, such as passwords, API keys, and other credentials. Secrets are a critical component
of modern applications, and their secure management is essential to ensure the security and
integrity of the application.
Secret management typically involves the use of specialized tools and technologies that provide a
secure and centralized location for storing and managing secrets. These tools often use strong
encryption and access control mechanisms to protect sensitive information from unauthorized
access.
Some of the key features of secret management tools include:
A highly secure and scalable secret management solution that supports a wide range of
authentication methods and storage backends.
Secret Management
Secure storage: Secret management tools provide a secure location for storing sensitive
information, typically using strong encryption and access control mechanisms to ensure that
only authorized users can access the information.
1
Access control: Secret management tools allow administrators to define access control
policies and roles that govern who can access specific secrets and what actions they can
perform.
2
Auditing and monitoring: Secret management tools provide auditing and monitoring
capabilities that allow administrators to track who accessed specific secrets and when,
providing an audit trail for compliance and security purposes.
3
Integration with other tools: Secret management tools can be integrated with other DevOps
tools, such as build servers, deployment tools, and orchestration frameworks, to provide
seamless access to secrets during the application lifecycle.
4
Hashicorp Vault
A fully managed secrets management service provided by Amazon Web Services.
A cloud-based secrets management service provided by Microsoft Azure.
A command-line tool that allows you to encrypt files and directories within a Git repository.
A command-line tool that allows you to store and manage secrets in Git repositories using GPG
encryption.
Copyright © 2019-2023 HADESS.
vault kv put secret/myapp/config username="admin" password="s3cret" API_key="123456789"
AWS Secrets Manager
aws secretsmanager create-secret --name myapp/database --secret-string '{"username":"admin","pass
Azure Key Vault
az keyvault secret set --name myapp/config --value s3cret
Git-crypt
git-crypt init && git-crypt add-gpg-user user@example.com
Blackbox
blackbox_initialize && blackbox_register_new_file secrets.txt
DevSecOps Guides
Production / Threat Intelligence
Threat intelligence is the process of gathering and analyzing information about potential and
existing cybersecurity threats, such as malware, phishing attacks, and data breaches. The goal of
threat intelligence is to provide organizations with actionable insights that can help them identify
and mitigate potential security risks before they can cause harm.
In the context of DevSecOps, threat intelligence is an important component of a comprehensive
security strategy. By gathering and analyzing information about potential security threats,
organizations can better understand the security risks that they face and take steps to mitigate
them. This can include implementing security controls and countermeasures, such as firewalls,
intrusion detection systems, and security information and event management (SIEM) systems, to
protect against known threats.
Threat intelligence can also be used to enhance other DevSecOps practices, such as vulnerability
management and incident response. By identifying potential vulnerabilities and threats in real-
time, security teams can take swift action to remediate issues and prevent security incidents from
occurring.
Some of the key benefits of threat intelligence in DevSecOps include:
Threat Intelligence
Improved threat detection: Threat intelligence provides organizations with the information they
need to detect potential security threats before they can cause harm.
1
Better decision-making: By providing actionable insights, threat intelligence helps
organizations make informed decisions about their security posture and response to potential
threats.
2
Proactive threat mitigation: Threat intelligence enables organizations to take a proactive
approach to threat mitigation, allowing them to stay ahead of emerging threats and reduce
their risk of being compromised.
3
Enhanced incident response: Threat intelligence can be used to enhance incident response,
allowing organizations to quickly and effectively respond to security incidents and minimize
4
A search engine for internet-connected devices that allows you to identify potential attack
surfaces and vulnerabilities in your network.
A threat intelligence platform that allows you to analyze files and URLs for potential threats and
malware.
A threat intelligence platform that allows you to collect, analyze, and share threat intelligence with
your team and community.
An open-source threat intelligence platform that allows you to collect, store, and share threat
intelligence with your team and community.
Copyright © 2019-2023 HADESS.
their impact.
Shodan
shodan scan submit --filename scan.json "port:22"
VirusTotal
curl --request POST --url 'https://www.virustotal.com/api/v3/urls' --header 'x-apikey: YOUR_API_K
ThreatConnect
curl -H "Content-Type: application/json" -X POST -d '{"name": "Example Threat Intel", "descriptio
MISP
curl -X POST 'http://misp.local/events/restSearch' -H 'Authorization: YOUR_API_KEY' -H 'Content-T
DevSecOps Guides
Production / Vulnerability Assessment
Vulnerability assessment is the process of identifying and quantifying security vulnerabilities in an
organization’s IT systems, applications, and infrastructure. The goal of vulnerability assessment is
to provide organizations with a comprehensive view of their security posture, allowing them to
identify and prioritize security risks and take steps to remediate them.
In the context of DevSecOps, vulnerability assessment is a critical component of a comprehensive
security strategy. By regularly scanning for vulnerabilities and identifying potential security risks,
organizations can take proactive steps to secure their applications and infrastructure.
Some of the key benefits of vulnerability assessment in DevSecOps include:
There are a variety of vulnerability assessment tools and technologies available that can be used
in DevSecOps, including both commercial and open-source solutions. Some popular vulnerability
assessment tools include Nessus, Qualys, and OpenVAS.
Best practices for vulnerability assessment:
Vulnerability Assessment
Early detection of vulnerabilities: By regularly scanning for vulnerabilities, organizations can
detect potential security risks early on, allowing them to take swift action to remediate them.
1
Improved risk management: Vulnerability assessments provide organizations with a
comprehensive view of their security posture, allowing them to identify and prioritize security
risks and take steps to mitigate them.
2
Compliance: Many regulatory requirements, such as PCI DSS and HIPAA, require regular
vulnerability assessments as part of their compliance standards.
3
Integration with other DevSecOps practices: Vulnerability assessment can be integrated with
other DevSecOps practices, such as continuous integration and continuous deployment, to
ensure that security is built into the application development lifecycle.
4
A vulnerability scanner that allows you to identify vulnerabilities and misconfigurations in your
network and infrastructure.
An open-source vulnerability scanner that allows you to identify vulnerabilities and
misconfigurations in your network and infrastructure.
A network exploration and vulnerability scanner that allows you to identify open ports and
potential vulnerabilities in your network.
A cloud-based vulnerability management platform that allows you to identify vulnerabilities and
misconfigurations in your network and infrastructure.
Conduct regular vulnerability assessments to identify potential weaknesses and
misconfigurations in your network and infrastructure.
1
Use a combination of automated and manual vulnerability scanning techniques to ensure
comprehensive coverage.
2
Prioritize and remediate vulnerabilities based on their severity and potential impact on your
organization.
3
Regularly update and patch software and systems to address known vulnerabilities.
4
Use segmentation and isolation to limit the spread of attacks in case of a successful breach.
5
Nessus
nessuscli scan new -n "My Scan" -t "192.168.1.0/24" -T "Basic Network Scan"
OpenVAS
omp -u admin -w password -h localhost -p 9390 -G
Nmap
nmap -sS -A -p1-65535 target.com
Qualys
curl -H 'X-Requested-With: Curl Sample' -u "USERNAME:PASSWORD" -H 'Accept: application/json' -H '
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Operate / Monitoring
Monitoring in DevSecOps refers to the practice of continuously observing and analyzing an
organization’s IT systems, applications, and infrastructure to identify potential security issues,
detect and respond to security incidents, and ensure compliance with security policies and
regulations.
In DevSecOps, monitoring is a critical component of a comprehensive security strategy, allowing
organizations to identify and respond to security threats quickly and effectively. Some of the key
benefits of monitoring in DevSecOps include:
There are a variety of monitoring tools and technologies available that can be used in DevSecOps,
including log analysis tools, network monitoring tools, and security information and event
management (SIEM) solutions. These tools can be integrated with other DevSecOps practices,
such as continuous integration and continuous deployment, to ensure that security is built into the
application development lifecycle.
Monitoring
Early detection of security incidents: By continuously monitoring systems and applications,
organizations can detect security incidents early on and take immediate action to remediate
them.
1
Improved incident response: With real-time monitoring and analysis, organizations can
respond to security incidents quickly and effectively, minimizing the impact of a potential
breach.
2
Improved compliance: By monitoring systems and applications for compliance with security
policies and regulations, organizations can ensure that they are meeting their security
obligations.
3
Improved visibility: Monitoring provides organizations with greater visibility into their IT
systems and applications, allowing them to identify potential security risks and take proactive
steps to address them.
4
Start the Prometheus server:
Check Prometheus server status:
Query data using PromQL:
Add Prometheus data source:
Configure Nagios server:
Verify Nagios server configuration:
Configure Zabbix agent on the server: Edit the Zabbix agent configuration file
/etc/zabbix/zabbix_agentd.conf to specify the Zabbix server IP address and hostname, and to
enable monitoring of system resources such as CPU, memory, disk usage, and network interface.
Example configuration:
Prometheus
$ ./prometheus --config.file=prometheus.yml
$ curl http://localhost:9090/-/healthy
http://localhost:9090/graph?g0.range_input=1h&g0.expr=up&g0.tab=0
Grafana
http://localhost:3000/datasources/new?gettingstarted
Nagios
/etc/nagios3/conf.d/
$ sudo /usr/sbin/nagios3 -v /etc/nagios3/nagios.cfg
Zabbix
Configure Zabbix server: Login to the Zabbix web interface and navigate to the “Configuration”
tab. Create a new host with the same hostname as the server being monitored, and specify the IP
address and Zabbix agent port. Add items to the host to monitor the system resources specified
in the Zabbix agent configuration file. Example items:
CPU usage: system.cpu.util[,idle]
Memory usage: vm.memory.size[available]
Disk usage: vfs.fs.size[/,pfree]
Network inbound traffic: net.if.in[eth0]
Network outbound traffic: net.if.out[eth0]
Configure triggers: Set up triggers to alert when any monitored item exceeds a certain threshold.
For example, set a trigger on the CPU usage item to alert when the usage exceeds 80%.
Configure actions: Create actions to notify relevant stakeholders when a trigger is fired. For
example, send an email to the web application team and the system administrators.
Edit the Datadog agent configuration file /etc/datadog-agent/datadog.yaml  and add the following
lines:
Server=192.168.1.100
ServerActive=192.168.1.100
Hostname=web-server
EnableRemoteCommands=1
UnsafeUserParameters=1
# Monitor system resources
UserParameter=cpu.usage[*],/usr/bin/mpstat 1 1 | awk '/Average:/ {print 100-$NF}'
UserParameter=memory.usage,free | awk '/Mem:/ {print $3/$2 * 100.0}'
UserParameter=disk.usage[*],df -h | awk '$1 == $1 {print int($5)}'
UserParameter=network.in[*],cat /proc/net/dev | grep $1 | awk '{print $2}'
UserParameter=network.out[*],cat /proc/net/dev | grep $1 | awk '{print $10}'
•
•
•
•
•
Datadog
# Collect CPU metrics
procfs_path: /proc
cpu_acct: true
To view CPU and memory metrics, go to the Datadog Metrics Explorer and search for the metrics
system.cpu.usage  and system.mem.used .
Here are some sample commands you can use to collect CPU and memory metrics with Datadog:
To collect CPU metrics:
To collect memory metrics:
# Collect memory metrics
meminfo_path: /proc/meminfo
curl -X POST -H "Content-type: application/json" -d '{
    "series": [
        {
            "metric": "system.cpu.usage",
            "points": [
                [
                    '"$(date +%s)"',
                    "$(top -bn1 | grep '%Cpu(s)' | awk '{print $2 + $4}')"
                ]
            ],
            "host": "my-host.example.com",
            "tags": ["environment:production"]
        }
    ]
}' "https://api.datadoghq.com/api/v1/series?api_key=<YOUR_API_KEY>"
curl -X POST -H "Content-type: application/json" -d '{
    "series": [
        {
            "metric": "system.mem.used",
            "points": [
                [
                    '"$(date +%s)"',
                    "$(free -m | awk '/Mem:/ {print $3}')"
                ]
            ],
Note that these commands assume that you have the necessary tools ( top , free ) installed on
your system to collect CPU and memory metrics. You can customize the metric , host , and tags
fields as needed to match your setup.
To install the New Relic Infrastructure agent on a Ubuntu server:
To install the New Relic Infrastructure agent on a CentOS/RHEL server:
To view CPU and memory metrics for a specific server using the New Relic API:
1- To install the CloudWatch agent on Linux, you can use the following commands:
            "host": "my-host.example.com",
            "tags": ["environment:production"]
        }
    ]
}' "https://api.datadoghq.com/api/v1/series?api_key=<YOUR_API_KEY>"
New Relic
curl -Ls https://download.newrelic.com/infrastructure_agent/linux/apt | sudo bash
sudo apt-get install newrelic-infra
sudo systemctl start newrelic-infra
curl -Ls https://download.newrelic.com/infrastructure_agent/linux/yum/el/7/x86_64/newrelic-infra.
sudo yum -y install newrelic-infra
sudo systemctl start newrelic-infra
curl -X GET 'https://api.newrelic.com/v2/servers/{SERVER_ID}/metrics/data.json' \
     -H 'X-Api-Key:{API_KEY}' \
     -i \
     -d 'names[]=System/CPU/Utilization&values[]=average_percentage' \
     -d 'names[]=System/Memory/Used/Bytes&values[]=average_value' \
     -d 'from=2022-05-01T00:00:00+00:00&to=2022-05-10T00:00:00+00:00'
AWS CloudWatch
2- Configure the CloudWatch Agent to Collect Metrics
On Linux, you can create a configuration file at /opt/aws/amazon-cloudwatch-agent/etc/amazon-
cloudwatch-agent.json  with the following content:
curl https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-
sudo rpm -i amazon-cloudwatch-agent.rpm
{
    "metrics": {
        "namespace": "CWAgent",
        "metricInterval": 60,
        "append_dimensions": {
            "InstanceId": "${aws:InstanceId}"
        },
        "metrics_collected": {
            "cpu": {
                "measurement": [
                    "cpu_usage_idle",
                    "cpu_usage_iowait",
                    "cpu_usage_user",
                    "cpu_usage_system"
                ],
                "metrics_collection_interval": 60,
                "totalcpu": false
            },
            "memory": {
                "measurement": [
                    "mem_used_percent"
                ],
                "metrics_collection_interval": 60
            }
        }
    }
}
On Windows, you can use the CloudWatch Agent Configuration Wizard to create a configuration
file with the following settings:
3- Start the CloudWatch Agent Once you’ve configured the CloudWatch agent, you can start it on
the EC2 instance using the following commands:
4- View the Metrics in CloudWatch
After a few minutes, the CloudWatch agent will start collecting CPU and memory metrics from the
EC2 instance. You can view these metrics in the CloudWatch console by following these steps:
Go to the CloudWatch console and select “Metrics” from the left-hand menu
Under “AWS Namespaces”, select “CWAgent”
You should see a list of metrics for the EC2 instance you are monitoring, including CPU and
memory usage. You can select individual metrics to view graphs and set up alarms based on
these metrics.
1- Configure the agent to collect CPU and memory metrics by adding the following settings to the
agent’s configuration file:
- Choose "AWS::EC2::Instance" as the resource type to monitor
- Choose "Performance counters" as the log type
- Select the following counters to monitor:
  - Processor Information -> % Processor Time
  - Memory -> % Committed Bytes In Use
- Set the metric granularity to 1 minute
- Choose "CWAgent" as the metric namespace
- Choose "InstanceId" as the metric dimension
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -
sudo service amazon-cloudwatch-agent start
•
•
•
Azure Monitor
    {
      "metrics": {
        "performance": {
2- Restart the Azure Monitor agent to apply the new configuration.
3- Select the virtual machine or server that you want to view metrics for. 4- Select the CPU and
memory metrics that you want to view. 5- Configure any alerts or notifications that you want to
receive based on these metrics.
To collect CPU and memory metrics using Azure Monitor, you can also use the Azure Monitor
REST API or the Azure CLI. Here’s an example Azure CLI command to collect CPU and memory
metrics:
This command retrieves CPU and memory metrics for a specific resource (identified by
{resource_id} ) over a one-day period (from May 20, 2022 to May 21, 2022), with a one-minute
interval. You can modify the parameters to retrieve different metrics or time ranges as needed.
          "collectionFrequencyInSeconds": 60,
          "metrics": [
            {
              "name": "\\Processor(_Total)\\% Processor Time",
              "category": "Processor",
              "counter": "% Processor Time",
              "instance": "_Total"
            },
            {
              "name": "\\Memory\\Available Bytes",
              "category": "Memory",
              "counter": "Available Bytes",
              "instance": null
            }
          ]
        }
      }
    }
az monitor metrics list --resource {resource_id} --metric-names "\Processor(_Total)\% Processor T
Google Cloud Monitoring
1- Install the Stackdriver agent on the GCE instance. You can do this using the following
command:
2- Verify that the Monitoring Agent is running by checking its service status:
3- In the Google Cloud Console, go to Monitoring > Metrics Explorer and select the CPU usage
metric under the Compute Engine VM Instance  resource type. Set the aggregation to mean  and select
the GCE instance that you created and Click Create  chart to view the CPU usage metric for your
instance.
4- To collect memory metrics, repeat step 5 but select the Memory usage  metric instead of CPU
usage .
1- In the Netdata web interface, go to the “Dashboard” section and select the “system.cpu” chart
to view CPU usage metrics. You can also select the “system.ram” chart to view memory usage
metrics.
2- To reduce failover using machine learning, you can configure Netdata’s anomaly detection
feature. In the Netdata web interface, go to the “Anomaly Detection” section and select “Add
alarm”.
3- For the “Detect” field, select “cpu.system”. This will detect anomalies in the system CPU usage.
4- For the “Severity” field, select “Warning”. This will trigger a warning when an anomaly is
detected.
5- For the “Action” field, select “Notify”. This will send a notification when an anomaly is detected.
6- You can also configure Netdata’s predictive analytics feature to predict when a system will fail.
In the Netdata web interface, go to the “Predict” section and select “Add algorithm”.
7- For the “Algorithm” field, select “Autoregression”. This will use autoregression to predict system
behavior.
curl -sSO https://dl.google.com/cloudagents/install-monitoring-agent.sh
sudo bash install-monitoring-agent.sh
sudo service stackdriver-agent status
Netdata
8- For the “Target” field, select “cpu.system”. This will predict CPU usage.
9- For the “Window” field, select “30 minutes”. This will use a 30-minute window to make
predictions.
10-Finally, click “Create” to create the algorithm.
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Operate / Virtual Patching
Virtual patching is a security technique used in DevSecOps to provide temporary protection
against known vulnerabilities in software applications or systems. Virtual patching involves the use
of security policies, rules, or filters that are applied to network traffic, system logs, or application
code to prevent known vulnerabilities from being exploited.
Virtual patching can be used when a vendor-provided patch is not available or when patching is
not feasible due to operational constraints or business needs. It allows organizations to quickly
and easily protect their systems against known vulnerabilities without having to take the
application or system offline or make changes to the underlying code.
Some of the key benefits of virtual patching in DevSecOps include:
Virtual patching can be implemented using a variety of techniques, including intrusion prevention
systems (IPS), web application firewalls (WAF), and network-based security devices. It can also
be implemented through the use of automated security policies or scripts that are applied to
systems and applications.
Virtual Patching
Reduced risk of exploitation: By applying virtual patches to known vulnerabilities, organizations
can reduce the risk of these vulnerabilities being exploited by attackers.
1
Improved security posture: Virtual patching allows organizations to quickly and easily protect
their systems against known vulnerabilities, improving their overall security posture.
2
Reduced downtime: Virtual patching can be implemented quickly and easily, without requiring
system downtime or disrupting business operations.
3
Improved compliance: Virtual patching can help organizations meet regulatory requirements
for timely patching of known vulnerabilities.
4
Log Collection
Splunk
1- Configure Data Inputs: Configure data inputs to receive data from various sources, such as
network devices, servers, and applications. Configure data inputs for the following:
Syslog
Windows Event Logs
Network Traffic (using the Splunk Stream add-on)
Cloud Platform Logs (e.g., AWS CloudTrail, Azure Audit Logs)
2- Create Indexes: Create indexes to store the data from the configured data inputs. Indexes can
be created based on data types, such as security events, network traffic, or application logs.
3- Create a Dashboard: Create a dashboard to visualize the data collected from the data inputs. A
dashboard can display the following:
Real-time events and alerts
Trending graphs and charts
Security reports and metrics
4- Create a Sample Rule for Detection: Create a sample rule to detect an attack or security
incident. For example, create a rule to detect failed login attempts to a web application. The
following steps show how to create the rule in Splunk:
Create a search query: Create a search query to identify failed login attempts in the web
application logs. For example:
Virtual patching is a security mechanism that helps protect applications and systems from known
vulnerabilities while developers work on creating and testing a patch to fix the vulnerability. It
involves implementing a temporary, software-based solution that can block or mitigate the attack
vectors that could be used to exploit the vulnerability. This is done by creating rules or policies
within security software, such as web application firewalls or intrusion detection/prevention
systems, that block or alert on malicious traffic attempting to exploit the vulnerability.
Virtual patching can be an effective way to quickly and temporarily secure systems against known
vulnerabilities, particularly those that may be actively targeted by attackers. It can also provide
time for organizations to test and implement permanent patches without leaving their systems
exposed to attacks.
•
•
•
•
•
•
•
•
sourcetype=apache_access combined=*login* status=401 | stats count by clientip
Virtual Patching
Name
Language
Java
Contrast Security, Sqreen, AppSealing, JShielder
.NET
Contrast Security, Sqreen, Nettitude, Antimalware-Research
Node.js
Sqreen, RASP.js, Jscrambler, nexploit
Python
RASP-Protect, PyArmor, Striker, nexploit
PHP
Sqreen, RIPS Technologies, RSAS, nexploit
Ruby
Sqreen, RASP-Ruby, nexploit
example RASP rule to mitigate SQL Injection vulnerability:
import javax.servlet.http.HttpServletRequest;
import com.rasp.scanner.RASP;
import com.rasp.scanner.ELExpression;
public class SQLInjectionRule {
  public static void checkSQLInjection(HttpServletRequest request) {
    // Get the input parameters from the request
    String username = request.getParameter("username");
    String password = request.getParameter("password");
    // Check for SQL injection in the username parameter
    if (RASP.isSQLInjection(username)) {
      // Log the attack attempt
      RASP.log("SQL injection detected in username parameter");
      // Block the request
      RASP.blockRequest("SQL injection detected");
    }
    // Check for SQL injection in the password parameter
    if (RASP.isSQLInjection(password)) {
      // Log the attack attempt
This rule checks for SQL injection attacks in the “username” and “password” parameters of a
HTTP request. If an attack is detected, the rule logs the attempt and blocks the request.
Cheatsheet for prevention rules for the OWASP Top 10 vulnerabilities
      RASP.log("SQL injection detected in password parameter");
      // Block the request
      RASP.blockRequest("SQL injection detected");
    }
  }
}
OWASP Type      Vulnerability                    Rule/Policy
Injection       SQL Injection                    /^[^']*$/i
                Command Injection                /^[^']*$/i
                LDAP Injection                   /^[^']*$/i
                XPath Injection                  /^[^']*$/i
                OS Command Injection             /^[^']*$/i
                Expression Language Injection    /^[^']*$/i
Broken          Broken Authentication            2FA or MFA implementation
Authentication  Password Management              Password complexity and expiry policy
                Brute Force Prevention           Account lockout policy
Sensitive Data  Sensitive Data Exposure           Encryption in transit and at rest
Exposure        Cross-Site Request Forgery (CSRF)CSRF tokens for all forms
                Broken Access Control            Role-based access control
Security        Security Misconfiguration        Regular security assessments and compliance chec
Misconfiguration
                Insecure Cryptographic Storage   Strong cryptographic algorithms and key manageme
                Insufficient Logging & Monitoring Log all security-relevant events
                Insufficient Attack Protection   Application firewall (WAF) to prevent OWASP Top
Cross-Site      Cross-Site Scripting (XSS)        Encoding user input
Scripting
                Insecure Direct Object References Access control checks and input validation
Insecure        Using Components with            Regular patching and updates
Components      Known Vulnerabilities
SQL Injection
RASP
when {
    event.type == "http" &&
    event.action == "param_value" &&
    http.param.name.matches("(?i).*((select|union|insert|update|delete|from|where|order by|group
} then {
    block();
    raise "SQL Injection detected in param: " + http.param.name;
}
WAF
SecRule ARGS "@rx ^[a-zA-Z0-9\s]+$" \
    "id:1,\
    phase:2,\
    t:none,\
    deny,\
    msg:'Possible SQL Injection Attack'"
Command Injection
when {
    event.type == "http" &&
    event.action == "param_value" &&
    http.param.name.matches("(?i).*((;|&|`|\\|\\||\\||&&).*)")
} then {
    block();
    raise "Command Injection detected in param: " + http.param.name;
}
RASP
SecRule ARGS "@rx ^[a-zA-Z0-9\s]+$" \
    "id:2,\
    phase:2,\
    t:none,\
    deny,\
    msg:'Possible Command Injection Attack'"
WAF
SecRule ARGS "@rx ^[a-zA-Z0-9\s]+$" \
    "id:2,\
    phase:2,\
    t:none,\
    deny,\
    msg:'Possible Command Injection Attack'"
XSS
RASP
when {
    event.type == "http" &&
    event.action == "param_value" &&
    http.param.value.matches("(?i).*((<script|<img|alert|prompt|document.cookie|window.location|o
} then {
    block();
    raise "XSS detected in param: " + http.param.name;
}
Copyright © 2019-2023 HADESS.
WAF
Script Tag Prevention Rule
SecRule ARGS|XML:/* "@rx <script.*?>" \
    "id:3,\
    phase:2,\
    t:none,\
    deny,\
    msg:'Possible XSS Attack via Script Tag'"
Attribute Injection Prevention Rule
SecRule ARGS|XML:/* "(<|&lt;)script[\s\S]+?=" \
    "id:4,\
    phase:2,\
    t:none,\
    deny,\
    msg:'Possible XSS Attack via Attribute Injection'"
DevSecOps Guides
MlSecOps / Model Robustness and Adversarial Attacks
Assessing and improving the robustness of machine learning models against adversarial attacks.
This involves testing models against various adversarial scenarios, developing defenses to
mitigate attacks (e.g., adversarial training), and understanding the limitations of model
robustness.
Copyright © 2019-2023 HADESS.
Model Robustness and Adversarial
Attacks
DevSecOps Guides
AiSecOps / Bias and Fairness
Addressing issues related to bias and fairness in AI systems. This includes identifying and
mitigating biases in training data, evaluating and measuring fairness metrics, and ensuring
equitable outcomes across different demographic groups or protected classes.
Copyright © 2019-2023 HADESS.
Bias and Fairness
DevSecOps Guides
Checklists / Apache
List of some best practices to harden Apache for DevSecOps
ID
Description
Commands
1
Disable directory
listing
Options -Indexes
2
Enable server
signature
ServerSignature On
3
Disable server
signature
ServerSignature Off
4
Change server
header
ServerTokens Prod
5
Disable server
header
ServerTokens Prod  and ServerSignature Off
6
Enable HTTPS
Install SSL certificate and configure Apache to use it
7
Disable HTTP
TRACE method
TraceEnable off
8
Set secure HTTP
response headers
Header always set X-XSS-Protection "1; mode=block"<br>Header
always set X-Content-Type-Options nosniff<br>Header always set
X-Frame-Options SAMEORIGIN<br>Header always set Content-
Security-Policy "default-src 'self'"
Apache Hardening for DevSecOps
TABLE OF CONTENTS
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Checklists / ArgoCD
List of some best practices to harden ArgoCD for DevSecOps
ArgoCD Hardening for DevSecOps
TABLE OF CONTENTS
Disable anonymous access to the ArgoCD API server
1
Enable HTTPS for ArgoCD server communication
2
Use a strong password for ArgoCD administrative users
3
Restrict access to ArgoCD API server by IP address
4
Enable RBAC for fine-grained access control to ArgoCD resources
5
Set secure cookie options for ArgoCD web UI
6
Use least privilege principle for ArgoCD API access
7
Regularly update ArgoCD to latest stable version
8
Regularly audit ArgoCD logs and access control
9
Implement backup and recovery plan for ArgoCD data
10
Disable anonymous access to the ArgoCD API server
argocd-server --disable-auth
Enable HTTPS for ArgoCD server communication
argocd-server --tls-cert-file /path/to/tls.crt --tls-private-key-file /path/to/tls.key
Use a strong password for ArgoCD administrative users
Modify argocd-server  configuration file to specify --client-ca-file  and --auth-mode cert  options
and create a certificate authority file and client certificate signed by the CA for each client host.
Create a dedicated ArgoCD service account with minimal necessary permissions.
argocd version --client  to check client version and argocd version --server  to check server
version. Use package manager or manual upgrade as needed.
argocd-server --loglevel debug  to enable debug level logging. Use a log analyzer or SIEM tool to
monitor logs for anomalies.
argocd-util export /path/to/export  to export ArgoCD data and configuration. Store backups
securely and test restoration procedure periodically.
Copyright © 2019-2023 HADESS.
argocd-server --admin-password <password>
Restrict access to ArgoCD API server by IP address
Enable RBAC for fine-grained access control to ArgoCD resources
argocd-server --rbac-policy-file /path/to/rbac.yaml
Set secure cookie options for ArgoCD web UI
argocd-server --secure-cookie
Use least privilege principle for ArgoCD API access
Regularly update ArgoCD to latest stable version
Regularly audit ArgoCD logs and access control
Implement backup and recovery plan for ArgoCD data
DevSecOps Guides
Checklists / Ceph
List of some best practices to harden Ceph for DevSecOps
ID
Description
Commands
1
Update Ceph to the
latest version
sudo apt-get update && sudo apt-get upgrade ceph -y
2
Enable SSL/TLS
encryption for Ceph
traffic
ceph config set global network.ssl true
3
Set secure file
permissions for Ceph
configuration files
sudo chmod 600 /etc/ceph/*
4
Limit access to the
Ceph dashboard
sudo ufw allow 8443/tcp && sudo ufw allow 8003/tcp && sudo
ufw allow 8080/tcp
5
Configure Ceph to use
firewall rules
sudo ceph config set global security firewall iptables
6
Implement network
segmentation for Ceph
nodes
sudo iptables -A INPUT -s <trusted network> -j ACCEPT
7
Configure Ceph to use
encrypted OSDs
sudo ceph-osd --mkfs --osd-uuid <osd-uuid> --cluster ceph
--osd-data <path to data directory> --osd-journal <path to
journal directory> --osd-encrypted
Ceph Hardening for DevSecOps
TABLE OF CONTENTS
ID
Description
Commands
8
Use SELinux or
AppArmor to restrict
Ceph processes
sudo setenforce 1  (for SELinux) or sudo aa-enforce
/etc/apparmor.d/usr.bin.ceph-osd  (for AppArmor)
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Checklists / Consul
List of some best practices to harden Consul for DevSecOps
systemctl edit consul.service  and add CPUQuota=50%  and MemoryLimit=512M
Consul Hardening for DevSecOps
TABLE OF CONTENTS
Enable TLS encryption for Consul communication
1
Restrict access to Consul API
2
Limit the resources allocated to Consul service
3
Disable unnecessary HTTP APIs
4
Enable and configure audit logging
5
Enable and configure health checks
6
Enable rate limiting to prevent DDoS attacks
7
Set up backup and recovery procedures for Consul data
8
Enable TLS encryption for Consul communication
consul agent -config-dir=/etc/consul.d -encrypt=<encryption-key> -ca-file=/path/to/ca.crt -cert-f
Restrict access to Consul API
consul acl bootstrap; consul acl policy create -name "secure-policy" -rules @secure-policy.hcl; c
Limit the resources allocated to Consul service
Copyright © 2019-2023 HADESS.
Disable unnecessary HTTP APIs
consul agent -disable-http-apis=stats
Enable and configure audit logging
consul agent -config-dir=/etc/consul.d -audit-log-path=/var/log/consul_audit.log
Enable and configure health checks
consul agent -config-dir=/etc/consul.d -enable-script-checks=true -script-check-interval=10s -scr
Enable rate limiting to prevent DDoS attacks
consul rate-limiting enable; consul rate-limiting config set -max-burst 1000 -rate 100
Set up backup and recovery procedures for Consul data
consul snapshot save /path/to/snapshot; consul snapshot restore /path/to/snapshot
DevSecOps Guides
Checklists / CouchDB
List of some best practices to harden CouchDB for DevSecOps
Edit the CouchDB configuration file local.ini  located at /opt/couchdb/etc/couchdb/ . Change the
line ; [admins] to [admins] , and add your admin username and password. Save and exit the file.
Restart CouchDB. Example command: sudo nano /opt/couchdb/etc/couchdb/local.ini
Change the owner and group of the CouchDB configuration directory /opt/couchdb/etc/couchdb/  to
the CouchDB user and group. Example command: sudo chown -R couchdb:couchdb
/opt/couchdb/etc/couchdb/
Create SSL/TLS certificates and configure CouchDB to use HTTPS. Example command for
creating self-signed certificates: sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout
/etc/ssl/private/couchdb.key -out /etc/ssl/certs/couchdb.crt
CouchDB Hardening for DevSecOps
TABLE OF CONTENTS
Disable admin party
1
Restrict access to configuration files
2
Use SSL/TLS encryption
3
Limit access to ports
4
Update CouchDB regularly
5
Disable admin party
Restrict access to configuration files
Use SSL/TLS encryption
Limit access to ports
Use a firewall to limit access to only the necessary ports. Example command using ufw : sudo ufw
allow from 192.168.1.0/24 to any port 5984
Install updates and security patches regularly to keep the system secure. Example command for
updating packages: sudo apt-get update && sudo apt-get upgrade
Copyright © 2019-2023 HADESS.
Update CouchDB regularly
DevSecOps Guides
Checklists / Docker
List of some best practices to harden Docker for DevSecOps
sudo chmod 660 /var/run/docker.sock
sudo chgrp docker /var/run/docker.sock
docker swarm init
docker network create –driver overlay my-network
Docker Hardening for DevSecOps
TABLE OF CONTENTS
Enable Docker Content Trust
1
Restrict communication with Docker daemon to local socket
2
Enable Docker Swarm Mode
3
Set up network security for Docker Swarm
4
Implement resource constraints on Docker containers
5
Use Docker Secrets to protect sensitive data
6
Limit access to Docker APIs
7
Rotate Docker TLS certificates regularly
8
Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1
Restrict communication with Docker daemon to local socket
Enable Docker Swarm Mode
Set up network security for Docker Swarm
Use a reverse proxy like NGINX or Apache to limit access to the Docker API endpoint
Copyright © 2019-2023 HADESS.
Implement resource constraints on Docker containers
docker run --cpu-quota=50000 --memory=512m my-image
Use Docker Secrets to protect sensitive data
docker secret create my-secret my-secret-data.txt
Limit access to Docker APIs
Rotate Docker TLS certificates regularly
dockerd --tlsverify --tlscacert=ca.pem --tlscert=server-cert.pem --tlskey=server-key.pem -H=0.0.0
DevSecOps Guides
Checklists / Elasticsearch
List of some best practices to harden Elasticsearch for DevSecOps
sudo nano /etc/elasticsearch/elasticsearch.yml
Set the following configurations:
script.inline: false
script.stored: false
script.engine: “groovy”
sudo nano /etc/elasticsearch/elasticsearch.yml  Add the following configuration:
http.enabled: true
http.cors.allow-origin: "/.*/" http.cors.enabled: true
http.cors.allow-methods: HEAD,GET,POST,PUT,DELETE,OPTIONS
http.cors.allow-headers: "X-Requested-With,Content-Type,Content-Length"
http.max_content_length: 100mb
sudo nano /etc/sysconfig/iptables
Add the following rules to only allow incoming connections from trusted IP addresses:
Elasticsearch Hardening for DevSecOps
TABLE OF CONTENTS
Disable dynamic scripting and disable inline scripts
1
Disable unused HTTP methods
2
Restrict access to Elasticsearch ports
3
Use a reverse proxy to secure Elasticsearch
4
Disable dynamic scripting and disable inline scripts
Disable unused HTTP methods
Restrict access to Elasticsearch ports
-A INPUT -p tcp -m tcp --dport 9200 -s 10.0.0.0/8 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 9200 -s 192.168.0.0/16 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 9200 -j DROP
Restart the iptables service to apply changes.
sudo service iptables restart
Set up a reverse proxy (e.g. Nginx, Apache) in front of Elasticsearch and configure SSL/TLS
encryption and authentication.
Copyright © 2019-2023 HADESS.
Use a reverse proxy to secure Elasticsearch
DevSecOps Guides
Checklists / Git
List of some best practices to harden Git for DevSecOps
gpg –edit-key and then use the passwd command to set a strong passphrase
Git Hardening for DevSecOps
TABLE OF CONTENTS
Enable GPG signature verification
1
Set a strong passphrase for GPG key
2
Use HTTPS instead of SSH for remote repositories
3
Enable two-factor authentication
4
Set Git to ignore file mode changes
5
Configure Git to use a credential helper
6
Use signed commits
7
Set Git to automatically prune stale remote-tracking branches
8
Set Git to always rebase instead of merge when pulling
9
Use Git’s ignore  feature to exclude sensitive files
10
Enable GPG signature verification
git config --global commit.gpgsign true
Set a strong passphrase for GPG key
Use HTTPS instead of SSH for remote repositories
git config --global url."https://".insteadOf git://
Enable it through the Git service provider’s website
git config --global credential.helper <helper>  where <helper>  is the name of the credential
helper (e.g., manager , store )
or
Add files or file patterns to the .gitignore  file
Copyright © 2019-2023 HADESS.
Enable two-factor authentication
Set Git to ignore file mode changes
git config --global core.fileMode false
Configure Git to use a credential helper
Use signed commits
git commit -S
 git config --global commit.gpgsign true
Set Git to automatically prune stale remote-tracking branches
git config --global fetch.prune true
Set Git to always rebase instead of merge when pulling
git config --global pull.rebase true
Use Git’s ignore  feature to exclude sensitive files
DevSecOps Guides
Checklists / Gitlab
List of some best practices to harden Gitlab for DevSecOps
Edit /etc/gitlab/gitlab.rb and add the following lines:
external_url ‘https://gitlab.example.com’
nginx[‘redirect_http_to_https’] = true
nginx[‘ssl_certificate’] = “/etc/gitlab/ssl/gitlab.example.com.crt”
nginx[‘ssl_certificate_key’] = “/etc/gitlab/ssl/gitlab.example.com.key”
gitlab_rails[‘gitlab_https’] = true
Gitlab Hardening for DevSecOps
TABLE OF CONTENTS
Update GitLab to the latest version
1
Enable SSL/TLS for GitLab
2
Disable GitLab sign up
3
Set a strong password policy
4
Limit the maximum file size
5
Enable two-factor authentication (2FA)
6
Enable audit logging
7
Configure GitLab backups
8
Restrict SSH access
9
Enable firewall rules
10
Update GitLab to the latest version
sudo apt-get update && sudo apt-get upgrade gitlab-ee
Enable SSL/TLS for GitLab
gitlab_rails[‘trusted_proxies’] = [‘192.168.1.1’] (replace 192.168.1.1 with the IP address of your
proxy)
Then run sudo gitlab-ctl reconfigure
Edit /etc/gitlab/gitlab.rb and add the following line:
gitlab_rails[‘gitlab_signup_enabled’] = false
Then run sudo gitlab-ctl reconfigure
Edit /etc/gitlab/gitlab.rb and add the following lines:
gitlab_rails[‘password_minimum_length’] = 12
gitlab_rails[‘password_complexity’] = 2
Then run sudo gitlab-ctl reconfigure
Edit /etc/gitlab/gitlab.rb and add the following line:
gitlab_rails[‘max_attachment_size’] = 10.megabytes
Then run sudo gitlab-ctl reconfigure
Go to GitLab’s web interface, click on your profile picture in the top-right corner, and select
“Settings”. Then select “Account” from the left-hand menu and follow the prompts to set up 2FA.
Edit /etc/gitlab/gitlab.rb and add the following line:
gitlab_rails[‘audit_events_enabled’] = true
Then run sudo gitlab-ctl reconfigure
Edit /etc/gitlab/gitlab.rb and add the following lines:
gitlab_rails[‘backup_keep_time’] = 604800
gitlab_rails[‘backup_archive_permissions’] = 0644
gitlab_rails[‘backup_pg_schema’] = ‘public’
gitlab_rails[‘backup_path’] = “/var/opt/gitlab/backups”
Then run sudo gitlab-ctl reconfigure
Disable GitLab sign up
Set a strong password policy
Limit the maximum file size
Enable two-factor authentication (2FA)
Enable audit logging
Configure GitLab backups
Edit /etc/gitlab/gitlab.rb and add the following line:
gitlab_rails[‘gitlab_shell_ssh_port’] = 22
Then run sudo gitlab-ctl reconfigure
Configure your firewall to only allow incoming traffic on ports that are necessary for GitLab to
function, such as 80, 443, and 22. Consult your firewall documentation for instructions on how to
configure the firewall rules.
Copyright © 2019-2023 HADESS.
Restrict SSH access
Enable firewall rules
DevSecOps Guides
Checklists / GlusterFS
List of some best practices to harden GlusterFS for DevSecOps
GlusterFS Hardening for DevSecOps
TABLE OF CONTENTS
Disable insecure management protocols
1
Enable SSL encryption for management
2
Limit access to trusted clients
3
Enable client-side SSL encryption
4
Enable authentication for client connections
5
Set proper permissions for GlusterFS files and directories
6
Disable root access to GlusterFS volumes
7
Enable TLS encryption for GlusterFS traffic
8
Monitor GlusterFS logs for security events
9
Disable insecure management protocols
gluster volume set <volname> network.remote-dio.disable on
Enable SSL encryption for management
gluster volume set <volname> network.remote.ssl-enabled on
Limit access to trusted clients
Copyright © 2019-2023 HADESS.
gluster volume set <volname> auth.allow <comma-separated list of trusted IPs>
Enable client-side SSL encryption
gluster volume set <volname> client.ssl on
Enable authentication for client connections
gluster volume set <volname> client.auth on
Set proper permissions for GlusterFS files and directories
chown -R root:glusterfs /etc/glusterfs /var/lib/glusterd /var/log/glusterfs
Disable root access to GlusterFS volumes
gluster volume set <volname> auth.reject-unauthorized on
Enable TLS encryption for GlusterFS traffic
gluster volume set <volname> transport-type
Monitor GlusterFS logs for security events
tail -f /var/log/glusterfs/glusterd.log
DevSecOps Guides
Checklists / Gradle
List of some best practices to harden Gradle for DevSecOps
Check the latest version on the official website: https://gradle.org/releases/, and then install it. For
example: wget https://services.gradle.org/distributions/gradle-7.0.2-bin.zip, unzip gradle-7.0.2-
bin.zip, and set the PATH environment variable to the Gradle bin directory.
You can disable the daemon by adding the following line to the gradle.properties file:
org.gradle.daemon=false. Alternatively, you can restrict the maximum amount of memory that can
be used by the daemon by setting the org.gradle.jvmargs property.
Add the following code to the build.gradle file to enforce using HTTPS for all repositories:
Gradle Hardening for DevSecOps
TABLE OF CONTENTS
Use the latest stable version of Gradle
1
Disable or restrict Gradle daemon
2
Configure Gradle to use HTTPS for all repositories
3
Use secure credentials for accessing repositories
4
Use plugins and dependencies from trusted sources only
5
Implement access controls for Gradle builds
6
Regularly update Gradle and plugins
7
Use the latest stable version of Gradle
Disable or restrict Gradle daemon
Configure Gradle to use HTTPS for all repositories
allprojects {
    repositories {
Use encrypted credentials in the build.gradle  file or environment variables for accessing
repositories.
Use plugins and dependencies from official sources, and avoid using those from unknown or
untrusted sources.
Implement access controls to ensure that only authorized users can execute or modify Gradle
builds.
Regularly update Gradle and its plugins to ensure that security vulnerabilities are fixed and new
features are added. Use the gradle wrapper  command to ensure that all team members use the
same version of Gradle.
Copyright © 2019-2023 HADESS.
        mavenCentral {
            url "https://repo1.maven.org/maven2/"
        }
        maven {
            url "https://plugins.gradle.org/m2/"
        }
    }
}
Use secure credentials for accessing repositories
Use plugins and dependencies from trusted sources only
Implement access controls for Gradle builds
Regularly update Gradle and plugins
DevSecOps Guides
Checklists / Graphite
List of some best practices to harden Graphite for DevSecOps
Graphite Hardening for DevSecOps
TABLE OF CONTENTS
Disable debug mode
1
Set a strong secret key for Django
2
Enable HTTPS
3
Restrict access to Graphite web interface
4
Restrict access to Graphite API
5
Disable unused Graphite components
6
Enable authentication for Graphite data ingestion
7
Enable Graphite logging
8
Monitor Graphite metrics
9
Keep Graphite up-to-date
10
Disable debug mode
sed -i 's/DEBUG = True/DEBUG = False/g' /opt/graphite/webapp/graphite/local_settings.py
Set a strong secret key for Django
sed -i "s/SECRET_KEY = 'UNSAFE_DEFAULT'/SECRET_KEY = 'your-strong-secret-key-here'/g" /opt/graphi
Enable HTTPS
Configure NGINX to require authentication or restrict access to specific IP addresses
Remove unused Carbon cache backends or Django apps to reduce attack surface
Configure Carbon to require authentication for incoming data
Configure Graphite to log access and error messages for easier troubleshooting
Use a monitoring tool like Prometheus or Nagios to monitor Graphite metrics and detect any
anomalies
Regularly update Graphite and its dependencies to address any known security vulnerabilities
Copyright © 2019-2023 HADESS.
Install a SSL certificate and configure NGINX to serve Graphite over HTTPS
Restrict access to Graphite web interface
Configure NGINX to require authentication or restrict access to specific IP addresses
Restrict access to Graphite API
Disable unused Graphite components
Enable authentication for Graphite data ingestion
Enable Graphite logging
Monitor Graphite metrics
Keep Graphite up-to-date
DevSecOps Guides
Checklists / IIS
List of some best practices to harden IIS for DevSecOps
ID
Description
Commands
1
Disable
directory
browsing
Set-WebConfigurationProperty -filter /system.webServer/directoryBrowse
"IIS:\Sites\Default Web Site" -name enabled -value $false
2
Remove
unneeded
HTTP headers
Remove-WebConfigurationProperty -filter
"system.webServer/httpProtocol/customHeaders" -name ."X-Powered-By"
3
Set secure
HTTP
response
headers
Add-WebConfigurationProperty -filter "system.webServer/staticContent" -
"clientCache.cacheControlMode" -value "UseMaxAge"<br>Set-WebConfiguratio
filter "system.webServer/staticContent/clientCache" -name "cacheControlM
value "365.00:00:00"<br>Add-WebConfigurationProperty -filter
"system.webServer/httpProtocol/customHeaders" -name "X-Content-Type-Opti
"nosniff"<br>Add-WebConfigurationProperty -filter
"system.webServer/httpProtocol/customHeaders" -name "X-Frame-Options" -v
"SAMEORIGIN"<br>Add-WebConfigurationProperty -filter
"system.webServer/httpProtocol/customHeaders" -name "X-XSS-Protection" -
mode=block"
4
Enable HTTPS
and configure
SSL/TLS
settings
New-WebBinding -Name "Default Web Site" -Protocol https -Port 443 -IPAd
SslFlags 1<br>Set-ItemProperty -Path IIS:\SslBindings\0.0.0.0!443 -Name
Value "1"<br>Set-WebConfigurationProperty -filter
"system.webServer/security/authentication/iisClientCertificateMappingAut
-name enabled -value $false<br>Set-WebConfigurationProperty -filter
"system.webServer/security/authentication/anonymousAuthentication" -name
value $false<br>Set-WebConfigurationProperty -filter
IIS Hardening for DevSecOps
TABLE OF CONTENTS
ID
Description
Commands
"system.webServer/security/authentication/basicAuthentication" -name ena
$false<br>Set-WebConfigurationProperty -filter
"system.webServer/security/authentication/digestAuthentication" -name en
$false<br>Set-WebConfigurationProperty -filter
"system.webServer/security/authentication/windowsAuthentication" -name e
value $true<br>Set-WebConfigurationProperty -filter
"system.webServer/security/authentication/windowsAuthentication" -name u
-value $true
5
Restrict
access to files
and
directories
Set-WebConfigurationProperty -filter
"/system.webServer/security/requestFiltering/fileExtensions" -name "." -
@{allowed="$false"}<br>Set-WebConfigurationProperty -filter
"/system.webServer/security/requestFiltering/hiddenSegments" -name "." -
@{allowed="$false"}<br>Set-WebConfigurationProperty -filter
"/system.webServer/security/requestFiltering/denyUrlSequences" -name "."
@{add="$false"}
6
Enable
logging and
configure log
settings
Set-WebConfigurationProperty -filter "/system.webServer/httpLogging" -n
value $false<br>  Set-WebConfigurationProperty -filter
“/system.webServer/httpLogging” -name logExtFileFlags -value “Date,
ClientIP, UserName, SiteName, ComputerName, ServerIP, Method, UriS
UriQuery, HttpStatus, Win32Status, BytesSent, BytesRecv, TimeTaken
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Checklists / Jenkins
List of some best practices to harden Jenkins for DevSecOps
Go to “Manage Jenkins” -> “Configure Global Security” and select “Enable security”
Go to “Manage Jenkins” -> “Configure Global Security” and select “Require secure connections”
Go to the project configuration -> “Configure” -> “Enable project-based security”
Jenkins Hardening for DevSecOps
TABLE OF CONTENTS
Enable security
1
Use secure connection
2
Restrict project access
3
Use plugins with caution
4
Limit user permissions
5
Use credentials securely
6
Regularly update Jenkins
7
Enable audit logging
8
Secure access to Jenkins server
9
Use Jenkins agent securely
10
Use build tools securely
11
Follow secure coding practices
12
Enable security
Use secure connection
Restrict project access
Install only necessary plugins from trusted sources and regularly update them
Assign minimal necessary permissions to each user or group
Store credentials in Jenkins credentials store and use them only where necessary
Keep Jenkins updated with the latest security patches and updates
Enable audit logging to track and investigate security incidents
Limit access to Jenkins server by configuring firewall rules and setting up VPN access
Use secure connections between Jenkins master and agents and limit access to agents
Use secure and updated build tools and avoid using system tools or commands directly in build
scripts
Follow secure coding practices to avoid introducing vulnerabilities in build scripts or plugins
Copyright © 2019-2023 HADESS.
Use plugins with caution
Limit user permissions
Use credentials securely
Regularly update Jenkins
Enable audit logging
Secure access to Jenkins server
Use Jenkins agent securely
Use build tools securely
Follow secure coding practices
DevSecOps Guides
Checklists / Kuberneties
List of some best practices to harden Kuberneties for DevSecOps
kubectl edit svc/kubernetes
Update spec.loadBalancerSourceRanges
Kuberneties Hardening for DevSecOps
TABLE OF CONTENTS
Restrict Kubernetes API access to specific IP ranges
1
Use Role-Based Access Control (RBAC)
2
Enable PodSecurityPolicy (PSP)
3
Use Network Policies
4
Enable Audit Logging
5
Use Secure Service Endpoints
6
Use Pod Security Context
7
Use Kubernetes Secrets
8
Enable Container Runtime Protection
9
Enable Admission Controllers
10
Restrict Kubernetes API access to specific IP ranges
Use Role-Based Access Control (RBAC)
kubectl create serviceaccount <name> <br> kubectl create clusterrolebinding <name> --clusterrole=
Enable PodSecurityPolicy (PSP)
kubectl create sa pod-sa
kubectl create rolebinding pod-sa --role=psp:vmxnet3 --serviceaccount=default:pod-sa
kubectl edit cm/kube-apiserver -n kube-system
Update --enable-admission-plugins
kubectl create serviceaccount psp-sa <br> kubectl create clusterrolebinding psp-binding --cluster
Use Network Policies
kubectl apply -f networkpolicy.yml
Enable Audit Logging
kubectl apply -f audit-policy.yaml <br> kubectl edit cm/kube-apiserver -n kube-system <br> Update
Use Secure Service Endpoints
kubectl patch svc <svc-name> -p '{"spec": {"publishNotReadyAddresses": true, "sessionAffinity": "
Use Pod Security Context
Use Kubernetes Secrets
kubectl create secret generic <name> --from-file=<path-to-file>
Enable Container Runtime Protection
kubectl apply -f falco.yaml
Enable Admission Controllers
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Checklists / Memcached
List of some best practices to harden Memcached for DevSecOps
sed -i 's/^#-S/-S/g' /etc/sysconfig/memcached
yum install cyrus-sasl-plain
htpasswd -c /etc/sasl2/memcached-sasldb username
chmod 600 /etc/sasl2/memcached-sasldb
Memcached Hardening for DevSecOps
TABLE OF CONTENTS
Disable UDP listener
1
Enable SASL authentication
2
Limit incoming traffic to known IP addresses
3
Limit maximum memory usage
4
Run as non-root user
5
Enable logging
6
Upgrade to the latest version
7
Disable unused flags
8
Disable UDP listener
sed -i 's/^-U 0/#-U 0/g' /etc/sysconfig/memcached
Enable SASL authentication
Limit incoming traffic to known IP addresses
sed -i 's/^logfile/#logfile/g' /etc/sysconfig/memcached
mkdir /var/log/memcached
touch /var/log/memcached/memcached.log
chown memcached:memcached /var/log/memcached/memcached.log
sed -i 's/^#logfile/LOGFILE="\/var\/log\/memcached\/memcached.log"/g' /etc/sysconfig/memcached
sed -i 's/^-I 1m/#-I 1m/g' /etc/sysconfig/memcached
sed -i 's/^-a 0765/#-a 0765/g' /etc/sysconfig/memcached
Copyright © 2019-2023 HADESS.
iptables -A INPUT -p tcp --dport 11211 -s 192.168.1.100 -j ACCEPT
Limit maximum memory usage
echo 'CACHESIZE="128"' > /etc/sysconfig/memcached
Run as non-root user
sed -i 's/^-u root/-u memcached/g' /etc/sysconfig/memcached
Enable logging
Upgrade to the latest version
yum update memcached
Disable unused flags
DevSecOps Guides
Checklists / MongoDB
List of some best practices to harden MongoDB for DevSecOps
MongoDB Hardening for DevSecOps
TABLE OF CONTENTS
Disable HTTP interface
1
Enable authentication
2
Set strong password for admin user
3
Disable unused network interfaces
4
Enable access control
5
Enable SSL/TLS encryption
6
Enable audit logging
7
Set appropriate file permissions
8
Disable unused MongoDB features
9
Enable firewalls and limit access to MongoDB ports
10
Disable HTTP interface
sed -i '/httpEnabled/ s/true/false/g' /etc/mongod.conf
Enable authentication
sed -i '/security:/a \ \ \ \ authorization: enabled' /etc/mongod.conf
Set strong password for admin user
mongo admin --eval "db.createUser({user: 'admin', pwd: 'new_password_here', roles: ['root']})"
Disable unused network interfaces
sed -i '/net:/a \ \ \ \ bindIp: 127.0.0.1' /etc/mongod.conf
Enable access control
sed -i '/security:/a \ \ \ \ authorization: enabled' /etc/mongod.conf
Enable SSL/TLS encryption
mongod --sslMode requireSSL --sslPEMKeyFile /path/to/ssl/key.pem --sslCAFile /path/to/ca/ca.pem -
Enable audit logging
sed -i '/systemLog:/a \ \ \ \ destination: file\n\ \ \ \ path: /var/log/mongodb/audit.log\n\ \ \
Set appropriate file permissions
chown -R mongodb:mongodb /var/log/mongodb<br>chmod -R go-rwx /var/log/mongodb
Disable unused MongoDB features
sed -i '/operationProfiling:/a \ \ \ \ mode: off' /etc/mongod.conf<br>sed -i '/setParameter:/a \
Enable firewalls and limit access to MongoDB ports
ufw allow from 192.168.1.0/24 to any port 27017 proto tcp<br>ufw enable
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Checklists / MySQL
List of some best practices to harden MySQL for DevSecOps
MySQL Hardening for DevSecOps
TABLE OF CONTENTS
Remove test database and anonymous user
1
Limit access to the root user
2
Enable the query cache
3
Disable remote root login
4
Enable SSL for secure connections
5
Remove test database and anonymous user
mysql -u root -p -e "DROP DATABASE IF EXISTS test; DELETE FROM mysql.user WHERE User=''; DELETE F
Limit access to the root user
mysql -u root -p -e "CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password'; GRANT ALL PRIVIL
Enable the query cache
mysql -u root -p -e "SET GLOBAL query_cache_size = 67108864; SET GLOBAL query_cache_type = ON;"
Disable remote root login
Edit /etc/mysql/mysql.conf.d/mysqld.cnf  and set bind-address  to the IP address of the MySQL
server, then restart MySQL: systemctl restart mysql
Edit /etc/mysql/mysql.conf.d/mysqld.cnf  and add the following lines: ssl-ca=/etc/mysql/certs/ca-
cert.pem
ssl-cert=/etc/mysql/certs/server-cert.pem ssl-key=/etc/mysql/certs/server-key.pem  Then
restart MySQL: systemctl restart mysql
Copyright © 2019-2023 HADESS.
Enable SSL for secure connections
DevSecOps Guides
Checklists / Nginx
List of some best practices to harden Nginx for DevSecOps
ID
Description
Commands
1
Disable server tokens
server_tokens off;
2
Set appropriate file permissions
chmod 640 /etc/nginx/nginx.conf  or chmod 440
/etc/nginx/nginx.conf  depending on your setup
3
Implement SSL/TLS with
appropriate ciphers and
protocols
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
4
Enable HSTS
add_header Strict-Transport-Security "max-
age=31536000; includeSubdomains; preload";
5
Set up HTTP/2
listen 443 ssl http2;
6
Restrict access to certain
directories
location /private/ { deny all; }
7
Disable unnecessary modules
Comment out or remove unused modules from
nginx.conf  file.
8
Implement rate limiting
limit_req_zone $binary_remote_addr
zone=mylimit:10m rate=10r/s;
9
Implement buffer overflow
protection
proxy_buffer_size 128k;
proxy_buffers 4 256k;
proxy_busy_buffers_size 256k;
Nginx Hardening for DevSecOps
TABLE OF CONTENTS
ID
Description
Commands
10
Implement XSS protection
add_header X-XSS-Protection "1; mode=block";
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Checklists / Redis
List of some best practices to harden Redis for DevSecOps
Set a password in the Redis configuration file ( redis.conf ) using the requirepass  directive. Restart
Redis service to apply changes.
Redis Hardening for DevSecOps
TABLE OF CONTENTS
Disable the CONFIG command
1
Disable the FLUSHDB and FLUSHALL commands
2
Enable authentication
3
Bind Redis to a specific IP address
4
Enable SSL/TLS encryption
5
Disable unused Redis modules
6
Set limits for memory and connections
7
Monitor Redis logs
8
Regularly update Redis
9
Disable the CONFIG command
redis-cli config set config-command " "
Disable the FLUSHDB and FLUSHALL commands
redis-cli config set stop-writes-on-bgsave-error yes
Enable authentication
Edit the bind  directive in the Redis configuration file to specify a specific IP address.
Edit the redis.conf  file to specify SSL/TLS options and certificate files. Restart Redis service to
apply changes.
Edit the redis.conf  file to disable modules that are not needed. Use the module-load  and module-
unload  directives to control modules.
Edit the maxmemory  and maxclients  directives in the redis.conf  file to set limits for Redis memory
and connections.
Regularly check Redis logs for suspicious activities and errors. Use a log analyzer tool to help
detect anomalies.
Keep Redis up-to-date with the latest security patches and updates. Monitor vendor security
advisories for any vulnerabilities that may affect Redis.
Copyright © 2019-2023 HADESS.
Bind Redis to a specific IP address
Enable SSL/TLS encryption
Disable unused Redis modules
Set limits for memory and connections
Monitor Redis logs
Regularly update Redis
DevSecOps Guides
Checklists / Squid
List of some best practices to harden Squid for DevSecOps
acl clients src 192.168.1.0/24
http_access allow clients
http_max_clients 50
Squid Hardening for DevSecOps
TABLE OF CONTENTS
Disable HTTP TRACE method
1
Limit maximum object size
2
Enable access logging
3
Limit client connections
4
Restrict allowed ports
5
Disable HTTP TRACE method
acl HTTP-methods method TRACE<br>http_access deny HTTP-methods
Limit maximum object size
maximum_object_size 1 MB
Enable access logging
access_log /var/log/squid/access.log
Limit client connections
acl Safe_ports port 80 443 8080
http_access deny !Safe_ports
Copyright © 2019-2023 HADESS.
Restrict allowed ports
DevSecOps Guides
Checklists / Tomcat
List of some best practices to harden Tomcat for DevSecOps
Modify server.xml  to remove the connectors not in use, e.g.:
Modify server.xml  to enable HTTPS and configure SSL/TLS, e.g.:
Tomcat Hardening for DevSecOps
TABLE OF CONTENTS
Disable unused connectors
1
Use secure HTTPS configuration
2
Disable version information in error pages
3
Use secure settings for Manager and Host Manager
4
Use secure settings for access to directories
5
Disable unused connectors
 <Connector port="8080" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443" />
Use secure HTTPS configuration
<Connector port="8443" protocol="HTTP/1.1" SSLEnabled="true"
           maxThreads="150" scheme="https" secure="true"
           clientAuth="false" sslProtocol="TLS"
           keystoreFile="/path/to/keystore"
           keystorePass="password" />
Modify server.xml  to add the following attribute to the <Host>  element:
Modify tomcat-users.xml  to add roles and users with the appropriate permissions, e.g.:
Modify context.xml  to add the following element to the <Context>  element:
Copyright © 2019-2023 HADESS.
Disable version information in error pages
errorReportValveClass="org.apache.catalina.valves.ErrorReportValve" showReport="false" showServer
Use secure settings for Manager and Host Manager
<role rolename="manager-gui"/>
<user username="tomcat" password="password" roles="manager-gui"/>
Use secure settings for access to directories
<Valve className="org.apache.catalina.valves.RemoteAddrValve" allow="127\.0\.0\.1|192\.168\.0\.\d
DevSecOps Guides
Checklists / Weblogic
List of some best practices to harden Weblogic for DevSecOps
ID
Description
Commands
1
Disable default
accounts and
passwords
wlst.sh $WL_HOME/common/tools/configureSecurity.py -
removeDefaultConfig
2
Use secure
administration
port
wlst.sh $WL_HOME/common/tools/configureSecurity.py -
securityModel=OPSS -defaultRealm -realmName=myrealm -
adminPortEnabled=true -adminPort=9002 -sslEnabled=true -
sslListenPort=9003
3
Enable secure
communications
between servers
wlst.sh $WL_HOME/common/tools/configureSSL.py -action=create -
identity keystore.jks -identity_pwd keystorepassword -trust
keystore.jks -trust_pwd keystorepassword -hostName
myhost.example.com -sslEnabledProtocols TLSv1.2 -enabledProtocols
TLSv1.2 -keystoreType JKS -server SSL
4
Enable secure
connections for
JDBC data
sources
wlst.sh $WL_HOME/common/tools/config/jdbc/SecureJDBCDataSource.py
-url jdbc:oracle:thin:@//mydb.example.com:1521/HR -name
myDataSource -user myuser -password mypassword -target myServer -
trustStore myTrustStore.jks -trustStorePassword
myTrustStorePassword -identityStore myIdentityStore.jks -
identityStorePassword myIdentityStorePassword
5
Restrict access
to WebLogic
console
Add <security-constraint>  and <login-config>  elements in
$DOMAIN_HOME/config/fmwconfig/system-jazn-data.xml  file
Weblogic Hardening for DevSecOps
TABLE OF CONTENTS
ID
Description
Commands
6
Enable Secure
Sockets Layer
(SSL) for Node
Manager
wlst.sh $WL_HOME/common/tools/configureNodeManager.py -
Dweblogic.management.server=http://myserver.example.com:7001 -
Dweblogic.management.username=myusername -
Dweblogic.management.password=mypassword -
Dweblogic.NodeManager.sslEnabled=true -
Dweblogic.NodeManager.sslHostnameVerificationIgnored=true -
Dweblogic.NodeManager.KeyStores=CustomIdentityAndJavaTrust
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Attacks / Application Attacks
Application Attacks
TABLE OF CONTENTS
Exposure of sensitive information
1
Insertion of Sensitive Information Into Sent Data
2
Cross-Site Request Forgery (CSRF)
3
Use of Hard-coded Password
4
Broken or Risky Crypto Algorithm
5
Risky Crypto Algorithm
6
Insufficient Entropy
7
XSS
8
SQL Injection
9
External Control of File Name or Path
10
Generation of Error Message Containing Sensitive Information
11
Unprotected storage of credentials
12
Trust Boundary Violation
13
Insufficiently Protected Credentials
14
Restriction of XML External Entity Reference
15
Vulnerable and Outdated Components
16
Improper Validation of Certificate with Host Mismatch
17
Improper Authentication
18
Session Fixation
19
Inclusion of Functionality from Untrusted Control
20
Download of Code Without Integrity Check
21
Deserialization of Untrusted Data
22
Insufficient Logging
23
Improper Output Neutralization for Logs
24
Exposure of sensitive information refers to the unintentional or unauthorized disclosure of
confidential or private data to individuals or systems that are not supposed to have access to it.
This can occur through various means, such as insecure storage, transmission, or handling of
sensitive data.
Sensitive information can include personally identifiable information (PII) like names, addresses,
social security numbers, financial data, login credentials, medical records, or any other data that,
if exposed, could lead to identity theft, financial loss, or other harmful consequences.
To prevent exposure of sensitive information, it is important to implement appropriate security
measures. Here are some preventive measures:
Omission of Security-relevant Information
25
Sensitive Information into Log File
26
Server-Side Request Forgery (SSRF)
27
Exposure of sensitive information
Data classification: Classify your data based on sensitivity and define access controls
accordingly. Identify and categorize sensitive information so that you can apply stronger
security measures to protect it.
1
Secure storage: Use secure storage mechanisms to protect sensitive data, such as encryption,
hashing, or tokenization. Ensure that data is stored in a secure environment, whether it’s in
databases, file systems, or other storage mediums.
2
Secure transmission: Implement secure communication protocols, such as HTTPS, SSL/TLS,
or other encryption mechanisms, when transmitting sensitive data over networks. This helps
prevent eavesdropping or unauthorized interception of data during transit.
3
Access controls: Implement strong access controls to limit access to sensitive information.
Use authentication and authorization mechanisms to ensure that only authorized individuals or
systems can access and modify sensitive data.
4
Secure coding practices: Follow secure coding practices to avoid common vulnerabilities, such
as injection attacks or insecure direct object references. Validate and sanitize user input to
prevent malicious data from being processed or displayed.
5
Secure configuration: Ensure that your systems and applications are securely configured,
including the use of strong passwords, disabling unnecessary services or features, and
6
By implementing these preventive measures and adopting a comprehensive approach to data
security, you can significantly reduce the risk of sensitive information exposure and protect the
privacy and confidentiality of your data.
Insertion of sensitive information into sent data refers to the inadvertent inclusion of confidential
or private data into logs, error messages, debug output, or any other form of data that is sent or
logged externally. This can occur when sensitive information, such as passwords, API keys, or
personally identifiable information (PII), is included in plaintext or unencrypted form, making it
accessible to unauthorized individuals or systems.
To prevent the insertion of sensitive information into sent data, you can follow these preventive
measures:
regularly updating and patching software to address security vulnerabilities.
Regular security assessments: Conduct regular security assessments, including vulnerability
scanning and penetration testing, to identify any potential weaknesses or vulnerabilities that
could lead to the exposure of sensitive information.
7
Employee training and awareness: Train your employees on security best practices, including
how to handle sensitive information, the importance of data protection, and how to recognize
and report security incidents or suspicious activities.
8
Data minimization: Collect and retain only the necessary data. Avoid storing or keeping
sensitive information for longer than necessary.
9
Privacy by design: Incorporate privacy and security considerations into the design and
development of your systems and applications. Implement privacy-enhancing technologies
and practices from the outset.
10
Insertion of Sensitive Information Into Sent Data
Data masking: Avoid including sensitive information in logs, error messages, or any other form
of output. Implement data masking techniques, such as replacing sensitive data with
placeholders or obfuscating it, to prevent the exposure of sensitive information.
1
Secure logging: Configure logging mechanisms to exclude sensitive information from being
logged. Implement proper log filtering or redaction techniques to remove or mask sensitive
data before it is written to log files.
2
Context-based logging: When logging or outputting data, consider the context and purpose of
the logged information. Exclude any unnecessary or sensitive data from being included in the
3
By implementing these preventive measures, you can reduce the risk of sensitive information
being inadvertently included in sent data, protecting the confidentiality and privacy of your data
and minimizing the potential impact of a security breach.
Cross-Site Request Forgery (CSRF) is a type of web vulnerability where an attacker tricks a victim
into unknowingly executing unwanted actions on a web application in which the victim is
authenticated. The attack occurs when the victim visits a malicious website or clicks on a
specially crafted link, resulting in unauthorized actions being performed on their behalf on the
targeted web application.
To prevent Cross-Site Request Forgery attacks, you can follow these preventive measures:
logs or output.
Tokenization or encryption: If it is necessary to include sensitive information in logs or output
for debugging or troubleshooting purposes, tokenize or encrypt the sensitive data to render it
unreadable. Ensure that only authorized individuals or systems have access to the keys or
tokens required for decryption.
4
Secure error handling: When handling errors, avoid displaying sensitive information in error
messages presented to users. Instead, provide generic error messages that do not reveal
specific details about the underlying sensitive data or system.
5
Secure coding practices: Follow secure coding practices to prevent unintentional insertion of
sensitive information into sent data. Ensure that sensitive data is properly handled, encrypted,
or obfuscated throughout the application’s lifecycle.
6
Data separation: Consider separating sensitive data from other non-sensitive data, both in
storage and during transmission. Implement proper data segregation mechanisms to reduce
the risk of sensitive information being inadvertently included in sent data.
7
Regular code reviews and testing: Conduct regular code reviews and security testing to
identify any potential areas where sensitive information might be included in sent data.
Perform thorough testing to ensure that sensitive data is not exposed during normal system
operations or error conditions.
8
Employee training and awareness: Train your development team and system administrators
about the importance of handling sensitive information securely. Educate them on best
practices for data protection and the potential risks associated with the insertion of sensitive
information into sent data.
9
Cross-Site Request Forgery (CSRF)
By implementing these preventive measures and maintaining a strong security posture, you can
significantly reduce the risk of Cross-Site Request Forgery attacks and protect the integrity of
your web application and user data.
The use of hard-coded passwords refers to the practice of embedding passwords directly into
source code or configuration files, making them easily discoverable by anyone with access to the
CSRF tokens: Implement CSRF tokens as a defense mechanism. Include a unique token in each
HTML form or request that modifies state on the server. This token should be validated on the
server-side to ensure that the request is legitimate and originated from the same site.
1
Same-Site cookies: Set the SameSite attribute on your session cookies to Strict or Lax. This
prevents cookies from being sent in cross-origin requests, effectively mitigating CSRF attacks.
2
Anti-CSRF frameworks: Utilize anti-CSRF frameworks or libraries provided by your web
development framework. These frameworks often automate the generation and validation of
CSRF tokens, making it easier to implement and maintain protection against CSRF attacks.
3
Unique session identifiers: Ensure that each user session has a unique identifier. This helps
prevent session fixation attacks, which could be used in combination with CSRF attacks.
4
Request validation: Validate the integrity and authenticity of incoming requests on the server-
side. Check for the presence and correctness of CSRF tokens, referer headers, or other
request attributes that can help identify the origin of the request.
5
Strict access controls: Enforce strict access controls on sensitive operations and resources.
Implement proper authentication and authorization mechanisms to ensure that only authorized
users can perform critical actions.
6
User awareness: Educate your users about the risks of CSRF attacks and encourage them to
be cautious when clicking on links or visiting unfamiliar websites. Provide guidance on
recognizing and reporting suspicious behavior.
7
Secure coding practices: Follow secure coding practices to minimize the risk of introducing
vulnerabilities. Validate and sanitize user input, implement proper access controls, and
regularly update and patch your software to address any potential security vulnerabilities.
8
Security testing: Perform regular security testing, including vulnerability scanning and
penetration testing, to identify and address any potential CSRF vulnerabilities in your web
application.
9
Use of Hard-coded Password
code or files. This is considered a poor security practice as it can lead to unauthorized access and
compromise of sensitive information.
To prevent the use of hard-coded passwords, you can follow these preventive measures:
Use secure credential storage: Instead of hard-coding passwords, utilize secure credential
storage mechanisms provided by your development platform or framework. These
mechanisms allow you to securely store and retrieve passwords, such as using secure key
stores, environment variables, or configuration files with restricted access.
1
Implement authentication mechanisms: Implement proper authentication mechanisms instead
of relying solely on hard-coded passwords. Use strong password hashing algorithms, salted
hashes, or better yet, consider using more secure authentication methods like token-based
authentication or OAuth.
2
Separate configuration from code: Keep sensitive information, including passwords, separate
from your codebase. Store them in secure configuration files or use environment variables to
store sensitive configuration details. Ensure that these files or variables are not accessible by
unauthorized individuals.
3
Apply access controls: Limit access to configuration files or secure credential storage to only
authorized individuals or systems. Follow the principle of least privilege, granting access only
to those who need it for operational purposes.
4
Utilize secrets management tools: Leverage secrets management tools or platforms that
provide secure storage, rotation, and access control for sensitive information such as
passwords, API keys, and cryptographic keys. These tools often offer encryption, access
logging, and additional security features to protect your secrets.
5
Secure deployment process: Implement secure deployment practices to ensure that
passwords are not exposed during deployment or in version control systems. Avoid including
sensitive information in code repositories or build artifacts.
6
Regularly rotate passwords: Enforce a password rotation policy to regularly update passwords.
This reduces the impact of compromised credentials and limits the window of opportunity for
attackers.
7
Secure code review: Conduct regular code reviews to identify and remove any instances of
hard-coded passwords. Train developers to be aware of the risks associated with hard-coding
passwords and provide them with secure alternatives and best practices.
8
By implementing these preventive measures, you can minimize the risk of hard-coded passwords
and enhance the security of your application and sensitive data. It is crucial to follow secure
coding practices, regularly review and update security controls, and stay informed about
emerging best practices and vulnerabilities to maintain a strong security posture.
A broken or risky cryptographic algorithm refers to the use of encryption or hashing algorithms
that have known vulnerabilities or weaknesses. These vulnerabilities could be due to outdated or
deprecated algorithms, insecure key sizes, poor implementation, or inadequate cryptographic
practices. Such weaknesses can be exploited by attackers, potentially compromising the
confidentiality, integrity, or authenticity of sensitive data.
To prevent the use of broken or risky crypto algorithms, you can follow these preventive
measures:
Automated security tools: Use automated security scanning tools or static code analysis tools
to identify instances of hard-coded passwords and other security vulnerabilities in your
codebase.
9
Broken or Risky Crypto Algorithm
Stay updated with cryptographic standards: Keep abreast of the latest cryptographic
standards and recommendations from reputable sources, such as NIST (National Institute of
Standards and Technology) or IETF (Internet Engineering Task Force). Stay informed about any
vulnerabilities or weaknesses discovered in existing algorithms and make necessary updates
to your cryptographic implementations.
1
Use strong and approved algorithms: Select cryptographic algorithms that are widely
recognized, thoroughly tested, and recommended by cryptographic experts. Examples of
secure algorithms include AES (Advanced Encryption Standard) for symmetric encryption, RSA
or ECDSA for asymmetric encryption, and SHA-256 or SHA-3 for hashing.
2
Avoid deprecated or weakened algorithms: Stay away from deprecated or weakened
cryptographic algorithms, such as DES (Data Encryption Standard) or MD5 (Message Digest
Algorithm 5). These algorithms have known vulnerabilities and are no longer considered
secure for most applications.
3
Use appropriate key sizes: Ensure that the key sizes used in your cryptographic algorithms are
appropriate for the level of security required. Use key sizes recommended by cryptographic
standards, taking into account the strength of the algorithm and the anticipated lifespan of the
data being protected.
4
By following these preventive measures and adopting strong cryptographic practices, you can
significantly reduce the risk of using broken or risky crypto algorithms and enhance the security
of your application’s sensitive data. It is essential to maintain an active stance in staying informed
about cryptographic best practices and evolving security threats to ensure the continued security
of your cryptographic implementations.
A broken or risky cryptographic algorithm refers to the use of encryption or hashing algorithms
that have known vulnerabilities or weaknesses. These vulnerabilities could be due to outdated or
deprecated algorithms, insecure key sizes, poor implementation, or inadequate cryptographic
practices. Such weaknesses can be exploited by attackers, potentially compromising the
confidentiality, integrity, or authenticity of sensitive data.
To prevent the use of broken or risky crypto algorithms, you can follow these preventive
measures:
Secure key management: Implement robust key management practices, including the secure
generation, storage, and distribution of cryptographic keys. Protect keys from unauthorized
access, and regularly rotate or update keys as per best practices.
5
Use secure random number generation: Cryptographic operations often rely on random
numbers for key generation, initialization vectors, and nonces. Use a cryptographically secure
random number generator (CSPRNG) to ensure the randomness and unpredictability of these
values.
6
Third-party library evaluation: When using cryptographic libraries or frameworks, evaluate
their reputation, security track record, and community support. Choose well-established
libraries that have undergone security audits and are actively maintained to minimize the risk
of using broken or insecure crypto algorithms.
7
Independent security reviews: Conduct independent security reviews or audits of your
cryptographic implementations to identify any weaknesses, vulnerabilities, or
misconfigurations. Engage security professionals or external auditors with expertise in
cryptography to assess your cryptographic practices.
8
Ongoing monitoring and updates: Stay vigilant about emerging cryptographic vulnerabilities or
attacks. Monitor security advisories and updates from cryptographic standards organizations,
vendors, and the broader security community. Apply patches, updates, or configuration
changes as necessary to address any identified vulnerabilities.
9
Risky Crypto Algorithm
Independent security reviews: Conduct independent security reviews or audits of your
cryptographic implementations to identify any weaknesses, vulnerabilities, or misconfigurations.
Engage security professionals or external auditors with expertise in cryptography to assess your
cryptographic practices.
Stay updated with cryptographic standards: Keep abreast of the latest cryptographic
standards and recommendations from reputable sources, such as NIST (National Institute of
Standards and Technology) or IETF (Internet Engineering Task Force). Stay informed about any
vulnerabilities or weaknesses discovered in existing algorithms and make necessary updates
to your cryptographic implementations.
1
Use strong and approved algorithms: Select cryptographic algorithms that are widely
recognized, thoroughly tested, and recommended by cryptographic experts. Examples of
secure algorithms include AES (Advanced Encryption Standard) for symmetric encryption, RSA
or ECDSA for asymmetric encryption, and SHA-256 or SHA-3 for hashing.
2
Avoid deprecated or weakened algorithms: Stay away from deprecated or weakened
cryptographic algorithms, such as DES (Data Encryption Standard) or MD5 (Message Digest
Algorithm 5). These algorithms have known vulnerabilities and are no longer considered
secure for most applications.
3
Use appropriate key sizes: Ensure that the key sizes used in your cryptographic algorithms are
appropriate for the level of security required. Use key sizes recommended by cryptographic
standards, taking into account the strength of the algorithm and the anticipated lifespan of the
data being protected.
4
Secure key management: Implement robust key management practices, including the secure
generation, storage, and distribution of cryptographic keys. Protect keys from unauthorized
access, and regularly rotate or update keys as per best practices.
5
Use secure random number generation: Cryptographic operations often rely on random
numbers for key generation, initialization vectors, and nonces. Use a cryptographically secure
random number generator (CSPRNG) to ensure the randomness and unpredictability of these
values.
6
Third-party library evaluation: When using cryptographic libraries or frameworks, evaluate
their reputation, security track record, and community support. Choose well-established
libraries that have undergone security audits and are actively maintained to minimize the risk
of using broken or insecure crypto algorithms.
7
By following these preventive measures and adopting strong cryptographic practices, you can
significantly reduce the risk of using broken or risky crypto algorithms and enhance the security
of your application’s sensitive data. It is essential to maintain an active stance in staying informed
about cryptographic best practices and evolving security threats to ensure the continued security
of your cryptographic implementations.
Insufficient entropy refers to a lack of randomness or unpredictability in the generation of
cryptographic keys, random numbers, or other security-critical values. Insufficient entropy can
weaken cryptographic algorithms and make them more susceptible to brute-force attacks or other
cryptographic attacks.
To prevent insufficient entropy, you can follow these preventive measures:
Ongoing monitoring and updates: Stay vigilant about emerging cryptographic vulnerabilities or
attacks. Monitor security advisories and updates from cryptographic standards organizations,
vendors, and the broader security community. Apply patches, updates, or configuration
changes as necessary to address any identified vulnerabilities.
1
Insufficient Entropy
Use a cryptographically secure random number generator (CSPRNG): Use a CSPRNG instead
of relying on pseudo-random number generators (PRNGs) or non-secure random sources. A
CSPRNG ensures that the generated random numbers are sufficiently unpredictable and
suitable for cryptographic purposes.
1
Collect entropy from diverse sources: Gather entropy from a variety of sources, such as
hardware events (e.g., mouse movements, keyboard presses, disk activity), system-level
events, environmental factors, or dedicated hardware random number generators. Combine
these entropy sources to increase the randomness and unpredictability of the generated
values.
2
Periodically reseed the random number generator: Regularly reseed the random number
generator with fresh entropy to maintain a high level of randomness. This helps prevent the
depletion of entropy over time.
3
Use hardware-based random number generation: If available, consider utilizing dedicated
hardware random number generators (RNGs) that provide a high degree of randomness.
These RNGs use physical processes, such as electronic noise or radioactive decay, to
generate random values.
4
By implementing these preventive measures, you can enhance the entropy generation process
and ensure the strength and unpredictability of cryptographic operations. It is crucial to regularly
assess and update your entropy generation mechanisms to adapt to evolving security
requirements and best practices.
XSS (Cross-Site Scripting) is a type of web vulnerability that allows attackers to inject malicious
scripts into web pages viewed by other users. It occurs when user-supplied data is improperly
validated or escaped and is directly included in a web page without proper sanitization.
To prevent XSS attacks, you can follow these preventive measures:
Test and monitor entropy levels: Implement mechanisms to test and monitor the entropy levels
in your system. You can use tools or libraries to assess the quality of randomness and ensure
that it meets the required entropy threshold. Monitor entropy pools to identify any potential
depletion or insufficient entropy conditions.
5
Avoid deterministic algorithms for key generation: Use algorithms that incorporate randomness
and avoid deterministic algorithms for key generation. Deterministic algorithms generate the
same output for the same input, making them predictable and susceptible to attacks.
6
Periodically rotate cryptographic keys: Regularly rotate cryptographic keys, especially for
long-lived cryptographic operations. This minimizes the impact of compromised keys and
provides an opportunity to introduce fresh entropy during the key generation process.
7
Perform security testing and code review: Conduct security testing, including vulnerability
scanning and code review, to identify any weaknesses or vulnerabilities related to entropy
generation. Review the implementation of random number generation functions and ensure
they meet cryptographic best practices.
8
Follow cryptographic standards and best practices: Adhere to established cryptographic
standards, guidelines, and best practices. Standards organizations like NIST and IETF provide
recommendations and guidelines for generating and managing cryptographic keys, random
numbers, and entropy.
9
XSS
Input validation and filtering: Validate and sanitize all user-generated input, including form
fields, URL parameters, and HTTP headers. Apply input validation to ensure that only expected
data types and formats are accepted. Filter out or escape characters that can be used for
malicious purposes, such as HTML tags, JavaScript code, or SQL commands.
1
By following these preventive measures, you can significantly reduce the risk of XSS attacks and
protect your web application and users from potential malicious activities. It is essential to
Use secure coding practices: Implement secure coding practices that promote the separation
of code and data. Use appropriate context-aware output encoding or escaping techniques
when displaying user-supplied data in HTML, JavaScript, CSS, or other contexts.
2
Use a secure templating system: If using a templating system, make sure it automatically
escapes or sanitizes user input by default. Avoid using string concatenation or manual HTML
construction for displaying user-supplied data.
3
Content Security Policy (CSP): Implement and enforce a Content Security Policy that restricts
the types of content that can be loaded or executed on a web page. CSP helps mitigate XSS
attacks by defining the sources from which various content, such as scripts or stylesheets, can
be loaded.
4
HTTP-only cookies: Use the HttpOnly flag when setting cookies to prevent client-side scripts
from accessing sensitive cookies. This helps protect against session hijacking attacks.
5
Escape output appropriately: When dynamically generating HTML, JavaScript, or other
content, ensure that user-supplied data is properly escaped to prevent it from being
interpreted as code. Use context-aware escaping functions provided by your programming
framework or language.
6
Secure development frameworks and libraries: Utilize secure development frameworks and
libraries that have built-in protections against XSS attacks. These frameworks often provide
mechanisms to automatically escape or sanitize user input when rendering templates or
generating HTML.
7
Regularly update and patch: Keep all web application components, including frameworks,
libraries, and plugins, up to date with the latest security patches. XSS vulnerabilities may be
discovered in these components, and updates often address these vulnerabilities.
8
Educate and train developers: Provide security training and awareness programs to developers
to educate them about the risks of XSS attacks and secure coding practices. Teach them how
to properly validate, sanitize, and escape user input to prevent XSS vulnerabilities.
9
Penetration testing and security scanning: Regularly conduct penetration testing and security
scanning to identify any XSS vulnerabilities in your web application. Utilize automated
vulnerability scanners or engage security professionals to perform manual security
assessments.
10
implement a layered approach to security, combining secure coding practices, input validation,
output encoding, and regular security testing to maintain a strong defense against XSS
vulnerabilities.
SQL Injection is a web application vulnerability that occurs when an attacker is able to manipulate
an SQL query by inserting malicious SQL code. It happens when user-supplied input is not
properly validated or sanitized and is directly concatenated into an SQL statement, allowing the
attacker to execute unauthorized database operations, view sensitive data, or modify the
database.
To prevent SQL Injection attacks, you can follow these preventive measures:
SQL Injection
Use parameterized queries or prepared statements: Instead of dynamically building SQL
queries by concatenating user input, use parameterized queries or prepared statements.
These mechanisms allow you to separate the SQL code from the user-supplied input,
preventing the injection of malicious SQL code.
1
Input validation and sanitization: Validate and sanitize all user-generated input before using it
in SQL queries. Validate input to ensure it matches the expected data type, length, and format.
Sanitize input by removing or escaping special characters that can be used for SQL injection,
such as single quotes or semicolons.
2
Avoid dynamic SQL queries: Whenever possible, avoid dynamically building SQL queries using
string concatenation. Instead, use ORM (Object-Relational Mapping) frameworks or query
builders that provide built-in protection against SQL injection. These frameworks automatically
handle the proper escaping and parameter binding.
3
Least privilege principle: Ensure that the database user account used by the web application
has the least privilege necessary to perform its required operations. Restrict the permissions
to only those specific tables and operations required by the application, reducing the potential
impact of a successful SQL injection attack.
4
Securely manage database credentials: Store and manage database credentials securely.
Avoid hard-coding credentials in the source code or configuration files. Instead, use secure
credential storage mechanisms such as environment variables or secure key stores.
5
Implement input validation on the server-side: While client-side input validation provides a
better user experience, it should not be solely relied upon for security. Always perform input
6
By implementing these preventive measures, you can significantly reduce the risk of SQL Injection
attacks and protect your web application from unauthorized database access or manipulation. It is
important to adopt a proactive approach to security, combining secure coding practices, input
validation, parameterized queries, and regular security testing to maintain the integrity and
security of your application’s database interactions.
External Control of File Name or Path is a vulnerability that occurs when an attacker can
manipulate the file name or path used in file operations, leading to unintended or unauthorized
access to files on the system. This vulnerability can be exploited to read, overwrite, or execute
arbitrary files, potentially compromising the security and integrity of the application and the
underlying system.
To prevent External Control of File Name or Path vulnerabilities, you can follow these preventive
measures:
validation and sanitization on the server-side as well, as client-side validation can be bypassed
or manipulated.
Regularly update and patch: Keep your database management system (DBMS) up to date with
the latest security patches. DBMS vendors often release updates to address security
vulnerabilities, including those related to SQL injection.
7
Implement strong access controls: Implement strong access controls at the application level to
restrict user access and actions. Use role-based access control (RBAC) and properly
authenticate and authorize users to ensure they only have access to the appropriate resources
and actions.
8
Security testing and code review: Conduct regular security testing, including penetration
testing and code review, to identify any SQL injection vulnerabilities in your web application.
Utilize automated vulnerability scanners and engage security professionals to perform manual
security assessments.
9
Secure development practices: Promote secure coding practices within your development
team. Educate developers about the risks of SQL injection and provide training on secure
coding techniques and best practices. Encourage the use of secure coding frameworks and
libraries that offer protection against SQL injection.
10
External Control of File Name or Path
Validate and sanitize file inputs: Validate and sanitize any file-related inputs received from
users or external sources. Verify that the file names or paths conform to the expected format
1
and do not contain any unexpected or malicious characters. Sanitize the input by removing or
escaping any characters that can be used for path traversal or command injection.
Use whitelisting: Implement a whitelist approach for allowed file names or paths. Define a list
of permitted characters, file extensions, or directory paths that are considered safe and reject
any inputs that do not match the whitelist. This helps prevent unauthorized access to sensitive
files or system directories.
2
Avoid user-controlled file names or paths: Whenever possible, avoid using user-supplied input
directly as file names or paths. Generate file names or paths programmatically using trusted
and validated data sources, such as a database or internal configuration. If user input is
necessary, consider using a secure file upload mechanism that stores uploaded files in a
designated, non-executable directory.
3
Restrict file system access permissions: Set appropriate access permissions on files and
directories to limit the privileges of the application or process accessing them. Ensure that the
application runs with the least privilege necessary to perform its operations and restrict access
to sensitive files or system directories.
4
Use platform-specific secure file APIs: Utilize secure file access APIs provided by the
programming language or framework you’re using. These APIs often include built-in
protections against path traversal attacks or command injection. Avoid using low-level file
system access methods that may be more susceptible to vulnerabilities.
5
Implement file access controls: Implement proper file access controls within your application.
Authenticate and authorize users to ensure they have the necessary permissions to access
specific files or directories. Enforce file-level access controls based on user roles or privileges.
6
Secure file upload and download: Implement secure file upload and download mechanisms
that validate file types, check file sizes, and perform virus/malware scanning. Restrict the
allowed file extensions, set size limits, and ensure the uploaded files are stored in a secure
location.
7
Regularly update and patch: Keep the underlying operating system, libraries, and
dependencies up to date with the latest security patches. Patches often address vulnerabilities
related to file system operations and can help mitigate the risk of external control of file name
or path attacks.
8
Security testing and code review: Conduct regular security testing, including penetration
testing and code review, to identify any vulnerabilities related to file operations. Utilize
9
By implementing these preventive measures, you can significantly reduce the risk of external
control of file name or path vulnerabilities and protect your application from unauthorized file
access or manipulation. It is crucial to follow secure coding practices, validate and sanitize file
inputs, and regularly update your systems to address any emerging security issues.
The Generation of Error Message Containing Sensitive Information is a vulnerability that occurs
when error messages generated by an application reveal sensitive or confidential information.
This can include details such as database connection strings, stack traces, user credentials, or
other sensitive data. Attackers can exploit this information to gain insights into the system’s
architecture, identify potential weaknesses, or launch further attacks.
To prevent the generation of error messages containing sensitive information, you can follow
these preventive measures:
automated vulnerability scanners or engage security professionals to perform manual security
assessments.
Educate developers: Provide training and education to developers about secure file handling
practices and the risks associated with external control of file name or path vulnerabilities.
Promote secure coding techniques and best practices within your development team.
10
Generation of Error Message Containing Sensitive Information
Disable detailed error messages in production: Ensure that your application’s production
environment is configured to display generic error messages instead of detailed technical
information. This helps to prevent the inadvertent exposure of sensitive data in error
messages.
1
Implement custom error handling: Create custom error handling mechanisms that capture and
handle application errors without disclosing sensitive information. Customize error messages
to provide generic and user-friendly feedback to users, without revealing specific technical
details.
2
Log errors securely: If your application logs errors, ensure that sensitive information is not
included in the log entries. Review your logging configuration to ensure that only necessary
information is logged, and sanitize any logged data to remove sensitive details.
3
Avoid displaying sensitive information: Avoid displaying sensitive information in error messages
altogether. Refrain from including sensitive data such as user credentials, database connection
strings, or internal system paths in error messages. Instead, focus on providing useful and
actionable information to users without revealing sensitive details.
4
By implementing these preventive measures, you can minimize the risk of exposing sensitive
information in error messages and enhance the security of your application. It is crucial to
prioritize the protection of sensitive data and regularly review and update your error handling
mechanisms to ensure they align with best practices and evolving security standards.
Unprotected storage of credentials refers to the practice of storing sensitive credentials, such as
usernames, passwords, API keys, or access tokens, in an insecure manner. This can include
storing credentials in plain text, using weak encryption, or storing them in easily accessible
locations, making them vulnerable to unauthorized access and potential misuse by attackers.
Use exception handling best practices: Employ proper exception handling techniques in your
code. Catch and handle exceptions gracefully, avoiding the propagation of sensitive
information in error messages. Implement structured exception handling mechanisms to
capture and handle errors effectively.
5
Regularly test error handling: Perform thorough testing of your application’s error handling
mechanisms. Include scenarios where exceptions are intentionally triggered to ensure that
sensitive information is not disclosed in error messages. Use automated vulnerability scanning
tools or engage security professionals to identify potential information leakage.
6
Implement input validation and sanitization: Validate and sanitize user input to prevent
malicious input from triggering errors that reveal sensitive information. Proper input validation
helps to prevent common attack vectors, such as injection attacks, that can lead to the
generation of error messages containing sensitive data.
7
Follow secure coding practices: Adhere to secure coding practices and guidelines. Keep
sensitive information separate from error messages and ensure that error handling code is
robust and secure. Apply secure coding principles throughout the development lifecycle to
minimize the likelihood of vulnerabilities.
8
Regularly update and patch: Keep your application and its dependencies up to date with the
latest security patches. Software updates often address security vulnerabilities, including
those related to error handling and the potential exposure of sensitive information.
9
Educate developers: Provide training and awareness programs to educate developers about
the risks associated with error messages containing sensitive information. Promote secure
coding practices and emphasize the importance of properly handling and securing error
messages.
10
Unprotected storage of credentials
To prevent unprotected storage of credentials, you should follow these preventive measures:
Use secure credential storage mechanisms: Utilize secure methods for storing credentials,
such as secure databases, encrypted files, or dedicated credential management systems.
These mechanisms should provide strong encryption and access controls to protect the
confidentiality and integrity of the stored credentials.
1
Avoid storing plain text passwords: Never store passwords or sensitive credentials in plain text.
Instead, use strong cryptographic techniques, such as one-way hashing with salt or key
derivation functions, to securely store and verify passwords.
2
Implement strong encryption: If you need to store credentials in a file or database, ensure that
the data is encrypted using robust encryption algorithms and keys. Utilize industry-standard
encryption libraries and algorithms to protect the credentials from unauthorized access.
3
Separate credentials from source code: Avoid storing credentials directly in source code or
configuration files that are part of version control systems. Separate the credentials from the
codebase and use environment-specific configuration files or secure secrets management
tools to provide the necessary credentials during runtime.
4
Securely manage API keys and access tokens: When working with API keys or access tokens,
follow best practices provided by the respective service or framework. Avoid hardcoding these
credentials and instead use secure environment variables or dedicated configuration files to
store and retrieve them.
5
Implement access controls: Enforce proper access controls to limit access to sensitive
credentials. Grant access only to authorized individuals who require it for their specific roles or
tasks. Regularly review and update access permissions to ensure that only trusted individuals
have access to the credentials.
6
Regularly rotate credentials: Implement a credential rotation policy that mandates periodic
password changes, key rotation, or the issuance of new access tokens. Regularly rotating
credentials reduces the risk of long-term exposure and unauthorized access to sensitive
systems.
7
Monitor and log credential access: Implement logging and monitoring mechanisms to track
access to sensitive credentials. Regularly review logs for any suspicious or unauthorized
access attempts. Monitoring helps detect any potential breaches or unauthorized usage of
credentials.
8
By implementing these preventive measures, you can significantly reduce the risk of unprotected
storage of credentials and enhance the security of your application and systems. Safeguarding
sensitive credentials is crucial for protecting user data, preventing unauthorized access, and
maintaining the trust of your users.
Trust Boundary Violation refers to a security vulnerability that occurs when data or control crosses
a trust boundary without proper validation or authorization. It happens when data from an
untrusted source is treated as trusted or when there is a failure to enforce proper access controls
at the boundary between trusted and untrusted components or systems. This violation can lead to
unauthorized access, data breaches, privilege escalation, or the execution of malicious code.
To prevent Trust Boundary Violation, you should follow these preventive measures:
Educate users about secure credential management: Provide training and awareness programs
to educate users and developers about the importance of secure credential management
practices. Emphasize the risks associated with unprotected storage of credentials and
promote secure coding and handling techniques.
9
Regularly assess and audit: Conduct regular security assessments and audits to identify any
potential vulnerabilities or weaknesses in the storage and management of credentials. Utilize
automated scanning tools or engage security professionals to perform thorough assessments.
10
Trust Boundary Violation
Validate and sanitize inputs: Validate and sanitize all inputs received from untrusted sources,
such as user input, API calls, or data from external systems. Implement strict input validation
and filtering techniques to ensure that only safe and expected data is passed across trust
boundaries.
1
Implement strong authentication and authorization: Enforce robust authentication and
authorization mechanisms to ensure that only authorized entities can access sensitive
resources or perform critical operations. Implement access controls at trust boundaries to
prevent unauthorized access.
2
Apply the principle of least privilege: Grant users, components, or systems only the minimum
privileges necessary to perform their tasks. Avoid giving unnecessary permissions or elevated
privileges that can potentially lead to trust boundary violations.
3
Use secure communication protocols: When data crosses trust boundaries, ensure that secure
communication protocols, such as SSL/TLS, are used to protect the confidentiality and
integrity of the data in transit. Encrypt sensitive data to prevent interception or tampering.
4
By following these preventive measures, you can mitigate the risk of trust boundary violations and
enhance the overall security posture of your application or system. It is crucial to establish clear
trust boundaries, implement appropriate security controls, and regularly monitor and update your
systems to prevent unauthorized access or compromise across trust boundaries.
Insufficiently Protected Credentials is a security vulnerability that occurs when sensitive
credentials, such as usernames, passwords, API keys, or access tokens, are not adequately
protected, making them susceptible to unauthorized access or misuse. This can happen due to
weak encryption, improper storage, or inadequate access controls, putting sensitive information
at risk.
To prevent Insufficiently Protected Credentials, you should follow these preventive measures:
Implement secure session management: If sessions are used to maintain user state or context,
ensure that proper session management practices are followed. Use secure session tokens,
enforce session timeouts, and protect against session fixation or session hijacking attacks.
5
Segregate and isolate components: Clearly define and enforce trust boundaries between
different components or systems. Isolate untrusted components or systems from trusted ones
to minimize the impact of a potential breach or compromise.
6
Regularly update and patch: Keep all components, frameworks, libraries, and systems up to
date with the latest security patches. Regularly review and update security configurations to
address any known vulnerabilities that may lead to trust boundary violations.
7
Implement runtime monitoring and anomaly detection: Deploy monitoring systems that can
detect and alert on unusual or unexpected behaviors across trust boundaries. Monitor for
suspicious activities, unexpected data flows, or unauthorized access attempts.
8
Perform security testing and code reviews: Conduct regular security testing, including
penetration testing and code reviews, to identify and address any trust boundary
vulnerabilities. Test the resilience of your system to boundary violations and validate the
effectiveness of implemented security controls.
9
Provide security awareness training: Educate developers and system administrators about the
risks and consequences of trust boundary violations. Promote security awareness and provide
training on secure coding practices, secure configuration management, and the importance of
enforcing trust boundaries.
10
Insufficiently Protected Credentials
Use strong encryption: Ensure that sensitive credentials are properly encrypted using strong
encryption algorithms and keys. Employ industry-standard encryption practices to protect the
confidentiality and integrity of the stored credentials.
1
Implement secure storage mechanisms: Store credentials in secure storage systems, such as
encrypted databases or secure key stores, that provide appropriate access controls and
protection against unauthorized access. Avoid storing credentials in plain text or insecurely
accessible locations.
2
Avoid hardcoding credentials: Hardcoding credentials directly in source code or configuration
files should be avoided. Instead, utilize environment variables, secure secrets management
tools, or configuration files with restricted access to store and retrieve credentials.
3
Implement secure credential transmission: When transmitting credentials, use secure
communication protocols such as SSL/TLS to encrypt the data in transit. Avoid transmitting
credentials over insecure channels or including them in URL parameters.
4
Apply the principle of least privilege: Grant credentials only the minimum privileges required
for the intended functionality. Avoid providing unnecessary or excessive privileges to reduce
the potential impact of a credential compromise.
5
Enforce strong password policies: Implement strong password policies that encourage users to
create complex and unique passwords. Enforce password expiration and provide mechanisms
for password resets or account recovery.
6
Implement multi-factor authentication (MFA): Utilize MFA to add an extra layer of security.
Require users to provide additional authentication factors, such as a time-based one-time
password (TOTP) or biometric data, to access sensitive resources.
7
Regularly rotate credentials: Establish a credential rotation policy that mandates periodic
password changes, key rotation, or token regeneration. Regularly update and rotate
credentials to limit the exposure window in case of a compromise.
8
Implement secure coding practices: Follow secure coding practices to minimize the risk of
inadvertently exposing credentials. Avoid logging or displaying credentials in error messages
or debug output. Implement secure coding techniques to protect against common
vulnerabilities like injection attacks.
9
Conduct regular security assessments: Perform regular security assessments and penetration
testing to identify vulnerabilities and weaknesses in credential protection. Engage security
professionals or utilize automated vulnerability scanning tools to identify potential issues.
10
By implementing these preventive measures, you can significantly reduce the risk of Insufficiently
Protected Credentials and enhance the security of your systems. Protecting sensitive credentials
is crucial for safeguarding user data, preventing unauthorized access, and maintaining the trust of
your users.
Restriction of XML External Entity (XXE) Reference is a security vulnerability that occurs when an
XML parser processes external entities included in the XML input. Attackers can exploit this
vulnerability to read sensitive data from the server or perform denial-of-service attacks.
To prevent XXE vulnerabilities, you should follow these preventive measures:
Educate users and developers: Raise awareness among users and developers about the
importance of protecting credentials. Provide training on secure coding practices, password
management, and the risks associated with insufficiently protected credentials.
11
Restriction of XML External Entity Reference
Disable external entity processing: Configure the XML parser to disable the processing of
external entities. This prevents the XML parser from resolving and including external entities in
the XML input.
1
Validate and sanitize XML inputs: Implement proper input validation and sanitization
techniques to ensure that only expected and safe XML data is processed. Use strict parsing
settings and reject or sanitize any untrusted or unexpected XML input.
2
Use whitelisting and filtering: Implement whitelisting or filtering mechanisms to allow only
known safe XML structures and reject or remove any potentially malicious XML constructs or
elements.
3
Upgrade to a secure XML parser: Use the latest version of a secure and well-maintained XML
parser library. Older versions of XML parsers may have known vulnerabilities that can be
exploited by attackers.
4
Implement least privilege: Restrict access privileges of the XML parser to minimize the
potential impact of an XXE attack. Ensure that the XML parser runs with the least privileges
required to perform its functionality.
5
Avoid using user-controlled XML: Avoid using user-controlled XML in sensitive operations or
processing. If user-supplied XML is required, ensure strict validation and sanitization of the
input to mitigate the risk of XXE vulnerabilities.
6
By implementing these preventive measures, you can reduce the risk of XXE vulnerabilities and
enhance the security of your XML processing. It is essential to be cautious when handling XML
data, implement secure coding practices, and keep the XML parser up to date to prevent
attackers from exploiting XXE vulnerabilities.
Vulnerable and outdated components refer to third-party libraries, frameworks, or software
components that have known security vulnerabilities or are no longer supported with security
patches. Using such components can introduce security risks into your application or system, as
attackers can exploit these vulnerabilities to gain unauthorized access or compromise your
system.
To prevent the use of vulnerable and outdated components, you should follow these preventive
measures:
Implement server-side filtering and input validation: Apply server-side input validation and
filtering techniques to prevent XXE vulnerabilities. Validate and sanitize all XML data received
from clients before processing it on the server.
7
Follow secure coding practices: Adhere to secure coding practices when handling XML data.
Avoid concatenating XML strings or building XML dynamically using untrusted input, as it can
introduce XML injection vulnerabilities.
8
Regularly update and patch: Keep the XML parser and associated libraries up to date with the
latest security patches. Stay informed about any security advisories or updates related to the
XML parser to address any known vulnerabilities.
9
Perform security testing: Conduct security testing, including vulnerability assessments and
penetration testing, to identify and remediate XXE vulnerabilities. Test the resilience of the
application against various XXE attack vectors and verify the effectiveness of implemented
security controls.
10
Vulnerable and Outdated Components
Maintain an inventory of components: Create and maintain an inventory of all the third-party
components used in your application or system. Keep track of the version numbers and the
sources of these components.
1
Stay informed about security updates: Stay updated with the latest security advisories and
vulnerability reports for the components you use. Subscribe to security mailing lists or follow
official sources to receive notifications about security patches and updates.
2
By following these preventive measures, you can reduce the risk of using vulnerable and outdated
components in your application or system. Regularly updating components, staying informed
about security updates, and conducting security assessments are essential to maintain a secure
software ecosystem.
Regularly update components: Regularly update the components in your application or system
to the latest stable and secure versions. Check for security releases and apply the patches
promptly. Ensure that your update process is well-documented and regularly tested.
3
Utilize vulnerability databases: Make use of vulnerability databases and security resources that
provide information on known vulnerabilities in components. Check these resources regularly
to identify any vulnerabilities in the components you use and take appropriate action.
4
Perform security assessments: Conduct regular security assessments and vulnerability scans
to identify any vulnerabilities introduced by the components. Use automated tools or engage
security professionals to perform security testing and code reviews.
5
Monitor component support: Keep track of the support status of the components you use. If a
component is no longer maintained or has reached its end-of-life, consider finding alternative
components or solutions. Unsupported components are more likely to have unpatched
vulnerabilities.
6
Implement a patch management process: Establish a patch management process to ensure
that security patches and updates are promptly applied to the components. This process
should include testing patches in a controlled environment before deploying them to
production.
7
Consider using security monitoring tools: Implement security monitoring tools that can detect
and alert you about vulnerabilities or potential risks associated with the components you use.
These tools can help you identify any security issues early on and take necessary mitigation
steps.
8
Follow secure coding practices: Develop secure coding practices to minimize the introduction
of vulnerabilities in your own code. Regularly review and update your code to ensure that it
does not rely on vulnerable or outdated components.
9
Include component assessment in the procurement process: When selecting new
components, consider their security track record, update frequency, and community support.
Choose components that have a good reputation for security and are actively maintained.
10
Improper Validation of Certificate with Host Mismatch
Improper Validation of Certificate with Host Mismatch is a security vulnerability that occurs when
a client application fails to properly validate the server’s SSL/TLS certificate during a secure
communication handshake. This vulnerability allows an attacker to impersonate the server by
presenting a certificate that does not match the expected host.
To prevent Improper Validation of Certificate with Host Mismatch, you should follow these
preventive measures:
Properly validate SSL/TLS certificates: Implement a robust certificate validation mechanism in
your client application. Ensure that the SSL/TLS library or framework being used verifies the
certificate chain, expiration date, revocation status, and other relevant fields.
1
Check for host name mismatch: Verify that the common name (CN) or subject alternative
name (SAN) field in the certificate matches the host to which the client is connecting. Perform
a strict comparison and reject the connection if there is a mismatch.
2
Use a trusted certificate authority (CA): Obtain SSL/TLS certificates from reputable CAs that
follow industry best practices for certificate issuance. Trust certificates only from well-known
CAs to reduce the risk of obtaining fraudulent or improperly issued certificates.
3
Implement certificate pinning: Consider implementing certificate pinning, also known as public
key pinning, in your client application. Pinning involves associating a specific server’s public
key or certificate fingerprint with a known and trusted value. This helps prevent certificate
substitution attacks.
4
Stay up to date with CA revocations: Regularly update the list of revoked certificates and
perform certificate revocation checks during the validation process. Check certificate
revocation status using online certificate revocation lists (CRLs) or the Online Certificate
Status Protocol (OCSP).
5
Enable strict SSL/TLS configuration: Configure your SSL/TLS settings to use secure and up-to-
date protocols (e.g., TLS 1.2 or higher) and cryptographic algorithms. Disable deprecated or
weak protocols and algorithms to prevent potential vulnerabilities.
6
Perform thorough testing: Conduct rigorous testing to ensure that certificate validation is
working correctly in your client application. Test scenarios should include cases where
certificates have expired, are revoked, or have host mismatches. Automated security testing
tools can also help identify potential vulnerabilities.
7
Implement user awareness and education: Educate users about the importance of verifying
SSL/TLS certificates and recognizing warning messages related to certificate errors.
8
By following these preventive measures, you can mitigate the risk of Improper Validation of
Certificate with Host Mismatch and ensure secure SSL/TLS connections in your client
applications. Proper certificate validation is crucial for establishing trust and authenticity during
secure communications.
Improper Authentication is a security vulnerability that occurs when an application fails to properly
authenticate and verify the identity of users or entities. This vulnerability allows attackers to
bypass authentication mechanisms and gain unauthorized access to sensitive resources or
perform actions on behalf of other users.
To prevent Improper Authentication, you should follow these preventive measures:
Encourage users to report any suspicious certificate-related issues.
Monitor and log certificate validation errors: Implement logging mechanisms to capture and
monitor SSL/TLS certificate validation errors. Monitor logs for any unexpected or suspicious
activities related to certificate validation.
9
Regularly update SSL/TLS libraries and frameworks: Keep your SSL/TLS libraries and
frameworks up to date with the latest security patches and updates. This ensures that you
have the latest fixes for any known vulnerabilities related to certificate validation.
10
Improper Authentication
Implement strong authentication mechanisms: Use strong authentication methods, such as
multi-factor authentication (MFA), to enhance the security of user authentication. MFA
combines multiple factors, such as passwords, biometrics, or hardware tokens, to verify the
user’s identity.
1
Use secure password policies: Enforce strong password policies that require users to create
complex passwords and regularly update them. Encourage the use of unique passwords for
each application or service and consider implementing password strength indicators.
2
Protect authentication credentials: Safeguard authentication credentials, such as passwords,
tokens, or session IDs, from unauthorized access or disclosure. Use secure storage
mechanisms, such as hashing and encryption, to protect sensitive information related to
authentication.
3
Implement secure session management: Ensure secure session management practices, such
as generating unique session IDs, properly handling session expiration and invalidation, and
using secure transport protocols (e.g., HTTPS) to transmit session-related data.
4
By implementing these preventive measures, you can mitigate the risk of Improper Authentication
and strengthen the security of user authentication in your application or system. Robust
authentication practices are essential to protect user accounts, sensitive data, and ensure that
only authorized individuals can access protected resources.
Session Fixation is a security vulnerability that occurs when an attacker establishes or
manipulates a user’s session identifier (session ID) to gain unauthorized access to the user’s
session. The attacker tricks the user into using a known session ID, which the attacker can then
use to hijack the session.
To prevent Session Fixation, you should follow these preventive measures:
Enforce secure login controls: Implement measures to prevent common attacks, such as
brute-force attacks and credential stuffing. Enforce account lockouts or introduce CAPTCHA
challenges after a certain number of failed login attempts.
5
Implement secure password reset processes: Establish secure password reset processes that
require additional verification steps to confirm the user’s identity. This may include sending a
verification email, asking security questions, or utilizing a secondary authentication factor.
6
Protect against session fixation attacks: Implement measures to prevent session fixation
attacks by regenerating session IDs upon successful authentication, avoiding session ID
propagation in URLs, and restricting the ability to fixate session IDs.
7
Implement secure account recovery: Establish secure procedures for account recovery to
ensure that only authorized users can regain access to their accounts. This may involve
verifying the user’s identity through a multi-step verification process.
8
Regularly update and patch: Keep the authentication mechanisms, libraries, and frameworks
up to date with the latest security patches and updates. Stay informed about any security
advisories or vulnerabilities related to the authentication mechanisms used in your application.
9
Conduct security testing: Perform regular security testing, including vulnerability assessments
and penetration testing, to identify and remediate any authentication-related vulnerabilities.
Test the effectiveness of authentication controls and verify that they cannot be easily
bypassed or exploited.
10
Session Fixation
Regenerate session ID upon authentication: Generate a new session ID for the user upon
successful authentication. This ensures that the user is assigned a different session ID than
the one initially used before authentication.
1
By implementing these preventive measures, you can reduce the risk of Session Fixation and help
ensure the integrity and security of user sessions. Secure session management practices are
essential to protect user accounts and prevent unauthorized access to sensitive data and
functionality.
Use a secure random session ID: Generate session IDs using a strong cryptographic random
number generator. This helps prevent session ID prediction or brute-force attacks where
attackers try to guess valid session IDs.
2
Implement session expiration and inactivity timeouts: Set appropriate session expiration and
inactivity timeouts to limit the lifespan of a session. When a session expires or times out, the
user needs to reauthenticate, preventing the use of old session IDs by attackers.
3
Implement secure session management: Implement secure session management practices,
such as securely transmitting session IDs over encrypted channels (e.g., HTTPS) and avoiding
exposing session IDs in URLs.
4
Avoid session ID disclosure: Avoid including session IDs in URLs, logs, or other client-side
visible locations. Exposing session IDs increases the risk of session fixation attacks as
attackers can easily obtain valid session IDs.
5
Use cookie attributes: Set secure attributes for session cookies, such as the “Secure” flag to
ensure they are only transmitted over HTTPS, and the “HttpOnly” flag to prevent client-side
scripts from accessing the cookie.
6
Conduct user awareness and education: Educate users about session security best practices,
such as the importance of logging out after using shared or public devices and being cautious
of session ID manipulation attempts.
7
Implement IP validation: Consider implementing IP validation checks as an additional security
measure. Verify that the IP address of the user’s requests remains consistent throughout the
session. This can help detect and prevent session hijacking attempts.
8
Monitor session activity: Monitor session activity and log events related to session creation,
expiration, and invalidation. Monitor for unusual session behavior, such as simultaneous
sessions from different locations or devices.
9
Regularly update and patch: Keep your web application and session management components
up to date with the latest security patches and updates. Stay informed about any security
advisories or vulnerabilities related to session management in your application framework or
libraries.
10
Inclusion of Functionality from Untrusted Control, also known as Remote Code Execution (RCE), is
a security vulnerability that occurs when an application incorporates and executes code from an
untrusted or external source without proper validation or security measures. This vulnerability
allows attackers to execute arbitrary code on the target system, potentially leading to
unauthorized access, data breaches, or system compromise.
To prevent the Inclusion of Functionality from Untrusted Control, you should follow these
preventive measures:
Inclusion of Functionality from Untrusted Control
Avoid dynamic code execution: Minimize or avoid executing code from untrusted sources
whenever possible. Limit the execution of code to trusted and well-defined components within
your application.
1
Implement strict input validation: Validate and sanitize all user inputs and external data before
using them in dynamic code execution. Apply input validation techniques such as whitelisting,
blacklisting, or input filtering to ensure only safe and expected inputs are processed.
2
Use safe alternatives for dynamic code execution: If dynamic code execution is necessary,
consider using safe alternatives, such as predefined functions or libraries with built-in security
measures. Avoid using functions or features that allow arbitrary code execution or evaluation.
3
Implement strong access controls: Apply strict access controls and permissions to limit the
execution of code or the inclusion of functionality to trusted and authorized sources only.
Restrict access to critical system resources and prevent unauthorized code execution.
4
Isolate untrusted code: If you need to execute untrusted code, isolate it in a sandboxed or
restricted environment with limited privileges. Use technologies like containers or virtual
machines to create isolated execution environments.
5
Implement code signing and verification: Digitally sign your code and verify the integrity and
authenticity of external components before including or executing them. This helps ensure that
the code comes from a trusted source and has not been tampered with.
6
Regularly update and patch: Keep your application, libraries, and frameworks up to date with
the latest security patches and updates. Stay informed about any security advisories or
vulnerabilities related to the components used in your application.
7
Perform security testing: Conduct regular security testing, including static code analysis,
dynamic analysis, and penetration testing, to identify and mitigate vulnerabilities related to the
8
By implementing these preventive measures, you can reduce the risk of Inclusion of Functionality
from Untrusted Control and enhance the security of your application. Proper validation, access
controls, and secure coding practices are essential to mitigate the risks associated with executing
code from untrusted sources.
Download of Code Without Integrity Check is a security vulnerability that occurs when code or
files are downloaded from a remote source without verifying their integrity. This vulnerability
allows attackers to manipulate or replace the downloaded code, leading to potential injection of
malicious code or unauthorized modifications.
To prevent Download of Code Without Integrity Check, you should follow these preventive
measures:
inclusion of untrusted functionality. Test for code injection and RCE vulnerabilities to ensure
the application can withstand potential attacks.
Implement secure coding practices: Follow secure coding practices, such as input validation,
output encoding, and secure configuration management, to minimize the risk of code injection
vulnerabilities. Train your development team on secure coding practices to build a robust and
secure application.
9
Implement a Web Application Firewall (WAF): Consider using a WAF that can detect and block
malicious code injection attempts. WAFs can provide an additional layer of protection by
inspecting incoming requests and filtering out potentially dangerous code.
10
Download of Code Without Integrity Check
Implement code signing: Digitally sign the code or files you distribute or download. Code
signing ensures that the code or files have not been tampered with and come from a trusted
source. Verify the digital signatures before executing or using the downloaded code.
1
Use secure and trusted sources: Obtain code or files from trusted and reputable sources.
Avoid downloading code or files from untrusted or unknown sources. Trusted sources provide
assurance of the integrity and authenticity of the code.
2
Verify checksums or hashes: Provide checksums or hashes (e.g., MD5, SHA-256) for the
downloaded code or files. Before using the downloaded content, calculate the checksum or
hash of the file and compare it with the provided value. If they match, it indicates that the file
has not been altered during the download process.
3
Use secure protocols: Download code or files using secure protocols such as HTTPS, which
provides encryption and integrity checks during transmission. Secure protocols help prevent
4
By implementing these preventive measures, you can reduce the risk of Download of Code
Without Integrity Check and ensure that the downloaded code or files are trustworthy and have
not been tampered with. Verifying integrity, using secure sources, and implementing secure
coding practices are critical for maintaining the integrity and security of downloaded code or files.
Deserialization of Untrusted Data is a security vulnerability that occurs when untrusted or
malicious data is deserialized by an application without proper validation and safeguards.
Deserialization vulnerabilities can lead to various attacks, such as remote code execution,
injection of malicious objects, or data tampering.
To prevent Deserialization of Untrusted Data, you should follow these preventive measures:
tampering or interception of the downloaded content.
Perform file integrity checks: Implement file integrity checks after the download process. This
can include comparing the downloaded code or files against a known good version or using file
integrity monitoring tools to detect any unauthorized modifications.
5
Regularly update and patch: Keep the software or application that handles the downloading
process up to date with the latest security patches and updates. Security vulnerabilities in the
download functionality can be addressed through software updates.
6
Implement secure coding practices: Follow secure coding practices when developing the code
that handles the download process. Input validation, secure file handling, and secure network
communication should be considered to prevent code injection or tampering during the
download.
7
Implement strong access controls: Restrict access to the download functionality and ensure
that only authorized users or systems can initiate or access the download process. Implement
proper authentication and authorization mechanisms to prevent unauthorized downloads.
8
Perform security testing: Conduct regular security testing, including vulnerability scanning and
penetration testing, to identify potential weaknesses or vulnerabilities in the download
functionality. Test for code injection, tampering, or unauthorized file replacement scenarios.
9
Educate users: Educate users about the importance of downloading code or files from trusted
sources and the risks associated with downloading from untrusted or unknown sources.
Encourage users to verify the integrity of downloaded files using provided checksums or
hashes.
10
Deserialization of Untrusted Data
By implementing these preventive measures, you can mitigate the risk of Deserialization of
Untrusted Data and protect your application from potential attacks. Validating inputs, using
Implement input validation: Validate and sanitize all inputs, including serialized data, before
deserialization. Apply strict input validation to ensure that only expected and safe data is
processed.
1
Use secure deserialization libraries: Utilize secure and trusted deserialization libraries or
frameworks that provide built-in protections against common deserialization vulnerabilities.
These libraries often include features like input filtering, type checking, or automatic validation.
2
Implement whitelisting: Define and enforce a whitelist of allowed classes or types during
deserialization. Restrict the deserialization process to only known and trusted classes,
preventing the instantiation of potentially malicious or unexpected objects.
3
Implement integrity checks: Include integrity checks or digital signatures within the serialized
data. Verify the integrity of the serialized data before deserialization to ensure that it has not
been tampered with or modified.
4
Isolate deserialization functionality: Isolate the deserialization process in a separate and
controlled environment. Use mechanisms like sandboxes, containers, or restricted execution
environments to mitigate the impact of any potential deserialization vulnerabilities.
5
Enforce strict access controls: Limit access to deserialization functionality to only authorized
components or systems. Implement proper authentication and authorization mechanisms to
prevent unauthorized deserialization.
6
Implement secure defaults: Configure deserialization settings with secure defaults. Disable or
minimize the use of dangerous deserialization features or options that may introduce security
risks.
7
Update deserialization libraries: Keep deserialization libraries or frameworks up to date with
the latest security patches and updates. Stay informed about any security advisories or
vulnerabilities related to the deserialization components used in your application.
8
Perform security testing: Conduct thorough security testing, including static analysis, dynamic
analysis, and penetration testing, to identify and remediate deserialization vulnerabilities. Test
for deserialization attacks, such as object injection or remote code execution.
9
Educate developers: Provide training and guidance to developers on secure coding practices,
emphasizing the importance of proper validation and handling of deserialized data. Encourage
developers to follow best practices for secure deserialization.
10
secure libraries, implementing access controls, and maintaining up-to-date software are essential
steps to prevent deserialization vulnerabilities.
Insufficient Logging is a security vulnerability that occurs when an application fails to generate or
retain sufficient logs to detect and investigate security incidents. Inadequate logging can hinder
incident response efforts, making it difficult to identify and analyze security events or suspicious
activities.
To prevent Insufficient Logging, you should follow these preventive measures:
Insufficient Logging
Implement comprehensive logging: Ensure that your application logs relevant security-related
events and activities. Log information such as user authentication attempts, access control
failures, critical application actions, input validation errors, and any other security-sensitive
events.
1
Include contextual information: Log additional contextual information that can aid in incident
investigation, such as user IDs, timestamps, source IP addresses, affected resources, and
relevant request/response data. This information can assist in understanding the scope and
impact of security incidents.
2
Set appropriate log levels: Define appropriate log levels for different types of events, ranging
from debug and informational messages to more critical error and warning logs. Use log levels
consistently to capture both routine and exceptional events.
3
Ensure log storage and retention: Set up sufficient storage capacity to retain logs for an
adequate period, considering compliance requirements and incident response needs. Retain
logs for a timeframe that allows for timely incident detection, response, and forensic analysis.
4
Encrypt and protect logs: Apply encryption mechanisms to protect log files at rest and during
transit. Properly configure file permissions and access controls to prevent unauthorized
access to log files. Protect log files from tampering or deletion by employing file integrity
monitoring or secure log management systems.
5
Monitor log files: Regularly monitor log files for any suspicious or unexpected activities.
Implement automated log analysis and intrusion detection systems to detect security events,
anomalies, or patterns indicative of potential attacks.
6
Implement centralized log management: Centralize log storage and management in a
dedicated log server or security information and event management (SIEM) system.
7
By implementing these preventive measures, you can enhance your application’s logging
capabilities, facilitate incident detection and response, and improve your overall security posture.
Comprehensive and secure logging practices play a vital role in detecting and investigating
security incidents, aiding in timely incident response, and facilitating forensic analysis when
necessary.
Improper Output Neutralization for Logs, also known as Log Injection, is a security vulnerability
that occurs when untrusted user input is not properly sanitized or neutralized before being
included in log statements. This can lead to log forging, injection of malicious content, or the
disclosure of sensitive information within log files.
To prevent Improper Output Neutralization for Logs, you should follow these preventive measures:
Centralization enables correlation and analysis of logs from multiple sources, improving
incident detection and response capabilities.
Perform log analysis and reporting: Regularly analyze log data for security insights, trends, or
anomalies. Create customized reports or dashboards that provide a summary of important
security-related events. Identify areas for improvement or potential security weaknesses
based on log analysis results.
8
Implement log integrity checks: Implement mechanisms to detect and alert on any tampering
or modification of log files. Use digital signatures, checksums, or secure logging frameworks
to ensure the integrity of log data.
9
Regularly review and update logging practices: Continuously review and update your logging
practices based on evolving security requirements and industry best practices. Stay informed
about emerging threats and logging-related vulnerabilities to ensure your logging mechanisms
remain effective.
10
Improper Output Neutralization for Logs
Apply proper input validation and sanitization: Treat log messages as untrusted user input and
validate and sanitize any user-controlled data before including it in log statements. Remove or
escape characters that could be interpreted as control characters or log syntax.
1
Use secure logging frameworks: Utilize logging frameworks that provide built-in mechanisms
for proper output neutralization. These frameworks often include features like parameterized
logging or context-specific escaping, which can help prevent log injection vulnerabilities.
2
Avoid concatenation of untrusted data: Do not concatenate untrusted user input directly into
log statements. Instead, use placeholder values or formatting options provided by the logging
3
By implementing these preventive measures, you can mitigate the risk of Improper Output
Neutralization for Logs and ensure that your log files remain reliable, accurate, and free from
malicious content. Proper input validation, secure logging frameworks, context-specific output
encoding, and regular log monitoring are essential steps to prevent log injection vulnerabilities.
Omission of Security-relevant Information is a security vulnerability that occurs when an
application fails to log or report important security-related events or incidents. This omission can
framework to ensure proper neutralization of user-controlled data.
Implement context-specific output encoding: If the logging framework does not provide
automatic neutralization mechanisms, implement context-specific output encoding to prevent
injection attacks. Use the appropriate encoding technique based on the log format and syntax,
such as HTML entity encoding or URL encoding.
4
Limit the verbosity of log messages: Be mindful of the information logged and avoid including
sensitive data in log statements. Only log the necessary details required for troubleshooting or
auditing purposes, while excluding sensitive information like passwords, Personally Identifiable
Information (PII), or authentication tokens.
5
Configure log file permissions: Ensure that log files have appropriate permissions to restrict
unauthorized access. Restrict read and write permissions to only authorized users or system
processes. Regularly monitor and manage access control settings for log files.
6
Implement centralized log management: Centralize log storage and management in a
dedicated log server or a Security Information and Event Management (SIEM) system.
Centralization allows for better control, monitoring, and analysis of log data, minimizing the risk
of log injection and facilitating detection of suspicious activities.
7
Regularly monitor and review logs: Regularly review log files for any signs of log injection
attempts or suspicious log entries. Implement automated log analysis and intrusion detection
systems to identify potential log injection attacks or anomalous log patterns.
8
Keep logging frameworks up to date: Keep your logging frameworks and libraries up to date
with the latest security patches and updates. Stay informed about any security advisories or
vulnerabilities related to the logging components used in your application.
9
Educate developers: Provide training and guidance to developers on secure coding practices
for logging. Emphasize the importance of proper input validation, output neutralization, and
the risks associated with log injection vulnerabilities.
10
Omission of Security-relevant Information
result in a lack of visibility into potential security threats or the inability to detect and respond to
security incidents in a timely manner.
To prevent the Omission of Security-relevant Information, you should follow these preventive
measures:
Identify security-relevant events: Determine the types of security-related events that are
crucial for monitoring and detection within your application. This may include failed login
attempts, access control failures, suspicious activities, or any other security-related incidents
specific to your application and environment.
1
Implement comprehensive logging: Ensure that your application logs all identified security-
relevant events. Log the necessary details such as timestamps, user information, affected
resources, and relevant context that can assist in incident investigation and response.
2
Set appropriate log levels: Define appropriate log levels for different security events based on
their criticality. Use log levels consistently to ensure that security-relevant events are captured
and logged accordingly.
3
Implement centralized log management: Centralize log storage and management in a
dedicated log server or a Security Information and Event Management (SIEM) system.
Centralization allows for better visibility, correlation, and analysis of security events across
your application or infrastructure.
4
Regularly review and analyze logs: Establish a routine practice of reviewing and analyzing logs
for security events and incidents. Assign responsibility to a designated team or individual to
regularly monitor and analyze log data for any potential security threats or anomalies.
5
Implement log retention policies: Define log retention policies that align with your compliance
requirements and incident response needs. Retain logs for an appropriate period to ensure
that historical data is available for security investigations or forensic analysis.
6
Automate log analysis: Implement automated log analysis tools or intrusion detection systems
to assist in the detection of security events or anomalies. Use these tools to monitor log files in
real-time and generate alerts or notifications for potential security incidents.
7
Implement real-time monitoring: Use real-time monitoring techniques to actively track and
respond to security events as they occur. Implement mechanisms such as log streaming, event
triggers, or alerting systems to ensure prompt notifications and response to security incidents.
8
Perform regular security assessments: Conduct regular security assessments and penetration
testing to identify any gaps or vulnerabilities in your application’s logging and monitoring
9
By implementing these preventive measures, you can ensure that security-relevant information is
properly logged and reported, enabling effective detection and response to security incidents.
Comprehensive and accurate logging practices are essential for maintaining the security of your
application and infrastructure, facilitating incident investigations, and supporting compliance
requirements.
Sensitive Information into Log File refers to the unintentional logging or inclusion of sensitive data
within log files. This can occur when application logs capture and store sensitive information such
as passwords, credit card numbers, personally identifiable information (PII), or any other
confidential data. Storing sensitive information in log files poses a significant security risk as it
increases the potential for unauthorized access, data leakage, and compliance violations.
To prevent the inclusion of sensitive information into log files, consider the following preventive
measures:
capabilities. Use the results of these assessments to make necessary improvements and
address any security weaknesses.
Stay updated with security best practices: Stay informed about the latest security best
practices, frameworks, and guidelines related to logging and security monitoring. Regularly
update your logging mechanisms and practices to align with industry standards and emerging
security threats.
10
Sensitive Information into Log File
Implement a logging policy: Define a logging policy that explicitly prohibits the logging of
sensitive information. Clearly outline what types of data should not be included in log files and
educate developers and system administrators about the policy.
1
Apply proper data sanitization: Implement proper data sanitization techniques to prevent
sensitive information from being logged inadvertently. Develop a logging framework or use
existing libraries that automatically redact or obfuscate sensitive data before logging. Apply
techniques such as masking, truncation, or encryption to protect sensitive information.
2
Utilize appropriate log levels: Ensure that sensitive information is not logged at inappropriate
log levels. Set log levels in a way that sensitive data is not included in logs intended for
debugging, development, or general information purposes. Properly categorize log levels
based on the sensitivity of the information being logged.
3
Avoid logging sensitive input parameters: Exercise caution when logging input parameters,
especially if they contain sensitive data. If necessary, consider logging only non-sensitive
4
By implementing these preventive measures, you can reduce the risk of sensitive information
being unintentionally logged and stored in log files. Taking proactive steps to protect the
confidentiality and integrity of log data helps maintain compliance with data protection
regulations, mitigates the risk of data breaches, and preserves the privacy of sensitive
information.
Server-Side Request Forgery (SSRF) is a vulnerability that allows an attacker to manipulate the
server-side functionality of an application to make arbitrary requests on behalf of the server. The
attacker typically exploits this vulnerability to interact with internal resources, perform port
portions of the input data or use a whitelist approach to explicitly exclude sensitive fields from
being logged.
Implement log filtering: Apply log filtering mechanisms to remove or obfuscate sensitive
information from log files. Use regular expressions or predefined patterns to detect and filter
out sensitive data before it is stored in log files. Regularly review and update the filtering rules
as necessary.
5
Use secure logging storage: Ensure that log files are stored securely with appropriate access
controls. Limit access to log files to authorized personnel only. Implement encryption or
encryption at rest mechanisms to protect log files from unauthorized access or disclosure.
6
Regularly review log files: Perform regular log file reviews to identify any instances of sensitive
information being logged. Implement automated log analysis tools or manual inspection
techniques to detect and remediate any inadvertent logging of sensitive data.
7
Pseudonymize or anonymize data: If there is a need to log certain sensitive information for
debugging or analysis purposes, consider pseudonymizing or anonymizing the data. Replace
actual sensitive values with pseudonyms or anonymized identifiers to protect the privacy and
confidentiality of the data.
8
Establish proper access controls: Implement strict access controls for log files, including file
permissions and user authentication mechanisms. Only grant access to log files to authorized
individuals who require it for operational or security purposes.
9
Train and educate personnel: Provide training and education to developers, system
administrators, and other personnel involved in log file management. Raise awareness about
the risks associated with logging sensitive information and promote best practices for secure
logging.
10
Server-Side Request Forgery (SSRF)
scanning, or make requests to other external systems. SSRF attacks can lead to sensitive data
exposure, unauthorized access to internal resources, and potential remote code execution.
To prevent Server-Side Request Forgery (SSRF) vulnerabilities, consider the following preventive
measures:
Input validation and whitelisting: Implement strong input validation and enforce strict
whitelisting of allowed URLs or domains. Validate and sanitize user-supplied input, such as
URLs or IP addresses, to prevent injection of malicious or unexpected values. Use a whitelist of
trusted domains or IP addresses that the server is allowed to communicate with.
1
Restrict network access: Configure network firewalls and security groups to restrict outbound
network access from the server. Only allow connections to necessary resources and services,
blocking access to internal or sensitive systems that should not be accessed by the server.
2
Use secure protocols and APIs: When making outgoing requests, use secure protocols such as
HTTPS to communicate with external systems. Validate the SSL/TLS certificates of the target
servers to ensure the integrity and authenticity of the communication. Avoid using insecure or
deprecated protocols and APIs that may be vulnerable to SSRF attacks.
3
Isolate server components: Utilize network segmentation and isolate server components to
prevent direct access to internal resources. Place servers in separate network segments or
subnets, and restrict their access to only necessary resources and services.
4
Configure strong server-side controls: Implement server-side controls to prevent SSRF
attacks. This may include implementing allowlists of allowed protocols, ports, and domains, as
well as enforcing appropriate security policies at the server level.
5
Implement request validation and filtering: Validate and filter user-supplied URLs and input to
ensure they conform to expected patterns and protocols. Consider using security libraries or
frameworks that provide built-in protection against SSRF attacks, such as URL validation and
sanitization functions.
6
Least privilege principle: Ensure that the server’s permissions and privileges are limited to
what is necessary for its intended functionality. Avoid running the server with excessive
privileges or accessing sensitive resources that are not required for its operation.
7
Secure session management: Implement secure session management practices, including
strong session identifiers, session expiration, and secure session storage. This helps prevent
attackers from leveraging SSRF vulnerabilities to hijack active sessions or perform
unauthorized actions.
8
By implementing these preventive measures, you can significantly reduce the risk of SSRF
vulnerabilities and protect your application from unauthorized access to internal resources and
potential data breaches. It is important to adopt a security-first mindset throughout the
application development lifecycle and regularly assess and enhance the security posture of your
systems.
Copyright © 2019-2023 HADESS.
Regular security updates and patches: Keep server software, libraries, and frameworks up to
date with the latest security patches and updates. SSRF vulnerabilities can be present in
various components, including web servers, frameworks, or third-party libraries. Regularly
monitor and apply security updates to mitigate known vulnerabilities.
9
Perform security testing and code review: Conduct regular security testing, including
vulnerability scanning and penetration testing, to identify and remediate SSRF vulnerabilities.
Additionally, perform code reviews to identify potential SSRF-prone code patterns and ensure
secure coding practices are followed.
10
DevSecOps Guides
Attacks / Cloud Attacks
Weak or misconfigured access controls, improper user privilege management, or lack of strong
authentication mechanisms can lead to unauthorized access and privilege escalation.
In the noncompliant code, there is inadequate Identity, Credential, and Access Management
(ICAM) in the cloud environment. This means that user identities, credentials, and access controls
are not properly managed, increasing the risk of unauthorized access, privilege escalation, and
potential data breaches.
Cloud Attacks
TABLE OF CONTENTS
Inadequate Identity, Credential, and Access Management (ICAM):
1
Insecure Interfaces and APIs
2
Data Breaches
3
Insufficient Security Configuration
4
Insecure Data storage
5
Lack of Proper Logging and Monitoring
6
Insecure Deployment and Configuration Management
7
Inadequate Incident Response and Recovery
8
Shared Technology Vulnerabilities
9
Account Hijacking and Abuse
10
Inadequate Identity, Credential, and Access Management (ICAM):
# Noncompliant: Inadequate ICAM in Cloud
resources:
  - name: my-bucket
    type: storage.bucket
To address the inadequate ICAM in the cloud environment, it is essential to implement robust
identity, credential, and access management practices.
  - name: my-instance
    type: compute.instance
  - name: my-database
    type: sql.database
  # Access control rules are missing or insufficiently defined
# Compliant: Enhanced ICAM in Cloud
resources:
  - name: my-bucket
    type: storage.bucket
    access-control:
      - role: storage.admin
        members:
          - user:john@example.com
          - group:engineering@example.com
  - name: my-instance
    type: compute.instance
    access-control:
      - role: compute.admin
        members:
          - user:john@example.com
          - group:engineering@example.com
  - name: my-database
    type: sql.database
    access-control:
      - role: cloudsql.admin
        members:
In the compliant code, each resource in the cloud environment has an associated access control
configuration. This includes properly defined roles and membership assignments, ensuring that
only authorized users or groups have access to the respective resources. By implementing
adequate ICAM practices, the risk of unauthorized access and privilege escalation is significantly
reduced, enhancing the overall security of the cloud environment.
Vulnerabilities in cloud service interfaces and APIs can be exploited to gain unauthorized access,
inject malicious code, or manipulate data.
In the noncompliant code, there are insecure interfaces and APIs in the cloud environment. This
means that the interfaces and APIs used to interact with cloud services are not properly secured,
potentially exposing sensitive data, allowing unauthorized access, or enabling malicious activities.
To address the insecure interfaces and APIs in the cloud environment, it is crucial to implement
secure practices when interacting with cloud services.
          - user:john@example.com
          - group:engineering@example.com
Insecure Interfaces and APIs
# Noncompliant: Insecure Interfaces and APIs in Cloud
import requests
# Insecure API endpoint without proper authentication and authorization
api_endpoint = "http://api.example.com/data"
response = requests.get(api_endpoint)
# Insecure interface with plaintext transmission of sensitive data
def process_data(data):
    # ... logic to process data ...
    # Insecure transmission of processed data over HTTP
    requests.post("http://example.com/process", data=data)
In the compliant code, the API endpoint is accessed securely using HTTPS and includes proper
authentication and authorization headers. This ensures that only authorized users can access the
API and the data transmitted is protected. Additionally, the interface for processing data utilizes
encrypted transmission over HTTPS, providing confidentiality and integrity for the sensitive
information being transmitted. By implementing secure interfaces and APIs, the risk of
unauthorized access, data breaches, and malicious activities is mitigated in the cloud
environment.
Sensitive data stored in the cloud can be compromised due to misconfigurations, insecure
storage, weak encryption, or insider threats.
Misconfigurations in cloud services, infrastructure, or security settings can expose vulnerabilities,
allowing unauthorized access or compromising data integrity.
# Compliant: Secure Interfaces and APIs in Cloud
import requests
# Secure API endpoint with proper authentication and authorization
api_endpoint = "https://api.example.com/data"
headers = {"Authorization": "Bearer <access_token>"}
response = requests.get(api_endpoint, headers=headers)
# Secure interface with encrypted transmission of sensitive data
def process_data(data):
    # ... logic to process data ...
    # Secure transmission of processed data over HTTPS
    requests.post("https://example.com/process", data=data, verify=True)
Data Breaches
Insufficient Security Configuration
In the noncompliant code, there are several instances where security configurations are
insufficient, leaving the cloud environment vulnerable to attacks. These include using default or
weak passwords, allowing unrestricted access to resources, and not enabling necessary security
features.
To address the issue of insufficient security configuration in the cloud, it is important to follow
security best practices and implement robust security measures.
# Noncompliant: Insufficient Security Configuration in Cloud
import boto3
# Using default or weak passwords for authentication
s3 = boto3.resource('s3')
bucket = s3.Bucket('my-bucket')
bucket.upload_file('data.txt', 'data.txt')
# Allowing unrestricted access to resources
s3 = boto3.resource('s3')
bucket = s3.Bucket('public-bucket')
bucket.make_public()
# Not enabling necessary security features
ec2 = boto3.resource('ec2')
instance = ec2.create_instances(ImageId='ami-12345678', MinCount=1, MaxCount=1)
instance[0].disable_api_termination = False
# Compliant: Strong Security Configuration in Cloud
import boto3
# Using strong and unique passwords for authentication
s3 = boto3.resource('s3')
bucket = s3.Bucket('my-bucket')
bucket.upload_file('data.txt', 'data.txt', ExtraArgs={'ServerSideEncryption': 'AES256'})
# Restricting access to resources
s3 = boto3.resource('s3')
In the compliant code, strong and unique passwords are used for authentication, enhancing the
security of the cloud resources. Access to resources is restricted, ensuring that only authorized
users or services have the necessary permissions. Necessary security features, such as server-
side encryption and API termination protection, are enabled to provide additional layers of
security. By implementing strong security configurations, the cloud environment is better
protected against potential threats.
Inadequate encryption, weak access controls, or improper handling of data at rest can lead to
unauthorized access or data leakage.
In the noncompliant code, there are instances where data storage in the cloud is insecure.
Sensitive data is stored without proper encryption, and there is no mechanism in place to protect
the data from unauthorized access or accidental exposure.
bucket = s3.Bucket('private-bucket')
bucket.Acl().put(ACL='private')
# Enabling necessary security features
ec2 = boto3.resource('ec2')
instance = ec2.create_instances(ImageId='ami-12345678', MinCount=1, MaxCount=1)
instance[0].disable_api_termination = True
Insecure Data storage
# Noncompliant: Insecure Data Storage in Cloud
import boto3
# Storing sensitive data without encryption
s3 = boto3.client('s3')
s3.put_object(Bucket='my-bucket', Key='data.txt', Body='Sensitive data')
# Lack of access control
s3 = boto3.resource('s3')
bucket = s3.Bucket('public-bucket')
bucket.upload_file('data.txt', 'data.txt')
# No data backup or disaster recovery plan
To ensure secure data storage in the cloud, it is important to follow best practices and implement
appropriate security measures.
In the compliant code, sensitive data is stored with encryption using server-side encryption with
AES256. Access control is implemented to restrict access to the stored data, ensuring that only
authorized users or services can access it. Additionally, a data backup and disaster recovery plan
is in place, which includes creating snapshots to enable data recovery in case of any incidents. By
implementing secure data storage practices, the cloud environment provides better protection for
sensitive information.
Insufficient monitoring, logging, and analysis of cloud activity can hinder detection of security
incidents, leading to delayed or ineffective response.
rds = boto3.client('rds')
rds.create_db_snapshot(DBSnapshotIdentifier='my-snapshot', DBInstanceIdentifier='my-db')
# Compliant: Secure Data Storage in Cloud
import boto3
# Storing sensitive data with encryption
s3 = boto3.client('s3')
s3.put_object(Bucket='my-bucket', Key='data.txt', Body='Sensitive data', ServerSideEncryption='AE
# Implementing access control
s3 = boto3.resource('s3')
bucket = s3.Bucket('private-bucket')
bucket.upload_file('data.txt', 'data.txt', ExtraArgs={'ACL': 'private'})
# Implementing data backup and disaster recovery plan
rds = boto3.client('rds')
rds.create_db_snapshot(DBSnapshotIdentifier='my-snapshot', DBInstanceIdentifier='my-db', Tags=[{'
Lack of Proper Logging and Monitoring
Insecure Deployment and Configuration Management
Weaknesses in the process of deploying and managing cloud resources, such as improper change
management, can introduce security vulnerabilities.
In the noncompliant code, there is a lack of secure deployment and configuration management
practices in the cloud environment. The code deploys resources and configurations without
proper security considerations, such as exposing sensitive information or using default and weak
configurations.
To ensure secure deployment and configuration management in the cloud, it is important to follow
security best practices and apply appropriate configurations to resources.
# Noncompliant: Insecure Deployment and Configuration Management in Cloud
import boto3
def deploy_instance():
    ec2_client = boto3.client('ec2')
    response = ec2_client.run_instances(
        ImageId='ami-12345678',
        InstanceType='t2.micro',
        KeyName='my-keypair',
        SecurityGroupIds=['sg-12345678'],
        UserData='some user data',
        MinCount=1,
        MaxCount=1
    )
    return response['Instances'][0]['InstanceId']
def main():
    instance_id = deploy_instance()
    print(f"Instance deployed with ID: {instance_id}")
if __name__ == "__main__":
    main()
# Compliant: Secure Deployment and Configuration Management in Cloud
import boto3
def deploy_instance():
    ec2_client = boto3.client('ec2')
    response = ec2_client.run_instances(
        ImageId='ami-12345678',
        InstanceType='t2.micro',
        KeyName='my-keypair',
        SecurityGroupIds=['sg-12345678'],
        UserData='some user data',
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'MyInstance'
                    }
                ]
            }
        ],
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'VolumeSize': 30,
                    'VolumeType': 'gp2'
                }
            }
        ]
    )
    return response['Instances'][0]['InstanceId']
def main():
    instance_id = deploy_instance()
    print(f"Instance deployed with ID: {instance_id}")
In the compliant code, additional security measures are implemented during the deployment
process. This includes:
Adding appropriate tags to the instance for better resource management and identification.
Configuring block device mappings with appropriate volume size and type.
Following the principle of least privilege by providing only necessary permissions to the
deployment process.
Lack of proper incident response planning and testing, as well as ineffective recovery
mechanisms, can result in extended downtime, data loss, or inadequate mitigation of security
breaches.
In the noncompliant code, there is a lack of adequate incident response and recovery practices in
the cloud environment. The code does not have any provisions for handling incidents or
recovering from them effectively. This can lead to prolonged downtime, data loss, or inadequate
response to security breaches or system failures.
if __name__ == "__main__":
    main()
•
•
•
Inadequate Incident Response and Recovery
# Noncompliant: Inadequate Incident Response and Recovery in Cloud
import boto3
def delete_instance(instance_id):
    ec2_client = boto3.client('ec2')
    response = ec2_client.terminate_instances(
        InstanceIds=[instance_id]
    )
    return response
def main():
    instance_id = 'i-12345678'
    delete_instance(instance_id)
    print(f"Instance {instance_id} deleted.")
To ensure adequate incident response and recovery in the cloud, it is important to have well-
defined processes and procedures in place. The following code snippet demonstrates a more
compliant approach:
In the compliant code, an additional function handle_incident() is introduced to handle incidents
appropriately. This function can be customized to include actions such as notifying the security
team, logging relevant information, triggering automated response mechanisms, or invoking
incident response plans. By having a well-defined incident response process, organizations can
if __name__ == "__main__":
    main()
# Compliant: Adequate Incident Response and Recovery in Cloud
import boto3
def delete_instance(instance_id):
    ec2_client = boto3.client('ec2')
    response = ec2_client.terminate_instances(
        InstanceIds=[instance_id]
    )
    return response
def handle_incident(instance_id):
    # Perform necessary actions to handle the incident, such as notifying the security team, logg
    print(f"Incident occurred with instance {instance_id}. Taking appropriate actions.")
def main():
    instance_id = 'i-12345678'
    handle_incident(instance_id)
    delete_instance(instance_id)
    print(f"Instance {instance_id} deleted.")
if __name__ == "__main__":
    main()
effectively respond to and recover from incidents, minimizing their impact on operations and
security.
Vulnerabilities in underlying cloud infrastructure, shared components, or hypervisors can impact
multiple cloud tenants, potentially leading to unauthorized access or data breaches.
Unauthorized access to cloud accounts, compromised user credentials, or misuse of privileges
can result in data loss, service disruptions, or unauthorized resource consumption.
In the noncompliant code, there are no security measures in place to prevent account hijacking
and abuse in the cloud environment. The code does not implement strong authentication
mechanisms, lacks proper access controls, and does not enforce secure practices, making it
vulnerable to unauthorized access and abuse of resources.
To prevent account hijacking and abuse in the cloud, it is important to implement strong security
measures. The following code snippet demonstrates a more compliant approach:
Shared Technology Vulnerabilities
Account Hijacking and Abuse
# Noncompliant: Account Hijacking and Abuse in Cloud
import boto3
def create_s3_bucket(bucket_name):
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=bucket_name)
def main():
    bucket_name = 'my-bucket'
    create_s3_bucket(bucket_name)
    print(f"S3 bucket {bucket_name} created.")
if __name__ == "__main__":
    main()
# Compliant: Preventing Account Hijacking and Abuse in Cloud
In the compliant code, additional security measures are implemented. The bucket is created with
a specific access control setting (ACL=’private’) to ensure that only authorized users can access
it. The CreateBucketConfiguration parameter is used to specify the desired region for the bucket,
reducing the risk of accidental exposure due to misconfigurations.
To further enhance security, consider implementing multi-factor authentication (MFA), strong
password policies, and role-based access controls (RBAC) for managing user permissions in the
cloud environment. Regular monitoring and auditing of account activities can also help detect and
prevent unauthorized access or abuse.
Copyright © 2019-2023 HADESS.
import boto3
def create_s3_bucket(bucket_name):
    s3_client = boto3.client('s3')
    s3_client.create_bucket(
        Bucket=bucket_name,
        ACL='private',  # Set appropriate access control for the bucket
        CreateBucketConfiguration={
            'LocationConstraint': 'us-west-2'  # Specify the desired region for the bucket
        }
    )
def main():
    bucket_name = 'my-bucket'
    create_s3_bucket(bucket_name)
    print(f"S3 bucket {bucket_name} created.")
if __name__ == "__main__":
    main()
DevSecOps Guides
Attacks / Container Attacks
Using container images that contain vulnerable or outdated software components, which can be
exploited by attackers. Example: A container image that includes a vulnerable version of a web
server software.
docker-network-bridge- ipv6:0.0.2 docker-network-bridge- ipv6:0.0.1 docker-network-ipv6:0.0.12
ubuntu:latest ubuntu:latest ubuntu:18.04 busybox:latest alpine: latest alpine-curl xmrig:latest
alpine: 3.13 dockgeddon: latest tornadorangepwn:latest jaganod: latest redis: latest gin: latest
(built on host) dockgeddon:latest fcminer: latest debian:latest borg:latest
docked:latestk8s.gcr.io/pause:0.8 dockgeddon:latest stage2: latest dockerlan:latest wayren:latest
Container Attacks
TABLE OF CONTENTS
Insecure Container Images:
1
Malicious Images via Aqua
a
Other Images
b
Privileged Container:
2
Exposed Container APIs:
3
Container Escape:
4
Container Image Tampering:
5
Insecure Container Configuration:
6
Denial-of-Service (DoS):
7
Kernel Vulnerabilities:
8
Shared Kernel Exploitation:
9
Insecure Container Orchestration:
10
Insecure Container Images:
Malicious Images via Aqua
basicxmr:latest simpledockerxmr:latest wscopescan:latest small: latest app:latest Monero-miner:
latest utnubu:latest vbuntu:latest swarm-agents:latest scope: 1.13.2 apache:latest kimura: 1.0
xmrig: latest sandeep078: latest tntbbo:latest kuben2
OfficialImagee Ubuntuu Cent0S Alp1ne Pythoon
Running containers with elevated privileges, allowing potential attackers to gain control over the
underlying host system. Example: Running a container with root-level access and unrestricted
capabilities.
In the noncompliant code, the container is launched with the –privileged flag, enabling privileged
mode. This grants the container unrestricted access to the host system, potentially compromising
its security boundaries.
The compliant code addresses the vulnerability by running the container without privileged mode.
This restricts the container’s access to system resources and reduces the risk of privilege
escalation and unauthorized access to the host.
Insecurely exposing container APIs without proper authentication or access controls, allowing
attackers to manipulate or extract sensitive information from containers. Example: Exposing
Other Images
Privileged Container:
# Noncompliant: Privileged container
FROM ubuntu
...
# Running container in privileged mode
RUN docker run -it --privileged ubuntu /bin/bash
# Compliant: Non-privileged container
FROM ubuntu
...
# Running container without privileged mode
RUN docker run -it ubuntu /bin/bash
Exposed Container APIs:
Docker API without any authentication or encryption.
In the noncompliant code, the container’s API is exposed on port 8080 without any authentication
or authorization mechanisms in place. This allows unrestricted access to the container API,
making it susceptible to unauthorized access and potential attacks.
The compliant code addresses the vulnerability by exposing the container’s API internally on port
8080 and leveraging a reverse proxy or API gateway for authentication and authorization. The
reverse proxy or API gateway acts as a security layer, handling authentication/authorization
requests before forwarding them to the container API.
To further enhance the security of exposed container APIs, consider the following best practices:
# Noncompliant: Exposed container API without authentication/authorization
FROM nginx
...
# Expose container API on port 8080
EXPOSE 8080
Implement strong authentication and authorization mechanisms: Use industry-standard
authentication protocols (e.g., OAuth, JWT) and enforce access controls based on user roles
and permissions.
1
Employ Transport Layer Security (TLS) encryption: Secure the communication between clients
and the container API using TLS certificates to protect against eavesdropping and tampering.
2
Regularly monitor and log API activity: Implement logging and monitoring mechanisms to
detect and respond to suspicious or malicious activity.
3
Apply rate limiting and throttling: Protect the API from abuse and denial-of-service attacks by
enforcing rate limits and throttling requests.
4
# Compliant: Secured container API with authentication/authorization
FROM nginx
...
# Expose container API on port 8080 (internal)
EXPOSE 8080
Exploiting vulnerabilities in the container runtime or misconfigurations to break out of the
container’s isolation and gain unauthorized access to the host operating system. Example:
Exploiting a vulnerability in the container runtime to access the host system and other containers.
The below code creates and starts a container without any security isolation measures. This
leaves the container susceptible to container escape attacks, where an attacker can exploit
vulnerabilities in the container runtime or misconfigured security settings to gain unauthorized
access to the host system.
we introduce security enhancements to mitigate the risk of container escape. The HostConfig
parameter is used to configure the container’s security settings. Here, we:
Set ‘Privileged’ => false to disable privileged mode, which restricts access to host devices and
capabilities. Use ‘CapDrop’ => [‘ALL’] to drop all capabilities from the container, minimizing the
potential attack surface. Add ‘SecurityOpt’ => [‘no-new-privileges’] to prevent privilege
escalation within the container.
# Use a reverse proxy or API gateway for authentication/authorization
Container Escape:
# Noncompliant: Running a container without proper security isolation
require 'docker'
# Create a container with default settings
container = Docker::Container.create('Image' => 'nginx')
container.start
# Compliant: Running a container with enhanced security isolation
require 'docker'
# Create a container with enhanced security settings
container = Docker::Container.create(
  'Image' => 'nginx',
Modifying or replacing container images with malicious versions that may contain malware,
backdoors, or vulnerable components. Example: Tampering with a container image to inject
malicious code that steals sensitive information.
The below code directly pulls and runs a container image without verifying its integrity. This leaves
the application vulnerable to container image tampering, where an attacker can modify the
container image to include malicious code or compromise the application’s security.
we address this issue by introducing integrity verification. The code calculates the expected
digest of the pulled image using the SHA256 hash algorithm. It then compares this expected
digest with the actual digest of the image obtained from the Docker API. If the digests do not
match, an integrity verification failure is raised, indicating that the image may have been tampered
with.
  'HostConfig' => {
    'Privileged' => false,           # Disable privileged mode
    'CapDrop' => ['ALL'],            # Drop all capabilities
    'SecurityOpt' => ['no-new-privileges']  # Prevent privilege escalation
  }
)
container.start
Container Image Tampering:
#Pulling and running a container image without verifying integrity
require 'docker'
# Pull the container image
image = Docker::Image.create('fromImage' => 'nginx')
# Run the container image
container = Docker::Container.create('Image' => image.id)
container.start
# Compliant: Pulling and running a container image with integrity verification
Misconfigurations in container settings, such as weak access controls or excessive permissions,
allowing attackers to compromise the container or its environment. Example: Running a container
with unnecessary capabilities or insecure mount points.
The noncompliant code creates and starts a container with default settings, which may have
insecure configurations. These misconfigurations can lead to vulnerabilities, such as privilege
escalation, excessive container privileges, or exposure of sensitive resources.
require 'docker'
require 'digest'
# Image name and tag
image_name = 'nginx'
image_tag = 'latest'
# Pull the container image
image = Docker::Image.create('fromImage' => "#{image_name}:#{image_tag}")
# Verify the integrity of the pulled image
expected_digest = Digest::SHA256.hexdigest(image.connection.get("/images/#{image.id}/json").body)
actual_digest = image.info['RepoDigests'].first.split('@').last
if expected_digest != actual_digest
  raise "Integrity verification failed for image: #{image_name}:#{image_tag}"
end
# Run the container image
container = Docker::Container.create('Image' => image.id)
container.start
Insecure Container Configuration:
# Noncompliant: Running a container with insecure configuration
require 'docker'
# Create a container with default settings
In the compliant code, we address these security concerns by applying secure container
configurations. The HostConfig parameter is used to specify the container’s configuration. Here,
we:
Set ‘ReadOnly’ => true to make the container’s filesystem read-only, preventing potential
tampering and unauthorized modifications. Use ‘CapDrop’ => [‘ALL’] to drop all capabilities from
the container, minimizing the attack surface and reducing the potential impact of privilege
escalation. Add ‘SecurityOpt’ => [‘no-new-privileges’] to prevent the container from gaining
additional privileges. Specify ‘NetworkMode’ => ‘bridge’ to isolate the container in a bridge
network, ensuring separation from the host and other containers. Use ‘PortBindings’ to bind the
container’s port to a specific host port (‘80/tcp’ => [{ ‘HostPort’ => ‘8080’ }]). This restricts
network access to the container and avoids exposing unnecessary ports.
container = Docker::Container.create('Image' => 'nginx')
container.start
# Compliant: Running a container with secure configuration
require 'docker'
# Create a container with secure settings
container = Docker::Container.create(
  'Image' => 'nginx',
  'HostConfig' => {
    'ReadOnly' => true,               # Set container as read-only
    'CapDrop' => ['ALL'],             # Drop all capabilities
    'SecurityOpt' => ['no-new-privileges'],  # Prevent privilege escalation
    'NetworkMode' => 'bridge',        # Use a bridge network for isolation
    'PortBindings' => { '80/tcp' => [{ 'HostPort' => '8080' }] }  # Bind container port to a spec
  }
)
container.start
Denial-of-Service (DoS):
Overloading container resources or exploiting vulnerabilities in the container runtime to disrupt
the availability of containerized applications. Example: Launching a DoS attack against a container
by overwhelming it with excessive requests.
The noncompliant code snippet shows a Dockerfile that is vulnerable to resource overloading and
DoS attacks. It does not implement any resource limitations or restrictions, allowing the container
to consume unlimited resources. This can lead to a DoS situation if an attacker overwhelms the
container with excessive requests or exploits vulnerabilities in the container runtime.
The compliant code snippet addresses this vulnerability by not explicitly setting any resource
limitations. However, it is essential to implement resource management and limit container
resources based on your application’s requirements and the resources available in your
environment. This can be achieved by configuring resource limits such as CPU, memory, and
network bandwidth using container orchestration platforms or Docker-compose files.
# Noncompliant: Vulnerable Dockerfile with unlimited resource allocation
FROM nginx:latest
COPY app /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
version: '3'
services:
  nginx:
    image: nginx:latest
    ports:
      - 80:80
    volumes:
      - ./app:/usr/share/nginx/html
    deploy:
      resources:
        limits:
Exploiting vulnerabilities in the kernel or host operating system to gain unauthorized access or
control over containers. Example: Exploiting a kernel vulnerability to escalate privileges and
compromise containers.
To mitigate kernel vulnerabilities, it is important to regularly check for updates and apply security
patches to the host system. Additionally, you can use tools to scan and assess the vulnerability
status of the kernel before creating a Docker container.
Here’s an example of compliant code that incorporates checking for kernel vulnerabilities using
the kubehunter tool before creating the container:
In the compliant code snippet, the kubehunter tool is used to perform a vulnerability assessment,
including checking for kernel vulnerabilities. The output of the tool is examined, and if any
vulnerabilities are found, appropriate steps are taken to address them before creating the Docker
container.
          cpus: '0.5'
          memory: '256M'
Kernel Vulnerabilities:
# Noncompliant: Ignoring kernel vulnerabilities
docker run -d ubuntu:latest /bin/bash
# Compliant: Checking kernel vulnerabilities
# Perform vulnerability assessment using kubehunter
kubehunter scan
# Check the output for kernel vulnerabilities
# If vulnerabilities are found, take necessary steps to address them
# Create the Docker container
docker run -d ubuntu:latest /bin/bash
Shared Kernel Exploitation:
Containers sharing the same kernel can be vulnerable to attacks that exploit kernel vulnerabilities,
allowing attackers to affect multiple containers. Example: Exploiting a kernel vulnerability to gain
unauthorized access to multiple containers on the same host.
In the noncompliant code, the Docker image installs a vulnerable package and runs a vulnerable
application. If an attacker manages to exploit a kernel vulnerability within the container, they could
potentially escape the container and compromise the host or other containers.
The compliant code addresses the vulnerability by ensuring that the container image only
includes necessary and secure packages. It performs regular updates and includes security
patches to mitigate known vulnerabilities. By running a secure application within the container, the
risk of a container breakout is reduced.
To further enhance security, additional measures can be taken such as utilizing container isolation
techniques like running containers with restricted privileges, leveraging security-enhanced
kernels (such as those provided by certain container platforms), and monitoring and logging
container activity to detect potential exploitation attempts.
# Noncompliant: Vulnerable to container breakout
FROM ubuntu:latest
# Install vulnerable package
RUN apt-get update && apt-get install -y vulnerable-package
# Run vulnerable application
CMD ["vulnerable-app"]
# Compliant: Mitigated container breakout vulnerability
FROM ubuntu:latest
# Install security updates and necessary packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y secure-package
# Run secure application
CMD ["secure-app"]
Misconfigurations or vulnerabilities in container orchestration platforms, such as Kubernetes, can
lead to unauthorized access, privilege escalation, or exposure of sensitive information. Example:
Exploiting a misconfigured Kubernetes cluster to gain unauthorized access to sensitive resources.
In the noncompliant code, the Pod definition enables privileged mode for the container, granting it
elevated privileges within the container orchestration environment. If an attacker gains access to
this container, they could exploit the elevated privileges to perform malicious actions on the host
or compromise other containers.
The compliant code addresses the vulnerability by explicitly disabling privileged mode for the
container. By running containers with reduced privileges, the impact of a potential compromise is
limited, and the attack surface is minimized.
In addition to disabling privileged mode, other security measures should be implemented to
enhance the security of container orchestration. This includes configuring appropriate RBAC
(Role-Based Access Control) policies, enabling network segmentation and isolation, regularly
applying security patches to the orchestration system, and monitoring the environment for
suspicious activities.
Insecure Container Orchestration:
# Noncompliant: Vulnerable to privilege escalation
apiVersion: v1
kind: Pod
metadata:
  name: vulnerable-pod
spec:
  containers:
    - name: vulnerable-container
      image: vulnerable-image
      securityContext:
        privileged: true  # Privileged mode enabled
# Compliant: Mitigated privilege escalation
apiVersion: v1
kind: Pod
metadata:
Copyright © 2019-2023 HADESS.
  name: secure-pod
spec:
  containers:
    - name: secure-container
      image: secure-image
      securityContext:
        privileged: false  # Privileged mode disabled
DevSecOps Guides
Attacks / Pipeline Attacks
Misconfiguration of configuration files, secrets, or environment variables in the pipeline, leading to
unauthorized access or exposure of sensitive information.
In the noncompliant code, there is a lack of encryption in the pipeline. This means that sensitive
data transmitted within the pipeline, such as configuration files, credentials, or deployment
artifacts, are not adequately protected, increasing the risk of unauthorized access or data
leakage.
Pipeline Attacks
TABLE OF CONTENTS
Insecure Configuration Management:
1
Weak Authentication and Authorization:
2
Insecure CI/CD Tools:
3
Lack of Secure Coding Practices:
4
Insecure Third-Party Dependencies:
5
Insufficient Testing:
6
Insecure Build and Deployment Processes:
7
Exposed Credentials:
8
Insufficient Monitoring and Logging:
9
Misconfigured Access Controls:
10
Insecure Configuration Management:
# Noncompliant: Lack of Encryption in pipeline
stages:
  - name: Build and Deploy
    steps:
To address the lack of encryption in the pipeline, it is essential to implement encryption
mechanisms to protect sensitive data.
      - name: Build Application
        command: |
          echo "Building application..."
          build-tool
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          deploy-tool
      - name: Upload Artifacts
        command: |
          echo "Uploading artifacts..."
          upload-tool
# Compliant: Enhanced Encryption in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          build-tool
        security:
          - encryption: true
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          deploy-tool
        security:
          - encryption: true
      - name: Upload Artifacts
        command: |
          echo "Uploading artifacts..."
In the compliant code, each step in the pipeline has an associated security configuration that
enables encryption. This ensures that sensitive data is encrypted during transmission within the
pipeline, providing an additional layer of protection against unauthorized access or data exposure.
Inadequate authentication mechanisms and weak authorization controls in the pipeline, allowing
unauthorized access to critical resources or actions.
In the noncompliant code, weak or inadequate authentication and authorization mechanisms are
used in the pipeline. This can lead to unauthorized access, privilege escalation, or other security
issues.
In the compliant code snippet, strong authentication mechanisms such as service accounts or
OAuth tokens are used to authenticate with the production environment. These mechanisms
provide stronger security controls and help prevent unauthorized access to sensitive resources.
          upload-tool
        security:
          - encryption: true
Weak Authentication and Authorization:
# Noncompliant: Weak authentication and authorization in pipeline
stages:
  - name: Deploy to Production
    steps:
      - name: Authenticate with Production Environment
        command: |
          echo "Authenticating with production environment..."
          # Weak authentication mechanism
          kubectl config set-credentials admin --username=admin --password=weakpassword
          kubectl config use-context production
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          kubectl apply -f deployment.yaml
Vulnerabilities in the Continuous Integration/Continuous Deployment (CI/CD) tools used in the
pipeline, such as outdated software versions or insecure configurations, leading to potential
exploits or unauthorized access.
In the noncompliant code, insecure CI/CD tools are used in the pipeline, which can pose security
risks. This may include using outdated or vulnerable versions of CI/CD tools, relying on insecure
configurations, or using tools with known security vulnerabilities.
# Compliant: Strong authentication and authorization in pipeline
stages:
  - name: Deploy to Production
    steps:
      - name: Authenticate with Production Environment
        command: |
          echo "Authenticating with production environment..."
          # Strong authentication mechanism (e.g., using a service account or OAuth tokens)
          kubectl config set-credentials prod-service-account --token=strongtoken
          kubectl config use-context production
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          kubectl apply -f deployment.yaml
Insecure CI/CD Tools:
# Compliant: Secure CI/CD Tools in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Scan for Vulnerabilities
        command: |
          echo "Scanning for vulnerabilities..."
          # Using a secure and up-to-date version of the CI/CD tool
          secure-cicd-tool scan --version 2.0.0
      - name: Deploy Application
        command: |
In the compliant code snippet, secure and up-to-date versions of the CI/CD tools are used, which
have been reviewed for security vulnerabilities. Additionally, it is important to ensure that the
configurations of these tools are properly secured and follow security best practices.
Development teams not following secure coding practices, leading to the introduction of
vulnerabilities, such as code injection, cross-site scripting (XSS), or SQL injection, into the
pipeline.
In the noncompliant code, there is a lack of secure coding practices in the pipeline. This can
include the absence of code review, the use of insecure libraries or frameworks, and the lack of
security testing and validation during the development and deployment process.
          echo "Deploying application..."
          secure-cicd-tool deploy -f deployment.yaml
# Compliant: Secure CI/CD Tools in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Scan for Vulnerabilities
        command: |
          echo "Scanning for vulnerabilities..."
          # Using a secure and up-to-date version of the CI/CD tool
          secure-cicd-tool scan --version 2.0.0
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          secure-cicd-tool deploy -f deployment.yaml
Lack of Secure Coding Practices:
# Noncompliant: Lack of Secure Coding Practices in pipeline
stages:
  - name: Build and Deploy
To address the lack of secure coding practices in the pipeline, it is important to adopt and
implement secure coding practices throughout the development and deployment process. This
includes incorporating code reviews, using secure coding guidelines, and performing security
testing and validation.
In the compliant code snippet, secure coding practices are implemented by incorporating code
review and security testing during the build process. This ensures that potential security
vulnerabilities are identified and addressed early in the development cycle. Additionally, the
deployment process includes the use of secure deployment tools that prioritize secure coding
practices.
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          # Building the application without any code review or security testing
          insecure-build-tool build
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          # Deploying the application without ensuring secure coding practices
          insecure-deploy-tool deploy -f deployment.yaml
# Compliant: Implementation of Secure Coding Practices in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          # Incorporating code review and security testing during the build process
          secure-build-tool build --code-review --security-testing
      - name: Deploy Application
        command: |
          echo "Deploying application..."
Integration of insecure or outdated third-party libraries or components into the pipeline, exposing
the pipeline to known vulnerabilities or exploits.
In the noncompliant code, there is a lack of consideration for insecure third-party dependencies in
the pipeline. This can include the use of outdated or vulnerable libraries, frameworks, or plugins
without proper validation or risk assessment.
To address the lack of consideration for insecure third-party dependencies in the pipeline, it is
crucial to implement proper validation and management practices. This includes conducting
regular vulnerability assessments, using dependency management tools, and maintaining an
updated inventory of dependencies.
          # Deploying the application with secure coding practices
          secure-deploy-tool deploy -f deployment.yaml
Insecure Third-Party Dependencies:
# Noncompliant: Lack of Insecure Third-Party Dependencies in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          # Building the application without considering insecure third-party dependencies
          insecure-build-tool build
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          # Deploying the application without validating the security of third-party dependencies
          insecure-deploy-tool deploy -f deployment.yaml
# Compliant: Validation and Management of Third-Party Dependencies in pipeline
stages:
In the compliant code snippet, validation and management practices for third-party dependencies
are implemented in the pipeline. This includes conducting vulnerability scans and utilizing
dependency management tools to ensure that only secure and up-to-date dependencies are used
in the application. By addressing insecure third-party dependencies, the pipeline can significantly
reduce the risk of introducing vulnerabilities and improve the overall security of the deployed
application.
Inadequate testing processes, including lack of security testing, vulnerability scanning, or
penetration testing, allowing potential vulnerabilities to go undetected in the pipeline.
In the noncompliant code, there is a lack of sufficient testing in the pipeline. This means that the
pipeline does not include appropriate testing stages, such as unit tests, integration tests, or
security tests, to ensure the quality and security of the deployed application.
  - name: Build and Deploy
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          # Building the application with vulnerability assessment and secure dependency manageme
          secure-build-tool build --vulnerability-scan --dependency-management
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          # Deploying the application after validating the security of third-party dependencies
          secure-deploy-tool deploy -f deployment.yaml
Insufficient Testing:
# Noncompliant: Insufficient Testing in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
To address the lack of sufficient testing in the pipeline, it is crucial to incorporate comprehensive
testing stages to validate the functionality, quality, and security of the application.
          # Building the application without running tests
          insecure-build-tool build
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          # Deploying the application without running tests
          insecure-deploy-tool deploy -f deployment.yaml
# Compliant: Comprehensive Testing in pipeline
stages:
  - name: Build and Test
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          # Building the application with unit tests
          secure-build-tool build --unit-tests
      - name: Run Integration Tests
        command: |
          echo "Running integration tests..."
          # Running integration tests to validate the application's behavior and interactions
          secure-test-tool run --integration-tests
  - name: Deploy
    steps:
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          # Deploying the application after successful build and tests
          secure-deploy-tool deploy -f deployment.yaml
In the compliant code snippet, a separate testing stage is added before the deployment stage.
This testing stage includes unit tests and integration tests to validate the application’s
functionality and behavior. By running comprehensive tests, potential issues and vulnerabilities
can be identified early in the pipeline, ensuring a higher level of quality and security for the
deployed application.
Weak controls and improper validation during the build and deployment processes, enabling the
inclusion of malicious code or unauthorized changes into the pipeline.
In the noncompliant code, the build and deployment processes lack proper controls and
validation, making them vulnerable to the inclusion of malicious code or unauthorized changes.
This can lead to the deployment of compromised or insecure applications.
To address the security vulnerabilities in the build and deployment processes, it is essential to
implement secure controls and validation measures.
Insecure Build and Deployment Processes:
# Noncompliant: Insecure Build and Deployment Processes in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          # Building the application without proper validation
          insecure-build-tool build
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          # Deploying the application without proper controls
          insecure-deploy-tool deploy -f deployment.yaml
# Compliant: Secure Build and Deployment Processes in pipeline
stages:
  - name: Build and Deploy
    steps:
In the compliant code snippet, the build and deployment processes have been enhanced with
secure controls and validation. The build process includes proper validation steps to ensure that
only valid and authorized code is included in the deployment package. Similarly, the deployment
process incorporates controls to verify the integrity and authenticity of the deployed application,
preventing unauthorized changes or inclusion of malicious code.
Storage or transmission of sensitive credentials, such as API keys or access tokens, in an insecure
manner within the pipeline, making them susceptible to unauthorized access or misuse.
In the noncompliant code, credentials are hardcoded or exposed in plain text within the pipeline
configuration or scripts. This makes them vulnerable to unauthorized access or disclosure, putting
the sensitive information at risk.
      - name: Build Application
        command: |
          echo "Building application..."
          # Building the application with proper validation
          secure-build-tool build --validate
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          # Deploying the application with proper controls
          secure-deploy-tool deploy -f deployment.yaml --verify
Exposed Credentials:
# Noncompliant: Exposed Credentials in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Set Environment Variables
        command: |
          export DATABASE_USERNAME=admin
          export DATABASE_PASSWORD=secretpassword
      - name: Build Application
        command: |
          echo "Building application..."
To address the security concern of exposed credentials in the pipeline, it is crucial to adopt
secure practices for handling sensitive information.
In the compliant code snippet, the sensitive credentials are retrieved securely from a secure vault
or secret management system. This ensures that the credentials are not exposed directly in the
pipeline configuration or scripts. By using a secure vault, the credentials remain encrypted and
are accessed only when needed during the pipeline execution.
Lack of robust monitoring and logging mechanisms in the pipeline, hindering the detection and
response to security incidents or unusual activities.
          build-tool --username=$DATABASE_USERNAME --password=$DATABASE_PASSWORD
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          deploy-tool --username=$DATABASE_USERNAME --password=$DATABASE_PASSWORD
# Compliant: Secure Handling of Credentials in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Retrieve Credentials from Secure Vault
        command: |
          export DATABASE_USERNAME=$(secure-vault read DATABASE_USERNAME)
          export DATABASE_PASSWORD=$(secure-vault read DATABASE_PASSWORD)
      - name: Build Application
        command: |
          echo "Building application..."
          build-tool --username=$DATABASE_USERNAME --password=$DATABASE_PASSWORD
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          deploy-tool --username=$DATABASE_USERNAME --password=$DATABASE_PASSWORD
Insufficient Monitoring and Logging:
In the noncompliant code, there is a lack of proper monitoring and logging practices in the
pipeline. This means that important events, errors, or security-related activities are not
adequately captured or logged, making it challenging to detect and respond to potential issues or
security incidents.
To address the insufficient monitoring and logging in the pipeline, it is essential to implement
proper logging and monitoring practices.
# Noncompliant: Insufficient Monitoring and Logging in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          build-tool
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          deploy-tool
# Compliant: Implementing Monitoring and Logging in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          build-tool
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          deploy-tool
  - name: Monitor and Log
    steps:
In the compliant code snippet, an additional stage called “Monitor and Log” is introduced to
handle monitoring and logging activities. This stage includes steps to send pipeline logs to a
centralized logging system and monitor the performance and health of the pipeline.
By sending the pipeline logs to a centralized logging system, you can gather and analyze log data
from multiple pipeline runs, enabling better visibility into pipeline activities and potential issues.
Monitoring the pipeline’s performance and health helps identify any abnormalities or bottlenecks,
allowing for proactive remediation.
Improperly configured access controls, permissions, or roles within the pipeline, allowing
unauthorized users or malicious actors to gain elevated privileges or access to critical resources.
In the noncompliant code, there is a lack of proper access controls in the pipeline. This means
that unauthorized individuals may have access to sensitive information or critical pipeline
components, leading to potential security breaches or unauthorized actions.
      - name: Send Pipeline Logs to Centralized Logging System
        command: |
          echo "Sending pipeline logs to centralized logging system..."
          send-logs --log-file=pipeline.log
      - name: Monitor Pipeline Performance and Health
        command: |
          echo "Monitoring pipeline performance and health..."
          monitor-pipeline
Misconfigured Access Controls:
# Noncompliant: Misconfigured Access Controls in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          build-tool
      - name: Deploy Application
To mitigate the risk of misconfigured access controls in the pipeline, it is crucial to implement
proper access controls and authentication mechanisms.
In the compliant code, each step in the pipeline has an associated security configuration that
specifies the necessary roles or permissions required to execute that step. This ensures that only
authorized individuals or entities can perform specific actions in the pipeline.
Copyright © 2019-2023 HADESS.
        command: |
          echo "Deploying application..."
          deploy-tool
# Compliant: Enhanced Access Controls in pipeline
stages:
  - name: Build and Deploy
    steps:
      - name: Build Application
        command: |
          echo "Building application..."
          build-tool
        security:
          - role: build-deploy
      - name: Deploy Application
        command: |
          echo "Deploying application..."
          deploy-tool
        security:
          - role: build-deploy
DevSecOps Guides
Rules / Android
Noncompliant code:
Android
TABLE OF CONTENTS
Java
1
Improper Platform Usage
a
Insecure Data Storage
b
Insecure Communication
c
Insecure Authentication
d
Insufficient Cryptography
e
Insecure Authorization
f
Client Code Quality
g
Code Tampering
h
Reverse Engineering
i
Extraneous Functionality
j
Java
Improper Platform Usage
// Noncompliant code
public class InsecureStorageActivity extends AppCompatActivity {
    private SharedPreferences preferences;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
In this noncompliant code, the SharedPreferences object is created with the mode
MODE_WORLD_READABLE, which allows any other application to read the stored preferences.
This violates the principle of proper platform usage, as sensitive data should not be stored in a
way that allows unauthorized access.
Compliant code:
In the compliant code, the SharedPreferences object is created with the mode MODE_PRIVATE,
which ensures that the preferences are only accessible by the application itself. This follows the
principle of proper platform usage by securely storing sensitive data without allowing
unauthorized access.
By using MODE_PRIVATE instead of MODE_WORLD_READABLE, the compliant code ensures that
the stored preferences are only accessible within the application, mitigating the risk of exposing
        setContentView(R.layout.activity_insecure_storage);

        preferences = getSharedPreferences("my_prefs", MODE_WORLD_READABLE);
    }
    // Rest of the code...
}
// Compliant code
public class SecureStorageActivity extends AppCompatActivity {
    private SharedPreferences preferences;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_secure_storage);

        preferences = getSharedPreferences("my_prefs", MODE_PRIVATE);
    }
    // Rest of the code...
}
sensitive information to other applications on the device.
Semgrep:
For Semgrep, you can use the following rule to detect the insecure use of
MODE_WORLD_READABLE in SharedPreferences:
CodeQL:
For CodeQL, you can use the following query to detect the insecure use of
MODE_WORLD_READABLE in SharedPreferences:
Noncompliant code:
rules:
  - id: insecure-sharedpreferences
    patterns:
      - pattern: "getSharedPreferences\\(\"\\w+\",\\s*MODE_WORLD_READABLE\\)"
    message: "Insecure use of MODE_WORLD_READABLE in SharedPreferences"
import java
import android
from MethodInvocation m
where m.getMethod().getQualifiedName() = "android.content.Context.getSharedPreferences"
  and m.getArgument(1).toString() = "MODE_WORLD_READABLE"
select m
Insecure Data Storage
// Noncompliant code
public class InsecureStorageActivity extends AppCompatActivity {
    private static final String FILENAME = "my_sensitive_data.txt";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_insecure_storage);

In this noncompliant code, sensitive data is written to a file using the FileWriter without
considering secure storage options. The data is stored in the application’s private file directory,
but it lacks proper encryption or additional security measures, making it vulnerable to
unauthorized access.
Compliant code:
        String sensitiveData = "This is my sensitive data";
        writeToFile(sensitiveData);
    }
    private void writeToFile(String data) {
        try {
            File file = new File(getFilesDir(), FILENAME);
            FileWriter writer = new FileWriter(file);
            writer.write(data);
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    // Rest of the code...
}
// Compliant code
public class SecureStorageActivity extends AppCompatActivity {
    private static final String FILENAME = "my_sensitive_data.txt";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_secure_storage);

        String sensitiveData = "This is my sensitive data";
        writeToFile(sensitiveData);
    }
In the compliant code, the FileOutputStream and OutputStreamWriter are used along with the
openFileOutput method to securely write the sensitive data to a file in the application’s private
storage directory. The MODE_PRIVATE flag ensures that the file is only accessible by the
application itself. This follows secure storage practices and helps protect the sensitive data from
unauthorized access.
By using openFileOutput with MODE_PRIVATE instead of FileWriter, the compliant code ensures
secure storage of sensitive data, mitigating the risk of unauthorized access or exposure.
Semgrep:
CodeQL:
    private void writeToFile(String data) {
        try {
            FileOutputStream fos = openFileOutput(FILENAME, Context.MODE_PRIVATE);
            OutputStreamWriter writer = new OutputStreamWriter(fos);
            writer.write(data);
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    // Rest of the code...
}
rules:
  - id: insecure-file-write
    patterns:
      - pattern: "FileWriter\\.write\\(\\w+\\)"
    message: "Insecure file write operation"
import java
import android
Noncompliant code:
from MethodInvocation m
where m.getMethod().getQualifiedName() = "java.io.FileWriter.write"
select m
Insecure Communication
// Noncompliant code
public class InsecureCommunicationActivity extends AppCompatActivity {
    private static final String API_URL = "http://example.com/api/";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_insecure_communication);

        String requestData = "Some sensitive data";
        String response = sendRequest(requestData);
        // Process the response...
    }
    private String sendRequest(String data) {
        try {
            URL url = new URL(API_URL);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);

            OutputStreamWriter writer = new OutputStreamWriter(conn.getOutputStream());
            writer.write(data);
            writer.flush();

            int responseCode = conn.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStr
                StringBuilder response = new StringBuilder();
In this noncompliant code, the app sends sensitive data over an insecure HTTP connection
(http://example.com/api/) using HttpURLConnection. This puts the data at risk of interception,
tampering, and unauthorized access.
Compliant code:
                String line;
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                reader.close();
                return response.toString();
            } else {
                // Handle error response...
            }

            conn.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }
    // Rest of the code...
}
// Compliant code
// Compliant code
public class SecureCommunicationActivity extends AppCompatActivity {
    private static final String API_URL = "https://example.com/api/";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_secure_communication);

        String requestData = "Some sensitive data";
        String response = sendRequest(requestData);
        // Process the response...
    }
    private String sendRequest(String data) {
        try {
            URL url = new URL(API_URL);
            HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);

            OutputStreamWriter writer = new OutputStreamWriter(conn.getOutputStream());
            writer.write(data);
            writer.flush();

            int responseCode = conn.getResponseCode();
            if (responseCode == HttpsURLConnection.HTTP_OK) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStr
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                reader.close();
                return response.toString();
            } else {
                // Handle error response...
            }

            conn.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }
In the compliant code, the app uses HttpsURLConnection to establish a secure HTTPS connection
(https://example.com/api/) for transmitting sensitive data. HTTPS ensures that the communication
is encrypted, providing confidentiality and integrity of the data. By using HTTPS instead of HTTP,
the compliant code addresses the vulnerability of insecure communication and reduces the risk of
interception or unauthorized access to sensitive data.
Semgrep:
CodeQL:
Noncompliant code:
    // Rest of the code...
}
rules:
  - id: insecure-file-write
    patterns:
      - pattern: "FileWriter\\.write\\(\\w+\\)"
    message: "Insecure file write operation"
import java
import android
from MethodInvocation m
where m.getMethod().getQualifiedName() = "java.io.FileWriter.write"
select m
Insecure Authentication
// Noncompliant code
public class LoginActivity extends AppCompatActivity {
    private EditText usernameEditText;
    private EditText passwordEditText;
    private Button loginButton;
    @Override
In this noncompliant code, the app performs authentication by comparing the username and
password entered by the user (admin and admin123) with hard-coded values. This approach is
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        usernameEditText = findViewById(R.id.usernameEditText);
        passwordEditText = findViewById(R.id.passwordEditText);
        loginButton = findViewById(R.id.loginButton);
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String username = usernameEditText.getText().toString();
                String password = passwordEditText.getText().toString();
                if (username.equals("admin") && password.equals("admin123")) {
                    // Login successful
                    openMainActivity();
                } else {
                    // Login failed
                    Toast.makeText(LoginActivity.this, "Invalid username or password", Toast.LENG
                }
            }
        });
    }
    private void openMainActivity() {
        // Start the main activity
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        finish();
    }

    // Rest of the code...
}
insecure because the credentials are easily discoverable and can be exploited by attackers.
Compliant code:
// Compliant code
public class LoginActivity extends AppCompatActivity {
    private EditText usernameEditText;
    private EditText passwordEditText;
    private Button loginButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        usernameEditText = findViewById(R.id.usernameEditText);
        passwordEditText = findViewById(R.id.passwordEditText);
        loginButton = findViewById(R.id.loginButton);
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String username = usernameEditText.getText().toString();
                String password = passwordEditText.getText().toString();
                // Perform secure authentication
                if (authenticateUser(username, password)) {
                    // Login successful
                    openMainActivity();
                } else {
                    // Login failed
                    Toast.makeText(LoginActivity.this, "Invalid username or password", Toast.LENG
                }
            }
        });
    }
    private boolean authenticateUser(String username, String password) {
In the compliant code, the app separates the authentication logic into a dedicated method
authenticateUser(), which can be implemented securely. This method can utilize secure
authentication mechanisms such as hashing, salting, and server-side validation. By implementing
a secure authentication process instead of relying on hard-coded credentials, the compliant code
addresses the vulnerability of insecure authentication and reduces the risk of unauthorized
access to user accounts.
Semgrep:
CodeQL:
        // Implement secure authentication logic here
        // Example: Make a secure API call to validate the user credentials
        // Return true if the authentication is successful, false otherwise
        return false;
    }
    private void openMainActivity() {
        // Start the main activity
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        finish();
    }

    // Rest of the code...
}
rules:
  - id: insecure-login-credentials
    patterns:
      - pattern: '(username.equals\\("admin"\\) && password.equals\\("admin123"\\))'
    message: "Insecure use of hardcoded login credentials"
import java
import android
Noncompliant code:
from BinaryExpression b
where b.getLeftOperand().toString() = "username.equals(\"admin\")"
  and b.getRightOperand().toString() = "password.equals(\"admin123\")"
select b
Insufficient Cryptography
// Noncompliant code
public class EncryptionUtils {
    private static final String KEY = "mySecretKey";

    public static String encrypt(String data) {
        try {
            Key key = generateKey();
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.ENCRYPT_MODE, key);
            byte[] encryptedData = cipher.doFinal(data.getBytes());
            return Base64.encodeToString(encryptedData, Base64.DEFAULT);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static String decrypt(String encryptedData) {
        try {
            Key key = generateKey();
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.DECRYPT_MODE, key);
            byte[] decodedData = Base64.decode(encryptedData, Base64.DEFAULT);
            byte[] decryptedData = cipher.doFinal(decodedData);
            return new String(decryptedData);
        } catch (Exception e) {
            e.printStackTrace();
        }
In this noncompliant code, a custom EncryptionUtils class is implemented to encrypt and decrypt
data using the AES algorithm. However, the code uses a hard-coded key (mySecretKey) and does
not incorporate other essential security measures like salting, key strengthening, or secure key
storage. This approach is insufficient and can be vulnerable to various cryptographic attacks.
Compliant code:
        return null;
    }

    private static Key generateKey() throws Exception {
        return new SecretKeySpec(KEY.getBytes(), "AES");
    }

    // Rest of the code...
}
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import android.util.Base64;
public class EncryptionUtils {
    private static final String KEY_ALGORITHM = "AES";
    private static final String CIPHER_TRANSFORMATION = "AES/CBC/PKCS7Padding";
    private SecretKeySpec secretKeySpec;
    private IvParameterSpec ivParameterSpec;
    public EncryptionUtils(String secretKey) {
        try {
            byte[] keyBytes = generateKeyBytes(secretKey);
            secretKeySpec = new SecretKeySpec(keyBytes, KEY_ALGORITHM);
            ivParameterSpec = new IvParameterSpec(keyBytes);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public String encrypt(String data) {
        try {
            Cipher cipher = Cipher.getInstance(CIPHER_TRANSFORMATION);
            cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec, ivParameterSpec);
            byte[] encryptedData = cipher.doFinal(data.getBytes());
            return Base64.encodeToString(encryptedData, Base64.DEFAULT);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
    public String decrypt(String encryptedData) {
        try {
            Cipher cipher = Cipher.getInstance(CIPHER_TRANSFORMATION);
            cipher.init(Cipher.DECRYPT_MODE, secretKeySpec, ivParameterSpec);
            byte[] decodedData = Base64.decode(encryptedData, Base64.DEFAULT);
            byte[] decryptedData = cipher.doFinal(decodedData);
            return new String(decryptedData);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
    private byte[] generateKeyBytes(String secretKey) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        md.update(secretKey.getBytes());
        return md.digest();
    }
}
In the compliant code, the key generation has been improved by using a more secure approach.
Instead of a simple byte conversion of the secretKey, a hashing algorithm (SHA-256) is used to
derive a stronger key from the secretKey. This enhances the security of the encryption process by
introducing a more robust key derivation function.
Semgrep:
CodeQL:
Noncompliant code:
rules:
  - id: insecure-encryption-key
    patterns:
      - pattern: "return new SecretKeySpec\\(KEY.getBytes\\(\\), \"AES\"\\)"
    message: "Insecure use of hard-coded encryption key"
import java
import javax.crypto
from MethodInvocation m
where m.getMethod().getQualifiedName() = "javax.crypto.spec.SecretKeySpec.<init>"
  and m.getArgument(0).toString() = "KEY.getBytes()"
  and m.getArgument(1).toString() = "\"AES\""
select m
Insecure Authorization
public class AuthorizationUtils {
    public boolean checkAdminAccess(String username, String password) {
        if (username.equals("admin") && password.equals("password")) {
            return true;
        } else {
            return false;
        }
    }
}
In this noncompliant code, the checkAdminAccess method performs an insecure authorization
check by comparing the username and password directly with hardcoded values. This approach is
vulnerable to attacks such as password guessing and brute-force attacks, as well as unauthorized
access if the credentials are compromised.
To address this issue, here’s an example of compliant code for secure authorization in Android
Java:
Compliant code:
In the compliant code, the username and password comparison is still present, but the actual
credentials are stored securely, such as in a secure database or a hashed and salted format.
Additionally, this code provides an example where the hardcoded values are defined as constants,
making it easier to manage and update the credentials if needed. It is important to implement
proper authentication mechanisms, such as using secure password storage and strong
authentication protocols, to ensure secure authorization in real-world scenarios.
Semgrep:
public class AuthorizationUtils {
    private static final String ADMIN_USERNAME = "admin";
    private static final String ADMIN_PASSWORD = "password";
    public boolean checkAdminAccess(String username, String password) {
        // Perform secure authentication logic
        // This could involve retrieving user credentials from a secure source,
        // such as a database, and comparing them using a secure hashing algorithm.
        // For demonstration purposes, we'll use a simple comparison with hardcoded values.
        if (username.equals(ADMIN_USERNAME) && password.equals(ADMIN_PASSWORD)) {
            return true;
        } else {
            return false;
        }
    }
}
rules:
  - id: insecure-admin-access
CodeQL:
Noncompliant code:
    patterns:
      - pattern: 'username.equals\\("admin"\\) && password.equals\\("password"\\)'
    message: "Insecure use of hardcoded admin credentials"
import java
class AuthorizationUtils extends AnyFile
{
  AuthorizationUtils() {
    exists(
      MethodDeclaration m |
      m.getEnclosingType().toString() = "AuthorizationUtils" and
      m.getParameters().toString() = "[String username, String password]" and
      m.getReturnType().toString() = "boolean" and
      m.getBody().toString() = "if (username.equals(\"admin\") && password.equals(\"password\"))
    )
  }
}
Client Code Quality
public class MainActivity extends AppCompatActivity {
    private TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = findViewById(R.id.textView);
        // Perform a long and complex operation on the main UI thread
In this noncompliant code, a long and complex operation is performed directly on the main UI
thread within the onCreate method of the MainActivity class. Performing such heavy
computations on the main UI thread can cause the app to become unresponsive and negatively
impact the user experience. It is essential to offload time-consuming operations to background
threads to keep the UI responsive.
To address this issue, here’s an example of compliant code that improves client code quality in
Android Java:
Compliant code:
        for (int i = 0; i < 1000000; i++) {
            // Perform some heavy computations
        }
        // Update the UI
        textView.setText("Operation completed");
    }
}
public class MainActivity extends AppCompatActivity {
    private TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = findViewById(R.id.textView);
        // Perform the long and complex operation on a background thread
        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 1000000; i++) {
                    // Perform some heavy computations
                }
In the compliant code, the heavy computations are performed on a background thread using
Thread or other concurrency mechanisms. Once the computations are completed, the UI update
is performed on the main UI thread using runOnUiThread to ensure proper synchronization with
the UI. By offloading the heavy computations to a background thread, the UI remains responsive,
providing a better user experience.
Semgrep:
CodeQL:
                // Update the UI on the main thread
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // Update the UI
                        textView.setText("Operation completed");
                    }
                });
            }
        }).start();
    }
}
rules:
  - id: long-operation-on-ui-thread
    patterns:
      - pattern: 'for \(int i = 0; i < \d+; i\+\+\)'
    message: "Long-running operation on the main UI thread"
import android
class MainActivity extends AnyFile
{
  MainActivity() {
    exists(
      MethodDeclaration m |
Noncompliant code:
      m.getEnclosingType().toString() = "MainActivity" and
      m.getQualifiedName() = "android.app.Activity.onCreate(Bundle)" and
      m.getBody().toString().indexOf("for (int i = 0; i < 1000000; i++)") >= 0
    )
  }
}
Code Tampering
public class MainActivity extends AppCompatActivity {
    private TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = findViewById(R.id.textView);
        // Check if the app is installed from an unauthorized source
        boolean isAuthorizedSource = checkInstallationSource();
        if (!isAuthorizedSource) {
            // Show an error message and exit the app
            textView.setText("Unauthorized app installation");
            finish();
        }
        // Rest of the code...
    }
    private boolean checkInstallationSource() {
        // Perform checks to determine the app installation source
        // For simplicity, assume the check always returns false in this example
        return false;
In this noncompliant code, there is a check performed in the onCreate method to verify if the app
is installed from an unauthorized source. If the check fails (returns false), an error message is
displayed, but the app continues its execution.
To address this issue, here’s an example of compliant code that mitigates code tampering in
Android Java:
Compliant code:
    }
}
public class MainActivity extends AppCompatActivity {
    private TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = findViewById(R.id.textView);
        // Check if the app is installed from an unauthorized source
        boolean isAuthorizedSource = checkInstallationSource();
        if (!isAuthorizedSource) {
            // Show an error message and exit the app
            textView.setText("Unauthorized app installation");
            finishAffinity(); // Close all activities and exit the app
            return; // Prevent further execution of code
        }
        // Rest of the code...
    }
    private boolean checkInstallationSource() {
        // Perform checks to determine the app installation source
In the compliant code, when the check for an unauthorized app installation fails, the finishAffinity()
method is called to close all activities and exit the app. Additionally, the return statement is used
to prevent further execution of code in the onCreate method. By terminating the app’s execution
upon detection of an unauthorized installation source, the potential for code tampering is
mitigated.
Semgrep:
CodeQL:
        // For simplicity, assume the check always returns false in this example
        return false;
    }
}
rules:
  - id: unauthorized-app-installation-check
    patterns:
      - pattern: 'checkInstallationSource\(\)'
    message: "Unauthorized app installation check"
import android
class MainActivity extends AnyFile
{
  MainActivity() {
    exists(
      MethodDeclaration m |
      m.getEnclosingType().toString() = "MainActivity" and
      m.getQualifiedName() = "android.app.Activity.onCreate(Bundle)" and
      m.getBody().toString().indexOf("checkInstallationSource()") >= 0
    )
  }
}
Reverse Engineering
Noncompliant code:
In this noncompliant code, sensitive data is processed in the performSensitiveOperation method.
The resulting sensitive data is then directly displayed on the screen in the onCreate method,
making it easier for an attacker to reverse engineer and extract the sensitive information from the
APK.
To address this issue, here’s an example of compliant code that mitigates reverse engineering in
Android Java:
Compliant code:
public class MainActivity extends AppCompatActivity {
    private TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = findViewById(R.id.textView);
        // Perform sensitive operation
        String sensitiveData = performSensitiveOperation();
        // Display sensitive data on the screen
        textView.setText(sensitiveData);
        // Rest of the code...
    }
    private String performSensitiveOperation() {
        // Perform sensitive operation
        // For simplicity, assume it involves sensitive data processing
        return "Sensitive Data";
    }
}
In the compliant code, instead of directly displaying the sensitive data on the screen, a generic
message is shown to avoid exposing sensitive information. By obfuscating the sensitive data and
displaying a generic message, the reverse engineering efforts are made more challenging, making
it harder for an attacker to extract sensitive information from the APK.
Semgrep:
public class MainActivity extends AppCompatActivity {
    private TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = findViewById(R.id.textView);
        // Perform sensitive operation
        String sensitiveData = performSensitiveOperation();
        // Display a generic message on the screen
        textView.setText("Sensitive data is protected");
        // Rest of the code...
    }
    private String performSensitiveOperation() {
        // Perform sensitive operation
        // For simplicity, assume it involves sensitive data processing
        return "Sensitive Data";
    }
}
rules:
  - id: sensitive-data-display
    patterns:
CodeQL:
Noncompliant code:
      - pattern: 'textView.setText\(performSensitiveOperation\(\)\)'
    message: "Sensitive data display"
import android
class MainActivity extends AnyFile
{
  MainActivity() {
    exists(
      MethodDeclaration m |
      m.getEnclosingType().toString() = "MainActivity" and
      m.getQualifiedName() = "android.app.Activity.onCreate(Bundle)" and
      m.getBody().toString().indexOf("textView.setText(performSensitiveOperation())") >= 0
    )
  }
}
Extraneous Functionality
public class MainActivity extends AppCompatActivity {
    private Button loginButton;
    private Button adminButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        loginButton = findViewById(R.id.loginButton);
        adminButton = findViewById(R.id.adminButton);
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
In this noncompliant code, there is an adminButton along with its associated functionality for
performing administrative actions. However, if the app does not require or intend to provide
administrative functionality to regular users, this can introduce unnecessary risk. It increases the
attack surface and potential for unauthorized access if an attacker gains control of the app.
To address this issue, here’s an example of compliant code that removes the extraneous
functionality:
Compliant code:
            public void onClick(View v) {
                // Perform login functionality
                performLogin();
            }
        });
        adminButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Perform admin functionality
                performAdminAction();
            }
        });
        // Rest of the code...
    }
    private void performLogin() {
        // Login functionality
    }
    private void performAdminAction() {
        // Admin functionality
    }
}
In the compliant code, the adminButton and its associated administrative functionality have been
removed. The app now focuses solely on the required login functionality for regular users,
reducing the attack surface and eliminating unnecessary functionality that could introduce
potential security risks.
Semgrep:
public class MainActivity extends AppCompatActivity {
    private Button loginButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        loginButton = findViewById(R.id.loginButton);
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Perform login functionality
                performLogin();
            }
        });
        // Rest of the code...
    }
    private void performLogin() {
        // Login functionality
    }
}
rules:
  - id: hardcoded-actions
    patterns:
      - pattern: 'performLogin\(\)'
CodeQL:
Copyright © 2019-2023 HADESS.
      - pattern: 'performAdminAction\(\)'
    message: "Hardcoded actions in onClick methods"
import android
class MainActivity extends AnyFile
{
  MainActivity() {
    exists(
      MethodDeclaration m |
      m.getEnclosingType().toString() = "MainActivity" and
      m.getBody().getAStatement() instanceof MethodInvocation and
      (
        m.getBody().getAStatement().toString().indexOf("performLogin()") >= 0 or
        m.getBody().getAStatement().toString().indexOf("performAdminAction()") >= 0
      )
    )
  }
}
DevSecOps Guides
Rules / C
Noncompliant code:
In this example, the copy_string  function copies the contents of src  to dest . However, there is no
check for the length of dest, and if src is longer than dest, a buffer overflow will occur, potentially
overwriting adjacent memory addresses and causing undefined behavior. In this case, str2 is 7
C
TABLE OF CONTENTS
Buffer Overflow
1
Buffer Overflow
void copy_string(char* dest, char* src) {
  int i = 0;
  while(src[i] != '\0') {
    dest[i] = src[i];
    i++;
  }
  dest[i] = '\0';
}
int main() {
  char str1[6];
  char str2[10] = "example";
  copy_string(str1, str2);
  printf("%s", str1);
  return 0;
}
characters long, so the call to copy_string will overflow the buffer of str1, which has a length of
only 6.
Compliant code:
In this compliant code, the copy_string  function takes an additional parameter dest_size, which is
the maximum size of the dest buffer. The function checks the length of src against dest_size to
avoid overflowing the buffer. The sizeof operator is used to get the size of the dest buffer, so it is
always passed correctly to copy_string. By using the dest_size parameter, the code ensures that
it doesn’t write more data than the destination buffer can hold, preventing buffer overflows.
Semgrep:
CodeQL:
void copy_string(char* dest, char* src, size_t dest_size) {
  int i = 0;
  while(src[i] != '\0' && i < dest_size - 1) {
    dest[i] = src[i];
    i++;
  }
  dest[i] = '\0';
}
int main() {
  char str1[6];
  char str2[10] = "example";
  copy_string(str1, str2, sizeof(str1));
  printf("%s", str1);
  return 0;
}
rules:
  - id: buffer-overflow
    patterns:
      - pattern: 'while\(src\[i\] != \'\\0\'\)'
    message: "Potential buffer overflow vulnerability"
Copyright © 2019-2023 HADESS.
import c
from Function f
where f.getName() = "copy_string"
select f
DevSecOps Guides
Rules / CloudFormation
Noncompliant code:
In this noncompliant code, an AWS CloudFormation template is used to create an S3 bucket. The
bucket name is hardcoded as my-bucket without considering potential naming conflicts or
security best practices. This approach introduces security risks, as the bucket name might
already be taken or it might inadvertently expose sensitive information.
Compliant code:
CloudFormation
TABLE OF CONTENTS
Hardcoded Name
1
Hardcoded Name
# Noncompliant code
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-bucket
# Compliant code
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName:
In the compliant code, the bucket name is dynamically generated using the Fn::Sub intrinsic
function. The bucket name is composed of the string “my-bucket-“, followed by the current
CloudFormation stack name (AWS::StackName), and the AWS region (AWS::Region). This
approach ensures uniqueness of the bucket name within the CloudFormation stack and helps
mitigate potential naming conflicts.
By using dynamic naming with the Fn::Sub function, you can avoid hardcoded values and provide
a more flexible and secure approach to resource creation in CloudFormation.
Additionally, you can implement other security measures such as:
Leveraging IAM policies to control access permissions for the created resources.
Implementing resource-level permissions using AWS Identity and Access Management (IAM)
roles and policies.
Encrypting sensitive data at rest using AWS Key Management Service (KMS) or other
encryption mechanisms.
Implementing stack-level or resource-level CloudFormation stack policies to control stack
updates and prevent unauthorized modifications.
By following security best practices and utilizing dynamic values in CloudFormation templates,
you can enhance the security, flexibility, and reliability of your infrastructure deployments in AWS.
Semgrep:
CodeQL:
        Fn::Sub: "my-bucket-${AWS::StackName}-${AWS::Region}"
]
•
•
•
•
rules:
  - id: noncompliant-s3-bucket-properties
    patterns:
      - pattern: 'Type: AWS::S3::Bucket\n    Properties:\n      BucketName: .+'
    message: "Noncompliant S3 bucket properties"
import cf
from Template t
Copyright © 2019-2023 HADESS.
where exists (Bucket b | b.getType().toString() = "AWS::S3::Bucket")
  and not exists (Bucket b | b.getType().toString() = "AWS::S3::Bucket" and b.getProperties().get
select t
DevSecOps Guides
Rules / Cpp
Noncompliant code:
In this example, the foo() function takes a pointer to an integer and dereferences it to set its value
to 42, but it does not check if the pointer is null. If a null pointer is passed to foo(), a null pointer
dereference will occur, which can cause the program to crash or exhibit undefined behavior.
Compliant code:
Cpp
TABLE OF CONTENTS
Null Pointer Dereference
1
Null Pointer Dereference
void foo(int* ptr) {
    if (ptr != nullptr) {
        *ptr = 42;
    } else {
        // handle error
    }
}
int main() {
    int* ptr = nullptr;
    foo(ptr);
    return 0;
}
Copyright © 2019-2023 HADESS.
DevSecOps Guides
Source: Devsecops War Stories
DevSecOps has emerged as a culture shift in software development, aiming to improve software
security by breaking down silos and fostering collaboration among security professionals and IT
teams. However, the transition to DevSecOps is not without its challenges. In this article, we will
explore one such challenge through a war story of a SAST (Static Application Security Testing)
rollout.
The Context of DevOps
Stories
TABLE OF CONTENTS
Stories
1
DevSecOps War Stories: The Challenges of Implementing SAST
a
Integrating DevSecOps into the Software Development Lifecycle: A Case Study by
Broadcom Software
b
The Evolution of DevSecOps: A Year in Review
c
The Evolution of DevSecOps: Advancing Security in the Digital Age
d
True Story of Implementing SecDevOps in FinTech
e
The Impact of DevSecOps on SOC: Enhancing Security Collaboration
f
Simplifying DevSecOps with Dynamic Application Security Testing (DAST)
g
Enhancing DevSecOps with OWASP DSOMM: A Maturity Model Perspective
h
The Role of Threat Modeling in DevSecOps: Strengthening Security from the Ground Up
i
Hard-Coding Secrets: Be Aware of the Scariest Breach for Your Organization
j
Hilti’s DevSecOps Journey: Building Secure and Efficient Software with GitLab
k
Capital One Data Breach
l
DevSecOps War Stories: The Challenges of Implementing SAST
Before diving into the war story, let’s briefly understand DevOps. DevOps is a modern software
development approach that emphasizes close collaboration between developers and operations
teams, leveraging automation to create reliable and high-quality products. DevOps encourages a
focus on system efficiency, rapid feedback loops, and continuous learning and improvement.
DevOps and Security
The goals of DevOps align well with security objectives. Reliable and performant systems enhance
availability, while automation reduces human error and increases opportunities for security
testing. Additionally, the use of infrastructure-as-code allows security scanning of infrastructure
configurations, similar to application code.
The Promise of DevSecOps
DevSecOps extends the DevOps philosophy by incorporating security into the development
process from the start. It aims to integrate security practices, tools, and expertise seamlessly into
the DevOps pipeline. However, realizing the full potential of DevSecOps requires addressing
various challenges along the way.
The SAST Rollout Story
In this war story, we follow the journey of an AppSec professional tasked with introducing SAST
into a client’s DevOps pipeline. The client was already progressing on their DevOps journey,
regularly pushing code to version control and running CI/CD pipelines every two weeks.
The Challenge of Integration
The client’s development process involved a change management board (CAB) meeting, where
teams presented their cases to move their code to production. Prior to the CAB meeting,
developers conducted their own tests to ensure smooth approval. The AppSec professional
introduced SAST, SCA (Software Composition Analysis), and IaC (Infrastructure-as-Code)
scanning into the CI/CD pipeline, adding three additional tests.
Ancient Applications and Red Flags
While the newer applications successfully passed the security scans, the older ones presented a
different story. The SAST scan results resembled a Christmas tree, with bright red flags indicating
numerous security issues. This revealed a significant challenge in securing legacy applications
within the DevSecOps framework.
The Emailing Mishap
In an effort to encourage developers to fix security issues early in the SDLC, the AppSec
professional configured the SAST tool to email reports whenever code changes were detected.
However, a crucial oversight occurred—every software developer in the company received an
email for each code check-in, causing an overwhelming amount of emails and embarrassment for
the developers.
The Road to Resolution
Upon learning about the unintended consequences of their approach, the AppSec professional
recognized the mistake and took swift action. They restructured the tool’s setup, creating two
separate configurations: one providing a holistic view of the organization’s security posture and
another delivering reports specific to each DevOps team. This adjustment alleviated the
spamming issue and allowed for accurate reporting while respecting the developers’ workflow.
The Importance of Learning and Adapting
The SAST rollout experience serves as a valuable lesson in the DevSecOps journey. When
confronted with the negative impact of their initial approach, the AppSec professional
demonstrated the third way of DevOps—taking time to improve daily work. By acknowledging the
mistake, making the necessary changes, and prioritizing the developers’ experience, they
exemplified the resilience and adaptability required for successful DevSecOps implementation.
Source: Securing the DX NetOps Development Lifecycle with DevSecOps
In today’s digital landscape, the rise of cybersecurity exploits and software vulnerabilities has
become a pressing concern for enterprises. Recent incidents, such as Sun Burst and Log4j, have
highlighted the importance of securing software supply chains and adopting robust security
practices. To address these challenges, forward-thinking organizations like Broadcom Software
have turned to DevSecOps, a strategic approach that integrates security into the early stages of
the software development lifecycle (SDLC).
Software Supply Chain Attacks: Software supply chain attacks have emerged as a significant
threat, targeting developers and suppliers. Attackers exploit unsecured networks and unsafe
SDLC practices to inject malware into legitimate applications. For organizations relying on third-
party software, it becomes nearly impossible to assess the security of every update from every
supplier they use.
Integrating DevSecOps into the Software Development Lifecycle: A Case Study
by Broadcom Software
Embracing DevSecOps: DevSecOps represents a paradigm shift in security tactics and strategies,
moving away from traditional reactive approaches. By adopting DevSecOps, organizations can
embed security practices throughout the SDLC, reducing issues, improving code reliability, and
enabling faster product launches. Broadcom Software’s DX NetOps development organization has
embraced DevSecOps to ensure enterprise-grade software reliability and security.
Key Practices for Secure SDLC at Broadcom Software:
Automation: Broadcom Software has standardized on proven systems for secure continuous
integration (CI) and continuous delivery (CD), minimizing manual interventions and ensuring build
control. Shift-Left Approach: Security checks are conducted early and often through static scans
after every code change, uncovering vulnerabilities and identifying potential risks associated with
third-party components. Continuous Audit: Broadcom Software enforces security throughout the
software lifecycle with a focus on team education, architectural risk assessment, code analysis,
penetration testing, and continuous vulnerability tracking. Bill of Materials: Unique fingerprints are
created to track the source code, bill of materials, and build systems used for every software
release, providing transparency and accountability. Benefits and Culture of Innovation: Broadcom
Software’s implementation of DevSecOps enables agility and speed without compromising
security and compliance. By incorporating security from the start, the organization fosters a
culture of innovation, leveraging the continuous flow of new features and capabilities.
Upgrades and Maintenance: To combat cyber threats effectively, staying up-to-date with the
latest software versions is crucial. Broadcom Software offers regular service packs to DX NetOps
customers, ensuring their products align with the latest security guidelines. The company
provides support during upgrade weekends, reducing the risk of extended downtime and upgrade
failure.
Source: Top Stories Of 2022 From The World Of DevOps
The year 2022 has been marked by numerous challenges, from the global impact of COVID-19
and ongoing conflicts to economic uncertainties. Amidst these adversities, however, innovation
has thrived. Today, as we bid farewell to 2022, let us reflect on the significant milestones in the
world of DevOps. What stands out when we think of DevOps in 2022?
Incorporation of DevSecOps Lifecycle: One of the prominent trends that gained attention in 2022
was the integration of the DevSecOps lifecycle. This approach embraces the shift-left philosophy,
prioritizing security from the beginning rather than treating it as an afterthought. Current
DevSecOps trends reveal that approximately 40% of businesses perform DAST tests, 50%
The Evolution of DevSecOps: A Year in Review
perform SAST tests, and 20% scan dependencies and containers. Enterprises have recognized
the importance of DevSecOps in enhancing security, streamlining governance, and improving
observability.
Serverless Computing and the Bridge between Development and Operations: The adoption of
serverless computing has significantly contributed to the DevOps process. By closing the gap
between development and operations, it has enhanced operability. Moreover, serverless
computing empowers hosts to develop, test, and deploy DevOps pipeline code efficiently. As a
result, more than 50% of enterprises with cloud-based services have integrated serverless
computing into their systems. The serverless market is projected to reach a value of $30 billion by
2030.
Microservice Architecture for Holistic Product Quality: The IT sector extensively embraced
microservice architecture in 2022. Breaking down large-scale applications into smaller,
manageable pieces has simplified development, testing, and deployment processes. This
approach has also facilitated consistent and frequent delivery of software and applications,
thereby improving the holistic quality of products.
AIOps and MLOps: Optimizing DevOps Operations: The significant roles played by AIOps and
MLOps in DevOps operations were notable in 2022. These technologies have optimized
processes for high-quality and rapid releases. MLOps supports the development of machine
learning systems, while AIOps automates IT operations and processes. AIOps allows organizations
to easily identify and resolve issues that hinder operational productivity, while MLOps boosts
productivity through optimization. It is predicted that by 2026, these technologies will grow into a
$40.91 billion industry.
Low-Code DevOps Approach for Enhanced Development and Deployment: In 2022, many robust
enterprises adopted a low-code DevOps approach, reaping benefits for their teams. Businesses
and organizations can now build applications using low-code platforms without the need to learn
how to code. This trend has accelerated the development and deployment processes, enabling
teams to work more efficiently.
GitOps: Automating Infrastructure: Another popular trend that emerged in DevOps workflows in
2022 was GitOps. It revolutionized the control, monitoring, and automation of infrastructure. By
emphasizing increased releases and consistent delivery, GitOps enabled organizations to develop,
test, and deploy software rapidly and efficiently.
Kubernetes: A Continuous and Autonomous Container-Based Ecosystem: Kubernetes, a
continuous and autonomous container-based integration ecosystem, has empowered developers
to scale resources dynamically. It facilitates cross-functional collaboration and minimizes
deployment downtime. Notably, 48% of developers have turned to Kubernetes for container
integration, highlighting its significance in the DevOps landscape.
The Future of DevOps: As DevOps continues to evolve and mature, it has become an
indispensable part of the modern software industry. The associated frameworks and technologies
will continue to drive faster and better development, maintenance, and management of software
and applications.
Source: Epic Failures in DevSecOps by DevSecOps Days Press
In today’s rapidly evolving digital landscape, security has become a critical concern for
organizations. The integration of security practices into the DevOps process has given rise to a
new approach known as DevSecOps. This article delves into the history of DevSecOps and
provides ten actionable ways to advance in this field.
The History of DevSecOps: DevSecOps emerged as a response to the growing need for
incorporating security early in the software development lifecycle. It builds upon the principles of
DevOps, emphasizing collaboration, automation, and continuous integration and delivery. By
integrating security practices from the beginning, DevSecOps aims to ensure that applications
and systems are resilient against potential threats.
10 Ways to Advance in DevSecOps:
See the new world: Recognize that the digital landscape is constantly changing, with new
technologies and threats emerging. Stay updated with the latest trends and challenges to adapt
and enhance your security practices.
Recognize your place in the value chain: Understand your role in the overall value chain of
software development and delivery. Recognize that security is not just an isolated function but an
integral part of the entire process.
Know Agile and DevOps: Familiarize yourself with Agile methodologies and DevOps practices.
Understanding how these frameworks operate will help you align security practices seamlessly
within the development process.
Live out bi-directional empathy: Develop empathy and foster strong collaboration between
security teams and developers. Encourage open communication and mutual understanding to
bridge the gap between security and development.
The Evolution of DevSecOps: Advancing Security in the Digital Age
Do security for the developer’s benefit: Shift the focus of security from being a hindrance to
becoming an enabler for developers. Provide them with the tools, training, and resources they
need to build secure applications without compromising on productivity.
Operationalize DevSecOps: Integrate security practices into the entire software development
lifecycle. Implement automated security testing, code analysis, and vulnerability management
tools to ensure continuous security throughout the process.
Make security normal: Embed security as a core component of the development culture. Promote
security awareness, conduct regular training, and establish security checkpoints at each stage of
development to make security practices a norm.
Track adversary interest: Stay vigilant and monitor evolving threats and adversary interests.
Understand the tactics and techniques used by potential attackers to proactively address
vulnerabilities and protect against emerging threats.
Create security observability: Implement robust monitoring and logging systems to gain visibility
into security events and incidents. Leverage security observability tools and practices to detect
and respond to security breaches effectively.
Build the future: Stay innovative and forward-thinking. Continuously explore emerging
technologies, frameworks, and best practices in DevSecOps. Actively contribute to the
DevSecOps community and share your knowledge and experiences to drive the field forward.
Source: Snyk
In the fast-paced world of FinTech, where technology and finance intersect, security is of
paramount importance. The integration of security practices into the DevOps workflow has given
rise to a powerful approach known as SecDevOps. In the captivating video “The True Story of
Implementing SecDevOps in FinTech” by John Smith, the challenges, successes, and lessons
learned from implementing SecDevOps in the FinTech industry are explored. This article will delve
into the key insights from the video and shed light on the journey of implementing SecDevOps in
the dynamic world of FinTech.
Understanding SecDevOps: SecDevOps, short for Secure DevOps, is an approach that aims to
embed security practices and principles into the DevOps process from the very beginning. It is a
collaborative effort between development, operations, and security teams, working together to
build secure and reliable software solutions. The implementation of SecDevOps ensures that
security is not an afterthought but an integral part of the development lifecycle.
True Story of Implementing SecDevOps in FinTech
Challenges Faced: In the video, John Smith discusses the challenges encountered during the
implementation of SecDevOps in the FinTech industry. One of the primary challenges was the
cultural shift required within the organization. Breaking down silos between teams and fostering
collaboration between developers and security professionals was crucial for success. Additionally,
balancing the need for speed and agility with stringent security requirements posed a significant
challenge. Finding the right balance between these two seemingly opposing forces was key to
achieving success in SecDevOps.
Successes and Lessons Learned: Despite the challenges, the implementation of SecDevOps in
the FinTech industry yielded remarkable successes. One notable achievement was the ability to
identify and mitigate security vulnerabilities early in the development process. By integrating
security practices into every stage of the software development lifecycle, the organization was
able to build robust and secure applications. This resulted in enhanced customer trust and
reduced security incidents.
Throughout the implementation journey, several valuable lessons were learned. Collaboration and
communication were highlighted as critical factors in successful SecDevOps adoption. Open
dialogue between teams, continuous learning, and sharing of knowledge were instrumental in
fostering a culture of security. Furthermore, automation played a pivotal role in ensuring
consistent security practices and enabling faster delivery without compromising on security
measures.
Source: DevSecOps and SOC
The integration of security into the DevOps process, known as DevSecOps, has revolutionized the
way organizations approach software development and deployment. This collaborative approach
not only improves the speed and efficiency of software delivery but also enhances security
practices. In the realm of cybersecurity, the Security Operations Center (SOC) plays a crucial role
in monitoring, detecting, and responding to security incidents. This article explores the
relationship between DevSecOps and SOC, highlighting the ways in which DevSecOps can
positively impact SOC operations.
Developing a Distributed SOC with DevOps Members: Incorporating SOC members who are
familiar with DevSecOps principles can greatly benefit incident response efforts. These team
members possess a deep understanding of the systems and can effectively collaborate with
security staff to identify vulnerabilities and threats. By bridging the gap between the SOC and
DevOps, a more comprehensive and proactive security approach can be established.
The Impact of DevSecOps on SOC: Enhancing Security Collaboration
Collaboration Between Threat Hunters and DevOps Team: Threat hunters, specialized individuals
responsible for proactively identifying security gaps and potential threats, can directly
communicate with DevSecOps or DevOps teams. This direct line of communication allows for
addressing security gaps at their core, rather than isolating threats and reporting them to
management. By involving threat hunters in the development process, organizations can ensure
that security is considered and implemented from the outset.
Implementing Security Best Practices: The SOC can collaborate with specific DevSecOps
development and operation groups to implement security best practices. This collaboration
ensures that security considerations are integrated into the development process, reducing
vulnerabilities and potential exploits. By actively involving the SOC in the implementation of
security measures, organizations can benefit from their expertise in risk assessment, threat
intelligence, and incident response.
SOC as an Advisory Entity: In a DevSecOps environment, everyone involved in security should
have quick access to the SOC and be an integral part of the security story. The SOC serves as an
advisory entity, providing guidance, support, and expertise across the organization. By fostering a
culture of open communication and knowledge sharing, organizations can strengthen their
security posture and respond effectively to emerging threats.
Source: How to declutter DevSecOps with DAST
DevSecOps is a crucial approach that combines development, security, and operations to ensure
secure and efficient software development. However, the complexity and rapid pace of modern
development environments can sometimes lead to challenges in integrating security effectively. In
this article, we will explore how Dynamic Application Security Testing (DAST) can help streamline
DevSecOps processes and enhance application security.
Understanding DAST: Dynamic Application Security Testing (DAST) is a technique used to identify
vulnerabilities and security flaws in applications by actively scanning and testing them during
runtime. Unlike static testing, which analyzes code without execution, DAST assesses applications
in real-world scenarios, simulating various attacks to uncover vulnerabilities.
Continuous Security Assessment: One of the key benefits of DAST in the context of DevSecOps is
its ability to provide continuous security assessment throughout the development lifecycle. By
integrating DAST tools into the DevOps pipeline, security vulnerabilities can be identified and
addressed early on, reducing the risk of exposing sensitive data or falling victim to cyberattacks.
Simplifying DevSecOps with Dynamic Application Security Testing (DAST)
Identifying Real-World Vulnerabilities: DAST tools simulate real-world attack scenarios, allowing
organizations to identify vulnerabilities that may not be apparent through other testing
methodologies. By actively probing applications, DAST tools uncover vulnerabilities that hackers
could exploit, such as injection flaws, cross-site scripting (XSS), and insecure server
configurations.
Collaboration and Automation: DAST can be seamlessly integrated into the DevSecOps workflow,
enabling collaboration between developers, security teams, and operations personnel.
Automation plays a vital role in DAST, as it allows for the continuous scanning of applications
during the development and deployment processes. This collaboration and automation ensure
that security issues are identified and resolved rapidly, reducing the time and effort required for
manual testing.
Remediation and Compliance: DAST provides actionable insights into identified vulnerabilities,
allowing teams to prioritize remediation efforts based on severity. By addressing vulnerabilities
early on, organizations can strengthen their overall security posture and ensure compliance with
industry standards and regulations. DAST also helps organizations demonstrate due diligence in
securing their applications, providing peace of mind to stakeholders and customers.
Source: DevSecOps maturity model using OWASP DSOMM
DevSecOps, the integration of security practices into the software development lifecycle, has
become crucial in today’s fast-paced and evolving digital landscape. To effectively implement and
mature DevSecOps practices, organizations can leverage frameworks and models that provide
guidance and structure. In this article, we will explore the OWASP DSOMM (DevSecOps Maturity
Model) and how it can help organizations enhance their DevSecOps initiatives.
Understanding the OWASP DSOMM: The OWASP DSOMM is a comprehensive maturity model
specifically designed to assess and guide organizations in implementing DevSecOps practices. It
provides a framework that encompasses various dimensions of DevSecOps maturity, including
governance, automation, security controls, and culture. The DSOMM model is based on the Open
Web Application Security Project (OWASP) principles and focuses on aligning security practices
with business objectives.
Assessing DevSecOps Maturity: The DSOMM maturity model consists of several levels, each
representing a different stage of DevSecOps maturity. These levels range from ad hoc security
practices to fully integrated and automated security throughout the development lifecycle. By
Enhancing DevSecOps with OWASP DSOMM: A Maturity Model Perspective
assessing their current maturity level using the DSOMM model, organizations can identify gaps
and establish a roadmap for continuous improvement.
Building a Governance Framework: A crucial aspect of DevSecOps maturity is the establishment
of a robust governance framework. This includes defining security policies, establishing clear
roles and responsibilities, and implementing effective risk management practices. The DSOMM
helps organizations evaluate their governance practices, ensuring that security is integrated into
decision-making processes and aligns with business objectives.
Automating Security Practices: Automation plays a vital role in DevSecOps maturity. By
automating security controls, organizations can reduce human error, enhance efficiency, and
achieve consistent application security. The DSOMM emphasizes the importance of automation
and guides organizations in implementing automated security testing, vulnerability scanning, and
continuous monitoring throughout the software development lifecycle.
Cultivating a Security Culture: DevSecOps is not just about implementing tools and technologies
but also fostering a security-centric culture within the organization. The DSOMM recognizes the
significance of creating a collaborative environment where security is everyone’s responsibility. It
encourages organizations to promote security awareness, provide training, and establish
communication channels for sharing security knowledge and best practices.
Source: Continuous Security: Threat Modeling in DevSecOps
In the fast-paced world of software development, security is a critical concern that cannot be
ignored. DevSecOps, the integration of security practices into the software development lifecycle,
has emerged as a powerful approach to building secure applications. One of the key components
of DevSecOps is threat modeling, a proactive technique that helps identify and address potential
security threats early in the development process. In this article, we will explore the significance of
threat modeling in DevSecOps and how it strengthens security from the ground up.
Understanding Threat Modeling: Threat modeling is a systematic approach to identify, assess, and
mitigate potential security threats and vulnerabilities in software applications. It involves analyzing
the application’s architecture, data flows, and potential attack vectors to uncover security
weaknesses. By identifying and addressing these issues during the design and development
phase, organizations can build robust and secure applications.
Proactive Risk Assessment: Threat modeling enables organizations to take a proactive stance
towards security by identifying potential threats and vulnerabilities before they are exploited by
The Role of Threat Modeling in DevSecOps: Strengthening Security from the
Ground Up
malicious actors. By conducting a comprehensive threat model, organizations can assess the
potential impact and likelihood of various threats and prioritize security measures accordingly.
This helps in allocating resources effectively and mitigating risks early in the development
lifecycle.
Integration into DevSecOps: Threat modeling seamlessly integrates into the DevSecOps approach
by incorporating security considerations into the software development process from the outset.
It fosters collaboration between development, security, and operations teams, ensuring that
security is not an afterthought but an integral part of the development process. Threat modeling
empowers organizations to embed security controls and countermeasures into the application
design, architecture, and code, reducing the likelihood of vulnerabilities.
Identifying Security Design Flaws: Through threat modeling, organizations can uncover design
flaws and weaknesses in the application’s architecture. By simulating potential attack scenarios
and analyzing the impact on the system, teams can identify security gaps that may not be
apparent during traditional code reviews or testing. This enables proactive remediation of security
issues and enhances the overall security posture of the application.
Cost-Effective Security Measures: By identifying security risks early in the development process,
organizations can prioritize security efforts and allocate resources efficiently. Threat modeling
helps teams focus on implementing cost-effective security measures that address the most
critical threats. This approach minimizes the likelihood of expensive security breaches and
reduces the need for reactive security patches or fixes down the line.
Source: Continuous Security: Threat Modeling in DevSecOps
In today’s digital age, organizations face an ever-increasing threat of data breaches and
cyberattacks. While there are various vulnerabilities that attackers exploit, one of the scariest
breaches that can occur is the exposure of hard-coded secrets. Hard-coding secrets, such as
passwords, API keys, and other sensitive information directly into software code, poses a
significant risk to organizations. In this article, we will explore the dangers of hard-coding secrets
and the steps organizations can take to mitigate this potential security nightmare.
Understanding Hard-Coded Secrets: Hard-coding secrets refers to the practice of embedding
sensitive information directly into the source code of applications. While it may seem convenient
during development, it poses a severe security risk. Hard-coded secrets are easily accessible to
anyone who has access to the code, including developers, third-party contractors, and potentially
Hard-Coding Secrets: Be Aware of the Scariest Breach for Your Organization
malicious actors. If an attacker gains access to the codebase, they can extract these secrets and
exploit them for unauthorized access, data theft, or other malicious activities.
The Risks and Consequences: The risks associated with hard-coding secrets are far-reaching and
can have severe consequences for organizations. When secrets are exposed, it can lead to
unauthorized access to sensitive data, compromise user accounts, and even result in financial
loss or damage to the organization’s reputation. Additionally, hard-coded secrets are challenging
to manage and rotate, as they are directly embedded in the code, making it difficult to update
them without modifying and redeploying the entire application.
Best Practices to Mitigate the Risk: To mitigate the risks associated with hard-coded secrets,
organizations should adopt the following best practices:
Use Secure Configuration Management: Store secrets in secure configuration management
systems or vaults that provide encryption and access control mechanisms. These tools allow for
centralized management, secure storage, and controlled access to sensitive information.
Implement Environment Variables: Utilize environment variables to store secrets and configure
applications to retrieve these values at runtime. This approach separates secrets from the
codebase and enables easy configuration changes without modifying the application’s source
code.
Employ Secrets Management Solutions: Leverage secrets management solutions that provide
secure storage, rotation, and distribution of secrets. These solutions offer a more robust and
scalable approach to managing sensitive information throughout the development and
deployment lifecycle.
Follow Principle of Least Privilege: Limit access to secrets by following the principle of least
privilege. Only provide necessary access to individuals or services, and regularly review and
revoke access rights to minimize the risk of unauthorized exposure.
Continuous Security Testing: Regularly conduct security testing, including static code analysis
and dynamic application security testing (DAST), to identify and remediate any instances of hard-
coded secrets. Implementing a comprehensive security testing program helps organizations
identify vulnerabilities and ensure that secrets are not inadvertently embedded in the codebase.
Source: How CI/CD and robust security scanning accelerated Hilti’s SDLC
Hilti’s DevSecOps Journey: Building Secure and Efficient Software with GitLab
DevSecOps has become a crucial practice for organizations seeking to develop secure and
efficient software. Hilti, a global leader in the construction industry, has embraced DevSecOps
principles and harnessed the power of GitLab to enhance its software development processes. In
this article, we will explore Hilti’s DevSecOps journey and how GitLab has played a pivotal role in
integrating security seamlessly into their development pipeline.
Embracing DevSecOps Culture: Hilti recognized the importance of shifting security left in the
software development lifecycle. By adopting DevSecOps principles, they fostered a culture where
security is an integral part of the development process from the start. This cultural shift
encouraged collaboration between development, security, and operations teams, resulting in
faster, more secure software delivery.
Integrated Security Tools: GitLab’s comprehensive platform provided Hilti with a wide array of
built-in security features and tools. From static application security testing (SAST) and dynamic
application security testing (DAST) to dependency scanning and container security, GitLab
enabled Hilti to automate security checks throughout the development process. This integration
allowed for early detection of vulnerabilities and ensured that security was continuously
monitored and addressed.
Automated Testing and Continuous Integration: Hilti leveraged GitLab’s continuous integration
capabilities to automate their testing processes. By integrating security testing into their CI/CD
pipelines, they ensured that every code change was thoroughly examined for potential security
issues. This approach enabled Hilti to catch vulnerabilities early on, reducing the risk of security
breaches and improving the overall quality of their software.
Collaboration and Visibility: GitLab’s collaborative features allowed Hilti’s teams to work
seamlessly together. Developers, security professionals, and operations personnel could easily
communicate and collaborate within the same platform, promoting cross-functional teamwork and
knowledge sharing. Additionally, GitLab’s intuitive dashboards provided clear visibility into the
security posture of their projects, enabling proactive remediation of vulnerabilities.
Compliance and Governance: As a global organization, Hilti operates in a regulated environment
and must adhere to various compliance standards. GitLab’s compliance management features
helped Hilti streamline their compliance efforts by providing a centralized platform for managing
policies, controls, and audits. This ensured that their software development practices met the
necessary regulatory requirements.
Capital One Data Breach
One notable real-world example of an attack resulting from inadequate Identity, Credential, and
Access Management (ICAM) in the cloud environment is the Capital One data breach in 2019. The
breach exposed the personal information of approximately 106 million customers and applicants.
In this case, the attacker exploited a misconfiguration in the web application firewall of Capital
One’s cloud infrastructure. The misconfiguration allowed the attacker to gain unauthorized access
to a specific server and execute commands, ultimately exfiltrating sensitive customer data.
The root cause of the breach was attributed to inadequate ICAM practices, specifically related to
the mismanagement of access controls and permissions. The attacker, a former employee of a
cloud service provider, utilized their knowledge of the cloud infrastructure’s vulnerabilities to
bypass security measures.
The inadequate ICAM practices in this incident included:
Copyright © 2019-2023 HADESS.
Insufficient access controls: The misconfiguration of the web application firewall allowed the
attacker to exploit a specific vulnerability and gain unauthorized access to the server.
1
Weak authentication mechanisms: The attacker was able to exploit weak authentication
mechanisms to gain initial access to the cloud infrastructure.
2
Inadequate monitoring and logging: The breach went undetected for a significant period due
to a lack of proper monitoring and logging practices. This delayed response allowed the
attacker to access and exfiltrate data without being detected.
3
Cover by Greg Rutkowski
HADESS is proud to commemorate our anniversary, marking a year of
unwavering commitment to cybersecurity excellence. As we look back on this
milestone, we celebrate the accomplishments, growth, and significant
milestones that have shaped our journey. Throughout the past year, we have
continued to fortify our position as a trusted partner in safeguarding digital
assets, protecting organizations from evolving cyber threats, and ensuring a
secure and resilient future.
