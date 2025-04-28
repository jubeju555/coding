import logging
import platform
import os
import subprocess
import psutil
import win32api
import win32con
import win32gui

class SystemInterface:
    """Interface for interacting with the underlying operating system."""
    
    def __init__(self):
        self.logger = logging.getLogger("SystemInterface")
        self.platform = platform.system()
        
    def adjust_lighting(self, level):
        """Adjust the lighting level in the environment."""
        pass

    def adjust_sound(self, volume):
        """Adjust the sound volume in the environment."""
        pass

    def get_current_settings(self):
        """Retrieve the current system settings for lighting and sound."""
        return {
            "lighting": None,
            "sound": None
        }

    def apply_settings(self, settings):
        """Apply the given settings to the system."""
        if "lighting" in settings:
            self.adjust_lighting(settings["lighting"])
        if "sound" in settings:
            self.adjust_sound(settings["sound"])

    def get_system_info(self):
        """Get basic system information."""
        info = {
            'platform': self.platform,
            'hostname': platform.node(),
            'version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'memory': psutil.virtual_memory().total / (1024 * 1024 * 1024)  # GB
        }
        return info
        
    def is_power_connected(self):
        """Check if the system is connected to power (AC) or on battery."""
        try:
            if self.platform == 'Windows':
                return psutil.sensors_battery().power_plugged
            else:
                # Default to True for non-laptop devices
                return True
        except:
            return True
            
    def get_battery_level(self):
        """Get the current battery level as a percentage."""
        try:
            battery = psutil.sensors_battery()
            return battery.percent if battery else 100
        except:
            return 100
            
    def lock_workstation(self):
        """Lock the workstation."""
        try:
            if self.platform == 'Windows':
                win32api.LockWorkStation()
                self.logger.info("Workstation locked")
                return True
        except Exception as e:
            self.logger.error(f"Error locking workstation: {e}")
            return False
            
    def put_display_to_sleep(self):
        """Put the display to sleep."""
        try:
            if self.platform == 'Windows':
                # Turn off monitor
                win32gui.SendMessage(win32con.HWND_BROADCAST, 
                                     win32con.WM_SYSCOMMAND, 
                                     win32con.SC_MONITORPOWER, 
                                     2)
                self.logger.info("Display put to sleep")
                return True
        except Exception as e:
            self.logger.error(f"Error putting display to sleep: {e}")
            return False
            
    def wake_display(self):
        """Wake up the display."""
        try:
            if self.platform == 'Windows':
                # Wake up monitor
                win32gui.SendMessage(win32con.HWND_BROADCAST, 
                                     win32con.WM_SYSCOMMAND, 
                                     win32con.SC_MONITORPOWER, 
                                     -1)
                self.logger.info("Display woken up")
                return True
        except Exception as e:
            self.logger.error(f"Error waking display: {e}")
            return False
            
    def start_application(self, app_path):
        """Start an application."""
        try:
            if os.path.exists(app_path) or app_path.lower() in ['notepad', 'calc', 'mspaint']:
                subprocess.Popen(app_path)
                self.logger.info(f"Started application: {app_path}")
                return True
            else:
                self.logger.warning(f"Application not found: {app_path}")
                return False
        except Exception as e:
            self.logger.error(f"Error starting application: {e}")
            return False
            
    def close_application(self, app_name):
        """Close an application by name."""
        try:
            closed = False
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == app_name.lower():
                        proc.terminate()
                        closed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                    
            if closed:
                self.logger.info(f"Closed application: {app_name}")
            else:
                self.logger.warning(f"Application not found: {app_name}")
                
            return closed
        except Exception as e:
            self.logger.error(f"Error closing application: {e}")
            return False
            
    def restart_application(self, app_path, app_name):
        """Restart an application."""
        try:
            self.close_application(app_name)
            # Wait briefly for the application to close
            import time
            time.sleep(1.5)
            return self.start_application(app_path)
        except Exception as e:
            self.logger.error(f"Error restarting application: {e}")
            return False