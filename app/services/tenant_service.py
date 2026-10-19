from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.models.domain import Invoice, Subscription, Tenant, User
from app.schemas.tenant import TenantOnboardRequest, TenantResponse

settings = get_settings()


async def onboard_tenant(session: AsyncSession, payload: TenantOnboardRequest) -> TenantResponse:
    tenant = Tenant(name=payload.company_name, tier=payload.plan, status="active")
    session.add(tenant)
    await session.flush()

    owner = User(
        tenant_id=tenant.id,
        name=payload.owner_name,
        email=payload.owner_email,
        role="owner",
        status="active",
        password_hash=get_password_hash(settings.admin_password),
    )
    session.add(owner)
    await session.flush()

    tenant.owner_user_id = owner.id

    subscription = Subscription(
        tenant_id=tenant.id,
        plan=payload.plan,
        mrr=Decimal("9999.00"),
        billing_cycle=payload.billing_cycle,
        status="active",
    )
    invoice = Invoice(
        tenant_id=tenant.id,
        amount=Decimal("9999.00"),
        currency="INR",
        status="pending",
        upi_qr_url=settings.default_upi_qr_url,
    )
    session.add_all([subscription, invoice])
    await session.commit()
    await session.refresh(tenant)

    return TenantResponse(
        tenant_id=str(tenant.id),
        name=tenant.name,
        tier=tenant.tier,
        status=tenant.status,
        owner_email=owner.email,
        created_at=tenant.created_at,
    )
