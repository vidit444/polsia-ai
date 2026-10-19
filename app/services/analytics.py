from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.workflow import Workflow
from app.models.workflow_run import WorkflowRun


class AnalyticsService:
    def get_kpis(self, db: Session, tenant_id: str) -> dict:
        total_workflows = db.execute(select(func.count(Workflow.id)).where(Workflow.tenant_id == tenant_id)).scalar_one()
        active_workflows = db.execute(select(func.count(Workflow.id)).where(Workflow.tenant_id == tenant_id, Workflow.is_active.is_(True))).scalar_one()
        workflow_ids_subquery = select(Workflow.id).where(Workflow.tenant_id == tenant_id)
        total_runs = db.execute(select(func.count(WorkflowRun.id)).where(WorkflowRun.workflow_id.in_(workflow_ids_subquery))).scalar_one()
        successful_runs = db.execute(select(func.count(WorkflowRun.id)).where(WorkflowRun.workflow_id.in_(workflow_ids_subquery), WorkflowRun.status == "success")).scalar_one()
        failed_runs = db.execute(select(func.count(WorkflowRun.id)).where(WorkflowRun.workflow_id.in_(workflow_ids_subquery), WorkflowRun.status == "failed")).scalar_one()
        open_tasks = db.execute(select(func.count(Task.id)).where(Task.tenant_id == tenant_id, Task.status != "completed")).scalar_one()
        return {
            "tenant_id": tenant_id,
            "total_workflows": total_workflows,
            "active_workflows": active_workflows,
            "total_runs": total_runs,
            "successful_runs": successful_runs,
            "failed_runs": failed_runs,
            "open_tasks": open_tasks,
        }
