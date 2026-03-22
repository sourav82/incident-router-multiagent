from langgraph.graph import StateGraph, END

from graph.state import IncidentState

from agents.router_agent import router_agent
from agents.classifier_agent import classifier_agent
from agents.kb_agent import kb_agent
from agents.troubleshoot_agent import troubleshoot_agent
from agents.notification_agent import notification_agent


def build_graph():

    workflow = StateGraph(IncidentState)

    workflow.add_node("router", router_agent)

    workflow.add_node("classifier", classifier_agent)

    workflow.add_node("kb_search", kb_agent)

    workflow.add_node("troubleshoot", troubleshoot_agent)

    workflow.add_node("notify", notification_agent)

    workflow.set_entry_point("router")

    workflow.add_edge("router", "classifier")

    workflow.add_edge("classifier", "kb_search")

    workflow.add_edge("kb_search", "troubleshoot")

    workflow.add_edge("troubleshoot", "notify")

    workflow.add_edge("notify", END)

    return workflow.compile()