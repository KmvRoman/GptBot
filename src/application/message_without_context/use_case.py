from src.application.common.use_case import UseCase
from src.application.message_without_context.dto import MessageWithoutContextDtoInput, MessageWithoutContextDtoOutput
from src.application.message_without_context.interfaces import DbGateway, RequestToApi
from src.domain.context.entity.constants import Role
from src.domain.context.service.context import ContextService


class CreateMessageWithoutContext(UseCase[MessageWithoutContextDtoInput, MessageWithoutContextDtoOutput]):
    def __init__(
            self,
            db_gateway: DbGateway,
            request_to_api: RequestToApi,
            context_service: ContextService,
    ):
        self.db_gateway = db_gateway
        self.request_to_api = request_to_api
        self.context_service = context_service

    async def __call__(self, data: MessageWithoutContextDtoInput) -> MessageWithoutContextDtoOutput:
        context = self.context_service.create_context(user_id=data.user_id, expire=data.expire_context)
        create_context = await self.db_gateway.create_context(context=context)
        message = self.context_service.create_message(
            role=Role.user, text=data.text, context_id=create_context.id,
        )
        create_message = await self.db_gateway.create_message(message=message)
        response_message_text = await self.request_to_api.without_context(text=data.text)

        response_message = self.context_service.create_message(
            role=Role.assistant, text=response_message_text,
            context_id=create_context.id, reply_to=create_message.id,
        )
        create_answer_message = await self.db_gateway.create_message(message=response_message)

        return MessageWithoutContextDtoOutput(
            user_id=data.user_id,
            context_id=create_context.id,
            text=response_message_text,
            message_question_id=create_message.id,
            message_answer_id=create_answer_message.id,
        )
