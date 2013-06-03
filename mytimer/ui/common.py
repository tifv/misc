from math import ceil

class CommonTimerApp:
    def __init__(self, timer, precision):
        self.timer = timer
        self.precision = precision

    def start_timer(self):
        self.timer.start_timer()

    def break_timer(self):
        remained = self.timer.remained()
        print("Remained: {}".format(self.format_remained(remained)))

    def format_remained(self, remained):
        if self.precision == 0:
            remained = ceil(remained)
            minutes = remained // (60)
            seconds = remained % 60
            return '{0:0=2d}:{1:0=2d}'.format(minutes, seconds)
        assert self.precision >= 0
        modulo = 10**self.precision
        remained = ceil(remained * modulo)
        minutes = remained // (60 * modulo)
        seconds = remained % (60 * modulo) // modulo
        subseconds = remained % modulo
        return '{0:0=2d}:{1:0=2d}.{2:0={precision}d}'.format(
            minutes, seconds, subseconds,
            precision=self.precision )



