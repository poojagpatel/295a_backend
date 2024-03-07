#!/usr/bin/env python3

from flask import Flask, jsonify
from pymongo import MongoClient, DESCENDING

from .utility import connect_to_mongodb

from flask import request

app = Flask(__name__)

client = connect_to_mongodb()
print("db client - ", client)

db = client["ENDDB"]


@app.route("/api/eq", methods=["GET"])
def get_earthquakes():
    """
    Retrieves paginated earthquake data from the 'earthquakes' collection in the database.

    Query Parameters:
        page (int): The page number to retrieve. Defaults to 1.
        page_size (int): The number of records per page. Defaults to 10.

    Returns:
        JSON: A list of earthquake data for the requested page, sorted by the 'updated' field in descending order.

    Raises:
        HTTP 500: If an exception occurs while retrieving the data.
    """
    try:
        # Access the 'earthquakes' collection
        earthquakes_collection = db["earthquakes"]

        # Pagination parameters
        page = int(request.args.get("page", 1))  # Default page is 1
        page_size = int(request.args.get("page_size", 10))  # Default page size is 10

        # Calculate skip value based on page number and page size
        skip = (page - 1) * page_size

        # Use the find method on the collection to retrieve paginated data
        # Sort the data based on the 'updated' field in descending order
        earthquakes_data = (
            earthquakes_collection.find({}, {"_id": 0})
            .sort("properties.updated", DESCENDING)
            .skip(skip)
            .limit(page_size)
        )

        # Convert the cursor to a list and jsonify the result
        result = list(earthquakes_data)

        return jsonify(result)

    except Exception as e:
        # Handle exceptions and return an appropriate error response
        return jsonify({"error": str(e)}), 500  # HTTP 500 for internal server error


@app.route("/api/eq/<string:code>", methods=["GET"])
def get_earthquake_by_code(code):
    """
    Retrieves an earthquake record from the 'earthquakes' collection in the database based on the given code.

    Args:
        code (str): The code of the earthquake record to retrieve.

    Returns:
        JSON: The earthquake record with the given code, or a message indicating that the earthquake was not found.

    Raises:
        HTTP 404: If no earthquake record was found with the given code.
    """
    # Query MongoDB to find the earthquake record by code
    collection = db["earthquakes"]
    earthquake = collection.find_one({"properties.code": code})
    if earthquake:
        return jsonify(earthquake)
    else:
        return jsonify({"message": "Earthquake not found"}), 404


# Endpoint to fetch all data from the 'Wildfire' collection
# todo: add data in wildfire collection first.


@app.route("/api/wf", methods=["GET"])
def get_wildfires():
    """
    Retrieves paginated wildfire data from the 'wildfires' collection in the database.

    Query Parameters:
        page (int): The page number to retrieve. Defaults to 1.
        page_size (int): The number of records per page. Defaults to 10.

    Returns:
        JSON: A list of wildfire data for the requested page, sorted by the 'updated' field in descending order.

    Raises:
        HTTP 500: If an exception occurs while retrieving the data.
    """
    try:
        # Access the 'Wildfire' collection
        wildfire_collection = db["wildfires"]

        # Pagination parameters
        page = int(request.args.get("page", 1))  # Default page is 1
        page_size = int(request.args.get("page_size", 10))  # Default page size is 10

        # Calculate skip value based on page number and page size
        skip = (page - 1) * page_size

        # Use the find method on the collection to retrieve paginated data
        # Sort the data based on the 'updated' field in descending order
        wildfire_data = (
            wildfire_collection.find({}, {"_id": 0})
            .sort("properties.updated", DESCENDING)
            .skip(skip)
            .limit(page_size)
        )

        # Convert the cursor to a list and jsonify the result
        result = list(wildfire_data)

        return jsonify(result)

    except Exception as e:
        # Handle exceptions and return an appropriate error response
        return jsonify({"error": str(e)}), 500  # HTTP 500 for internal server error


@app.route("/api/wf/<string:code>", methods=["GET"])
def get_wildfire_by_code(code):
    """
    Get wildfire information by code.

    Args:
        code (str): The unique identifier code of the wildfire.

    Returns:
        dict: The JSON response containing the wildfire information if found, or a message indicating that the wildfire was not found.

    """
    # Query MongoDB to find the wildfire record by code
    collection = db["wildfires"]
    wildfire = collection.find_one({"properties.UniqueId": code})
    if wildfire:
        return jsonify(wildfire)
    else:
        return jsonify({"message": "Wildfire not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
