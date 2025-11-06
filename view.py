import tkinter as tk
import math

class ClockView:

    def __init__(self, root, theme_colors):
        self.root = root
        self.theme = theme_colors
        self.root.title("Cellyusis CodeCamp - Digital Clock (MVC)")
        self.root.geometry("420x520")
        self.root.config(bg=self.theme["bg"])
        self.root.iconbitmap(r'C:\Users\miste\OneDrive\Desktop\TIME_CLOCK\images\clock_image.ico')

        self.school_label = tk.Label(root, text="CELLYUSIS CODECAMP",
                                     font=("Helvetica", 15, "bold"),
                                     fg=self.theme["fg"], bg=self.theme["bg"])
        self.school_label.pack(pady=8)
        self.canvas = tk.Canvas(root, width=420, height=420,
                                bg=self.theme["bg"], highlightthickness=0)
        self.canvas.pack()
        self.center_x, self.center_y, self.radius = 210, 210, 150
        self.draw_clock_face()
        self.date_label = tk.Label(root, font=("Helvetica", 13, "bold"),
                                   fg=self.theme["hr"], bg=self.theme["bg"])
        self.date_label.pack()
        self.time_label = tk.Label(root, font=("Helvetica", 13, "bold"),
                                   fg=self.theme["fg"], bg=self.theme["bg"])
        self.time_label.pack()
        self.toggle_button = tk.Button(root, text="Switch Theme",
                                       command=None,
                                       font=("Helvetica", 10),
                                       bg=self.theme["fg"], fg=self.theme["bg"])
        self.toggle_button.pack(pady=5)
        self.footer = tk.Label(root, text="Created by Pope | Computer Science Project",
                               font=("Helvetica", 10), fg="#aaaaaa", bg=self.theme["bg"])
        self.footer.pack(side="bottom", pady=5)

    def draw_clock_face(self):
        self.canvas.delete("face")
        self.canvas.create_oval(self.center_x - self.radius, self.center_y - self.radius,
                                self.center_x + self.radius, self.center_y + self.radius,
                                outline=self.theme["mark"], width=4, tags="face")
        for i in range(12):
            angle = math.radians(i * 30)
            x_outer = self.center_x + self.radius * 0.9 * math.sin(angle)
            y_outer = self.center_y - self.radius * 0.9 * math.cos(angle)
            x_inner = self.center_x + self.radius * 0.75 * math.sin(angle)
            y_inner = self.center_y - self.radius * 0.75 * math.cos(angle)
            self.canvas.create_line(x_inner, y_inner, x_outer, y_outer,
                                    fill=self.theme["mark"], width=3, tags="face")

    def draw_hands(self, hr_angle, min_angle, sec_angle):
        self.canvas.delete("hands")
        sec_len = self.radius * 0.9
        min_len = self.radius * 0.75
        hr_len = self.radius * 0.55
        x_sec = self.center_x + sec_len * math.sin(sec_angle)
        y_sec = self.center_y - sec_len * math.cos(sec_angle)
        x_min = self.center_x + min_len * math.sin(min_angle)
        y_min = self.center_y - min_len * math.cos(min_angle)
        x_hr = self.center_x + hr_len * math.sin(hr_angle)
        y_hr = self.center_y - hr_len * math.cos(hr_angle)
        self.canvas.create_line(self.center_x, self.center_y, x_hr, y_hr,
                                fill=self.theme["hr"], width=6, tags="hands")
        self.canvas.create_line(self.center_x, self.center_y, x_min, y_min,
                                fill=self.theme["min"], width=4, tags="hands")
        self.canvas.create_line(self.center_x, self.center_y, x_sec, y_sec,
                                fill=self.theme["sec"], width=2, tags="hands")
        self.canvas.create_oval(self.center_x - 8, self.center_y - 8,
                                self.center_x + 8, self.center_y + 8,
                                fill=self.theme["center"], outline="", tags="hands")

    def update_labels(self, date, digital_time):
        self.date_label.config(text=date)
        self.time_label.config(text=digital_time)

    def update_theme(self, new_theme):
        self.theme = new_theme
        self.root.config(bg=self.theme["bg"])
        self.canvas.config(bg=self.theme["bg"])
        self.school_label.config(fg=self.theme["fg"], bg=self.theme["bg"])
        self.date_label.config(fg=self.theme["hr"], bg=self.theme["bg"])
        self.time_label.config(fg=self.theme["fg"], bg=self.theme["bg"])
        self.toggle_button.config(bg=self.theme["fg"], fg=self.theme["bg"])
        self.footer.config(bg=self.theme["bg"])
        self.draw_clock_face()

   