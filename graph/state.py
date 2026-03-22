from typing import TypedDict, List

class IncidentState(TypedDict):

    incident: dict

    queue_name: str

    kb_results: List

    processed: bool