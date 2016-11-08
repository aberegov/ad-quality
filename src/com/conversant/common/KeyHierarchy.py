
class KeyHierarchy:
    def __init__(self, keys):
        self.base_keys  = keys
        self.hierarchies = {}

    def index(self, keys):
        return [i for i in map(lambda x: [i for i,j in enumerate(self.base_keys) if j == x][0], keys)]

    def set(self, name, keys):
        self.hierarchies.update({name: self.index(keys)})

    def reorder(self, hierarchy, data):
        if hierarchy in self.hierarchies:
            o = [data[i] for i in self.hierarchies[hierarchy]]
        else:
            o = list(data)
        return o

    def clear(self):
        self.hierarchies.clear()


