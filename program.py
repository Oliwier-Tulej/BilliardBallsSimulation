import tkinter as tk
from ball import *
import time

root = tk.Tk()

#window properties
root.title("Billiard balls simulation - Oliwier Tulej")
root.configure(background="yellow")
root.minsize(1200, 800)
root.maxsize(1200, 800)
root.geometry("900x600+700+400")

#frames
frameValues = tk.Frame(root, width=250, height=800, bg="red", highlightbackground="black", highlightthickness=1)
myCanvas = tk.Canvas(root, width=950, height=800, bg="SpringGreen4", highlightbackground="black", highlightthickness=1)

myCanvas.place(x=0, y=0, anchor="nw", width=950, height=800)
frameValues.place(x=950, y=0, anchor="nw", width=250, height=800)

#values
forceX = tk.StringVar()
forceX.set("0")
forceY = tk.StringVar()
forceY.set("0")
friction = tk.StringVar()
friction.set("0.4")
show_vectors = tk.BooleanVar(value=True)
show_speed = tk.BooleanVar(value=True)
last_time = time.perf_counter() 
fps_time = time.perf_counter()
isRunning = False
startingVector = None

#balls
f = 0.4
whiteBall = Ball(myCanvas, 475, 675, 40, 0, 0, f, "white")
yellowBall = Ball(myCanvas, 475, 265, 40, 0, 0, f, "yellow")
blueBall = Ball(myCanvas, 515, 195, 40, 0, 0, f, "blue")
redBall = Ball(myCanvas, 435, 195, 40, 0, 0, f, "red")
orangeBall = Ball(myCanvas, 555, 125, 40, 0, 0, f, "orange")
greenBall = Ball(myCanvas, 395, 125, 40, 0, 0, f, "lightgreen")
blackBall = Ball(myCanvas, 475, 125, 40, 0, 0, f, "black")

balls = [whiteBall, yellowBall, blueBall, redBall, orangeBall, greenBall, blackBall]

def get_inputs():
    global isRunning, startingVector
    if(isRunning==False):
        balls[0].setVelocity(int(forceX.get()), int(forceY.get()))
        for b in balls:
            b.friction = float(friction.get())
            b.show_vector = bool(show_vectors.get())
            b.show_speed = bool(show_speed.get())
        if(startingVector):
            myCanvas.delete(startingVector)
            startingVector = None
        isRunning = True

def resetBalls():
    positions = [(475, 675), (475, 265), (515, 195), (435, 195), (555, 125), (395, 125), (475, 125)]

    for b, (x,y) in zip(balls, positions):
        cx, cy = b.center()
        dx = x - cx
        dy = y - cy
        myCanvas.move(b.image, dx, dy)

        b.vx = 0
        b.vy = 0

        if b.vector_line:
            myCanvas.delete(b.vector_line)
            b.vector_line = None

    global isRunning
    isRunning = False
    drawStartingVector()

def drawStartingVector(*args):
    if(isRunning == False):
        fx = forceX.get()
        fy = forceY.get()

        global startingVector
        if(startingVector):
            myCanvas.delete(startingVector)
            startingVector = None

        cx, cy = balls[0].center()
        end_x = cx + int(fx) * 0.2
        end_y = cy + int(fy) * 0.2
        startingVector = myCanvas.create_line(
            cx, cy, end_x, end_y, 
            arrow="last", fill="red", width=2, arrowshape=(8, 10, 5)
        )
forceX.trace_add("write", drawStartingVector)
forceY.trace_add("write", drawStartingVector)

#input frame
tk.Label(frameValues, text="White Ball Velocity X").pack(pady=10, padx=30)
forceX_entry = tk.Scale(frameValues, from_=-2000, to=2000, orient="horizontal", length=200, variable=forceX)
forceX_entry.set(0)
forceX_entry.pack()
tk.Label(frameValues, text="White Ball Velocity Y").pack(pady=10, padx=30)
forceY_entry = tk.Scale(frameValues, from_=-2000, to=2000, orient="vertical", length=200, variable=forceY)
forceY_entry.set(0)
forceY_entry.pack()
tk.Label(frameValues, text="Friction").pack(pady=10, padx=30)
friction_entry = tk.Scale(frameValues, from_=0, to=1, resolution=0.01, orient="horizontal", length=200, variable=friction, digits=3)
friction_entry.set(0.4)
friction_entry.pack()
tk.Checkbutton(frameValues, text="Show Velocity Vectors", variable=show_vectors).pack(pady=10, padx=30)
tk.Checkbutton(frameValues, text="Show Speed", variable=show_speed).pack(pady=10, padx=30)

tk.Button(frameValues, text="Start", command=get_inputs, width=18).pack(pady=10, padx=30)

tk.Button(frameValues, text="Reset", command=resetBalls, width=18).pack(pady=10, padx=30)

#coordinate system
myCanvas.create_line(
            20, 20, 930, 20, 
            arrow="last", fill="black", width=2, arrowshape=(8, 10, 5)
        )
myCanvas.create_line(
            20, 20, 20, 780, 
            arrow="last", fill="black", width=2, arrowshape=(8, 10, 5)
        )
myCanvas.create_text(925, 35, text="X", fill="black", font=("Arial", 10, "bold"))
myCanvas.create_text(35, 775, text="Y", fill="black", font=("Arial", 10, "bold"))

#main loop
def animate():
    global last_time, frame_count, fps_time, startingVector

    #delta time
    now = time.perf_counter()
    dt = now - last_time
    last_time = now

    for b in balls:
        b.move(dt)

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].checkCollision(balls[j])

    root.after(1, animate)

resetBalls()
animate()
root.mainloop() 