from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import JSON, Boolean, DateTime, Float, Integer, String

from app.core.config import settings
from app.models.domain import (
    AuditLog,
    Conversation,
    Customer,
    Invoice,
    Lead,
    Message,
    Payment,
    Tenant,
    User,
    Workflow,
    WorkflowRun,
)


class Base(DeclarativeBase):
    pass


class TenantRecord(Base):
    __tablename__ = "tenants"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)


class UserRecord(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String, index=True)
    normalized_email: Mapped[str] = mapped_column(String, unique=True, index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)


class GenericTenantRecord(Base):
    __tablename__ = "generic_tenant_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    table_name: Mapped[str] = mapped_column(String, index=True)
    entity_id: Mapped[str] = mapped_column(String, index=True)
    tenant_id: Mapped[str] = mapped_column(String, index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)


class GenericGlobalRecord(Base):
    __tablename__ = "generic_global_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    table_name: Mapped[str] = mapped_column(String, index=True)
    entity_id: Mapped[str] = mapped_column(String, index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)


class AuthStateRecord(Base):
    __tablename__ = "auth_state"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[str | None] = mapped_column(String, nullable=True)
    last_ip: Mapped[str | None] = mapped_column(String, nullable=True)


class RateLimitRecord(Base):
    __tablename__ = "rate_limits"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    window_started_at: Mapped[float] = mapped_column(Float)
    count: Mapped[int] = mapped_column(Integer, default=0)


class IdempotencyRecord(Base):
    __tablename__ = "idempotency_keys"
    key: Mapped[str] = mapped_column(String, primary_key=True)
    scope: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[str] = mapped_column(String)


engine = create_async_engine(settings.database_url, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


TABLE_MODELS: dict[str, type] = {
    "tenants": Tenant,
    "users": User,
    "customers": Customer,
    "leads": Lead,
    "workflows": Workflow,
    "workflow_runs": WorkflowRun,
    "conversations": Conversation,
    "messages": Message,
    "invoices": Invoice,
    "payments": Payment,
    "audit_logs": AuditLog,
}
TENANT_SCOPED_TABLES = {"customers", "leads", "workflows", "conversations", "invoices", "audit_logs"}
GLOBAL_GENERIC_TABLES = {"workflow_runs", "messages", "payments"}


@asynccontextmanager
async def session_scope():
    session = SessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class SqlRepository:
    async def insert(self, table: str, item: Any) -> Any:
        async with session_scope() as session:
            payload = item.model_dump(mode="json")
            if table == "tenants":
                session.add(TenantRecord(id=item.id, payload=payload))
            elif table == "users":
                session.add(UserRecord(id=item.id, tenant_id=item.tenant_id, normalized_email=item.normalized_email, payload=payload))
            elif table in TENANT_SCOPED_TABLES:
                session.add(GenericTenantRecord(table_name=table, entity_id=item.id, tenant_id=item.tenant_id, payload=payload))
            elif table in GLOBAL_GENERIC_TABLES:
                session.add(GenericGlobalRecord(table_name=table, entity_id=item.id, payload=payload))
            else:
                raise KeyError(table)
        return item

    async def get(self, table: str, item_id: str) -> Any | None:
        model = TABLE_MODELS[table]
        async with session_scope() as session:
            if table == "tenants":
                row = await session.get(TenantRecord, item_id)
                return model.model_validate(row.payload) if row else None
            if table == "users":
                row = await session.get(UserRecord, item_id)
                return model.model_validate(row.payload) if row else None
            if table in TENANT_SCOPED_TABLES:
                result = await session.execute(select(GenericTenantRecord).where(GenericTenantRecord.table_name == table, GenericTenantRecord.entity_id == item_id))
                row = result.scalar_one_or_none()
                return model.model_validate(row.payload) if row else None
            result = await session.execute(select(GenericGlobalRecord).where(GenericGlobalRecord.table_name == table, GenericGlobalRecord.entity_id == item_id))
            row = result.scalar_one_or_none()
            return model.model_validate(row.payload) if row else None

    async def list(self, table: str) -> list[Any]:
        model = TABLE_MODELS[table]
        async with session_scope() as session:
            if table == "tenants":
                result = await session.execute(select(TenantRecord))
                return [model.model_validate(row.payload) for row in result.scalars().all()]
            if table == "users":
                result = await session.execute(select(UserRecord))
                return [model.model_validate(row.payload) for row in result.scalars().all()]
            if table in TENANT_SCOPED_TABLES:
                result = await session.execute(select(GenericTenantRecord).where(GenericTenantRecord.table_name == table))
                return [model.model_validate(row.payload) for row in result.scalars().all()]
            result = await session.execute(select(GenericGlobalRecord).where(GenericGlobalRecord.table_name == table))
            return [model.model_validate(row.payload) for row in result.scalars().all()]

    async def filter(self, table: str, **criteria: Any) -> list[Any]:
        return [item for item in await self.list(table) if all(getattr(item, key) == value for key, value in criteria.items())]

    async def get_user_by_normalized_email(self, normalized_email: str) -> User | None:
        async with session_scope() as session:
            result = await session.execute(select(UserRecord).where(UserRecord.normalized_email == normalized_email))
            row = result.scalar_one_or_none()
            return User.model_validate(row.payload) if row else None

    async def update(self, table: str, item_id: str, **fields: Any) -> Any:
        item = await self.get(table, item_id)
        if not item:
            raise KeyError(item_id)
        data = item.model_dump(mode="json")
        data.update(fields)
        updated = TABLE_MODELS[table].model_validate(data)
        async with session_scope() as session:
            if table == "tenants":
                row = await session.get(TenantRecord, item_id)
                row.payload = updated.model_dump(mode="json")
            elif table == "users":
                row = await session.get(UserRecord, item_id)
                row.payload = updated.model_dump(mode="json")
                row.normalized_email = updated.normalized_email
                row.tenant_id = updated.tenant_id
            elif table in TENANT_SCOPED_TABLES:
                result = await session.execute(select(GenericTenantRecord).where(GenericTenantRecord.table_name == table, GenericTenantRecord.entity_id == item_id))
                row = result.scalar_one()
                row.payload = updated.model_dump(mode="json")
                row.tenant_id = updated.tenant_id
            else:
                result = await session.execute(select(GenericGlobalRecord).where(GenericGlobalRecord.table_name == table, GenericGlobalRecord.entity_id == item_id))
                row = result.scalar_one()
                row.payload = updated.model_dump(mode="json")
        return updated

    async def register_failure(self, key: str, ip: str) -> tuple[int, str | None]:
        from datetime import datetime, timedelta, timezone

        async with session_scope() as session:
            state = await session.get(AuthStateRecord, key)
            if not state:
                state = AuthStateRecord(key=key, failure_count=0, locked_until=None, last_ip=ip)
                session.add(state)
            state.failure_count += 1
            state.last_ip = ip
            locked_until = None
            if state.failure_count >= settings.auth_max_failures:
                locked_until = (datetime.now(timezone.utc) + timedelta(seconds=settings.auth_lockout_seconds)).isoformat()
                state.locked_until = locked_until
                state.failure_count = 0
            return state.failure_count, locked_until

    async def clear_failures(self, key: str) -> None:
        async with session_scope() as session:
            state = await session.get(AuthStateRecord, key)
            if state:
                await session.delete(state)

    async def is_locked(self, key: str) -> bool:
        from datetime import datetime, timezone

        async with session_scope() as session:
            state = await session.get(AuthStateRecord, key)
            if not state or not state.locked_until:
                return False
            if datetime.fromisoformat(state.locked_until) <= datetime.now(timezone.utc):
                await session.delete(state)
                return False
            return True

    async def consume_rate_limit(self, key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
        import time

        now = time.time()
        async with session_scope() as session:
            row = await session.get(RateLimitRecord, key)
            if not row or now - row.window_started_at >= window_seconds:
                if not row:
                    row = RateLimitRecord(key=key, window_started_at=now, count=0)
                    session.add(row)
                row.window_started_at = now
                row.count = 0
            if row.count >= limit:
                return False, max(0, limit - row.count)
            row.count += 1
            return True, max(0, limit - row.count)

    async def ensure_idempotency(self, key: str, scope: str, created_at: str) -> bool:
        async with session_scope() as session:
            existing = await session.get(IdempotencyRecord, key)
            if existing:
                return False
            session.add(IdempotencyRecord(key=key, scope=scope, created_at=created_at))
            return True

    async def delete_all(self, table: str) -> None:
        async with session_scope() as session:
            if table == "tenants":
                await session.execute(delete(TenantRecord))
            elif table == "users":
                await session.execute(delete(UserRecord))
            elif table in TENANT_SCOPED_TABLES:
                await session.execute(delete(GenericTenantRecord).where(GenericTenantRecord.table_name == table))
            else:
                await session.execute(delete(GenericGlobalRecord).where(GenericGlobalRecord.table_name == table))


store = SqlRepository()
