import logging
import os
import pickle
import csv
from abc import ABCMeta
from com.conversant.viewability.MultiKeyPredictor import MultiKeyPredictor
from com.conversant.viewability.PredictorEnum import PredictorEnum
from com.conversant.common.SQLShell import SQLShell


class AbstractViewabilitySimulator(metaclass=ABCMeta):
    def __init__(self, source):
        logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(message)s')
        self.logger = logging.getLogger(__name__)

        self.source = source
        self.results = {}
        self.predictor = None
        self.build_predictors()

    def build_predictors(self):
        file = self.get_serialization_file()

        if os.path.isfile(file):
            self.logger.info('Loading multi-key predictors from %s' % file)
            with open(file, 'rb') as f:
                self.predictor = pickle.load(f)
        else:
            self.logger.info('Building multi-key predictors and saving into %s' % file)
            self.predictor = MultiKeyPredictor()
            self.predictor.build()
            with open(file, 'wb') as f:
                pickle.dump(self.predictor, f)

    @staticmethod
    def get_serialization_file():
        return os.path.normpath(
            os.path.join(os.path.expanduser("~"),
                         'multi_key_predictors_%s.data' % MultiKeyPredictor.serialization_version))

    def execute(self, sql):
        self.logger.info('Processing rows')
        try:
            shell = SQLShell()
            self.run(shell.iterate(sql.format(str(self.predictor.multi_key), self.source), {}))
        finally:
            shell.close()

    def run(self, rows):
        for i in rows:
            self.handle_row(i)

    def handle_row(self, row):
        self.process_row(row, float(self.predictor.predict(PredictorEnum.in_view.value, row[1:-2])))

    def append(self, row, tag='data'):
        if tag not in self.results:
            self.results.update({tag: []})

        self.results[tag].append(row)

    def process_row(self, row, view):
        pass

    def print_tree(self):
        print(self.predictor)

    def output(self):
        path = os.path.normpath(os.path.join(os.path.expanduser("~"), 'view_results.csv'))
        with open(path, "w") as out_file:
            writer = csv.writer(out_file,  delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow(self.predictor.multi_key.keys + ['predictor', 'data_0', 'data_1'])
            for row in self.results['data']:
                writer.writerow(row)

