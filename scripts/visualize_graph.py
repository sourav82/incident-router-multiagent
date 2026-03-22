from graph.incident_graph import build_graph

graph = build_graph()

print("\nAgent Workflow:\n")

print(graph.get_graph().draw_mermaid())