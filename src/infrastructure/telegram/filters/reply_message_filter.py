from typing import Optional

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types.base import TelegramObject


class ReplyFilter(BoundFilter):
    key = 'reply'

    def __init__(self, reply: Optional[bool]):
        self.reply = reply

    async def check(self, obj: TelegramObject):
        if self.reply is None:
            return
        if obj.reply_to_message is not None and self.reply is True:
            return True
        elif obj.reply_to_message is None and self.reply is not True:
            return True
