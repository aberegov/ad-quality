import unittest
from com.conversant.common.EnvConfig import EnvConfig

class EnvConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.config = EnvConfig()

    def tearDown(self):
        self.config = None


    def test_get(self):
        self.assertEqual('value0',self.config.get('example', 'name0'))
        self.assertEqual('value1',self.config.get('example', 'name1'))


    def test_get_no_key(self):
        try:
            c = self.config.get('yyy', 'xxx')
            self.fail('Must throw an exception')
        except KeyError:
            c = None
