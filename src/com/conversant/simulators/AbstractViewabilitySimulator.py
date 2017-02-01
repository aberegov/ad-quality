import logging
import os
import pickle
import csv
from com.conversant.viewability.MultiKeyPredictor import MultiKeyPredictor
from com.conversant.viewability.PredictorEnum import PredictorEnum
from abc import ABCMeta

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class AbstractViewabilitySimulator(metaclass=ABCMeta):
    def __init__(self, source):
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

    def run(self, rows):
        for i in rows:
            self.handle_row(i)

    def handle_row(self, row):
        self.process_row(row, float(self.predictor.predict(PredictorEnum.in_view.value, row[1:-2])))

    def append(self, data):
        self.results.append(data)

    def process_row(self, row, view):
        pass

    def output(self):
        path = os.path.normpath(os.path.join(os.path.expanduser("~"), 'viewability_results.csv'))
        with open(path, "w") as out_file:
            writer = csv.writer(out_file,  delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow(['ecpm_usd', 'ecpm_view', 'predictor'] + self.predictor.multi_key.keys)
            for row in self.results:
                writer.writerow(row)

