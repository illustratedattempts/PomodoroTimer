import tkinter as tk
from tkinter import ttk


def eval_2digs(num):
    if num < 10:
        return "0" + str(num)
    return str(num)

class SettingsWindow:
    window_exist = False

    # Alive Variable attributes need to be implemented only when you want to close it a second way
    # Alive Variable attributes: Changing the timer while it is running?
    def __init__(self, pomo_time, lbreak_time, sbreak_time, change_func):
        self.apply_changes = change_func

        self.settings = tk.Toplevel()
        self._setup_settings_win(pomo_time, lbreak_time, sbreak_time)
        self.settings.protocol("WM_DELETE_WINDOW", self._on_close)

        SettingsWindow.window_exist = True

        # grab_set() function invokes MODAL mode.
        # Guarantees that the user can not create new Settings Windows
        self.settings.grab_set()

    def _on_close(self):
        print("[SETTINGS] Destroying Window...")
        SettingsWindow.window_exist = False
        self.settings.destroy()

    def _setup_settings_win(self, pomo_time, lbreak_time, sbreak_time):
        self.settings.config(width=300, height=200)
        self.settings.minsize(width=200, height=250)
        self.settings.geometry("300x200+600+400")
        self.settings.title("Settings")

        self.pomo_label = ttk.Label(self.settings, text="Pomodoro Timer")
        self.pomo_label.pack()
        self.pomo_timer_frame = ttk.Frame(self.settings, padding=10)
        self.pomo_timer_frame.pack()

        self.long_label = ttk.Label(self.settings, text="Long Break Timer")
        self.long_label.pack()
        self.long_frame = ttk.Frame(self.settings, padding=10)
        self.long_frame.pack()

        self.short_label = ttk.Label(self.settings, text="Short Break Timer")
        self.short_label.pack()
        self.short_frame = ttk.Frame(self.settings, padding=10)
        self.short_frame.pack()

        # For Combobox Values that represents digits of time
        self.timer_digit1 = ["0", "1", "2", "3", "4", "5"]
        self.timer_digit2 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        # Pomodoro Timer
        # -----------------------------------------------------------------------------------------------------
        # Min Digit
        self.chosen_pomo_min = tk.IntVar()
        self.pomo_min = ttk.Spinbox(self.pomo_timer_frame, wrap=True, state="readonly", from_=0, to=59, increment=1,
                                    textvariable=self.chosen_pomo_min)
        self.pomo_min.grid(row=0, column=0)

        # Colon In Between
        self.pomo_colons = ttk.Label(self.pomo_timer_frame, text=":")
        self.pomo_colons.grid(row=0, column=1)

        # Sec Digit
        self.chosen_pomo_sec = tk.IntVar()
        self.pomo_sec = ttk.Spinbox(self.pomo_timer_frame, wrap=True, state="readonly", from_=0, to=59, increment=1,
                                    textvariable=self.chosen_pomo_sec)
        self.pomo_sec.grid(row=0, column=2)

        # Long Break Timer
        # -----------------------------------------------------------------------------------------------------
        # Min Digit
        self.chosen_long_min = tk.IntVar()
        self.long_min = ttk.Spinbox(self.long_frame, wrap=True, state="readonly", from_=0, to=59, increment=1,
                                    textvariable=self.chosen_long_min)
        self.long_min.grid(row=0, column=0)

        # Colon In Between
        self.long_colons = ttk.Label(self.long_frame, text=":")
        self.long_colons.grid(row=0, column=1)

        # Sec Digit
        self.chosen_long_sec = tk.IntVar()
        self.long_sec = ttk.Spinbox(self.long_frame, wrap=True, state="readonly", from_=0, to=59, increment=1,
                                    textvariable=self.chosen_long_sec)
        self.long_sec.grid(row=0, column=2)

        # Short Break Timer ComboBoxes
        # -----------------------------------------------------------------------------------------------------
        # Min Digit
        self.chosen_short_min = tk.IntVar()
        self.short_min = ttk.Spinbox(self.short_frame, wrap=True, state="readonly", from_=0, to=59, increment=1,
                                     textvariable=self.chosen_short_min)
        self.short_min.grid(row=0, column=0)

        # Colon In Between
        self.short_colons = ttk.Label(self.short_frame, text=":")
        self.short_colons.grid(row=0, column=1)

        # Sec Digit
        self.chosen_short_sec = tk.IntVar()
        self.short_min = ttk.Spinbox(self.short_frame, wrap=True, state="readonly", from_=0, to=59, increment=1,
                                     textvariable=self.chosen_short_sec)
        self.short_min.grid(row=0, column=2)
        # -----------------------------------------------------------------------------------------------------

        self.apply_btn = ttk.Button(self.settings, text="Apply Changes", command=self.settings_finished)
        self.apply_btn.pack()

    def settings_finished(self):
        built_ptimer = eval_2digs(self.chosen_pomo_min.get()) + ":" + eval_2digs(self.chosen_pomo_sec.get())
        built_ltimer = eval_2digs(self.chosen_long_min.get()) + ":" + eval_2digs(self.chosen_long_sec.get())
        built_stimer = eval_2digs(self.chosen_short_min.get()) + ":" + eval_2digs(self.chosen_short_sec.get())

        self.apply_changes(built_ptimer, built_ltimer, built_stimer)
        SettingsWindow.window_exist = False
        self.settings.destroy()

    def pomo_debug_show(self, event):
        print("--------------------------[SETTINGS] POMODORO TIMER---------------------------------")
        print("Min Tens:", self.pomo_chosen_min_dig1.get())
        print("Min Ones", self.pomo_chosen_min_dig2.get())
        print("Second Tens:", self.pomo_chosen_sec_dig1.get())
        print("Second Ones:", self.pomo_chosen_sec_dig2.get())
        print(
            str(self.pomo_chosen_min_dig1.get()) + str(self.pomo_chosen_min_dig2.get()) + ":" +
            str(self.pomo_chosen_sec_dig1.get()) +
            str(self.pomo_chosen_sec_dig2.get())
        )
        print("------------------------------------------------------------------------------------")

    def lbreak_debug_show(self, event):
        print("--------------------------[SETTINGS] LONG BREAK TIMER---------------------------------")
        print("Min Tens:", self.lbreak_chosen_min_dig1.get())
        print("Min Ones", self.lbreak_chosen_min_dig2.get())
        print("Second Tens:", self.lbreak_chosen_sec_dig1.get())
        print("Second Ones:", self.lbreak_chosen_sec_dig2.get())
        print(
            str(self.lbreak_chosen_min_dig1.get()) + str(self.lbreak_chosen_min_dig2.get()) + ":" +
            str(self.lbreak_chosen_sec_dig1.get()) +
            str(self.lbreak_chosen_sec_dig2.get())
        )
        print("--------------------------------------------------------------------------------------")

    def sbreak_debug_show(self, event):
        print("--------------------------[SETTINGS] SHORT BREAK TIMER---------------------------------")
        print("Min Tens:", self.sbreak_chosen_min_dig1.get())
        print("Min Ones", self.sbreak_chosen_min_dig2.get())
        print("Second Tens:", self.sbreak_chosen_sec_dig1.get())
        print("Second Ones:", self.sbreak_chosen_sec_dig2.get())
        print(
            str(self.sbreak_chosen_min_dig1.get()) + str(self.sbreak_chosen_min_dig2.get()) + ":" +
            str(self.sbreak_chosen_sec_dig1.get()) +
            str(self.sbreak_chosen_sec_dig2.get())
        )
        print("----------------------------------------------------------------------------------------")
