from com.conversant.common.Node import Node


class NodeNotFound(Exception):
    pass


class NodeDuplicate(Exception):
    pass


class RootNodeAlreadyExists(Exception):
    pass


class Tree(object):
    def __init__(self):
        self.root_nid = None
        self.nodes = {}

    def get_node(self, nid):
        return self.nodes[nid] if nid in self.nodes else None

    def add_node(self, node, parent_nid=None):
        if not isinstance(node, Node):
            raise Exception("The node parameter must be of Node type")

        if node.identifier in self.nodes:
            raise NodeDuplicate("Duplicate node %s" % str(node))

        if parent_nid is None:
            if self.root_nid is not None:
                raise RootNodeAlreadyExists("The tree already has a root (id=%s)" % self.root_nid)
            else:
                self.root_nid = node.identifier
        elif parent_nid not in self.nodes:
            raise NodeNotFound("The parent node ID %s is not in tree" % parent_nid)

        if parent_nid is not None:
            self.nodes[parent_nid].add_child(node)

        self.nodes.update({node.identifier: node})

    def build_path(self, node_names, value):
        node = None
        nid = self.root_nid
        for name in node_names:
            if name not in self[nid].children:
                node = Node(name)
                self.add_node(node, nid)
                nid = node.identifier
            else:
                nid = self[nid].children[name]

        if node is None:
            raise Exception("Can't build a tree path for %s" % str(node_names))

        node.value = value
        return node

    def match_path(self, match_names, nid=None, index=0, wildcard='-1'):
        if nid is None:
            nid = self.root_nid

        if index >= len(match_names):
            return self[nid]

        name = match_names[index]
        branches = self[nid].children

        for o in [name, wildcard]:
            if o in branches:
                node = self.match_path(match_names, branches[o], index + 1)
                if node is not None:
                    return node
        return None

    def __contains__(self, key):
        return [nid for nid in self.nodes if nid == key]

    def __getitem__(self, key):
        try:
            return self.nodes[key]
        except KeyError:
            raise NodeNotFound("Node %s can't found in the tree" % key)

    def __len__(self):
        return len(self.nodes)

    def clear(self):
        self.nodes.clear()
