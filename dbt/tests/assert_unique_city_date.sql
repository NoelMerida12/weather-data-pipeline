-- Check for duplicate city and date combinations.
SELECT
    city,
    weather_date,
    COUNT(*) AS total_rows

FROM {{ ref('fct_weather_daily') }}

GROUP BY city, weather_date
HAVING COUNT(*) > 1