from src.application.common.use_case import UseCase
from src.application.remote_limit.dto import CheckLimitDtoInput
from src.application.remote_limit.interfaces import DbGateway
from src.domain.user.services.access import SubscriptionAccessService
from src.domain.user.services.subscription import SubscriptionService


class CreateLimit(UseCase[CheckLimitDtoInput, None]):
    def __init__(
            self, db_gateway: DbGateway, access_send_service: SubscriptionAccessService,
            subscription_service: SubscriptionService,
    ):
        self.db_gateway = db_gateway
        self.subscription_service = subscription_service
        self.access_send_service = access_send_service

    async def __call__(self, data: CheckLimitDtoInput) -> None:
        subscription = await self.db_gateway.get_subscription(user_id=data.user_id)
        self.subscription_service.give_limit(subscription=subscription, datetime_now=data.datetime_now)
        self.access_send_service.can_send_request(subscription=subscription, datetime_now=data.datetime_now)
        self.subscription_service.waste_request(subscription=subscription)
        await self.db_gateway.refresh_limit(subscription=subscription)
