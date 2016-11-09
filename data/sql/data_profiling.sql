
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