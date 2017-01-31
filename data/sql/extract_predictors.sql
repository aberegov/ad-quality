psql -h dtord01pgm05p.dc.dotomi.net -d prod_dm -U aberegov

SELECT
    vendor_id
        ,network_id                     as network_id
        ,seller_id                      as seller_id
        ,site_id                        as site_id
        ,ad_format_id                   as ad_format_id
        ,media_size_id                  as media_size
        ,ad_position_id                 as ad_position
        ,browser_desc                   as browser_name
        ,browser_major_version_attr     as browser_version
        ,operating_system_desc          as os
        ,device_desc                    as device
        ,multikey_name                  as predictor_type
        ,multikey_value                 as predictor_value
        ,multikey_confidence            as confidence_score
FROM
    anly_prod.dim_global_multikey_lookup



