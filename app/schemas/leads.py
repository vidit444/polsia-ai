from datetime import datetime

from pydantic import BaseModel, Field


class LeadCreateRequest(BaseModel):
    customer_name: str = Field(min_length=2, max_length=120)
    industry: str | None = None
    source: str | None = None
    lifecycle_stage: str = "lead"
    status: str = "new"
    score: int = Field(default=0, ge=0, le=100)
    next_action_at: datetime | None = None


class LeadResponse(BaseModel):
    lead: dict
    customer: dict
