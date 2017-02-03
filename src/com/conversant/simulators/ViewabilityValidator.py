from com.conversant.simulators.AbstractViewabilitySimulator import AbstractViewabilitySimulator


class ViewabilityValidator(AbstractViewabilitySimulator):
    def __init__(self, source='ad_quality.bids_view'):
        super().__init__(source)

    def process_row(self, row, view):
        cost = float(row[-2])
        self.append(list(row[1:-2]) + [view, cost, -1 if cost == 4.83 else cost / 7.0])


if __name__ == '__main__':
    validator = ViewabilityValidator()
    validator.execute("SELECT transaction_nbr, {0}, ecpm_usd, test FROM {1} where test = 1")
    validator.output()
