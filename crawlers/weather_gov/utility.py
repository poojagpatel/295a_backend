import datetime
from dotenv import load_dotenv
import os
from pymongo import MongoClient

from pyfcm import FCMNotification

def convert_unix_milliseconds_to_datetime(milliseconds):
    return datetime.utcfromtimestamp(milliseconds / 1000.0)


def connect_to_mongodb():
    # Load environment variables from .env file
    load_dotenv()
    # MongoDB connection string
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '27017')
    db_name = os.getenv('DB_NAME', 'sample_database')
    collection_name = os.getenv('COLLECTION_NAME', 'weather_misc')
    print("db_name: " + db_name, "collection_name: " + collection_name,"db_host: " + db_host, "db_port: "+(db_port))
                                                                    
    connection_string = (
        f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        "?authSource=admin"
    )

    # Initialize MongoDB client
    client = MongoClient(connection_string)
    
    return client

async def async_send_firebase_notification(template,body):
    print("helllo from firebase")
    import firebase_admin
    from firebase_admin import credentials, messaging
    firebase_cred = credentials.Certificate("./fase.json")
    firebase_app = firebase_admin.initialize_app(firebase_cred)
    import pdb; pdb.set_trace()
    # This registration token comes from the client FCM SDKs.
    registration_token = 'YOUR_REGISTRATION_TOKEN'
    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    print("template: ",template,"body: ",body)


async_send_firebase_notification("test","test")