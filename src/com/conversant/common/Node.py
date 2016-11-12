import uuid


class Node(object):
    def __init__(self, name=None, nid=None, data=None):
        self.identifier = nid if nid is not None else str(uuid.uuid1())
        self.name = name if name is not None else self.identifier
        self.parent = None
        self.children = {}
        self.data = data

    def set_parent(self, nid):
        self.parent = nid

    def add_child(self, node):
        self.children.update({node.name: node.identifier})
        node.set_parent(self.identifier)

    def __repr__(self):
        name = self.__class__.__name__
        args = [
            "tag=%r" % self.tag,
            "identifier=%r" % self.identifier,
            "data=%r" % self.data
        ]
        return "%s(%s)" % (name, ", ".join(args))
