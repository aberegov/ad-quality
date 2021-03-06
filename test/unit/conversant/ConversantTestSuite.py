import unittest

from unit.conversant.viewability.MultiKeyTestCase import MultiKeyTestCase
from unit.conversant.viewability.BigExpertSegmentsTestCase import BigExpertSegmentsTestCase
from unit.conversant.common.URLEndpointTestCase import URLEndpointTestCase
from unit.conversant.common.URLResourceTestCase import URLResourceTestCase
from unit.conversant.common.EnvConfigTestCase import EnvConfigTestCase
from unit.conversant.common.SQLCommanderTestCase import SQLCommanderTestCase
from unit.conversant.common.SQLShellTestCase import SQLShellTestCase
from unit.conversant.common.TreeTestCase import TreeTestCase
from unit.conversant.common.NodeTestCase import NodeTestCase
from unit.conversant.common.SlidingBufferTestCase import SlidingBufferTestCase


class ConversantTestSuite(unittest.TestCase):
    def suite(self):
        suite = unittest.TestSuite([
            URLResourceTestCase().suite()
            ,URLEndpointTestCase().suite()
            ,EnvConfigTestCase().suite()
            ,BigExpertSegmentsTestCase().suite()
            ,SQLCommanderTestCase().suite()
            ,SQLShellTestCase().suite()
            ,TreeTestCase.suite()
            ,NodeTestCase.suite()
            ,SlidingBufferTestCase.suite()
            ,MultiKeyTestCase.suite()
        ])

        return suite
