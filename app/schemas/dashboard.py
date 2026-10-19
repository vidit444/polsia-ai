from pydantic import BaseModel


class DashboardMetricsResponse(BaseModel):
    tenant_id: str
    active_leads: int
    workflow_runs: int
    monthly_revenue: float
    open_invoices: int
    health_status: str
