
class SlidingBuffer:
    def __init__(self, limit):
        self.data = []
        self.archived = 0
        self.sliding_sum = 0
        self.limit = limit

    def add(self, item):
        self.data.append(item)
        self.sliding_sum += item

        if len(self.data) > self.limit:
            removed = self.data.pop(0)
            self.archived += removed
            self.sliding_sum -= removed

    @property
    def current(self):
        return self.sliding_sum

    @property
    def total(self):
        return self.archived + self.current

    def __iadd__(self, y):
        self.add(y)
        return  self

    def clear(self):
        self.data.clear()
        self.archived = 0
        self.sliding_sum = 0
