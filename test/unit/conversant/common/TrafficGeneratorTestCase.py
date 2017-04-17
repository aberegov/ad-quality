import unittest
from matplotlib import pyplot
from com.conversant.common.TrafficGenerator import TrafficGenerator
from com.conversant.common.Throttling import Throttling

class TrafficGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.gen = TrafficGenerator()
        self.throttle = Throttling(1000)

    def tearDown(self):
        del self.gen

    def test_gen(self):
        self.gen.gen_period(3)

        for i in self.gen.d:
            self.throttle.tick(int(i))

        pyplot.plot(range(len(self.throttle.results)), self.throttle.results, marker='.')
        pyplot.show()
