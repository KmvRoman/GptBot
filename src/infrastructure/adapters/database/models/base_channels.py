from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey

from src.infrastructure.adapters.database.models.base import Base


class Channel(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
