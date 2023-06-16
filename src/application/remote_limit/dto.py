from dataclasses import dataclass
from datetime import datetime

from src.domain.user.entity.user import UserId


@dataclass
class CheckLimitDtoInput:
    user_id: UserId
    datetime_now: datetime
