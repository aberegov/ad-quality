import unittest
from com.conversant.common.Node import Node


class NodeTestCase(unittest.TestCase):
    def test_defined_id(self):
        node = Node("node", 1)
        self.assertEqual(1, node.identifier)

    def test_generated_id(self):
        node = Node("node")
        self.assertIsNotNone(node.identifier)

    def test_set_id(self):
        node = Node("node")
        node.identifier = 5
        self.assertEqual(5, node.identifier)

    def test_parent(self):
        node = Node("node")
        self.assertIsNone(node.parent)

