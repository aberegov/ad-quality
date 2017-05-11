import unittest
from matplotlib import pyplot
from random import random
from com.conversant.common.TrafficGenerator import TrafficGenerator
from com.conversant.common.Throttling import Throttling


class TrafficGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.generator = TrafficGenerator(max_traffic=20, min_traffic=1, noise_to_signal=0.1)
        self.throttle = Throttling(200, period=2000)

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
                win_rate = 0.05 if random() <= 0.5 else 0.001

            self.throttle.tick(int(i), win_rate=win_rate)

        #plots = pyplot.plot(range(len(self.throttle.results)), self.throttle.results, marker='.')
        #pyplot.axis([0, len(self.generator.d), 0, 600])
        #pyplot.legend(iter(plots), ('1h avail', '24h cap', '24h avail', '24h spend'))
        #pyplot.show()

        plots = []
        x = range(len(self.throttle.results))
        y = list(zip(*self.throttle.results))
        fig, ax1 = pyplot.subplots()
        plots.append(ax1.plot(x, y[0]))

        ax2 = ax1.twinx()
        plots.append(ax2.plot(x, y[1]))
        plots.append(ax2.plot(x, y[2]))
        plots.append(ax2.plot(x, y[3]))
        pyplot.show()