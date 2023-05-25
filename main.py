from tkinter import *
from tkinter import ttk
import time
import threading


class PomoTimer:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("PomoTimer")
        self.window.geometry("500x500+500+300")

        # Outer Frame
        self.outer = ttk.Frame(self.window, padding=10)
        self.outer.grid()

        # Top-Inner Frame
        self.top_frame = ttk.Frame(self.outer, padding=5)
        self.top_frame.grid(row=0, column=0)

        # Bottom-Inner Frame
        self.bottom_frame = ttk.Frame(self.outer, padding=5)
        self.bottom_frame.grid(row=1, column=0)

        # Timer Label
        self.timer = ttk.Label(self.top_frame, padding=5, text="43")
        self.timer.pack()

        # Buttons
        self.reset = ttk.Button(self.bottom_frame, text="RESET")
        self.reset.grid(row=0, column=0)

        self.start = ttk.Button(self.bottom_frame, text="START", command=self.start_timer)
        self.start.grid(row=0, column=1)

        self.pause = ttk.Button(self.bottom_frame, text="PAUSE")
        self.pause.grid(row=0, column=2)

    def reset_timer(self):
        return

    def start_timer(self):
        set_time = self.timer.cget("text")
        running_thread = threading.Thread(target=self.update_timer, args=(set_time,))
        running_thread.start()

    def update_timer(self, set_time):
        num_time = int(set_time)
        while num_time:
            time.sleep(1)
            num_time -= 1
            self.timer.config(text=str(num_time))

    def pause_timer(self):
        return


if __name__ == "__main__":
    app = PomoTimer()
    app.run()
