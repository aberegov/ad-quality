import unittest

from unittest.mock import MagicMock
from com.conversant.common.URLEndpoint import URLEndpoint
from com.conversant.viewability.BidExpert import BidExpert

class BidExpertTestCase(unittest.TestCase):
    def setUp(self):
        endpoint = URLEndpoint('https://www.google.com/finance/info?q={0}')
        endpoint.getContent = MagicMock(return_value = '{"segment_ids": ["840","402"]}')
        self.expert = BidExpert(endpoint)

    def tearDown(self):
        self.expert = None

    def handler(self, output):
        self.assertEqual({1 : 'NASDAQ:AAPL', 2 : 'NASDAQ:GOOGL'}[output[1]], output[0])

    def test_run(self):
        self.expert.run([['NASDAQ:AAPL',1], ['NASDAQ:GOOGL',2]], self.handler)
