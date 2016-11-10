from enum import Enum


class PredictorEnum(Enum):
    # The predictor name for an impression to be in-view
    in_view = "viewability"

    # The predictor name for an impession to be measured
    measure = "measurability"