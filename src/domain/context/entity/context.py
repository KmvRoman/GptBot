from dataclasses import dataclass
from datetime import datetime
from typing import NewType, Optional

from src.domain.context.entity.constants import Role
from src.domain.user.entity.user import UserId

MessageId = NewType(name="MessageId", tp=int)
ContextId = NewType(name="ContextId", tp=int)


@dataclass
class Message:
    id: MessageId
    role: Role
    text: str
    context_id: ContextId
    reply_to: Optional[MessageId]


@dataclass
class Context:
    id: ContextId
    user_id: UserId
    expire: datetime
