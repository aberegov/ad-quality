from com.conversant.common.DatabaseTree import DatabaseTree


class MultiKeyPredictor(DatabaseTree):
        def __init__(self):
            super().__init__("""
        SELECT
            predictor_type,
            (case when network_id       is null then '(null)' else network_id::varchar end) as network_id,
            (case when seller_id        is null then '(null)' else seller_id end) as seller_id,
            (case when site_id          is null then '(null)' else site_id end) as site_id,
            (case when ad_format_id     is null then '(null)' else ad_format_id::varchar end) as ad_format_id,
            (case when media_size       is null then '(null)' else media_size::varchar end) as media_size,
            (case when ad_position      is null then '(null)' else ad_position::varchar end) as ad_position,
            (case when browser_name     is null then '(null)' else browser_name end) as browser_name,
            (case when browser_version  is null then '(null)' else browser_version end) as browser_version,
            (case when os               is null then '(null)' else os end) as os,
            (case when device           is null then '(null)' else device end) as device,
            predictor_value
        FROM
            adquality.viewability_predictors
            """)

        def predict(self, type, keys):
            return self.node_by_path([type] + keys).data
