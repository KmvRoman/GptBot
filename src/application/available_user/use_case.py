from src.application.available_user.dto import CheckUserDtoInput, UserDtoOutput
from src.application.available_user.exceptions import UserNotExist
from src.application.available_user.interfaces import DbGateway
from src.application.common.use_case import UseCase
from src.domain.user.services.user import UserService


class AvailableUser(UseCase[CheckUserDtoInput, UserDtoOutput]):
    def __init__(
            self,
            db_gateway: DbGateway,
            user_service: UserService,
    ):
        self.db_gateway = db_gateway
        self.user_service = user_service

    async def __call__(self, data: CheckUserDtoInput) -> UserDtoOutput:
        user_id = await self.db_gateway.get_messenger_user(messenger_user_id=data.messenger_user_id)
        if user_id:
            return UserDtoOutput(user_id=user_id)
        raise UserNotExist()
