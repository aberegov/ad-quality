from copy import deepcopy
from com.conversant.common.Node import Node


class NodeIdNotFound(Exception):
    """Exception thrown if a node's identifier is unknown"""
    pass


class NodeIdDuplicate(Exception):
    pass


class RootNodeAlreadyExists(Exception):
    pass


class Tree(object):
    (ROOT, DEPTH, WIDTH) = list(range(3))

    def __init__(self, tree=None, deep=False):
        """ Create a new tree as a new or cloned if the tree parameter is specified
        Args:
            :param tree (Tree): A tree to clone from if it is specified
            :param deep (bool): Indicates whether to perform a deep copy
        """
        self.nodes_dict = {}

        self.tags_index = {}

        self.root = None

        if tree is not None:
            self.root = tree.root
            if deep:
                for nid in tree.nodes:
                    self.nodes_dict[nid] = deepcopy(tree.nodes[nid])
                else:
                    self.nodes_dict = tree.nodes

    @property
    def nodes(self):
        """
        :return: a dict form of nodes in a tree: {id: node_instance}
        """
        return self.nodes_dict

    def get_node(self, nid):
        """
        Returns a node with the given identifier
        :param nid: the node identifier
        :return: The node object or None
        """
        if nid is None or not self.__contains__(nid):
            return None
        return self.nodes_dict[nid]

    def add_node(self, node, parent=None):
        """
        Adds a new node to the tree
        :param node: the node to add
        :param parent: the identifier of a parent node
        :return:
        """
        if not isinstance(node, Node):
            raise OSError("The node parameter must be of Node type")

        if node.identifier in self.nodes_dict:
            raise NodeIdDuplicate("The node (id=%s tag=%s) is already in the tree" % (node.identifier, node.tag))

        if parent is None:
            if self.root is not None:
                raise RootNodeAlreadyExists("The tree already has a root (id=%s)" % self.root)
            else:
                self.root = node.identifier
        elif parent not in self.nodes_dict:
            raise NodeIdNotFound("The parent with ID %s is not in tree" % parent)

        self.nodes_dict.update({node.identifier: node})
        self.tags_index.update({node.identifier: {}})

        if parent is not None:
            self.nodes_dict[parent].add_child(node.identifier)
            self.tags_index[parent].update({node.tag: node.identifier})
            node.set_parent(parent)

    def node_by_path(self, tags, default='-1'):
        """
        Returns a node for the given tags path. Since tags are not unique, the only first match is returned
        :param tags: the path
        :param default:
        :return:
        """

        current = self.root
        for tag in tags:
            tag = tag if tag in self.tags_index[current] else default
            current = self.tags_index[current][tag]

        return self[current]

    def build_path(self, tags, data):
        node = None
        current = self.root
        for tag in tags:
            if tag not in self.tags_index[current]:
                node = Node(tag)
                self.add_node(node, current)
                current = node.identifier
            else:
                current = self.tags_index[current][tag]

        if node is None:
            print(tags)
            print(len(self.nodes))
            print(self.nodes[current])
            raise Exception("Can't build a tree path for %s" % str(tags))

        node.data = data
        return node

    def __contains__(self, key):
        """
        Indicates whether the tree contains the given key
        :param key: the node identifier
        :return: True of the tree contains the given item; otherwise returns False
        """
        return [nid for nid in self.nodes_dict if nid == key]

    def __getitem__(self, key):
        try:
            return self.nodes_dict[key]
        except KeyError:
            raise NodeIdNotFound("Node % s is not found in the tree" % key)

    def __len__(self):
        return len(self.nodes_dict)

    def __setitem__(self, key, value):
        self.nodes_dict.update({key: value})

    def __str__(self):
        self.reader = ""

        def write(line):
            self.reader += line.decode('utf-8') + "\n"

        self.__print_backend(func=write)
        return self.reader

    def __print_backend(self, nid=None, level=ROOT, filtering=None, line_type='ascii-ex', func=print):
        for prefix, node in self.__get(nid, level, filtering, line_type):
            label = "%s[%s] %s" % (node.tag, node.identifier, node.data if node.data is not None else '')
            func('{0}{1}'.format(prefix, label).encode('utf-8'))

    def __get(self, nid, level, filtering, line_type):
        if filtering is None:
            def filtering(node):
                return True

        dt = {
            'ascii': ('|', '|-- ', '+-- '),
            'ascii-ex': ('\u2502', '\u251c\u2500\u2500 ', '\u2514\u2500\u2500 '),
            'ascii-exr': ('\u2502', '\u251c\u2500\u2500 ', '\u2570\u2500\u2500 '),
            'ascii-em': ('\u2551', '\u2560\u2550\u2550 ', '\u255a\u2550\u2550 '),
            'ascii-emv': ('\u2551', '\u255f\u2500\u2500 ', '\u2559\u2500\u2500 '),
            'ascii-emh': ('\u2502', '\u255e\u2550\u2550 ', '\u2558\u2550\u2550 '),
        }[line_type]

        return self.__get_iterator(nid, level, filtering, dt, [])

    def __get_iterator(self, nid, level, filtering, dt, is_last):
        dt_v_line, dt_inter_con, dt_last_con = dt

        nid = self.root if (nid is None) else nid
        node = self[nid]

        if level == self.ROOT:
            yield "", node
        else:
            leading = ''.join(map(lambda x: dt_v_line + ' ' * 3 if not x else ' ' * 4, is_last[0:-1]))
            lasting = dt_last_con if is_last[-1] else dt_inter_con
            yield leading + lasting, node

        if filtering(node):
            children = [self[i] for i in node.children if filtering(self[i])]
            last_index = len(children) - 1

            level += 1
            for i, child in enumerate(children):
                is_last.append(i == last_index)
                for item in self.__get_iterator(child.identifier, level, filtering, dt, is_last):
                    yield item
                is_last.pop()

    def clear(self):
        self.tags_index.clear()
        self.nodes_dict.clear()