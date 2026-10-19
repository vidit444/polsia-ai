from fastapi import APIRouter, Depends, Request, status

from app.api.deps import get_current_user, get_tenant_id
from app.models.domain import Customer, Lead, User
from app.schemas.leads import LeadCreateRequest, LeadResponse
from app.services.audit import record_audit_log
from app.services.scoring import calculate_lead_score
from app.db.memory import store

router = APIRouter()


@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(payload: LeadCreateRequest, request: Request, current_user: User = Depends(get_current_user), tenant_id: str = Depends(get_tenant_id)):
    customer = Customer(
        tenant_id=tenant_id,
        name=payload.customer_name,
        industry=payload.industry,
        source=payload.source,
        lifecycle_stage=payload.lifecycle_stage,
    )
    store.insert("customers", customer)
    computed_score = max(payload.score, calculate_lead_score(payload.customer_name, payload.industry, payload.source))
    lead = Lead(
        tenant_id=tenant_id,
        customer_id=customer.id,
        owner_id=current_user.id,
        status=payload.status,
        score=computed_score,
        next_action_at=payload.next_action_at,
    )
    store.insert("leads", lead)
    record_audit_log(tenant_id, current_user.id, "lead.create", "lead", lead.id, request.client.host if request.client else None)
    return LeadResponse(lead=lead.model_dump(mode="json"), customer=customer.model_dump(mode="json"))
