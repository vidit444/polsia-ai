from app.db.memory import store
from app.models.domain import AuditLog


def record_audit_log(tenant_id: str, actor_id: str | None, action: str, entity_type: str, entity_id: str, ip: str | None = None) -> AuditLog:
    log = AuditLog(tenant_id=tenant_id, actor_id=actor_id, action=action, entity_type=entity_type, entity_id=entity_id, ip=ip)
    store.insert("audit_logs", log)
    return log
