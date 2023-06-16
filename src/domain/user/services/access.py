from datetime import datetime

from src.domain.user.entity.constants import SubLevelEnum
from src.domain.user.entity.user import Subscription
from src.domain.user.exceptions.access import CantSendRequest


class SubscriptionAccessService:
    def can_send_request(self, subscription: Subscription, datetime_now: datetime):
        if subscription.level == SubLevelEnum.unlimited:
            return
        if subscription.level != SubLevelEnum.free:
            if subscription.expire_at < datetime_now:
                raise CantSendRequest()
        if subscription.limit.limit > 0:
            return
        raise CantSendRequest()
