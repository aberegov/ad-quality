from com.conversant.common.EnvConfig import EnvConfig
from com.conversant.common.DatabaseTree import DatabaseTree
from com.conversant.viewability.MultiKey import MultiKey
from com.conversant.viewability.PredictorEnum import PredictorEnum


class MultiKeyPredictor(DatabaseTree):
    serialization_version = '1.0'

    def __init__(self, source='ad_quality.predictors'):
        config = EnvConfig()
        self.multi_key = MultiKey(config.get('hierarchy', PredictorEnum.in_view.value).split(','))
        self.multi_key[PredictorEnum.measure.value] = config.get('hierarchy', PredictorEnum.measure.value).split(',')
        super().__init__("SELECT predictor_type, {0}, predictor_value FROM {1}".format(str(self.multi_key), source))

    def __setitem__(self, name, keys):
        self.multi_key[name] = keys

    def prepare_row(self, row):
        return [row[0]] + self.multi_key.reorder(row[0], row[1:-1]) + [row[-1]]

    def predict(self, name, data):
        return self.match_path([name] + self.multi_key.reorder(name, data)).value
