import unittest
from com.conversant.common.Tree import Tree
from com.conversant.common.Node import Node


class TreeTestCase(unittest.TestCase):
    def setUp(self):
        self.tree = Tree()

    def tearDown(self):
        self.tree.clear()
        del self.tree

    def init_tree(self):
        self.tree.add_node(Node('001', '001'))
        self.tree.add_node(Node('011', '011'), '001')
        self.tree.add_node(Node('012', '012'), '001')
        self.tree.add_node(Node('013', '013'), '001')
        self.tree.add_node(Node('111', '111'), '011')
        self.tree.add_node(Node('112', '112'), '011')

    def test_add_node(self):
        node = Node('node')
        self.tree.add_node(node)
        self.assertEqual('node', self.tree.nodes[node.identifier].tag)
        self.assertEqual(node.identifier, self.tree.root)

    @unittest.expectedFailure
    def test_second_root(self):
        self.tree.add_node(Node('node'))
        self.tree.add_node(Node('root'))

    @unittest.expectedFailure
    def test_double_add(self):
        node = Node('node')
        self.tree.add_node(node)
        self.tree.add_node(node)

    def test_create_tree(self):
        self.init_tree()
        self.assertEquals(6, len(self.tree.nodes))
        self.assertEquals(3, len(self.tree['001'].children))
        self.assertEquals(2, len(self.tree['011'].children))
        self.assertEquals(0, len(self.tree['012'].children))

    def test_node_by_path(self):
        self.init_tree()
        node = self.tree.node_by_path(['011', '111'])
        self.assertEquals('111', node.identifier)

    def test_build_path(self):
        self.init_tree()
        self.tree.build_path(['011', '111', '1111', '11111'], '12345')
        node = self.tree.node_by_path(['011', '111', '1111', '11111'])
        self.assertEquals('12345', node.data)

    def test_create_tree(self):
        self.tree.add_node(Node('root'))
        self.tree.build_path(['14200', '558570', '-1', '17', '-1', '-1', '-1', '-1', '-1', '-1'], 0.5)