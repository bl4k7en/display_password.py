from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import logging
import os


class DisplayPassword(plugins.Plugin):
    __author__ = '@vanshksingh, @avipars, @bl4k7en'
    __version__ = '2.3.0'
    __license__ = 'GPL3'
    __name__ = "DisplayPassword"
    __description__ = 'Displays recently cracked WPA passwords on the Pwnagotchi display. SSID is truncated if too long, password is always shown in full.'
    __defaults__ = {
        "enabled": False,
        "orientation": "horizontal",
        "position_x": None,
        "position_y": None,
        "max_ssid_len": 12,
    }

    def on_loaded(self):
        logging.info("[DisplayPassword] Plugin loaded")

    def _truncate(self, text, max_len):
        if len(text) > max_len:
            return text[:max_len - 1] + '…'
        return text

    def on_ui_setup(self, ui):
        if ui.is_waveshare_v2() or ui.is_waveshare_v3() or ui.is_waveshare_v4():
            h_pos = (0, 95)
            v_pos = (180, 61)
        elif ui.is_waveshare_v1():
            h_pos = (0, 95)
            v_pos = (170, 61)
        elif ui.is_waveshare144lcd():
            h_pos = (0, 92)
            v_pos = (78, 67)
        elif ui.is_inky():
            h_pos = (0, 83)
            v_pos = (165, 54)
        elif ui.is_waveshare27inch():
            h_pos = (0, 153)
            v_pos = (216, 122)
        else:
            h_pos = (0, 91)
            v_pos = (180, 61)

        if self.options.get('orientation') == "vertical":
            position = v_pos
        else:
            position = h_pos

        custom_x = self.options.get('position_x')
        custom_y = self.options.get('position_y')

        if custom_x is not None and custom_y is not None:
            position = (custom_x, custom_y)
            logging.info(f"[DisplayPassword] Using custom position: {position}")

        ui.add_element(
            'display-password',
            LabeledValue(
                color=BLACK,
                label='',
                value='',
                position=position,
                label_font=fonts.Bold,
                text_font=fonts.Small
            )
        )
        logging.info(f"[DisplayPassword] UI element added at {position}")

    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('display-password')
        logging.info("[DisplayPassword] Plugin unloaded")

    def on_ui_update(self, ui):
        potfile = '/home/pi/handshakes/wpa-sec.cracked.potfile'

        max_ssid = self.options.get('max_ssid_len', 12)

        try:
            if not os.path.exists(potfile):
                logging.warning(f"[DisplayPassword] Potfile not found: {potfile}")
                ui.set('display-password', 'No potfile found')
                return

            if os.path.getsize(potfile) == 0:
                logging.debug("[DisplayPassword] Potfile is empty")
                ui.set('display-password', 'No passwords yet')
                return

            with open(potfile, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            if not lines:
                ui.set('display-password', 'No passwords yet')
                return

            last_line = ''
            for line in reversed(lines):
                if line.strip():
                    last_line = line.strip()
                    break

            if not last_line:
                ui.set('display-password', 'No passwords yet')
                return

            parts = last_line.split(':')

            if len(parts) >= 4:
                ssid     = self._truncate(parts[2], max_ssid)
                password = parts[3]
                display_text = f"{password} - {ssid}"
                logging.debug(f"[DisplayPassword] Showing: {display_text}")
            else:
                logging.warning(f"[DisplayPassword] Invalid format: {last_line}")
                display_text = 'Invalid format'

            ui.set('display-password', display_text)

        except PermissionError as e:
            logging.error(f"[DisplayPassword] Permission denied: {e}")
            ui.set('display-password', 'Permission denied')
        except Exception as e:
            logging.error(f"[DisplayPassword] Error: {e}")
            ui.set('display-password', 'Error reading file')
