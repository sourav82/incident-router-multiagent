import azure.functions as func
import logging
import sys
import os

# Make sure your project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logging.info("Module incident_router loaded")


from graph.incident_graph import build_graph


# Build the LangGraph workflow once at cold start
graph = build_graph()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Incident AI workflow started")

    try:
        # Parse JSON payload
        body = req.get_json()
        logging.info(f"Payload received: {body}")

        state = {
            "incident": body,
            "queue_name": "",
            "kb_results": [],
            "processed": False
        }

        # Invoke the multi-agent workflow
        graph.invoke(state)

        logging.info(f"Workflow finished for incident: {body.get('number', 'N/A')}")
        return func.HttpResponse("Incident processed successfully", status_code=200)

    except Exception as e:
        logging.error(f"Exception during workflow execution: {e}", exc_info=True)
        return func.HttpResponse(f"Workflow failed: {str(e)}", status_code=500)