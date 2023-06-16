from loguru import logger
from src.application.available_user.dto import CheckUserDtoInput
from src.application.available_user.exceptions import UserNotExist
from src.application.check_follow_to_channel.dto import CheckFollowDtoInput
from src.application.message_without_context.dto import MessageWithoutContextDtoInput
from src.application.remote_limit.dto import CheckLimitDtoInput
from src.application.send_message.dto import SendMessageDTOInput
from src.application.user_create.dto import UserCreateDtoInput
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.mediator.send_message_without_context.dto import SendMessageWithoutContextDtoInput


async def send_message_without_context(
        data: SendMessageWithoutContextDtoInput,
        ioc: InteractorFactory,
):
    check_follow = await ioc.check_follow_to_channel()
    available = await ioc.check_available()
    limit_remote = await ioc.remote_limit()
    message_without_context = await ioc.message_without_context()
    messenger_message_saver = await ioc.send_message()
    try:
        available_data = await available(data=CheckUserDtoInput(messenger_user_id=data.messenger_user_id, name=data.name))
    except UserNotExist:
        create_user = await ioc.create_user()
        user = await create_user(data=UserCreateDtoInput(
                messenger_user_id=data.messenger_user_id,
                name=data.name,
                limit_expire=data.datetime_now,
            ),
        )
        logger.error(
            f"User not exists telegram user_id = {data.messenger_user_id}. "
            f"User created UserId = {user.user_id}"
        )
        await ioc.commit()
        return user
    await check_follow(data=CheckFollowDtoInput(messenger_user_id=data.messenger_user_id))
    await limit_remote(data=CheckLimitDtoInput(user_id=available_data.user_id, datetime_now=data.datetime_now))
    message_action = await message_without_context(
        data=MessageWithoutContextDtoInput(
            user_id=available_data.user_id,
            text=data.text,
            expire_context=data.datetime_now,
        ),
    )
    await messenger_message_saver(
        data=SendMessageDTOInput(
            messenger_user_id=data.messenger_user_id,
            message_question_id=message_action.message_question_id,
            message_question_messenger_id=data.messenger_message_id,
            message_answer_id=message_action.message_answer_id,
            context_id=message_action.context_id,
            text=message_action.text,
        ),
    )
    await ioc.commit()
