import uuid


class Node(object):
    def __init__(self, name=None, nid=None, value=None):
        self.identifier = nid if nid is not None else str(uuid.uuid1())
        self.name = name if name is not None else self.identifier
        self.value = value
        self.parent = None
        self.children = {}

    def set_parent(self, nid):
        self.parent = nid

    def add_child(self, node):
        self.children.update({node.name: node.identifier})
        node.set_parent(self.identifier)

    def __hash__(self):
        return self.identifier.__hash__()

    def __repr__(self):
        name = self.__class__.__name__
        args = [
            "id=%r" % self.identifier,
            "name=%r" % self.name,
            "value=%r" % self.value
        ]
        return "%s(%s)" % (name, ", ".join(args))
