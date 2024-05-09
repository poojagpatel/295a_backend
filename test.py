# import os
# import chromadb
# from chromadb.config import Settings
# from langchain_openai import OpenAIEmbeddings
# from openai import OpenAI

# from crawlers import earthquake
# from utility import (
#     get_conversation_chain,
# )
# from langchain_chroma import Chroma
# from langchain_community.document_loaders import JSONLoader
# import pdb
# import json


# # create_store_embeddings()
# # vectordb = Chroma(
# #     embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_store"
# # )

# print(os.getenv("DB_HOST"))
# chroma_client = chromadb.HttpClient(
#     host=os.getenv("DB_HOST"),
#     port=8000,
#     settings=Settings(allow_reset=True, anonymized_telemetry=False),
# )
# vectordb = Chroma(
#     client=chroma_client,
#     collection_name="langchain",
#     embedding_function=OpenAIEmbeddings(),
# )
# op = get_conversation_chain(vectordb)


# # response = op({"question": "give me news info about earthquakes in california today "})
# # response = op({"question": "give me news info about crime "})
# response = op({"question": "give me news about environment "})
# # response = op({"question": "give me wildfire info "})
# print(response["answer"])


s = "A man, a plan, a canal: Panama"
s = s.strip()
print(s)
