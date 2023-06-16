from dataclasses import dataclass
from datetime import datetime

from src.domain.user.entity.constants import SubLevelEnum
from src.domain.user.entity.user import UserId


@dataclass
class SetRateDtoInput:
    user_id: UserId
    rate: SubLevelEnum
    datetime_now: datetime


@dataclass
class SetRateDtoOutput:
    user_id: UserId
    rate: SubLevelEnum
