DisplayPassword Plugin


Description

Displays recently cracked WPA passwords on the Pwnagotchi display.


Authors

Original: @vanshksingh, @avipars

Modified: bl4k7en


Installation

Copy display_password.py to /usr/local/share/pwnagotchi/custom-plugins/
Configuration
```
main.plugins.display_password.enabled = true
main.plugins.display_password.orientation = "horizontal"
main.plugins.display_password.position_x = 10
main.plugins.display_password.position_y = 100
```


Options

enabled - Enable/disable plugin (default: false)

orientation - Display orientation: "horizontal" or "vertical" (default: "horizontal")

position_x - Custom X position (optional, overrides default)

position_y - Custom Y position (optional, overrides default)



How it works

Reads /home/pi/handshakes/wpa-sec.cracked.potfile and displays the most recent cracked password in format: PASSWORD - SSID

Potfile format: hash1:hash2:SSID:PASSWORD

Requirements

Working wpa-sec plugin

Cracked passwords in potfile


Default positions

Plugin automatically adjusts position based on display type:


Waveshare v2/v3/v4: (0, 95) horizontal / (180, 61) vertical
Waveshare v1: (0, 95) horizontal / (170, 61) vertical
Waveshare 1.44 LCD: (0, 92) horizontal / (78, 67) vertical
Inky: (0, 83) horizontal / (165, 54) vertical
Waveshare 2.7": (0, 153) horizontal / (216, 122) vertical
Default: (0, 91) horizontal / (180, 61) vertical
