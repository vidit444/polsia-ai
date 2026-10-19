from pydantic import BaseModel


class DashboardAnalyticsResponse(BaseModel):
    tenant_id: str
    customers: int
    deals: int
    workflows: int
    workflow_runs_by_status: dict[str, int]
