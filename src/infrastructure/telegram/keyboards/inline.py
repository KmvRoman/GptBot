from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.domain.user.entity.constants import SubLevelEnum


def choose_rate() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [InlineKeyboardButton(text="100 messages a day for 4.99$", callback_data=SubLevelEnum.low)],
            [InlineKeyboardButton(text="1000 messages a day for 9.99$", callback_data=SubLevelEnum.medium)],
            [InlineKeyboardButton(text="Unlimited messages for 9.99$", callback_data=SubLevelEnum.unlimited)],
        ]
    )
