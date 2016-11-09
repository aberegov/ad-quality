CREATE TABLE
    ad_quality.impressions
    (
        transaction_nbr BIGINT,
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
        measured NUMERIC(12,5),
        in_view NUMERIC(12,5)
    );

ALTER TABLE ad_quality.impressions OWNER TO aberegov;

CREATE VIEW
    ad_quality.impressions_view AS
    (
    SELECT
        transaction_nbr,
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
        (case when measured = 1 then 1 else 0 end) as measured,
        (case when in_view = 1 then 1 else 0 end) as in_view
    FROM ad_quality.impressions
    );

ALTER TABLE ad_quality.impressions_view OWNER TO aberegov;