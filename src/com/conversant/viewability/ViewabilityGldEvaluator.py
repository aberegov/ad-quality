from com.conversant.dlg.DlgEvaluator import DlgEvaluator


class ViewabilityGldEvaluator(DlgEvaluator):
    def __init__(self):
        super().__init__()
        self.set_params(
            formula='%2F%2F+API+v1%0D%0Afun+modelScore+%3A+Real+%2C%0D%0A+viewability+%3A+%7B+performance+%3A+Real%7D%0D%0A+%3D+viewability.performance'
        )
