from dataclasses import dataclass
from src.domain.context.entity.context import ContextId, MessageId


@dataclass
class SendMessageDTOInput:
    messenger_user_id: int
    context_id: ContextId
    message_question_id: MessageId
    message_question_messenger_id: int
    message_answer_id: MessageId
    text: str
