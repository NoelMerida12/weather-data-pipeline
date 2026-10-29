{{ config(materialized='table') }}

SELECT
    city,
    weather_date,
    avg_temperature_c,
    avg_humidity_pct,
    total_precipitation_mm,
    max_wind_speed_kmh,
    hourly_records,

    CASE
        WHEN total_precipitation_mm > 0 THEN 'Rainy'
        ELSE 'Dry'
    END AS weather_condition,

    CASE
        WHEN hourly_records = 24 THEN TRUE
        ELSE FALSE
    END AS is_complete_day

FROM {{ ref('int_weather_daily') }}