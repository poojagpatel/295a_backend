#!/bin/bash

# Step 1: Earthquake
cd crawlers/earthquake
python extract_usgs_json.py
python load_json_mongodb.py
cd ../..

# Step 2: Weather
cd crawlers/weather_gov
python extract_weather_json.py
python load_json_mongodb.py
cd ../..

# Step 3: Wildfire
cd crawlers/wildfire
python extract.py
python load_json_mongodb.py
cd ../..

# Step 4: Embeddings
python3 embeddings.py