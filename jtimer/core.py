from math import ceil
from time import time

class TimerCore:
    def __init__(self, seconds, precision):
        self.registered_time = None
        self.remained = seconds
        self.precision = precision

        self.state = 'paused'

        self.update_label()

    def time(self):
        return time()

    def interact(self):
        if self.state in {'running'}:
            self.pause()
        elif self.state in {'paused'}:
            self.start()
        elif self.state in {'exhausted'}:
            self.shutdown()
        elif self.state in {'shutdown'}:
            raise AssertionError

    def close(self):
        try:
            if self.state in {'running', 'paused'}:
                self.print_remained()
        finally:
            self.state = 'shutdown'
            self.shutdown()

    def update(self):
        assert self.state in {'running'}, self.state
        self.update_label()
        if self.state in {'exhausted'}:
            self.stop_timeout()

    def update_label(self):
        remained = self.get_remained()
        self.set_label_text(self.format_remained(remained), finished=remained <= 0.0)

    def get_remained(self):
        if self.state in {'running'}:
            self.update_time()
            remained = self.remained
            if remained <= 0.0:
                self.state = 'exhausted'
                return 0.0
            return remained
        if self.state in {'paused'}:
            return self.remained
        if self.state in {'exhausted'}:
            return 0.0
        if self.state in {'shutdown'}:
            raise AssertionError

    def start(self):
        assert self.state in {'paused'}
        assert self.remained > 0.0
        self.registered_time = self.time()
        self.state = 'running'
        self.start_timeout()

    def pause(self):
        assert self.state in {'running'}
        self.update_time()
        self.stop_timeout()
        if self.remained <= 0.0:
            self.state = 'exhausted'
        else:
            self.state = 'paused'

    def update_time(self):
        assert self.state in {'running'}
        passed_time = self.time() - self.registered_time
        self.registered_time += passed_time
        self.remained -= passed_time

    def print_remained(self):
        """Print remained time on stdout."""
        print('Remained: ' + self.format_remained(self.get_remained()))

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

    def mainloop(self):
        raise NotImplementedError

    def shutdown(self):
        raise NotImplementedError

    def set_label_text(self, text, finished=False):
        raise NotImplementedError

    def start_timeout(self):
        raise NotImplementedError

    def stop_timeout(self):
        raise NotImplementedError

