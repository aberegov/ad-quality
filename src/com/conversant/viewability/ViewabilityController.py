from com.conversant.common.SlidingBuffer import SlidingBuffer

class ViewabilityController:
    def __init__(self, goal, predictor, period=1000000, window=10000, freshness=10000, e=0.1):
        self.threshold = goal
        self.goal = goal
        self.e = e
        self.period = period
        self.predictor = predictor
        self.actual = {'measured': SlidingBuffer(freshness), 'viewable' :  SlidingBuffer(freshness)}
        self.estimate = {'measured': SlidingBuffer(window), 'viewable' :  SlidingBuffer(window)}
        self.impressions = 0

    @property
    def elapsed(self):
        return self.impressions / self.period

    @property
    def historical_rate(self):
        return self.actual['viewable'].sunk \
               / self.actual['measured'].sunk if self.actual['measured'].sunk > 0 else 0

    @property
    def window_rate(self):
        return self.estimate['viewable'].sum \
               / self.estimate['measured'].sum if self.estimate['measured'].sum > 0 else 0

    def process_event(self, imp):
        # Make predictions
        pv = self.predictor.predict(  'viewability', imp[0:-2])
        pm = self.predictor.predict('measurability', imp[0:-2])

        # calculate compensating target and threshold
        if self.impressions > 100:
            target = (self.goal - self.elapsed * self.historical_rate()) / (1 - self.elapsed)
            self.threshold += self.e * (target - self.window_rate())

        # make bid / no-bid decision
        if pv > self.threshold:
            self.impressions += 1
            self.estimate['viewable'].add(pv)
            self.estimate['measured'].add(pm)
            self.actual['viewable'].add(imp[-1])
            self.actual['measured'].add(imp[-2])
