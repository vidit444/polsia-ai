from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain import Invoice, Lead, WorkflowRun
from app.schemas.auth import TokenPayload
from app.schemas.dashboard import DashboardMetricsResponse


async def get_dashboard_metrics(
    session: AsyncSession,
    context: TokenPayload,
    tenant_id: str,
) -> DashboardMetricsResponse:
    if context.tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tenant mismatch")

    leads_count = await session.scalar(select(func.count()).select_from(Lead).where(Lead.tenant_id == tenant_id))
    workflow_runs_count = await session.scalar(
        select(func.count()).select_from(WorkflowRun).where(WorkflowRun.tenant_id == tenant_id)
    )
    monthly_revenue = await session.scalar(
        select(func.coalesce(func.sum(Invoice.amount), 0)).select_from(Invoice).where(Invoice.tenant_id == tenant_id)
    )
    open_invoices = await session.scalar(
        select(func.count()).select_from(Invoice).where(Invoice.tenant_id == tenant_id, Invoice.status != "paid")
    )

    return DashboardMetricsResponse(
        tenant_id=tenant_id,
        active_leads=int(leads_count or 0),
        workflow_runs=int(workflow_runs_count or 0),
        monthly_revenue=float(monthly_revenue or Decimal("0")),
        open_invoices=int(open_invoices or 0),
        health_status="healthy",
    )
