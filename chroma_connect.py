import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader


from utility import get_conversation_chain, get_id_from_document


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
    print("data inserted")
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
    print("data inserted")
    return vectordb


if __name__ == "__main__":
    # create_store_eq1_embeddings()
    chroma_client = chromadb.HttpClient(host="13.58.222.32", port=8000)
    # create_store_eq1_embeddings()
    # create_store_we_embeddings()

    db4 = Chroma(
        client=chroma_client,
        collection_name="langchain",
        embedding_function=OpenAIEmbeddings(),
    )

    op = get_conversation_chain(db4)
    response = op({"question": "give me some earthquake results from california  "})
    print(response["answer"])
