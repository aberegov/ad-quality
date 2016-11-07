from com.conversant.common.DatabaseTree import DatabaseTree


class MultiKeyViewabilityPredictor(DatabaseTree):
        def __init__(self):
            super().__init__("""
        SELECT
            network_id::varchar,
            seller_id,
            site_id,
            ad_format_id::varchar,
            media_size::varchar,
            ad_position::varchar,
            browser_name,
            browser_version,
            os,
            device,
            predictor_value
        FROM
            adquality.viewability_predictors
        WHERE
            predictor_type = 'viewability'
            """)

        def predict(self, keys):
            return self.node_by_path(keys).data
