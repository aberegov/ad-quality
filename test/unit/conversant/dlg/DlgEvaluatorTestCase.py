import unittest
from com.conversant.dlg.DlgEvaluator import DlgEvaluator


class DlgEvaluatorTestCase(unittest.TestCase):
    def setUp(self):
        self.eval = DlgEvaluator()

    def tearDown(self):
        self.eval = None

    """
   -- dtmid
        -- companyId
        -- msgCampaignId
        -- isTest
        -- bucketId
        -- base_ecpm
        -- cpm_decay
        -- non_cpm_decay
        -- model_score
        -- userAgent
        -- network_id
        -- seller_id
        -- site_id
        -- request_type_id
        -- supply_type_id
        -- ad_position
        -- media_size
        """

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
            'formula': '%2F%2F+API+v1%0D%0Afun+modelScore+%3A+Real+%2C%0D%0A+viewability+%3A+%7B+performance+%3A+Real%7D%0D%0A+%3D+viewability.performance',
            'userAgent': 'Mozilla%2F5.0%2B(Linux%3BAndroid%2B7.2%3B%2BLGLS991%2BBuild%2FLMY47D%3B%2Bwv)%2BAppleWebKit%2F537.36(KHTML%2Clike%2BGecko)%2BVersion%2F4.0%2BChrome%2F56.0.2526.77%2BMobile%2BSafari%2F537.36%5BFB_IAB%2FFB4A%3BFBAV%2F56.0.0.23.68%3B%5D',

        })
        self.eval.evaluate()
        print(self.eval.get_data())