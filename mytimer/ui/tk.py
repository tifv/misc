from tkinter import Tk, Label
from functools import partial

from .common import CommonTimerApp

class TkTimerApp(CommonTimerApp):
    def __init__(self, timer, precision, title='timer'):
        super().__init__(timer, precision)

        self.master = Tk()
        self.master.wm_title(title)

        self.label = Label(self.master, font='Monospace 100')
        self.label.pack(expand=True)

        self.show_remained()
        self.master.bind('<space>', self.start_timer)

    def start_timer(self, event):
        super().start_timer()
        self.show_remained(repeat=True)
        self.master.bind('<space>', self.break_timer)

    def break_timer(self, event):
        super().break_timer()
        self.master.quit()

    def quit_timer(self, event):
        self.master.quit()

    def mainloop(self):
        return self.master.mainloop()

    def show_remained(self, repeat=False):
        remained = self.timer.remained()
        if remained <= 0:
            return self.finish_timer()
        self.label.config(text=self.format_remained(remained))
        if repeat:
            self.master.after(20, partial(self.show_remained, repeat=True))

    def finish_timer(self):
        self.label.config(text=self.format_remained(0.0), fg='red')
        self.master.bind('<space>', self.quit_timer)

