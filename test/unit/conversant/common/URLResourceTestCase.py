import unittest

from com.conversant.common.URLResource import URLResource

class URLResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.resource = URLResource('http://www.google.com')

    def tearDown(self):
        self.resource = None

    def test_open(self):
        self.assertIsNotNone(self.resource.read())

    def test_elapsed_wo_open(self):
        self.assertEqual(0, self.resource.elapsed())

    def suite(self):
        suite = unittest.TestSuite()
        suite = unittest.TestLoader().loadTestsFromTestCase(URLResource)
        return suite

