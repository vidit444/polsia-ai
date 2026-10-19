from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.workflow import WorkflowCreate, WorkflowResponse, WorkflowRunCreate, WorkflowRunResponse
from app.services.workflow import WorkflowService

router = APIRouter(prefix="/tenants/{tenant_id}/workflows")
service = WorkflowService()


@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(tenant_id: str, payload: WorkflowCreate, db=Depends(get_db), user: dict = Depends(get_current_user)) -> WorkflowResponse:
    if user.get("tenant_id") != tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tenant access denied")
    workflow = service.create_workflow(db, tenant_id, payload)
    return WorkflowResponse.model_validate(workflow)


@router.post("/{workflow_id}/run", response_model=WorkflowRunResponse, status_code=status.HTTP_201_CREATED)
async def run_workflow(tenant_id: str, workflow_id: str, payload: WorkflowRunCreate, db=Depends(get_db), user: dict = Depends(get_current_user)) -> WorkflowRunResponse:
    if user.get("tenant_id") != tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tenant access denied")
    try:
        workflow_run = service.run_workflow(db, workflow_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return WorkflowRunResponse.model_validate(workflow_run)
