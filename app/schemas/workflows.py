from typing import Any

from pydantic import BaseModel, Field


class WorkflowRunRequest(BaseModel):
    input: dict[str, Any] = Field(default_factory=dict)
    mode: str = "sync"


class WorkflowRunResponse(BaseModel):
    run: dict
