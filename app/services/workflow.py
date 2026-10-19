from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.models.workflow import Workflow
from app.repositories.tenant import TenantRepository
from app.repositories.workflow import WorkflowRepository
from app.schemas.workflow import WorkflowCreateRequest, WorkflowResponse


class WorkflowService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.workflow_repository = WorkflowRepository(session)
        self.tenant_repository = TenantRepository(session)

    async def create_workflow(self, payload: WorkflowCreateRequest, actor) -> WorkflowResponse:
        tenant = await self.tenant_repository.get_by_id(payload.tenant_id)
        if tenant is None:
            raise HTTPException(status_code=404, detail="Tenant not found")
        if str(actor.tenant_id) != payload.tenant_id and actor.role not in {"admin", "owner"}:
            raise HTTPException(status_code=403, detail="Tenant scope violation")

        workflow = Workflow(
            tenant_id=payload.tenant_id,
            name=payload.name,
            trigger_type=payload.trigger_type,
            config_json=payload.config_json,
            active=payload.active,
        )
        await self.workflow_repository.create(workflow)
        self.session.add(
            AuditLog(
                tenant_id=workflow.tenant_id,
                actor_user_id=actor.id,
                action="workflow.create",
                entity="workflow",
                metadata_json={"trigger_type": workflow.trigger_type, "active": workflow.active},
            )
        )
        await self.session.commit()
        return WorkflowResponse(
            id=str(workflow.id),
            tenant_id=str(workflow.tenant_id),
            name=workflow.name,
            trigger_type=workflow.trigger_type,
            config_json=workflow.config_json,
            active=workflow.active,
        )
