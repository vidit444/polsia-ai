from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.memory import store
from app.models.domain import AIAgent, Invoice, Tenant, User, Workflow


def bootstrap_data() -> None:
    if store.list("tenants"):
        return
    tenant = Tenant(id=settings.default_tenant_id, name="Polsia Demo Tenant", plan="enterprise", gstin="29ABCDE1234F1Z5")
    store.insert("tenants", tenant)
    admin = User(
        tenant_id=tenant.id,
        role="admin",
        name="Platform Admin",
        email=settings.default_admin_email,
        phone="+919999999999",
        mfa_enabled=True,
        hashed_password=get_password_hash(settings.default_admin_password),
    )
    store.insert("users", admin)
    workflow = Workflow(
        tenant_id=tenant.id,
        name="Lead Qualification Workflow",
        trigger_type="manual",
        config_json={
            "steps": [
                {"name": "validate-input", "type": "validation"},
                {"name": "score-lead", "type": "enrichment"},
                {"name": "notify-owner", "type": "notification"},
            ]
        },
    )
    store.insert("workflows", workflow)
    agent = AIAgent(
        tenant_id=tenant.id,
        name="Sales Copilot",
        model="router:auto",
        prompt_version="v1",
        safety_policy="strict-business",
    )
    store.insert("ai_agents", agent)
    invoice = Invoice(
        tenant_id=tenant.id,
        amount=4999.0,
        currency="INR",
        status="pending",
        due_date=datetime.now(timezone.utc) + timedelta(days=7),
        payment_ref=None,
    )
    store.insert("invoices", invoice)
