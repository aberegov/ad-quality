import unittest
from com.conversant.common.Node import Node


class NodeTestCase(unittest.TestCase):
    def test_defined_id(self):
        node = Node("node", 1)
        self.assertEqual(1, node.identifier)
        self.assertEqual("node", node.name)

    def test_generated_id(self):
        node = Node("node")
        self.assertIsNotNone(node.identifier)
        self.assertEqual("node", node.name)

    def test_set_id(self):
        node = Node("node")
        node.identifier = 5
        self.assertEqual(5, node.identifier)

    def test_parent(self):
        node = Node("node")
        self.assertIsNone(node.parent)

    def test_add_child(self):
        node = Node('1')
        node.add_child(Node('11', '011'))
        node.add_child(Node('12', '012'))
        self.assertEqual(2, len(node.children))
        self.assertEqual('011', node.children['11'])
        self.assertEqual('012', node.children['12'])
