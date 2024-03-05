import datetime
from dotenv import load_dotenv
import os
from pymongo import MongoClient


def convert_unix_milliseconds_to_datetime(milliseconds):
    return datetime.utcfromtimestamp(milliseconds / 1000.0)


def connect_to_mongodb():
    # Load environment variables from .env file
    load_dotenv()
    # MongoDB connection string
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "27017")
    db_name = os.getenv("DB_NAME", "sample_database")
    collection_name = os.getenv("COLLECTION_NAME", "earthquakes")
    print(
        "db_name: " + db_name,
        "collection_name: " + collection_name,
        "db_host: " + db_host,
        "db_port: " + (db_port),
    )

    connection_string = (
        f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        "?authSource=admin"
    )

    # Initialize MongoDB client
    client = MongoClient(connection_string)

    return client
