[[ PAGE 1 ]]

# Auto resize X screen for Kali on KVM

Some time ago I started migrating my virtual machines from Virtual Box to Virt-Manager. Mainly because of performance, the fact that sometimes things don’t work in Virtual Box as I would like them to, and of course KVM is harder to configure so I’m going to be a real pro h4ck3r and advanced user (ehh…). As is always the case in the world of everyday Linux use something always doesn’t work :) And what better thing to do on the second day of Christmas than to waste your life configuring your computer, programs and swearing that when something seems to work, it doesn’t.

![Linux Christmas](linux-christmas.webp)

I am currently on Fedora 41 after many years of sitting only on Debian and Ubuntu (but that’s a story for another article). I’ve already migrated my Windows 11, which you can read about in the article [Windows 11 virtual machine on KVM](https://reycdxyc24gf7jrnwutzdn3smmweizedy7uojsa7ols6sflwu25ijoyd.onion/2024/10/26/windows11-kvm). It works beautifully and I don’t have to play around with dual boot thanks to this.

I recently migrated my hacking machine my Kali Linux which I call Bounty Hunter.

Kali uses the XFCE desktop environment, which does not adapt the screen size to the virtual machine window. I think only Gnome and maybe KDE do this by default.

I modified a [solution found on the internet](https://logos-red.com/blog/how-to-fix-kali-linux-qemu-resize-issue/) and adapted it to myself.

```bash
#!/bin/bash
# Bash required
# Should be run as root and saved to /usr/local/bin/x-resize
# Requies udev rule: /etc/udev/rules.d/50-x-resize.rules
# udev rule content: ACTION=="change",KERNEL=="card0", SUBSYSTEM=="drm", RUN+="/usr/local/bin/x-resize" 
# Make sure auto-resize is enabled in virt-viewer/spicy
# Credit for Finding Sessions as Root: https://unix.stackexchange.com/questions/117083/how-to-get-the-list-of-all-active-x-sessions-and-owners-of-them
# Credit for Resizing via udev: https://superuser.com/questions/1183834/no-auto-resize-with-spice-and-virt-manager
## Ensure Log Directory Exists
LOG_DIR=/var/log/autores;
if [ ! -d $LOG_DIR ]; then
    mkdir $LOG_DIR;
fi
LOG_FILE=${LOG_DIR}/autores.log
## Function to find User Sessions & Resize their display
function x_resize() {
    declare -A disps usrs
    usrs=()
    disps=()                                                                                                                                                 
    for i in $(users);do                                                                                                                                     
        [[ $i = root ]] && continue # skip root                                                                                                              
        usrs[$i]=1                                                                                                                                           
    done                                                                                                                                                     
    for u in "${!usrs[@]}"; do                                                                                                                               
        for i in $(sudo ps e -u "$u" | sed -rn 's/.* DISPLAY=(:[0-9]*).*/\1/p');do                                                                           
            disps[$i]=$u                                                                                                                                     
        done                                                                                                                                                 
    done                                                                                                                                                     
    for d in "${!disps[@]}";do                                                                                                                               
            session_user="${disps[$d]}"                                                                                                                      
            session_display="$d"                                                                                                                             
            session_output=$(sudo -u "$session_user" PATH=/usr/bin DISPLAY="$session_display" xrandr | awk '/ connected/{print $1; exit; }')                 
            echo "Session User: $session_user" | tee -a $LOG_FILE;                                                                                           
            echo "Session Display: $session_display" | tee -a $LOG_FILE;                                                                                     
            echo "Session Output: $session_output" | tee -a $LOG_FILE;
            sudo -u "$session_user" PATH=/usr/bin DISPLAY="$session_display" xrandr --output "$session_output" --auto | tee -a $LOG_FILE;
    done
}
echo "Resize Event: $(date)" | tee -a $LOG_FILE
x_resize 
```

It worked until I updated Kali yesterday. I don’t know if it was the new XFCE version 4.20 or Kali itself that changed something so that my solution no longer worked. I don’t want to have to manually enter `xrandr --output Virtual-0 --auto` every time to make the screen change, and I’ve started digging around to make it change automatically.

After several hours of browsing the internet, configuring, listening to jazz, crying, swearing and conferring with GPT chat, success was achieved. The Kali window in KVM scales and I can get back hacking. That is, to get up from the computer for 10 minutes after hours of configuration to sit down to it for another hour and scan the network for vulnerabilities and low hanging fruits. [FML](fml.webp).

The final solution looks like this, I have two files.

First: `x-resize`

```bash
sudo nano /usr/local/bin/x-resize

#!/bin/bash
# Script to listen for RANDR events and automatically adjust the resolution

function x_resize() {
    declare -A disps usrs
    usrs=()
    disps=()

    # Get active users from the 'w' command, skipping 'root'
    for i in $(w -h | awk '{print $1}' | sort | uniq); do
        [[ $i = root ]] && continue  # Skip the root user
        usrs[$i]=1
        echo "Found user: $i"
    done

    # Iterate through users to find active X sessions
    for u in "${!usrs[@]}"; do
        # Check environment variables and X processes
        session_display=$(sudo -u "$u" printenv DISPLAY 2>/dev/null)
        if [[ -n "$session_display" ]]; then
            disps[$session_display]=$u
        fi
    done

    # Listen for resolution changes
    xev -root -event randr | \
    grep --line-buffered 'subtype XRROutputChangeNotifyEvent' | \
    while read foo ; do
        for d in "${!disps[@]}"; do
            session_user="${disps[$d]}"
            session_display="$d"
            session_output=$(sudo -u "$session_user" PATH=/usr/bin DISPLAY="$session_display" xrandr | awk '/ connected/{print $1; exit; }')
            echo "Session User: $session_user"
            echo "Session Display: $session_display"
            echo "Session Output: $session_output"
            sudo -u "$session_user" PATH=/usr/bin DISPLAY="$session_display" xrandr --output "$session_output" --auto
        done
    done
}

# Run the function
x_resize
```

and second `x-resize.service`

```bash
sudo nano /etc/systemd/system/x-resize.service

[Unit]
Description=Auto resize X screen on resolution change
After=lightdm.service
Requires=lightdm.service

[Service]
ExecStart=$SCRIPT_FILE
ExecStartPre=/bin/sleep 5
User=$CURRENT_USER
Environment=DISPLAY=:0
Environment=XAUTHORITY=$USER_HOME/.Xauthority
Type=simple
Restart=always

[Install]
WantedBy=graphical.target
```

after that, all you have to do is give the authority to execute:

```bash
chmod +x /usr/local/bin/x-resize
```

then add and start the service

```bash
systemctl daemon-reload
systemctl enable x-resize.service
systemctl start x-resize.service
```

and done!

I have also created a simple installer for this solution. So if one of life’s problems you have is similar to mine, you can simply use this [GitHub - h0ek/x-resize: Auto-resize X screen on resolution change.](https://github.com/h0ek/x-resize)

Well. Regardless of when you read this. Merry Christmas.
