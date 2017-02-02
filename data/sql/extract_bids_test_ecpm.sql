--
-- psql -h dtord01gpv01p.dc.dotomi.net -d vds_prd -U aberegov
--

select
        0 as transaction_nbr
        ,network_id
        ,seller_id
        ,site_id
        ,request_type_id
        ,supply_type_id
        ,media_size_id as media_size
        ,ad_position_id as ad_position
        ,browser_desc as browser_name
        ,browser_major_version_attr as browser_version
        ,operating_system_desc as os
        ,device_desc as device
        ,(case when (case msg_eval_level_id when 2 then dtm_individual_id when 1 then hh_id else dtm_id end # 172005387) % 100 <=50 then 0 else 1 end) as test
        ,message_ecpm_usd as ecpm_usd
from whse_secure.raw_rtb_bid_log_ext
where bid_date >= '2017-01-30' and bid_date + bid_ts >= '2017-01-30 19:00' and company_id = 2997 and campaign_id = 21390 and operation_id in (3,12,53,54)
group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14

