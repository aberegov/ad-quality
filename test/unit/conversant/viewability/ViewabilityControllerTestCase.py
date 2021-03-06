import unittest
import logging
import random
from com.conversant.viewability.ViewabilityController import ViewabilityController

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ViewabilityControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.controller = ViewabilityController(goal=0.5, predictor=self, period=100, latency=10, window=10)

    def tearDown(self):
        del self.controller

    def predict(self, predictor, keys):
        return 0.4 + keys[0] * 0.1 + keys[1] * 0.2

    def test_process_event(self):
        for i in range(100):
            m = random.choice([0, 1])
            v = m * random.choice([0, 1])

            self.controller.process_event([
                i,
                random.choice([0, 1]),
                random.choice([0, 1]),
                v,
                m], self.output)

    def output(self, data):
        logger.info('%s', str(data))