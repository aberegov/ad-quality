import logging
import os
import pickle
from matplotlib import pyplot
from com.conversant.viewability.MultiKeyPredictor import MultiKeyPredictor
from com.conversant.viewability.ViewabilityController import ViewabilityController
from com.conversant.common.SQLShell import SQLShell

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO,format=FORMAT)
logger = logging.getLogger(__name__)


class ViewabilitySimulator:
    def __init__(self, goal, period=100000, window=10000, latency=10000, sensitivity=0.01, source='ad_quality.impressions_view'):
        self.predictor = None
        self.source = source
        self.build_predictors()
        self.results = {'threshold': [], 'actual_rate': [], 'window_rate': []}
        self.controller = ViewabilityController(
            predictor=self.predictor, goal=goal, period=period, window=window, latency=latency, sensitivity=sensitivity)

    def build_predictors(self):
        mk_file = os.path.normpath(os.path.join(os.path.expanduser("~"), 'multi-key.data'))
        if os.path.isfile(mk_file):
            logger.info('Loading multi-key lookup from %s' % mk_file)
            with open(mk_file, 'rb') as f:
                self.predictor = pickle.load(f)
        else:
            logger.info('Building multi-key lookup')
            self.predictor = MultiKeyPredictor()
            self.predictor.build()

            logger.info('Serializing multi-key lookup into %s' % mk_file)
            with open(mk_file, 'wb') as f:
                pickle.dump(self.predictor, f)

    def run(self):
        logger.info('Processing impressions')
        data = SQLShell()
        data.execute("SELECT transaction_nbr, {0}, in_view, measured FROM {1}".format
                     (str(self.predictor.multi_key), self.source), {}, self.handle_impression)

    def handle_impression(self, imp):
        return self.controller.process_event(imp, self.output)

    def output(self, data):
        logger.debug(data)
        if data[0]:
            self.results['threshold'].append(data[2])
            self.results['window_rate'].append(data[-2])
            self.results['actual_rate'].append(data[-1])

    def show_results(self):
        logger.info('Showing results')
        x = list(range(len(self.results['window_rate'])))

        f, (ax1, ax2) = pyplot.subplots(2, sharex=True, sharey=True)

        threshold, = ax1.plot(x, self.results['threshold'], color='blue', linestyle='solid', label="threshold")
        actual, = ax2.plot(x, self.results['actual_rate'], color='green', linestyle='solid', label="actual rate")
        window, = ax2.plot(x, self.results['window_rate'], color='red', linestyle='solid', label="window rate")

        pyplot.grid(True)
        pyplot.legend(bbox_to_anchor=(0., 1.02, 1., .102),
                      loc=3, ncol=3, mode="expand", borderaxespad=0.,handles=[actual, window, threshold])
        pyplot.show()


if __name__ == '__main__':
    simulator = ViewabilitySimulator(goal=0.7, period=100000, window=1000, latency=1000)
    simulator.run()
    simulator.show_results()
