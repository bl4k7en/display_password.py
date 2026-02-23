# DisplayPassword Plugin

Displays recently cracked WPA passwords on the Pwnagotchi display.

## Authors

- Original: [@vanshksingh](https://github.com/vanshksingh), [@avipars](https://github.com/avipars)
- Modified: [@bl4k7en](https://github.com/bl4k7en)

## Installation

Copy `display_password.py` to `/usr/local/share/pwnagotchi/custom-plugins/`

## Configuration

```toml
[main.plugins.display-password]
enabled = true
orientation = "horizontal"
position_x = 75
position_y = 110
max_ssid_len = 12
show_count = true
count_position_x = 160
count_position_y = 67
```

## Options

| Option | Default | Description |
|---|---|---|
| `enabled` | `false` | Enable/disable the plugin |
| `orientation` | `"horizontal"` | Display orientation: `"horizontal"` or `"vertical"` |
| `position_x` | auto | Custom X position for password line (overrides default) |
| `position_y` | auto | Custom Y position for password line (overrides default) |
| `max_ssid_len` | `12` | Max SSID length before truncation (password is never truncated) |
| `show_count` | `true` | Show total number of cracked passwords |
| `count_position_x` | auto | Custom X position for count line (overrides default) |
| `count_position_y` | auto | Custom Y position for count line (overrides default) |

## How it works

Reads `/home/pi/handshakes/wpa-sec.cracked.potfile` and displays:
- The most recently cracked password: `PASSWORD - SSID`
- Total count of cracked passwords: `Cracked: 299`

Long SSIDs are truncated with `…`, passwords are always shown in full.

Potfile format: `hash1:hash2:SSID:PASSWORD`

## Requirements

- Working `wpa-sec` plugin
- Cracked passwords in potfile

## Default positions

| Display | Horizontal | Vertical |
|---|---|---|
| Waveshare v2/v3/v4 | (0, 95) | (180, 61) |
| Waveshare v1 | (0, 95) | (170, 61) |
| Waveshare 1.44 LCD | (0, 92) | (78, 67) |
| Inky | (0, 83) | (165, 54) |
| Waveshare 2.7" | (0, 153) | (216, 122) |
| Default | (0, 91) | (180, 61) |
