from src.application.available_user.dto import CheckUserDtoInput
from src.application.set_rate.dto import SetRateDtoInput
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.mediator.change_rate.dto import ChangeRateDtoInput, ChangeRateDtoOutput


async def change_rate(data: ChangeRateDtoInput, ioc: InteractorFactory) -> ChangeRateDtoOutput:
    available = await ioc.check_available()
    rate = await ioc.set_rate()

    available_data = await available(
        data=CheckUserDtoInput(
            messenger_user_id=data.messenger_user_id,
            name=data.name,
        ),
    )
    set_rate = await rate(
        data=SetRateDtoInput(
            user_id=available_data.user_id,
            rate=data.rate,
            datetime_now=data.datetime_now,
        ),
    )
    await ioc.commit()
    return ChangeRateDtoOutput(user_id=set_rate.user_id, rate=set_rate.rate)
