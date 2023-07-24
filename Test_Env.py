import tkinter as tk
from tkinter import ttk

window = tk.Tk()
holder_val = tk.IntVar()
w = ttk.Spinbox(window, wrap=True, state="readonly", from_=0, to=59, increment=1,
                textvariable=holder_val)
w.pack()

label = tk.Label(window, text='')
label.pack()


def showSelected():
    label.config(text=holder_val.get())


btn = tk.Button(window, text="GET", command=showSelected)
btn.pack()
window.mainloop()
