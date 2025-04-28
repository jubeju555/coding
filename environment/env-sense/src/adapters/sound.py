import logging
import subprocess
import ctypes
from ctypes import cast, POINTER
import os
from playsound import playsound

# Try to import Windows-specific audio libraries
try:
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False

class SoundManager:
    def __init__(self):
        self.sound_profiles = {
            'focus': 'sounds/focus.mp3',
            'relax': 'sounds/relax.mp3',
            'energize': 'sounds/energize.mp3'
        }
        self.current_profile = None

    def set_sound_profile(self, profile_name):
        if profile_name in self.sound_profiles:
            self.current_profile = self.sound_profiles[profile_name]
            self.play_sound()
        else:
            print(f"Profile '{profile_name}' not found.")

    def play_sound(self):
        if self.current_profile and os.path.exists(self.current_profile):
            playsound(self.current_profile)
        else:
            print("No sound profile set or file does not exist.")

    def stop_sound(self):
        # Placeholder for stopping sound functionality
        print("Stopping sound... (functionality to be implemented)")

    def list_profiles(self):
        return list(self.sound_profiles.keys())

class SoundAdapter:
    """Adapter for controlling sound settings in the user's environment."""
    
    def __init__(self):
        self.logger = logging.getLogger("SoundAdapter")
        self.current_settings = {
            'sound_volume': 50,
            'sound_mute': False,
            'sound_profile': 'normal'  # normal, meeting, media, quiet
        }
        
    def supported_settings(self):
        """Return a list of settings this adapter can modify."""
        return ['sound_volume', 'sound_mute', 'sound_profile']
        
    def apply_settings(self, settings):
        """Apply sound settings to the environment."""
        # Update internal state
        self.current_settings.update(settings)
        
        success = False
        
        # Apply system volume
        if 'sound_volume' in settings or 'sound_mute' in settings:
            success = self._set_system_volume()
            
        # Apply sound profile
        if 'sound_profile' in settings:
            success = self._apply_sound_profile() or success
            
        return success
        
    def get_current_settings(self):
        """Return current sound settings."""
        return self.current_settings.copy()
        
    def _set_system_volume(self):
        """Set the system volume level."""
        volume = self.current_settings['sound_volume']
        mute = self.current_settings['sound_mute']
        
        try:
            if PYCAW_AVAILABLE:
                # Use pycaw to control Windows audio
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
                
                # Set volume (0.0 to 1.0)
                volume_interface.SetMasterVolumeLevelScalar(volume / 100.0, None)
                
                # Set mute state
                volume_interface.SetMute(mute, None)
                
                self.logger.info(f"Set system volume to {volume}%, mute: {mute}")
                return True
            else:
                # Fallback using nircmd on Windows
                vol_level = int(655.35 * volume)  # Convert percentage to nircmd value
                if os.name == 'nt':  # Check if Windows
                    mute_cmd = "nircmd.exe mutesysvolume 1" if mute else "nircmd.exe mutesysvolume 0"
                    vol_cmd = f"nircmd.exe setsysvolume {vol_level}"
                    
                    # Run commands if nircmd is available
                    subprocess.run(vol_cmd, shell=True)
                    subprocess.run(mute_cmd, shell=True)
                    self.logger.info(f"Set system volume using nircmd to {volume}%, mute: {mute}")
                    return True
                else:
                    self.logger.warning("No supported volume control method available")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error setting system volume: {e}")
            return False
            
    def _apply_sound_profile(self):
        """Apply the selected sound profile."""
        profile = self.current_settings['sound_profile']
        
        try:
            # Define volume levels for different apps based on profile
            if profile == 'meeting':
                app_volumes = {
                    'Teams.exe': 90,
                    'Zoom.exe': 90,
                    'slack.exe': 85,
                    'chrome.exe': 60,
                    'spotify.exe': 30,
                    'vlc.exe': 30
                }
            elif profile == 'media':
                app_volumes = {
                    'spotify.exe': 85,
                    'vlc.exe': 85,
                    'chrome.exe': 80,
                    'Teams.exe': 40,
                    'slack.exe': 40
                }
            elif profile == 'quiet':
                app_volumes = {
                    'Teams.exe': 50,
                    'Zoom.exe': 50,
                    'slack.exe': 50,
                    'chrome.exe': 50,
                    'spotify.exe': 40,
                    'vlc.exe': 40
                }
            else:  # normal
                app_volumes = {
                    'Teams.exe': 75,
                    'Zoom.exe': 75,
                    'slack.exe': 75,
                    'chrome.exe': 75,
                    'spotify.exe': 70,
                    'vlc.exe': 70
                }
                
            if PYCAW_AVAILABLE:
                # For each audio session, set the volume per application
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions:
                    volume = app_volumes.get(session.Process.name(), None)
                    if volume is not None:
                        session.SimpleAudioVolume.SetMasterVolume(volume / 100.0, None)
                        self.logger.info(f"Set volume for {session.Process.name()} to {volume}%")
                return True
            else:
                self.logger.warning("PYCAW not available, cannot apply sound profile")
                return False
                
        except Exception as e:
            self.logger.error(f"Error applying sound profile: {e}")
            return False