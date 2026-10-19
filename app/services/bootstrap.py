from sqlalchemy.engine import Connection

from app.models.base import Base
from app.db import base  # noqa: F401


class BootstrapService:
    @staticmethod
    def create_schema(connection: Connection) -> None:
        Base.metadata.create_all(bind=connection)
