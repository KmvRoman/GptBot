from src.application.available_user.dto import CheckUserDtoInput
from src.application.available_user.exceptions import UserNotExist
from src.application.user_create.dto import UserCreateDtoInput
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.mediator.user_observe.dto import UserStartCommandDtoInput
from loguru import logger


async def get_user_or_create(ioc: InteractorFactory, data: UserStartCommandDtoInput):
    try:
        user_available = await ioc.check_available()
        user = await user_available(
            data=CheckUserDtoInput(messenger_user_id=data.messenger_user_id, name=data.name)
        )
        logger.info(f"User existed UserId = {user.user_id}")
    except UserNotExist:
        user = await (await ioc.create_user())(
            data=UserCreateDtoInput(
                messenger_user_id=data.messenger_user_id,
                name=data.name,
                limit_expire=data.limit_expire,
            )
        )
        logger.error(
            f"User not exists telegram user_id = {data.messenger_user_id}. "
            f"User created UserId = {user.user_id}"
        )
        await ioc.commit()
