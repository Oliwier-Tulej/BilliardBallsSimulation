import tkinter as tk

root = tk.Tk()

# Window properties
root.title("Symulacja kuli billardowych")
root.configure(background="yellow")
root.minsize(1200, 800)
root.maxsize(1200, 800)
root.geometry("900x600+700+400")

# Frames
frameValues = tk.Frame(root, width=250, height=800, bg="red")
frameSimulation = tk.Frame(root, width=950, height=800, bg="white")

frameValues.place(x=0, y=0, anchor="nw", width=250, height=800)
frameSimulation.place(x=250, y=0, anchor="nw", width=950, height=800)


def get_inputs():
    value1 = value1_entry.get()
    value2 = value2_entry.get()
    tk.Label(frameSimulation, text=value1 + " " + value2).pack()

tk.Label(frameValues, text="Wartosc 1").pack()
value1_entry = tk.Entry(frameValues)
value1_entry.pack()
tk.Label(frameValues, text="Wartosc 2").pack()
value2_entry = tk.Entry(frameValues)
value2_entry.pack()

tk.Button(frameValues, text="Enter", command=get_inputs, width=18).pack(pady=10, padx=30)

root.mainloop() 