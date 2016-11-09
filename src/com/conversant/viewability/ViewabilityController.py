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
    def compensating_rate(self):
        return float((self.goal - self.elapsed * self.historical_rate) / (1 - self.elapsed)) \
            if self.historical_rate is not None else self.goal

    def process_event(self, imp, output):
        if self.impressions > self.n:
            return

        # make predictions
        predictors = self.predictor.predict_all(self.predictor_types, imp[1:-2])

        # P(in_view) = P(in_view|measured) x P(measured)
        prob_in_view = float(predictors[self.VIEW]) * float(predictors[self.MEASURE])

        # calculate the threshold
        if self.window_rate is not None:
            # T[t] = T[t-1] + e x (target - current)
            self.threshold += self.e * (self.compensating_rate - self.window_rate)

        # make the decision
        if prob_in_view >= self.threshold:
            # record predictors and actual
            self.impressions += 1

            # sum of in-view impressions
            self.actual[self.VIEW].add(imp[-2])

            # sum of measured impressions
            self.actual[self.MEASURE].add(imp[-1])

            # Estimate for the number of in-view impressions: N(in-view) = N x P(in-view|measured) x P(measured)
            self.estimate[self.VIEW].add(prob_in_view)

            # Estimate for the n umber of measured impressions: N(measured) = N x P(measured)
            self.estimate[self.MEASURE].add(float(predictors[self.MEASURE]))

            # output the event information and stats
            output([imp[0],
                self.threshold,
                self.window_rate,
                self.actual_rate,
                prob_in_view,
                predictors[self.MEASURE],
                imp[-2],
                imp[-1]
            ])
