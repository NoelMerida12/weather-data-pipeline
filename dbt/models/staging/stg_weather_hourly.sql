SELECT
    city,
    observed_at,
    (observed_at AT TIME ZONE 'UTC')::DATE AS weather_date,
    temperature_2m AS temperature_c,
    relative_humidity_2m AS humidity_pct,
    precipitation AS precipitation_mm,
    wind_speed_10m AS wind_speed_kmh,
    ingested_at
FROM {{ source('raw', 'weather_hourly') }}