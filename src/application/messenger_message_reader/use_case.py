from src.application.common.use_case import UseCase
from src.application.messenger_message_reader.dto import MessengerMessageDtoInput, MessengerMessageDtoOutput
from src.application.messenger_message_reader.interfaces import DbGateway


class MessengerMessageToMessage(UseCase[MessengerMessageDtoInput, MessengerMessageDtoOutput]):
    def __init__(
            self,
            db_gateway: DbGateway,
    ):
        self.db_gateway = db_gateway

    async def __call__(self, data: MessengerMessageDtoInput) -> MessengerMessageDtoOutput:
        message = await self.db_gateway.get_messenger_message(messenger_message_id=data.messenger_message_id)
        return MessengerMessageDtoOutput(message_id=message.id, context_id=message.context_id)
