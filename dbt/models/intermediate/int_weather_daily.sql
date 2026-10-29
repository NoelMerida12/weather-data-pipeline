SELECT
    city,
    weather_date,
    ROUND(AVG(temperature_c), 2) AS avg_temperature_c,
    ROUND(AVG(humidity_pct), 2) AS avg_humidity_pct,
    ROUND(SUM(precipitation_mm), 2) AS total_precipitation_mm,
    MAX(wind_speed_kmh) AS max_wind_speed_kmh,
    COUNT(*) AS hourly_records

FROM {{ ref('stg_weather_hourly') }}

GROUP BY city, weather_date