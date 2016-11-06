import uuid


class Node(object):
    id = None

    def __init__(self, tag=None, nid=None, data=None):
        # sets the node identifier
        self.set_id(nid)

        # set human-readable tag
        if tag is None:
            self.tag = self.id
        else:
            self.tag = tag

        # the parent is not defined yet
        self.parent = None

        # prepare a list to reference to-be-added children
        self.children = list()

        # arbitrary data associated with the node
        self.data = data

    def set_id(self, nid):
        """Sets the node identifier using supplied or generated id"""
        if nid is None:
            self.id = str(uuid.uuid1())
        else:
            self.id = nid

    @property
    def identifier(self):
        return self.id

    @identifier.setter
    def identifier(self, value):
        if value is None:
            print("WARNING: node ID must be defined")
        else:
            self.set_id(value)

    def is_leaf(self):
        """Returns true if the node doesn't have children nodes"""
        if len(self.children) == 0:
            return True
        else:
            return False

    def set_parent(self, nid):
        """Sets the patent"""
        self.parent = nid

    def add_child(self, nid):
        """Adds a child"""
        self.children.append(nid)

    def __repr__(self):
        name = self.__class__.__name__
        args = [
            "tag=%r" % self.tag,
            "identifier=%r" % self.identifier,
            "data=%r" % self.data
        ]
        return "%s(%s)" % (name, ", ".join(args))
