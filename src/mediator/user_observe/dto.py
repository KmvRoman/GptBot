from dataclasses import dataclass
from datetime import date


@dataclass
class UserStartCommandDtoInput:
    messenger_user_id: int
    name: str
    limit_expire: date
