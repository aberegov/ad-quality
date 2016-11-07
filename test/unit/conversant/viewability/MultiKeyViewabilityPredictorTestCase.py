import unittest
from decimal import Decimal
from com.conversant.viewability.MultiKeyViewabilityPredictor import MultiKeyViewabilityPredictor


class MultiKeyViewabilityPredictorTestCase(unittest.TestCase):
    def setUp(self):
        self.predictor = MultiKeyViewabilityPredictor()

    def tearDown(self):
        self.predictor.clear()

    def test_predict(self):
        self.predictor.build()
        self.assertEqual(round(Decimal(0.15838), 5),
                         round(self.predictor.predict([
                             '14200',
                             '558570',
                             '-1',
                             '17',
                             '-1',
                             '-1',
                             '-1',
                             '-1',
                             '-1',
                             '-1']), 5))
