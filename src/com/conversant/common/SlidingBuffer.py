
class SlidingBuffer:
    def __init__(self, limit):
        self.data = []
        self.sunk = 0
        self.sliding_sum = 0
        self.limit = limit

    def add(self, item):
        self.data.append(item)
        self.sliding_sum += item

        if len(self.data) > self.limit:
            removed = self.data.pop(0)
            self.sunk += removed
            self.sliding_sum -= removed

    @property
    def sum(self):
        return self.sliding_sum

    @property
    def total(self):
        return self.sunk + self.sum

    def clear(self):
        self.data.clear()
        self.sunk = 0
        self.sliding_sum = 0
