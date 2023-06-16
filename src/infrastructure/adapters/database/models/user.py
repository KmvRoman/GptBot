from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, VARCHAR

from src.infrastructure.adapters.database.models.base import Base


class SystemUser(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(25), nullable=False)
