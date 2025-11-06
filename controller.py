import tkinter as tk
from models import ClockModel
from view import ClockView

class ClockController:
    def __init__(self, root):
        self.model = ClockModel()
        self.current_theme = "dark"
        self.view = ClockView(root, self.model.themes[self.current_theme])
        self.view.toggle_button.config(command=self.toggle_theme)
        self.update_clock()

    def update_clock(self):
        time_data = self.model.get_time()
        hr_angle, min_angle, sec_angle = self.model.get_hand_angles(
            time_data["hour"], time_data["minute"], time_data["second"]
        )
        self.view.draw_hands(hr_angle, min_angle, sec_angle)
        self.view.update_labels(time_data["date"], time_data["digital"])
        self.view.root.after(1000, self.update_clock)

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.view.update_theme(self.model.themes[self.current_theme])

if __name__ == "__main__":
    root = tk.Tk()
    app = ClockController(root)
    root.mainloop()
