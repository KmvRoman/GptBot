from aiogram.utils import exceptions
from aiogram import types, Bot
from aiogram import Dispatcher
from loguru import logger

from src.domain.user.exceptions.access import CantSendRequest
from src.infrastructure.adapters.database.exceptions import MessageNotFound


async def errors_handler(update: types.Update, exception: Exception):
    if isinstance(exception, exceptions.CantDemoteChatCreator):
        logger.error(
            f"Can't demote chat creator:{exception}\n\n"
            f"Update:\n{update}")
        return True
    if isinstance(exception, CantSendRequest):
        logger.error(f"Can't send request: {update} {exception}")
        return True
    if isinstance(exception, MessageNotFound):
        logger.error(f"Context not found: {update} {exception}")
        return True
    # if isinstance(exception, exceptions.MessageCantBeDeleted):
    #     await bot.send_message(chat_id=exceptions_group, text=f"<b>Message cant be deleted:</b> <i>{exception}</i>\n\n"
    #                                                           f"<b>Update:</b>\n<code>{update}</code>")
    #     return True
    # if isinstance(exception, exceptions.MessageToDeleteNotFound):
    #     await bot.send_message(chat_id=exceptions_group, text=f"<b>Message to delete not found:</b> <i>{exception}</i>"
    #                                                           f"\n\n<b>Update:</b>\n<code>{update}</code>")
    #     return True
    #
    # if isinstance(exception, exceptions.MessageTextIsEmpty):
    #     await bot.send_message(chat_id=exceptions_group, text=f'<b>MesextIsEmptysageT:</b> <i>{exception}</i>\n\n'
    #                                                           f'<b>Update:</b>\n<code>{update}</code>')
    #     return True
    # if isinstance(exception, exceptions.BotBlocked):
    #     await bot.send_message(chat_id=exceptions_group, text=f'<b>BotBlocked:</b> <i>{exception}</i>\n\n'
    #                                                           f'<b>Update:</b>\n<code>{update}</code>')
    #     return True
    # if isinstance(exception, exceptions.Unauthorized):
    #     await bot.send_message(chat_id=exceptions_group, text=f'<b>Unauthorized:</b> <i>{exception}</i>')
    #     return True
    # if isinstance(exception, exceptions.InvalidQueryID):
    #     await bot.send_message(chat_id=exceptions_group, text=f'<b>InvalidQueryID:</b> <i>{exception}</i>\n\n'
    #                                                           f'<b>Update:</b>\n<code>{update}</code>')
    #     return True
    # if isinstance(exception, exceptions.MessageNotModified):
    #     return True
    # if isinstance(exception, exceptions.TelegramAPIError):
    #     await bot.send_message(chat_id=exceptions_group, text=f'<b>TelegramAPIError:</b> <i>{exception}</i>\n\n'
    #                                                           f'<b>Update:</b>\n<code>{update}</code>')
    #     return True
    # if isinstance(exception, exceptions.RetryAfter):
    #     await bot.send_message(chat_id=exceptions_group, text=f'<b>RetryAfter:</b> <i>{exception}</i>\n\n'
    #                                                           f'<b>Update:</b>\n<code>{update}</code>')
    #     return True
    # if isinstance(exception, exceptions.CantParseEntities):
    #     await bot.send_message(chat_id=exceptions_group, text=f'<b>CantParseEntities:</b> <i>{exception}</i>\n\n'
    #                                                           f'<b>Update:</b>\n<code>{update}</code>')
    #     return True
    # if isinstance(exception, exceptions.MessageCantBeEdited):
    #     await bot.send_message(chat_id=exceptions_group, text=f'<b>MessageCantBeEdited:</b> <i>{exception}</i>\n\n'
    #                                                           f'<b>Update:</b>\n<code>{update}</code>')
    #     return True
    # else:
    #     await bot.send_message(chat_id=exceptions_group,
    #                            text=f"<b>NOT CATCHED ERROR!</b>\n\n"
    #                                 f"<i>Exception:</i> <b>{exception}</b>\n\n<code>{update}</code>")
    #     return True


def register_handlers_error(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
