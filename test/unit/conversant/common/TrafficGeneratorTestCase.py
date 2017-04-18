import unittest
from matplotlib import pyplot
from com.conversant.common.TrafficGenerator import TrafficGenerator
from com.conversant.common.Throttling import Throttling


class TrafficGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.generator = TrafficGenerator(max_traffic=200, min_traffic=40, noise_to_signal=0.05)
        self.throttle = Throttling(100, win_rate=0.03, period=3000)

    def tearDown(self):
        del self.generator
        del self.throttle

    def test_gen(self):
        self.generator.gen_period(n_periods=4, tick_per_period=3000)

        for i in self.generator.d:
            self.throttle.tick(int(i))

        pyplot.plot(range(len(self.throttle.results)), self.throttle.results, marker='.')
        pyplot.show()
