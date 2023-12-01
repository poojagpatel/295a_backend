#!/usr/bin/env python

import sys
import os
import json
import logging
from datetime import datetime, timedelta

from pymongo import MongoClient
from utility import convert_unix_milliseconds_to_datetime
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(filename="earthquake.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Function to connect to MongoDB and return the collection
def connect_to_mongodb():
    # Load environment variables from .env file
    load_dotenv()
    
    # MongoDB connection string
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '27017')
    db_name = os.getenv('DB_NAME', 'sample_database')
    collection_name = os.getenv('COLLECTION_NAME', 'earthquakes')
    
    connection_string = (
        f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        "?authSource=admin"
    )

    # Initialize MongoDB client
    client = MongoClient(connection_string)
    
    # Select your database and collection
    db = client[db_name]
    collection = db[collection_name]
    
    return collection

# Function to convert Unix epoch milliseconds timestamps to datetime objects
def convert_timestamps(features):
    for feature in features:
        timestamp_in_milliseconds = feature["properties"]["time"]
        timestamp_in_seconds = timestamp_in_milliseconds / 1000.0
        feature["properties"]["time"] = datetime.fromtimestamp(timestamp_in_seconds)

# Function to insert new earthquake records into MongoDB
def insert_new_records(collection, features):
    # Insert new records at the beginning of the collection
    for feature in reversed(features):
        # Check if the earthquake record with the same ID already exists
        existing_record = collection.find_one({"id": feature["id"]})
        if not existing_record:
            collection.insert_one(feature)

# Function to retrieve the latest timestamp from MongoDB
def get_latest_timestamp(collection):
    latest_record = collection.find_one(sort=[("properties.time", -1)])
    if latest_record:
        return latest_record["properties"]["time"]
    else:
        # If no records are present, return a default start date
        return datetime.now() - timedelta(days=30)

# Calculate the latest timestamp from MongoDB
collection = connect_to_mongodb()
latest_timestamp = get_latest_timestamp(collection)

# Calculate the end date as the current date
end_date = datetime.now()
end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")

# Define the API URL with the date range from the latest timestamp to the current date
api_url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={latest_timestamp.strftime('%Y-%m-%dT%H:%M:%S')}&orderby=time"

try:
    # Make the API request for data
    response = requests.get(api_url)

    import pdb; pdb.set_trace()
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response for data
        earthquake_data = response.json()

        # Convert Unix epoch milliseconds timestamps to datetime objects
        convert_timestamps(earthquake_data["features"])

        # Sort the data in descending order based on time
        earthquake_data["features"].sort(key=lambda x: x["properties"]["time"], reverse=True)

        # Insert only new earthquake records into MongoDB
        # insert_new_records(collection, earthquake_data["features"])

        print("New earthquake data appended to MongoDB")

        # Logging success
        logging.info("New earthquake data appended to MongoDB")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
except Exception as e:
    # Logging an error if any exception occurs
    logging.error(f"An error occurred: {str(e)}")
