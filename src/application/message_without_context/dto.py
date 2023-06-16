from dataclasses import dataclass
from datetime import datetime

from src.domain.context.entity.context import MessageId, ContextId
from src.domain.user.entity.user import UserId


@dataclass
class MessageWithoutContextDtoInput:
    user_id: UserId
    text: str
    expire_context: datetime


@dataclass
class MessageWithoutContextDtoOutput:
    user_id: UserId
    context_id: ContextId
    message_question_id: MessageId
    message_answer_id: MessageId
    text: str
