from services.servicenow_client import update_incident
import logging 

GROUP_MAPPING = {
    "Network-L2": "a13551cd53737210ba58d301a0490efb",
    "MBS-L2": "84555dcd53737210ba58d301a0490ef8",
    "IBS-L2": "c0855dcd53737210ba58d301a0490e50",
    "Algo-L2": "29a5510153b37210ba58d301a0490eb9"
}

def troubleshoot_agent(state):

    sys_id = state["incident"]["sys_id"]
    logging.info(f"Sys ID: {sys_id}")

    queue_name = state["queue_name"]
    logging.info(f"Queue Name: {queue_name}")
    queue_name = queue_name.strip()
    logging.info(f"Queue Name: {queue_name}")
    for key in GROUP_MAPPING:
        if key in queue_name:
            queue_name = key
            break

    queue_sys_id = GROUP_MAPPING.get(queue_name)
    logging.info(f"Queue Sys Id : {queue_sys_id}")

    comment = "AI Found Similar Incidents:\n"

    for doc in state["kb_results"]:
        comment += f"- {doc.page_content}\n"

    update_incident(
        sys_id,
        assignment_group=queue_sys_id,
        comment=comment,
        state="2"
    )

    return state