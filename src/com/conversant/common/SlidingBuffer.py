
class SlidingBuffer:
    def __init__(self, limit):
        self.data = []
        self.sunk = 0
        self.limit = limit

    def add(self, item):
        self.data.append(item)
        if len(self.data) > self.limit:
            self.sunk += self.data.pop(0)

    @property
    def sum(self):
        return sum(self.data)

    @property
    def total(self):
        return self.sunk + self.sum

    def clear(self):
        self.data.clear()
        self.sunk = 0