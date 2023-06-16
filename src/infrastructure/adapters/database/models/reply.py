from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey
from src.infrastructure.adapters.database.models.base import Base


class Reply(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    message_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="dialogmessages.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    reply_to: Mapped[int] = mapped_column(BIGINT, nullable=False)
