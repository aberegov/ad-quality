import unittest
from com.conversant.common.DatabaseTree import DatabaseTree


class DatabaseTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.tree = DatabaseTree("""
            select network_id::varchar, site_id, predictor
            from adquality.viewability_predictor
            """)

    def tearDown(self):
        del self.tree

    def test_build(self):
        self.tree.build()
