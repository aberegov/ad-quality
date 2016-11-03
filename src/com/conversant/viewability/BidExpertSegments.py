
import json

from com.conversant.viewability.Segment import Segment

class BidExpertSegments:
    def __init__(self, data):
        self.doc = json.loads(data)
        self.segments = self.list_to_dict(self.doc['segment_ids'])


    def list_to_dict(self, li):
        dct = {}
        for item in li:
            dct[item] = 1

        return  dct

    def video(self):
        return [
            self.segments.get(Segment.VV40.value, 0),
            self.segments.get(Segment.VV50.value, 0),
            self.segments.get(Segment.VV60.value, 0),
            self.segments.get(Segment.VV70.value, 0),
            self.segments.get(Segment.VV80.value, 0)
        ]

    def clear(self):
            self.doc = None
            self.segments.clear()
            self.segments = None