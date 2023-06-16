from loguru import logger
from src.application.access_context.dto import AccessContextDtoInput
from src.application.available_user.dto import CheckUserDtoInput
from src.application.available_user.exceptions import UserNotExist
from src.application.check_follow_to_channel.dto import CheckFollowDtoInput
from src.application.message_with_context.dto import MessageWithContextDtoInput
from src.application.messenger_message_reader.dto import MessengerMessageDtoInput
from src.application.remote_limit.dto import CheckLimitDtoInput
from src.application.send_message.dto import SendMessageDTOInput
from src.application.user_create.dto import UserCreateDtoInput
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.mediator.send_message_with_context.dto import SendMessageWithContextDtoInput


async def send_message_with_context(
        ioc: InteractorFactory,
        data: SendMessageWithContextDtoInput,
):
    check_follow = await ioc.check_follow_to_channel()
    available_user = await ioc.check_available()
    limit_remote = await ioc.remote_limit()
    message_reader = await ioc.messenger_message_reader()
    access_context = await ioc.access_context()
    message_with_context = await ioc.message_with_context()
    messenger_message_saver = await ioc.send_message()

    try:
        available_data = await available_user(
            data=CheckUserDtoInput(messenger_user_id=data.messenger_user_id, name=data.name),
        )
    except UserNotExist:
        create_user = await ioc.create_user()
        user = await create_user(
            UserCreateDtoInput(
                messenger_user_id=data.messenger_user_id,
                name=data.name,
                limit_expire=data.datetime_now,
            )
        )
        logger.error(
            f"User not exists telegram user_id = {data.messenger_user_id}. "
            f"User created UserId = {user.user_id}"
        )
        await ioc.commit()
        return user
    await check_follow(data=CheckFollowDtoInput(messenger_user_id=data.messenger_user_id))
    await limit_remote(data=CheckLimitDtoInput(user_id=available_data.user_id, datetime_now=data.datetime_now))
    messenger_reader = await message_reader(
        data=MessengerMessageDtoInput(messenger_message_id=data.messenger_message_id_reply),
    )
    await access_context(data=AccessContextDtoInput(
        context_id=messenger_reader.context_id, datetime_now=data.datetime_now),
    )
    message_action = await message_with_context(
        data=MessageWithContextDtoInput(
            user_id=available_data.user_id, context_id=messenger_reader.context_id,
            text=data.text, reply_to=messenger_reader.message_id,
        ),
    )
    await messenger_message_saver(data=SendMessageDTOInput(
        messenger_user_id=data.messenger_user_id,
        message_question_id=message_action.message_question_id,
        message_question_messenger_id=data.messenger_message_id,
        message_answer_id=message_action.message_answer_id,
        context_id=messenger_reader.context_id,
        text=message_action.text,
    ),
    )
    await ioc.commit()
