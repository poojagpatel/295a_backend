import firebase_admin
from firebase_admin import credentials, messaging

# Initialize the Firebase Admin SDK
cred = credentials.Certificate("emergency-news-delivery-firebase-adminsdk-2tiy5-34f226f552.json")
firebase_admin.initialize_app(cred)


def send_message(token):
    # Construct the message payload
    message = messaging.Message(
        notification=messaging.Notification(
            title="Hi from python",
            body="hello world"
        ),
        token=token)

    # Send the message
    response = messaging.send(message)
    print("Successfully sent message:", response)


def subscribe_to_topic(tokens, topic_name):
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = tokens

    # Subscribe the devices corresponding to the registration tokens to the topic.
    response = messaging.subscribe_to_topic(registration_tokens, topic_name)
    # See the TopicManagementResponse reference documentation for the contents of response.
    print(response)
    print(response.success_count, 'tokens were subscribed successfully')


def unsubscribe_to_topic(tokens, topic_name):
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = tokens

    # Unubscribe the devices corresponding to the registration tokens from the topic.
    response = messaging.unsubscribe_from_topic(registration_tokens, topic_name)
    print(response.success_count, 'tokens were unsubscribed successfully')


def send_message_to_topic(topic):
    # Sending message to the topic
    # The topic name can be optionally prefixed with "/topics/".
    topic = topic

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        topic=topic
    )

    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


if __name__ == '__main__':
    topic = 'python_alerts'
    tokens = [
        'cqbrfIfE0GIlvAAZslhAhz:APA91bF38ihhtbp304FZ25mnih4FB3BFgcnbKE3X9ZZJ-SIaGdJ1aQygqQqVO3BjG1cZVeLOhKVdgc5TSd9E9QINpNEBru0GIE9PruOW3IFspv5AHAV81wKKXQoIOxu2sJRCyDZ3jin0'
        ]
    subscribe_to_topic(tokens, topic)
    send_message_to_topic(topic)