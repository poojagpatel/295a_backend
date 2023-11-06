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
    db_name = os.getenv('DB_NAME', 'sample_database')
    collection_name = os.getenv('COLLECTION_NAME', 'users')
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

    # Insert the sample document
    sample_data = {
        "name": "John Doe",
        "age": 30,
        "address": {
            "street": "123 Elm Street",
            "city": "Springfield",
            "zip": "12345"
        },
        "email": "johndoe@example.com",
        "is_active": True,
        "scores": [70, 88, 92]
    }
    insert_result = collection.insert_one(sample_data)
    print(f"Inserted document id: {insert_result.inserted_id}")

    # Retrieve all documents from the collection
    documents = collection.find()
    # Print all documents
    for document in documents:
        print(document)


if __name__ == "__main__":
    main()
