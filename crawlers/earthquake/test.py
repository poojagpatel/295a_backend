import json
import requests
from datetime import datetime


with open("earthquake.json", "r") as file:
    data = json.load(file)

    last_updated = datetime.strptime(
        data["metadata"]["lastUpdated"], "%Y-%m-%dT%H:%M:%S"
    )

    api_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={last_updated}"
    # Make the API request for new data
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response for new data
        new_earthquake_data = response.json()
        # Filter the new data based on last_updated time
        filtered_data = [
            record
            for record in new_earthquake_data["features"]
            if datetime.fromtimestamp(record["properties"]["time"] / 1000)
            > last_updated
        ]

    print("filtered_data: ", filtered_data)
