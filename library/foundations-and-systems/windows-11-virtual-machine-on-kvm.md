---
id: ckb-e9d841c9b454
title: Windows 11 virtual machine on KVM
category: foundations-and-systems
format: guide
language: en
tags: [homelab, linux, windows]
summary: A technical guide on setting up a Windows 11 virtual machine using VirtManager and KVM on a Linux host.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-26b-a4b-it
  confidence: 0.95
classified_by: google:gemma-4-26b-a4b-it@2026-10-08T00:24:29Z
---

# Windows 11 virtual machine on KVM

I have switched back to Linux as my daily operating system. For virtualisation I have always used [Virtual Box](https://www.virtualbox.org/) and still do, but I have always wanted to try [VirtManager](https://virt-manager.org/). In the past, I was put off by the number of configurations, and there was always something not working for me. I thought ok, I’ll give it a try and see what has changed after so many years. Here are my steps for setting up a Windows 11 virtual machine using VirtManager. If you have any comments or suggestions I would love to hear them and refine my instructions to make them even better. It is my instruction to myself not to start everything from the scratch in the future on how to install virt-manager with KVM and set up a virtual machine with Windows 11. Maybe someone will find it useful. Such a solution is better than dual-booting, and sometimes you need the whole system and not just, for example, an application emulated with [Wine](https://www.winehq.org/). Of course, there is also better performance.

Tired of AI-generated article headline illustrations? Me too, so here’s another one for you.

![windows11-virtualization](windows11-virtualization.webp)

## Preparation

First install all the necessary stuff. I am using an [Ubuntu](https://ubuntu.com/download) based distribution (more specifically [Tuxedo](https://www.tuxedocomputers.com/en/TUXEDO-OS_1.tuxedo), just because I bought one of their laptops) so your commands and packages may depend on your Linux distribution, but the overall configuration will be the same.

Instalation on Debian:

```bash
sudo apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils libguestfs-tools genisoimage virtinst libosinfo-bin virt-manager dnsmasq-base safe-rm
```

Instalation on Fedora:

```bash
sudo dnf install @virtualization
or
sudo dnf group install --with-optional virtualization
```

Add your user to the appropriate groups (for the Fedora only first one, on Debian all three commands):

```bash
sudo adduser "$(whoami)" libvirt
sudo adduser "$(whoami)" libvirt-qemu
sudo adduser "$(whoami)" kvm
```

Enable the modular **libvirt** daemon:

```bash
sudo systemctl enable libvirtd.service
```

[Download ISO of Windows 11](https://www.microsoft.com/en-us/software-download/windows11) and prepare your product key (or install a trial system for testing). Also download **virto-win** ISO. The latest version can be found [here](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/). **VirtIO** is a virtualisation standard for network and disk device drivers. They allow direct (paravirtualised) access to devices and peripherals for virtual machines using them, instead of slower, emulated, ones. If you are familiar with **Virtual Box** think of it as [Virtual Guest Additions](https://www.virtualbox.org/manual/ch04.html). The last thing you need to have is a link for [spice-guest-tools](https://www.spice-space.org/download.html). Do not download yet, save it for later.

Reboot your system. After the reboot, validate the host setup:

```bash
sudo virt-host-validate qemu
```

The output for this command should show each step as **PASS**, you can ignore “*QEMU: Checking for secure guest support : WARN (Unknown if this platform has Secure Guest support”*), but look out for ERRORS and Google how to fix them if there are any.

To summarise, you have now installed **virt-manager** and all the additional packages needed to run virtualisation (read about each package to make sure you understand what they are for). You have added your user to the correct groups to have the correct permissions, and you have downloaded the **Windows 11** installation image, **virtIO** drivers to proper handle the Windows 11 installation and the **spice guest tools** contain some optional drivers and services that can be installed in the Windows guest to improve **SPICE** performance and integration. These include the qxl video driver and the **SPICE guest agent** (for copy and paste, automatic resolution switching, etc). In the last step you have enabled **libvrt** service. You are now ready to create your Windows 11 virtual machine.

Oh, and most importantly, check that your hardware supports virtualisation, you can check this using the command:

```bash
lscpu | grep Virtualization
```

if the output is VT-x or AMD-V, you are good to go. Otherwise virtualisation is not enabled in the BIOS or your hardware does not support it.

## Configure Windows 11 Virtual Hardware

I will not add a screenshot for everything, this is not a “*VirtManager for dummies*“ tutorial. I bet, if you are here, you know a little bit about Linux and how applications work, so I will only add screenshots in a few places.

Launch the Virtual Machine Manager application. In Settings, enable XML editing: **Edit** > **Preferences** -> **Enable XML editing**.

![enablexmlediting](enablexmlediting.webp)

Next, create a new virtual machine: **File** -> **New Virtual Machine**. This will show you a nice wizard that will guide you through all the steps.

The first step is to select the installation media, so select **Local install media (ISO image or CDROM)**. In the second step browse for the Windows 11 ISO image. The operating system should be detected automatically, if not, select **Microsoft Windows 11**. In the third step allocate memory and CPU. I recommend at least 6 GB of RAM and 2 CPUs. The fourth step is to create a hard drive storage. The storage image that is created will be of the type qcow2. Choose whatever size you want, just remember that Windows 11 is large after installation so 20 GB may not be enough, start with 60 GB. The initial qcow2’s file size will be smaller, and it will only grow as more data is added. The last fifth step of the wizard is the name for your machine and a summary of the previous choices. Don’t forget to select **Customise configuration before install**. This is important because when you **finish** button you will want to make additional changes, before installation.

Once you have pressed the Finish button, you will see a new window with additional setup options. In the Overview section select the chipset as **Q35** and the firmware as **UEFI**. While you are still in the **Overview** section, change from the **Details** tab to **XML**.

![xmledit](xmledit.webp)

Find the hyperview part and replace it with:

```bash
<hyperv mode="custom">
  <relaxed state="on"/>
  <vapic state="on"/>
  <spinlocks state="on" retries="8191"/>
  <vpindex state="on"/>
  <runtime state="on"/>
  <synic state="on"/>
  <stimer state="on">
    <direct state="on"/>
  </stimer>
  <reset state="on"/>
  <vendor_id state="on" value="KVM Hv"/>
  <frequencies state="on"/>
  <reenlightenment state="on"/>
  <tlbflush state="on"/>
  <ipi state="on"/>
  <evmcs state="on"/>
</hyperv>
```

If you have an AMD processor remove `<evmcs state="on"/>`. It only works for Intel.

In the part for `<clock offset="localtime">` add one line just before `</clock>`

```bash
<timer name="hypervclock" present="yes"/>
```

These changes improve the performance of the Windows 11 virtual machine. You can take my word for it, or explore the details with [Uncle Google](https://www.google.com/) or Auntie [ChatGPT](https://chatgpt.com/). If you care about privacy you might want to use [Brave Search](https://search.brave.com/). They are getting better every day.

Return to the configuration. Go back to the **Details** tab and go to CPUs. Select **Copy host CPU configuration (host-passthrough)**. Next section is **SATA Disk 1**, here **Disk bus** should be **VirtIO** and in Advanced options **Cache mode: none** and **Discard mode: unmap**. (If you set the discard mode to unmap, the qcow2 disk image will automatically shrink to reflect the newly freed space.) After making some changes always press **Apply** before proceeding to the next section.

The default installation of Windows 11 does not recognise the SATA disc when it is set up for Disk Bus VirtIO. So we downloaded the VirtIO-Win ISO file. In the left corner of the window there is a button called **Add Hardware**. Press it and add **Storage** as a new virtual hardware. In the **Details** tab select **Custom Storage** and enter a path to **virtio-win.iso**, as **Device type** select **CDROM device**. Click **Finish**. Now we have an additional CDROM drive with a mounted ISO image with drivers.

![cdrom](cdrom.webp)

Go to the **NIC** section to configure the network. Select **Device model** as the **virtio**.

Remove the **Tablet** device. This can reduce idle CPU usage and context switches.

Add hardware again, and select, **Channel** with **Name: org.qemu.guest_agent.0**. This will create a private communication channel between the physical host machine and the guest virtual machine. This allows the host machine to issue commands to the guest operating system using libvirt. The guest operating system then responds to these commands asynchronously.

Next go to the **TPM** section and select **Type: Emulated**, and in the advanced options **Model: CRB** and **Version 2.0**. Do not forget to press the **Apply** button.

We are now ready to install. Click **Begin installation** at the top of the window.

## Windows 11 virtual machine on KVM installation

The steps to install Windows 11 are the same as for the standard installation on the physical laptop or desktop hardware, just follow the installation wizard. Choose your language, keyboard etc., then enter your product key, select the correct Windows version, and choose the **Custom: Install Windows only (advanced) option**.

![windows11custom](windows11custom.webp)

When you get to the point where you need to select the disc where Windows will be installed, you will find an empty list because Windows does not have drivers for VirtIO storage. You will need to install the drivers manually.

Select **Load driver**, then **Browse**, expand the **CD Drive (E:)**, expand **Viostor**, expand **w11**, select **amd64**, and click **OK**. Then click **Next**. This will load the drivers and the installer will recognise the disc. But do not press the Next button yet. We need to load and install the VirtIO network drivers. Repeat the process for the network device as well. Click on **Load driver**, then **Browse**, expand the **CD Drive (E:)**, expand **NetKVM**, expand **w11**, select **amd64**, and click **OK**. Continue with the Windows installation.

Once you have completed the installation and initial configuration steps and everything has gone according to plan, you will see the Windows 11 desktop. Open Windows Explorer and navigate to the mounted image on the **E drive**, locate the **virtio-win-guest-tools** package and install it.

Finally download and install [spice-guest-tools](https://www.spice-space.org/download.html) on the Windows 11 virtual machine. After installing the spice -guest-tools, go to the Windows 11 window, click **View** -> **Scale Display**, and check the ‘**Auto resize VM with window**‘ option. This will enable the Windows 11 guest window to automatically resize when you scale it. Don’t forget to reboot the system after each agent installation.

The installation is complete. To clean up stuff you can check machine configuration and unmount the virtio ISO image from **SATA CDROM 2** and remove **CDROM** as well. In **SATA CDROM 1** you can unmount the Windows 11 iso image, and keep this CDROM for other images you may want to mount in the future.

## Enable Core Isolation

If you wish you can also enable Core Isolation in **Settings** > **Privacy & Security** > **Windows Security** > **Device Security** > **Core isolation details**.

To do this you need to go to the **virtual hardware details** page, then click the **Overview** option in the left pane and the **XML** tab in the right. Under the **<cpu>** section, specify the CPU mode and add the policy flag.

```bash
<cpu mode="host-passthrough" check="none" migratable="on">
  <feature policy="require" name="vmx"/>
</cpu>
```

Restart the VM and enable Core Isolation.

## Optimize Windows 11 Performance

- **Disable SuperFetch** - run **services** and look for **SysMain**. Right click for Properties and disable the service.
- Disable Windows Web Search - run **regedit** go to `Computer\HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows` Right click on the **Windows** key, select **New**, and then select the **Key** option. Enter **Explorer** as the key name and press [Enter]. Right click on the newly created **Explorer** key, select **New**, and then select the **DWORD (32-bit) Value** option. Name the DWORD **DisableSearchBoxSuggestions** and press [Enter]. Double-click the newly created DWORD **DisableSearchBoxSuggestions** and change its value from **0** to **1**. Restart the virtual machine.
- **Disable useplatformclock** - run **CMD** as admin and execute the following command: `bcdedit /set useplatformclock No`
- **Adjust the Visual Effects** - type **performance** in the Search box, then select **Adjust the appearance and performance of Windows** from the list of results. On the **Visual Effects** tab, select **Adjust for best performance** > **Apply**.

## Other useful stuff

Here are some additional commands and tips for working with Virt-Manager.

### Convert vdi to qcow2

I have done this a few times, and sometimes machines wake up and sometimes they are dead :) If you have your **VirtualBox** machine disk image in **vdi** format you can convert it to **qcow2**, setup the machine with that drive and run it (if it’s up, install all the drivers, and uninstall VirtualBox guest additions).

```bash
TMPDIR=/home/user/Download/temp virt-sparsify /home/user/VMs/Windows11/Win11.vdi --convert qcow2 /home/user/Downloads/Win11.qcow2
```

### Shared folder

In the machine sesttings in the Virt-Manager go to the **Memory** section and select **Enable shared memory**. Then go to **Add Hardware**, choose **filesystem** and set **Driver** to **virtiofs**, select **Source path** to the folder you want to share and in **Target path** select the name of the folder that will be displayed in the file explorer on the guest machine. Download and install [WinFPS](https://github.com/winfsp/winfsp/releases/) on the Windows 11 guest machine (only the **Core** option should be selected in the installer). In Windows 11, run **Services** and search for **VirtIO-FS Service**. Start it. Also to enable it on every boot go to **VirtIO-Sevice-FS** > **Properties** > **Startup type** and change from **Manual** to **Automatic**. After starting the service, open explorer and you will see a new drive mounted, if you open it, it will be the shared folder of your physical machine.

### Extend drive size

If your virtual drive gets too small, you can expand it. Before you resize the drive, delete your snapshots. To get a list of snapshots, use the command:

```bash
virsh snapshot-list Windows11
```

To delete a snapshot:

```bash
virsh snapshot-delete --domain Windows11 --snapshotname mysnapshot
```

First, check your drive and verify its size and information:

```bash
qemu-img info /var/lib/libvirt/images/Windows11.qcow2
```

Then resize it, for example by 20 GB

```bash
qemu-img resize  /var/lib/libvirt/images/Windows11.qcow2 +20G
```

check the info again and you will see that it is now resized.

### Dynamic drive

If your drive was not created as dynamic, you can convert it:

```bash
qemu-img convert -f qcow2 -O qcow2 -o preallocation=off disk1.qcow2 newdisc1.qcow2
```

- the -f format flag specifies the format of the input disk
- the -O format flag specifies the format of the output disk
- the -o flag is used to specify some options for the output file, such as the way data is allocated (in this case, no data pre-allocation)

Rename `disc1.qcow2` to `disc1.qcow2.bak` just to back it up. Do not delete it until you are sure that `newdisc1.qcow2` is working as expected. Rename `newdisk1.qcow2` to `disc1.qcow2` when you are finished, using command `sudo mv newdisc1.qcow2 disc1.qcow2`

If you want to create a dynamic virtual disk from scratch, you can run this command:

```bash
qemu-img create -f qcow2 -o preallocation=off <disk-name> <disk-size>
```

where `disk-name` is the name of the dynamic virtual disk and `disk-size` is the maximum size of the disk (you can use k, M, G, T, P or E as suffixes)

### Recover free space

First make sure you have **libguestfs-tools** installed, then run the command

```bash
virt-sparsify in_disk out_disk
```

which copies `in_disk` to `out_disk, making the output sparse. The format of the input disk is detected (e.g. qcow2) and the same format is used for the output disk. Virt-sparsify tries to zero out and sparsify free space on every file system it can find in the source disk image.

If you get error like: `There may not be enough free space on /tmp.`

Just do it in other temp location like: `sudo TMPDIR=/var/tmp virt-sparsify in_disk out_disk`

You can get it to ignore (not zero free space on) certain file systems by doing the following:

```bash
virt-sparsify --ignore /dev/sda1 in_disk out_disk
```

Since [virt-sparsify ≥ 1.26](https://libguestfs.org/virt-sparsify.1.html), you can now sparsify a disk image in place by doing:

```bash
virt-sparsify --in-place in_disc
```

Manual version to do the same is to backup disk file `cp image.qcow2 image.qcow2_backup` zero out disk on quest `sudo dd if=/dev/zero of=/mytempfile && sudo rm -f /mytempfile`then shrink disk without compression (better performance, larger disk size): `qemu-img convert -O qcow2 image.qcow2_backup image.qcow2` or shrink disk with compression (smaller disk size, takes longer to shrink, performance impact on slower systems): `qemu-img convert -O qcow2 -c image.qcow2_backup image.qcow2` then delete the backup when everything works fine.

### NAT forwarding

It is a complex subject and it is better to follow the official documentation:

<https://wiki.libvirt.org/Networking.html#Forwarding_Incoming_Connections>

## References

I did not invent everything in this article, I am not that smart. I just took everything from the Internet and put it together for my needs. Here are some of the sources I used for my guide. These sources have a lot of screenshots and YouTube videos, so they are more user-friendly for people who likes pictures and moving images.

- [How to Properly Install a Windows 11 Virtual Machine on KVM](https://sysguides.com/install-a-windows-11-virtual-machine-on-kvm)
- [How Do I Properly Install KVM on Linux](https://sysguides.com/install-kvm-on-linux)
- [Share Folder Between Windows Guest and Linux Host in KVM using virtiofs](https://www.debugpoint.com/kvm-share-folder-windows-guest/)
- [Setup A Shared Folder Between KVM Host And Guest](https://ostechnix.com/setup-a-shared-folder-between-kvm-host-and-guest/)
- [NAT forwarding - Libvirt WIki](https://wiki.libvirt.org/Networking.html#Forwarding_Incoming_Connections)

Thanks for reading, and please do not join my Discord server, as nothing happens there except people joining to say hello or complain that the server is dead. However, if you have any comments on the article, please drop by there and give your feedback. You can also find me on the official 0ut3r.space Matrix channel or on the Mastodon. You will have to find the links yourself, they are somewhere on the website.

Amen.
