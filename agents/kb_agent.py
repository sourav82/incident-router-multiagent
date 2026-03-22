from services.vector_store import search_similar
from vectorstore.kb_loader import build_vector_store
import logging


def kb_agent(state):

    
    description = state["incident"]["description"]

    results = search_similar(description)

    state["kb_results"] = results

    return state