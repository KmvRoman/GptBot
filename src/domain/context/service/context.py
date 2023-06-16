from datetime import datetime, timedelta
from typing import Optional

from src.domain.context.entity.constants import Role
from src.domain.context.entity.context import MessageId, Message, Context, ContextId
from src.domain.user.entity.user import UserId


class ContextService:
    def create_message(
            self, role: Role, text: str, context_id: ContextId, reply_to: Optional[MessageId] = None,
    ) -> Message:
        return Message(
            id=None,
            role=role,
            text=text,
            context_id=context_id,
            reply_to=reply_to,
        )

    def create_context(
            self, user_id: UserId, expire: datetime,
    ) -> Context:
        return Context(
            id=None,
            user_id=user_id,
            expire=expire + timedelta(days=1),
        )
