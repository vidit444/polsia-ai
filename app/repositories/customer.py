from sqlalchemy import func, select

from app.models.customer import Customer
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository):
    async def count_by_tenant(self, tenant_id: str) -> int:
        result = await self.session.execute(select(func.count()).select_from(Customer).where(Customer.tenant_id == tenant_id))
        return int(result.scalar_one())
