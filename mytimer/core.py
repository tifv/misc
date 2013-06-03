#!/usr/bin/env python3

from math import sqrt, exp
from random import uniform, normalvariate
import time

class RegularTimer:
    def __init__(self, seconds):
        self.start_time = None
        self.current_time = None
        self.duration = seconds

    def start_timer(self):
        self.start_time = time.time()

    def remained(self):
        if self.start_time is None:
            return self.duration
        return self.duration + self.start_time - time.time()

class PoissonTimer(RegularTimer):
    def __init__(self, seconds):
        self.poisson_last = None
        super().__init__(seconds)
        self.duration = int(self.duration)

    def start_timer(self):
        super().start_timer()
        self.poisson_last = self.start_time
        self.duration -= 1

    def remained(self):
        if self.poisson_last is None:
            return self.duration
        time_passed = time.time() - self.poisson_last
        self.poisson_last += time_passed
        self.duration -= self.poisson(time_passed)
        return self.duration

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

class WienerTimer(RegularTimer):
    def __init__(self, seconds):
        self.wiener_last = None
        super().__init__(seconds)
        self.original_duration = self.duration
        self.duration = sqrt(self.duration)

    def start_timer(self):
        super().start_timer()
        self.wiener_last = self.start_time

    def remained(self):
        if self.wiener_last is None:
            return self.original_duration
        time_passed = time.time() - self.wiener_last
        self.wiener_last += time_passed
        self.duration -= self.wiener(time_passed)
        return self.duration**2 if self.duration >= 0.0 else self.duration

    @staticmethod
    def wiener(time_passed):
        return normalvariate(0, 1.4826022184455 * sqrt(time_passed))

