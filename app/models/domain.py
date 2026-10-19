from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:16]}"


class Tenant(BaseModel):
    id: str = Field(default_factory=lambda: new_id("tenant"))
    name: str
    plan: str = "growth"
    status: str = "active"
    gstin: str | None = None
    created_at: datetime = Field(default_factory=utcnow)


class User(BaseModel):
    id: str = Field(default_factory=lambda: new_id("user"))
    tenant_id: str
    role: str
    name: str
    email: EmailStr
    phone: str | None = None
    mfa_enabled: bool = False
    hashed_password: str
    created_at: datetime = Field(default_factory=utcnow)


class Customer(BaseModel):
    id: str = Field(default_factory=lambda: new_id("cust"))
    tenant_id: str
    name: str
    industry: str | None = None
    source: str | None = None
    lifecycle_stage: str = "lead"


class Lead(BaseModel):
    id: str = Field(default_factory=lambda: new_id("lead"))
    tenant_id: str
    customer_id: str
    owner_id: str
    status: str = "new"
    score: int = 0
    next_action_at: datetime | None = None
    created_at: datetime = Field(default_factory=utcnow)


class Workflow(BaseModel):
    id: str = Field(default_factory=lambda: new_id("wf"))
    tenant_id: str
    name: str
    trigger_type: str
    config_json: dict[str, Any]
    enabled: bool = True


class WorkflowRun(BaseModel):
    id: str = Field(default_factory=lambda: new_id("wfr"))
    workflow_id: str
    status: str
    input_json: dict[str, Any]
    output_json: dict[str, Any]
    started_at: datetime = Field(default_factory=utcnow)


class AIAgent(BaseModel):
    id: str = Field(default_factory=lambda: new_id("agent"))
    tenant_id: str
    name: str
    model: str
    prompt_version: str
    safety_policy: str


class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: new_id("conv"))
    tenant_id: str
    channel: str
    external_ref: str | None = None
    status: str = "active"


class Message(BaseModel):
    id: str = Field(default_factory=lambda: new_id("msg"))
    conversation_id: str
    sender_type: str
    content: str
    tokens: int = 0
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class Invoice(BaseModel):
    id: str = Field(default_factory=lambda: new_id("inv"))
    tenant_id: str
    amount: float
    currency: str = "INR"
    status: str = "pending"
    due_date: datetime | None = None
    payment_ref: str | None = None


class Payment(BaseModel):
    id: str = Field(default_factory=lambda: new_id("pay"))
    invoice_id: str
    provider: str
    amount: float
    status: str
    upi_ref: str | None = None


class AuditLog(BaseModel):
    id: str = Field(default_factory=lambda: new_id("audit"))
    tenant_id: str
    actor_id: str | None = None
    action: str
    entity_type: str
    entity_id: str
    ip: str | None = None
    created_at: datetime = Field(default_factory=utcnow)
