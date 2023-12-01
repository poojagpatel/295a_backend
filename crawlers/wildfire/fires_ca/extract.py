import sys
import os
import json
import logging
from datetime import datetime, timedelta

import requests

# Configure logging
logging.basicConfig(filename="fires_ca.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Calculate current year
today = datetime.now()
year = today.year

# Define the API URL with the date range for new data
api_url = f"https://incidents.fire.ca.gov/umbraco/api/IncidentApi/GeoJsonList?year={year}"

try:
    # Make the API request for new data
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON for the new data
        new_fire_ca_data = response.json()

        # Sort the new data in descending order based on time (latest first)
        new_fire_ca_data["features"].sort(
            key=lambda x: x["properties"]["Started"], reverse=True)
        
        # Update the "metadata" section
        new_last_updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        new_fire_ca_data["metadata"] = {}
        new_fire_ca_data["metadata"]["lastUpdated"] = new_last_updated
        new_fire_ca_data["metadata"]["url"] = api_url
        new_fire_ca_data["metadata"]["title"] = "Fire CA Incidents"
        new_fire_ca_data["metadata"]["status"] = 200
        new_fire_ca_data["metadata"]["count"] = len(new_fire_ca_data["features"])

        # Save the new data to a JSON file
        with open("fires_ca.json", "w") as json_file:
            json.dump(new_fire_ca_data, json_file, default=str, indent=4)
        
        print(f"New fire data saved to fires_ca.json (latest first)")

        # Logging success
        logging.info("New fire data appended to fires_ca.json")

    else:
        print(
            f"Failed to retrieve new data. Status code: {response.status_code}")

except Exception as e:
    # Logging an error if any exception occurs
    logging.error(f"An error occurred: {str(e)}")
