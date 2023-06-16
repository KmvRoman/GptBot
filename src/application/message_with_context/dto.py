from dataclasses import dataclass
from src.domain.context.entity.context import ContextId, MessageId
from src.domain.user.entity.user import UserId


@dataclass
class MessageWithContextDtoInput:
    user_id: UserId
    context_id: ContextId
    text: str
    reply_to: MessageId


@dataclass
class MessageWithContextDtoOutput:
    user_id: UserId
    message_question_id: MessageId
    message_answer_id: MessageId
    text: str
