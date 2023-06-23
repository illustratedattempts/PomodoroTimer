import tkinter as tk
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


class SettingsWindow:
    # Alive Variable attributes need to be implemented only when you want to close it a second way
    def __init__(self):
        self.settings = tk.Toplevel()
        self._setup_settings_window()

        # grab_set() function invokes MODAL mode.
        # Guarantees that the user can not create new Settings Windows
        self.settings.grab_set()

    def _setup_settings_window(self):
        self.settings.config(width=300, height=200)
        self.settings.geometry("300x200+600+400")
        self.settings.title("Settings")

        self.pomo_label = ttk.Label(self.settings, text="Timer")
        self.pomo_label.pack()

        self.timer_frame = ttk.Frame(self.settings, padding=5)
        self.timer_frame.pack()

        self.timer_digit1 = ["0", "1", "2", "3", "4", "5"]
        self.timer_digit2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.chosen_min_dig1 = tk.IntVar()
        self.min_digit1 = ttk.Combobox(self.timer_frame, textvariable=self.chosen_min_dig1, state="readonly", values=self.timer_digit1)
        self.min_digit1.current(0)
        self.min_digit1.bind('<<ComboboxSelected>>', self.test)
        self.min_digit1.grid(row=0, column=0)

        self.chosen_min_dig2 = tk.IntVar()
        self.min_digit2 = ttk.Combobox(self.timer_frame, textvariable=self.chosen_min_dig2, state="readonly", values=self.timer_digit2)
        self.min_digit2.current(0)
        self.min_digit2.bind('<<ComboboxSelected>>', self.test)
        self.min_digit2.grid(row=0, column=1)

    def test(self, event):
        print("ComboBox1 Selected:", self.chosen_min_dig1.get())
        print("ComboBox2 Selected:", self.chosen_min_dig2.get())



class PomoTimer:
    def __init__(self):
        self.running_thread = None
        self.semp_num = Semaphore(1)  # Used to synchronize functions RUN & RESET
        self.thread_event = Event()
        # Gives an error because we rely on having the start button first

        self.default_time = "00:10"
        self.timer_num = convertToNum(self.default_time)

        self.window = tk.Tk()
        self._setup_main_window()

        self.settings_window = None

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("PomoTimer")
        self.window.geometry("300x200+500+300")

        # Define Min Size behavior -- for now
        self.window.minsize(230, 100)

        # Outer Frame
        self.outer = ttk.Frame(self.window, padding=10)
        self.outer.place(in_=self.window, anchor="c", relx=.5, rely=.5)

        # Top-Inner Frame
        self.top_frame = ttk.Frame(self.outer, padding=5)
        self.top_frame.grid(row=0, column=0)

        # Bottom-Inner Frame
        self.bottom_frame = ttk.Frame(self.outer, padding=5)
        self.bottom_frame.grid(row=1, column=0)

        # Timer Label
        self.timer = ttk.Label(self.top_frame, padding=5, text=self.default_time)
        self.timer.pack()

        # Settings Button
        self.setting_btn = ttk.Button(self.top_frame, text="SETTINGS", command=self.open_settings)
        self.setting_btn.pack()

        # Manipulate Timer Buttons
        self.reset_btn = ttk.Button(self.bottom_frame, text="RESET", command=self.reset_timer)
        self.reset_btn.grid(row=0, column=0)

        self.run_btn = ttk.Button(self.bottom_frame, text="RUN", command=self.run_timer)
        self.run_btn.grid(row=0, column=1)

        self.pause_btn = ttk.Button(self.bottom_frame, text="PAUSE", command=self.pause_timer)
        self.pause_btn.grid(row=0, column=2)

    # Widget Callback Functions Below
    def open_settings(self):
        self.settings_window = SettingsWindow()

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
