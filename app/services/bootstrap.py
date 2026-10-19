from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.security import get_password_hash, normalize_email
from app.db.memory import store
from app.models.domain import AIAgent, Invoice, Tenant, User, Workflow


async def seed_demo_data() -> None:
    if await store.list("tenants"):
        return
    tenant = Tenant(id=settings.default_tenant_id, name="Polsia Demo Tenant", plan="enterprise", gstin="29ABCDE1234F1Z5")
    await store.insert("tenants", tenant)
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
    await store.insert("workflows", workflow)
    agent = AIAgent(
        tenant_id=tenant.id,
        name="Sales Copilot",
        model="router:auto",
        prompt_version="v1",
        safety_policy="strict-business",
    )
    await store.insert("ai_agents", agent)
    invoice = Invoice(
        tenant_id=tenant.id,
        amount=4999.0,
        currency="INR",
        status="pending",
        due_date=datetime.now(timezone.utc) + timedelta(days=7),
        payment_ref=None,
    )
    await store.insert("invoices", invoice)


async def create_initial_admin() -> User:
    existing = await store.get_user_by_normalized_email(normalize_email(settings.default_admin_email))
    if existing:
        return existing
    tenant = (await store.list("tenants") or [None])[0]
    if tenant is None:
        tenant = Tenant(id=settings.default_tenant_id, name="Polsia Demo Tenant", plan="enterprise")
        await store.insert("tenants", tenant)
    admin = User(
        tenant_id=tenant.id,
        role="admin",
        name="Platform Admin",
        email=settings.default_admin_email,
        normalized_email=normalize_email(settings.default_admin_email),
        phone="+919999999999",
        mfa_enabled=True,
        hashed_password=get_password_hash(settings.default_admin_password),
        password_rotation_required=True,
    )
    await store.insert("users", admin)
    return admin
