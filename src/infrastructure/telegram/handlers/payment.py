from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.infrastructure.ioc.interfaces import InteractorFactory
from src.infrastructure.telegram.keyboards.inline import choose_rate
from src.infrastructure.telegram.states.user import Payment
from src.mediator.change_rate.dto import ChangeRateDtoInput
from src.mediator.change_rate.service import change_rate


async def get_rates(message: types.Message, bot: Bot, state: FSMContext):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Вы можете оплатить наши услуги по таким расценкам:\n",
        reply_markup=choose_rate(),
    )
    await state.set_state(state=Payment.start_payment)


async def change_rate_payment(call: types.CallbackQuery, bot: Bot, ioc: InteractorFactory, state: FSMContext):
    response = await change_rate(
        ioc=ioc,
        data=ChangeRateDtoInput(
            messenger_user_id=call.from_user.id,
            name=call.from_user.first_name,
            rate=call.data,
            datetime_now=datetime.now(),
        ),
    )
    await bot.edit_message_text(
        chat_id=call.from_user.id, message_id=call.message.message_id,
        text=f"Rate was changed on {response.rate}",
    )
    await state.finish()


def register_payment_handlers(dp: Dispatcher):
    dp.register_message_handler(get_rates, content_types=types.ContentTypes.TEXT, commands=["payment"])
    dp.register_callback_query_handler(change_rate_payment, state=Payment.start_payment)
