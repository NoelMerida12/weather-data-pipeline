#Tools for working with dates and UTC timestamps.
from datetime import datetime, timedelta, timezone

# Manipulate file paths. 
from pathlib import Path

# To save python data as JSON files.

import json

# HTTP request to the Open-Meteo API.

import requests


# Open-Meteo endpoint used to request weather data.

WEATHER_API_URL ="https://api.open-meteo.com/v1/forecast"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Cities included

CITIES = [
    "Barcelona",
    "Madrid",
    "Valencia",
    "Sevilla",
    "Bilbao",
    "Malaga",
    "Zaragoza",
    "Murcia",
    "Palma",
    "Alicante",
]

# Hourly variables

HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
]

def get_city_coordinates(city):
    """Get latitude and longitude for a Spanish city."""

    parameters = {
        "name": city,
        "count": 1,
        "language": "en",
        "countryCode": "ES",
        "format": "json",
    }

    response = requests.get(
        GEOCODING_API_URL,
        params=parameters,
        timeout=30,
    )

    # Raise an error if the HTTP request was not successful.
    response.raise_for_status()

    # Convert the JSON response into a Python dictionary.
    data = response.json()

    # Check if the API found at least one city.
    if "results" not in data or not data["results"]:
        raise ValueError(f"No coordinates found for city: {city}")

    # Take the first result returned by the API.
    result = data["results"][0]

    # Return only the information needed.
    return {
        "name": result["name"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
    }

def get_target_date():
    """Return yesterday's date in UTC."""

    yesterday = datetime.now(timezone.utc).date() - timedelta(days=1)

    return yesterday.isoformat()


def fetch_weather(city_coordinates, target_date):
    """Download hourly wather data for one city and one date."""

    parameters = {
        "latitude": city_coordinates["latitude"],
        "longitude": city_coordinates["longitude"],
        "hourly": ",".join(HOURLY_VARIABLES),
        "start_date": target_date,
        "end_date": target_date,
        "timezone": "UTC",
    }

    response = requests.get(
        WEATHER_API_URL,
        params=parameters,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    # Check that the API response contains hourly data.
    if "hourly" not in data:
        raise ValueError ("The API response does not contain hourly weather data.")
    return data



def save_raw_data(city,target_date, data):
    """Save raw weather data as JSON file."""

    output_directory = (
        Path("/opt/airflow/data/raw/weather")
        / f"date={target_date}"
        / f"city={city.lower()}"
    )


    # Create the directory if it does not exist.
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )


    output_file = output_directory / "weather.json"

    # Open the file in write mode and save the JSON data.

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
        )
    return output_file


def main():
    """Run the weather extraction pipeline."""

    target_date = get_target_date()


    print(f"Extracting weather data for {target_date}")

    for city in CITIES:
        coordinates = get_city_coordinates(city)

        weather_data = fetch_weather(
        coordinates,
        target_date,
    )

        saved_file = save_raw_data(
        city,
        target_date,
        weather_data,
    )

        print(saved_file)

if __name__ == "__main__":
    main()