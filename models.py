# clock_model.py
import datetime
import pytz

class ClockModel:
    COMMON_TIMEZONES = {
        "Local Time": None, 
        "UTC": "UTC",
        "EST (New York)": "America/New_York",
        "PST (Los Angeles) - 3 ": "America/Los_Angeles",
        "CET (Paris)": "Europe/Paris",
        "JST (Tokyo)": "Asia/Tokyo"
    }
    
    def __init__(self):
        self._is_24_hour_format = True
        self._selected_timezone_key = "Local Time"
        self._selected_timezone = None 
        
        self._alarm_time = None 
        self._alarm_set = False
        self._alarm_triggered = False
        self._just_triggered = False 

        self._timer_total_seconds = 0
        self._timer_remaining_seconds = 0
        self._timer_running = False
        self._timer_finished = False
        self._timer_just_finished = False

    def toggle_format(self):
        """Toggles between 12-hour and 24-hour format."""
        self._is_24_hour_format = not self._is_24_hour_format

    def get_time_string(self):
        """Returns the current time string based on the selected format and timezone."""
        if self._selected_timezone:
            try:
                tz = pytz.timezone(self._selected_timezone)
                now = datetime.datetime.now(tz)
            except pytz.exceptions.UnknownTimeZoneError:
                now = datetime.datetime.now()
        else:
            now = datetime.datetime.now()

        if self._is_24_hour_format:
            time_str = now.strftime("%H:%M:%S")
        else:
            time_str = now.strftime("%I:%M:%S %p")
            
        self.check_alarm(now)
        
        return time_str

    def get_alarm_status(self):
        """Returns the status of the alarm."""
        if self._alarm_triggered:
            return "ALARM TRIGGERED!"
        elif self._alarm_set:
            alarm_str = self._alarm_time.strftime("%H:%M")
            return f"ALARM SET: {alarm_str}"
        else:
            return "ALARM OFF"

    def check_alarm(self, current_datetime):
        """Checks if the current time matches the set alarm time."""
        self._just_triggered = False
        if self._alarm_set and not self._alarm_triggered:
            current_time = current_datetime.time()
            if current_time.hour == self._alarm_time.hour and current_time.minute == self._alarm_time.minute:
                self._alarm_triggered = True
                self._just_triggered = True 
                
    def set_alarm(self, hour, minute):
        """Sets the alarm time."""
        try:
            self._alarm_time = datetime.time(hour, minute)
            self._alarm_set = True
            self._alarm_triggered = False
        except ValueError:
            pass

    def clear_alarm(self):
        """Clears the alarm."""
        self._alarm_set = False
        self._alarm_time = None
        self._alarm_triggered = False
        self._just_triggered = False
        self.hour = 0
        self.minute = 0
        

        

    # --- Timer Methods ---

    def set_timer(self, hours, minutes, seconds):
        """Sets the timer duration in seconds."""
        self._timer_total_seconds = hours * 3600 + minutes * 60 + seconds
        self._timer_remaining_seconds = self._timer_total_seconds
        self._timer_running = False
        self._timer_finished = False
        self._timer_just_finished = False

    def start_timer(self):
        """Starts the countdown timer."""
        if self._timer_remaining_seconds > 0 and not self._timer_running:
            self._timer_running = True
            self._timer_finished = False
            self._timer_just_finished = False

    def stop_timer(self):
        """Stops the countdown timer."""
        self._timer_running = False

    def reset_timer(self):
        """Resets the timer to its initial duration."""
        self._timer_total_seconds = 0
        self._timer_remaining_seconds = self._timer_total_seconds
        self._timer_running = False
        self._timer_finished = False
        self._timer_just_finished = False

    def tick_timer(self):
        """Decrements the timer by one second if running."""
        self._timer_just_finished = False
        if self._timer_running and self._timer_remaining_seconds > 0:
            self._timer_remaining_seconds -= 1
            if self._timer_remaining_seconds == 0:
                self._timer_running = False
                self._timer_finished = True
                self._timer_just_finished = True

    def get_timer_string(self):
        """Returns the remaining time as an HH:MM:SS string."""
        seconds = self._timer_remaining_seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_timer_status(self):
        """Returns the status of the timer."""
        if self._timer_finished:
            return "TIMER FINISHED!"
        elif self._timer_running:
            return "RUNNING"
        elif self._timer_total_seconds > 0:
            return "READY"
        else:
            return "OFF"

    def get_timer_just_finished_status(self):
        """Returns True if the timer just finished in this cycle."""
        return self._timer_just_finished

    def get_just_triggered_status(self):
        """Returns True if the alarm was just triggered in this cycle."""
        return self._just_triggered

    def get_date_string(self):
        """Returns the current date and day of the week string for the selected timezone."""
        if self._selected_timezone:
            try:
                tz = pytz.timezone(self._selected_timezone)
                now = datetime.datetime.now(tz)
            except pytz.exceptions.UnknownTimeZoneError:
                now = datetime.datetime.now()
        else:
            now = datetime.datetime.now()
            
        return now.strftime("%a, %b %d, %Y")

    def get_format_status(self):
        """Returns a string indicating the current format."""
        return "24-Hour" if self._is_24_hour_format else "12-Hour"

    def get_timezone_keys(self):
        """Returns the display names of the available timezones."""
        return list(self.COMMON_TIMEZONES.keys())

    def get_selected_timezone_key(self):
        """Returns the display name of the currently selected timezone."""
        return self._selected_timezone_key

    def set_timezone(self, tz_key):
        """Sets the new timezone based on the display key."""
        self._selected_timezone_key = tz_key
        self._selected_timezone = self.COMMON_TIMEZONES.get(tz_key)

# import tkinter as tk
# from tkinter import ttk
# import time
# import datetime
# import pytz
# import os 

# # --- Model ---
# class ClockModel:
#     COMMON_TIMEZONES = {
#         "Local Time": None, 
#         "UTC": "UTC",
#         "EST (New York)": "America/New_York",
#         "PST (Los Angeles)": "America/Los_Angeles",
#         "CET (Paris)": "Europe/Paris",
#         "JST (Tokyo)": "Asia/Tokyo"
#     }
    
#     def __init__(self):
#         self._is_24_hour_format = True
#         self._selected_timezone_key = "Local Time"
#         self._selected_timezone = None 
        
#         self._alarm_time = None 
#         self._alarm_set = False
#         self._alarm_triggered = False
#         self._just_triggered = False 

#         self._timer_total_seconds = 0
#         self._timer_remaining_seconds = 0
#         self._timer_running = False
#         self._timer_finished = False
#         self._timer_just_finished = False

#     def toggle_format(self):
#         """Toggles between 12-hour and 24-hour format."""
#         self._is_24_hour_format = not self._is_24_hour_format

#     def get_time_string(self):
#         """Returns the current time string based on the selected format and timezone."""
#         if self._selected_timezone:
#             try:
#                 tz = pytz.timezone(self._selected_timezone)
#                 now = datetime.datetime.now(tz)
#             except pytz.exceptions.UnknownTimeZoneError:
#                 now = datetime.datetime.now()
#         else:
#             now = datetime.datetime.now()

#         if self._is_24_hour_format:
#             time_str = now.strftime("%H:%M:%S")
#         else:
#             time_str = now.strftime("%I:%M:%S %p")
            
#         self.check_alarm(now)
        
#         return time_str

#     def get_alarm_status(self):
#         """Returns the status of the alarm."""
#         if self._alarm_triggered:
#             return "ALARM TRIGGERED!"
#         elif self._alarm_set:
#             alarm_str = self._alarm_time.strftime("%H:%M")
#             return f"Alarm Set: {alarm_str}"
#         else:
#             return "Alarm Off"

#     def check_alarm(self, current_datetime):
#         """Checks if the current time matches the set alarm time."""
#         self._just_triggered = False
#         if self._alarm_set and not self._alarm_triggered:
#             current_time = current_datetime.time()
#             if current_time.hour == self._alarm_time.hour and current_time.minute == self._alarm_time.minute:
#                 self._alarm_triggered = True
#                 self._just_triggered = True 
                
#     def set_alarm(self, hour, minute):
#         """Sets the alarm time."""
#         try:
#             self._alarm_time = datetime.time(hour, minute)
#             self._alarm_set = True
#             self._alarm_triggered = False
#         except ValueError:
#             pass

#     def clear_alarm(self):
#         """Clears the alarm."""
#         self._alarm_set = False
#         self._alarm_time = None
#         self._alarm_triggered = False
#         self._just_triggered = False

#     # --- Timer Methods ---

#     def set_timer(self, hours, minutes, seconds):
#         """Sets the timer duration in seconds."""
#         self._timer_total_seconds = hours * 3600 + minutes * 60 + seconds
#         self._timer_remaining_seconds = self._timer_total_seconds
#         self._timer_running = False
#         self._timer_finished = False
#         self._timer_just_finished = False

#     def start_timer(self):
#         """Starts the countdown timer."""
#         if self._timer_remaining_seconds > 0 and not self._timer_running:
#             self._timer_running = True
#             self._timer_finished = False
#             self._timer_just_finished = False

#     def stop_timer(self):
#         """Stops the countdown timer."""
#         self._timer_running = False

#     def reset_timer(self):
#         """Resets the timer to its initial duration."""
#         self._timer_remaining_seconds = self._timer_total_seconds
#         self._timer_running = False
#         self._timer_finished = False
#         self._timer_just_finished = False

#     def tick_timer(self):
#         """Decrements the timer by one second if running."""
#         self._timer_just_finished = False
#         if self._timer_running and self._timer_remaining_seconds > 0:
#             self._timer_remaining_seconds -= 1
#             if self._timer_remaining_seconds == 0:
#                 self._timer_running = False
#                 self._timer_finished = True
#                 self._timer_just_finished = True

#     def get_timer_string(self):
#         """Returns the remaining time as an HH:MM:SS string."""
#         seconds = self._timer_remaining_seconds
#         hours = seconds // 3600
#         minutes = (seconds % 3600) // 60
#         seconds = seconds % 60
#         return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

#     def get_timer_status(self):
#         """Returns the status of the timer."""
#         if self._timer_finished:
#             return "TIMER FINISHED!"
#         elif self._timer_running:
#             return "RUNNING"
#         elif self._timer_total_seconds > 0:
#             return "READY"
#         else:
#             return "OFF"

#     def get_timer_just_finished_status(self):
#         """Returns True if the timer just finished in this cycle."""
#         return self._timer_just_finished

#     def get_just_triggered_status(self):
#         """Returns True if the alarm was just triggered in this cycle."""
#         return self._just_triggered

#     def get_date_string(self):
#         """Returns the current date and day of the week string for the selected timezone."""
#         if self._selected_timezone:
#             try:
#                 tz = pytz.timezone(self._selected_timezone)
#                 now = datetime.datetime.now(tz)
#             except pytz.exceptions.UnknownTimeZoneError:
#                 now = datetime.datetime.now()
#         else:
#             now = datetime.datetime.now()
            
#         return now.strftime("%a, %b %d, %Y")

#     def get_format_status(self):
#         """Returns a string indicating the current format."""
#         return "24-Hour" if self._is_24_hour_format else "12-Hour"

#     def get_timezone_keys(self):
#         """Returns the display names of the available timezones."""
#         return list(self.COMMON_TIMEZONES.keys())

#     def get_selected_timezone_key(self):
#         """Returns the display name of the currently selected timezone."""
#         return self._selected_timezone_key

#     def set_timezone(self, tz_key):
#         """Sets the new timezone based on the display key."""
#         self._selected_timezone_key = tz_key
#         self._selected_timezone = self.COMMON_TIMEZONES.get(tz_key)

# # --- View ---
# class ClockView(tk.Tk):
    
#     def __init__(self, controller):
#         super().__init__()
#         # Store the controller reference
#         self.controller = controller
#         self.title("Digital Clock (MVC)")
#         self.geometry("600x500") 
#         self.configure(bg="#1c1c1c") 

#         # Style configuration 
#         style = ttk.Style(self)
#         style.theme_use('clam') 
#         style.configure("TLabel", background="#1c1c1c", foreground="#00ff00", font=("Consolas", 50, "bold")) 
#         style.configure("Date.TLabel", background="#1c1c1c", foreground="#00cc00", font=("Consolas", 18)) 
#         style.configure("TButton", font=("Helvetica", 10, "bold"), padding=5)
#         style.configure("TFrame", background="#1c1c1c")


#         # Time Label
#         self.time_label = ttk.Label(self, text="--:--:--", style="TLabel")
#         self.time_label.pack(pady=(10, 5))

#         # Time Zone Selection Frame
#         tz_frame = ttk.Frame(self, style="TFrame")
#         tz_frame.pack(pady=(0, 10))

#         # Time Zone Label
#         ttk.Label(tz_frame, text="Time Zone:", style="Date.TLabel").pack(side=tk.LEFT, padx=5)

#         # Time Zone Dropdown (Combobox) - Initialization only
#         self.tz_var = tk.StringVar(self)
#         self.tz_combobox = ttk.Combobox(tz_frame, textvariable=self.tz_var, state="readonly", width=20)
#         self.tz_combobox.pack(side=tk.LEFT, padx=5)

#         # Date Label
#         self.date_label = ttk.Label(self, text="---, --- --, ----", style="Date.TLabel")
#         self.date_label.pack(pady=(0, 5))

#         # Alarm Status Label 
#         self.alarm_status_label = ttk.Label(self, text="Alarm Off", style="Date.TLabel", foreground="#ff0000")
#         self.alarm_status_label.pack(pady=(5, 5))

#         # --- Timer Display --- 
#         self.timer_label = ttk.Label(self, text="00:00:00", style="TLabel", font=("Consolas", 36, "bold"))
#         self.timer_label.pack(pady=(10, 5))

#         # Timer Status Label 
#         self.timer_status_label = ttk.Label(self, text="Timer Off", style="Date.TLabel", foreground="#00cc00")
#         self.timer_status_label.pack(pady=(0, 10))

#         # --- Timer Controls Frame (CONTAINERS ONLY) --- 
#         self.timer_input_frame = ttk.Frame(self, style="TFrame")
#         self.timer_input_frame.pack(pady=(10, 5))
#         ttk.Label(self.timer_input_frame, text="Timer (HH:MM:SS):", style="Date.TLabel").pack(side=tk.LEFT, padx=5)
#         self.timer_hour_var = tk.StringVar(self, value="00")
#         self.timer_hour_entry = ttk.Entry(self.timer_input_frame, textvariable=self.timer_hour_var, width=3)
#         self.timer_hour_entry.pack(side=tk.LEFT)
#         ttk.Label(self.timer_input_frame, text=":", style="Date.TLabel").pack(side=tk.LEFT)
#         self.timer_minute_var = tk.StringVar(self, value="00")
#         self.timer_minute_entry = ttk.Entry(self.timer_input_frame, textvariable=self.timer_minute_var, width=3)
#         self.timer_minute_entry.pack(side=tk.LEFT)
#         ttk.Label(self.timer_input_frame, text=":", style="Date.TLabel").pack(side=tk.LEFT)
#         self.timer_second_var = tk.StringVar(self, value="00")
#         self.timer_second_entry = ttk.Entry(self.timer_input_frame, textvariable=self.timer_second_var, width=3)
#         self.timer_second_entry.pack(side=tk.LEFT)

#         # Timer Buttons Frame (CONTAINER ONLY)
#         self.timer_button_frame = ttk.Frame(self, style="TFrame")
#         self.timer_button_frame.pack(pady=(5, 10))
        
#         # Alarm Controls Frame (CONTAINERS ONLY)
#         self.alarm_frame = ttk.Frame(self, style="TFrame")
#         self.alarm_frame.pack(pady=(10, 10))
#         ttk.Label(self.alarm_frame, text="Alarm (HH:MM):", style="Date.TLabel").pack(side=tk.LEFT, padx=5)
#         self.alarm_hour_var = tk.StringVar(self, value="00")
#         self.alarm_hour_entry = ttk.Entry(self.alarm_frame, textvariable=self.alarm_hour_var, width=3)
#         self.alarm_hour_entry.pack(side=tk.LEFT)
#         ttk.Label(self.alarm_frame, text=":", style="Date.TLabel").pack(side=tk.LEFT)
#         self.alarm_minute_var = tk.StringVar(self, value="00")
#         self.alarm_minute_entry = ttk.Entry(self.alarm_frame, textvariable=self.alarm_minute_var, width=3)
#         self.alarm_minute_entry.pack(side=tk.LEFT)

#         # Status Label for format
#         self.status_label = ttk.Label(self, text="", style="Date.TLabel")
#         self.status_label.pack(pady=(5, 10))
        
#     def setup_controller_dependent_widgets(self):
#         """
#         Initializes ALL widgets (buttons, combobox bindings, etc.) that require a 
#         valid reference to self.controller.
#         """
#         # --- 1. Combobox Setup ---
#         self.tz_combobox['values'] = self.controller.get_timezone_keys()
#         self.tz_combobox.current(0)
#         self.tz_combobox.bind('<<ComboboxSelected>>', self.controller.timezone_selected_action)

#         # --- 2. Timer Buttons Setup ---
#         self.set_timer_button = ttk.Button(self.timer_button_frame, text="Set", command=self.controller.set_timer_action)
#         self.set_timer_button.pack(side=tk.LEFT, padx=5)
#         self.start_stop_timer_button = ttk.Button(self.timer_button_frame, text="Start", command=self.controller.start_stop_timer_action)
#         self.start_stop_timer_button.pack(side=tk.LEFT, padx=5)
#         self.reset_timer_button = ttk.Button(self.timer_button_frame, text="Reset", command=self.controller.reset_timer_action)
#         self.reset_timer_button.pack(side=tk.LEFT, padx=5)

#         # --- 3. Alarm Buttons Setup ---
#         self.set_alarm_button = ttk.Button(self.alarm_frame, text="Set Alarm", command=self.controller.set_alarm_action)
#         self.set_alarm_button.pack(side=tk.LEFT, padx=5)
#         self.clear_alarm_button = ttk.Button(self.alarm_frame, text="Clear Alarm", command=self.controller.clear_alarm_action)
#         self.clear_alarm_button.pack(side=tk.LEFT, padx=5)
        
#         # --- 4. Format Toggle Button Setup ---
#         self.format_button = ttk.Button(self, text="Toggle Format", command=self.controller.toggle_format_action)
#         self.format_button.pack(pady=(5, 0))


#     def update_display(self, time_str, date_str, format_status):
#         """Updates the time, date, and status labels."""
#         self.time_label.config(text=time_str)
#         self.date_label.config(text=date_str)
#         self.status_label.config(text=f"Format: {format_status} | Time Zone: {self.controller.get_selected_timezone_key()}")
        
#         # Update alarm status 
#         alarm_status = self.controller.get_alarm_status()
#         self.alarm_status_label.config(text=alarm_status)
#         if "TRIGGERED" in alarm_status:
#             current_color = self.time_label.cget("foreground")
#             new_color = "#ff0000" if current_color == "#00ff00" else "#00ff00"
#             self.time_label.config(foreground=new_color)
#         else:
#             self.time_label.config(foreground="#00ff00")

#         # Update timer display 
#         timer_str = self.controller.get_timer_string()
#         timer_status = self.controller.get_timer_status()
#         self.timer_label.config(text=timer_str)
#         self.timer_status_label.config(text=timer_status)
#         if "FINISHED" in timer_status:
#             current_color = self.timer_label.cget("foreground")
#             new_color = "#ff0000" if current_color == "#00ff00" else "#00ff00"
#             self.timer_label.config(foreground=new_color)
#             self.start_stop_timer_button.config(text="Start")
#         elif "RUNNING" in timer_status:
#             self.timer_label.config(foreground="#00ff00")
#             self.start_stop_timer_button.config(text="Stop")
#         else:
#             self.timer_label.config(foreground="#00ff00")
#             self.start_stop_timer_button.config(text="Start")

# # --- Controller ---
# class ClockController:
    
#     def __init__(self, model, view):
#         self.model = model
#         self.view = view
#         # self.update_clock() <--- REMOVED! It is now called manually later.

#     def update_clock(self):
#         """
#         Fetches the latest data from the Model and updates the View.
#         Schedules itself to run again after 1000ms (1 second).
#         """
#         self.model.tick_timer()

#         time_str = self.model.get_time_string()
#         date_str = self.model.get_date_string()
#         format_status = self.model.get_format_status()
        
#         self.view.update_display(time_str, date_str, format_status)

#         if self.model.get_just_triggered_status() or self.model.get_timer_just_finished_status():
#             os.system('echo -e "\a"')

#         self.view.after(1000, self.update_clock)

#     def toggle_format_action(self):
#         self.model.toggle_format()

#     def get_alarm_status(self):
#         return self.model.get_alarm_status()

#     def set_alarm_action(self):
#         try:
#             hour = int(self.view.alarm_hour_var.get())
#             minute = int(self.view.alarm_minute_var.get())
#             if 0 <= hour <= 23 and 0 <= minute <= 59:
#                 self.model.set_alarm(hour, minute)
#             else:
#                 print("Invalid time entered for alarm.")
#         except ValueError:
#             print("Please enter valid numbers for hour and minute.")

#     def clear_alarm_action(self):
#         self.model.clear_alarm()

#     def get_timer_string(self):
#         return self.model.get_timer_string()

#     def get_timer_status(self):
#         return self.model.get_timer_status()

#     def set_timer_action(self):
#         try:
#             hours = int(self.view.timer_hour_var.get())
#             minutes = int(self.view.timer_minute_var.get())
#             seconds = int(self.view.timer_second_var.get())
#             if 0 <= hours <= 99 and 0 <= minutes <= 59 and 0 <= seconds <= 59:
#                 self.model.set_timer(hours, minutes, seconds)
#             else:
#                 print("Invalid time entered for timer.")
#         except ValueError:
#             print("Please enter valid numbers for timer.")

#     def start_stop_timer_action(self):
#         status = self.model.get_timer_status()
#         if status == "RUNNING":
#             self.model.stop_timer()
#         elif status in ["READY", "TIMER FINISHED!"]:
#             self.model.start_timer()

#     def reset_timer_action(self):
#         self.model.reset_timer()

#     def get_timezone_keys(self):
#         return self.model.get_timezone_keys()

#     def get_selected_timezone_key(self):
#         return self.model.get_selected_timezone_key()

#     def timezone_selected_action(self, event):
#         selected_tz_key = self.view.tz_var.get()
#         self.model.set_timezone(selected_tz_key)

# # --- Application Entry Point (Corrected Instantiation) ---
# if __name__ == "__main__":
#     # 1. Create the Model
#     model = ClockModel()

#     # 2. Create the View (controller=None)
#     view = ClockView(controller=None) 

#     # 3. Create the Controller
#     controller = ClockController(model, view)

#     # 4. Set the final controller reference in the View
#     view.controller = controller
    
#     # 5. Run the setup that initializes all controller-dependent widgets (buttons/combobox)
#     view.setup_controller_dependent_widgets()

#     # 6. Manually start the clock update loop now that everything is linked and set up
#     controller.update_clock() 

#     # 7. Start the Tkinter event loop 
#     view.mainloop()