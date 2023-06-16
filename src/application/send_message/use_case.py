from src.application.common.use_case import UseCase
from src.application.send_message.dto import SendMessageDTOInput
from src.application.send_message.interfaces import DbGateway, MessengerGateway
from src.domain.context.entity.constants import Role
from src.domain.context.service.context import ContextService


class SendMessage(UseCase[SendMessageDTOInput, None]):
    def __init__(
            self,
            db_gateway: DbGateway,
            messenger_gateway: MessengerGateway,
            context_service: ContextService,
    ):
        self.db_gateway = db_gateway
        self.messenger_gateway = messenger_gateway
        self.context_service = context_service

    async def __call__(self, data: SendMessageDTOInput) -> None:
        await self.db_gateway.create_messenger_message(
            message_id=data.message_question_id, messenger_message_id=data.message_question_messenger_id,
        )
        # message = self.context_service.create_message(role=Role.assistant, text=data.text, context_id=data.context_id)
        # create_message = await self.db_gateway.create_message(message=message)
        messenger_message_id = await self.messenger_gateway.send_message(
            chat_id=data.messenger_user_id, text=data.text, reply_to_message=data.message_question_messenger_id,
        )
        await self.db_gateway.create_messenger_message(
            message_id=data.message_answer_id, messenger_message_id=messenger_message_id,
        )
