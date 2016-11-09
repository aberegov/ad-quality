import logging
import os
import pickle
from matplotlib import pyplot
from com.conversant.viewability.MultiKeyPredictor import MultiKeyPredictor
from com.conversant.viewability.ViewabilityController import ViewabilityController
from com.conversant.common.SQLShell import SQLShell

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ViewabilitySimulator:
    def __init__(self, goal, n=100000, w=10000, l=10000,source='ad_quality.impressions_view'):
        self.source = source
        self.build_predictors()
        self.controller = ViewabilityController(predictor=self.predictor, goal=goal, n=n, w=w, l=l)
        self.results = {'threshold': [], 'actual_rate': [], 'window_rate': []}

    def build_predictors(self):
        mk_file = os.path.normpath(os.path.join(os.path.expanduser("~"), 'multi-key.data'))
        if (os.path.isfile(mk_file)):
            logger.info('Loading multi-key lookup from %s' % mk_file)
            with open(mk_file, 'rb') as f:
                self.predictor = pickle.load(f)
        else:
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
            logger.info('Building multi-key lookup')
            self.predictor.build()

            logger.info('Serializing multi-key lookup into %s' % mk_file)
            with open(mk_file, 'wb') as f:
                pickle.dump(self.predictor, f)

    def run(self):
        logger.info('Processing impressions')
        data = SQLShell()
        data.execute("SELECT transaction_nbr, {0}, in_view, measured FROM {1}".format
                     (str(self.predictor.multi_key), self.source), {}, self.handle_impression, self.controller.n)

    def handle_impression(self, imp):
        self.controller.process_event(imp, self.output)

    def output(self, data):
        logger.info(data)
        if data[0]:
            self.results['threshold'].append(data[2])
            self.results['window_rate'].append(data[-2])
            self.results['actual_rate'].append(data[-1])

    def show_results(self):
        logger.info('Showing results')
        x = list(range(len(self.results['window_rate'])))
        actual, = pyplot.plot(x, self.results['actual_rate'], color='green', linestyle='solid', label="actual rate")
        window, = pyplot.plot(x, self.results['window_rate'], color='red', linestyle='--', label="window rate")
        pyplot.grid(True)
        pyplot.legend(handles=[actual, window])
        pyplot.show()


if __name__ == '__main__':
    simulator = ViewabilitySimulator(goal=0.7, n=100000, w=1000, l=1000)
    simulator.run()
    simulator.show_results()
