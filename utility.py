import datetime
import chromadb
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pymongo import MongoClient
from openai import OpenAI

load_dotenv()
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from langchain_community.document_loaders import JSONLoader
import pdb
import json


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


def get_ids_from_collection(collection_name):
    client = connect_to_mongodb()
    db = client["ENDDB"]
    collection = db[collection_name]
    ids = [doc["_id"] for doc in collection.find({}, {"_id": 1})]
    return ids


def get_conversation_chain(_vectorstore):
    general_system_template = r""" You are an helpful, funny and clever QA agent.Use the following pieces of context and name of the context to answer the question at the end.if you dont know the answer, then say i dont know. please check online resources.The context could be unrelevant to the question, in that case do not use it. Answer the question in english language irrespective of the language of the question.
----
{context}
----
    """
    general_user_template = "Question:```{question}```"
    messages = [
        SystemMessagePromptTemplate.from_template(general_system_template),
        HumanMessagePromptTemplate.from_template(general_user_template),
    ]
    qa_prompt = ChatPromptTemplate.from_messages(messages)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(),
        retriever=_vectorstore.as_retriever(),
        chain_type="stuff",
        memory=memory,
    )


def get_id_from_document(doc_type, document):
    page_content = json.loads(document.page_content)
    if doc_type == "earthquake":
        return page_content.get("id", None)
    elif doc_type == "weather":
        return page_content.get("properties").get("id", None)
    elif doc_type == "wildfire":
        return page_content.get("properties").get("UniqueId", None)
    else:
        return None


def create_store_eq_embeddings(filepath):
    loader = JSONLoader(
        filepath,
        jq_schema=".features[]",
        text_content=False,
    )
    documents = loader.load()
    ids = [get_id_from_document("earthquake", doc) for doc in documents]
    chromadb.Client().get_or_create_collection("earthquake")

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(),
        persist_directory="../295a_backend-feature_sw/chroma_store",
        ids=ids,
        collection_name="earthquake",
    )
    return vectordb


def create_store_embeddings():
    eq_loader = JSONLoader(
        "./crawlers/earthquake/earthquake.json",
        jq_schema=".features[]",
        text_content=False,
    )
    weather_loader = JSONLoader(
        "./crawlers/weather_gov/weather_gov.json",
        jq_schema=".features[]",
        text_content=False,
    )
    eq_documents = eq_loader.load()
    weather_documents = weather_loader.load()

    eq_ids = [get_id_from_document("earthquake", doc) for doc in eq_documents]
    weather_ids = [get_id_from_document("weather", doc) for doc in weather_documents]

    # todo at a time dono se me ek hi collection me store karna hai..else we will face rate limiting issue
    vectordb = Chroma.from_documents(
        documents=weather_documents,
        embedding=OpenAIEmbeddings(),
        persist_directory="./chroma_store",
        ids=weather_ids,
    )

    return vectordb
