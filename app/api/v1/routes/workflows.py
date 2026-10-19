from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.deps import get_current_user, get_tenant_id
from app.db.memory import store
from app.models.domain import User, WorkflowRun
from app.schemas.workflows import WorkflowRunRequest, WorkflowRunResponse
from app.services.audit import record_audit_log
from app.services.workflow_engine import execute_workflow

router = APIRouter()


@router.post("/{workflow_id}/run", response_model=WorkflowRunResponse)
def run_workflow(workflow_id: str, payload: WorkflowRunRequest, request: Request, current_user: User = Depends(get_current_user), tenant_id: str = Depends(get_tenant_id)):
    workflow = store.get("workflows", workflow_id)
    if not workflow or workflow.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Workflow not found")
    result = execute_workflow(workflow, payload.input)
    run = WorkflowRun(workflow_id=workflow.id, status="completed", input_json=payload.input, output_json=result)
    store.insert("workflow_runs", run)
    record_audit_log(tenant_id, current_user.id, "workflow.run", "workflow", workflow.id, request.client.host if request.client else None)
    return WorkflowRunResponse(run=run.model_dump(mode="json"))
