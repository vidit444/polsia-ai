from sqlalchemy import func, select

from app.models.deal import Deal
from app.repositories.base import BaseRepository


class DealRepository(BaseRepository):
    async def count_by_tenant(self, tenant_id: str) -> int:
        result = await self.session.execute(select(func.count()).select_from(Deal).where(Deal.tenant_id == tenant_id))
        return int(result.scalar_one())
