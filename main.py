# main.py
import tkinter as tk
from models import ClockModel
from controller import ClockController
from view import ClockView
from splash import SplashScreen  # Make sure you save the previous splash class as splash.py

def start_main_app():
    """Creates the main app after splash screen closes."""
    # 1. Create the Model
    model = ClockModel()

    # 2. Create the Controller
    controller = ClockController(model)

    # 3. Create the Main View Window
    view = ClockView(controller)

    # 4. Set the View reference in the Controller
    controller.set_view(view)

    # 5. Manually start the clock update loop
    controller.update_clock()

    # 6. Start Tkinter main loop
    view.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root while splash shows

    # Splash screen with a 3-second duration
    splash = SplashScreen(root, duration=3000, image_path="DGIF.gif")

    # Schedule the main app to start after splash duration
    root.after(3000, lambda: [splash.destroy(), start_main_app()])

    root.mainloop()
