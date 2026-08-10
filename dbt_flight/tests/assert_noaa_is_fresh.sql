SELECT max(observed_at) AS latest
FROM {{ ref('NOAA_data') }}
HAVING date_diff('day', max(observed_at), current_date::timestamp) > 7
