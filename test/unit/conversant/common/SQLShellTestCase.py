import unittest
from com.conversant.common.SQLShell import SQLShell


class SQLShellTestCase(unittest.TestCase):
    def setUp(self):
        self.shell = SQLShell()

    def tearDown(self):
        self.shell.close()
        self.shell = None

    def processRow(self, row):
        self.assertEqual(123456, row[0])

    def test_execute_success(self):
        self.shell.execute('select 123456', {}, self.processRow)
