# # clock_controller.py
# import os

# class ClockController:
    
#     def __init__(self, model):
#         self.model = model
#         self.view = None
        
#     def set_view(self, view):
#         """Sets the single main view reference."""
#         self.view = view
        
#     def show_page(self, page_name):
#         """Called by the navigation buttons to switch views."""
#         if self.view:
#             self.view.show_frame(page_name)

#     def update_clock(self):
#         """
#         Fetches the latest data from the Model and updates the View.
#         Schedules itself to run again after 1000ms (1 second).
#         """
#         self.model.tick_timer()

#         time_str = self.model.get_time_string()
#         date_str = self.model.get_date_string()
#         format_status = self.model.get_format_status()
        
#         if self.view:
#             self.view.update_displays({
#                 "time_str": time_str,
#                 "date_str": date_str,
#                 "format_status": format_status,
#                 "alarm_status": self.model.get_alarm_status(),
#                 "timer_str": self.model.get_timer_string(),
#                 "timer_status": self.model.get_timer_status(),
#                 "tz_key": self.model.get_selected_timezone_key()
#             })

#         if self.model.get_just_triggered_status() or self.model.get_timer_just_finished_status():
#             os.system('echo -e "\a"')

#         if self.view:
#             self.view.after(1000, self.update_clock)
            
#     # --- Action Methods ---
    
#     def toggle_format_action(self):
#         self.model.toggle_format()
        
#     def get_timezone_keys(self):
#         return self.model.get_timezone_keys()

#     def timezone_selected_action(self, event):
#         # Access the current_time_frame's tz_var via the main view's storage
#         selected_tz_key = self.view.frames["CurrentTime"].tz_var.get()
#         self.model.set_timezone(selected_tz_key)

#     def set_alarm_action(self):
#         try:
#             # Access the alarm_frame's input variables
#             alarm_frame = self.view.frames["Alarm"]
#             hour = int(alarm_frame.alarm_hour_var.get())
#             minute = int(alarm_frame.alarm_minute_var.get())
#             if 0 <= hour <= 23 and 0 <= minute <= 59:
#                 self.model.set_alarm(hour, minute)
#             else:
#                 print("Invalid time entered for alarm.")
#         except ValueError:
#             print("Please enter valid numbers for hour and minute.")

#     def clear_alarm_action(self):
#         self.model.clear_alarm()

#     def set_timer_action(self):
#         try:
#             # Access the timer_frame's input variables
#             timer_frame = self.view.frames["Timer"]
#             hours = int(timer_frame.timer_hour_var.get())
#             minutes = int(timer_frame.timer_minute_var.get())
#             seconds = int(timer_frame.timer_second_var.get())
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


# clock_controller.py
import os
from tkinter import messagebox


class ClockController:
    
    def __init__(self, model):
        self.model = model
        self.view = None
        
    def set_view(self, view):
        """Sets the single main view reference."""
        self.view = view
        
    def update_clock(self):
        # ... (rest of the method is the same)
        self.model.tick_timer()

        time_str = self.model.get_time_string()
        date_str = self.model.get_date_string()
        format_status = self.model.get_format_status()
        
        if self.view:
            self.view.update_displays({
                "time_str": time_str,
                "date_str": date_str,
                "format_status": format_status,
                "alarm_status": self.model.get_alarm_status(),
                "timer_str": self.model.get_timer_string(),
                "timer_status": self.model.get_timer_status(),
                "tz_key": self.model.get_selected_timezone_key()
            })

        if self.model.get_just_triggered_status() or self.model.get_timer_just_finished_status():
            os.system('echo -e "\a"')

        if self.view:
            self.view.after(1000, self.update_clock)
            
    # --- Data Retrieval Methods (The FIX is here) ---
    def get_timezone_keys(self):
        """Fetches the available timezone keys from the Model."""
        return self.model.get_timezone_keys()

    # --- Action Methods ---
    
    def toggle_format_action(self):
        self.model.toggle_format()
        
    def timezone_selected_action(self, event):
        # Access the current_time_frame's tz_var via the main view's storage
        # Note: The view needs to be updated if you changed the internal frame keys from "CurrentTime" to "Time"
        selected_tz_key = self.view.frames["Time"].tz_var.get()
        self.model.set_timezone(selected_tz_key)

    def set_alarm_action(self):
        alarm_frame = self.view.frames["Alarm"]
    
        hour_raw = alarm_frame.alarm_hour_var.get().strip()
        minute_raw = alarm_frame.alarm_minute_var.get().strip()

    # Validate numeric first
        if not (hour_raw.isdigit() and minute_raw.isdigit()):
            messagebox.showerror("Invalid Input", "Alarm time must contain only digits.")
            alarm_frame.alarm_hour_var.set("00")
            alarm_frame.alarm_minute_var.set("00")
            return

        hour = int(hour_raw)
        minute = int(minute_raw)

    # Validate ranges
        if not (0 <= hour <= 23):
            messagebox.showerror("Invalid Hour", "Hour must be between 00 and 23.")
            alarm_frame.alarm_hour_var.set("00")
            return

        if not (0 <= minute <= 59):
            messagebox.showerror("Invalid Minute", "Minutes must be between 00 and 59.")
            alarm_frame.alarm_minute_var.set("00")
            return

    # Passed validation → set alarm
        self.model.set_alarm(hour, minute)


    def clear_alarm_action(self):
        alarm_frame = self.view.frames["Alarm"]
        self.model.clear_alarm()

    # Reset UI fields
        alarm_frame.alarm_hour_var.set("00")
        alarm_frame.alarm_minute_var.set("00")

       

    def set_timer_action(self):
        timer_frame = self.view.frames["Timer"]

        h_raw = timer_frame.timer_hour_var.get().strip()
        m_raw = timer_frame.timer_minute_var.get().strip()
        s_raw = timer_frame.timer_second_var.get().strip()

    # Validate numeric
        if not (h_raw.isdigit() and m_raw.isdigit() and s_raw.isdigit()):
            messagebox.showerror("Invalid Input", "Timer fields must contain digits only.")
            timer_frame.timer_hour_var.set("00")
            timer_frame.timer_minute_var.set("00")
            timer_frame.timer_second_var.set("00")
            return

        hours = int(h_raw)
        minutes = int(m_raw)
        seconds = int(s_raw)

    # Range validation
        if not (0 <= hours <= 99):
            messagebox.showerror("Invalid Hours", "Hours must be between 00 and 99.")
            timer_frame.timer_hour_var.set("00")
            return

        if not (0 <= minutes <= 59):
            messagebox.showerror("Invalid Minutes", "Minutes must be between 00 and 59.")
            timer_frame.timer_minute_var.set("00")
            return

        if not (0 <= seconds <= 59):
            messagebox.showerror("Invalid Seconds", "Seconds must be between 00 and 59.")
            timer_frame.timer_second_var.set("00")
            return

    # Valid → set timer
        self.model.set_timer(hours, minutes, seconds)


    def start_stop_timer_action(self):
        status = self.model.get_timer_status()
        if status == "RUNNING":
            self.model.stop_timer()
        elif status in ["READY", "TIMER FINISHED!"]:
            self.model.start_timer()

    def reset_timer_action(self):
        timer_frame = self.view.frames["Timer"]
        self.model.reset_timer()

    # Reset UI
        timer_frame.timer_hour_var.set("00")
        timer_frame.timer_minute_var.set("00")
        timer_frame.timer_second_var.set("00")
