---
id: ckb-9c225a27218c
title: API Security Handbook
category: application-security
format: guide
language: en
tags: [api-security, devsecops, password-security, tls, web-security]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.95
---

Table of Contents

What is API?
4
What is API Testing?
6
What is REST API?
6
Difference between REST API vs SOAP API.
8
What to Test in API Testing?
8
HTTP - Fundamentals
9
What is an Cookies?
10
What is Authentication?
10
HTTP Methods explained.
12
HTTP GET Method Explained -
12
HTTP POST Method Explained -
13
HTTP PUT Method Explained -
13
HTTP PATCH Method Explained -
14
HTTP DELETE & OPTIONS Method Explained -
14
HTTP HEAD/TRACE Method Explained -
15
How to Test an API ( API Testing)?
15
API Testing tools
16
How to do API Testing using Postman
16

What is API?

API stands for the Application Programming Interface, They are basically a collection of functions and
procedures which allows us to communicate two application or library.

For example, It like a connector as seen in the picture. All data connects to our organization through API.

In one line, API is its an interface between different software programs or service.

Simple Examples is,
Suppose you go to a restaurant.

API is the messenger that takes your order(waiter) and tells the system(kitchen) what to do (to prepare food)
and in return gives back the response you asked for (waiter returns with the ordered food).
Source - Quora. https://www.quora.com/What-is-an-API

Type of APIs :-

What is API Testing?

When we talk about API Testing,

API testing is testing that APIs and its integration with the services.

It is one of the most challenging type of testing, If we miss the certain cases in API Testing that can cause a
very big problem in production after full integration and it will hard to debug in production environment..

In this definite guide,
We are basically discussing about the REST API Testing.Where we need to test the REST APIs for the
validation, error codes and load testing.

What is REST API?
As REST is an acronym for REpresentational State Transfer, statelessness is key. An API can be REST if it
follows the below constraints.

The REST architectural style describes six constraints. These constraints, put on the architecture, were initially
communicated by Roy Fielding in his doctoral dissertation and defines the basis of RESTful-style.

1. Uniform Interface
2. Stateless
3. Cacheable
4. Client-Server
5. Layered System
6. Code on Demand

Uniform Interface
The uniform interface constraint defines the interface between clients and servers.
In other terms,

First constraint of the REST API states that the Client and server has to communicate and agree to certain
rules based on resources(they should communicate with same resource like json, xml, html , txt) and with
proper encoding like UTF-8 extra.
Another point they should communicate with the Self-descriptive Messages e.g Use the same MIME types.

Stateless
APIs in REST are stateless and Client and server doesn’t worry about the state of the request or response..

Cacheable
According to the World Wide Web, clients can cache responses. Responses should therefore, implicitly or
explicitly, define themselves as cacheable. Its upto server when they want the cache to expired etc.

Client-Server
Client and Server are two different entity, It means that servers and clients may also be replaced and
developed independently, as long as the interface is not altered.

Layered System.
It means that the between client and server there can be any number of layered systems it does not matter.

Code on Demand
Server can store the Code or logic to themselves and transfer it whenever needed rather client side logic.

If any API fulfill all the constraints then we can it REST API.

Difference between REST API vs SOAP API.
We have already discussed REST API , Lets now Learn what is SOAP API.

SOAP (Simple Object Access Protocol) is a messaging protocol that allows programs that run on disparate
operating systems or services like frontend or backend to communicate using Hypertext Transfer Protocol
(HTTP) and its Extensible Markup Language (XML).

SOAP uses WSDL is an XML format for describing network services as a set of endpoints operating on
messages containing either document-oriented or procedure-oriented information.

Enough of background lets come to topic…

What to Test in API Testing?

●
Validate the keys with the Min. and Max range of APIs (e.g maximum and minimum length)
●
Have a Testcase to do XML,JSON Schema validation.
●
Keys verification. If we have JSON, XML apis we should verify it's that all the keys are coming.
●
Verify that how the APIs error codes handled.

Lets understand why API Testing is important…
Why you should perform API Testing?
●
Many of the services that we use every day rely on hundreds of different interconnected APIs, if any
one of them fails then the service will not work.

●
Right now, Internet uses millions of APIs and they should be tested thoroughly.

●
Developers make mistake and they create buggy APIs..

●
Validation of APIs is very important which are going live to production.

Above image shows the architecture of an application and notice that API Testing is important part..
Now…
Lets learn one more concept HTTP Methods

HTTP - Fundamentals

HTTP is an application layer protocol designed within the framework of the Internet protocol suite.

There is Client which perform a request resource which can be HTMLPage, file extra from Server and server
perform the response to the client back using the same protocol known as HTTP.

HTTP is a stateless protocol. In other words, the current request does not know what has been done in the
previous requests.

What is an Cookies?
Cookies are usually small text files, given ID tags that are stored on your computer's browser directory or
program data subfolders.

GET /spec.html HTTP/1.1
Host: www.example.org
Cookie: theme=light; sessionToken=abc123

Record the user's browsing activity.
Which pages were visited in the past.
Contain the name of the domain & Lifetime.
Tool : EditThisCookie - http://bit.ly/1oe1o08

What is Authentication and its types lets understand it...

What is Authentication?
Authentication is a process of presenting your credentials like username, password or another secret key to
the system and the system to validate your credentials or you. In the API terms Authentication is used to
protect the content over web mean only a valid user with valid credentials can access that API endpoint.
These credentials tell the system about who you are. Which enables the system to ensures and confirms a
user’s identity. Here system can be anything, it can be a computer, phone, bank or any physical office
premises.

Basic authentication - String is encoded with Base64.
curl --header "Authorization: Basic am9objpzZWNyZXQ=" my-website.com
Digest Authentication - Authentication is performed by transmitting the password in an ENCRYPTED
form.(With Some Salt etc)

OAuth- Authentication protocol that allows you to approve one application interacting with another on your
behalf without giving away your password.

E.g OAuth 1, 2.

More authentication are discussed here -
https://scrolltest.com/2018/11/22/how-to-handle-authentications-with-postman/

In Client as Browser and Server as DB with the service running in PHP.

We can create an HTTP request from browser by typing a URL.

Just for more information, URL can be broken down into the further chunks like protocol, host , post and query
params. More discussion is out of scope for URL

Lets Understand what all HTTP methods are present
HTTP Methods explained.

HTTP GET Method Explained -

.
HTTP POST Method Explained -

HTTP PUT Method Explained -

HTTP PATCH Method Explained -

HTTP DELETE & OPTIONS Method Explained -

HTTP HEAD/TRACE Method Explained -

Now we have a HTTP Methods knowledge lets understand what are Cookie and authentication.

How to Test an API ( API Testing)?

Before that take a look into the example api that can available freely.
https://api.chucknorris.io/jokes/random

Here Keys are
cateroy, icon_url, id, url and value and they have corresponding values as String or number.
API Testing can be done manually or using a Tools. It is always recommend to certain tools.

Lets learn API Testing using our favorite tools..
Below is the list of API testing tools, You can learn or use whichever tool you feel is great for you, I encourage
you to start with Postman it's an awesome API Testing tool which provide lots of feature like command line,
CI/CD and monitoring of APIs with testcase support.

API Testing tools

●
Runscope.com
● Postman CI/CD
●
Katalon using CI/CD
●
SoapUI CI/CD
●
Rest Assured CI/CD

API Testing using POSTMAN

What is Postman?

First of all, let’s understand what is Postman.

It is an API Testing tool used by developers and Testers to perform API Testing with lots of different features
like Global variables, mock request, Environment and monitoring of APIs.

You can learn more about a postman in my full Video lecture series here. Download and install it.
P.S – This article assumes that you have some experience with Postman. If not please go through my previous
tutorials.

Its available in the MacOS, Windows and Linux as Native app.

Download Postman - https://www.getpostman.com
Major features of postman
