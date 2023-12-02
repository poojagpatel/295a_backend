import json

import pymongo

from utility import connect_to_mongodb

def update_or_insert_earthquake(record):
    # Update or insert the earthquake record into the MongoDB collection
    query = {"properties.code": record["properties"]["code"]}
    result = collection.replace_one(query, record, upsert=True)
    print(f"Record updated: {result.modified_count}, Record inserted: {result.upserted_id}")


# Read data from the JSON file
with open("./earthquake.json", "r") as file:
    data = json.load(file)

client=connect_to_mongodb()

db = client['ENDDB'] 
collection = db["earthquakes"]  # Replace with your actual collection name

# Insert data into MongoDB
for feature in data["features"]:
    # Use 'id' as '_id' in MongoDB
    feature["_id"] = feature["id"]
    del feature["id"]  # Remove the original 'id' field
    update_or_insert_earthquake(feature)

print("Data inserted into MongoDB.")