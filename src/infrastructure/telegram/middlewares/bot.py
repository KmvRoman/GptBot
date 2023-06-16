from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram import Bot, types

from src.infrastructure.adapters.database.repositories.user_repository import UserRepository


class BotMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def pre_process(self, obj, data, *args):
        data["bot"] = self.bot

    async def post_process(self, obj, data, *args):
        del data["bot"]
