from math import sqrt
from random import normalvariate

from ..core import TimerCore

class WienerTimerCore(TimerCore):
    def __init__(self, seconds, *args, **kwargs):
        seconds = sqrt(seconds)
        super().__init__(seconds, *args, **kwargs)

    def get_remained(self):
        remained = super().get_remained()
        assert remained >= 0.0
        return remained**2

    def update_time(self):
        passed_time = self.time() - self.registered_time
        self.registered_time += passed_time
        self.remained -= self.wiener(passed_time)

    @staticmethod
    def wiener(passed_time):
        return normalvariate(0, 1.4826022184455 * sqrt(passed_time))

