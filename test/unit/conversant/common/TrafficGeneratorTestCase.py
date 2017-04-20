import unittest
from matplotlib import pyplot
from random import random
from com.conversant.common.TrafficGenerator import TrafficGenerator
from com.conversant.common.Throttling import Throttling


class TrafficGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.generator = TrafficGenerator(max_traffic=10, min_traffic=1, noise_to_signal=0.1)
        self.throttle = Throttling(400, period=2000)

    def tearDown(self):
        del self.generator
        del self.throttle

    def test_gen(self):
        self.generator.gen_period(n_periods=5, tick_per_period=2000)

        count = 0
        win_rate = 0.02

        for i in self.generator.d:
            count += 1
            if count % (self.throttle.period / 4) == 0:
                win_rate = 0.04 if random() <= 0.5 else 0.005

            self.throttle.tick(int(i), win_rate=win_rate)

        plots = pyplot.plot(range(len(self.throttle.results)), self.throttle.results, marker='.')
        pyplot.legend(iter(plots), ('24h cap', '24h avail', '24h spend'))
        pyplot.axis([0, len(self.generator.d), 0, 600])
        pyplot.show()
