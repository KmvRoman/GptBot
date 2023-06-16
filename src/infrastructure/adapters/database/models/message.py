from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey, VARCHAR

from src.domain.context.entity.constants import Role
from src.infrastructure.adapters.database.models.base import Base


class DialogMessage(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    context_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="messagecontexts.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    role: Mapped[Role] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(VARCHAR(3000), nullable=False)
