from dataclasses import dataclass
from datetime import datetime


@dataclass
class SendMessageWithContextDtoInput:
    messenger_user_id: int
    messenger_message_id: int
    messenger_message_id_reply: int
    name: str
    datetime_now: datetime
    text: str
