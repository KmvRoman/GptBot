from dataclasses import dataclass

from src.domain.context.entity.context import MessageId, ContextId


@dataclass
class MessengerMessageDtoInput:
    messenger_message_id: int


@dataclass
class MessengerMessageDtoOutput:
    message_id: MessageId
    context_id: ContextId
