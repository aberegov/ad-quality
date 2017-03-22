import unittest
from com.conversant.viewability.ViewabilityGldEvaluator import ViewabilityGldEvaluator


class ViewabilityGldEvaluatorTestCase(unittest.TestCase):
    def setUp(self):
        self.eval = ViewabilityGldEvaluator()

    def tearDown(self):
        self.eval = None

    def test_view_eval(self):
        self.eval.set_params({
            'dtmid': 574903730095077103,
            'companyId': 2997,
            'msgCampaignId': 23254,
            'network_id': 19998,
            'site_id': 185129,
            'request_type_id': 1,
            'supply_type_id': 4,
            'ad_position': 1,
            'media_size': 11,
            'userAgent': 'Mozilla%2F5.0%2B(Linux%3BAndroid%2B7.2%3B%2BLGLS991%2BBuild%2FLMY47D%3B%2Bwv)%2BAppleWebKit%2F537.36(KHTML%2Clike%2BGecko)%2BVersion%2F4.0%2BChrome%2F56.0.2526.77%2BMobile%2BSafari%2F537.36%5BFB_IAB%2FFB4A%3BFBAV%2F56.0.0.23.68%3B%5D',

        })
        self.eval.evaluate()
        print(self.eval.get_data())