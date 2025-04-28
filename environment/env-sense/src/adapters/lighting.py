import logging
import subprocess
import os

class LightingAdapter:
    """Adapter for controlling lighting in the user's environment."""
    
    def __init__(self):
        self.logger = logging.getLogger("LightingAdapter")
        self.current_settings = {
            'lighting_brightness': 75,
            'lighting_color_temp': 4000,  # Kelvin
            'lighting_mode': 'auto'
        }
        # Check which lighting systems are available
        self.available_systems = self._detect_lighting_systems()
        
    def supported_settings(self):
        """Return a list of settings this adapter can modify."""
        return ['lighting_brightness', 'lighting_color_temp', 'lighting_mode']
        
    def apply_settings(self, settings):
        """Apply lighting settings to the environment."""
        if not self.available_systems:
            self.logger.warning("No supported lighting systems found")
            return False
            
        success = False
        
        # Update internal state
        self.current_settings.update(settings)
        
        # Apply settings to detected systems
        for system in self.available_systems:
            if system == 'hue':
                success |= self._apply_hue_settings()
            elif system == 'yeelight':
                success |= self._apply_yeelight_settings()
            elif system == 'windows':
                success |= self._apply_windows_settings()
                
        return success
        
    def get_current_settings(self):
        """Return current lighting settings."""
        return self.current_settings.copy()
        
    def _detect_lighting_systems(self):
        """Detect available lighting systems."""
        systems = []
        
        # Check for Phillips Hue Bridge
        try:
            # Simple check if Hue bridge IP is stored in config file
            if os.path.exists(os.path.expanduser('~/.hue_bridge')):
                systems.append('hue')
        except:
            pass
            
        # Check for Yeelight bulbs on network
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            sock.sendto(b'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1982\r\nMAN: "ssdp:discover"\r\nST: wifi_bulb\r\n', ('239.255.255.250', 1982))
            try:
                sock.recvfrom(1024)
                systems.append('yeelight')
            except socket.timeout:
                pass
        except:
            pass
            
        # Windows always available for screen brightness
        systems.append('windows')
        
        self.logger.info(f"Detected lighting systems: {systems}")
        return systems
        
    def _apply_hue_settings(self):
        """Apply settings to Phillips Hue lights."""
        try:
            # This would use a proper Hue API in production
            bridge_ip = open(os.path.expanduser('~/.hue_bridge')).read().strip()
            brightness = self.current_settings['lighting_brightness']
            color_temp = self.current_settings['lighting_color_temp']
            
            # Mock implementation - in production, use the Hue API
            self.logger.info(f"Setting Hue lights to brightness: {brightness}, color temp: {color_temp}")
            return True
        except Exception as e:
            self.logger.error(f"Error setting Hue lights: {e}")
            return False
            
    def _apply_yeelight_settings(self):
        """Apply settings to Yeelight bulbs."""
        try:
            from yeelight import discover_bulbs, Bulb
            
            bulbs = discover_bulbs()
            brightness = self.current_settings['lighting_brightness']
            color_temp = self.current_settings['lighting_color_temp']
            
            for bulb_info in bulbs:
                bulb = Bulb(bulb_info["ip"])
                bulb.set_brightness(brightness)
                bulb.set_color_temp(color_temp)
                
            self.logger.info(f"Set {len(bulbs)} Yeelight bulbs to brightness: {brightness}, color temp: {color_temp}")
            return True
        except Exception as e:
            self.logger.error(f"Error setting Yeelight bulbs: {e}")
            return False
            
    def _apply_windows_settings(self):
        """Apply settings to Windows display brightness."""
        try:
            brightness = self.current_settings['lighting_brightness']
            
            # Use powercfg to adjust screen brightness
            subprocess.run(["powercfg", "/setacvalueindex", "SCHEME_CURRENT", "SUB_VIDEO", "VIDEODIM", str(100 - brightness)])
            subprocess.run(["powercfg", "/setdcvalueindex", "SCHEME_CURRENT", "SUB_VIDEO", "VIDEODIM", str(100 - brightness)])
            subprocess.run(["powercfg", "/setactive", "SCHEME_CURRENT"])
            
            self.logger.info(f"Set Windows screen brightness to {brightness}%")
            return True
        except Exception as e:
            self.logger.error(f"Error setting Windows screen brightness: {e}")
            return False