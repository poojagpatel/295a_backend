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


# response = op({"question": "give me some earthquake results from california  "})
# # response = op({"question": "give me wildfire info "})
# print(response["answer"])


def decode_message(file_path):
    dt = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.split()
            if len(parts) == 2:
                number, word = parts
                if number.isdigit():
                    dt[int(number)] = word

    decoded_msg = []
    num = 1
    while num in dt:
        decoded_msg.append(dt[num])
        num += 1

    return "".join(decoded_msg)


if __name__ == "__main__":
    print(decode_message("coding_qual_input.txt"))
