import unittest
from com.conversant.common.Node import Node


class NodeTestCase(unittest.TestCase):
    def test_defined_id(self):
        node = Node("node", 1)
        self.assertEqual(1, node.identifier)
        self.assertEqual("node", node.tag)

    def test_generated_id(self):
        node = Node("node")
        self.assertIsNotNone(node.identifier)
        self.assertEqual("node", node.tag)

    def test_set_id(self):
        node = Node("node")
        node.identifier = 5
        self.assertEqual(5, node.identifier)

    def test_parent(self):
        node = Node("node")
        self.assertIsNone(node.parent)

    def test_add_child(self):
        node = Node("1")
        node.add_child('11')
        self.assertEqual('11', node.children[0])

    def test_add_children(self):
        node = Node('1')
        node.add_child('11')
        node.add_child('12')
        self.assertEqual(2, len(node.children))
        self.assertEqual('11', node.children[0])
        self.assertEqual('12', node.children[1])
