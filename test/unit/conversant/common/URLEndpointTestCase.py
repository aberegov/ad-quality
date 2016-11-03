import unittest
import json

from com.conversant.common.URLEndpoint import URLEndpoint

class URLEndpointTestCase (unittest.TestCase):
    def setUp(self):
        self.endpoint = URLEndpoint('https://www.google.com/finance/info?q={0}')

    def test_content_appl(self):
        content = self.endpoint.getContent('NASDAQ:AAPL')
        data = json.loads(content[3:])
        self.assertEqual('AAPL', data[0]['t'])

    def test_content_googl(self):
        content = self.endpoint.getContent('NASDAQ:GOOGL')
        data = json.loads(content[3:])
        self.assertEqual('GOOGL', data[0]['t'])