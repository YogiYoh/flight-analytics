SELECT max("FlightDate") AS latest
FROM {{ ref('transtats_data') }}
HAVING date_diff('day', max("FlightDate"), current_date) > 100
