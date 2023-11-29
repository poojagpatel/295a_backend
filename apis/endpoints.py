from flask import Flask, jsonify
from pymongo import MongoClient

from utilities import connect_to_mongodb

app = Flask(__name__)

client=connect_to_mongodb()

db = client['ENDDB']  # Replace 'your_database_name' with your actual database name

# Endpoint to fetch all data from the 'earthquakes' collection
@app.route('/api/eq', methods=['GET'])

def get_earthquakes():
    # Access the 'earthquakes' collection
    earthquakes_collection = db['earthquakes']

    # Use the find method on the collection to retrieve all data
    earthquakes_data = earthquakes_collection.find({}, {'_id': 0})

    # Convert the cursor to a list and jsonify the result
    return jsonify(list(earthquakes_data))


# Endpoint to fetch all data from the 'earthquakes' collection
@app.route('/api/wf', methods=['GET'])

def get_earthquakes():
    # Access the 'earthquakes' collection
    earthquakes_collection = db['wildfires']

    # Use the find method on the collection to retrieve all data
    earthquakes_data = earthquakes_collection.find({}, {'_id': 0})

    # Convert the cursor to a list and jsonify the result
    return jsonify(list(earthquakes_data))

if __name__ == '__main__':
    app.run(debug=True)
