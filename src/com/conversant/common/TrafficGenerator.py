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
            amplitude = (self.max_traffic - self.min_traffic) * (1 + self.noise_to_signal * random())
            periodic = abs(sin((w + 0.00001 * random()) * i))

            self.d.append(amplitude * periodic + self.min_traffic)

    def __del__(self):
        del self.d
