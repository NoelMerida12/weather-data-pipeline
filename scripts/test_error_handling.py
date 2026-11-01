import unittest
from unittest.mock import patch
from requests.exceptions import Timeout

from extract_weather import fetch_weather, get_city_coordinates



class TestWeatherErrors(unittest.TestCase):

    @patch(
        "extract_weather.requests.get",
        side_effect=Timeout("Simulated API timeout")
    )
    def test_weather_timeout(self, mock_get):


        coordinates =  {
            "name": "Barcelona",
            "latitude": 41.38,
            "longitude": 2.17,
        }


        with self.assertRaisesRegex(
            RuntimeError,
            "Failed to fetch weather for Barcelona"
        ):
            fetch_weather(coordinates,"2026-10-31")
    @patch(
        "extract_weather.requests.get",
        side_effect=Timeout("Simulated geocoding timeout")
    )
   
    def test_geocoding_timeout(self, mock_get):

        with self.assertRaisesRegex(
            RuntimeError,
            "Failed to get coordinates for Madrid"
        ):
            get_city_coordinates("Madrid")


    @patch("extract_weather.requests.get")
    def test_incomplete_weather_data(self, mock_get):

        # Simulate an API response containing only 20 hours.
        mock_get.return_value.json.return_value = {
            "hourly": {
                "time": [
                    f"2026-10-31T{hour:02d}:00"
                    for hour in range(20)
                ]
            }
        }

        coordinates = {
            "name": "Barcelona",
            "latitude": 41.38,
            "longitude": 2.17,
        }

        # Verify that incomplete data raises an error.
        with self.assertRaisesRegex(
            ValueError,
            "expected 24 hours, got 20"
        ):
            fetch_weather(coordinates, "2026-10-31")

    @patch("extract_weather.requests.get")
    def test_missing_weather_values(self, mock_get):

        # Simulate 24 hours of weather data.
        temperatures = [20.0] * 24

        # Simulate a missing temperature value.
        temperatures[5] = None

        mock_get.return_value.json.return_value = {
            "hourly": {
                "time": [
                    f"2026-10-31T{hour:02d}:00"
                    for hour in range(24)
                ],
                "temperature_2m": temperatures,
                "relative_humidity_2m": [60] * 24,
                "precipitation": [0.0] * 24,
                "wind_speed_10m": [10.0] * 24,
            }
        }

        coordinates = {
            "name": "Barcelona",
            "latitude": 41.38,
            "longitude": 2.17,
        }

        # Verify that missing values are rejected.
        with self.assertRaisesRegex(
            ValueError,
            "Missing values in temperature_2m"
        ):
            fetch_weather(coordinates, "2026-10-31")

            
if __name__ == "__main__":
    unittest.main()