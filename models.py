import time
import math

class ClockModel:
    def __init__(self):
        self.radius = 150
        self.themes = {
            "dark": {
                "bg": "#1e1e2f",
                "fg": "#00ffcc",
                "mark": "#00ffcc",
                "hr": "#ffffff",
                "min": "#00ffff",
                "sec": "#ff0000",
                "center": "#00ffcc"
            },
            "light": {
                "bg": "#f4f4f4",
                "fg": "#007acc",
                "mark": "#007acc",
                "hr": "#000000",
                "min": "#007acc",
                "sec": "#ff3333",
                "center": "#007acc"
            }
        }

    def get_time(self):
        t = time.localtime()
        return {
            "hour": t.tm_hour % 12,
            "minute": t.tm_min,
            "second": t.tm_sec,
            "date": time.strftime("%A, %d %B %Y"),
            "digital": time.strftime("%I:%M:%S %p")
        }

    def get_hand_angles(self, hour, minute, second):
        sec_angle = math.radians(second * 6)
        min_angle = math.radians(minute * 6 + second * 0.1)
        hr_angle = math.radians(hour * 30 + minute * 0.5)
        return hr_angle, min_angle, sec_angle
