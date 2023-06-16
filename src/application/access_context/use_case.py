from src.application.access_context.dto import AccessContextDtoInput
from src.application.access_context.interfaces import DbGateway
from src.application.common.use_case import UseCase
from src.domain.context.service.access import ContextAccessService


class AccessContext(UseCase[AccessContextDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, context_access_service: ContextAccessService):
        self.db_gateway = db_gateway
        self.context_access_service = context_access_service

    async def __call__(self, data: AccessContextDtoInput) -> None:
        messages = await self.db_gateway.get_messages(context_id=data.context_id)
        context = await self.db_gateway.get_context(context_id=data.context_id)
        self.context_access_service.can_continue_context(context=context, datetime_now=data.datetime_now)
        self.context_access_service.is_context_full(contexts_messages=messages)
