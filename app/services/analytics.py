from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.customer import CustomerRepository
from app.repositories.deal import DealRepository
from app.repositories.workflow import WorkflowRepository
from app.repositories.workflow_run import WorkflowRunRepository
from app.schemas.analytics import DashboardAnalyticsResponse


class AnalyticsService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.customer_repository = CustomerRepository(session)
        self.deal_repository = DealRepository(session)
        self.workflow_repository = WorkflowRepository(session)
        self.workflow_run_repository = WorkflowRunRepository(session)

    async def dashboard(self, tenant_id: str, actor) -> DashboardAnalyticsResponse:
        if actor.tenant_id and str(actor.tenant_id) != tenant_id and actor.role not in {"admin", "owner"}:
            raise HTTPException(status_code=403, detail="Tenant scope violation")

        customers = await self.customer_repository.count_by_tenant(tenant_id)
        deals = await self.deal_repository.count_by_tenant(tenant_id)
        workflows = await self.workflow_repository.list_by_tenant(tenant_id)
        workflow_status_counts = await self.workflow_run_repository.count_by_status([workflow.id for workflow in workflows])

        return DashboardAnalyticsResponse(
            tenant_id=tenant_id,
            customers=customers,
            deals=deals,
            workflows=len(workflows),
            workflow_runs_by_status=workflow_status_counts,
        )
