from sqlalchemy import func, select

from app.models.workflow_run import WorkflowRun
from app.repositories.base import BaseRepository


class WorkflowRunRepository(BaseRepository):
    async def count_by_status(self, tenant_workflow_ids: list) -> dict[str, int]:
        if not tenant_workflow_ids:
            return {}
        result = await self.session.execute(
            select(WorkflowRun.status, func.count())
            .where(WorkflowRun.workflow_id.in_(tenant_workflow_ids))
            .group_by(WorkflowRun.status)
        )
        return {row[0]: int(row[1]) for row in result.all()}
