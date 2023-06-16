from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from src.application.available_user.exceptions import UserNotExist
from src.application.check_follow_to_channel.exceptions import UserNotFollowed
from src.domain.context.exceptions.access import ContextExpired, ContextIsFull
from src.domain.user.exceptions.access import CantSendRequest
from src.infrastructure.adapters.database.exceptions import MessageNotFound
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.infrastructure.openai.chat_completion.exceptions import SomethingWentWrong
from src.mediator.send_message_with_context.dto import SendMessageWithContextDtoInput
from src.mediator.send_message_with_context.service import send_message_with_context
from src.mediator.send_message_without_context.dto import SendMessageWithoutContextDtoInput
from src.mediator.send_message_without_context.service import send_message_without_context
from src.mediator.user_observe.dto import UserStartCommandDtoInput
from src.mediator.user_observe.service import get_user_or_create


async def start_command(message: types.Message, bot: Bot, ioc: InteractorFactory):
    await get_user_or_create(
        ioc=ioc,
        data=UserStartCommandDtoInput(
            messenger_user_id=message.from_user.id,
            name=message.from_user.first_name,
            limit_expire=datetime.now(),
        ),
    )
    await bot.send_message(chat_id=message.from_user.id, text="Hi!")


async def without_context_message(message: types.Message, bot: Bot, ioc: InteractorFactory):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    try:
        user = await send_message_without_context(
            ioc=ioc,
            data=SendMessageWithoutContextDtoInput(
                messenger_user_id=message.from_user.id,
                messenger_message_id=message.message_id,
                name=message.from_user.first_name,
                datetime_now=datetime.now(),
                text=message.text,
            ),
        )
        if user:
            await bot.send_message(chat_id=message.from_user.id, text="Добро пожаловать!")
    except CantSendRequest:
        await bot.send_message(chat_id=message.from_user.id, text="У вас закончились лимиты!")
    except UserNotExist:
        await bot.send_message(chat_id=message.from_user.id, text="Нажмите старт для регистрации")
    except UserNotFollowed:
        await bot.send_message(chat_id=message.from_user.id, text="Вы не подписались на каналы!")
    except SomethingWentWrong:
        await bot.send_message(chat_id=message.from_user.id, text="Пожалуйста повторите вопрос")


async def with_context_message(message: types.Message, bot: Bot, ioc: InteractorFactory):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    try:
        user = await send_message_with_context(
            ioc=ioc,
            data=SendMessageWithContextDtoInput(
                messenger_user_id=message.from_user.id,
                messenger_message_id=message.message_id,
                messenger_message_id_reply=message.reply_to_message.message_id,
                name=message.from_user.first_name,
                datetime_now=datetime.now(),
                text=message.text,
            ),
        )
        if user:
            await bot.send_message(chat_id=message.from_user.id, text="Добро пожаловать!")
    except ContextExpired:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Время жизни контекста истекло",
        )
    except ContextIsFull:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Контекст переполнен пожалуйста начните новый",
        )
    except CantSendRequest:
        await bot.send_message(chat_id=message.from_user.id, text="У вас закончились лимиты!")
    except UserNotExist:
        await bot.send_message(chat_id=message.from_user.id, text="Нажмите старт для регистрации")
    except UserNotFollowed:
        await bot.send_message(chat_id=message.from_user.id, text="Вы не подписались на каналы!")
    except SomethingWentWrong:
        await bot.send_message(chat_id=message.from_user.id, text="Пожалуйста повторите вопрос")
    except MessageNotFound:
        await bot.send_message(
            chat_id=message.from_user.id, text="Это сообщение недоступно для контекста, отметьте другое",
        )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, content_types=types.ContentTypes.TEXT, commands=["start"])
    dp.register_message_handler(without_context_message, content_types=types.ContentTypes.TEXT, reply=False)
    dp.register_message_handler(with_context_message, content_types=types.ContentTypes.TEXT, reply=True)
