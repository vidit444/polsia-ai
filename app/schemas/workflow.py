from typing import Any

from pydantic import BaseModel, Field


class WorkflowCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    type: str = Field(min_length=2, max_length=100)
    is_active: bool = True
    version: int = 1


class WorkflowRunCreate(BaseModel):
    input_json: dict[str, Any] = Field(default_factory=dict)


class WorkflowResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    type: str
    is_active: bool
    version: int

    model_config = {"from_attributes": True}


class WorkflowRunResponse(BaseModel):
    id: str
    workflow_id: str
    status: str
    input_json: dict[str, Any]
    output_json: dict[str, Any]

    model_config = {"from_attributes": True}
