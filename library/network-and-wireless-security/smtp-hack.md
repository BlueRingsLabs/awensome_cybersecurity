---
id: ckb-a204ce0fd795
title: SMTP Hack
category: network-and-wireless-security
format: article
language: en
tags: [powershell, python]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.78
---

# SMTP Hack

When I enter the company (if I am hired to make a mess, not to break in), the first thing I do is look for the [low hanging fruit](https://en.wiktionary.org/wiki/low-hanging_fruit). If there are a lot of them, I know the job will be easy and the company will have a lot to do in the next few months or even years if there is a mess in the environment. If there are no easy choices, I know it will be challenging and I will really have to work to show some results. Sometimes I won’t show anything, but that doesn’t mean I’m bad (or maybe I am), it just means the company is very well protected and ready for the attacker or insider threat (or ready for more skilled pentester). One of the tests I do is to check servers, forwarders or email relays.

But before I start, today’s header image for this article was created by a user of the 0ut3r Space Discord server, thanks for the interesting fan graphics. If you would like to hire this young artist for any kind of graphic work, feel free to visit Discord and contact user @011.

![SMTP Hack](smtp-hack.webp)

Oki doki, the unauthorized sending of email through a company’s email servers, relays and forwards is a very old vulnerability. Maybe it is no a vulnerability, but a misconfiguration, or a configuration that was made before Christ and that nobody has ever changed. In a nutshell, this SMTP configuration allows emails to be sent without authorization. E.g. by connecting via telnet to port 25, executing a few commands and sending a message on behalf of anyone in the company to anyone inside or outside the company, so that it looks like a real message.

Spam groups often look for such gems to send out their spam in a very credible way. It can also be used in a hacking attack to send phishing emails to gain access to another part of the network or server and obtain the login and password of a more privileged user - a classic lateral movement. Also cool for financial fraud, by analyzing a company’s email communications, either within the company or from a leak in the past, it is easy to determine who is writing to whom, who is sending the invoices to whom, what the information on deposit account changes looks like, etc. It is then very easy to send a fake message that looks legitimate to a partner of the company just before an important transfer that there has been a change in the deposit account and replace account. You can, for example, rake in a million and disappear. All you have to do is get access to one company user’s computer, send an email and wait for the transfer. It is possible to send such an email to several companies and claim even more, or at least one of it, before anyone notices. I don’t need to explain this to you - you know what you can do with a fake email.

All right, but why such an error in the configuration? A few ideas spring to mind.

1. Lack of knowledge of the person who configured it, because they did it a very long time ago when the company was just being established. Nobody ever audited it afterwards.
2. The configuration was set up so that the administrator could check the connectivity and operation of the email server and it stayed that way.
3. The company has old equipment or equipment that is so simple (OT in production) that it cannot send status information or alerts in any other way than in plain text via the mail server without authorization. Instead of putting up a separate relay just for the OT that can only send certain things to certain places an existing email server was used.

There is probably more, but who cares?

## Telnet to port 25

A simple test to see if it is possible to send unauthorised messages? Telnet to port 25 of your SMTP relay, forwarder or mail server.

You can use Putty if you are on Windows, or just the telnet command if you are on Linux.

```powershell
PUTTY.EXE -telnet smtp.example.org 25
or
telnet smtp.example.org 25
```

If the connection is successful, type commands:

```bash
helo localhost
ehlo localhost
mail from: user1@example.org
rcpt to: user2@example.org
data
Subject: Test Subject
Content-Type: text/plain OR Content-Type: text/html
Message content or HTML code
.
```

1. `helo localhost`: This command initiates the SMTP session and identifies the sender’s domain to the receiving server. In this case, it’s saying “hello” to the server and identifying itself as “localhost” (the local host or domain or whatever you would type here).
2. `ehlo localhost`: Similar to `helo`, `ehlo` (extended hello) is another command to initiate the SMTP session. It provides extended information about the client’s capabilities to the server. Again, it’s saying “hello” to the server, but in a more extended manner, and identifying itself as “localhost.” It will also show you possible commands to use on the server.
3. `mail from: user1@example.org`: This command specifies the sender’s email address. In this case, it’s indicating that the email is from “[user1@example.org](mailto:user1@example.org)“.
4. `rcpt to: user2@example.org`: This command specifies the recipient’s email address. It tells the server that the email should be delivered to “[user2@example.org](mailto:user2@example.org)“.
5. `data`: This command indicates the start of the email message data. It tells the server that the following lines will contain the email content.
6. `Subject: Test Subject`: This line sets the subject of the email to “Test Subject”.
7. `Content-Type: text/plain OR Content-Type: text/html`: This line specifies the content type of the email body. It can be either plain text (`text/plain`) or HTML (`text/html`), depending on which one is chosen.
8. `Message content or HTML code`: This is the actual content of the email message. It can be either plain text or HTML code, depending on the content type specified earlier.
9. `.` (period): This signifies the end of the email message data. It tells the server that the email content has finished and should be processed and delivered accordingly.

These commands are fundamental to the SMTP protocol for sending email from a client to a server.

I found that the connection was sometimes lost while typing the commands, so I wrote a script in PowerShell and Python to automate this.

### PowerShell mail sender

It will do the same as the commands from Telnet example, but all in one. Comments in the code.

```bash
# Setting up the sender email address
$From = user1@example.org

# Setting up the recipient email address
$To = user1@example.org

# Setting up the email subject
$Subject = "Test Subject"

# Setting up the email body content, can be html or text
$Body = "Test Body"

# Defining additional email headers including MIME version and content type
$Headers = @{
  "MIME-Version" = "1.0"
  "Content-Type" = "text/html; charset=UTF-8"
}

# Constructing headers string for the email
$HeadersString = ""
foreach ($key in $Headers.Keys) {
  $HeadersString += "$($key): $($Headers[$key])`r`n"
}

# Setting up the SMTP server address 
$SmtpServer = "smtp.example.org"

# Setting up the SMTP server port
$Port = 25

# Sending the email using Send-MailMessage cmdlet with specified parameters
Send-MailMessage -From $From -To $To -Subject $Subject -Body $Body -BodyAsHtml -SmtpServer $SmtpServer -Port $Port -Encoding ([System.Text.Encoding]::UTF8) 
#remove -BodyAsHtml to send it as plain text
```

Now set up your own mails and server address and test it out! Make sure your boss has given you permission to do this ;)

### Python mail sender

Example 1, with html code as body, less comments as you already know what is happening, based on the previous examples.

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Mail settings
smtp_server = "smtp.example.org"
smtp_port = 25
sender_email = "user1@example.org"
receiver_email = "user2@example.org"
subject = "Test Subject"

# HTML message content
html_content = """
<html>
HTML CODE HERE
</html>
"""

# Creating the message
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject

# Adding HTML content to the message
msg.attach(MIMEText(html_content, "html"))

# Sending the message
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.sendmail(sender_email, receiver_email, msg.as_string())
```

Example 2, different approach and body as text:

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

# Setting the sender's email address
from_email = user1 @ example.org

# Setting the recipient's email address
to_email = user2 @ example.org

# Setting the email subject
subject = "Test Subject"

# Setting the email body content
body = "Test Body"

# Creating an instance of MIME Multipart
msg = MIMEMultipart()

# Setting the headers
msg["From"] = from_email
msg["To"] = to_email
msg["Subject"] = Header(subject, "utf-8")

# Setting custom headers
msg.add_header("MIME-Version", "1.0")
msg.add_header("Content-Type", 'application/ms-tnef; name="winmail.dat"')
msg.add_header("Content-Transfer-Encoding", "binary")

# Creating the email body content as MIMEText
body_content = MIMEText(body, "plain")

# Attaching the email body content to the message
msg.attach(body_content)

# Setting the SMTP server
smtp_server = "smtp.example.org"
smtp_port = 25

# Creating an SMTP connection
server = smtplib.SMTP(smtp_server, smtp_port)

# Sending the email message
server.send_message(msg)

# Closing the SMTP connection
server.quit()
```

Please don’t laugh at my code, I’m just learning Python.

So these are the simplest steps to see if we can mess with SMTP in the company.

Some companies add some sort of configuration on the server to add a banner saying that the message is from outside, even though you sent it internally using examples above, or a banner saying that you rarely receive email from a certain person in the company, e.g. the CEO. If you send the message as text rather than HTML, the formatting of these banners will also be ignored and they will be plain text, i.e. they will not glow red or yellow. Also, I know from experience that people see the same banners over and over again and ignore them after a while. When you send a message outside your company, nothing of the sort will happen. The message will be normal, without warnings, and after checking the source, the official company name will appear.

Enjoy the pentesting.
