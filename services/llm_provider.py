from langchain_openai import AzureChatOpenAI
from config.settings import *
import os



def get_llm():
    api_key = os.environ.get("AZURE_OPENAI_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT")
    
    llm = AzureChatOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        deployment_name=deployment_name,
        api_version="2024-02-15-preview",
        temperature=0
    )

    return llm