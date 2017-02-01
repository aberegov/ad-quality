import logging
from com.conversant.common.SQLShell import SQLShell
from com.conversant.simulators.AbstractViewabilitySimulator import AbstractViewabilitySimulator

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class ViewabilityValidator(AbstractViewabilitySimulator):
    def __init__(self, source='ad_quality.bid_view'):
        super().__init__(source)

    def execute(self):
        logger.info('Processing bids/impressions')
        data = SQLShell()
        self.run(data.iterate("SELECT transaction_nbr, {0}, in_view, measured FROM {1} where measured = 1".format
                     (str(self.predictor.multi_key), self.source), {}))

    def process_row(self, row, view):
        cost = float(row[-2])
        self.append([cost, -1 if cost == 4.83 else cost / 7.0, view] + list(row[1:-2]))

if __name__ == '__main__':
    validator = ViewabilityValidator()
    validator.execute()
    validator.output()