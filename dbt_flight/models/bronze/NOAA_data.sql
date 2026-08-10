{{
    config (
        materialized = 'incremental',
        unique_key = ['STATION', 'observed_at']
    )
}}

SELECT  
    * exclude ("DATE"),
    "DATE"::timestamp as observed_at

FROM {{source('SOURCE', 'noaa_ghcnh_hourly')}}

{% if is_incremental() %}
    WHERE "DATE"::timestamp >= (SELECT MAX("observed_at") FROM {{this}})
{% endif %}