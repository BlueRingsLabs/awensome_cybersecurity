[[ PAGE 1 ]]

# Server backup

It is good to have a backup of your server. After you configure your server and run a website don’t forget prepare automatic backup. I also encourage you to do the same with your data at home.

![backup](backup.jpg)

You can also make a manual backup which is not bad, however I know from experience that sooner or later you will forget, or give up this manual task. In fact, the whole process can be completely automated. That is why it is worth to configure it once and only monitor it from time to time.

Just after setting up the server and its configuration you should make a copy of all configuration files in which you made some changes. It is enough to make such copy once and update only when some changes are made. As the changes in the configuration do not take place too often, you can do this part manually.

The most important is the backup of services that work on your server. For example, I will describe below the backup of two most popular services on the server. Website server and database.

## Requirements

To make everything work properly you need a few additional packages, install them with the commands below.

[Rclone](https://rclone.org/) - is a command line program to sync files and directories.

```bash
curl https://rclone.org/install.sh | sudo bash
```

[7zip](https://www.7-zip.org/) - is a file archiver with a high compression ratio.

```bash
sudo apt install p7zip-full
```

## Database backup

To make a MySQL/MariaDB database backup and compress it use command:

```bash
mysqldump -u root --password='database_password' database_name | gzip > /home/user/backup/database_name_db_$(date +\%Y_\%m_\%d).sql.gz
```

Update parameters with your `database password`, `database name` and `location of backup`.

## Website backup

To make website files backup with compression use command:

```bash
/usr/bin/7z a -t7z -mx=3 /home/user/backup/backup_$(date +\%Y-\%m-\%d).7z /var/www/website_files/
```

Also update parameters like [compression ratio](https://sevenzip.osdn.jp/chm/cmdline/switches/method.htm#ZipX) `-mx=3`, `backup location` and `path to website files`.

## Remove old backups

To keep only few latest backup files on server and sync them to the cloud we can remove old backups before syncing them. It can save a lot of space in our cloud server.

```bash
find /home/user/backup/* -mtime +31 -exec rm -f {} \;
```

This command will find and delete files older than 31 days.

## Backup script

It is good to create backup script rather than add above commands to [crontab](https://en.wikipedia.org/wiki/Cron) separately.

So create and edit new script file:

```bash
touch /home/user/backup.sh
nano /home/user/backup.sh
```

add your backup commands:

```bash
#!/bin/sh
# Database backup
mysqldump -u root --password='yourpassword' database_name | gzip > /home/user/backup/database_name_db_$(date +\%Y_\%m_\%d).sql.gz
# Website files backup
/usr/bin/7z a -t7z -mx=3 /home/user/backup/backup_$(date +\%Y-\%m-\%d).7z /var/www/website_files/
# Find and remove backup files older than 31 days
find /home/user/backup/* -mtime +31 -exec rm -f {} \;
# Sync our backuped files with cloud server
rclone sync /home/user/backup/ remote:backup
```

allow script to be executed:

```bash
chmod +x ./backup.sh
```

In this script we will use rclone to sync backup files to remote location.

```bash
rclone sync /home/user/backup/ remote:backup
```

Instead of `sync` you can use `copy` parameter to send and keep all files to cloud.

On the official rclone website you can check how to configure [one of many](https://rclone.org/overview/) remote location like [Google Drive](https://rclone.org/drive/), [Dropbox](https://rclone.org/dropbox/), [Mega](https://rclone.org/mega/), [FTP](https://rclone.org/ftp/), [Amazon](https://rclone.org/amazonclouddrive/), [OneDrive](https://rclone.org/onedrive/) etc.

Just run command:

```bash
sudo rclone config
```

and follow configuration wizard.

Rclone configuration is located in user folder `/home/user/.config/rclone/rclone.conf`. If you will configure rclone as user and run cron as root then you should add path to configuration file as parameter.

```bash
rclone --config /home/user/.config/rclone/rclone.conf copy /home/user/backup/ remote:backup
```

or just configure rclone as root.

It’s important to keep backups in a different location than on a server from which we make copies ;)

### Mysqldump password config

If you don’t want to use database password in script file you can configure username and password in root folder. Create mysqldump config file as root.

```bash
nano ~/.my.cnf
```

and add there your database info:

```bash
[mysqldump]
user = mysqldbusername
password = mysqldbpassword
```

change permission:

```bash
chmod 600 ~/.my.cnf
```

automatically `mysql` and `mysqldump` commands takes the password from this file. Then your backup script can look like this:

```bash
#!/bin/sh
# Database backup
mysqldump database_name | gzip > /home/user/backup/database_name_db_$(date +\%Y_\%m_\%d).sql.gz
# Website files backup
/usr/bin/7z a -t7z -mx=3 /home/user/backup/backup_$(date +\%Y-\%m-\%d).7z /var/www/website_files/
# Find and remove backup files older than 31 days
find /home/user/backup/* -mtime +31 -exec rm -f {} \;
# Sync our backuped files with cloud server
rclone sync /home/user/backup/ remote:backup
```

## Cron

Once your remote location is configured schedule backup script execution using crontab

```bash
sudo crontab -e
```

add line:

```bash
0 0 * * 0 /bin/bash /home/user/backup.sh > /dev/null 2>&1
```

This will execute backup script at 00:00 on Sunday. To adjust your own time you can use [crontab guru](https://crontab.guru/).

`/dev/null` will notify when error occurs

`/dev/null 2>&1` shows nothing

If you want check cron logs use command:

```bash
sudo grep CRON /var/log/syslog
```

That’s all! Backup your stuff and be happy :)
