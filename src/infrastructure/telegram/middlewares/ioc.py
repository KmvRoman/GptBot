from aiogram import Bot
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiohttp import ClientSession

from src.infrastructure.adapters.database.repositories.user_repository import UserRepository
from src.infrastructure.config.config import Config
from src.infrastructure.ioc.ioc import IoC


class IoCMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, repo: UserRepository, bot: Bot, config: Config, aiohttp_session: ClientSession):
        super().__init__()
        self.repo = repo
        self.bot = bot
        self.config = config
        self.session = aiohttp_session

    async def pre_process(self, obj, data, *args):
        data["ioc"] = IoC(
            repo=self.repo,
            bot=self.bot,
            aiohttp_session=self.session,
            config=self.config,
        )

    async def post_process(self, obj, data, *args):
        del data["ioc"]
