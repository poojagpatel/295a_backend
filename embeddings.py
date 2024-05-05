from langchain_openai import OpenAIEmbeddings

from utility import get_id_from_document
from langchain_chroma import Chroma
import chromadb
from langchain_community.document_loaders import JSONLoader
import os


def create_store_eq1_embeddings():
    loader = JSONLoader(
        "./crawlers/earthquake/earthquake.json",
        jq_schema=".features[]",
        text_content=False,
    )
    documents = loader.load()
    ids = [get_id_from_document("earthquake", doc) for doc in documents]

    vectordb = Chroma.from_documents(
        client=chroma_client,
        documents=documents,
        embedding=OpenAIEmbeddings(),
        ids=ids,
    )
    print("\n\n earthquake embeddings data inserted", len(documents))
    return vectordb


def create_store_we_embeddings():
    loader = JSONLoader(
        "./crawlers/weather_gov/weather_gov.json",
        jq_schema=".features[]",
        text_content=False,
    )
    documents = loader.load()
    ids = [get_id_from_document("weather", doc) for doc in documents]

    vectordb = Chroma.from_documents(
        client=chroma_client,
        documents=documents,
        embedding=OpenAIEmbeddings(),
        ids=ids,
    )
    print("\n\nweather embeddings data inserted", len(documents))
    return vectordb


def create_store_wf_embeddings():
    loader = JSONLoader(
        "./crawlers/wildfire/fires_ca.json",
        jq_schema=".features[]",
        text_content=False,
    )
    documents = loader.load()
    ids = [get_id_from_document("wildfire", doc) for doc in documents]

    vectordb = Chroma.from_documents(
        client=chroma_client,
        documents=documents,
        embedding=OpenAIEmbeddings(),
        ids=ids,
    )
    print("n\n wildfire embeddings data inserted", len(documents))
    return vectordb


if __name__ == "__main__":
    chroma_client = chromadb.HttpClient(host=os.getenv("DB_HOST"), port=8000)
    create_store_eq1_embeddings()
    print("created earthquake embeddings")
    # create_store_we_embeddings()
    # print("created weather embeddings")
    create_store_wf_embeddings()
    print("created wildfire embeddings")
