from copy import deepcopy
from com.conversant.common.Node import Node


class NodeNotFound(Exception):
    """Exception thrown if a node's identifier is unknown"""
    pass


class NodeDuplicate(Exception):
    pass


class RootNodeAlreadyExists(Exception):
    pass


class Tree(object):
    def __init__(self, tree=None, deep=False):
        """ Create a new tree as a new or cloned if the tree parameter is specified
        Args:
            :param tree (Tree): A tree to clone from if it is specified
            :param deep (bool): Indicates whether to perform a deep copy
        """
        self.nodes_map = {}

        self.child_tag = {}

        self.root = None

        if tree is not None:
            self.root = tree.root
            if deep:
                for nid in tree.nodes:
                    self.nodes_map[nid] = deepcopy(tree.nodes[nid])
                else:
                    self.nodes_map = tree.nodes

    @property
    def nodes(self):
        """
        :return: a dict form of nodes in a tree: {id: node_instance}
        """
        return self.nodes_map

    def get_node(self, nid):
        """
        Returns a node with the given identifier
        :param nid: the node identifier
        :return: The node object or None
        """
        if nid is None or not self.__contains__(nid):
            return None
        return self.nodes_map[nid]

    def add_node(self, node, parent=None):
        """
        Adds a new node to the tree
        :param node: the node to add
        :param parent: the identifier of a parent node
        :return:
        """
        if not isinstance(node, Node):
            raise OSError("The node parameter must be of Node type")

        if node.identifier in self.nodes_map:
            raise NodeDuplicate("The node (id=%s tag=%s) is already in the tree" % (node.identifier, node.tag))

        if parent is None:
            if self.root is not None:
                raise RootNodeAlreadyExists("The tree already has a root (id=%s)" % self.root)
            else:
                self.root = node.identifier
        elif parent not in self.nodes_map:
            raise NodeNotFound("The parent with ID %s is not in tree" % parent)

        self.nodes_map.update({node.identifier: node})
        self.child_tag.update({node.identifier: {}})

        if parent is not None:
            self.nodes_map[parent].add_child(node.identifier)
            self.child_tag[parent].update({node.tag: node.identifier})
            node.set_parent(parent)

    def path_best_match(self, tags):
        (scores, data) = self.path_traverse(tags, self.root)
        if scores is None:
            raise Exception("Can't find predictors for %s" % str(tags))

        a = [int(s, 2) for s in scores]
        return data[a.index(max(a))]

    def path_traverse(self, tags, nid, index=0, score='0', default='-1'):
        if index >= len(tags):
            return [score], [self[nid].data]

        scores = []
        data = []

        tag = tags[index]
        downstream = self.child_tag[nid]

        if tag in downstream:
            s, d = self.path_traverse(tags, downstream[tag], index + 1, '1' + score)
            if s is not None:
                scores.extend(s)
                data.extend(d)

        if default in downstream:
            s, d = self.path_traverse(tags, downstream[default], index + 1, '0' + score)
            if s is not None:
                scores.extend(s)
                data.extend(d)

        return (scores, data) if len(scores) > 0 else (None, None)

    def node_by_path(self, tags, default='-1'):
        """
        Returns a node for the given tags path. Since tags are not unique, the only first match is returned
        :param tags: the path
        :param default:
        :return:
        """
        nid = self.root
        for tag in tags:
            downstream = self.child_tag[nid]
            if tag in downstream:
                nid = downstream[tag]
            elif default in downstream:
                nid = downstream[default]
            else:
                raise KeyError('Cannot find a match for %s from %s (%s)' % (tag, str(tags), str(self.parent_node(nid))))
        return self[nid]

    def build_path(self, tags, data):
        node = None
        nid = self.root
        for tag in tags:
            if tag not in self.child_tag[nid]:
                node = Node(tag)
                self.add_node(node, nid)
                nid = node.identifier
            else:
                nid = self.child_tag[nid][tag]

        if node is None:
            raise Exception("Can't build a tree path for %s" % str(tags))

        node.data = data
        return node

    def parent_node(self, nid):
        node = self[nid]
        return self[node.parent_node]

    def __contains__(self, key):
        """
        Indicates whether the tree contains the given key
        :param key: the node identifier
        :return: True of the tree contains the given item; otherwise returns False
        """
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
        self.child_tag.clear()
        self.nodes_map.clear()