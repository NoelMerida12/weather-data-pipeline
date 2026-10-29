-- Check that every city has 24 hourly records per day.
SELECT
    city,
    weather_date,
    hourly_records

FROM {{ ref('fct_weather_daily') }}

WHERE hourly_records IS DISTINCT FROM 24
   OR is_complete_day IS DISTINCT FROM TRUE