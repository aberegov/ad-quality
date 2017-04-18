import unittest
from matplotlib import pyplot
from random import random
from com.conversant.common.TrafficGenerator import TrafficGenerator
from com.conversant.common.Throttling import Throttling


class TrafficGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.generator = TrafficGenerator(max_traffic=100, min_traffic=10, noise_to_signal=0.05)
        self.throttle = Throttling(100, period=2000)

    def tearDown(self):
        del self.generator
        del self.throttle

    def test_gen(self):
        self.generator.gen_period(n_periods=10, tick_per_period=2000)

        count = 0
        win_rate = 0.01

        for i in self.generator.d:
            count += 1
            if count % (self.throttle.period / 4) == 0:
                win_rate = win_rate * 1.5 if random() <= 0.7 else win_rate / 1.5

            self.throttle.tick(int(i), win_rate=win_rate)

        plots = pyplot.plot(range(len(self.throttle.results)), self.throttle.results, marker='.')
        pyplot.legend(iter(plots), ('daily spend', 'daily cap', 'bid req'))
        pyplot.show()
