import tkinter as tk
from tkinter import ttk
import threading
import time
import logging
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard:
    """Simple dashboard UI for the environment manager."""
    
    def __init__(self, env_manager, storage):
        """
        Initialize the dashboard.
        
        Args:
            env_manager: The environment manager instance
            storage: The data storage instance
        """
        self.env_manager = env_manager
        self.storage = storage
        self.logger = logging.getLogger("Dashboard")
        self.root = None
        self.update_thread = None
        self.running = False
        
    def start(self):
        """Start the dashboard."""
        if self.root:
            self.logger.warning("Dashboard already running")
            return
            
        self.running = True
        
        # Create root window
        self.root = tk.Tk()
        self.root.title("Environment Manager Dashboard")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        
        # Create notebook with tabs
        notebook = ttk.Notebook(self.root)
        
        # Create main status tab
        status_tab = ttk.Frame(notebook)
        notebook.add(status_tab, text="Status")
        self._setup_status_tab(status_tab)
        
        # Create settings tab
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="Settings")
        self._setup_settings_tab(settings_tab)
        
        # Create history tab
        history_tab = ttk.Frame(notebook)
        notebook.add(history_tab, text="History")
        self._setup_history_tab(history_tab)
        
        notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Start update thread
        self.update_thread = threading.Thread(target=self._update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        # Run UI
        self.root.mainloop()
        
    def stop(self):
        """Stop the dashboard."""
        self.running = False
        if self.root:
            self.root.destroy()
            self.root = None
            
        if self.update_thread:
            self.update_thread.join(timeout=1.0)
            
    def _setup_status_tab(self, parent):
        """Set up the status tab."""
        # Status header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header_frame, text="Environment Status", font=("Arial", 16)).pack(side="left")
        
        self.status_indicator = ttk.Label(header_frame, text="●", font=("Arial", 16))
        self.status_indicator.pack(side="right")
        self.status_indicator.config(foreground="green")
        
        # Current environment
        env_frame = ttk.LabelFrame(parent, text="Current Environment")
        env_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create status grid
        status_grid = ttk.Frame(env_frame)
        status_grid.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Row 0: Lighting
        ttk.Label(status_grid, text="Lighting:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.lighting_label = ttk.Label(status_grid, text="Unknown")
        self.lighting_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Row 1: Sound
        ttk.Label(status_grid, text="Sound:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.sound_label = ttk.Label(status_grid, text="Unknown")
        self.sound_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Row 2: Workspace
        ttk.Label(status_grid, text="Workspace:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.workspace_label = ttk.Label(status_grid, text="Unknown")
        self.workspace_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Row 3: Last Adjustment
        ttk.Label(status_grid, text="Last Adjustment:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.last_adjustment_label = ttk.Label(status_grid, text="Never")
        self.last_adjustment_label.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Feedback frame
        feedback_frame = ttk.LabelFrame(parent, text="Provide Feedback")
        feedback_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(feedback_frame, text="How satisfied are you with the current environment?").pack(padx=10, pady=5)
        
        scale_frame = ttk.Frame(feedback_frame)
        scale_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(scale_frame, text="Not at all").pack(side="left")
        
        self.satisfaction_scale = ttk.Scale(scale_frame, from_=0, to=100, orient="horizontal")
        self.satisfaction_scale.pack(side="left", fill="x", expand=True, padx=5)
        self.satisfaction_scale.set(50)
        
        ttk.Label(scale_frame, text="Very satisfied").pack(side="left")
        
        ttk.Button(feedback_frame, text="Submit Feedback", 
                   command=self._submit_feedback).pack(pady=10)
        
    def _setup_settings_tab(self, parent):
        """Set up the settings tab."""
        # Create settings frame
        settings_frame = ttk.Frame(parent)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create scrollable canvas for settings
        canvas = tk.Canvas(settings_frame)
        scrollbar = ttk.Scrollbar(settings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create settings controls
        
        # General settings
        general_frame = ttk.LabelFrame(scrollable_frame, text="General Settings")
        general_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(general_frame, text="Environment check frequency (seconds):").grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.frequency_var = tk.StringVar(value="60")
        frequency_entry = ttk.Entry(general_frame, textvariable=self.frequency_var, width=10)
        frequency_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Lighting settings
        lighting_frame = ttk.LabelFrame(scrollable_frame, text="Lighting Settings")
        lighting_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(lighting_frame, text="Brightness:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.brightness_var = tk.IntVar(value=75)
        brightness_slider = ttk.Scale(lighting_frame, from_=0, to=100, 
                                     orient="horizontal", variable=self.brightness_var)
        brightness_slider.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Label(lighting_frame, text="Color Temperature:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.color_temp_var = tk.IntVar(value=4000)
        color_temp_slider = ttk.Scale(lighting_frame, from_=2000, to=6500, 
                                     orient="horizontal", variable=self.color_temp_var)
        color_temp_slider.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Sound settings
        sound_frame = ttk.LabelFrame(scrollable_frame, text="Sound Settings")
        sound_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(sound_frame, text="Volume:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.volume_var = tk.IntVar(value=50)
        volume_slider = ttk.Scale(sound_frame, from_=0, to=100, 
                                 orient="horizontal", variable=self.volume_var)
        volume_slider.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Label(sound_frame, text="Sound Profile:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.sound_profile_var = tk.StringVar(value="normal")
        sound_profile_combo = ttk.Combobox(sound_frame, textvariable=self.sound_profile_var)
        sound_profile_combo['values'] = ('normal', 'meeting', 'media', 'quiet')
        sound_profile_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Workspace settings
        workspace_frame = ttk.LabelFrame(scrollable_frame, text="Workspace Settings")
        workspace_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(workspace_frame, text="App Arrangement:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.app_arrangement_var = tk.StringVar(value="default")
        app_arrangement_combo = ttk.Combobox(workspace_frame, textvariable=self.app_arrangement_var)
        app_arrangement_combo['values'] = ('default', 'focused', 'productive', 'relaxed')
        app_arrangement_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Label(workspace_frame, text="Desktop Arrangement:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.desktop_arrangement_var = tk.StringVar(value="default")
        desktop_arrangement_combo = ttk.Combobox(workspace_frame, 
                                               textvariable=self.desktop_arrangement_var)
        desktop_arrangement_combo['values'] = ('default', 'focused', 'productive', 'relaxed')
        desktop_arrangement_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Save/Apply button
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill="x", padx=10, pady=20)
        
        ttk.Button(button_frame, text="Apply Settings", 
                  command=self._apply_settings).pack(side="right", padx=5)
        
        ttk.Button(button_frame, text="Save Current Layout", 
                  command=self._save_layout).pack(side="right", padx=5)
        
    def _setup_history_tab(self, parent):
        """Set up the history tab."""
        # Create container for the plot
        plot_frame = ttk.Frame(parent)
        plot_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(7, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Create controls frame
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(controls_frame, text="Metric:").pack(side="left", padx=5)
        
        self.metric_var = tk.StringVar(value="satisfaction")
        metric_combo = ttk.Combobox(controls_frame, textvariable=self.metric_var, width=15)
        metric_combo['values'] = ('satisfaction', 'lighting_brightness', 'sound_volume')
        metric_combo.pack(side="left", padx=5)
        
        ttk.Button(controls_frame, text="Refresh", 
                  command=self._update_history_plot).pack(side="right", padx=5)
        
        # Initial plot
        self._update_history_plot()
        
    def _update_loop(self):
        """Background thread to update the UI."""
        while self.running:
            try:
                # Update status
                if self.env_manager:
                    # Get current state from adapters
                    lighting_adapter = next((a for a in self.env_manager.adapters 
                                          if a.__class__.__name__ == 'LightingAdapter'), None)
                    sound_adapter = next((a for a in self.env_manager.adapters 
                                        if a.__class__.__name__ == 'SoundAdapter'), None)
                    workspace_adapter = next((a for a in self.env_manager.adapters 
                                           if a.__class__.__name__ == 'WorkspaceAdapter'), None)
                    
                    # Update UI with adapter state
                    if lighting_adapter:
                        settings = lighting_adapter.get_current_settings()
                        brightness = settings.get('lighting_brightness', 'Unknown')
                        color_temp = settings.get('lighting_color_temp', 'Unknown')
                        self.root.after(0, lambda: self.lighting_label.config(
                            text=f"Brightness: {brightness}%, Color Temp: {color_temp}K"))
                        
                    if sound_adapter:
                        settings = sound_adapter.get_current_settings()
                        volume = settings.get('sound_volume', 'Unknown')
                        profile = settings.get('sound_profile', 'Unknown')
                        self.root.after(0, lambda: self.sound_label.config(
                            text=f"Volume: {volume}%, Profile: {profile}"))
                        
                    if workspace_adapter:
                        settings = workspace_adapter.get_current_settings()
                        app_mode = settings.get('app_arrangement', 'Unknown')
                        desktop_mode = settings.get('desktop_arrangement', 'Unknown')
                        self.root.after(0, lambda: self.workspace_label.config(
                            text=f"App Mode: {app_mode}, Desktop: {desktop_mode}"))
                    
                    # Update last adjustment time
                    self.root.after(0, lambda: self.last_adjustment_label.config(
                        text=datetime.now().strftime("%H:%M:%S")))
                
            except Exception as e:
                self.logger.error(f"Error in UI update loop: {e}")
                
            # Sleep before next update
            time.sleep(2)
        
    def _submit_feedback(self):
        """Submit user feedback."""
        try:
            satisfaction = self.satisfaction_scale.get()
            
            # Get current settings from adapters
            current_settings = {}
            
            for adapter in self.env_manager.adapters:
                if hasattr(adapter, 'get_current_settings'):
                    current_settings.update(adapter.get_current_settings())
            
            # Record feedback
            self.env_manager.preference_engine.record_feedback(current_settings, satisfaction)
            
            # Show confirmation
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Feedback", f"Thank you for your feedback! (Score: {satisfaction}/100)")
            
        except Exception as e:
            self.logger.error(f"Error submitting feedback: {e}")
            
    def _apply_settings(self):
        """Apply settings from UI to environment manager."""
        try:
            # Collect settings from UI
            settings = {
                'lighting_brightness': self.brightness_var.get(),
                'lighting_color_temp': self.color_temp_var.get(),
                'sound_volume': self.volume_var.get(),
                'sound_profile': self.sound_profile_var.get(),
                'app_arrangement': self.app_arrangement_var.get(),
                'desktop_arrangement': self.desktop_arrangement_var.get()
            }
            
            # Update adjustment frequency
            try:
                frequency = int(self.frequency_var.get())
                if 10 <= frequency <= 3600:  # Reasonable bounds
                    self.env_manager.adjustment_frequency = frequency
            except ValueError:
                pass
                
            # Apply settings through adapters
            for adapter in self.env_manager.adapters:
                relevant_settings = {k: v for k, v in settings.items() 
                                    if k in adapter.supported_settings()}
                if relevant_settings:
                    adapter.apply_settings(relevant_settings)
            
            # Show confirmation
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Settings Applied", "Environment settings have been applied.")
            
        except Exception as e:
            self.logger.error(f"Error applying settings: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Could not apply settings: {e}")
            
    def _save_layout(self):
        """Save current window layout."""
        try:
            # Find the workspace adapter
            workspace_adapter = next((a for a in self.env_manager.adapters 
                                    if a.__class__.__name__ == 'WorkspaceAdapter'), None)
                                    
            if workspace_adapter:
                layout_name = self.app_arrangement_var.get()
                workspace_adapter.save_current_layout(layout_name)
                
                # Show confirmation
                import tkinter.messagebox as messagebox
                messagebox.showinfo("Layout Saved", f"Current window layout has been saved as '{layout_name}'.")
                
        except Exception as e:
            self.logger.error(f"Error saving layout: {e}")
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Could not save layout: {e}")
            
    def _update_history_plot(self):
        """Update the history plot with selected metric."""
        try:
            metric = self.metric_var.get()
            
            # Get historical data
            user_prefs = self.storage.get_environment_data(limit=50)
            
            if not user_prefs:
                return
                
            # Extract timestamps and metric values
            timestamps = []
            values = []
            
            if metric == 'satisfaction':
                for pref in user_prefs:
                    if 'satisfaction' in pref:
                        timestamps.append(datetime.fromisoformat(pref['timestamp']))
                        values.append(pref['satisfaction'])
            else:
                for pref in user_prefs:
                    if metric in pref:
                        timestamps.append(datetime.fromisoformat(pref['timestamp']))
                        values.append(pref[metric])
            
            # Clear existing plot
            self.ax.clear()
            
            # Create new plot
            if timestamps and values:
                self.ax.plot(timestamps, values, 'o-')
                self.ax.set_title(f"{metric.replace('_', ' ').title()} Over Time")
                self.ax.set_xlabel("Time")
                self.ax.set_ylabel(metric.replace('_', ' ').title())
                self.ax.grid(True)
                
                # Format x-axis as time
                self.fig.autofmt_xdate()
                
                # Redraw
                self.canvas.draw()
            
        except Exception as e:
            self.logger.error(f"Error updating history plot: {e}")