from com.conversant.common.SlidingBuffer import SlidingBuffer


class ViewabilityController:
    (VIEW, MEASURE) = range(2)
    predictor_types = ['viewability', 'measurability']

    def __init__(self, goal, predictor, n=1000000, w=10000, l=10000, e=0.1):
        self.goal = goal
        self.threshold = goal
        self.e = e
        self.n = n
        self.predictor = predictor
        self.actual = [SlidingBuffer(l), SlidingBuffer(l)]
        self.estimate = [SlidingBuffer(w), SlidingBuffer(w)]
        self.impressions = 0

    @property
    def elapsed(self):
        return float(self.impressions / self.n)

    @property
    def actual_rate(self):
        return float(self.actual[self.VIEW].total / self.actual[self.MEASURE].total) \
            if self.actual[self.MEASURE].total > 0 else None

    @property
    def historical_rate(self):
        return float(self.actual[self.VIEW].sunk / self.actual[self.MEASURE].sunk) \
            if self.actual[self.MEASURE].sunk > 0 else None

    @property
    def window_rate(self):
        return float(self.estimate[self.VIEW].sum / self.estimate[self.MEASURE].sum)\
            if self.estimate[self.MEASURE].sum > 0 else None

    @property
    def target(self):
        return float((self.goal - self.elapsed * self.historical_rate) / (1 - self.elapsed)) \
            if self.historical_rate is not None else self.goal

    def process_event(self, imp, output):
        if self.impressions > self.n:
            return

        # make predictions
        predictors = self.predictor.predict_all(self.predictor_types, imp[:-2])

        # calculate threshold
        if self.window_rate is not None:
            self.threshold += self.e * (self.target - self.window_rate)

        # make decision
        if predictors[self.VIEW] >= self.threshold:
            # record event
            self.impressions += 1
            for x in [self.VIEW, self.MEASURE]:
                self.estimate[x].add(float(predictors[x]))
                self.actual[x].add(imp[x - 2])

            # output event information and decision
            output([
                self.threshold,
                self.window_rate,
                self.actual_rate,
                predictors[self.VIEW],
                predictors[self.MEASURE],
                imp[-2],
                imp[-1]
            ])
