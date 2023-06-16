from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey, TIMESTAMP
from src.infrastructure.adapters.database.models.base import Base


class LimitExpire(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    limit_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="limits.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    expire_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
