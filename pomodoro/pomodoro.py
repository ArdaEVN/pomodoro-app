import tkinter as tk
from tkinter import simpledialog, Toplevel

try:
    import winsound  # For Windows
except ImportError:
    import os  # Use os.system to play sound on macOS and Linux

def play_sound(sound_file):
    try:
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)
    except:
        os.system(f'aplay {sound_file}')

class PomodoroTimer:
    def __init__(self, master, sound_file, bg_color, fg_color, break_function):
        self.master = master
        self.sound_file = sound_file
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.break_function = break_function
        self.work_duration = 25 * 60  # Default to 25 minutes
        self.remaining_time = self.work_duration
        self.running = False

        self.master.configure(background=self.bg_color)

        # Task label
        self.task_label = tk.Label(master, text="Click to set task", font=('Helvetica', 16),
                                   bg=self.bg_color, fg=self.fg_color)
        self.task_label.pack()
        self.task_label.bind("<Button-1>", self.set_task_label)

        # Timer display
        self.timer_display = tk.Label(master, text=self.format_time(self.remaining_time), font=('Helvetica', 48),
                                      bg=self.bg_color, fg=self.fg_color)
        self.timer_display.pack()
        self.timer_display.bind("<Button-1>", self.set_timer_duration)

        # Control buttons
        button_font = ('Helvetica', 14)
        self.start_button = tk.Button(master, text='Start', font=button_font, command=self.start_timer, bg='green', fg='white')
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(master, text='Stop', font=button_font, command=self.stop_timer, bg='red', fg='white')
        self.stop_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def set_task_label(self, event):
        task = simpledialog.askstring("Task Label", "Set the task name:", parent=self.master)
        if task:
            self.task_label.config(text=task)

    def set_timer_duration(self, event):
        time_str = simpledialog.askstring("Set Timer", "Enter time in minutes:", parent=self.master)
        if time_str and time_str.isdigit():
            self.work_duration = int(time_str) * 60
            self.remaining_time = self.work_duration
            self.timer_display.config(text=self.format_time(self.remaining_time))

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return '{:02d}:{:02d}'.format(mins, secs)

    def update_timer(self):
        if self.running:
            self.remaining_time -= 1
            self.timer_display.config(text=self.format_time(self.remaining_time))
            if self.remaining_time <= 0:
                play_sound(self.sound_file)
                self.running = False
                self.break_function()
            else:
                self.master.after(1000, self.update_timer)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.remaining_time = self.work_duration  # Reset time each start
            self.update_timer()

    def stop_timer(self):
        self.running = False

class PomodoroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.geometry('1200x300')  # Wider window for better layout

        self.sound_file = "alarm.wav"  # Path to your sound file
        colors = ['light blue', 'light green', 'light yellow', 'light pink']

        for color in colors:
            frame = tk.Frame(master, bg=color, bd=2, relief=tk.RAISED)
            frame.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.BOTH)
            PomodoroTimer(frame, self.sound_file, color, 'black', self.start_break)

    def start_break(self):
        break_window = Toplevel(self.master)
        break_window.title("Break Time!")
        break_window.geometry('300x100')  # Smaller window for break time
        tk.Label(break_window, text="Break Time!", font=('Helvetica', 24), bg='light coral').pack(expand=True, fill=tk.BOTH)
        play_sound(self.sound_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
