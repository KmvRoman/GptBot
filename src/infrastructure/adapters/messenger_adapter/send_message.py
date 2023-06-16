from aiogram import Bot

from src.application.check_follow_to_channel.constants import UserChannelStatus


class MessengerAdapter:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_message(self, chat_id: int, text: str, reply_to_message: int) -> int:
        message = await self.bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_to_message)
        return message.message_id

    async def get_member(self, chat_id: int, user_id: int) -> UserChannelStatus:
        member = await self.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member.status
