from com.conversant.common.DatabaseTree import DatabaseTree
from com.conversant.viewability.MultiKey import MultiKey


class MultiKeyPredictor(DatabaseTree):
        multi_key = MultiKey([
            'ad_format_id',
            'network_id',
            'seller_id',
            'site_id',
            'media_size',
            'ad_position',
            'device',
            'os',
            'browser_name',
            'browser_version'
        ])

        def __init__(self, source='adquality.predictors'):
            super().__init__("SELECT predictor_type, {0}, predictor_value FROM {1}".format(str(self.multi_key), source))

        def __setitem__(self, name, keys):
            self.multi_key[name] = keys

        def prepare_row(self, row):
            return [row[0]] + self.multi_key.reorder(row[0], row[1:-1]) + [row[-1]]

        def predict(self, name, keys):
            return self.path_best_match([name] + self.multi_key.reorder(name, keys))

        def predict_all(self, predictors, keys):
            return [self.predict(t, keys) for t in predictors]
