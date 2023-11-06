import pdb
import requests

# Define the API endpoint URL
api_url = "https://crashviewer.nhtsa.dot.gov/CrashAPI//crashes/GetCaseList?states=1,51&fromYear=2022&toYear=2023&minNumOfVehicles=1&maxNumOfVehicles=6&format=json"

# Define the query parameters to retrieve the latest 10 crash reports
params = {
    "modelType": "SimpleSearch",
    "simpleSearch": {
        "dateFilter": "Year",
        "showIncapacitatedCount": "true",
        "dateYear": "2023",  # You can adjust the year as needed
    }
}

# Make the API request
response = requests.get(api_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    crash_data = response.json()
    pdb.set_trace()
    # Extract and print the latest 10 crash reports
    latest_crashes = crash_data[:10]
    for crash in latest_crashes:
        print(crash)
else:
    print(
        f"Failed to retrieve crash data. Status code: {response.status_code}")
