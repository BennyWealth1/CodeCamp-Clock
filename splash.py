
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class SplashScreen(tk.Toplevel):
    def __init__(self, parent, duration=3000, image_path=None):
        super().__init__(parent)
        self.duration = duration
        self.overrideredirect(True)
        self.configure(bg="#2b2b2b")
        self.geometry("400x250+500+300")
        self.progress_value = 0.0

        # Icon Image
        self.icon_label = None
        if image_path:
            try:
                img = Image.open(image_path)
                img = img.resize((400, 240), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.icon_label = tk.Label(self, image=self.photo, bg="#2b2b2b")
                self.icon_label.pack(pady=10)
            except Exception as e:
                print("Splash image could not load:", e)

        # Loading text
        tk.Label(self, text="⏱ Loading Clock App...", font=("Helvetica", 16, "bold"),
                 fg="#00ff00", bg="#2b2b2b").pack(pady=(0, 10))

        # Canvas-based Progress Bar
        self.canvas = tk.Canvas(self, width=300, height=20, bg="#1c1c1c", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.progress_rect = self.canvas.create_rectangle(0, 0, 0, 20, fill="#00ff00", width=0)

        # Percentage label
        self.percent_label = tk.Label(self, text="0%", font=("Helvetica", 12),
                                      fg="#00ff00", bg="#2b2b2b")
        self.percent_label.pack()

        # Progress parameters
        self.max_steps = 100
        self.step_duration = self.duration / self.max_steps
        self.increment = 0.5

        # Fade-in
        self.attributes("-alpha", 0.0)
        self.fade_in_step = 0.02
        self.after(0, self.fade_in)

        # Bounce parameters
        self.bounce_direction = 1
        self.bounce_max = 10  # pixels
        self.bounce_speed = 3  # pixels per frame

        # Start updates
        self.after(10, self.update_progress)
        if self.icon_label:
            self.after(10, self.bounce_icon)

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1.0:
            alpha = min(alpha + self.fade_in_step, 1.0)
            self.attributes("-alpha", alpha)
            self.after(30, self.fade_in)

    def update_progress(self):
        if self.progress_value < self.max_steps:
            self.progress_value += self.increment
            if self.progress_value > self.max_steps:
                self.progress_value = self.max_steps

            # Update progress bar width
            bar_width = (self.progress_value / self.max_steps) * 300
            self.canvas.coords(self.progress_rect, 0, 0, bar_width, 20)

            # Dynamic gradient color
            green = max(0, 255 - int(self.progress_value * 2.5))
            red = min(255, int(self.progress_value * 2.5))
            color = f'#{red:02x}{green:02x}00'
            self.canvas.itemconfig(self.progress_rect, fill=color)
            self.percent_label.config(text=f"{int(self.progress_value)}%", fg=color)

            self.after(int(self.step_duration / self.increment), self.update_progress)
        else:
            self.destroy()

    def bounce_icon(self):
        if self.icon_label:
            # Get current y-position
            y = self.icon_label.winfo_y()
            # Move up/down
            if y <= 10:
                self.bounce_direction = 1
            elif y >= 10 + self.bounce_max:
                self.bounce_direction = -1
            self.icon_label.place_configure(y=y + self.bounce_direction * self.bounce_speed)
            self.after(50, self.bounce_icon)
