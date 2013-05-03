#!/usr/bin/env python3

from math import ceil, sqrt, exp
from random import uniform, normalvariate
import time

from tkinter import *

def main(minutes, precision=0,
    poisson=False, wiener=False,
    immediate=False
):
    if wiener:
        App = WienerTimerApp
    elif poisson:
        App = PoissonTimerApp
    else:
        App = TimerApp
    app = App(Tk(), minutes, precision)
    if immediate:
        app.start_timer(event=None)
    app.mainloop()

class TimerApp:
    def __init__(self, master, minutes, precision):
        self.master = master

        self.label = Label(master, font='Monospace 100')
        self.label.pack(expand=True)

        self.start_time = None
        self.duration = 60 * minutes
        self.precision = precision
        self.print_remained(after=False)
        self.master.bind('<space>', self.start_timer)

        master.wm_title('Timer')

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

    def print_remained(self, after=True):
        remained = self.remained
        if remained <= 0:
            return self.finish_timer()
        self.label.config(text=self.format_remained(remained))
        if after:
            self.master.after(10, self.print_remained)

    def finish_timer(self):
        self.label.config(text='Finish!', fg='red')
        #self.master.update_idletasks()

        self.master.bind('<space>', self.quit_timer)

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

class PoissonTimerApp(TimerApp):
    def __init__(self, master, minutes, precision):
        assert precision == 0
        self.poisson_last = None
        super().__init__(master, minutes, precision)
        self.duration = int(self.duration)
        master.wm_title('Poisson timer')

    def start_timer(self, event):
        super().start_timer(event)
        self.poisson_last = self.start_time
        self.duration -= 1

    @property
    def remained(self):
        if self.poisson_last is None:
            return self.duration
        time_passed = time.time() - self.poisson_last
        self.poisson_last += time_passed
        self.duration -= self.poisson(time_passed)
        return self.duration + 0.5

    @staticmethod
    def poisson(mean):
        x = uniform(0, 1)
        k = 0
        p = exp(-mean)
        while (x > p):
            x -= p
            k += 1
            p *= mean / k
        else:
            return k

class WienerTimerApp(TimerApp):
    def __init__(self, master, minutes, precision):
        self.wiener_last = None
        super().__init__(master, minutes, precision)
        master.wm_title('Wiener timer')

    def start_timer(self, event):
        super().start_timer(event)
        self.duration = sqrt(self.duration)
        self.wiener_last = self.start_time

    @property
    def remained(self):
        if self.wiener_last is None:
            return self.duration
        time_passed = time.time() - self.wiener_last
        self.wiener_last += time_passed
        self.duration -= self.wiener(time_passed)
        return self.duration**2 if self.duration >= 0.0 else self.duration

    @staticmethod
    def wiener(time_passed):
        return normalvariate(0, 1.4826022184455 * sqrt(time_passed))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='tktimer', description="Tkinter-based timer")
    parser.add_argument('minutes', type=float,
        metavar='DURATION', help='duration in minutes' )
    parser.add_argument('-p', '--precision', type=int,
        default=0, const=1, nargs='?',
        help='print fractions of seconds' )
    parser.add_argument('-P', '--poisson',
        action='store_true',
        help='Poisson timer' )
    parser.add_argument('-W', '--wiener',
        action='store_true',
        help='Wiener timer' )
    parser.add_argument('-i', '--immediate',
        action='store_true',
        help='Start timer immediately')
    args = parser.parse_args()
    if (args.precision < 0):
        parser.error('precision must be non-negative')

    main(**vars(args))

