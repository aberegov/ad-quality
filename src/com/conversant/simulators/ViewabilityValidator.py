from com.conversant.simulators.AbstractViewabilitySimulator import AbstractViewabilitySimulator


class ViewabilityValidator(AbstractViewabilitySimulator):
    def __init__(self, source='ad_quality.bids_view'):
        super().__init__(source)

    def process_row(self, row, view):
        special_values = {2.52: None, 2.66 : -1, 2.80: 1, 2.94 : -100, 3.08 : 0, 3.22: 100}

        cost = float(row[-2])

        try:
            p = special_values[cost]
        except KeyError:
            p = cost / 7.0

        self.append(list(row[1:-2]) + [view, p, cost])


if __name__ == '__main__':
    validator = ViewabilityValidator()
    validator.execute("SELECT transaction_nbr, {0}, ecpm_usd, test FROM {1} where test = 1")
    validator.output()
