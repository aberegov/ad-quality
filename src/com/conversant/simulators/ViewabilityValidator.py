import logging
import os
import pickle
import csv
from com.conversant.viewability.MultiKeyPredictor import MultiKeyPredictor
from com.conversant.common.SQLShell import SQLShell
from com.conversant.viewability.PredictorEnum import PredictorEnum

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class ViewabilityValidator:
    def __init__(self, source='ad_quality.bid_view'):
        self.source = source
        self.results = []
        self.build_predictors()

    def build_predictors(self):
        mk_file = os.path.normpath(os.path.join(os.path.expanduser("~"), 'multi-key_v1.data'))
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
        data.execute("SELECT transaction_nbr, {0}, in_view, measured FROM {1} where measured = 1".format
                     (str(self.predictor.multi_key), self.source), {}, self.handle_bid)

    def handle_bid(self, bid):
        usd = float(bid[-2])
        key = bid[1:-2]
        predictor = float(self.predictor.predict(PredictorEnum.in_view.value, key))

        self.results.append([usd, -1 if usd == 4.83 else usd / 7.0, predictor] + list(key))

    def output(self):
        path = os.path.normpath(os.path.join(os.path.expanduser("~"), 'mk_validation.csv'))
        with open(path, "w") as out_file:
            writer = csv.writer(out_file,  delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow(['ecpm_usd', 'ecpm_view', 'predictor'] + self.predictor.multi_key.keys)
            for row in self.results:
                writer.writerow(row)


if __name__ == '__main__':
    validator = ViewabilityValidator()
    validator.run()
    validator.output()