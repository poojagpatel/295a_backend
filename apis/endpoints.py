#!/usr/bin/env python3

from flask import Flask, jsonify
from pymongo import ASCENDING, MongoClient, DESCENDING
from flask_cors import CORS
import os
import openai
from dotenv import load_dotenv

from utility import connect_to_mongodb, get_conversation_chain

from flask import request

from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from openai import OpenAI

load_dotenv()
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32 MB

CORS(app)  # This will enable CORS for all routes

openai_api_key = os.getenv("OPENAI_API_KEY")

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
            .sort("properties.time", DESCENDING)
            .skip(skip)
            .limit(page_size)
        )
        # uniqueID: String
        # Type: String (earthquake/wildfire/etc…)
        # Time: String
        # Title: String
        # Description: String
        # Url: String
        # latitude: Double,
        # longitude: Double
        # intensity: Double

        # Convert the cursor to a list and jsonify the result
        data = list(earthquakes_data)
        formatted_data = []

        for item in data:
            unique_id = item["properties"]["code"]
            event_type = item["type"]
            time = item["properties"]["time"]
            title = item["properties"]["title"]
            description = item["properties"].get(
                "detail", ""
            )  # If 'alert' is not present, set to empty string
            url = item["properties"]["url"]
            latitude = item["geometry"]["coordinates"][1]
            longitude = item["geometry"]["coordinates"][0]
            intensity = item["properties"]["mag"]

            formatted_data.append(
                {
                    "uniqueID": unique_id,
                    "Type": event_type,
                    "Time": time,
                    "Title": title,
                    "Description": description,
                    "Url": url,
                    "latitude": latitude,
                    "longitude": longitude,
                    "intensity": intensity,
                }
            )

        return jsonify(formatted_data)

    except Exception as e:
        # Handle exceptions and return an appropriate error response
        return jsonify({"error": str(e)}), 500  # HTTP 500 for internal server error


@app.route("/api/eq_by_time", methods=["GET"])
def get_earthquakes_by_time():
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
      - start_time:
        in: query
        type: string
        description: The start time from which the records need to be retrieved.
      - end_time:
        in: query
        type: string
        description: The end time from which the records need to be retrieved.
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
            earthquakes_collection.find(
                {
                    "properties.time": {
                        "$gte": str(
                            request.args.get("start_time", "2024-05-02 08:00:00")
                        ),
                        "$lte": str(
                            request.args.get("end_time", "2024-05-02 09:00:00")
                        ),
                    }
                }
            )
            .sort("properties.time", ASCENDING)
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
    earthquake_data = collection.find_one({"properties.code": code})
    # Extracting desired fields
    unique_id = earthquake_data["properties"]["code"]
    event_type = earthquake_data["properties"]["type"]
    time = earthquake_data["properties"]["time"]
    title = earthquake_data["properties"]["title"]
    description = earthquake_data["properties"]["place"]
    url = earthquake_data["properties"]["url"]
    latitude = earthquake_data["geometry"]["coordinates"][1]
    longitude = earthquake_data["geometry"]["coordinates"][0]
    intensity = earthquake_data["properties"]["mag"]

    # Creating new dictionary
    desired_data = {
        "uniqueID": unique_id,
        "Type": event_type,
        "Time": time,
        "Title": title,
        "Description": description,
        "Url": url,
        "latitude": latitude,
        "longitude": longitude,
        "intensity": intensity,
    }

    if earthquake_data:
        return jsonify(desired_data)
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
            .sort("properties.Updated", DESCENDING)
            .skip(skip)
            .limit(page_size)
        )

        # Convert the cursor to a list and jsonify the result
        data = list(wildfire_data)

        formatted_data = []

        for item in data:
            unique_id = item["properties"]["UniqueId"]
            event_type = item["properties"]["Type"]
            time = item["properties"]["Started"]
            title = item["properties"]["Name"]
            description = (
                item["properties"]["County"] + ", " + item["properties"]["Location"]
            )
            url = item["properties"]["Url"]
            latitude = item["geometry"]["coordinates"][1]
            longitude = item["geometry"]["coordinates"][0]
            intensity = item["properties"]["AcresBurned"]

            formatted_data.append(
                {
                    "uniqueID": unique_id,
                    "Type": event_type,
                    "Time": time,
                    "Title": title,
                    "Description": description,
                    "Url": url,
                    "latitude": latitude,
                    "longitude": longitude,
                    "intensity": intensity,
                }
            )

        return jsonify(formatted_data)

    except Exception as e:
        # Handle exceptions and return an appropriate error response
        return jsonify({"error": str(e)}), 500  # HTTP 500 for internal server error


@app.route("/api/wf_by_time", methods=["GET"])
def get_wildfires_by_time():
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
      - start_time:
        in: query
        type: string
        description: The start time from which the records need to be retrieved.
      - end_time:
        in: query
        type: string
        description: The end time from which the records need to be retrieved.
    responses:
      200:
        description: A list of earthquake data for the requested page, sorted by the 'updated' field in descending order.
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
        # Sort the data based on the 'updated' field in ascending order
        wildfires_data = (
            wildfire_collection.find(
                {
                    "properties.Updated": {
                        "$gte": str(
                            request.args.get("start_time", "2024-05-03T12:10:48Z")
                        ),
                        "$lte": str(
                            request.args.get("end_time", "2024-05-03T13:50:48Z")
                        ),
                    }
                }
            )
            .sort("properties.Updated", ASCENDING)
            .skip(skip)
            .limit(page_size)
        )
        # Convert the cursor to a list and jsonify the result
        result = list(wildfires_data)
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
    data = collection.find_one({"properties.UniqueId": code})
    # Extracting desired fields
    unique_id = data["properties"]["UniqueId"]
    event_type = data["properties"]["Type"]
    time = data["properties"]["Started"]
    title = data["properties"]["Name"]
    description = data["properties"]["County"] + ", " + data["properties"]["Location"]
    url = data["properties"]["Url"]
    latitude = data["geometry"]["coordinates"][1]
    longitude = data["geometry"]["coordinates"][0]
    intensity = data["properties"]["AcresBurned"]

    # Creating new dictionary
    desired_data = {
        "uniqueID": unique_id,
        "Type": event_type,
        "Time": time,
        "Title": title,
        "Description": description,
        "Url": url,
        "latitude": latitude,
        "longitude": longitude,
        "intensity": intensity,
    }

    if data:
        return jsonify(desired_data)
    else:
        return jsonify({"message": "Wildfire not found"}), 404


@app.route("/api/weather", methods=["GET"])
def get_weather_misc():
    """
    Retrieves paginated weather data from the 'weather_misc' collection in the database.
    ---
    parameters:
        - in: query
          name: page
          type: integer
          description: The page number to retrieve. Defaults to 1.
        - in: query
          name: page_size
          type: integer
          description: The number of records per page. Defaults to 10.
    responses:
        200:
            description: A list of weather data for the requested page, sorted by the 'effective' field in descending order.
        500:
            description: If an exception occurs while retrieving the data.
    """
    try:
        # Access the 'weather_misc' collection
        weather_misc_collection = db["weather_misc"]

        # Pagination parameters
        page = int(request.args.get("page", 1))  # Default page is 1
        page_size = int(request.args.get("page_size", 10))  # Default page size is 10

        # Calculate skip value based on page number and page size
        skip = (page - 1) * page_size

        # Use the find method on the collection to retrieve paginated data
        # Sort the data based on the 'updated' field in descending order
        weather_misc_data = (
            weather_misc_collection.find({}, {"_id": 0})
            .sort("properties.effective", DESCENDING)
            .skip(skip)
            .limit(page_size)
        )

        # Convert the cursor to a list and jsonify the result
        result = list(weather_misc_data)

        return jsonify(result)

    except Exception as e:
        # Handle exceptions and return an appropriate error response
        return jsonify({"error": str(e)}), 500  # HTTP 500 for internal server error


@app.route("/api/wt_by_time", methods=["GET"])
def get_weather_by_time():
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
      - start_time:
        in: query
        type: string
        description: The start time from which the records need to be retrieved.
      - end_time:
        in: query
        type: string
        description: The end time from which the records need to be retrieved.
    responses:
      200:
        description: A list of earthquake data for the requested page, sorted by the 'updated' field in descending order.
      500:
        description: If an exception occurs while retrieving the data.
    """
    try:
        # Access the 'Wildfire' collection
        weather_collection = db["weather_misc"]

        # Pagination parameters
        page = int(request.args.get("page", 1))  # Default page is 1
        page_size = int(request.args.get("page_size", 10))  # Default page size is 10

        # Calculate skip value based on page number and page size
        skip = (page - 1) * page_size

        # Use the find method on the collection to retrieve paginated data
        # Sort the data based on the 'updated' field in ascending order
        weather_data = (
            weather_collection.find(
                {
                    "properties.sent": {
                        "$gte": str(
                            request.args.get("start_time", "2024-04-29T15:00:00")
                        ),
                        "$lte": str(
                            request.args.get("end_time", "2024-04-29T16:00:00")
                        ),
                    }
                }
            )
            .sort("properties.sent", ASCENDING)
            .skip(skip)
            .limit(page_size)
        )
        # Convert the cursor to a list and jsonify the result
        result = list(weather_data)
        return jsonify(result)

    except Exception as e:
        # Handle exceptions and return an appropriate error response
        return jsonify({"error": str(e)}), 500  # HTTP 500 for internal server error


@app.route("/api/weather/<string:code>", methods=["GET"])
def get_weather_by_code(code):
    """
    Retrieves a weather record based on the given code.
    ---
    parameters:
        - name: code
          in: path
          type: string
          required: true
          description: The code of the weather record to retrieve.
    responses:
        200:
            description: The weather record with the given code.
        404:
            description: If no weather record was found with the given code.
    """
    # Query MongoDB to find the weather record by code
    weather_misc_collection = db["weather_misc"]
    weather = weather_misc_collection.find_one({"properties.id": code})
    if weather:
        return jsonify(weather)
    else:
        return jsonify({"message": "Weather record not found"}), 404


@app.route("/api/event_chat", methods=["POST"])
def chat_with_event():
    """
    Initiate a chat about an event using OpenAI's API.
    ---
    parameters:
        - in: body
          name: event
          description: The event to chat about.
          required: true
          schema:
            type: object
            properties:
                event:
                    type: object
                    description: The data of the event.
                question:
                    type: string
                    description: The question to ask about the event.
    responses:
        200:
            description: Chat response with the event.
    """
    data = request.get_json()
    event = data.get("event")
    question = data.get("question")
    # ... rest of your code ...
    try:
        if event:
            # Use OpenAI's API to generate a response based on the prompt
            # response = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     messages=[
            #         {
            #             "role": "system",
            #             "content": f"give answers to the questions from {event} data in 60 words or less",
            #         },
            #         {"role": "user", "content": question},
            #     ],
            # )
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"give answers to the questions from {event} data in 60 words or less",
                    },
                    {"role": "user", "content": question},
                ],
            )

            # Extract the chat response from the OpenAI API response
            chat_response = response["choices"][0]["message"]["content"]

            # Return the chat response
            return jsonify({"chat_response": chat_response}), 200
        else:
            # If no event is found in the database with the provided event ID, return a 404 error
            return jsonify(
                {"error": "No event found in the database with the provided event ID"}
            ), 404

    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({"error": str(e)}), 500


@app.route("/api/ask", methods=["POST"])
def ask():
    """
    Ask a question
    ---
    parameters:
        - name: question
          in: body
          type: string
          required: true
          description: The question to ask
    responses:
        200:
            description: The answer to the question
            schema:
                type: object
                properties:
                    answer:
                        type: string
    """
    question = request.json.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    import chromadb

    chroma_client = chromadb.HttpClient(host=os.getenv("DB_HOST"), port=8000)

    vectordb = Chroma(
        client=chroma_client,
        collection_name="langchain",
        embedding_function=OpenAIEmbeddings(),
    )
    op = get_conversation_chain(vectordb)
    response = op({"question": question})

    return jsonify({"answer": response["answer"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
