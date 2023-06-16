from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import INTEGER, BIGINT, Identity, ForeignKey
from src.infrastructure.adapters.database.models.base import Base


class Limit(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    subscription_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="usersubscriptions.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    limit: Mapped[int] = mapped_column(INTEGER, nullable=False)
