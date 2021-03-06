from com.conversant.common.SlidingBuffer import SlidingBuffer
from com.conversant.viewability.PredictorEnum import PredictorEnum


class ViewabilityController:
    def __init__(self, goal, predictor, period=1000000, window=10000, latency=10000, sensitivity=0.01):
        self.goal = goal
        self.threshold = goal
        self.sensitivity = sensitivity
        self.period = period
        self.predictor = predictor
        self.actual_in_view = SlidingBuffer(latency)
        self.actual_measure = SlidingBuffer(latency)
        self.estimate_in_view = SlidingBuffer(window)
        self.estimate_measure = SlidingBuffer(window)
        self.impressions = 0

    @property
    def elapsed(self):
        return float(self.impressions / self.period)

    @property
    def actual_window(self):
        return float(self.actual_in_view.current / self.actual_measure.current) \
            if self.actual_measure.current > 0 else None

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
        return float(self.estimate_in_view.current / self.estimate_measure.current)\
            if self.estimate_measure.current > 0 else None

    @property
    def compensating_rate(self):
        return float((self.goal - self.elapsed * self.historical_rate) / (1 - self.elapsed)) \
            if self.historical_rate is not None and self.elapsed < 1 else self.goal

    def process_event(self, imp, output):
        if self.impressions > self.period:
            return False

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
        prob_in_view = float(self.predictor.predict(PredictorEnum.in_view.value, imp_mk_data))
        prob_measure = float(self.predictor.predict(PredictorEnum.measure.value, imp_mk_data))

        # calculate the threshold
        if self.window_rate is not None:
            # T[t] = T[t-1] + sensitivity x (target - current)
            self.threshold += self.sensitivity * (self.compensating_rate - self.window_rate)
            # apply limits [0.1, 0.8] to threshold
            self.threshold = min(0.8, max(0.1, self.threshold))

        # make the decision
        make_bid = prob_in_view >= self.threshold
        if make_bid:
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
            1 if make_bid else 0,
            imp_tid,
            self.threshold,
            prob_in_view,
            imp_in_view,
            prob_measure,
            imp_measure,
            self.window_rate,
            self.actual_rate,
        ])

        return True