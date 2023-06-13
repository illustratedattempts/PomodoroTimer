from tkinter import *
from tkinter import ttk
import time
import threading


def convertToTime(num_time):
    num_minutes = num_time // 60
    num_seconds = num_time % 60
    minutes = str(num_minutes)
    seconds = str(num_seconds)
    if num_minutes < 10:
        minutes = "0" + str(num_minutes)
    if num_seconds < 10:
        seconds = "0" + str(num_seconds)
    return minutes + ":" + seconds


def convertToNum(time_text):
    minutes = int(time_text[:2])
    seconds = int(time_text[3:])
    return minutes*60 + seconds


class PomoTimer:
    def __init__(self):
        self.running_thread = None
        self.semp_num = threading.Semaphore(1)  # Used to correctly synchronize the timer
        self.thread_event = threading.Event()

        self.reset_time = None  # Gives an error because we rely on having the start button first
        self.num_time = None
        self.default_time = "00:05"

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
        self.timer = ttk.Label(self.top_frame, padding=5, text=self.default_time)
        self.timer.pack()

        # Buttons
        self.reset = ttk.Button(self.bottom_frame, text="RESET", command=self.reset_timer)
        self.reset.grid(row=0, column=0)

        self.start_or_continue = ttk.Button(self.bottom_frame, text="START", command=self.start_or_continue_timer)
        self.start_or_continue.grid(row=0, column=1)

        self.pause = ttk.Button(self.bottom_frame, text="PAUSE", command=self.pause_timer)
        self.pause.grid(row=0, column=2)

    def reset_timer(self):
        self.semp_num.acquire()
        self.num_time = convertToNum(self.default_time)
        self.timer.config(text=convertToTime(self.num_time))
        self.start_or_continue.config(text="START")
        self.thread_event.clear()
        self.semp_num.release()
        # print("Num Time:", self.num_time)
        print("Does this still function?")

    def start_or_continue_timer(self):
        if self.running_thread:
            if self.num_time <= 0:
                self.num_time = convertToNum(self.default_time)
            self.thread_event.set()
            print(self.thread_event.is_set())
            print(self.running_thread)
            self.start_or_continue.config(text="CONTINUE")
        else:
            set_time = convertToNum(self.default_time)
            self.running_thread = threading.Thread(target=self.update_timer, args=(set_time,), daemon=True)
            self.thread_event.set()
            self.running_thread.start()
            self.start_or_continue.config(text="CONTINUE")

    def update_timer(self, set_time):
        self.reset_time = int(set_time)
        self.num_time = int(set_time)
        while self.num_time:
            time.sleep(1)
            self.thread_event.wait()
            self.semp_num.acquire()
            self.num_time -= 1
            self.semp_num.release()
            self.timer.config(text=convertToTime(self.num_time))
            if self.num_time <= 0:
                self.thread_event.clear()
                print(self.thread_event.is_set())
            # print("Num Time:", self.num_time)

    def pause_timer(self):
        self.thread_event.clear()
        print(self.thread_event.is_set())
        print("Timer should be paused")
        self.start_or_continue.config(text="CONTINUE")


if __name__ == "__main__":
    app = PomoTimer()
    app.run()
