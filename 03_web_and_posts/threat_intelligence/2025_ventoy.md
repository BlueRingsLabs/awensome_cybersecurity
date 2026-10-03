[[ PAGE 1 ]]

# One USB Drive with multiple live systems and rescue tools

Everyone in IT has lots of flash drives. Each one has something different on it. But they’re all important and useful. Sometimes only once a year, but still useful. I decided to tidy up my USB drives and put everything in one place. I thought it would be difficult, but it turns out there is a very cool project called [Ventoy](https://www.ventoy.net/), which allows easily build a USB drive with several systems to choose from in the menu.

Personally, I use:

- [Hiren’s BootCD PE](https://www.hirensbootcd.org/) - for fixing Windows stuff
- [SystemRescue](https://www.system-rescue.org/) - in case my Linux laptop crashes when I mess around too much
- [Rescuezilla](https://rescuezilla.com/) - for cloning disks, making copies of systems for later analysis, Rescuezilla is nothing more than Clonezilla with a GUI
- [Kali OS](https://www.kali.org/) - because, well, Kali always comes in handy
- [Parrot OS](https://parrotsec.org/) - as a portable alternative to Kali Linux
- [Tails](https://tails.net/) - as a system when I need to do something on the go when I don’t trust the computer I have available.

I keep Tails on a separate USB stick because I use persistent. I don’t recommend putting Tails on Ventoy. It is possible, but need some tweaks in default Ventoy partitions.

Here are the steps I took to build my flash drive.

## Ventoy USB preparation

64 GB multiboot drive built on Ventoy with persistence and custom theme.

- Parrot OS (Security 6.4) + persistent 5 GB
- Kali OS (2025.3) + persistent 5 GB
- SystemRescue (12.02)
- RescueZilla (2.6.1)
- Hiren’s BootCD PE (v1.0.8)
- [Custom theme](https://github.com/odiegoduarte/ventoy-themes)

### Install Ventoy on the USB

```bash
tar xzf ventoy-1.1.07-linux.tar.gz
cd ventoy-1.1.07
lsblk # find your USB device, e.g. /dev/sda
sudo ./Ventoy2Disk.sh -i /dev/sdX
```

After installation Ventoy creates:

```bash
/dev/sdX1 → VENTOY (≈57 GB, exFAT)
/dev/sdX2 → VTOYEFI (≈32 MB, FAT16)
```

⚠️ All data on the USB will be erased.

### Prepare folder structure

```bash
cd /run/media/$USER/Ventoy/
mkdir -p ISO/Linux ISO/Windows persistence ventoy
```

### Copy ISO files (renamed for consistency)

```bash
cp ~/Downloads/Parrot-security-6.4_amd64.iso ISO/Linux/parrotos.iso
cp ~/Downloads/systemrescue-12.02-amd64.iso ISO/Linux/systemrescue.iso
cp ~/Downloads/rescuezilla-2.6.1-64bit.oracular.iso ISO/Linux/rescuezilla.iso
cp ~/Downloads/HBCD_PE_x64.iso ISO/Windows/hirensbootcdpe.iso
cp ~/Downloads/kali-linux-2025.3-installer-amd64.iso SO/Linux/kali.iso
```

### Create 5 GB persistence for Parrot OS and Kali

```bash
#Parrot
cd /run/media/$USER/Ventoy/persistence/
sudo dd if=/dev/zero of=parrot.dat bs=1M count=5120
sudo mkfs.ext4 -L persistence parrotos.dat
sudo mkdir /mnt/persist
sudo mount -o loop parrotos.dat /mnt/persist
sudo bash -c 'echo "/ union" > /mnt/persist/persistence.conf'
sudo umount /mnt/persist

#Kali
cd /run/media/$USER/Ventoy/persistence/
sudo dd if=/dev/zero of=kali.dat bs=1M count=5120
sudo mkfs.ext4 -L persistence kali.dat
sudo mkdir /mnt/persist
sudo mount -o loop kali.dat /mnt/persist
sudo bash -c 'echo "/ union" > /mnt/persist/persistence.conf'
sudo umount /mnt/persist
```

Persistence files created: `/persistence/parrotos.dat` and `/persistence/kali.dat`

### Setup custom theme

Select and download a custom theme. I chose <https://github.com/odiegoduarte/ventoy-themes/releases/tag/0.7>

Extract the file and place the theme folder in the Ventoy folder.

### Ventoy configuration

Path: `/run/media/$USER/Ventoy/ventoy/ventoy.json`

```bash
{
    "control":[
        { "VTOY_DEFAULT_SEARCH_ROOT": "/ISO" }
    ],
    "theme":{
        "file":[
            "/ventoy/purple-theme/theme.txt",
            "/ventoy/purple-theme/theme_legacy.txt"
        ],
        "default_file": 1,
        "resolution_fit": 1,
        "gfxmode": "max"
    },
    "menu_alias":[
        {
            "image": "/ISO/Linux/systemrescue.iso",
            "alias": "System Rescue"
        },
        {
            "image": "/ISO/Windows/hirensbootcdpe.iso",
            "alias": "Hirens Boot CD"
        },
        {
            "image": "/ISO/Linux/rescuezilla.iso",
            "alias": "Rescuezilla"
        },
        {
            "image": "/ISO/Linux/kali.iso",
            "alias": "Kali Linux"
        },
        {
            "image": "/ISO/Linux/parrotos.iso",
            "alias": "Parrot OS"
        }
    ],
    "persistence":[
        {
            "image": "/ISO/Linux/kali.iso",
            "backend":[
                "/persistence/kali.dat"
            ]
        },
        {
            "image": "/ISO/Linux/parrotos.iso",
            "backend":[
                "/persistence/parrotos.dat"
            ]
        }
    ]
}
```

If you want to use the default theme, simply remove this section from the configuration file.

```bash
"theme":{
    "file":[
        "/ventoy/purple-theme/theme.txt",
        "/ventoy/purple-theme/theme_legacy.txt"
    ],
    "default_file": 1,
    "resolution_fit": 1,
    "gfxmode": "max"
},
```

### Test the USB

```bash
sync && sudo umount /run/media/$USER/Ventoy/
```

Boot from the USB. You should see

![Ventoy](ventoy.webp)

Check Parrot persistence by creating a file in `/home` and rebooting.

### Updating and Maintenance

| Action | Command / Note |
| --- | --- |
| Update Ventoy | `sudo ./Ventoy2Disk.sh -u /dev/sdX` |
| Replace ISO with new version | overwrite file with same name |
| Backup config folder | `cp -a /run/media/$USER/Ventoy/ventoy ~/VentoyBackup_$(date +%F)` |
| Check Ventoy version | `sudo ./Ventoy2Disk.sh -l /dev/sdX` |

Updating Ventoy does not affect your ISOs, persistence, or theme.

### Final layout

```bash
ISO
├── Linux
│   ├── kali.iso
│   ├── parrotos.iso
│   ├── rescuezilla.iso
│   └── systemrescue.iso
├── Windows
|   └── hirensbootcdpe.iso
├── persistence
│   ├── kali.dat
│   └── parrotos.dat
└── ventoy
    ├── purple-theme
    │   ├── 1024x768.png
    │   ├── background.png
    │   ├── menu_c.png
    │   ├── menu_e.png
    │   ├── menu_ne.png
    │   ├── menu_n.png
    │   ├── menu_nw.png
    │   ├── menu_se.png
    │   ├── menu_s.png
    │   ├── menu_sw.png
    │   ├── menu_w.png
    │   ├── select_c.png
    │   ├── slider_c.png
    │   ├── slider_n.png
    │   ├── slider_s.png
    │   ├── terminal_box_c.png
    │   ├── terminal_box_e.png
    │   ├── terminal_box_ne.png
    │   ├── terminal_box_n.png
    │   ├── terminal_box_nw.png
    │   ├── terminal_box_se.png
    │   ├── terminal_box_s.png
    │   ├── terminal_box_sw.png
    │   ├── terminal_box_w.png
    │   ├── theme_legacy.txt
    │   └── theme.txt
    └── ventoy.json
```

## Documentation

For more information and additional configuration options, please refer to the official [Ventoy website](https://www.ventoy.net/) and the documentation.

That’s all. I hope you find it useful and that it helps you recover some free USB sticks.
