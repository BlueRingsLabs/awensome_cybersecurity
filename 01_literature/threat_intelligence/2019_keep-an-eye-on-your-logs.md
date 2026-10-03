[[ PAGE 1 ]]

# Keep an eye on your logs

It is important to check and analyze logs, not just to find errors but also to make sure that system, installed applications and services are secure and work correctly. You can track and monitor important events manually from console and automatically using some third part applications.

![logs](logs.jpg)

Today I will just let you know where to find logs, which of them are most important and how to view them in console. At the end I will show you how to configure [logwatch](https://sourceforge.net/projects/logwatch/) to get daily email notification with logs summary.

The log files generated in a Linux can be classified into four different categories:

- Application Logs
- Event Logs
- Service Logs
- System Logs

Monitoring and analyzing all of them can be a challenging task.

All log files can be displayed in console using on of these commands:

`more` - is used to view the text files in the command prompt, displaying one screen at a time in case the file is large. The more command also allows the user do scroll up and down through the page.

`less` - similar to more, less command allows you to view the contents of a file and navigate through file. The main difference between more and less is that less command is faster because it does not load the entire file at once and allows navigation though file using page up/down keys.

`cat` - stands for “catenate.” It reads data from files, and outputs their contents. It is the simplest way to display the contents of a file at the command line.

`grep` - which stands for “global regular expression print,” processes text line by line and prints any lines which match a specified pattern.

`tail` - outputs the last part, or “tail”, of files. It can also monitor new information written to the file in real time, displaying the newest entries.

You can combine these commands and use various parameters, check some examples below:

```bash
tail -f /var/log/access.log | grep 24.10.160.10
```


```bash
cat /var/log/access.log | more
```


```bash
tail -f -n 5 /var/log/syslog
```

Take some time and [DuckDuck](https://duckduckgo.com/) this commands to learn more about their usage and parameters.

## Important log files

### System Logs

```bash
cat /var/log/syslog
```

Store informational and non-critical system messages. You can track non-kernel boot errors, application-related service errors and the messages that are logged during system startup.

### Authentication

```bash
cat /var/log/auth.log
```

All authentication related events in Debian and Ubuntu server are logged here. Investigate failed login attempts, brute-force attacks and other vulnerabilities related to user authorization mechanism.

### Boot

```bash
cat /var/log/boot.log
```

Booting related information and messages logged during system startup process. Check for issues related to improper shutdown, unplanned reboots or booting failures.

### Kernel

```bash
cat /var/log/kern.log
```

Perfect for troubleshooting kernel related errors and warnings.

### Mail

```bash
cat /var/log/mail.log
```

All mail server related logs are stored here.

### Database

```bash
cat /var/log/mysql.log
```

All debug, failure and success messages related to the MySQL/MariaDB

### Other

Depends on what is installed on your system, you can have other various log files.

All are located in `/var/log/`, check what you have there using command:

```bash
ls /var/log/
```

## Logwatch

Logwatch is an application that helps with simple log management by daily analyzing and reporting a short digest from activities taking place on your machine.

You can install it from repository:

```bash
sudo apt install logwatch
```

or download latest version from [SourceForge](https://sourceforge.net/projects/logwatch/files/) and run installation script.

Make a copy of default configuration to avoid overwrite configuration file during update.

```bash
sudo cp /usr/share/logwatch/default.conf/logwatch.conf /etc/logwatch/conf/logwatch.conf
```

Edit configuration:

```bash
sudo nano /etc/logwatch/conf/logwatch.conf
```

Things you need to change:

```bash
Output = mail
Format = html
MailTo = your@email.com
MailFrom = your@email.com
Range = yesterday
Detail = Low
Service = All
```

**Output** - can be set to mail or stdout.

**Format** - html or text.

**MailTo** and **MailFrom** is your email address.

**Range** - you have options of receiving reports for All (all available since the beginning), Today (just today) or Yesterday (just yesterday).

**Detail** - options are: Low, Medium and High.

**Service** - By default, Logwatch covers a really wide range of services. If you would like to see a full list, you can query the contents of the file scripts/services, example:

```bash
ls -l /usr/share/logwatch/scripts/services
```

You can choose to receive reports for all services or some specific ones. For all services, keep the line as: `Service = All`. If you wish to receive reports for specific ones, modify it similar to the following example, listing each service on a new line e.g. `Service = [name]`

```bash
Service = sendmail
Service = http
Service = identd
Service = sshd2
Service = sudo
..
```

If you do not wish to have daily reports generated, you should uncomment this line.

```bash
DailyReport = No
```

Next step is to create cache folder:

```bash
sudo mkdir /var/cache/logwatch 
```

You can generate test report to see how it works:

```bash
sudo logwatch --output stdout --detail med --format text
```

By default logwatch will send daily report because cron is configured here:

```bash
/etc/cron.daily/00logwatch
```

If you would like to modify time of report remove that file and add new entry to cron, e.g.:

```bash
0 6 * * * root /usr/sbin/logwatch --output mail
```

Thats all, you can now analyze logs report on your email.
