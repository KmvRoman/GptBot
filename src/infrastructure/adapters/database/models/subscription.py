from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey

from src.domain.user.entity.constants import SubLevelEnum
from src.infrastructure.adapters.database.models.base import Base


class UserSubscription(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="systemusers.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    level: Mapped[SubLevelEnum] = mapped_column(nullable=False)
