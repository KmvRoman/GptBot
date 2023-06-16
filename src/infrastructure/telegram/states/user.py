from aiogram.dispatcher.filters.state import StatesGroup, State


class Payment(StatesGroup):
    start_payment = State()
