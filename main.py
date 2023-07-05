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
    # Alive Variable attributes: Changing the timer while it is running?
    def __init__(self, default_time, change_func):
        self.apply_changes = change_func

        self.settings = tk.Toplevel()
        self._setup_settings_win(default_time)

        # grab_set() function invokes MODAL mode.
        # Guarantees that the user can not create new Settings Windows
        self.settings.grab_set()

    def _setup_settings_win(self, initial_time):
        self.settings.config(width=300, height=200)
        self.settings.geometry("300x200+600+400")
        self.settings.title("Settings")

        self.pomo_label = ttk.Label(self.settings, text="Pomodoro Timer")
        self.pomo_label.pack()

        self.timer_frame = ttk.Frame(self.settings, padding=10)
        self.timer_frame.pack()

        # For Combobox Values that represents digits of time
        self.timer_digit1 = ["0", "1", "2", "3", "4", "5"]
        self.timer_digit2 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        # Min Tens Digit
        self.chosen_min_dig1 = tk.IntVar()
        self.min_digit1 = ttk.Combobox(self.timer_frame, textvariable=self.chosen_min_dig1, state="readonly",
                                       values=self.timer_digit1)
        self.min_digit1.current(int(initial_time[0]))
        self.min_digit1.bind('<<ComboboxSelected>>', self.pomo_debug_show)
        self.min_digit1.grid(row=0, column=0)

        # Min Ones Digit
        self.chosen_min_dig2 = tk.IntVar()
        self.min_digit2 = ttk.Combobox(self.timer_frame, textvariable=self.chosen_min_dig2, state="readonly",
                                       values=self.timer_digit2)
        self.min_digit2.current(int(initial_time[1]))
        self.min_digit2.bind('<<ComboboxSelected>>', self.pomo_debug_show)
        self.min_digit2.grid(row=0, column=1)

        # Colon In Between
        self.time_colons = ttk.Label(self.timer_frame, text=":")
        self.time_colons.grid(row=0, column=2)

        # Second Tens Digit
        self.chosen_sec_dig1 = tk.IntVar()
        self.sec_digit1 = ttk.Combobox(self.timer_frame, textvariable=self.chosen_sec_dig1, state="readonly",
                                       values=self.timer_digit1)
        self.sec_digit1.current(int(initial_time[3]))
        self.sec_digit1.bind('<<ComboboxSelected>>', self.pomo_debug_show)
        self.sec_digit1.grid(row=0, column=3)

        # Second Ones Digit
        self.chosen_sec_dig2 = tk.IntVar()
        self.sec_digit1 = ttk.Combobox(self.timer_frame, textvariable=self.chosen_sec_dig2, state="readonly",
                                       values=self.timer_digit2)
        self.sec_digit1.current(int(initial_time[4]))
        self.sec_digit1.bind('<<ComboboxSelected>>', self.pomo_debug_show)
        self.sec_digit1.grid(row=0, column=4)

        # Readjust Weight Values of Columns for Even-ness
        self.timer_frame.grid_columnconfigure(0, weight=1)
        self.timer_frame.grid_columnconfigure(1, weight=1)
        # self.timer_frame.grid_columnconfigure(2, weight=1)
        self.timer_frame.grid_columnconfigure(3, weight=1)
        self.timer_frame.grid_columnconfigure(4, weight=1)

        self.submit_btn = ttk.Button(self.settings, text="Submit Stuff", command=self.settings_finished)
        self.submit_btn.pack()

    def settings_finished(self):
        self.apply_changes(
            str(self.chosen_min_dig1.get()) + str(self.chosen_min_dig2.get()) + ":" + str(self.chosen_sec_dig1.get()) +
            str(self.chosen_sec_dig2.get())
        )
        self.settings.destroy()

    def pomo_debug_show(self, event):
        print("--------------------------POMODORO TIMER---------------------------------")
        print("Min Tens:", self.chosen_min_dig1.get())
        print("Min Ones", self.chosen_min_dig2.get())
        print("Second Tens:", self.chosen_sec_dig1.get())
        print("Second Ones:", self.chosen_sec_dig2.get())
        print(
            str(self.chosen_min_dig1.get()) + str(self.chosen_min_dig2.get()) + ":" + str(self.chosen_sec_dig1.get()) +
            str(self.chosen_sec_dig2.get())
        )
        print("-------------------------------------------------------------------------")


class PomoTimer:
    def __init__(self):
        self.running_thread = None
        self.semp_num = Semaphore(1)  # Used to synchronize functions RUN & RESET
        self.thread_event = Event()
        # Gives an error because we rely on having the start button first

        self.pomo_time = "00:25"
        self.lbreak_time = "00:15"
        self.sbreak_time = "00:05"

        self.timer_num = convertToNum(self.pomo_time)
        self.timer_type = "Pomodoro"  # May not be useful -- only for labeling
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
        self.outer.place(in_=self.window, anchor="c", relx=.5, rely=.5)

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
        if self.timer_type != "Pomodoro":
            print("[CHANGE TYPE] Type changed to: Pomodoro")
            self.thread_event.clear()

            self.timer_type = "Pomodoro"

            self.semp_num.acquire()
            self.manip_timer(time_type="Pomodoro")
            self.semp_num.release()
        else:
            print("[CHANGE TYPE] Attempted to change to POMODORO but already in state")

    def diff_timer_long(self):
        if self.timer_type != "Long Break":
            print("[CHANGE TYPE] Type changed to: Long Break")
            self.thread_event.clear()

            self.timer_type = "Long Break"

            self.semp_num.acquire()
            self.manip_timer(time_type="Long Break")
            self.semp_num.release()
        else:
            print("[CHANGE TYPE] Attempted to change to LONG BREAK but already in state")

    def diff_timer_short(self):
        if self.timer_type != "Short Break":
            print("[CHANGE TYPE] Type changed to: Short Break")
            self.thread_event.clear()

            self.timer_type = "Short Break"

            self.semp_num.acquire()
            self.manip_timer(time_type="Short Break")
            self.semp_num.release()
        else:
            print("[CHANGE TYPE] Attempted to change to SHORT BREAK but already in state")

    def reset_timer(self):
        self.semp_num.acquire()
        self.manip_timer(time_type=self.timer_type)

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
                self.manip_timer(time_type=self.timer_type)

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

            self.semp_num.acquire()

            # Addresses the case where the USER hits PAUSE just before as we are decrementing
            print("[UPDATE THREAD] Is it set?", self.thread_event.is_set())
            if not self.thread_event.is_set():  # To force another 1 sec delay after RUNNING again
                print("[UPDATE THREAD] System detected a pause right before decrementing")
                print("[UPDATE THREAD] Forcing an additional 1 sec delay (if applicable)")
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

    # Settings Window Below:
    def open_settings(self):
        # Does this need an existence flag?
        print("[SETTINGS] Window Open Invoked")
        self.settings_window = SettingsWindow(self.pomo_time, self.invoke_changes)

    # For the Settings' Window
    # For now assume that the timer is NOT running
    def invoke_changes(self, new_time):
        #self.default_time = new_time
        # self.timer_num = convertToNum(new_time)

        print("From Main Window:", new_time)
        self.timer.config(text=new_time)
        print("[SETTINGS] Default Timer Changed?! (Text Only)")

    # Assumes that calling block will be surrounded by semaphores...scary
    def manip_timer(self, time_type="Pomodoro"):
        if time_type == "Pomodoro":
            self.timer_num = convertToNum(self.pomo_time)
            self.timer.config(text=self.pomo_time)
            return self.pomo_time
        elif time_type == "Long Break":
            self.timer_num = convertToNum(self.lbreak_time)
            self.timer.config(text=self.lbreak_time)
            return self.lbreak_time
        elif time_type == "Short Break":
            self.timer_num = convertToNum(self.sbreak_time)
            self.timer.config(text=self.sbreak_time)
            return self.sbreak_time


if __name__ == "__main__":
    app = PomoTimer()
    app.run()
