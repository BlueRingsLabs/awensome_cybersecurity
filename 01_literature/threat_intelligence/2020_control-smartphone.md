[[ PAGE 1 ]]

# Control Smartphone from PC

I like to keep an eye on my smartphone or rather what is happening on it. Not all the time, but when I need it, I use desktop app to not miss any notification, or to transfer files between smartphone and PC. Today with all smart watches and sport bands people are connected with their phones all the time. If you are looking for something that also allow you to control almost all of the smartphone options from your PC, here are some apps for you to check.

![mirroring](mirroring.jpg)

Personally I am using scrcpy. Because, in my opinion it is the best solution for Linux users, this is why there is also short description how to install it and configure. Check other options and choose the best solution for yourself.

## scrcpy

Connection: USB or TCP/IP

Version: Free/Opensource

Supported desktop OS: Windows/Linux/macOS

Supported mobile OS: Android

Download: [scrcpy](https://github.com/Genymobile/scrcpy)

### Installation

Latest zip and source for each system can be downloaded on [release page](https://github.com/Genymobile/scrcpy/releases).

Snap packages: <https://snapcraft.io/scrcpy>.

Manual build from GitHub described [here](https://github.com/Genymobile/scrcpy/blob/master/BUILD.md).

Requirements: The Android part requires at least API 21 (Android 5.0). Make sure you enabled adb debugging on your device(s). Don’t forget to install ADB `sudo apt install adb`.

### Go wireless

1. Connect the device to the same Wi-Fi as your computer
2. Get your device IP address (in Settings → About phone → Status)
3. Enable adb over TCP/IP on your device: `adb tcpip 5555`
4. Connect to your device: `adb connect DEVICE_IP:5555` (replace `DEVICE_IP`)
5. Unplug your device
6. Run scrcpy as usual

The default scrcpy bit-rate is 8Mbps, which is probably too much for a Wi-Fi connection. Depending on the use case, decreasing the bit-rate and the resolution may be a good compromise:

```bash
scrcpy --bit-rate 2M --max-size 800
or
scrcpy -b2M -m800
```

To switch back to USB mode: `adb usb`.

### Resolution

To limit both width and height to some value (e.g. 1024):

```bash
scrcpy --max-size 1024
or
scrcpy -m 1024
```

### Record screen

It is possible to record the screen while mirroring:

```bash
scrcpy --record file.mp4
or
scrcpy -r file.mkv
```

To disable mirroring while recording:

```bash
scrcpy --no-display --record file.mp4
or
scrcpy -Nr file.mkv
```

interrupt recording with Ctrl+C

### Issues

When you run `scrcpy` and get error like this:

```bash
adb: error: failed to get feature set: more than one device/emulator
ERROR: "adb push" returned with value 1
```

check devices:

```bash
adb devices
```

List of devices attached

```bash
YOUR_DEVICE_CODE devices
YOUR_DEVICE_CODE devices
```

you need find YOUR_DEVICE_CODE some string or IP address

```bash
adb disconnect
```

then choose one of these, depending on how you are connecting to your device:

```bash
adb usb
```

for USB or

```bash
adb tcpip 5555
```

for adb over WiFi.

## Dell Mobile Connect

Connection: Bluetooth

Version: Free/Commercial

Supported desktop OS: Windows (only with some Dell devices)

Supported mobile OS: Android/iOS

Download: [Dell Mobile Connect](https://www.dell.com/en-us/shop/dell-mobile-connect/ab/dell-mobile-connect)

## Vysor

Connection: USB/WiFi

Version: Freemium (limited options in free version)

Supported desktop OS: Windows/Linux/macOS/Chrome Plugin

Supported mobile OS: Android

Download: [Vysor](http://www.vysor.io/)

## AirDroid

Connection: USB/WiFi

Version: Freemium (limited options in free version)

Supported desktop OS: Windows/Linux/macOS/Chrome Plugin

Supported mobile OS: Android

Download: [AirDroid](https://www.airdroid.com/)

## AirMore

Connection: WiFi

Version: Free

Supported desktop OS: Web interface

Supported mobile OS: Android/iOS

Download: [AirMore](https://airmore.com/)

## KDEConnect

Connection: WiFi

Version: Free/Opensource

Supported desktop OS: Linux

Supported mobile OS: Android

Download: [KDEConnect](https://community.kde.org/KDEConnect)

## GSConnect

Connection: WiFi

Version: Free/Opensource

Supported desktop OS: Linux/Chrome Extension/Firefox Extension

Supported mobile OS: Android

Download: [GSConnect](https://github.com/andyholmes/gnome-shell-extension-gsconnect/wiki)

## Join

Connection: WiFi

Version: Commercial

Supported desktop OS: Windows 10/Chrome Extension

Supported mobile OS: Android

Download: [Join](https://joaoapps.com/join/)

## Pushbullet

Connection: WiFi

Version: Commercial

Supported desktop OS: Windows/Chrome Extension/Firefox Extension

Supported mobile OS: Android

Download: [Pushbullet](https://www.pushbullet.com/)

## Mightytext

Connection: WiFi

Version: Commercial

Supported desktop OS: Windows/iOS/Chrome Extension

Supported mobile OS: Android

Download: [Mightytext](https://mightytext.net/)

## Mobizen

Connection: USB/WiFi

Version: Freemium

Supported desktop OS: Windows/Web interface

Supported mobile OS: Android

Download: [Mobizen](https://www.mobizen.com/)
