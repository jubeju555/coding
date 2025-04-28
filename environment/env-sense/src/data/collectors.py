import win32api
import win32con
import win32gui
import win32process
import psutil
import datetime
import pythoncom
import win32com.client
import os
import logging

class DataCollector:
    def __init__(self):
        self.data = []

    def collect_user_activity(self):
        # Logic to collect user activity data
        pass

    def collect_environment_data(self):
        # Logic to collect environmental data (e.g., lighting, sound)
        pass

    def collect_time_based_data(self):
        # Logic to collect data based on time of day
        pass

    def aggregate_data(self):
        # Logic to aggregate collected data for processing
        pass

    def get_collected_data(self):
        return self.data

    def clear_data(self):
        self.data = []


class TimeCollector:
    """Collects time-related data."""
    
    def __init__(self):
        self.logger = logging.getLogger("TimeCollector")
    
    def collect(self):
        """Gather time-related data."""
        now = datetime.datetime.now()
        data = {
            'time_hour': now.hour,
            'time_minute': now.minute,
            'time_day_of_week': now.weekday(),
            'time_is_weekend': 1 if now.weekday() >= 5 else 0,
            'time_is_morning': 1 if 5 <= now.hour < 12 else 0,
            'time_is_afternoon': 1 if 12 <= now.hour < 17 else 0,
            'time_is_evening': 1 if 17 <= now.hour < 22 else 0,
            'time_is_night': 1 if now.hour >= 22 or now.hour < 5 else 0
        }
        return data


class WindowsSystemCollector:
    """Collects system-related data from Windows."""
    
    def __init__(self):
        self.logger = logging.getLogger("WindowsSystemCollector")
    
    def collect(self):
        """Gather system-related data."""
        try:
            data = {
                'system_cpu_usage': psutil.cpu_percent(),
                'system_memory_usage': psutil.virtual_memory().percent,
                'system_battery': self._get_battery_info(),
                'system_active_window': self._get_active_window(),
                'system_active_processes': self._get_active_processes()
            }
            return data
        except Exception as e:
            self.logger.error(f"Error collecting Windows system data: {e}")
            return {}
    
    def _get_battery_info(self):
        """Get battery percentage if available."""
        try:
            battery = psutil.sensors_battery()
            return battery.percent if battery else 100
        except:
            return 100  # Default to 100% if not available
    
    def _get_active_window(self):
        """Get the currently active window."""
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                return process.name()
            except:
                return "unknown"
        except:
            return "unknown"
            
    def _get_active_processes(self):
        """Get a list of user-facing applications currently running."""
        active_apps = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Filter to only include visible applications
                if win32gui.IsWindowVisible(win32gui.FindWindow(None, proc.name())):
                    active_apps.append(proc.name())
            except:
                pass
        return active_apps


class CalendarCollector:
    """Collects calendar events from Outlook."""
    
    def __init__(self):
        self.logger = logging.getLogger("CalendarCollector")
    
    def collect(self):
        """Gather calendar events for today."""
        try:
            # Initialize COM for this thread
            pythoncom.CoInitialize()
            
            outlook = win32com.client.Dispatch("Outlook.Application")
            namespace = outlook.GetNamespace("MAPI")
            calendar = namespace.GetDefaultFolder(9)  # 9 is the calendar folder
            
            today = datetime.datetime.now().date()
            start_time = datetime.datetime.combine(today, datetime.time.min)
            end_time = datetime.datetime.combine(today, datetime.time.max)
            
            # Filter for today's events
            restriction = f"[Start] >= '{start_time.strftime('%m/%d/%Y')}' AND [End] <= '{end_time.strftime('%m/%d/%Y')}'"
            appointments = calendar.Items.Restrict(restriction)
            
            # Process the events
            current_events = []
            upcoming_events = []
            now = datetime.datetime.now()
            
            for appointment in appointments:
                event_data = {
                    'subject': appointment.Subject,
                    'start': appointment.Start,
                    'end': appointment.End,
                    'location': appointment.Location
                }
                
                # Check if event is happening now
                if appointment.Start <= now <= appointment.End:
                    current_events.append(event_data)
                elif now < appointment.Start:
                    upcoming_events.append(event_data)
            
            return {
                'calendar_has_current_meeting': len(current_events) > 0,
                'calendar_current_meetings': current_events,
                'calendar_upcoming_meetings': upcoming_events,
                'calendar_next_meeting_in_minutes': self._get_minutes_to_next_meeting(upcoming_events, now)
            }
            
        except Exception as e:
            self.logger.error(f"Error collecting calendar data: {e}")
            return {
                'calendar_has_current_meeting': False,
                'calendar_current_meetings': [],
                'calendar_upcoming_meetings': [],
                'calendar_next_meeting_in_minutes': None
            }
        finally:
            pythoncom.CoUninitialize()
    
    def _get_minutes_to_next_meeting(self, upcoming_events, now):
        """Calculate minutes until the next meeting."""
        if not upcoming_events:
            return None
        
        next_meeting = min(upcoming_events, key=lambda x: x['start'])
        delta = next_meeting['start'] - now
        return int(delta.total_seconds() / 60)