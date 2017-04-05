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
        ,(case when (case msg_eval_level_id when 2 then dtm_individual_id else dtm_id end # 172005387) % 100 <=50 then 0 else 1 end) as test
        ,message_ecpm_usd as inview
        ,mix(user_agent_attr)
        ,max(dtm_id)
from whse_secure.raw_rtb_bid_log_ext
where bid_date >= '2017-03-17' and company_id = 2997 and campaign_id = 23254  and operation_id in (3,12,53,54)
group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14


select
         network_id
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
        ,max(user_agent_attr)
        ,max(dtm_id)
from raw_rtb_bid_log
where partition_start_date = 20170317 and company_id = 2997 and campaign_id = 23254  and operation_id in (3,12,53,54)
group by
         network_id
        ,seller_id
        ,site_id
        ,request_type_id
        ,supply_type_id
        ,media_size_id
        ,ad_position_id
        ,browser_desc
        ,browser_major_version_attr
        ,operating_system_desc
        ,device_desc;


select
         network_id
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
        ,max(company_id)
        ,max(campaign_id)
        ,max(user_agent_attr)
        ,max(dtm_id)
from whse.raw_rtb_bid_log
where partition_start_date = 20170403
--    and company_id = 2997
    and campaign_id = 24429
    and operation_id in (3,12,53,54)
group by
    network_id
    ,seller_id
    ,site_id
    ,request_type_id
    ,supply_type_id
    ,media_size_id
    ,ad_position_id
    ,browser_desc
    ,browser_major_version_attr
    ,operating_system_desc
    ,device_desc
limit 10000;


update ad_quality.bids
set
	 seller_id      = trim(seller_id)
	,site_id        = trim(site_id)
	,browser_name   = trim(browser_name)
	,browser_version= trim(browser_version)
	,os             = trim(os)
	,device         = trim(device)
	,user_agent     = trim(user_agent)

update ad_quality.bids
set
	 seller_id      = (case when seller_id      = 'NULL' then null else seller_id       end)
	,site_id        = (case when site_id        = 'NULL' then null else site_id         end)
	,browser_name   = (case when browser_name   = 'NULL' then null else browser_name    end)
	,browser_version= (case when browser_version= 'NULL' then null else browser_version end)
	,os             = (case when os             = 'NULL' then null else os              end)
	,device         = (case when device         = 'NULL' then null else device          end)
	,user_agent     = (case when user_agent     = 'NULL' then null else user_agent      end)
