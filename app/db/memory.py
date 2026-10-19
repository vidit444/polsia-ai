from __future__ import annotations

from threading import RLock
from typing import Any


class InMemoryStore:
    def __init__(self) -> None:
        self.lock = RLock()
        self.tables: dict[str, dict[str, Any]] = {
            "tenants": {},
            "users": {},
            "customers": {},
            "leads": {},
            "workflows": {},
            "workflow_runs": {},
            "ai_agents": {},
            "conversations": {},
            "messages": {},
            "invoices": {},
            "payments": {},
            "audit_logs": {},
            "rate_limits": {},
        }

    def insert(self, table: str, item: Any) -> Any:
        with self.lock:
            self.tables[table][item.id] = item
            return item

    def get(self, table: str, item_id: str) -> Any | None:
        return self.tables[table].get(item_id)

    def list(self, table: str) -> list[Any]:
        return list(self.tables[table].values())

    def update(self, table: str, item_id: str, **fields: Any) -> Any:
        with self.lock:
            item = self.tables[table][item_id]
            for key, value in fields.items():
                setattr(item, key, value)
            return item

    def filter(self, table: str, **criteria: Any) -> list[Any]:
        result = []
        for item in self.tables[table].values():
            if all(getattr(item, key) == value for key, value in criteria.items()):
                result.append(item)
        return result


store = InMemoryStore()
