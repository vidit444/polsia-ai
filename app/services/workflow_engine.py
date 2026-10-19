from typing import Any


def execute_workflow(workflow, payload: dict[str, Any]) -> dict[str, Any]:
    steps = workflow.config_json.get("steps", [])
    trace = []
    enriched = dict(payload)
    for index, step in enumerate(steps, start=1):
        trace.append({"step": index, "name": step["name"], "type": step["type"], "status": "completed"})
        if step["type"] == "enrichment":
            enriched["score"] = min(100, int(enriched.get("score", 0)) + 15)
        elif step["type"] == "notification":
            enriched["notification"] = "owner_notified"
    return {"trace": trace, "result": enriched, "workflow": workflow.name}
