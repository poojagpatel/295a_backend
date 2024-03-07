#!/usr/bin/env python3

from flask import Flask, jsonify
from pymongo import MongoClient, DESCENDING


from .utility import connect_to_mongodb

from flask import request

app = Flask(__name__)

from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger

swagger = Swagger(app)


# Swagger UI setup
SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI (without trailing '/')
API_URL = "http://0.0.0.0:5000/static/swagger.json"  # Our API url (can be an URL)


# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be served at {SWAGGER_URL}/dist/
    API_URL,
    config={  # Swagger UI config overrides
        "app_name": "Earthquake and Wildfire API"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

client = connect_to_mongodb()
print("db client - ", client)

db = client["ENDDB"]


@app.route("/api/eq", methods=["GET"])
def get_earthquakes():
    """
    Retrieves paginated earthquake data
    ---
    parameters:
      - name: page
        in: query
        type: integer
        description: The page number to retrieve. Defaults to 1.
      - name: page_size
        in: query
        type: integer
        description: The number of records per page. Defaults to 10.
    responses:
      200:
        description: A list of earthquake data for the requested page, sorted by the 'updated' field in descending order.
      500:
        description: If an exception occurs while retrieving the data.
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
    Retrieves an earthquake record based on the given code.
    ---
    parameters:
      - name: code
        in: path
        type: string
        required: true
        description: The code of the earthquake record to retrieve.
    responses:
      200:
        description: The earthquake record with the given code.
      404:
        description: If no earthquake record was found with the given code.
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
    ---
    parameters:
      - name: page
        in: query
        type: integer
        description: The page number to retrieve. Defaults to 1.
      - name: page_size
        in: query
        type: integer
        description: The number of records per page. Defaults to 10.
    responses:
      200:
        description: A list of wildfire data for the requested page, sorted by the 'updated' field in descending order.
      500:
        description: If an exception occurs while retrieving the data.
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
    Retrieves a wildfire record based on the given code.
    ---
    parameters:
      - name: code
        in: path
        type: string
        required: true
        description: The code of the wildfire record to retrieve.
    responses:
      200:
        description: The wildfire record with the given code.
      404:
        description: If no wildfire record was found with the given code.
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
