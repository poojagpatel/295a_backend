import os
from pymongo import MongoClient
from dotenv import load_dotenv


def main():
    # Load environment variables from .env file
    load_dotenv()

    # MongoDB connection string
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '27017')
    db_name = os.getenv('DB_NAME', 'mydatabase')
    collection_name = os.getenv('COLLECTION_NAME', 'mycollection')

    connection_string = (
        f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        "?authSource=admin"
    )

    # Initialize MongoDB client
    client = MongoClient(connection_string)

    # Select your database
    db = client[db_name]

    # Select your collection
    collection = db[collection_name]

    # Retrieve all documents from the collection
    documents = collection.find()

    # Print all documents
    for document in documents:
        print(document)


if __name__ == "__main__":
    main()
