from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.models.tenant import Tenant
from app.repositories.tenant import TenantRepository
from app.schemas.tenant import TenantOnboardRequest, TenantResponse


class TenantService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = TenantRepository(session)

    async def onboard(self, tenant_id: str, payload: TenantOnboardRequest, actor) -> TenantResponse:
        tenant = await self.repository.get_by_id(tenant_id)
        if tenant is not None:
            raise HTTPException(status_code=409, detail="Tenant already exists")

        tenant = Tenant(id=tenant_id, name=payload.name, plan=payload.plan, status=payload.status)
        await self.repository.create(tenant)
        self.session.add(
            AuditLog(
                tenant_id=tenant.id,
                actor_user_id=actor.id,
                action="tenant.onboard",
                entity="tenant",
                metadata_json={"plan": payload.plan, "status": payload.status},
            )
        )
        await self.session.commit()
        return TenantResponse(id=str(tenant.id), name=tenant.name, plan=tenant.plan, status=tenant.status)
