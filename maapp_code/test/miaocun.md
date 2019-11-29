```sql
create table if not exists mediate_tb.dw_like_share_web_page_event_data
(
 country string
 ,share_os string
 ,share_client_version bigint
 ,page string
 ,currenturl string
 ,share_video_owner string
 ,share_yyuid bigint
 ,share_uid bigint
 ,event string
 ,client_ip string
 ,pv bigint
)
partitioned by (day string)
stored as orc tblproperties ('orc.compress'='SNAPPY')
```