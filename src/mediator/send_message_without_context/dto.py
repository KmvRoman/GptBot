from dataclasses import dataclass
from datetime import datetime


@dataclass
class SendMessageWithoutContextDtoInput:
    messenger_user_id: int
    messenger_message_id: int
    name: str
    datetime_now: datetime
    text: str
