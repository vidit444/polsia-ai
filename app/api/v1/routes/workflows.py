from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.schemas.workflow import WorkflowCreateRequest, WorkflowResponse
from app.services.workflow import WorkflowService

router = APIRouter()


@router.post("", response_model=WorkflowResponse)
async def create_workflow(
    payload: WorkflowCreateRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> WorkflowResponse:
    return await WorkflowService(session).create_workflow(payload, current_user)
