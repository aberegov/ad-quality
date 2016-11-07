import unittest
from com.conversant.common.DatabaseTree import DatabaseTree


class DatabaseTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.tree = DatabaseTree("""
        SELECT
            network_id::varchar,
            seller_id,
            site_id,
            ad_format_id::varchar,
            media_size::varchar,
            ad_position::varchar,
            browser_name,
            browser_version,
            os,
            device,
            predictor_value
        FROM
            adquality.viewability_predictors
        WHERE
            predictor_type = 'viewability'
            """)

    def tearDown(self):
        del self.tree

    def test_build(self):
        self.tree.build()
