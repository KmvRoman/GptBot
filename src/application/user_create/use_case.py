from src.application.common.use_case import UseCase
from src.application.user_create.dto import UserCreateDtoInput, UserCreateDtoOutput
from src.application.user_create.interfaces import DbGateway
from src.domain.user.entity.constants import SubLevelEnum
from src.domain.user.services.subscription import SubscriptionService
from src.domain.user.services.user import UserService


class CreateUser(UseCase[UserCreateDtoInput, UserCreateDtoOutput]):
    def __init__(
            self,
            db_gateway: DbGateway,
            user_service: UserService,
            subscription_service: SubscriptionService,
    ):
        self.db_gateway = db_gateway
        self.user_service = user_service
        self.subscription_service = subscription_service

    async def __call__(self, data: UserCreateDtoInput) -> UserCreateDtoOutput:
        user = self.user_service.create_user(name=data.name)
        user_create = await self.db_gateway.create_user(user=user)
        await self.db_gateway.create_messenger_user(
            user_id=user_create.id, messenger_user_id=data.messenger_user_id,
        )
        subscription = self.subscription_service.give_rate(
            sub_level=SubLevelEnum.free, user_id=user_create.id, datetime_now=data.limit_expire,
        )
        await self.db_gateway.create_subscription(subscription=subscription)
        return UserCreateDtoOutput(user_id=user_create.id)
