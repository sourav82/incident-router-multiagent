from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from config.settings import *
import os
import logging

from vectorstore import vector_store


api_key = os.environ.get("AZURE_OPENAI_KEY")
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-12-01-preview",
    azure_deployment="text-embedding-3-large",
    model="text-embedding-3-large"
)

# vector_store = Chroma(
#     collection_name="incident_kb",
#     embedding_function=embeddings,
#     persist_directory="/tmp/vectordb"
# )

def search_similar(description):

    logging.info(f"Vector store document count: {len(vector_store.get(include=['documents'])['documents'])}")

    # Print number of documents in the collection
    all_docs = vector_store.get(include=["metadatas", "documents"])
    num_docs = len(all_docs["documents"])
    logging.info(f"Number of documents in vector store: {num_docs}")

    logging.info(f"Persist directory exists: {os.path.exists('/tmp/vectordb')}")
    logging.info(f"Contents of /tmp/vectordb: {os.listdir('/tmp/vectordb')}")

    results = vector_store.similarity_search(
        description,
        k=5
    )
    logging.info(f"Found {len(results)} results")

    return results