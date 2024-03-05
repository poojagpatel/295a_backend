from bs4 import BeautifulSoup
import requests
import pandas as pd

def crawler():

    website_url = 'https://www.fire.ca.gov/incidents'
    response = requests.get(website_url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find('table', attrs={'id':'incidents'})
    headers = table.find('thead')
    header_cells = headers.find_all('th')
    columns = ['Link']
    for th in header_cells:
        columns.append(th.text)
    print(columns)


    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    prefix_url = 'https://www.fire.ca.gov'

    for row in rows:
        curr = []
        incident_th = row.find('th')
        lnk = incident_th.find('a')
        curr.append(prefix_url + lnk['href'])
        curr.append(incident_th.text.strip())

        cols = row.find_all('td')
        for ele in cols:
            lnk = ele.find('a')
            if lnk:
                lnk = lnk['href']
                curr.append(lnk)
            else:
                curr.append(ele.text.strip())
        data.append(curr)


    for i in data:
        print(i)
    df = pd.DataFrame(data=data, columns=columns)
    #df.to_csv('fire_ca.csv', header=True, index=False)
    print(df.head(5))

    df.to_csv('s3://fires-ca-airflow/fire_ca.csv', header=True, index=False)
