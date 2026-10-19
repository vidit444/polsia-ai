from typing import Any

from pydantic import BaseModel, Field


class WorkflowExecuteRequest(BaseModel):
    workflow_name: str
    workflow_type: str
    payload: dict[str, Any] = Field(default_factory=dict)


class WorkflowRunResponse(BaseModel):
    workflow_run_id: str
    workflow_id: str
    status: str
    duration_ms: int
    output: dict[str, Any]
