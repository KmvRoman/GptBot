from datetime import timedelta, datetime

from src.domain.user.entity.constants import SubLevelEnum, MessageCount
from src.domain.user.entity.user import Subscription, UserId, SubscriptionLimit


class SubscriptionService:
    def give_rate(self, sub_level: SubLevelEnum, user_id: UserId, datetime_now: datetime = None) -> Subscription:
        if sub_level == SubLevelEnum.low:
            expire_at = datetime_now + timedelta(days=30)
        elif sub_level == SubLevelEnum.medium:
            expire_at = datetime_now + timedelta(days=30)
        elif sub_level == SubLevelEnum.unlimited:
            expire_at = datetime_now + timedelta(days=30)
        else:
            expire_at = None
        return Subscription(
            user_id=user_id,
            level=sub_level,
            expire_at=expire_at,
            limit=self._rate_limit(sub_level=sub_level, datetime_now=datetime_now),
        )

    def waste_request(self, subscription: Subscription):
        if subscription.level != SubLevelEnum.unlimited:
            subscription.limit.limit = subscription.limit.limit - 1

    def give_limit(self, subscription: Subscription, datetime_now: datetime):
        if subscription.level == SubLevelEnum.unlimited:
            subscription.limit = None
        elif subscription.limit.expire_at < datetime_now:
            subscription.limit = self._rate_limit(sub_level=subscription.level, datetime_now=datetime_now)

    def _rate_limit(self, sub_level: SubLevelEnum, datetime_now: datetime) -> SubscriptionLimit:
        if sub_level == SubLevelEnum.free:
            return SubscriptionLimit(limit=MessageCount.free.value, expire_at=datetime_now + timedelta(days=1))
        elif sub_level == SubLevelEnum.low:
            return SubscriptionLimit(limit=MessageCount.low.value, expire_at=datetime_now + timedelta(days=1))
        elif sub_level == SubLevelEnum.medium:
            return SubscriptionLimit(limit=MessageCount.medium.value, expire_at=datetime_now + timedelta(days=1))
