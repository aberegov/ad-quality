select
        i.transaction_nbr
        ,network_id
        ,seller_id
        ,site_id
        ,request_type_id
        ,(case when device_id is not NULL then 3
            when device_type_attr in ('Mobile', 'Tablet') then 4 else 1 end) as supply_type_id
        ,media_size_id as media_size
        ,ad_position_id as ad_position
        ,browser_desc as browser_name
        ,browser_major_version_attr as browser_version
        ,operating_system_desc as os
        ,device_desc as device
        ,(case when in_viewability_sample_attr = 'yes' then 1 else 0 end) as measured
        ,(case when request_type_id in (2, 4) then video_ad_in_view_meas else in_view_1s_meas end) as inview
from fact_dmm_log i
        inner join raw_trafficscope_log v
            on i.transaction_nbr = v.transaction_nbr and dmm_date between '2016-10-27' and '2016-10-30'
where dmm_date between '2016-10-27' and '2016-10-30'
        and ext_channel_id ~ E'^\\d{3}$'
                and ext_channel_id::integer & 15 = 1
                    and i.transaction_nbr > 1000
limit 1000000
