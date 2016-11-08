import unittest
from decimal import Decimal
from com.conversant.viewability.MultiKeyPredictor import MultiKeyPredictor


class MultiKeyPredictorTestCase(unittest.TestCase):
    def setUp(self):
        self.predictor = MultiKeyPredictor()

    def tearDown(self):
        self.predictor.clear()

    def test_predict(self):
        self.predictor['viewability'] = self.predictor.multi_key.keys
        self.predictor.build()
        self.assertEqual(round(Decimal(0.81043), 5),
                        round(self.predictor.predict('viewability',
                          ['0','15900','537114956','537203316','18','-1','Other','Windows 10','Firefox','49']), 5))