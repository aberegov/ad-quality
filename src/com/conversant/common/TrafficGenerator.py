from math import sin,pi
from random import random

class TrafficGenerator:
    sec_per_hour = 3600
    sec_per_day  = sec_per_hour * 24

    def __init__(self, noise_to_signal=0.3,max_traffic=100):
        self.d = []
        self.noise_to_signal = noise_to_signal
        self.max_traffic = max_traffic

    def gen_period(self, n_days=10):
        w = 2 * pi / self.sec_per_day

        for i in range(self.sec_per_day * n_days):
            self.d.append((self. max_traffic * (1 + random())) * (sin(w * i) + self.noise_to_signal * random() + 1))

    def __del__(self):
        del self.d
        self.d = []