
import requests
from bs4 import BeautifulSoup

# URL of the website
url = 'https://inciweb.wildfire.gov/accessible-view'

# Send an HTTP request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table you want to scrape (you might need to inspect the page source to get the right tag and class)
    table = soup.find(
        'table', {'class': 'usa-table cols-5 sticky-enabled sticky-table'})

    # Check if the table is found
    if table:
        # Extract data from the table
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if columns:
                # Print or store the data as needed
                print([column.get_text(strip=True) for column in columns])
    else:
        print('Table not found on the page.')
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
