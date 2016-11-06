import sys
import json
from copy import deepcopy
from io import BytesIO

class NodeIdNotFound(Exception):
    """Exception thrown if a node's identifier is unknown"""
    pass


class Tree(object):
    (ROOT, DEPTH, WIDTH, ZIGZAG) = list(range(4))

    def __init__(self, tree=None, deep=False):
        # Nodes: dictionary id: node
        self._nodes = {}

        self.root = None

        if tree is not None:
            self.root = tree.root
            if deep:
                for nid in tree._nodes:
                    self._nodes[nid] = deepcopy(tree._nodes[nid])
                else:
                    self._nodes = tree._nodes

    def __contains__(self, item):
        return [node for node in self._nodes if node == item]

    def __getitem__(self, key):
        try:
            return self._nodes[key]
        except KeyError:
            raise NodeIdNotFound("Node % s is not found in the tree" % key)

    def __len__(self):
        return len(self._nodes)

    def __setitem__(self, key, value):
        self._nodes.update({key: value})

    def __str__(self):
        self.reader = ""

        def write(line):
            self.reader += line.decode('utf-8') + "\n"

        self.__print_backend(func=write)
        return self.reader

    def __print_backend(self, nid=None, level=ROOT, filtering=None, line_type='ascii-ex', func=print):
        for prefix, node in self.__get(nid, level, filtering, line_type):
            label = "%s[%s]" % (node.tag, node.identifier)
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


