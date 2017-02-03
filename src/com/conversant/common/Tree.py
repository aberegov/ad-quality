from com.conversant.common.Node import Node


class NodeNotFound(Exception):
    pass


class NodeDuplicate(Exception):
    pass


class RootExists(Exception):
    pass


class Tree(object):
    def __init__(self):
        self.root_nid = None
        self.nodes = {}

    def root_node(self):
        return self[self.root_nid]

    def get_node(self, nid):
        return self.nodes[nid] if nid in self.nodes else None

    def add_node(self, node, parent_nid=None):
        if node.identifier in self.nodes:
            raise NodeDuplicate("Duplicate node %s" % str(node))

        if parent_nid is None and self.root_nid is not None:
            raise RootExists("The tree already has a root %s" % self.root_nid)

        if parent_nid is not None and parent_nid not in self.nodes:
            raise NodeNotFound("The parent node %s is not in tree" % parent_nid)

        if parent_nid is not None:
            self.nodes[parent_nid].add_child(node)
        else:
            self.root_nid = node.identifier

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

    def __str__(self):
        self.reader = ""

        def write(line):
            self.reader += line.decode('utf-8') + "\n"

        self.__print_backend(func=write)
        return self.reader

    def __print_backend(self, nid=None, level=0, filtering=None, line_type='ascii-ex', func=print):
        for prefix, node in self.__get(nid, level, filtering, line_type):
            label = "%s" % node.name
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

        nid = self.root_nid if (nid is None) else nid
        node = self[nid]

        if level == 0:
            yield "", node
        else:
            leading = ''.join(map(lambda x: dt_v_line + ' ' * 3 if not x else ' ' * 4, is_last[0:-1]))
            lasting = dt_last_con if is_last[-1] else dt_inter_con
            yield leading + lasting, node

        if filtering(node):
            children = [self[nid] for name, nid in node.children.items() if filtering(self[nid])]
            last_index = len(children) - 1

            level += 1
            for i, child in enumerate(children):
                is_last.append(i == last_index)
                for item in self.__get_iterator(child.identifier, level, filtering, dt, is_last):
                    yield item
                is_last.pop()
