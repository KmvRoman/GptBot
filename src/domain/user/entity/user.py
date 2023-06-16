from dataclasses import dataclass
from datetime import datetime
from typing import NewType, Optional

from src.domain.user.entity.constants import SubLevelEnum

UserId = NewType("UserId", int)


@dataclass
class User:
    id: UserId
    name: str


@dataclass
class SubscriptionLimit:
    limit: Optional[int]
    expire_at: Optional[datetime]


@dataclass
class Subscription:
    user_id: UserId
    level: SubLevelEnum
    expire_at: Optional[datetime]
    limit: SubscriptionLimit
