import requests
from config.settings import *
import logging
import random

SERVICENOW_URL=os.environ.get("SERVICENOW_URL")
SERVICENOW_USER=os.environ.get("SERVICENOW_USER")
SERVICENOW_PASSWORD=os.environ.get("SERVICENOW_PASSWORD")

def get_group_members(group_sys_id):
    url = f"{SERVICENOW_URL}/api/now/table/sys_user_grmember"
    params = {
        "sysparm_query": f"group={group_sys_id}",
        "sysparm_fields": "user"
    }        
    r = requests.get(url, auth=(SERVICENOW_USER, SERVICENOW_PASSWORD), params=params)
    if r.status_code != 200:
        logging.error(f"Failed to fetch group members: {r.status_code} {r.text}")
        return []
    members = []
    for item in r.json().get("result", []):
        user_field = item.get("user")
        if isinstance(user_field, dict) and "value" in user_field:
            members.append(user_field["value"])
    logging.info(f"Found {len(members)} members in group {group_sys_id}")
    return members


def update_incident(sys_id, assignment_group=None, comment=None, state=None):

    # Fetch team members
    members = get_group_members(assignment_group)
    if not members:
        logging.warning(f"No members found in group {assignment_group}. Assigning to None.")
        assigned_to = None
    else:
        assigned_to = random.choice(members)

    assigned_to = random.choice(members) if members else None

    url = f"{SERVICENOW_URL}/api/now/table/incident/{sys_id}"
    logging.info(f"URL : {url}")

    payload = {}

    if assignment_group:
        payload["assignment_group"] = assignment_group

    if assigned_to:
        payload["assigned_to"] = assigned_to

    if comment:
        payload["comments"] = comment

    if state:
        payload["state"] = state

    response = requests.patch(
        url,
        auth=(SERVICENOW_USER, SERVICENOW_PASSWORD),
        json=payload
    )

    return response.json()