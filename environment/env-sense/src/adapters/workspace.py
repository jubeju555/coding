import logging
import subprocess
import json
import os
import win32gui
import win32con
import win32process
import psutil
import time

class Workspace:
    def __init__(self):
        self.settings = {
            "theme": "light",
            "font_size": 12,
            "layout": "default",
            "notifications": True
        }

    def update_settings(self, new_settings):
        self.settings.update(new_settings)

    def get_settings(self):
        return self.settings

    def apply_settings(self):
        # Logic to apply workspace settings
        pass

    def reset_settings(self):
        self.settings = {
            "theme": "light",
            "font_size": 12,
            "layout": "default",
            "notifications": True
        }

class WorkspaceAdapter:
    """Adapter for controlling window and application arrangements."""
    
    def __init__(self):
        self.logger = logging.getLogger("WorkspaceAdapter")
        self.current_settings = {
            'app_arrangement': 'default',
            'desktop_arrangement': 'default',
            'active_apps': []
        }
        # Store window positions for different arrangements
        self.window_layouts = {
            'default': {},
            'focused': {},
            'productive': {},
            'relaxed': {}
        }
        # Load saved layouts if available
        self._load_layouts()
        
    def supported_settings(self):
        """Return a list of settings this adapter can modify."""
        return ['app_arrangement', 'desktop_arrangement', 'active_apps']
        
    def apply_settings(self, settings):
        """Apply workspace settings to the environment."""
        # Update internal state
        self.current_settings.update(settings)
        
        success = False
        
        # Apply app arrangement
        if 'app_arrangement' in settings:
            success = self._arrange_windows() or success
            
        # Apply desktop arrangement
        if 'desktop_arrangement' in settings:
            success = self._apply_desktop_settings() or success
            
        # Launch or close apps as needed
        if 'active_apps' in settings:
            success = self._manage_active_apps() or success
            
        return success
        
    def get_current_settings(self):
        """Return current workspace settings."""
        return self.current_settings.copy()
        
    def save_current_layout(self, layout_name):
        """Save the current window layout."""
        layout = {}
        
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    process = psutil.Process(pid)
                    app_name = process.name()
                    
                    # Get window position and state
                    rect = win32gui.GetWindowRect(hwnd)
                    placement = win32gui.GetWindowPlacement(hwnd)
                    
                    layout[app_name] = {
                        'hwnd': hwnd,
                        'title': win32gui.GetWindowText(hwnd),
                        'rect': rect,
                        'state': placement[1]  # Window state (minimized, maximized, etc.)
                    }
                except:
                    pass
            return True
            
        win32gui.EnumWindows(callback, None)
        
        # Save layout
        self.window_layouts[layout_name] = layout
        self._save_layouts()
        
        self.logger.info(f"Saved window layout '{layout_name}' with {len(layout)} windows")
        return True
        
    def _arrange_windows(self):
        """Arrange windows according to the current layout setting."""
        layout_name = self.current_settings['app_arrangement']
        layout = self.window_layouts.get(layout_name, {})
        
        if not layout:
            self.logger.warning(f"No saved layout found for '{layout_name}'")
            return False
            
        # Find and arrange windows
        for app_name, window_info in layout.items():
            try:
                # Find matching windows by process name
                def enum_callback(hwnd, results):
                    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                        try:
                            _, pid = win32process.GetWindowThreadProcessId(hwnd)
                            process = psutil.Process(pid)
                            if process.name() == app_name:
                                results.append(hwnd)
                        except:
                            pass
                    return True
                    
                matching_windows = []
                win32gui.EnumWindows(enum_callback, matching_windows)
                
                # Arrange each matching window
                for hwnd in matching_windows:
                    # Set window position and state
                    rect = window_info['rect']
                    state = window_info['state']
                    
                    # First restore the window if minimized or maximized
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    
                    # Set position
                    win32gui.MoveWindow(hwnd, rect[0], rect[1], 
                                        rect[2] - rect[0], rect[3] - rect[1], True)
                    
                    # Set state (minimized, maximized, etc.)
                    if state == win32con.SW_SHOWMAXIMIZED:
                        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                    elif state == win32con.SW_SHOWMINIMIZED:
                        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                        
            except Exception as e:
                self.logger.error(f"Error arranging window for {app_name}: {e}")
                
        self.logger.info(f"Applied window layout '{layout_name}'")
        return True
        
    def _apply_desktop_settings(self):
        """Apply desktop environment settings."""
        desktop_mode = self.current_settings['desktop_arrangement']
        
        try:
            if desktop_mode == 'focused':
                # Hide desktop icons
                subprocess.run(['reg', 'add', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 
                               '/v', 'HideIcons', '/t', 'REG_DWORD', '/d', '1', '/f'])
                               
                # Turn on Do Not Disturb mode
                subprocess.run(['powershell', '-Command', 'Set-WinUserNotificationSetting -Type DoNotDisturb -Setting Enabled'])
                
            elif desktop_mode == 'productive':
                # Show desktop icons
                subprocess.run(['reg', 'add', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 
                               '/v', 'HideIcons', '/t', 'REG_DWORD', '/d', '0', '/f'])
                               
                # Turn on Do Not Disturb mode
                subprocess.run(['powershell', '-Command', 'Set-WinUserNotificationSetting -Type DoNotDisturb -Setting Enabled'])
                
            elif desktop_mode == 'relaxed':
                # Show desktop icons
                subprocess.run(['reg', 'add', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 
                               '/v', 'HideIcons', '/t', 'REG_DWORD', '/d', '0', '/f'])
                               
                # Turn off Do Not Disturb mode
                subprocess.run(['powershell', '-Command', 'Set-WinUserNotificationSetting -Type DoNotDisturb -Setting Disabled'])
                
            else:  # default
                # Show desktop icons
                subprocess.run(['reg', 'add', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 
                               '/v', 'HideIcons', '/t', 'REG_DWORD', '/d', '0', '/f'])
                               
                # Turn off Do Not Disturb mode
                subprocess.run(['powershell', '-Command', 'Set-WinUserNotificationSetting -Type DoNotDisturb -Setting Disabled'])
                
            # Refresh desktop
            subprocess.run(['ie4uinit.exe', '-show'])
            
            self.logger.info(f"Applied desktop arrangement '{desktop_mode}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying desktop settings: {e}")
            return False
            
    def _manage_active_apps(self):
        """Launch or close applications as needed."""
        target_apps = set(self.current_settings['active_apps'])
        
        # Get currently running apps
        running_apps = set()
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                running_apps.add(proc.info['name'])
            except:
                pass
                
        # Apps to launch
        to_launch = target_apps - running_apps
        
        # Launch required apps
        for app_name in to_launch:
            try:
                # Simple mapping of common app names to executable paths
                app_paths = {
                    'chrome.exe': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                    'msedge.exe': 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
                    'notepad.exe': 'notepad.exe',
                    'code.exe': 'code',
                    'outlook.exe': 'outlook',
                    'Teams.exe': 'Teams',
                    'spotify.exe': 'spotify',
                }
                
                if app_name in app_paths:
                    subprocess.Popen(app_paths[app_name])
                    self.logger.info(f"Launched application: {app_name}")
                
            except Exception as e:
                self.logger.error(f"Error launching {app_name}: {e}")
                
        self.logger.info(f"Managed active applications, launched {len(to_launch)} apps")
        return len(to_launch) > 0
        
    def _load_layouts(self):
        """Load saved window layouts from file."""
        try:
            layout_path = os.path.join(os.path.expanduser('~'), '.env-sense', 'window_layouts.json')
            if os.path.exists(layout_path):
                with open(layout_path, 'r') as f:
                    # Load layouts but convert string keys back to integers for hwnd
                    saved_layouts = json.load(f)
                    
                    # Process layouts to handle serialization issues
                    for layout_name, layout in saved_layouts.items():
                        processed_layout = {}
                        for app_name, window_info in layout.items():
                            # Convert rect from list to tuple
                            if 'rect' in window_info and isinstance(window_info['rect'], list):
                                window_info['rect'] = tuple(window_info['rect'])
                            processed_layout[app_name] = window_info
                            
                        self.window_layouts[layout_name] = processed_layout
                        
                self.logger.info(f"Loaded {len(saved_layouts)} window layouts")
        except Exception as e:
            self.logger.error(f"Error loading window layouts: {e}")
            
    def _save_layouts(self):
        """Save window layouts to file."""
        try:
            # Ensure directory exists
            layout_dir = os.path.join(os.path.expanduser('~'), '.env-sense')
            if not os.path.exists(layout_dir):
                os.makedirs(layout_dir)
                
            layout_path = os.path.join(layout_dir, 'window_layouts.json')
            
            # Process layouts for serialization
            serializable_layouts = {}
            for layout_name, layout in self.window_layouts.items():
                serializable_layout = {}
                for app_name, window_info in layout.items():
                    serializable_window_info = dict(window_info)
                    
                    # Convert rect tuple to list for serialization
                    if 'rect' in serializable_window_info and isinstance(serializable_window_info['rect'], tuple):
                        serializable_window_info['rect'] = list(serializable_window_info['rect'])
                        
                    serializable_layout[app_name] = serializable_window_info
                    
                serializable_layouts[layout_name] = serializable_layout
                
            with open(layout_path, 'w') as f:
                json.dump(serializable_layouts, f, indent=2)
                
            self.logger.info(f"Saved {len(serializable_layouts)} window layouts")
        except Exception as e:
            self.logger.error(f"Error saving window layouts: {e}")