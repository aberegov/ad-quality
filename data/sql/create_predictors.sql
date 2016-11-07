--
-- Create viewability predictors table
--
CREATE TABLE
    adquality.viewability_predictors
    (
        vendor_id INTEGER NOT NULL,
        network_id INTEGER,
        seller_id CHARACTER VARYING(100),
        site_id TEXT,
        ad_format_id INTEGER,
        media_size INTEGER,
        ad_position INTEGER,
        browser_name CHARACTER VARYING(100),
        browser_version CHARACTER VARYING(100),
        os CHARACTER VARYING(100),
        device CHARACTER VARYING(100),
        predictor_type CHARACTER VARYING(100) NOT NULL,
        predictor_value NUMERIC(12,5),
        confidence_score NUMERIC(12,5)
    );

ALTER TABLE adquality.viewability_predictors OWNER TO aberegov;
