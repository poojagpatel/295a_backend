import os
from pymongo import MongoClient
from dotenv import load_dotenv


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
    print("db_name: " + db_name, "collection_name: " + collection_name,"db_host: " + db_host, "db_port: "+(db_port))
                                                                    
    connection_string = (
        f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        "?authSource=admin"
    )

    # Initialize MongoDB client
    client = MongoClient(connection_string)
    
    return client


def insert_earthquake_data(collection, earthquake_data):
    # Insert the earthquake data
    insert_result = collection.insert_many(earthquake_data)
    print(f"Inserted {len(insert_result.inserted_ids)} documents")


def retrieve_all_documents(collection):
    client=connect_to_mongodb()
    # Retrieve all documents from the collection
    documents = client.collection.find({})
    # Print all documents
    for document in documents:
        print(document)

