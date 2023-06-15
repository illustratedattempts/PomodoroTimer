from tkinter import *
from tkinter import ttk
from time import *
from threading import *


def convertToTime(time_num):
    num_minutes = time_num // 60
    num_seconds = time_num % 60
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
    return minutes * 60 + seconds


class PomoTimer:
    def __init__(self):
        self.running_thread = None
        self.semp_num = Semaphore(1)  # Used to synchronize functions RUN & RESET
        self.thread_event = Event()
        # Gives an error because we rely on having the start button first

        self.default_time = "00:10"
        self.timer_num = convertToNum(self.default_time)

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
        self.reset_btn = ttk.Button(self.bottom_frame, text="RESET", command=self.reset_timer)
        self.reset_btn.grid(row=0, column=0)

        self.run_btn = ttk.Button(self.bottom_frame, text="RUN", command=self.run_timer)
        self.run_btn.grid(row=0, column=1)

        self.pause_btn = ttk.Button(self.bottom_frame, text="PAUSE", command=self.pause_timer)
        self.pause_btn.grid(row=0, column=2)

    def reset_timer(self):
        self.semp_num.acquire()

        self.timer_num = convertToNum(self.default_time)
        self.timer.config(text=self.default_time)

        print("[RESET] Stopped Timer:", self.timer_num)

        self.semp_num.release()
        self.thread_event.clear()

    def run_timer(self):
        # Initialize Thread
        if not self.running_thread:
            self.running_thread = Thread(target=self.update_timer, daemon=True)
            print("[RUN] Thread created! :L")
            self.thread_event.set()  # By default, it is not set
            self.running_thread.start()
        else:
            if self.timer_num <= 0:  # The Update Thread will not check until after decrementing timer
                self.timer_num = convertToNum(self.default_time)
                self.timer.config(text=self.default_time)

            self.thread_event.set()
            print("[RUN] Letting the thread run again ;)")
        if self.running_thread and self.thread_event.is_set():
            print("[RUN] Thread is able to run! XD")

        # Is it set by default? Let's find out! >:D
        # self.thread_event.set()

    def update_timer(self):
        while True:  # Assumption: The thread SHOULD continue to exist
            self.thread_event.wait()

            # An alternative to using sleep()
            time_delay = 1
            start_time = time()
            while (time() - start_time) < time_delay:
                continue

            self.semp_num.acquire()

            # Addresses the case where the USER hits PAUSE just before as we are decrementing
            print("[UPDATE THREAD] Is it set?", self.thread_event.is_set())
            if not self.thread_event.is_set():  # To force another 1 sec delay after RUNNING again
                print("[UPDATE THREAD] System detected a pause right before decrementing")
                print("[UPDATE THREAD] Forcing an additional 1 sec delay")
                self.semp_num.release()  # Emulates end of loop
                continue

            self.timer_num -= 1

            print("[UPDATE THREAD] Running Timer:", self.timer_num)
            self.timer.config(text=convertToTime(self.timer_num))

            if self.timer_num <= 0:
                print("[UPDATE THREAD] Timer has reached the end")
                self.thread_event.clear()

            self.semp_num.release()

    def pause_timer(self):
        self.thread_event.clear()
        print("[PAUSE] Call for pause! :#")


if __name__ == "__main__":
    app = PomoTimer()
    app.run()
