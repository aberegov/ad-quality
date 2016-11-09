import unittest
from com.conversant.viewability.MultiKey import MultiKey


class MultiKeyTestCase(unittest.TestCase):
    def setUp(self):
        self.hierarchies = MultiKey([
            'ad_format_id',
            'network_id',
            'seller_id',
            'site_id',
            'media_size',
            'ad_position',
            'device',
            'os',
            'browser_name',
            'browser_version'
        ])

    def test_assign(self):
        self.hierarchies['name'] = [
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

        self.assertListEqual(
            [
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
            ],
            self.hierarchies.reorder('name', [
                'ad_format_id',
                'network_id',
                'seller_id',
                'site_id',
                'media_size',
                'ad_position',
                'device',
                'os',
                'browser_name',
                'browser_version'
            ] ))

