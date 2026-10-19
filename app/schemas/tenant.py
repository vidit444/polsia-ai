from datetime import datetime

from pydantic import BaseModel, EmailStr


class TenantOnboardRequest(BaseModel):
    company_name: str
    owner_name: str
    owner_email: EmailStr
    plan: str
    billing_cycle: str


class TenantResponse(BaseModel):
    tenant_id: str
    name: str
    tier: str
    status: str
    owner_email: EmailStr
    created_at: datetime
