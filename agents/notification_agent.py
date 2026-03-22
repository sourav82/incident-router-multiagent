from services.email_service import send_email

def notification_agent(state):

    incident = state["incident"]

    body = f"Incident {incident['number']} processed\n"

    for doc in state["kb_results"]:
        body += f"{doc.page_content}\n"

    send_email(body)

    return state