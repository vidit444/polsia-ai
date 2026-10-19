from pydantic import BaseModel, Field


class WorkflowCreateRequest(BaseModel):
    tenant_id: str
    name: str = Field(min_length=2, max_length=255)
    trigger_type: str = Field(min_length=2, max_length=100)
    config_json: dict = Field(default_factory=dict)
    active: bool = True


class WorkflowResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    trigger_type: str
    config_json: dict
    active: bool
