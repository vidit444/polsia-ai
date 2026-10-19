from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user, get_tenant_id
from app.db.memory import store
from app.models.domain import Workflow, WorkflowRun
from app.models.user import User
from app.schemas.workflow import WorkflowRunCreate, WorkflowRunResponse

router = APIRouter()


@router.post("/{workflow_id}/run", response_model=WorkflowRunResponse, status_code=status.HTTP_202_ACCEPTED)
async def run_workflow(
    workflow_id: str,
    payload: WorkflowRunCreate,
    current_user: User = Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
) -> WorkflowRunResponse:
    workflow = await store.get("workflows", workflow_id)
    if not workflow or workflow.tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")

    run = WorkflowRun(
        workflow_id=workflow.id,
        status="completed",
        input_json=payload.input_json,
        output_json={
            "message": "Workflow executed",
            "run_by": current_user.id,
            "tenant_id": tenant_id,
        },
    )
    await store.insert("workflow_runs", run)
    return WorkflowRunResponse.model_validate(run)
