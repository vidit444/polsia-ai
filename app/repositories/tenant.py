from sqlalchemy import select

from app.models.tenant import Tenant
from app.repositories.base import BaseRepository


class TenantRepository(BaseRepository):
    async def get_by_id(self, tenant_id: str) -> Tenant | None:
        result = await self.session.execute(select(Tenant).where(Tenant.id == tenant_id))
        return result.scalar_one_or_none()

    async def create(self, tenant: Tenant) -> Tenant:
        self.session.add(tenant)
        await self.session.flush()
        return tenant
