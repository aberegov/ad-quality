import unittest

from com.conversant.common.SQLCommander import SQLCommander
from com.conversant.common.EnvConfig import EnvConfig


class SQLCommanderTestCase(unittest.TestCase):
    def setUp(self):
        config = EnvConfig()
        self.command = SQLCommander(
            config.get('database', 'login'),
            config.get('database', 'password'),
            config.get('database', 'host'),
            config.get('database', 'database'))

    def tearDown(self):
        self.command.close();

    def processRow(self, row):
        self.assertEqual(123456, row[0])

    def test_execute_success(self):
        self.command.execute('select 123456', {}, self.processRow)

    @unittest.expectedFailure
    def test_closed_connection(self):
        self.command.close();
        self.command.execute('select 123456', {}, self.processRow)

    def test_double_close(self):
        self.command.close()
        self.command.close()