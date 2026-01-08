import tkinter as tk
from ball import *
import time

root = tk.Tk()

# Window properties
root.title("Symulacja kuli billardowych")
root.configure(background="yellow")
root.minsize(1200, 800)
root.maxsize(1200, 800)
root.geometry("900x600+700+400")

# Frames
frameValues = tk.Frame(root, width=250, height=800, bg="red")
myCanvas = tk.Canvas(root, width=950, height=800, bg="SpringGreen4")

myCanvas.place(x=0, y=0, anchor="nw", width=950, height=800)
frameValues.place(x=950, y=0, anchor="nw", width=250, height=800)

# Values
value1, value2 = 1, 1
last_time = time.perf_counter()
fps_time = time.perf_counter()

# Input frame
def get_inputs():
    global value1, value2
    value1 = value1_entry.get()
    value2 = value2_entry.get()

tk.Label(frameValues, text="Wartosc 1").pack()
value1_entry = tk.Entry(frameValues)
value1_entry.pack()
tk.Label(frameValues, text="Wartosc 2").pack()
value2_entry = tk.Entry(frameValues)
value2_entry.pack()

tk.Button(frameValues, text="Enter", command=get_inputs, width=18).pack(pady=10, padx=30)

# Balls
whiteBall = Ball(myCanvas, 100, 100, 40, 500, 500, 0.4, "white")

def animate():
    global last_time, frame_count, fps_time

    now = time.perf_counter()
    dt = now - last_time
    last_time = now

    whiteBall.move(dt)
    root.after(1, animate)

animate()
root.mainloop() 