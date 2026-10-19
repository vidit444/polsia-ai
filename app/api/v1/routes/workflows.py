from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_context, get_db_session
from app.schemas.auth import TokenPayload
from app.schemas.workflow import WorkflowExecuteRequest, WorkflowRunResponse
from app.services.workflow_service import execute_workflow

router = APIRouter()


@router.post("/execute", response_model=WorkflowRunResponse)
async def execute(
    payload: WorkflowExecuteRequest,
    context: TokenPayload = Depends(get_current_context),
    session: AsyncSession = Depends(get_db_session),
) -> WorkflowRunResponse:
    return await execute_workflow(session, context, payload)
