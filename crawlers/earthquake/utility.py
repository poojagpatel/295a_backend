import datetime


def convert_unix_milliseconds_to_datetime(milliseconds):
    return datetime.utcfromtimestamp(milliseconds / 1000.0)
