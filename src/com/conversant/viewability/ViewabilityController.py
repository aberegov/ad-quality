from com.conversant.common.SlidingBuffer import SlidingBuffer

class ViewabilityController:
    def __init__(self, goal, predictor, period=1000000, window=10000, freshness=10000):
        self.goal = goal
        self.predictor = predictor
        self.actual_measured = SlidingBuffer(freshness)
        self.actual_viewable = SlidingBuffer(freshness)
        self.predicted_measured = SlidingBuffer(window)
        self.predicted_viewable = SlidingBuffer(window)
        self.impressions = 0

    def processImpression(self, imp):
        self.impressions += 1



