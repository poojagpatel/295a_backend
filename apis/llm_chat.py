from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import json


from flask import Flask, jsonify
from flask_cors import CORS
from flask import request

# Initialize flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  


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


@app.route("/api/chat", methods=["POST"])
def get_chat_response():
    """
    Retrieves paginated weather data from the 'weather_misc' collection in the database.
    ---
    parameters:
        - in: body
          incident: json
          query: string
    responses:
        200:
            description: Response to the user query from OpenAI LLM
        500:
            description: If an exception occurs while retrieving the result.
    """
    try:
        data = request.json
        incident_data = data['incident']
        query = data['query']

        chat_result = get_response(query, incident_data)
        response = {
          'result': chat_result
        }

        return jsonify(response), 200

    except Exception as e:
          # Handle exceptions and return an appropriate error response
          return jsonify({"error": str(e)}), 500  # HTTP 500 for internal server error
      
if __name__ == "__main__":
    app.run(debug=True)
