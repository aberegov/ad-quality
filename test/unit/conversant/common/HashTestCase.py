import unittest

from com.conversant.common.Hash import fnv64
class HashTestCase(unittest.TestCase):

    def test_fnv64(self):
        h = fnv64('com.grindrapp.android')
        print(h)

