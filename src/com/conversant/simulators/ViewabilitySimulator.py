from matplotlib import pyplot
from com.conversant.viewability.ViewabilityController import ViewabilityController
from com.conversant.simulators.AbstractViewabilitySimulator import AbstractViewabilitySimulator


class ViewabilitySimulator(AbstractViewabilitySimulator):
    def __init__(self, goal, period=100000, window=10000, latency=10000, sensitivity=0.01,
                 source='ad_quality.impressions_view'):
        super().__init__(source)
        self.controller = ViewabilityController(
            predictor=self.predictor, goal=goal, period=period, window=window, latency=latency, sensitivity=sensitivity)

    def process_row(self, row, view):
        return self.controller.process_event(row, self.output)

    def output(self, data):
        if data[0]:
            self.append(data[+2], 'threshold')
            self.append(data[-2], 'window_rate')
            self.append(data[-1], 'actual_rate')

    def show_results(self):
        self.logger.info('Showing results')

        x = list(range(len(self.results['window_rate'])))
        f, (ax1, ax2) = pyplot.subplots(2, sharex=True, sharey=True)
        thresh, = ax1.plot(x, self.results['threshold'], color='blue', linestyle='solid', label="threshold")
        actual, = ax2.plot(x, self.results['actual_rate'], color='green', linestyle='solid', label="actual rate")
        window, = ax2.plot(x, self.results['window_rate'], color='red', linestyle='solid', label="window rate")

        pyplot.grid(True)
        pyplot.legend(bbox_to_anchor=(0., 1.02, 1., .102),
                      loc=3, ncol=3, mode="expand", borderaxespad=0., handles=[actual, window, thresh])
        pyplot.show()


if __name__ == '__main__':
    simulator = ViewabilitySimulator(goal=0.3, period=100000, window=1000, latency=1000, sensitivity=0.001)
    simulator.execute("SELECT transaction_nbr, {0}, in_view, measured FROM {1}")
    simulator.show_results()
