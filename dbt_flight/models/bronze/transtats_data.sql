{{
    config (
        materialized = 'incremental',
        unique_key = ['OriginAirportID', 'DOT_ID_Reporting_Airline',
              'Flight_Number_Reporting_Airline', 'FlightDate', 'Dest']
    )
}}

SELECT  
    *
FROM {{source('SOURCE', 'on_time_performance')}}

{% if is_incremental() %}
    WHERE "FlightDate" >= (SELECT MAX("FlightDate") FROM {{this}})
{% endif %}