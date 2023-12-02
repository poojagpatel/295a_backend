import json
from pymongo import MongoClient, UpdateOne
from utility import connect_to_mongodb

def update_or_insert_earthquakes(records):
    # Create a list of UpdateOne operations for bulk update/insert
    operations = [
        UpdateOne(
            {"properties.code": record["properties"]["code"]},
            {"$set": record},
            upsert=True
        )
        for record in records
    ]

    # Execute bulk write operations
    result = collection.bulk_write(operations)

    print(f"Records updated: {result.modified_count}, Records inserted: {result.upserted_count}")

# Read data from the JSON file
with open("./earthquake.json", "r") as file:
    data = json.load(file)

client = connect_to_mongodb()

db = client['ENDDB']
collection = db["earthquakes"]  # Replace with your actual collection name

# Use 'id' as '_id' in MongoDB for each feature
for feature in data["features"]:
    feature["_id"] = feature["id"]
    del feature["id"]  # Remove the original 'id' field

# Insert data into MongoDB using bulk operations
update_or_insert_earthquakes(data["features"])

print("Data inserted into MongoDB.")
