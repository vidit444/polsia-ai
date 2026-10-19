from pydantic import BaseModel


class KPIResponse(BaseModel):
    tenant_id: str
    total_workflows: int
    active_workflows: int
    total_runs: int
    successful_runs: int
    failed_runs: int
    open_tasks: int
