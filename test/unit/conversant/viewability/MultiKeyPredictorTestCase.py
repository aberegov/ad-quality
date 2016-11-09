import unittest
from decimal import Decimal
from com.conversant.viewability.MultiKeyPredictor import MultiKeyPredictor


class MultiKeyPredictorTestCase(unittest.TestCase):
    def setUp(self):
        self.predictor = MultiKeyPredictor()

    def tearDown(self):
        self.predictor.clear()

    def test_path_best_match(self):
        self.predictor['measurability'] = [
            'ad_format_id',
            'device',
            'os',
            'browser_name',
            'browser_version',
            'media_size',
            'network_id',
            'seller_id',
            'site_id',
            'ad_position'
        ]
        self.predictor.build()
        self.predictor.path_best_match('measureability',
            ['17', '5010', '(null)', '(null)', '29', '(null)', 'Other', 'Windows 10', 'Chrome', '54'])
