from dataclasses import dataclass
from datetime import datetime

from src.domain.user.entity.user import UserId


@dataclass
class UserCreateDtoInput:
    messenger_user_id: int
    name: str
    limit_expire: datetime


@dataclass
class UserCreateDtoOutput:
    user_id: UserId
