import datetime
from dotenv import load_dotenv
import os
from pymongo import MongoClient

from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI


def convert_unix_milliseconds_to_datetime(milliseconds):
    return datetime.utcfromtimestamp(milliseconds / 1000.0)


def connect_to_mongodb():
    # Load environment variables from .env file
    load_dotenv()
    # MongoDB connection string
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "27017")
    db_name = os.getenv("DB_NAME", "sample_database")
    collection_name = os.getenv("COLLECTION_NAME", "earthquakes")
    print(
        "db_name: " + db_name,
        "collection_name: " + collection_name,
        "db_host: " + db_host,
        "db_port: " + (db_port),
    )

    connection_string = (
        f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        "?authSource=admin"
    )

    # Initialize MongoDB client
    client = MongoClient(connection_string)

    return client


def get_conversation_chain(_vectorstore):
    general_system_template = r""" You are an helpful, funny and clever QA agent.Use the following pieces of context and name of the context to answer the question at the end.if you dont know the answer, then say i dont know. please check online resources.The context could be unrelevant to the question, in that case do not use it. Answer the question in english language irrespective of the language of the question.
----
{context}
----
    """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(),
        retriever=_vectorstore.as_retriever(),
        chain_type="stuff",
        memory=memory,
    )
