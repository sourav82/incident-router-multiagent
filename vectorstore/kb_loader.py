from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.documents import Document
import chromadb
from langchain_community.vectorstores import Chroma
from services.sqlite_client import fetch_kb_articles
from config.settings import *
import logging
import os

api_key = os.environ.get("AZURE_OPENAI_KEY")
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")

def build_vector_store():
    persist_dir = "/tmp/vectordb"

    # Rebuild every cold start
    if os.path.exists(persist_dir):
        logging.info("Vector DB directory exists, removing for rebuild.")
        import shutil
        shutil.rmtree(persist_dir)

    articles = fetch_kb_articles()
    logging.info(f"Fetched {len(articles)} articles from SQLite")

    if not articles:
        logging.warning("No KB articles found! Vector store will be empty.")

    documents = []
    for item in articles:
        text = f"Title: {item['title']}\nDescription: {item['description']}\nResolution: {item['resolution']}"
        documents.append(Document(page_content=text, metadata=item))

    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version="2024-12-01-preview",
        azure_deployment="text-embedding-3-large",
        model="text-embedding-3-large"
    )

    vector_store = Chroma(
        collection_name="incident_kb",
        embedding_function=embeddings,
        persist_directory=persist_dir
    )

    vector_store.add_documents(documents)
    logging.info(f"Loaded {len(documents)} KB articles into vector store")
    return vector_store



