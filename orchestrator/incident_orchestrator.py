from agents.router_agent import is_level1_incident
from agents.classifier_agent import classify_incident
from agents.kb_agent import find_similar
from agents.troubleshoot_agent import process
from agents.notification_agent import notify
import logging

def handle_incident(incident):

    description = incident.get("description")

    if not is_level1_incident(incident):
        return

    queue_name = classify_incident(description)
    logging.info(f"Classification returned queue name {queue_name}")

    kb_results = find_similar(description)

    process(
        incident["sys_id"],
        queue_name,
        kb_results
    )

    notify(incident, kb_results)