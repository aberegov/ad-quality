from com.conversant.viewability.MultiKeyPredictor import MultiKeyPredictor
from com.conversant.viewability.ViewabilityController import ViewabilityController
from com.conversant.common.SQLShell import SQLShell


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

        self.predictor.build()
        self.controller = ViewabilityController(predictor=self.predictor, goal=goal, n=n, w=w, l=l)

    def run(self):
        data = SQLShell()
        data.execute("SELECT {0}, in_view, measured FROM {1}".format
                     (str(self.predictor.multi_key), self.source), {}, self.handle_impression)

    def handle_impression(self, imp):
        self.controller.process_event(imp, self.output)

    def output(self, data):
        print(data)

if __name__ == '__main__':
    simulator = ViewabilitySimulator(goal=0.7, n=1000, w=100, l=100)
    simulator.run()
