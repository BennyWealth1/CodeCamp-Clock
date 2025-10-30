
import tkinter as tk
import time
import math


#This is the main window
root = tk.Tk()
root.title("Analog Clock")
root.geometry("400x400")
#root.sizeable(False, False)
root.configure(bg="#1e1e2f")

#This is the canvas where the clock will be drawn
canvas = tk.Canvas(root, width=400, height=400, bg="#1e1e2f", highlightthickness=0)
canvas.pack()   
center_x = 200
center_y = 200      
radius = 150

#Clock Outline

canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="#ffffff", width=4)

#This covers hour marks
for i in range(12):
    angle = math.radians(i * 30)
    x_start = center_x + (radius - 10) * math.cos(angle)
    y_start = center_y + (radius - 10) * math.sin(angle)
    x_end = center_x + radius * math.cos(angle)
    y_end = center_y + radius * math.sin(angle)
    canvas.create_line(x_start, y_start, x_end, y_end, fill="#ffffff", width=3) 

date_label = tk.Label(root, text=" ", font=("Helvetica", 13, "bold"), fg="#ffffff", bg="#1e1e2f")
date_label.pack()
time.label = tk.Label(root, text=" ", font=("Helvetica", 13, "bold"), fg="#c03c3c", bg="#1e1e2f")
time.label.pack()


