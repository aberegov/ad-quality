from com.conversant.common.KeyHierarchy import KeyHierarchy


class MultiKey:
    key_sql = "(case when %s is null then '(null)' else %s::varchar end) as %s"

    def __init__(self, keys):
        self.keys = keys
        self.hierarchies = KeyHierarchy(keys)

    def __str__(self):
        return ','.join(map(lambda x: self.key_sql % (x, x, x), self.keys))

    def __setitem__(self, name, keys):
        self.hierarchies.set(name, keys)

    def reorder(self, name, data):
        return self.hierarchies.reorder(name, data)
