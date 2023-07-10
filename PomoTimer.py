import sys
import tkinter as tk
from tkinter import ttk
from time import *
from threading import *

from SettingWindows import SettingsWindow


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
        self.semp_time = Semaphore(1)  # Used to synchronize functions that manipulate the timer
        self.thread_event = Event()
        # Gives an error because we rely on having the start button first

        self.pomo_time = "00:25"
        self.lbreak_time = "00:15"
        self.sbreak_time = "00:05"

        self.elapsed_time = 0

        self.timer_num = convertToNum(self.pomo_time)
        self.curr_timer_type = "Pomodoro"  # May not be useful -- only for labeling
        # Pomodoro, LongBreak, ShortBreak

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
        self.outer.place(in_=self.window, anchor="center", relx=.5, rely=.5)

        # Top-Inner Frame
        self.top_frame = ttk.Frame(self.outer, padding=5)
        self.top_frame.grid(row=0, column=0)

        # Middle-Inner Frame
        self.middle_frame = ttk.Frame(self.outer, padding=5)
        self.middle_frame.grid(row=1, column=0)

        # Bottom-Inner Frame
        self.bottom_frame = ttk.Frame(self.outer, padding=5)
        self.bottom_frame.grid(row=2, column=0)

        # Different Timer Type Buttons
        self.pomo_btn = ttk.Button(self.top_frame, text="POMODORO", command=self.diff_timer_pomo)
        self.pomo_btn.grid(row=0, column=0)

        self.long_break_btn = ttk.Button(self.top_frame, text="LONG BREAK", command=self.diff_timer_long)
        self.long_break_btn.grid(row=0, column=1)

        self.short_break_btn = ttk.Button(self.top_frame, text="SHORT BREAK", command=self.diff_timer_short)
        self.short_break_btn.grid(row=0, column=2)

        # Timer Label
        self.timer = ttk.Label(self.middle_frame, padding=5, text=self.pomo_time)
        self.timer.pack()

        # Settings Button
        self.setting_btn = ttk.Button(self.middle_frame, text="SETTINGS", command=self.open_settings)
        self.setting_btn.pack()

        # Manipulate Timer Buttons
        self.reset_btn = ttk.Button(self.bottom_frame, text="RESET", command=self.reset_timer)
        self.reset_btn.grid(row=0, column=0)

        self.run_btn = ttk.Button(self.bottom_frame, text="RUN", command=self.run_timer)
        self.run_btn.grid(row=0, column=1)

        self.pause_btn = ttk.Button(self.bottom_frame, text="PAUSE", command=self.pause_timer)
        self.pause_btn.grid(row=0, column=2)

    # Widget Callback Functions Below

    # Changing Timer Type Functions
    # These are intended to pause execution and then change the timer
    # The Semaphore is assumed to be released -- potential deadlock could happen here
    # Might need a Semaphore for adjusting timer type
    def diff_timer_pomo(self):
        if self.curr_timer_type != "Pomodoro":
            print("[CHANGE TYPE] Type changed to: Pomodoro")
            self.thread_event.clear()

            self.curr_timer_type = "Pomodoro"

            self.semp_time.acquire()
            self.manip_timer(time_type="Pomodoro")
            self.semp_time.release()
        else:
            print("[CHANGE TYPE] Attempted to change to POMODORO but already in state")

    def diff_timer_long(self):
        if self.curr_timer_type != "Long Break":
            print("[CHANGE TYPE] Type changed to: Long Break")
            self.thread_event.clear()

            self.curr_timer_type = "Long Break"

            self.semp_time.acquire()
            self.manip_timer(time_type="Long Break")
            self.semp_time.release()
        else:
            print("[CHANGE TYPE] Attempted to change to LONG BREAK but already in state")

    def diff_timer_short(self):
        if self.curr_timer_type != "Short Break":
            print("[CHANGE TYPE] Type changed to: Short Break")
            self.thread_event.clear()

            self.curr_timer_type = "Short Break"

            self.semp_time.acquire()
            self.manip_timer(time_type="Short Break")
            self.semp_time.release()
        else:
            print("[CHANGE TYPE] Attempted to change to SHORT BREAK but already in state")

    def reset_timer(self):
        self.semp_time.acquire()

        self.elapsed_time = 0
        self.manip_timer(time_type=self.curr_timer_type)
        print("[RESET] Stopped Timer:", self.timer_num)

        self.semp_time.release()
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
                self.manip_timer(time_type=self.curr_timer_type)

            self.thread_event.set()
            print("[RUN] Letting the thread run again ;)")
        if self.running_thread and self.thread_event.is_set():
            print("[RUN] Thread is able to run! XD")

    def update_timer(self):
        while True:  # Assumption: The thread SHOULD continue to exist
            self.thread_event.wait()

            # An alternative to using sleep()
            time_delay = 1
            start_time = time()
            while (time() - start_time) < time_delay:
                continue

            self.semp_time.acquire()

            # Addresses the case where the USER hits PAUSE just before as we are decrementing
            print("[UPDATE THREAD] Is it set?", self.thread_event.is_set())
            if not self.thread_event.is_set():  # To force another 1 sec delay after RUNNING again
                print("[UPDATE THREAD] System detected a pause right before decrementing")
                print("[UPDATE THREAD] Forcing an additional 1 sec delay (if applicable)")
                self.semp_time.release()  # Emulates end of loop
                continue

            self.elapsed_time = self.elapsed_time + 1
            self.timer_num -= 1

            print("[UPDATE THREAD] Running Timer:", self.timer_num)
            self.timer.config(text=convertToTime(self.timer_num))

            if self.timer_num <= 0:
                print("[UPDATE THREAD] Timer has reached the end")
                self.elapsed_time = 0
                self.thread_event.clear()

            self.semp_time.release()

    def pause_timer(self):
        self.thread_event.clear()
        print("[PAUSE] Call for pause! :#")

    # Settings Window Below:
    def open_settings(self):
        print("[SETTINGS] Invoking Window Opening")
        # Just in case the modal focus mode fails
        if not SettingsWindow.window_exist:
            self.settings_window = SettingsWindow(pomo_time=self.pomo_time, lbreak_time=self.lbreak_time,
                                                  sbreak_time=self.sbreak_time, change_func=self.invoke_changes)

            print("[SETTINGS] New Window Opened")
        else:
            print("[SETTINGS] Window Already Exists, Only One Window May Exist")

    # For the Settings' Window
    # For now assume that the timer is NOT running
    def invoke_changes(self, new_pomo_time, new_lbreak_time, new_sbreak_time):
        # self.default_time = new_time
        # self.timer_num = convertToNum(new_time)
        print("[SETTINGS -> MAIN] Timer Settings has Invoked Changes to Timer Types Values")

        any_curr_changes = False

        # Makes sure that only NEW times get changed and that we call manip timer only when it's the current timer
        if not self.pomo_time == new_pomo_time:
            if self.curr_timer_type == "Pomodoro":
                any_curr_changes = True
            self.pomo_time = new_pomo_time

        if not self.lbreak_time == new_lbreak_time:
            if self.curr_timer_type == "Long Break":
                any_curr_changes = True
            self.lbreak_time = new_lbreak_time

        if not self.sbreak_time == new_sbreak_time:
            if self.curr_timer_type == "Short Break":
                any_curr_changes = True
            self.sbreak_time = new_sbreak_time

        # Pushes any relevant changes to the GUI thread
        if any_curr_changes:
            self.semp_time.acquire()
            self.manip_timer(self.curr_timer_type)
            self.semp_time.release()

    # Assumes that calling block will be surrounded by semaphores...scary
    # It may be that when the elapsed time changes, that if it greater than the time than it will be 0:00 or less than 0 which should not happen
    # Solution: Use the flag and set the time to 0:00
    def manip_timer(self, time_type="Pomodoro"):
        if time_type == "Pomodoro":
            self.timer_num = convertToNum(self.pomo_time) - self.elapsed_time
            print("[MANIP] Elapsed Time:", self.elapsed_time)
            if self.timer_num <= 0:
                print("[UPDATE THREAD] Timer has reached the end")
                self.thread_event.clear()
                self.elapsed_time = 0
                self.timer.config(text=convertToTime(0))
            else:
                self.timer.config(text=convertToTime(self.timer_num))
        elif time_type == "Long Break":
            self.timer_num = convertToNum(self.lbreak_time) - self.elapsed_time
            if self.timer_num <= 0:
                print("[UPDATE THREAD] Timer has reached the end")
                self.thread_event.clear()
                self.elapsed_time = 0
                self.timer.config(text=convertToTime(0))
            else:
                self.timer.config(text=convertToTime(self.timer_num))
        elif time_type == "Short Break":
            self.timer_num = convertToNum(self.sbreak_time) - self.elapsed_time
            if self.timer_num <= 0:
                print("[UPDATE THREAD] Timer has reached the end")
                self.thread_event.clear()
                self.elapsed_time = 0
                self.timer.config(text=convertToTime(0))
            else:
                self.timer.config(text=convertToTime(self.timer_num))


def main():
    app = PomoTimer()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
