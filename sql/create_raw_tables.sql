-- Create the raw schema for weather ingestion.
CREATE SCHEMA IF NOT EXISTS raw;

-- Store hourly weather observations for each city.
CREATE TABLE IF NOT EXISTS raw.weather_hourly (
    city VARCHAR(100) NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    temperature_2m NUMERIC(6,2),
    relative_humidity_2m SMALLINT,
    precipitation NUMERIC(8,2),
    wind_speed_10m NUMERIC(8,2),
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (city, observed_at)
);