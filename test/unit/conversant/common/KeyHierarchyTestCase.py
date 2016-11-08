import unittest
from com.conversant.common.KeyHierarchy import KeyHierarchy

class KeyHierarchyTestCase(unittest.TestCase):
    def setUp(self):
        self.hierarchies = KeyHierarchy(['key0', 'key1', 'key2', 'key3', 'key4'])

    def tearDown(self):
        self.hierarchies.clear()
        del self.hierarchies

    def test_index0(self):
        self.assertListEqual(
            [2, 3, 1, 0, 4], self.hierarchies.index(['key2', 'key3', 'key1', 'key0', 'key4']))

    def test_index1(self):
        self.assertListEqual(
            [1, 2, 3, 4, 0], self.hierarchies.index(['key1', 'key2', 'key3', 'key4', 'key0']))

    def test_add(self):
        self.hierarchies.set('h', ['key2', 'key3', 'key1', 'key0', 'key4'])
        self.assertListEqual(
            ['data2', 'data3', 'data1', 'data0', 'data4'],
            self.hierarchies.reorder('h', ['data0', 'data1', 'data2', 'data3', 'data4']))

    def test_reorder(self):
        self.hierarchies.set('h', ['key2', 'key3', 'key1', 'key0', 'key4'])
        self.assertListEqual(
            ['data0', 'data1', 'data2', 'data3', 'data4'],
            self.hierarchies.reorder('m', ['data0', 'data1', 'data2', 'data3', 'data4']))

