import  unittest

from com.conversant.viewability.BidExpertSegments import BidExpertSegments

class BigExpertSegmentsTestCase(unittest.TestCase):
    expert = None

    def tearDown(self):
        self.expert.clear()
        self.expert = None

    def assertSegments(self, mask, segments):
        self.expert = BidExpertSegments(segments)
        video = self.expert.video()
        for m, v in zip(mask, video):
            self.assertEqual(m, v)

    def test_video40(self):
        self.assertSegments([1, 0, 0, 0, 0], '{"segment_ids": ["840","402"]}')

    def test_video50(self):
        self.assertSegments([0, 1, 0, 0, 0], '{"segment_ids": ["850","402"]}')

    def test_video4050(self):
        self.assertSegments([1, 1, 0, 0, 0], '{"segment_ids": ["850","840"]}')

    def test_video_all(self):
        self.assertSegments([1, 1, 1, 1, 1], '{"segment_ids": ["840","850","860","870","880","401"]}')

    def test_video_none(self):
        self.assertSegments([0, 0, 0, 0, 0], '{"segment_ids": ["140","150","160","170","180","401"]}')

    def suite(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(BigExpertSegmentsTestCase)
        return suite

