from services.email_service import send_email

def notification_agent(state):

    incident = state["incident"]

    body = f"Incident {incident['number']} processed\n"

    for doc in state["kb_results"]:
        body += f"{doc.page_content}\n"

    #### Presently this is printing the KB articles which has matched the incident description
    #### We can alter this logic to send email only if nothing matched to identify the uniqueness of this issue.
    #### We need to write HTML and use SMTP server here to actually send the email to the recipients.
    if (len(state["kb_results"]) == 0):
      send_email(body)

    return state