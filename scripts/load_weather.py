# Read environment variables.
import os

# Work with JSON data.
import json

# Connect to AWS S3.
import boto3

# Connect to PostgreSQL.
import psycopg2


# Convert date strings into datetime objects and handle UTC timezones.
from datetime import datetime, timezone


# Reuse the city list and UTC date logic from the extraction script.
from extract_weather import CITIES, get_target_date


def read_weather_from_s3(city,target_date):
    """Read raw weather JSON data from Amazon S3."""


    bucket_name = os.environ["S3_BUCKET_NAME"]
    

    s3_key = (
        f"raw/weather/date={target_date}/"
        f"city={city.lower()}/weather.json"
    )

    s3_client = boto3.client("s3")

    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=s3_key,
    )

    weather_data = json.loads(response["Body"].read())

    return weather_data

def build_weather_rows(city, weather_data):
    """Convert hourly weather arrays into databases rows."""


    hourly = weather_data ["hourly"]
    rows = []

    for i, timestamp in enumerate(hourly["time"]):
        observed_at = datetime.fromisoformat(timestamp).replace(
            tzinfo=timezone.utc
        )


        rows.append((
            city,
            observed_at,
            hourly["temperature_2m"][i],
            hourly["relative_humidity_2m"][i],
            hourly["precipitation"][i],
            hourly["wind_speed_10m"][i]
        ))

    return rows

def connect_to_postgres():
    """Create a connection to the PostgreSQL database."""

    connection = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["POSTGRES_PORT"]),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    return connection


def insert_weather_rows(connection, rows):
    """Insert weather rows into PostgreSQL without creating duplicates."""

    insert_query = """
        INSERT INTO raw.weather_hourly (
            city,
            observed_at,
            temperature_2m,
            relative_humidity_2m,
            precipitation,
            wind_speed_10m
        )
        VALUES (%s, %s, %s, %s, %s, %s)

        ON CONFLICT (city, observed_at)
        DO UPDATE SET
            temperature_2m = EXCLUDED.temperature_2m,
            relative_humidity_2m = EXCLUDED.relative_humidity_2m,
            precipitation = EXCLUDED.precipitation,
            wind_speed_10m = EXCLUDED.wind_speed_10m;
    """    
    with connection.cursor() as cursor:
        cursor.executemany(insert_query, rows)

    connection.commit()

    print(f"Loaded {len(rows)} weather rows into PostgreSQL.")

def main():
    """Load weather data from S3 into PostgreSQL."""

    target_date = get_target_date()
    connection = connect_to_postgres()
    try:
        for city in CITIES:
            weather_data = read_weather_from_s3(city, target_date)

            rows = build_weather_rows(city, weather_data)

            insert_weather_rows(connection, rows)

    finally:
        connection.close()


if __name__ == "__main__":
    main()