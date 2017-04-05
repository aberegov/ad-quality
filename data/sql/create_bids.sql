DROP VIEW ad_quality.bids_view;

DROP TABLE ad_quality.bids;

CREATE TABLE
    ad_quality.bids
    (
        network_id INTEGER,
        seller_id CHARACTER VARYING(100),
        site_id TEXT,
        request_type_id INTEGER,
        supply_type_id INTEGER,
        media_size INTEGER,
        ad_position INTEGER,
        browser_name CHARACTER VARYING(100),
        browser_version CHARACTER VARYING(100),
        os CHARACTER VARYING(100),
        device CHARACTER VARYING(100),
        company_id INTEGER,
        campaign_id INTEGER,
        user_agent CHARACTER VARYING(1000),
        dtm_id NUMERIC(20)
    );

ALTER TABLE ad_quality.bids OWNER TO aberegov;

CREATE VIEW
    ad_quality.bids_view AS
    (
    SELECT
        network_id,
        seller_id,
        site_id,
        (request_type_id << 4) + supply_type_id as ad_format_id,
        supply_type_id,
        media_size,
        ad_position,
        browser_name,
        browser_version,
        os,
        device,
        company_id,
        campaign_id,
        user_agent,
        dtm_id
    FROM ad_quality.bids
    );

ALTER TABLE ad_quality.bids_view OWNER TO aberegov;