import sys
import os
import json
import logging
from datetime import datetime, timedelta

import requests

# Configure logging
logging.basicConfig(
    filename="weather_gov.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Define the API URL with the date range for new data
api_url = f"https://api.weather.gov/alerts/active"

try:
    # Make the API request for new data
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON for the new data
        new_weather_gov_data = response.json()

        # Update the "metadata" section
        new_last_updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        new_weather_gov_data["metadata"] = {}
        new_weather_gov_data["metadata"]["lastUpdated"] = new_last_updated
        new_weather_gov_data["metadata"]["url"] = api_url
        new_weather_gov_data["metadata"]["title"] = "All active weather alerts"
        new_weather_gov_data["metadata"]["status"] = 200
        new_weather_gov_data["metadata"]["count"] = len(
            new_weather_gov_data["features"]
        )

        # Save the new data to a JSON file
        with open("weather_gov.json", "w") as json_file:
            json.dump(new_weather_gov_data, json_file, default=str, indent=4)

        print(
            f"New weather alert data saved to new_weather_gov_data.json (latest first)"
        )

        # Logging success
        logging.info("New weather alert data appended to new_weather_gov_data.json")

    else:
        print(f"Failed to retrieve new data. Status code: {response.status_code}")

except Exception as e:
    # Logging an error if any exception occurs
    logging.error(f"An error occurred: {str(e)}")
