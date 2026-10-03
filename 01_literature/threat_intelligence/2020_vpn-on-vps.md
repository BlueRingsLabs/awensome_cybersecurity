[[ PAGE 1 ]]

# Quick VPN setup on VPS

In my article about [VPN](https://0ut3r.space/2019/10/13/vpn/) I provide some information why you should use VPN, and I also suggested some free and paid solutions.

There is one more option to have a free (ohh ok, almost free, but really cheap) personal VPN server. You can buy cheap VPS server and setup there a VPN server. You can check my small guide how to [setup secure VPS server](https://0ut3r.space/2020/04/13/first-vps/). Now using steps in this article you can setup secure, personal VPN server.  
The only cons of this solution compared to commercial is that you will have only one location (geolocation), and this location is the same where your VPN is localized. Anyway, this is always good solution for securing your connection when you are in places, with network connection you do not trust, or if you do not trust VPN providers. It is also a chance to setup something new on your VPS, if you have one and it is not used. In addition, you can be sure that if you turn off logs, it will definitely be a VPN without logs :)

![vpn on vps](vpnonvps.jpg)

Totally manual setup of VPN for newbies can be something hard, even for advanced users it can be something demanding. Fortunately, there are several automated solutions that can easily help us configure VPNs while maintaining the appropriate level of security.

Automated script you can use:  
<https://github.com/trailofbits/algo>  
<https://github.com/StreisandEffect/streisand>  
<https://github.com/angristan/openvpn-install>  
<https://github.com/Nyr/openvpn-install>

Choose the one that best fits your needs.

Personally I am using solution provide by [angristan](https://angristan.xyz/) and it works very well. Using his script I will show you how to configure VPN.

## OpenVPN Install

First download it:

```bash
curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-	install.sh
```

and make it executable

```bash
chmod +x openvpn-install.sh
```

then run it and follow the steps on the screen, you need to run the script as root and have the TUN module enabled (TUN module can be disabled/enabled in your VPS dashboard):

```bash
sudo ./openvpn-install.sh
```

All default options are suggested to keep for best performance and security. So if you do not know what to choose, leave it as it is. If you are expert you will know what to change.

Once all is installed and configured you will be asked about new client you want to add. You can create as many, as you want for each device or user.

To run configuration, for the next user, just run script again. It only install all necessary stuff at the first lunch, after that scripts is just an text menu to add and remove users.

After all don’t forget to open port you chose during the configuration on the firewall, to allow VPN connection.

Yes, it was so easy. In these few steps you have configured your own VNP server. Now just download generated Open VPN configuration file and import it to your desktop, laptop and mobile phone device.

## Disable logs

If you would like to disable VPN logs, edit server configuration:

```bash
sudo nano /etc/openvpn/server.conf
```

and change line `verb 3` to `verb 0`. 0 mean no output except fatal errors. This line should be last line in your server configuration. Then line `status /var/log/openvpn/status.log` to `status /dev/null` and next to status line add `log /dev/null`.

With all these options it is harder to find the issues with VPN, but if you configured and tested everything already and don’t need logs anymore it is ok to make this changes.

That’s all folks.
