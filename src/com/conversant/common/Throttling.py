from random import random
import pandas as pd

class Throttling:
    def __init__(self, cap,  period=5000):
        self.value = 0.5
        self.cap = cap
        self.window = []
        self.results = []
        self.period = period

    def tick(self, n_bids, win_rate=0.03):
        # simulate biddy/exchange/nessy
        n_impressions = 0
        for i in range(n_bids):
            n_impressions += win_rate if random() <= self.value else 0

        # simulate maelstrom
        d = [n_impressions, n_impressions / self.value]
        self.window.insert(0, d)
        if len(self.window) > self.period:
            self.window.pop()

        # [0] impressions over period
        # [1] available impressions over period
        impression_stats = [sum(i) for i in zip(*self.window)]

        # throttle = (cap / available) x correction
        # correction = min(1, cap / spend) ^ 8
        if impression_stats[0] > 0 and impression_stats[1] > 0:
            # simulate DMA
            t = min(1, (self.cap / impression_stats[1]))
            c =  pow(min(1, self.cap / impression_stats[0]), 8)
            self.value = t * c
            print(impression_stats[0], t,c)

        if len(self.window) == self.period:
            self.results.append([impression_stats[0], self.cap, n_bids])

    def __del__(self):
        del self.window
        del self.results
