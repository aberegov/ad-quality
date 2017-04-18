from random import random


class Throttling:
    def __init__(self, cap, win_rate=0.03, period=5000):
        self.value = 0.5
        self.win_rate = win_rate
        self.cap = cap
        self.window = []
        self.results = []
        self.period = period

    def tick(self, n_bids):
        # simulate biddy/exchange/nessy
        n_impressions = 0
        for i in range(n_bids):
            n_impressions += self.win_rate if random() <= self.value else 0

        # simulate maelstrom
        self.window.insert(0, [n_impressions, n_impressions / self.value])
        if len(self.window) > self.period:
            self.window.pop()

        # impression_stats[0] impressions over period
        # impression_stats[1] available impressions over period
        impression_stats = [sum(i) for i in zip(*self.window)]

        # throttle = (cap / available) x correction
        # correction = min(1, cap / spend) ^ 8
        if impression_stats[0] > 0 and impression_stats[1] > 0:
            # simulate DMA
            self.value = min(1, (self.cap / impression_stats[1])) * pow(min(1, self.cap / impression_stats[0]), 8)

        self.results.append([impression_stats[0], self.cap, n_bids])

    def __del__(self):
        del self.window
        del self.results
