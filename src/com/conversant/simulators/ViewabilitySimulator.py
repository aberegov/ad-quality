import logging
from matplotlib import pyplot
from com.conversant.viewability.MultiKeyPredictor import MultiKeyPredictor
from com.conversant.viewability.ViewabilityController import ViewabilityController
from com.conversant.common.SQLShell import SQLShell

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ViewabilitySimulator:
    def __init__(self, goal, n=100000, w=10000, l=10000,source='ad_quality.impressions_view'):
        self.source = source
        self.predictor = MultiKeyPredictor()
        self.predictor["measurability"] = [
            'ad_format_id',
            'device',
            'os',
            'browser_name',
            'browser_version',
            'media_size',
            'network_id',
            'seller_id',
            'site_id',
            'ad_position'
        ]

        logger.info('Start building multi-key lookup tree')
        self.predictor.build()

        self.controller = ViewabilityController(predictor=self.predictor, goal=goal, n=n, w=w, l=l)
        self.results = {'rate': [], 'threshold': []}

    def run(self):
        logger.info('Start running simulation')
        data = SQLShell()
        data.execute("SELECT transaction_nbr, {0}, in_view, measured FROM {1}".format
                     (str(self.predictor.multi_key), self.source), {}, self.handle_impression, self.controller.n)

    def handle_impression(self, imp):
        self.controller.process_event(imp, self.output)

    def output(self, data):
        logger.info(data)
        self.results['threshold'].append(data[1])
        self.results['rate'].append(data[3])

    def show_results(self):
        logger.info('Displaying results')
        x = list(range(len(self.results['rate'])))
        pyplot.plot(x, self.results['rate'], color='green', linestyle='solid')
        pyplot.show()


if __name__ == '__main__':
    simulator = ViewabilitySimulator(goal=0.6, n=100000, w=1000, l=1000)
    simulator.run()
    simulator.show_results()
