from random import random
class Throttling:
    size = 3600 * 24

    def __init__(self, cap, win=0.03):
        self.value = 0.5
        self.win = win
        self.cap = cap
        self.window = []
        self.count = 0
        self.results = []

    def tick(self, n_events):
        d = n_events * self.win if random() < self.value else 0

        self.window.append(d)
        if len(self.window) > self.size:
            self.window.pop(0)

        s = sum(self.window)
        if s > 0 and self.value > 1e-20:
            self.value = min(1, min(1, (self.cap / (s / self.value))) * pow(min(1, self.cap / s), 8))
        else:
            self.value = 0.000001

        print(s, self.value, len(self.window))

        self.count += 1
        if self.count % 3600 == 0:
            self.results.append(s)