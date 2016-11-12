from com.conversant.common.Node import Node


class NodeNotFound(Exception):
    pass


class NodeDuplicate(Exception):
    pass


class RootNodeAlreadyExists(Exception):
    pass


class Tree(object):
    def __init__(self):
        self.nodes_map = {}
        self.root = None

    @property
    def nodes(self):
        return self.nodes_map

    def get_node(self, nid):
        return self.nodes_map[nid] if nid in self.nodes_map else None

    def add_node(self, node, parent=None):
        if not isinstance(node, Node):
            raise OSError("The node parameter must be of Node type")

        if node.identifier in self.nodes_map:
            raise NodeDuplicate("The node (id=%s name=%s) is already in the tree" % (node.identifier, node.name))

        if parent is None:
            if self.root is not None:
                raise RootNodeAlreadyExists("The tree already has a root (id=%s)" % self.root)
            else:
                self.root = node.identifier
        elif parent not in self.nodes_map:
            raise NodeNotFound("The parent with ID %s is not in tree" % parent)

        self.nodes_map.update({node.identifier: node})

        if parent is not None:
            self.nodes_map[parent].add_child(node)

    def build_path(self, node_names, data):
        node = None
        nid = self.root
        for name in node_names:
            if name not in self[nid].children:
                node = Node(name)
                self.add_node(node, nid)
                nid = node.identifier
            else:
                nid = self[nid].children[name]

        if node is None:
            raise Exception("Can't build a tree path for %s" % str(node_names))

        node.data = data
        return node

    def match_path(self, match_names, nid=None, index=0, wildcard='-1'):
        if nid is None:
            nid = self.root

        if index >= len(match_names):
            return self[nid].data

        name = match_names[index]
        branches = self[nid].children

        for o in [name, wildcard]:
            if o in branches:
                data = self.match_path(match_names, branches[o], index + 1)
                if data is not None:
                    return data
        return None

    def node_by_path(self, path_names, wildcard='-1'):
        nid = self.root
        for names in path_names:
            branches = self[nid].children
            if names in branches:
                nid = branches[names]
            elif wildcard in branches:
                nid = branches[wildcard]
            else:
                raise KeyError('Cannot find a match for %s from %s' % (names, str(path_names)))
        return self[nid]

    def __contains__(self, key):
        return [nid for nid in self.nodes_map if nid == key]

    def __getitem__(self, key):
        try:
            return self.nodes_map[key]
        except KeyError:
            raise NodeNotFound("Node % s is not found in the tree" % key)

    def __len__(self):
        return len(self.nodes_map)

    def __setitem__(self, key, value):
        self.nodes_map.update({key: value})

    def clear(self):
        self.nodes_map.clear()
