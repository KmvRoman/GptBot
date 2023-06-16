from src.application.common.use_case import UseCase
from src.application.message_with_context.dto import MessageWithContextDtoInput, MessageWithContextDtoOutput
from src.application.message_with_context.interfaces import DbGateway, RequestToApi
from src.domain.context.entity.constants import Role
from src.domain.context.service.context import ContextService


class CreateMessageWithContext(UseCase[MessageWithContextDtoInput, MessageWithContextDtoOutput]):
    def __init__(
            self,
            db_gateway: DbGateway,
            request_to_api: RequestToApi,
            context_service: ContextService,
    ):
        self.db_gateway = db_gateway
        self.request_to_api = request_to_api
        self.context_service = context_service

    async def __call__(self, data: MessageWithContextDtoInput) -> MessageWithContextDtoOutput:
        message = self.context_service.create_message(
            role=Role.user, text=data.text, context_id=data.context_id, reply_to=data.reply_to,
        )
        create_message = await self.db_gateway.create_message(message=message)
        messages = await self.db_gateway.get_messages(context_id=data.context_id)
        response_message_text = await self.request_to_api.with_context(messages=messages)

        response_message = self.context_service.create_message(
            role=Role.assistant, text=response_message_text,
            context_id=data.context_id, reply_to=create_message.id,
        )
        create_response_message = await self.db_gateway.create_message(message=response_message)

        return MessageWithContextDtoOutput(
            user_id=data.user_id,
            message_question_id=create_message.id,
            message_answer_id=create_response_message.id,
            text=response_message_text,
        )
