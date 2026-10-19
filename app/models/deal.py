import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDTimestampMixin


class Deal(UUIDTimestampMixin, Base):
    __tablename__ = "deals"

    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    owner_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    value: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    stage: Mapped[str] = mapped_column(String(100), nullable=False)
    close_date: Mapped[date | None] = mapped_column(Date, nullable=True)
