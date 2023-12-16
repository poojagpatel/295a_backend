from flask import Flask, jsonify
from pymongo import MongoClient,DESCENDING

from utility import connect_to_mongodb



app = Flask(__name__)

client=connect_to_mongodb()

db = client['ENDDB'] 

# Endpoint to fetch all data from the 'earthquakes' collection
@app.route('/api/eq', methods=['GET'])
def get_earthquakes():
    try:
        # Access the 'earthquakes' collection
        earthquakes_collection = db['earthquakes']

        # Use the find method on the collection to retrieve all data
        # Sort the data based on the 'updated' field in descending order
        earthquakes_data = earthquakes_collection.find({}, {'_id': 0}).sort('properties.updated', DESCENDING)

        # Convert the cursor to a list and jsonify the result
        result = list(earthquakes_data)

        return jsonify(result)

    except Exception as e:
        # Handle exceptions and return an appropriate error response
        return jsonify({'error': str(e)}), 500  # HTTP 500 for internal server error


# Endpoint to fetch all data from the 'Wildfire' collection
#todo: add data in wildfire collection first.

@app.route('/api/wf', methods=['GET'])

def get_wildfires():
    # Access the 'earthquakes' collection
    earthquakes_collection = db['wildfires']

    # Use the find method on the collection to retrieve all data
    earthquakes_data = earthquakes_collection.find({}, {'_id': 0})

    # Convert the cursor to a list and jsonify the result
    return jsonify(list(earthquakes_data))

if __name__ == '__main__':
    app.run(debug=True)
