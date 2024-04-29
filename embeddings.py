from langchain_openai import OpenAIEmbeddings

from utility import get_id_from_document
from langchain_chroma import Chroma
import chromadb
from langchain_community.document_loaders import JSONLoader


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
        persist_directory="./chroma_store",
        ids=ids,
        collection_name="earthquake",
    )
    return vectordb


def create_store_weather_embeddings(filepath):
    loader = JSONLoader(
        filepath,
        jq_schema=".features[]",
        text_content=False,
    )
    documents = loader.load()
    ids = [get_id_from_document("weather", doc) for doc in documents]
    chromadb.Client().get_or_create_collection("weather")

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(),
        persist_directory="./chroma_store",
        ids=ids,
        collection_name="weather",
    )
    return vectordb


if __name__ == "__main__":
    create_store_eq_embeddings("./crawlers/earthquake/earthquake.json")
    create_store_weather_embeddings("./crawlers/weather_gov/weather_gov.json")
