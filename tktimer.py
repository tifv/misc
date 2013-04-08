#!/usr/bin/env python3
from math import ceil
from tkinter import *

import time

class TimerApp:
    def __init__(self, master, minutes, precision):
        self.master = master

        self.label = Label(master, font='Monospace 100')
        self.label.pack(expand=True)

        self.start_time = None
        self.duration = 60 * minutes
        self.precision = precision
        self.print_remained()
        self.master.bind('<space>', self.start_timer)

    def start_timer(self, event):
        self.master.bind('<space>', self.break_timer)
        self.start_time = time.time()
        self.print_remained()

    def break_timer(self, event):
        self.master.quit()
        print("Remained: {}".format(self.format_remained(self.remained)))

    def quit_timer(self, event):
        self.master.quit()

    def mainloop(self):
        return self.master.mainloop()

    def print_remained(self):
        remained = self.remained
        if remained <= 0:
            return self.finish_timer()
        self.label.config(text=self.format_remained(remained))
        self.master.after(10, self.print_remained)

    def finish_timer(self):
        self.label.config(text='Finish!', fg='red')
        self.master.update_idletasks()

        self.master.after(1, self.noise)

        self.master.bind('<space>', self.quit_timer)

    def noise(self):
        pass

    @property
    def remained(self):
        if self.start_time is None:
            return self.duration
        return self.duration + self.start_time - time.time()

    def format_remained(self, remained):
        precision = self.precision
        modulo = 10**precision
        remained = ceil(remained * modulo)
        minutes = remained // (60 * modulo)
        seconds = remained % (60 * modulo) // modulo
        subseconds = remained % modulo
        if precision > 0:
            return '{0:0=2d}:{1:0=2d}.{2:0={precision}d}'.format(
                minutes, seconds, subseconds,
                precision=precision )
        else:
            return '{0:0=2d}:{1:0=2d}'.format(minutes, seconds)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='tktimer', description="Tkinter-based timer")
    parser.add_argument('minutes', type=float,
        metavar='DURATION', help='duration in minutes' )
    parser.add_argument('-p', '--precision', type=int,
        default=0, const=1, nargs='?',
        help='print fractions of seconds')
    args = parser.parse_args()
    assert args.precision >= 0
    app = TimerApp(Tk(), args.minutes, args.precision)
    app.mainloop()

