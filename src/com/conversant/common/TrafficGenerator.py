from math import sin, pi
from random import random


class TrafficGenerator:
    def __init__(self, min_traffic=50, max_traffic=100, noise_to_signal=0.1):
        self.d = []
        self.noise_to_signal = noise_to_signal
        self.max_traffic = max_traffic
        self.min_traffic = min_traffic

    def gen_period(self, n_periods=10, tick_per_period=5000):
        w = pi / tick_per_period

        for i in range(tick_per_period * n_periods):
            a = (self.max_traffic - self.min_traffic) * (1 + self.noise_to_signal * random())
            p = abs(sin(w * i)) + self.noise_to_signal * random()

            self.d.append(a * p + self.min_traffic)

    def __del__(self):
        del self.d
