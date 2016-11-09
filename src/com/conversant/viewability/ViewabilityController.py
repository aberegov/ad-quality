from com.conversant.common.SlidingBuffer import SlidingBuffer


class ViewabilityController:
    def __init__(self, goal, predictor, n=1000000, w=10000, l=10000, e=0.01):
        self.goal = goal
        self.threshold = goal
        self.e = e
        self.n = n
        self.predictor = predictor
        self.actual_in_view = SlidingBuffer(l)
        self.actual_measure = SlidingBuffer(l)
        self.estimate_in_view = SlidingBuffer(w)
        self.estimate_measure = SlidingBuffer(w)
        self.impressions = 0

    @property
    def elapsed(self):
        return float(self.impressions / self.n)

    @property
    def actual_rate(self):
        return float(self.actual_in_view.total / self.actual_measure.total) \
            if self.actual_measure.total > 0 else None

    @property
    def historical_rate(self):
        return float(self.actual_in_view.archived / self.actual_measure.archived) \
            if self.actual_measure.archived > 0 else None

    @property
    def window_rate(self):
        return float(self.estimate_in_view.sum / self.estimate_measure.sum)\
            if self.estimate_measure.sum > 0 else None

    @property
    def compensating_rate(self):
        return float((self.goal - self.elapsed * self.historical_rate) / (1 - self.elapsed)) \
            if self.historical_rate is not None else self.goal

    def process_event(self, imp, output):
        if self.impressions > self.n:
            return

        # extract from impression data, which has the following layout
        # 0     transaction ID
        # 1..k  multi key data
        # -2    actual in view signal
        # -1    actual measured signal
        imp_tid = imp[0]
        imp_mk_data = imp[1:-2]
        imp_in_view = imp[-2]
        imp_measure = imp[-1]

        # make predictions
        prob_in_view = float(self.predictor.predict(  'viewability', imp_mk_data))
        prob_measure = float(self.predictor.predict('measurability', imp_mk_data))

        # calculate the threshold
        if self.window_rate is not None:
            # T[t] = T[t-1] + e x (target - current)
            self.threshold += self.e * (self.compensating_rate - self.window_rate)
            # apply limits [0.1, 0.8] to threshold
            self.threshold = min(0.8, max(0.1, self.threshold))

        # make the decision
        if prob_in_view >= self.threshold:
            # update controller's state variables
            self.impressions += 1

            # Estimate for the number of in-view impressions: N(in-view) = N x P(in-view|measured) x P(measured)
            self.estimate_in_view += prob_in_view * prob_measure

            # Estimate for the n umber of measured impressions: N(measured) = N x P(measured)
            self.estimate_measure += prob_measure

            # sum of in-view impressions
            self.actual_in_view += imp_in_view

            # sum of measured impressions
            self.actual_measure += imp_measure

        # output the event information and stats
        output([
            prob_in_view >= self.threshold,
            imp_tid,
            self.threshold,
            prob_in_view,
            imp_in_view,
            prob_measure,
            imp_measure,
            self.window_rate,
            self.actual_rate,
        ])