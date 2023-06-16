import asyncio

from aiohttp import ClientSession
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.infrastructure.adapters.database.db_adapter.database_adapter import DatabaseAdapter
from src.infrastructure.adapters.database.repositories.user_repository import UserRepository
from src.infrastructure.config.parse_config import load_config, BASE_DIR
from src.infrastructure.telegram.catching_errors.catch_errors import register_handlers_error
from src.infrastructure.telegram.filters.reply_message_filter import ReplyFilter
from src.infrastructure.telegram.handlers.payment import register_payment_handlers
from src.infrastructure.telegram.handlers.user import register_handlers
from src.infrastructure.telegram.middlewares.bot import BotMiddleware
from src.infrastructure.telegram.middlewares.ioc import IoCMiddleware
from src.infrastructure.telegram.middlewares.throttling import ThrottlingMiddleware


async def main():
    logger.add("logs/file.log", rotation="12:00")
    config = load_config(path=BASE_DIR / "infrastructure" / "config" / "config.yaml")
    engine = create_async_engine(url=config.database.connection_uri)
    session_make = sessionmaker(  # NOQA
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    aiohttp_session = ClientSession()
    repo = UserRepository(session_or_pool=session_make)
    adapter = DatabaseAdapter(repo=repo)
    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)
    dp.middleware.setup(middleware=BotMiddleware(bot=bot))
    dp.middleware.setup(
        middleware=IoCMiddleware(
            repo=adapter, bot=bot, config=config, aiohttp_session=aiohttp_session,
        ),
    )
    dp.middleware.setup(middleware=ThrottlingMiddleware())
    dp.filters_factory.bind(ReplyFilter)
    register_payment_handlers(dp=dp)
    register_handlers(dp=dp)
    register_handlers_error(dp=dp)
    try:
        logger.debug("Start polling")
        await dp.start_polling(
            allowed_updates=[
                *types.AllowedUpdates.MESSAGE,
                *types.AllowedUpdates.CALLBACK_QUERY,
                *types.AllowedUpdates.CHAT_MEMBER,
            ]
        )
    finally:
        await engine.dispose()
        await aiohttp_session.close()
        session = await bot.get_session()
        await session.close()
        await storage.close()


def cli():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug("Keyboard Interrupt")
    finally:
        logger.debug("Bot stopped")


if __name__ == '__main__':
    cli()
