import json
from pymongo import MongoClient, UpdateOne

from utility import async_send_firebase_notification, connect_to_mongodb

# from utility import async_send_firebase_notification, connect_to_mongodb

async def update_or_insert_earthquakes_async(records, collection):
    bulk_operations = [
        UpdateOne(
            {"properties.code": record["properties"]["code"]},
            {"$set": record},
            upsert=True
        )
        for record in records
    ]

    result = collection.bulk_write(bulk_operations)

    # Notify Firebase if new records are inserted
    if result.upserted_count > 0:
        record_ids = [record['_id'] for record in records if record['_id']]
        # await async_send_firebase_notification("New Earthquake Data", f"{result.upserted_count} new records inserted into MongoDB: {record_ids}")

    print(f"Records updated: {result.modified_count}, Records inserted: {result.upserted_count}")

async def main():
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
    await update_or_insert_earthquakes_async(data["features"], collection)

    print("Data inserted into MongoDB.")

# Run the asynchronous function
import asyncio
asyncio.run(main())
