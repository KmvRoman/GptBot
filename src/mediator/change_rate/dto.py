from dataclasses import dataclass
from datetime import datetime

from src.domain.user.entity.constants import SubLevelEnum
from src.domain.user.entity.user import UserId


@dataclass
class ChangeRateDtoInput:
    messenger_user_id: int
    name: str
    rate: SubLevelEnum
    datetime_now: datetime


@dataclass
class ChangeRateDtoOutput:
    user_id: UserId
    rate: SubLevelEnum
