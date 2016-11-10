
--
-- Stats about available predictors
--
select predictor_type, count(1)
from ad_quality.predictors
group by 1


--
-- The number of available impressions for simulations
--
select count(1)
from ad_quality.impressions_view

--
-- NULLs and empty strings
--
select 'predictors' as stats, seller_id_null, seller_id_empty, site_id_null, site_id_empty
from
    (select count(1) as seller_id_null from ad_quality.predictors where seller_id is null) a
    cross join
    (select count(1) as seller_id_empty from ad_quality.predictors where seller_id = '') b
    cross join
    (select count(1) as site_id_null from ad_quality.predictors where site_id is null) c
    cross join
    (select count(1) as site_id_empty from ad_quality.predictors where site_id = '') d
    union
select 'impressions' as stats, seller_id_null, seller_id_empty, site_id_null, site_id_empty
from
    (select count(1) as seller_id_null from ad_quality.impressions_view where seller_id is null) a
    cross join
    (select count(1) as seller_id_empty from ad_quality.impressions_view where seller_id = '') b
    cross join
    (select count(1) as site_id_null from ad_quality.impressions_view where site_id is null) c
    cross join
    (select count(1) as site_id_empty from ad_quality.impressions_view where site_id = '') d