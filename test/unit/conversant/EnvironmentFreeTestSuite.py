import unittest

from unit.conversant.viewability.MultiKeyTestCase import MultiKeyTestCase
from unit.conversant.common.TreeTestCase import TreeTestCase
from unit.conversant.common.NodeTestCase import NodeTestCase
from unit.conversant.common.KeyHierarchyTestCase import KeyHierarchyTestCase
from unit.conversant.common.SlidingBufferTestCase import SlidingBufferTestCase


class EnvironmentFreeTestSuite(unittest.TestCase):
    def suite(self):
        suite = unittest.TestSuite([
            TreeTestCase.suite()
            ,KeyHierarchyTestCase.suite()
            ,NodeTestCase.suite()
            ,SlidingBufferTestCase.suite()
            ,MultiKeyTestCase.suite()
        ])

        return suite
