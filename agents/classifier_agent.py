from services.llm_provider import get_llm

llm = get_llm()

def classifier_agent(state):

    description = state["incident"]["description"]

    prompt = f"""
Classify the IT incident.

Incident:
{description}

Return one of:
Network-L2 - This is related to any network connectivity issues, like connecting to Internet, on-premise to Cloud etc.
MBS-L2 - MBS is Major Business Services which includes application like EAP, Intellipay, Cloudapp, MajorTrails, Mobility. Any issues, other than connectivity, in these applications will be assigned to MBS-L2
IBS-L2 - IBS stands for Important Business Services which includes application like ALPS, DAST, SASM, APPIM. Any issues with these applications, other than network connectivity, will be assigned to this queue IBS-L2
Algo-L2 - This queue delas with any application issues other than network connectivity for Algo applications.
"""

    response = llm.invoke(prompt)

    state["queue_name"] = response.content.strip()

    return state