from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import logging
import os


class DisplayPassword(plugins.Plugin):
    __author__ = '@vanshksingh, @avipars, @bl4k7en'
    __version__ = '2.4.0'
    __license__ = 'GPL3'
    __name__ = "DisplayPassword"
    __description__ = 'Displays recently cracked WPA passwords and total count on the Pwnagotchi display.'
    __defaults__ = {
        "enabled": False,
        "orientation": "horizontal",
        "position_x": None,
        "position_y": None,
        "max_ssid_len": 12,
        "show_count": True,
        "count_position_x": None,
        "count_position_y": None,
    }

    def on_loaded(self):
        logging.info("[DisplayPassword] Plugin loaded")

    def _truncate(self, text, max_len):
        if len(text) > max_len:
            return text[:max_len - 1] + '…'
        return text

    def _count_lines(self, potfile):
        try:
            with open(potfile, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for line in f if line.strip())
        except Exception:
            return 0

    def on_ui_setup(self, ui):
        if ui.is_waveshare_v2() or ui.is_waveshare_v3() or ui.is_waveshare_v4():
            h_pos = (0, 95)
            v_pos = (180, 61)
            h_count_pos = (0, 105)
        elif ui.is_waveshare_v1():
            h_pos = (0, 95)
            v_pos = (170, 61)
            h_count_pos = (0, 105)
        elif ui.is_waveshare144lcd():
            h_pos = (0, 92)
            v_pos = (78, 67)
            h_count_pos = (0, 102)
        elif ui.is_inky():
            h_pos = (0, 83)
            v_pos = (165, 54)
            h_count_pos = (0, 93)
        elif ui.is_waveshare27inch():
            h_pos = (0, 153)
            v_pos = (216, 122)
            h_count_pos = (0, 163)
        else:
            h_pos = (0, 91)
            v_pos = (180, 61)
            h_count_pos = (0, 101)

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

        if self.options.get('show_count', True):
            count_x = self.options.get('count_position_x')
            count_y = self.options.get('count_position_y')
            if count_x is not None and count_y is not None:
                count_pos = (count_x, count_y)
            else:
                count_pos = h_count_pos
                logging.info(f"[DisplayPassword] Count position: {count_pos}")

            ui.add_element(
                'display-password-count',
                LabeledValue(
                    color=BLACK,
                    label='',
                    value='',
                    position=count_pos,
                    label_font=fonts.Bold,
                    text_font=fonts.Small
                )
            )

    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('display-password')
            if self.options.get('show_count', True):
                ui.remove_element('display-password-count')
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
                if self.options.get('show_count', True):
                    ui.set('display-password-count', 'Cracked: 0')
                return

            with open(potfile, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            valid_lines = [l for l in lines if l.strip()]

            if not valid_lines:
                ui.set('display-password', 'No passwords yet')
                if self.options.get('show_count', True):
                    ui.set('display-password-count', 'Cracked: 0')
                return

            if self.options.get('show_count', True):
                ui.set('display-password-count', f"Cracked: {len(valid_lines)}")

            last_line = valid_lines[-1].strip()
            parts = last_line.split(':')

            if len(parts) >= 4:
                ssid = self._truncate(parts[2], max_ssid)
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
