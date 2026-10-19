from sqlalchemy import select

from app.models.workflow import Workflow
from app.repositories.base import BaseRepository


class WorkflowRepository(BaseRepository):
    async def create(self, workflow: Workflow) -> Workflow:
        self.session.add(workflow)
        await self.session.flush()
        return workflow

    async def list_by_tenant(self, tenant_id: str) -> list[Workflow]:
        result = await self.session.execute(select(Workflow).where(Workflow.tenant_id == tenant_id))
        return list(result.scalars().all())
