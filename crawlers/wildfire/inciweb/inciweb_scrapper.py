import pdb
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup


def scrape_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(
            f'Failed to retrieve page with status code: {response.status_code}')
        return None  # Return None if the request was unsuccessful

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all(
        'table', class_='usa-table usa-table--compact usa-table--striped')

    # Initialize a single dictionary to hold all data for this URL
    data_dict = {'URL': url}  # Add the URL as the first key-value pair

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['th', 'td'])
            key = cols[0].text.strip()
            value = cols[1].text.strip()
            # Add the key-value pair to data_dict
            data_dict[key] = value

    return data_dict


# List of URLs to scrape
urls = ['https://inciweb.nwcg.gov//incident-information/caknp-redwood-fire',
        # 'https://inciweb.nwcg.gov//incident-information/casqf-rabbit-fire',
        # 'https://inciweb.nwcg.gov//incident-information/orrsf-anvil-fire',
        # 'https://inciweb.nwcg.gov//incident-information/xx1002-flat-fire',
        # 'https://inciweb.nwcg.gov//incident-information/castf-2023stfquarry-fire'

        ]


# Initialize an empty list to hold all data dictionaries
all_data = []

# Loop through each URL and scrape data
for url in urls:
    data = scrape_data(url)
    if data:  # Check if data was successfully scraped
        # Append the data dictionary to all_data
        all_data.append(data)

# Convert the list of dictionaries to a DataFrame
all_data_df = pd.DataFrame(all_data)

# Print the DataFrame
all_data_df.to_csv("news.csv")
