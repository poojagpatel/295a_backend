import requests

#!/usr/bin/env python
import requests
import json

# List of API URLs
api_urls = [
    "https://newsdata.io/api/1/news?apikey=pub_433808d30bab60f10fc4108f7d11b661deb6a&country=us&language=en&category=environment",
    "https://newsdata.io/api/1/news?apikey=pub_433808d30bab60f10fc4108f7d11b661deb6a&country=us&language=en&category=crime",
    "https://newsdata.io/api/1/news?apikey=pub_433808d30bab60f10fc4108f7d11b661deb6a&country=us&language=en&category=politics",
]

# Initialize an empty list to store all the news data
all_news_data = []

# Fetch data from each API
for api_url in api_urls:
    response = requests.get(api_url)
    if response.status_code == 200:
        news_data = response.json()
        all_news_data.append(news_data)

# Save all the news data to a JSON file
with open("api_news.json", "w") as json_file:
    json.dump(all_news_data, json_file, indent=4)
