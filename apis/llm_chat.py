from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import json

# configure the enviroment with open ai api key
load_dotenv()

# function to retrieve answer to user query based on incident dat
def get_response(query, incident_data):

    # build template for the prompt
    template = '''You are a helpful assistant. Answer the user questions considering only the Incident Data provided.
    Incident Data: {incident_data}
    User question: {user_question}'''

    # create prompt, initialize llm and chain
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()

    # invoke the chain and return the response of the user query
    return chain.invoke(
        {
        "incident_data": incident_data,
        "user_question": query
        }
    )

data = """{
  "_id": "nc74013551",
  "geometry": {
    "coordinates": [
      -122.7259979,
      38.7803345,
      1.05
    ],
    "type": "Point"
  },
  "properties": {
    "alert": null,
    "cdi": null,
    "code": "74013551",
    "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=nc74013551&format=geojson",
    "dmin": 0.008871,
    "felt": null,
    "gap": 47,
    "ids": ",nc74013551,",
    "mag": 2.21,
    "magType": "md",
    "mmi": null,
    "net": "nc",
    "nst": 48,
    "place": "3 km E of The Geysers, CA",
    "rms": 0.08,
    "sig": 75,
    "sources": ",nc,",
    "status": "automatic",
    "time": "2024-03-07 22:37:00.480000",
    "title": "M 2.2 - 3 km E of The Geysers, CA",
    "tsunami": 0,
    "type": "earthquake",
    "types": ",focal-mechanism,nearby-cities,origin,phase-data,scitech-link,",
    "tz": null,
    "updated": 1709880023997,
    "url": "https://earthquake.usgs.gov/earthquakes/eventpage/nc74013551"
  },
  "type": "Feature"
}"""

json_data = json.loads(data)
query = 'can you give me a brief summary about this incident?'
response = get_response(query, data)
print(response)