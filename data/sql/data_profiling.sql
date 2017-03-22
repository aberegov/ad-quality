
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


select score
	,predictor_value
	,(case when max(score) over () = score then 'winner' else '' end) as result
from	
(
	select
		(((case when ad_format_id	=  -1  then '0' else '1' end)
		||(case when network_id		=  -1  then '0' else '1' end)
		||(case when seller_id		= '-1' then '0' else '1' end)
		||(case when site_id		= '-1' then '0' else '1' end)
		||(case when media_size		=  -1  then '0' else '1' end)
		||(case when ad_position	=  -1  then '0' else '1' end)
		||(case when device		= '-1' then '0' else '1' end)
		||(case when os			= '-1' then '0' else '1' end)
		||(case when browser_name	= '-1' then '0' else '1' end)
		||(case when browser_version	= '-1' then '0' else '1' end))::bit(10))::integer as score
		,predictor_value
	from ad_quality.predictors 
	where 		
		(ad_format_id	=  -1  or ad_format_id	 = 17)
	and 	(network_id	=  -1  or network_id	 = 12783)	
	and 	(seller_id	= '-1' or seller_id	 = '10970')			
	and 	(site_id	= '-1' or site_id	 = '56976')	
	and 	(media_size	=  -1  or media_size	 = 11)	
	and 	(ad_position	=  -1  or ad_position	 = 0)	
	and 	(device		= '-1' or device	 = 'Other')	
	and 	(os		= '-1' or os		 = 'Mac OS X')	
	and 	(browser_name	= '-1' or browser_name 	 = 'Safari')	
	and 	(browser_version= '-1' or browser_version= '10')	
) scoring
order by 3 desc

select ad_format_id
	,network_id
	,seller_id
	,site_id
	,media_size
	,ad_position
	,device
	,os
	,browser_name
	,browser_version
	,predictor_value
from ad_quality.predictors
where predictor_type in ('viewability')
and	(ad_format_id	= 17			or ad_format_id = -1)
and	(network_id	= 60			or network_id = -1)
and	(seller_id	= '9983' 	or seller_id = '-1')
and	(site_id	= '9983-306809' 	or site_id = '-1')
and	(media_size	= 32 			or media_size = -1)
and	(ad_position	= -1			or ad_position = -1)
and	(device		= 'Other' 		or device = '-1')
and	(os		= 'Windows 10' 	or os = '-1')
and	(browser_name	= 'Firefox' 		or browser_name = '-1')
and	(browser_version = '51'			or browser_version = '-1')


select * from ad_quality.predictors limit 100

delete from ad_quality.predictors 



select mask
	,score
	,predictor_value as viewability_predictor
	,(case when max(score) over () = score then 'winner' else '' end) as race
from
(
	select mask, (mask::bit(10))::integer as score, predictor_value
	from (
	select
		((case when ad_format_id	=  -1  then '0' else '1' end)
		||(case when network_id		=  -1  then '0' else '1' end)
		||(case when seller_id		= '-1' then '0' else '1' end)
		||(case when site_id		= '-1' then '0' else '1' end)
		||(case when media_size		=  -1  then '0' else '1' end)
		||(case when ad_position	=  -1  then '0' else '1' end)
		||(case when device		= '-1' then '0' else '1' end)
		||(case when os			= '-1' then '0' else '1' end)
		||(case when browser_name	= '-1' then '0' else '1' end)
		||(case when browser_version	= '-1' then '0' else '1' end)) as mask
		,predictor_value
	from dm.viewability_predictors
	where
		ad_format_id	in ( -1,	17)
	and 	network_id	in ( -1,	12783)
	and 	seller_id	in ('-1', 	'10970')
	and 	site_id	 	in ('-1', 	'56976')
	and 	media_size	in ( -1,   	11)
	and 	ad_position	in ( -1,  	0)
	and 	device		in ('-1',  	'Other')
	and 	os		    in ('-1', 	'Mac OS X')
	and 	browser_name	in ('-1', 	'Safari')
	and 	browser_version	in ('-1',	'10')
	) d
) scoring
order by 2 desc