from graph.incident_graph import build_graph

graph = build_graph()

print("\nAgent Workflow:\n")

graph.get_graph().print_ascii()