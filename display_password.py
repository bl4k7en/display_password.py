# display-password shows recently cracked passwords on the pwnagotchi display 
#
###############################################################

from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import logging
import os


class DisplayPassword(plugins.Plugin):
    __author__ = '@vanshksingh, @avipars, bl4k7en'
    __version__ = '2.1.0'
    __license__ = 'GPL3'
    __name__ = "DisplayPassword"
    __description__ = 'A plugin to display recently cracked passwords'
    __defaults__ = {
        "enabled": False,
        "orientation": "horizontal",
        "position_x": None,
        "position_y": None
    }
    
    def on_loaded(self):
        logging.info("[DisplayPassword] Plugin loaded")
    
    def on_ui_setup(self, ui):
        # Display positions (defaults)
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
        
        # Select position based on orientation
        if self.options.get('orientation') == "vertical":
            position = v_pos
        else:
            position = h_pos
        
        # Override with custom position if provided
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
        
        try:
            # Check if file exists
            if not os.path.exists(potfile):
                logging.warning(f"[DisplayPassword] Potfile not found: {potfile}")
                ui.set('display-password', 'No potfile found')
                return
            
            # Check if file is empty
            if os.path.getsize(potfile) == 0:
                logging.debug("[DisplayPassword] Potfile is empty")
                ui.set('display-password', 'No passwords yet')
                return
            
            # Read last line
            with open(potfile, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            if not lines:
                logging.debug("[DisplayPassword] No lines in potfile")
                ui.set('display-password', 'No passwords yet')
                return
            
            # Get last non-empty line
            last_line = ''
            for line in reversed(lines):
                if line.strip():
                    last_line = line.strip()
                    break
            
            if not last_line:
                logging.debug("[DisplayPassword] No valid lines in potfile")
                ui.set('display-password', 'No passwords yet')
                return
            
            # Parse format: hash1:hash2:ssid:password
            parts = last_line.split(':')
            
            if len(parts) >= 4:
                ssid = parts[2]
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
