def router_agent(state):

    incident = state["incident"]

    assignment_group = incident.get("assignment_group")

    if assignment_group is None or assignment_group == "Level-1":
        return state

    state["processed"] = True
    return state