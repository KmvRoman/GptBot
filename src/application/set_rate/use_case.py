from src.application.common.use_case import UseCase
from src.application.set_rate.dto import SetRateDtoInput, SetRateDtoOutput
from src.application.set_rate.interfaces import DbGateway
from src.domain.user.services.subscription import SubscriptionService


class SetRate(UseCase[SetRateDtoInput, SetRateDtoOutput]):
    def __init__(self, db_gateway: DbGateway, subscription_service: SubscriptionService):
        self.db_gateway = db_gateway
        self.subscription_service = subscription_service

    async def __call__(self, data: SetRateDtoInput) -> SetRateDtoOutput:
        subscription = self.subscription_service.give_rate(
            sub_level=data.rate, user_id=data.user_id,
            datetime_now=data.datetime_now,
        )
        await self.db_gateway.create_subscription(subscription=subscription)
        return SetRateDtoOutput(user_id=data.user_id, rate=data.rate)
