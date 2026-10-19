from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain import AuditLog, Event, Workflow, WorkflowRun
from app.schemas.auth import TokenPayload
from app.schemas.workflow import WorkflowExecuteRequest, WorkflowRunResponse


async def execute_workflow(
    session: AsyncSession,
    context: TokenPayload,
    payload: WorkflowExecuteRequest,
) -> WorkflowRunResponse:
    result = await session.execute(
        select(Workflow).where(Workflow.tenant_id == context.tenant_id, Workflow.name == payload.workflow_name)
    )
    workflow = result.scalar_one_or_none()
    if workflow is None:
        workflow = Workflow(
            tenant_id=context.tenant_id,
            name=payload.workflow_name,
            type=payload.workflow_type,
            status="active",
            config_json={"created_by": context.user_id},
        )
        session.add(workflow)
        await session.flush()

    started_at = datetime.now(UTC)
    output = {
        "echo": payload.payload,
        "workflow": payload.workflow_name,
        "processed_by": "rule-engine-v1",
        "fallback_used": False,
    }
    duration_ms = max(int((datetime.now(UTC) - started_at).total_seconds() * 1000), 1)

    run = WorkflowRun(
        workflow_id=workflow.id,
        tenant_id=context.tenant_id,
        input_json=payload.model_dump(),
        output_json=output,
        status="completed",
        duration_ms=duration_ms,
    )
    audit = AuditLog(
        tenant_id=context.tenant_id,
        actor_user_id=context.user_id,
        action="workflow.execute",
        entity_type="workflow",
        entity_id=str(workflow.id),
    )
    event = Event(
        tenant_id=context.tenant_id,
        type="workflow.completed",
        payload_json={"workflow_id": str(workflow.id), "run_status": "completed"},
        processed_at=datetime.now(UTC),
        status="processed",
    )
    session.add_all([run, audit, event])
    await session.commit()
    await session.refresh(run)

    return WorkflowRunResponse(
        workflow_run_id=str(run.id),
        workflow_id=str(workflow.id),
        status=run.status,
        duration_ms=run.duration_ms,
        output=run.output_json,
    )
