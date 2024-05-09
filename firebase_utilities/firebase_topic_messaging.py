from sys import exception
from turtle import st
import firebase_admin
from firebase_admin import credentials, messaging
import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta


load_dotenv()

cred = credentials.Certificate("./emergency-news-delivery-firebase-adminsdk.json")
app = firebase_admin.initialize_app(cred)


def send_message_to_topic(topic_name, data):
    topic_name = topic_name
    message = messaging.Message(data=data, topic=topic_name)
    response = messaging.send(message)
    print("Successfully sent message:", response)


def get_earthquakes():
    url = os.getenv("API_URL") + "/eq_by_time"
    page_counter = 1
    page_size = 20
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

    # start_time = '2024-05-02 09:30:00'
    # end_time = '2024-05-02 10:00:00'

    num_results = 0
    data = []
    while True:
        params = {
            "page": page_counter,
            "page_size": page_size,
            "start_time": start_time,
            "end_time": end_time,
        }
        response = requests.get(url, params=params)
        result = response.json()
        num_results += len(result)
        page_counter += 1

        print(
            f"Number of earthquake records fetched for the timeframe {start_time} - {end_time} : {num_results}."
        )
        if len(result) == 0:
            break

        data.extend(result)

    return data


def get_wildfires():
    url = os.getenv("API_URL") + "/wf_by_time"
    page_counter = 1
    page_size = 20
    end_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    start_time = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    num_results = 0
    data = []
    while True:
        params = {
            "page": page_counter,
            "page_size": page_size,
            "start_time": start_time,
            "end_time": end_time,
        }
        response = requests.get(url, params=params)
        result = response.json()
        num_results += len(result)
        page_counter += 1
        print(
            f"Number of wilfire records fetched for the timeframe {start_time.replace('T', ' ').replace('Z', '')} - {end_time.replace('T', ' ').replace('Z', '')} : {num_results}."
        )

        if len(result) == 0:
            break

        data.extend(result)
    return data


def get_weather_alerts():
    url = os.getenv("API_URL") + "/wt_by_time"
    page_counter = 1
    page_size = 20
    end_time = datetime.now().strftime("%Y-%m-%dT%H:00:00")
    start_time = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00")
    start_time = "2024-04-29T15:00:00"
    end_time = "2024-04-29T16:00:00"

    num_results = 0
    data = []
    while True:
        params = {
            "page": page_counter,
            "page_size": page_size,
            "start_time": start_time,
            "end_time": end_time,
        }
        response = requests.get(url, params=params)
        result = response.json()
        num_results += len(result)
        page_counter += 1

        print(
            f"Number of weather alert records fetched for the timeframe {start_time}, {end_time} : {num_results}."
        )
        if len(result) == 0:
            break

        data.extend(result)
    return data


def send_earthquake_messages():
    topic_name = "earthquake"
    events = get_earthquakes()
    if not events:
        print("No records found to send to the firebase topic.")
        return None

    msg_count = 0
    for event in events:
        try:
            event_coords = (
                event["geometry"]["coordinates"][1],
                event["geometry"]["coordinates"][0],
            )
            data = {
                "id": event["_id"],
                "topic_name": topic_name,
                "title": event["properties"]["title"],
                "location": event["properties"]["place"],
                "time_started": event["properties"]["time"][:19],
                "magnitude": str(event["properties"]["mag"]),
                "url": event["properties"]["url"],
                "type": event["properties"]["type"],
                "latitude": str(event_coords[0]),
                "longitude": str(event_coords[1]),
                "msg_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            send_message_to_topic(topic_name, data)
            msg_count += 1

        except Exception as e:
            print("Message could not be delievered.")
    print("Total messages sent: ", msg_count)


def send_wildfire_messages():
    topic_name = "wildfire"
    events = get_wildfires()
    if not events:
        print("No records found to send to the firebase topic.")
        return None

    msg_count = 0
    for event in events:
        try:
            data = {
                "id": event["_id"],
                "topic_name": topic_name,
                "title": event["properties"]["Name"],
                "location": event["properties"]["Location"],
                "time_started": event["properties"]["Started"]
                .replace("T", " ")
                .replace("Z", ""),
                "time_updated": event["properties"]["Updated"]
                .replace("T", " ")
                .replace("Z", ""),
                "url": event["properties"]["Url"],
                "type": event["properties"]["Type"],
                "latitude": str(event["properties"]["Latitude"]),
                "longitude": str(event["properties"]["Longitude"]),
                "msg_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            send_message_to_topic(topic_name, data)
            msg_count += 1
        except Exception as e:
            print("Message could not be delievered.")

    print("Total messages sent: ", msg_count)


def send_weather_messages():
    topic_name = "weather"
    events = get_weather_alerts()
    if not events:
        print("No records found to send to the firebase topic.")
        return None

    msg_count = 0
    for event in events:
        try:
            polygon = event.get("geometry", None)
            result_string = ""

            if polygon:
                polygon_coordinates = polygon.get("coordinates", None)
                for coords in polygon_coordinates:
                    generator_expr = (str(element) for element in coords)
                    separator = ","
                    result_string = separator.join(generator_expr)

            data = {
                "id": event["_id"],
                "topic_name": topic_name,
                "title": event["properties"]["headline"],
                "location": event["properties"]["areaDesc"],
                "time_started": event["properties"]["sent"],
                "type": event["properties"]["event"],
                "severity": event["properties"]["severity"],
                "certainty": event["properties"]["certainty"],
                "urgency": event["properties"]["urgency"],
                "polygon_coordinates": result_string,
                "msg_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            send_message_to_topic(topic_name, data)
            msg_count += 1
        except Exception as e:
            print("Message could not be delievered.")
    print("Total messages sent: ", msg_count)


if __name__ == "__main__":
    send_earthquake_messages()
    send_wildfire_messages()
    # send_weather_messages()
