[[ PAGE 1 ]]

# Send emails by local applications only

It is good if your server can talk to you. Maybe not literally, but it’s good if it can send you emails with logs or issues. It’s also nice to allow your website script located on server to send some emails, to users or administrators. You do not always need a fully configured mail server for this. All you need is a simple [MTA](https://en.wikipedia.org/wiki/Message_transfer_agent) for internal communication.

![Send Only SMTP](mtaserver.jpg)

There is a lot of [mail server software](https://en.wikipedia.org/wiki/List_of_mail_server_software). I will use one of the most popular, which is [Postfix](http://www.postfix.org/). In this article you will also find two alternatives ([SSMTP](https://github.com/ajwans/sSMTP) and [MSMTP](https://marlam.de/msmtp/)) for [SMTP](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol) solution which allow your server to send emails.

## Postfix

Here are steps to configure Postfix as a send-only SMTP server.

Install postfix and mail utilities.

```bash
sudo apt install postfix
sudo apt install mailutils
```

During installation of Postfix you will be asked to choose mail configuration and domain. Choose `Internal Site` and enter the fully qualified name of your domain, **fqdn.example.com**. This configuration allow Postfix to process requests to send emails only from the server on which it is running, i.e. from localhost.

Now edit configuration.

```bash
sudo nano /etc/postfix/main.cf
```

Change the line that reads `inet_interfaces = all` to `inet_interfaces = loopback-only`

Also modify `mydestination`

```bash
mydestination = $myhostname, localhost.$your_domain, $your_domain
```

That’s all. Now restart Postfix using command:

```bash
sudo systemctl restart postfix
```

It’s worth to edit aliases:

```bash
sudo nano /etc/aliases
```

and add email for users or services, example below.

```bash
root: your_email_address1
default: your_email_address2
postmaster: your_email_address3
```

Save file and run:

```bash
sudo newaliase
```

### Sending test email

To send email use command:

```bash
echo "This is the body of the email" | mail -s "This is the subject line" email_address
```

### Hardening Postfix

In addition, since we are already in the Postfix subject it’s worth to mention how to make your mail server more secure. Here are some tips.

Make sure the Postfix is running with non-root account:

```bash
ps aux | grep postfix | grep -v '^root'
```

Change permissions and ownership on the destinations below:

```bash
chmod 755 /etc/postfix
chmod 644 /etc/postfix/*.cf
chmod 755 /etc/postfix/postfix-script*
chmod 755 /var/spool/postfix
chown root:root /var/log/mail*
chmod 600 /var/log/mail*
```

Edit `/etc/postfix/main.cf` and add make the following changes:

Configure Trusted Networks, for example:

Configure the SMTP server to masquerade outgoing emails as coming from your DNS domain, for example:

```bash
myorigin = example.com
```

Configure the SMTP domain destination, for example:

```bash
mydomain = example.com
```

Configure to which SMTP domains to relay messages to, for example:

```bash
relay_domains = example.com
```

Configure SMTP Greeting Banner:

```bash
smtpd_banner = $myhostname
```

Limit Denial of Service Attacks:

```bash
default_process_limit = 100
smtpd_client_connection_count_limit = 10
smtpd_client_connection_rate_limit = 30
queue_minfree = 20971520
header_size_limit = 51200
message_size_limit = 10485760
smtpd_recipient_limit = 100
```

Restart the Postfix daemon:

```bash
sudo service postfix restart
```

### Make it more private

You can hide some information from header of emails sent by your server. To do that, create file

```bash
sudo nano /etc/postfix/header_checks
```

and add lines:

```bash
/^Received:/			        IGNORE
/^X-Originating-IP:/            IGNORE
/^X-Mailer:/                    IGNORE
/^Mime-Version:/                IGNORE
/^User-Agent:/                  IGNORE
```

Now edit Postfix configuration

```bash
sudo nano /etc/postfix/main.cf
```

and add at the end

```bash
mime_header_checks = regexp:/etc/postfix/header_checks
header_checks = regexp:/etc/postfix/header_checks
```

Rebuild the hash table:

```bash
postmap /etc/postfix/header_checks
```

and reload the postfix configuration:

```bash
sudo service postfix restart
```

## SSMTP

SSMTP is a program which delivers email from a local computer to a configured mailhost. It is not a mail server and does not receive mail, expand aliases or manage a queue. One of its primary uses is for forwarding automated email (like system alerts) off your machine and to an external email address.

This is good alternative to Postfix solution and configuration is very easy.

Install software:

```bash
sudo apt install ssmtp
```

Edit ssmtp configuration:

```bash
sudo nano /etc/ssmtp/ssmtp.conf
```

Here is example for Gmail account:

```bash
mailhub=smtp.gmail.com:587
rewriteDomain=
UseSTARTTLS=YES
AuthUser=username@gmail.com
AuthPass=your_gmail_password
FromLineOverride=YES
```

Edit revaliases configuration:

```bash
sudo nano /etc/ssmtp/revaliases
```

Add:

```bash
root:username@gmail.com:smtp.gmail.com:587
```

Send test email:

```bash
echo "This is the body of the email" | mail -s "This is the subject line" email_address
```

To allow PHP mail use this solution you need to make a change in your `php.ini` configuration file. It’s located in various places depends on distribution and PHP version. Below is and example for PHP7.2 FPM

```bash
sudo nano /etc/php/7.2/fpm/php.ini
```

change `sendmail_path`:

```bash
sendmail_path = /usr/sbin/ssmtp -i
```

## MSMTP

In the default mode, it transmits a mail to an SMTP server (for example at a free mail provider) which takes care of further delivery. So doing same thing like SSMTP but is constantly developed (SSMTP is not maintained anymore) and offer more:

- Sendmail compatible interface (command line options and exit codes)
- Support for multiple accounts
- TLS/SSL support including client certificates
- Many authentication methods
- Support for Internationalized Domain Names (IDN)
- Fast SMTP implementation using command pipelining
- DSN (Delivery Status Notification) support
- SOCKS proxy support

Lets do it, Install software:

```bash
sudo apt-get install msmtp
```

Edit msmtp configuration:

```bash
sudo nano /etc/msmtprc
```

Here is example for Gmail account:

```bash
defaults
tls on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile /var/log/msmtp.log
account gmail
host smtp.gmail.com
port 587
auth on
user username@gmail.com
password your_gmail_password
from username@gmail.com

account default : gmail
```

Change permission:

```bash
sudo chmod 0644 /etc/msmtprc
```

Create log file and add permission:

```bash
sudo touch /var/log/msmtp.log
sudo chmod 0777 /var/log/msmtp.log
```

Send test email using msmtp:

```bash
echo -e "Subject: This is the subject line\r\n\r\nThis is the body of the email" | msmtp -t test@test.com
```

you can choose from which account message should be sent:

```bash
echo -e "Subject: This is the subject line\r\n\r\nThis is the body of the email" | msmtp --account=gmail-t test@test.com
```

send message from file:

```bash
cat name.file | msmtp
```

debug option

```bash
echo -e "Subject: This is the subject line\r\n\r\nThis is the body of the email" | msmtp -t test@test.com -d
```

debug to file:

```bash
echo -e "Subject: This is the subject line\r\n\r\nThis is the body of the email" | msmtp -t test@test.com -d > test_log
```

Once everything is working fine, link msmtp as sendmail. You can use ready solution by installing:

```bash
sudo apt install msmtp-mta
```

or create link manually

```bash
sudo ln -s /usr/bin/msmtp /usr/lib/sendmail
sudo ln -s /usr/bin/msmtp /usr/bin/sendmail
sudo ln -s /usr/bin/msmtp /usr/sbin/sendmail
```

thanks to that you can send emails using mail command:

```bash
echo "This is the body of the email" | mail -s "This is the subject line" email_address
```

For PHP mail function is the same story like with SSMTP. Edit your `php.ini` file:

```bash
sudo nano /etc/php/7.2/fpm/php.ini
```

and change `sendmail_path`:

```bash
sendmail_path = "/usr/bin/msmtp -t"
```

## Other scripts

For Wordpress you can use for example plug-in [EASY WP SMTP](https://wordpress.org/plugins/easy-wp-smtp/). Other popular scripts also have some plug-ins or already implemented solution to send email directly from website script.

That’s all for today. Let me know in comments if you have some suggestions or improvements.
