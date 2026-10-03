[[ PAGE 1 ]]

# Mount Synology NAS in Linux

From some time I am happy user of [Synology DiskStation DS218j](https://www.synology.com/pl-pl/products/DS218j). I recommend it to all who would like to cut themselves off from the cloud solutions of popular suppliers like Dropbox, Google Drive or Onedrive.

By setting up your private NAS, you have full control over your data, you gain access to your data from each device and additional features such as VPN, web server, backup of your devices, calendar, office package, group work, chat, audio server, video server and many other functions which description can be found on the manufacturer’s website. A one-off expense at the beginning may seem quite large, however, it returns from the first day of use. Personally, I use the Synology solution but there are more companies on the market that produce this type of equipment for home and professional use. If you are interested in such a solution, look for something that will meet all your requirements.

![DiskStation Manager](synology.jpg)

Mounting and mapping shared resources from a NAS server in Windows should not cause major problems. In the Linux system it requires a bit more knowledge but it is possible and with the description below it will become trivial for every intermediate Linux user.

You can mount shares in two ways via [SMB/CIFS](https://reycdxyc24gf7jrnwutzdn3smmweizedy7uojsa7ols6sflwu25ijoyd.onion/2019/07/23/mount-nas/SMB/CIFS) and [NFS](https://en.wikipedia.org/wiki/Network_File_System). Both solutions are good and fast. It seems to me that the first way is less complicated and requires less configuration. Additionally, it works in any environment with variable configuration of computer IP addresses.

## SMB/CIFS

### NAS configuration

Log in to your *Synology Disk Station Manager* and go to *Control Panel*. Choose *File Services* in tab *SMB/AFP/NFS* and select *SMB* service. Provide name of your *Workgroup*. Remember name of field *Mac (Finder): smb://nas_name*. In *Advanced Settings* you can choose maximum and minimum SMB protocol (if are not sure what to select choose maximum version to *SMB3* and minimum to *SMB2* - Do NOT use SMBv1. SMB1 lacks encryption, is inefficient, and has been exploited in the wild by ransomware attacks). Additionally switch *Transport Encryption Mode* to *Auto* and select *Enable Opportunistic Locking*. Now you are ready to mount folders on Linux.

### System configuration

Edit *hosts* file:

```bash
sudo nano /etc/hosts
```

and add line with IP and name of your NAS.

```bash
xx.xx.xx.xx nas_name
```

Create folders:

```bash
mkdir /media/nas
mkdir /media/nas/test_folder
```

Create file with NAS credentials in your home directory:

```bash
nano .smbcredentials
```

add your NAS credentials:

```bash
username=nas_username
password=nas_password
```

change permission for this file:

```bash
chmod 0600 ~/.smbcredentials
```

Install *cifs-utils*:

```bash
sudo apt install cifs-utils
```

Edit *fstab* and add line (this will allow to map your folders automatically on system boot):

```bash
//nas_name/test_folder /media/nas/test_folder cifs credentials=/home/username/.smbcredentials,vers=3.0,uid=1000,gid=1000 0 0
```

in line above replace values to yours (*nas_name*, *test_folder*, path to *smbcredentials* file. To check your user `uid` and `gid` just type `id -u username`.

Now map folders using command:

```bash
sudo mount -a
```

Do it for all your folders you want to map from NAS and check results in your file explorer.

If you have some permission issues, you might also consider allowing all users to mount network shares.

```bash
//nas_name/test_folder /media/nas/test_folder cifs credentials=/home/username/.smbcredentials,vers=3.0,noauto,user 0 0
```

`user` - add user group, so all users in user group will be able to mount drives.

`noauto` - is something I use to not mount drives by default at startup, they will be mounted when I click on share link.

## NFS

### NAS configuration

Log in to your *Synology Disk Station Manager* and go to *Control Panel*. Choose *File Services* in tab *SMB/AFP/NFS* and select *NFS* service. Now in *Control Panel* got to *Shared Folder*. Choose folder you want to mount and hit *Edit* button, go to *NFS Permissions* tab. Hit *Create* button and set fields like this:  
Provide *IP* of your PC.  
*Privilege* set to *Read/Write*.  
*Squash* to *Map root to Admin*  
*Security* to *sys*  
and *Enable Asynchronous* option. Hit *OK*.

Remember the *Mount path* on *NSF Permissions* tab. This info is located at the bottom and looks like: *Mount path:/volume1/test_folder*

Do the same for all folders you want to mount on Linux machine.

### System configuration

Edit *hosts* file:

```bash
sudo nano /etc/hosts
```

and add line with IP and name of your NAS.

```bash
xx.xx.xx.xx nas_name
```

Create folders:

```bash
mkdir /media/nas
mkdir /media/nas/test_folder
```

Install *nfs-common*:

```bash
sudo apt install nfs-common
```

Edit *fstab* and add line (this will allow to map your folders automatically on system boot):

```bash
nas_name:/volume1/test_folder /media/nas/test_folder nfs rsize=8192,wsize=8192,timeo=14,intr
```

in line above replace values to yours (*nas_name*, *test_folder*).

Now map folders using command:

```bash
sudo mount -a
```

Do it for all your folders you want to map from NAS and check results in your file explorer.
