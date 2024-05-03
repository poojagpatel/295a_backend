import os
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

from crawlers import earthquake
from utility import (
    create_record_embeddings,
    get_conversation_chain,
    get_ids_from_collection,
)
from langchain_chroma import Chroma
from langchain_community.document_loaders import JSONLoader
import pdb
import json


# create_store_embeddings()
# vectordb = Chroma(
#     embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_store"
# )

chroma_client = chromadb.HttpClient(host="13.58.222.32", port=8000)
vectordb = Chroma(
    client=chroma_client,
    embedding_function=OpenAIEmbeddings(),
)

op = vectordb.similarity_search("earthquake", 5)
print(op)
# op = get_conversation_chain(vectordb)

# response = op({"question": "give me some earthquake results from california  "})
# print(response["answer"])
