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


-- Store Spanish municipalities and their geographical coordinates.
CREATE TABLE IF NOT EXISTS raw.municipalities (
    municipality_id VARCHAR(5) PRIMARY KEY,
    municipality_name VARCHAR(150) NOT NULL,
    province_name VARCHAR(100) NOT NULL,
    province_code VARCHAR(2) NOT NULL,
    autonomous_community_code VARCHAR(10) NOT NULL,
    latitude NUMERIC(9,6) NOT NULL,
    longitude NUMERIC(9,6) NOT NULL,
    population INTEGER,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);