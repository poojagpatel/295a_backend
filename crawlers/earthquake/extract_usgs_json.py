#!/usr/bin/env python

from itertools import count
import pdb
import sys
import os
import json
import logging
from datetime import datetime, timedelta

import requests

# Configure logging
logging.basicConfig(
    filename="earthquake.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Calculate the start date for the new data (e.g., 1 day ago)
start_date = datetime.now().date()
start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")

# Define the API URL with the date range for new data
api_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date_str}"

try:
    with open("earthquake.json", "r") as file:
        data = json.load(file)
        last_updated = datetime.strptime(
            data["metadata"]["lastUpdated"], "%Y-%m-%dT%H:%M:%S"
        )

    # Make the API request for new data
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response for new data
        new_earthquake_data = response.json()

        filtered_data = {}

        filtered_data["features"] = [
            record
            for record in new_earthquake_data["features"]
            if datetime.fromtimestamp(record["properties"]["time"] / 1000)
            > last_updated
        ]
        # Update the last update date in the "metadata" section
        new_last_updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        filtered_data["metadata"] = {}
        filtered_data["type"] = "FeatureCollection"
        filtered_data["metadata"]["lastUpdated"] = new_last_updated
        filtered_data["metadata"]["url"] = api_url
        filtered_data["metadata"]["title"] = "USGS Earthquakes"
        filtered_data["metadata"]["status"] = 200
        filtered_data["metadata"]["count"] = len(filtered_data["features"])

        # # Convert Unix epoch milliseconds timestamps to datetime objects
        for feature in filtered_data["features"]:
            timestamp_in_milliseconds = feature["properties"]["time"]
            timestamp_in_seconds = timestamp_in_milliseconds / 1000.0
            feature["properties"]["time"] = datetime.fromtimestamp(timestamp_in_seconds)

        # Sort the new data in descending order based on time (latest first)
        filtered_data["features"].sort(
            key=lambda x: x["properties"]["time"], reverse=True
        )

        # Save the new data to a JSON file
        with open("earthquake.json", "w") as json_file:
            json.dump(filtered_data, json_file, default=str, indent=4)

        print(
            "New earthquake data saved to earthquake.",
            count(filtered_data["features"]),
        )

        # Logging success
        logging.info("New earthquake data appended to earthquake.json")
    else:
        print(f"Failed to retrieve new data. Status code: {response.status_code}")
except Exception as e:
    # Logging an error if any exception occurs
    logging.error(f"An error occurred: {str(e)}")
