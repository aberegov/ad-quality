select score
	,predictor_value
	,(case when max(score) over () = score then 'winner' else '' end) as result
from
(
	select bm, (bm::bit(10))::integer as score,predictor_value
	from (
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
			||(case when browser_version	= '-1' then '0' else '1' end))) as bm
			,predictor_value
		from ad_quality.predictors
		where 	predictor_type = 'viewability'
		and	(ad_format_id	=  -1  or ad_format_id	 = 17)
		and 	(network_id	=  -1  or network_id	 = 1982)
		and 	(seller_id	= '-1' or seller_id	 = '215230')
		and 	(site_id	= '-1' or site_id	 = '1223815')
		and 	(media_size	=  -1  or media_size	 = 11)
		and 	(ad_position	=  -1  or ad_position	 = -1)
		and 	(device		= '-1' or device	 = 'Other')
		and 	(os		= '-1' or os		 = 'Mac OS X')
		and 	(browser_name	= '-1' or browser_name 	 = 'Firefox')
		and 	(browser_version= '-1' or browser_version= '47')
	) d
	order by 2 desc
) scoring
order by 1 desc