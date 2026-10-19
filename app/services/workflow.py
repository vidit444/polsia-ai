from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.workflow import Workflow
from app.models.workflow_run import WorkflowRun
from app.schemas.workflow import WorkflowCreate, WorkflowRunCreate


class WorkflowService:
    def create_workflow(self, db: Session, tenant_id: str, payload: WorkflowCreate) -> Workflow:
        workflow = Workflow(
            tenant_id=tenant_id,
            name=payload.name,
            type=payload.type,
            is_active=payload.is_active,
            version=payload.version,
        )
        db.add(workflow)
        db.commit()
        db.refresh(workflow)
        return workflow

    def run_workflow(self, db: Session, workflow_id: str, payload: WorkflowRunCreate) -> WorkflowRun:
        workflow = db.get(Workflow, workflow_id)
        if not workflow:
            raise ValueError("Workflow not found")

        run_count = db.execute(select(func.count(WorkflowRun.id)).where(WorkflowRun.workflow_id == workflow_id)).scalar_one()
        workflow_run = WorkflowRun(
            workflow_id=workflow_id,
            status="success",
            input_json=payload.input_json,
            output_json={"message": "Workflow executed", "run_sequence": run_count + 1},
        )
        db.add(workflow_run)
        db.commit()
        db.refresh(workflow_run)
        return workflow_run
