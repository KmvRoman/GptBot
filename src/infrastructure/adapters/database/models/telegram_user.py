from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey

from src.infrastructure.adapters.database.models.base import Base


class TelegramUser(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="systemusers.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    telegram_user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
