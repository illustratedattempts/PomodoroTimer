import tkinter as tk
from tkinter import ttk


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

        self.lbreak_label = ttk.Label(self.settings, text="Long Break Timer")
        self.lbreak_label.pack()
        self.lbreak_timer_frame = ttk.Frame(self.settings, padding=10)
        self.lbreak_timer_frame.pack()

        self.sbreak_label = ttk.Label(self.settings, text="Short Break Timer")
        self.sbreak_label.pack()
        self.sbreak_timer_frame = ttk.Frame(self.settings, padding=10)
        self.sbreak_timer_frame.pack()

        # For Combobox Values that represents digits of time
        self.timer_digit1 = ["0", "1", "2", "3", "4", "5"]
        self.timer_digit2 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        # Pomodoro Timer ComboBoxes
        # -----------------------------------------------------------------------------------------------------
        # Min Tens Digit
        self.pomo_chosen_min_dig1 = tk.IntVar()
        self.pomo_min_digit1 = ttk.Combobox(self.pomo_timer_frame, textvariable=self.pomo_chosen_min_dig1,
                                            state="readonly",
                                            values=self.timer_digit1)
        self.pomo_min_digit1.current(int(pomo_time[0]))
        self.pomo_min_digit1.bind('<<ComboboxSelected>>', self.pomo_debug_show)
        self.pomo_min_digit1.grid(row=0, column=0)
        # Min Ones Digit
        self.pomo_chosen_min_dig2 = tk.IntVar()
        self.pomo_min_digit2 = ttk.Combobox(self.pomo_timer_frame, textvariable=self.pomo_chosen_min_dig2,
                                            state="readonly",
                                            values=self.timer_digit2)
        self.pomo_min_digit2.current(int(pomo_time[1]))
        self.pomo_min_digit2.bind('<<ComboboxSelected>>', self.pomo_debug_show)
        self.pomo_min_digit2.grid(row=0, column=1)
        # Colon In Between
        self.pomo_time_colons = ttk.Label(self.pomo_timer_frame, text=":")
        self.pomo_time_colons.grid(row=0, column=2)
        # Second Tens Digit
        self.pomo_chosen_sec_dig1 = tk.IntVar()
        self.pomo_sec_digit1 = ttk.Combobox(self.pomo_timer_frame, textvariable=self.pomo_chosen_sec_dig1,
                                            state="readonly",
                                            values=self.timer_digit1)
        self.pomo_sec_digit1.current(int(pomo_time[3]))
        self.pomo_sec_digit1.bind('<<ComboboxSelected>>', self.pomo_debug_show)
        self.pomo_sec_digit1.grid(row=0, column=3)
        # Second Ones Digit
        self.pomo_chosen_sec_dig2 = tk.IntVar()
        self.pomo_sec_digit1 = ttk.Combobox(self.pomo_timer_frame, textvariable=self.pomo_chosen_sec_dig2,
                                            state="readonly",
                                            values=self.timer_digit2)
        self.pomo_sec_digit1.current(int(pomo_time[4]))
        self.pomo_sec_digit1.bind('<<ComboboxSelected>>', self.pomo_debug_show)
        self.pomo_sec_digit1.grid(row=0, column=4)
        # Readjust Weight Values of Columns for Even-ness
        self.pomo_timer_frame.grid_columnconfigure(0, weight=1)
        self.pomo_timer_frame.grid_columnconfigure(1, weight=1)
        # self.timer_frame.grid_columnconfigure(2, weight=1)
        self.pomo_timer_frame.grid_columnconfigure(3, weight=1)
        self.pomo_timer_frame.grid_columnconfigure(4, weight=1)

        # Long Break Timer ComboBoxes
        # -----------------------------------------------------------------------------------------------------
        self.lbreak_chosen_min_dig1 = tk.IntVar()
        self.lbreak_min_digit1 = ttk.Combobox(self.lbreak_timer_frame, textvariable=self.lbreak_chosen_min_dig1,
                                              state="readonly",
                                              values=self.timer_digit1)
        self.lbreak_min_digit1.current(int(lbreak_time[0]))
        self.lbreak_min_digit1.bind('<<ComboboxSelected>>', self.lbreak_debug_show)
        self.lbreak_min_digit1.grid(row=0, column=0)
        # Min Ones Digit
        self.lbreak_chosen_min_dig2 = tk.IntVar()
        self.lbreak_min_digit2 = ttk.Combobox(self.lbreak_timer_frame, textvariable=self.lbreak_chosen_min_dig2,
                                              state="readonly",
                                              values=self.timer_digit2)
        self.lbreak_min_digit2.current(int(lbreak_time[1]))
        self.lbreak_min_digit2.bind('<<ComboboxSelected>>', self.lbreak_debug_show)
        self.lbreak_min_digit2.grid(row=0, column=1)
        # Colon In Between
        self.lbreak_time_colons = ttk.Label(self.lbreak_timer_frame, text=":")
        self.lbreak_time_colons.grid(row=0, column=2)
        # Second Tens Digit
        self.lbreak_chosen_sec_dig1 = tk.IntVar()
        self.lbreak_sec_digit1 = ttk.Combobox(self.lbreak_timer_frame, textvariable=self.lbreak_chosen_sec_dig1,
                                              state="readonly",
                                              values=self.timer_digit1)
        self.lbreak_sec_digit1.current(int(lbreak_time[3]))
        self.lbreak_sec_digit1.bind('<<ComboboxSelected>>', self.lbreak_debug_show)
        self.lbreak_sec_digit1.grid(row=0, column=3)
        # Second Ones Digit
        self.lbreak_chosen_sec_dig2 = tk.IntVar()
        self.lbreak_sec_digit1 = ttk.Combobox(self.lbreak_timer_frame, textvariable=self.lbreak_chosen_sec_dig2,
                                              state="readonly",
                                              values=self.timer_digit2)
        self.lbreak_sec_digit1.current(int(lbreak_time[4]))
        self.lbreak_sec_digit1.bind('<<ComboboxSelected>>', self.lbreak_debug_show)
        self.lbreak_sec_digit1.grid(row=0, column=4)
        # Readjust Weight Values of Columns for Even-ness
        self.lbreak_timer_frame.grid_columnconfigure(0, weight=1)
        self.lbreak_timer_frame.grid_columnconfigure(1, weight=1)
        # self.timer_frame.grid_columnconfigure(2, weight=1)
        self.lbreak_timer_frame.grid_columnconfigure(3, weight=1)
        self.lbreak_timer_frame.grid_columnconfigure(4, weight=1)

        # Short Break Timer ComboBoxes
        # -----------------------------------------------------------------------------------------------------
        self.sbreak_chosen_min_dig1 = tk.IntVar()
        self.sbreak_min_digit1 = ttk.Combobox(self.sbreak_timer_frame, textvariable=self.sbreak_chosen_min_dig1,
                                              state="readonly",
                                              values=self.timer_digit1)
        self.sbreak_min_digit1.current(int(sbreak_time[0]))
        self.sbreak_min_digit1.bind('<<ComboboxSelected>>', self.sbreak_debug_show)
        self.sbreak_min_digit1.grid(row=0, column=0)
        # Min Ones Digit
        self.sbreak_chosen_min_dig2 = tk.IntVar()
        self.sbreak_min_digit2 = ttk.Combobox(self.sbreak_timer_frame, textvariable=self.sbreak_chosen_min_dig2,
                                              state="readonly",
                                              values=self.timer_digit2)
        self.sbreak_min_digit2.current(int(sbreak_time[1]))
        self.sbreak_min_digit2.bind('<<ComboboxSelected>>', self.sbreak_debug_show)
        self.sbreak_min_digit2.grid(row=0, column=1)
        # Colon In Between
        self.sbreak_time_colons = ttk.Label(self.sbreak_timer_frame, text=":")
        self.sbreak_time_colons.grid(row=0, column=2)
        # Second Tens Digit
        self.sbreak_chosen_sec_dig1 = tk.IntVar()
        self.sbreak_sec_digit1 = ttk.Combobox(self.sbreak_timer_frame, textvariable=self.sbreak_chosen_sec_dig1,
                                              state="readonly",
                                              values=self.timer_digit1)
        self.sbreak_sec_digit1.current(int(sbreak_time[3]))
        self.sbreak_sec_digit1.bind('<<ComboboxSelected>>', self.sbreak_debug_show)
        self.sbreak_sec_digit1.grid(row=0, column=3)
        # Second Ones Digit
        self.sbreak_chosen_sec_dig2 = tk.IntVar()
        self.sbreak_sec_digit1 = ttk.Combobox(self.sbreak_timer_frame, textvariable=self.sbreak_chosen_sec_dig2,
                                              state="readonly",
                                              values=self.timer_digit2)
        self.sbreak_sec_digit1.current(int(sbreak_time[4]))
        self.sbreak_sec_digit1.bind('<<ComboboxSelected>>', self.sbreak_debug_show)
        self.sbreak_sec_digit1.grid(row=0, column=4)
        # Readjust Weight Values of Columns for Even-ness
        self.sbreak_timer_frame.grid_columnconfigure(0, weight=1)
        self.sbreak_timer_frame.grid_columnconfigure(1, weight=1)
        # self.timer_frame.grid_columnconfigure(2, weight=1)
        self.sbreak_timer_frame.grid_columnconfigure(3, weight=1)
        self.sbreak_timer_frame.grid_columnconfigure(4, weight=1)
        # -----------------------------------------------------------------------------------------------------

        self.submit_btn = ttk.Button(self.settings, text="Submit Stuff", command=self.settings_finished)
        self.submit_btn.pack()

    def settings_finished(self):
        build_pomo_timer = str(self.pomo_chosen_min_dig1.get()) + str(self.pomo_chosen_min_dig2.get()) + ":" + \
                           str(self.pomo_chosen_sec_dig1.get()) + str(self.pomo_chosen_sec_dig2.get())
        self.apply_changes()
        print("[SETTINGS] Destroying Window...")
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
        print("")
        print("--------------------------[SETTINGS] SHORT BREAK TIMER---------------------------------")
        print("Min Tens:", self.lbreak_chosen_min_dig1.get())
        print("Min Ones", self.lbreak_chosen_min_dig2.get())
        print("Second Tens:", self.lbreak_chosen_sec_dig1.get())
        print("Second Ones:", self.lbreak_chosen_sec_dig2.get())
        print(
            str(self.lbreak_chosen_min_dig1.get()) + str(self.lbreak_chosen_min_dig2.get()) + ":" +
            str(self.lbreak_chosen_sec_dig1.get()) +
            str(self.lbreak_chosen_sec_dig2.get())
        )
        print("----------------------------------------------------------------------------------------")
